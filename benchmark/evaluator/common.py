"""Shared deterministic helpers for the public benchmark evaluator."""
from __future__ import annotations
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SEVERITIES = {"critical", "high", "medium", "low", "informational"}
CATEGORIES = {"correctness", "security", "architecture", "performance", "reliability", "maintainability"}
REQUIRED = ("title", "category", "severity", "file", "description")

def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)

def write_json(path: str | Path, value: Any) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def normalize_path(value: str) -> str:
    path = value.replace("\\", "/").strip()
    while path.startswith("./"):
        path = path[2:]
    return re.sub(r"/+", "/", path)

def normalize_findings(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        findings = payload
    elif isinstance(payload, dict) and isinstance(payload.get("findings"), list):
        findings = payload["findings"]
    else:
        raise ValueError("Input must be an array or an object containing a findings array.")
    normalized = []
    for index, item in enumerate(findings):
        if not isinstance(item, dict):
            raise ValueError(f"Finding {index} must be an object.")
        missing = [key for key in REQUIRED if not isinstance(item.get(key), str) or not item[key].strip()]
        if missing:
            raise ValueError(f"Finding {index} missing valid fields: {', '.join(missing)}")
        category, severity = item["category"].strip().lower(), item["severity"].strip().lower()
        if category not in CATEGORIES:
            raise ValueError(f"Finding {index} has unsupported category: {category}")
        if severity not in SEVERITIES:
            raise ValueError(f"Finding {index} has unsupported severity: {severity}")
        line = item.get("line")
        if line is not None and (isinstance(line, bool) or not isinstance(line, int) or line < 1):
            raise ValueError(f"Finding {index} line must be a positive integer or null.")
        file_path = normalize_path(item["file"])
        if file_path.startswith("/") or ".." in file_path.split("/"):
            raise ValueError(f"Finding {index} file must be a safe repository-relative path.")
        normalized.append({**item, "title": item["title"].strip(), "category": category,
                           "severity": severity, "file": file_path, "line": line,
                           "description": item["description"].strip()})
    return normalized

def deduplicate_findings(findings: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    seen, unique, duplicates = set(), [], 0
    for item in findings:
        key = (item["file"], item.get("line"), item["category"],
               re.sub(r"\s+", " ", item["title"].lower()).strip())
        if key in seen:
            duplicates += 1
        else:
            seen.add(key)
            unique.append(item)
    return unique, duplicates
