#!/usr/bin/env python3
"""Validate the public benchmark manifest, schemas, and referenced fixture files."""
from __future__ import annotations
import sys
from common import ROOT, load_json

EXPECTED = {
    "logic-001", "logic-002", "logic-003", "logic-004", "logic-005", "logic-006", "logic-007",
    "security-001", "security-002", "security-003", "security-004", "security-005", "security-006", "security-007",
    "architecture-001", "architecture-002", "architecture-003", "architecture-004", "architecture-005", "architecture-006", "performance-001", "control-001", "control-002", "control-003",
    "logic-008", "logic-009", "logic-010", "security-008", "security-009", "security-010",
    "performance-002", "performance-003", "performance-004", "performance-005", "performance-006",
    "control-004", "control-005", "control-006", "control-007", "control-008",
}
CASE_REQUIRED = {"id", "category", "difficulty", "title", "task_file", "project_files"}

def validate() -> list[str]:
    errors: list[str] = []
    benchmark_root = ROOT / "benchmark"
    schema_paths = [
        benchmark_root / "DATASET_SCHEMA.json",
        benchmark_root / "schemas/case.schema.json",
        benchmark_root / "schemas/finding.schema.json",
    ]
    for path in schema_paths:
        try:
            schema = load_json(path)
            if not isinstance(schema, dict) or schema.get("type") != "object":
                errors.append(f"{path.relative_to(ROOT)} must contain a JSON Schema object.")
        except (OSError, ValueError) as exc:
            errors.append(f"Invalid or missing schema {path.relative_to(ROOT)}: {exc}")
    try:
        data = load_json(benchmark_root / "cases/manifest.json")
    except (OSError, ValueError) as exc:
        return errors + [f"Cannot load manifest: {exc}"]
    if not isinstance(data, dict) or data.get("version") != "1.0.0":
        errors.append("Manifest version must be 1.0.0.")
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        return errors + ["Manifest cases must be an array."]
    ids: list[str] = []
    allowed_categories = {"logic", "security", "architecture", "performance", "control"}
    for case in cases:
        if not isinstance(case, dict):
            errors.append("Each case must be an object.")
            continue
        case_id = case.get("id")
        if not isinstance(case_id, str) or case_id not in EXPECTED:
            errors.append(f"Invalid case ID: {case_id!r}")
            continue
        ids.append(case_id)
        if set(case) != CASE_REQUIRED:
            errors.append(f"{case_id}: case fields must be exactly {sorted(CASE_REQUIRED)}.")
        if case.get("category") not in allowed_categories:
            errors.append(f"{case_id}: invalid category.")
        if case.get("difficulty") not in {"easy", "medium", "hard"}:
            errors.append(f"{case_id}: invalid difficulty.")
        expected_task = f"benchmark/cases/{case_id}/task.md"
        task = case.get("task_file")
        if task != expected_task or not (ROOT / expected_task).is_file():
            errors.append(f"{case_id}: task_file must be {expected_task}.")
        project_files = case.get("project_files")
        if not isinstance(project_files, list) or not project_files:
            errors.append(f"{case_id}: project_files must be a non-empty array.")
        else:
            for item in project_files:
                prefix = f"benchmark/cases/{case_id}/project/"
                if not isinstance(item, str) or not item.startswith(prefix) or ".." in item.split("/"):
                    errors.append(f"{case_id}: unsafe project file path {item!r}.")
                elif not (ROOT / item).is_file():
                    errors.append(f"{case_id}: missing project file {item!r}.")
    if len(ids) != len(set(ids)):
        errors.append("Case IDs must be unique.")
    if set(ids) != EXPECTED:
        errors.append(f"Batch A+B+C+D dataset must contain exactly: {sorted(EXPECTED)}.")
    forbidden = {"ground-truth", "expected-results", "answer-key", "answer_key"}
    for path in benchmark_root.rglob("*"):
        if any(part.lower() in forbidden for part in path.parts):
            errors.append(f"Forbidden ground-truth path: {path.relative_to(ROOT)}")
    return errors

def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("SUCCESS: Batch A+B+C+D public manifest, schemas, and referenced files are valid.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
