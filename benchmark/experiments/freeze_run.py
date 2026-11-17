#!/usr/bin/env python3
"""Freeze prompt and raw-output hashes into a private experiment run record."""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SHA256 = re.compile(r"^[a-f0-9]{64}$")
SHA1 = re.compile(r"^[a-f0-9]{40}$")
RUN_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{2,127}$")
CASE_ID = re.compile(r"^(logic|security|architecture|performance|control)-[0-9]{3}$")
REQUIRED = {
    "run_id", "case_id", "arm", "dataset_version", "manifest_sha256",
    "public_commit", "model_provider", "model_version", "evaluator_commit",
    "sampling_parameters", "enabled_tools", "execution_environment",
    "ground_truth_accessed_before_freeze",
}
OPTIONAL = {"started_at", "exclusions", "failures"}
ALLOWED = REQUIRED | OPTIONAL

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def _require_nonempty_string(record: dict, key: str) -> None:
    if not isinstance(record.get(key), str) or not record[key].strip():
        raise ValueError(f"{key} must be a non-empty string")

def build_record(metadata: dict, prompt: Path, raw_output: Path) -> dict:
    if not isinstance(metadata, dict):
        raise ValueError("metadata must be a JSON object")
    unknown = set(metadata) - ALLOWED
    if unknown:
        raise ValueError("Unknown metadata fields: " + ", ".join(sorted(unknown)))
    missing = REQUIRED - set(metadata)
    if missing:
        raise ValueError("Missing metadata fields: " + ", ".join(sorted(missing)))
    if metadata["ground_truth_accessed_before_freeze"] is not False:
        raise ValueError("ground_truth_accessed_before_freeze must be explicitly false")
    record = dict(metadata)
    if not isinstance(record["run_id"], str) or not RUN_ID.fullmatch(record["run_id"]):
        raise ValueError("run_id must match the schema pattern")
    if not isinstance(record["case_id"], str) or not CASE_ID.fullmatch(record["case_id"]):
        raise ValueError("case_id must match the public benchmark case ID pattern")
    if record["arm"] not in ("baseline", "skill-enabled"):
        raise ValueError("arm must be baseline or skill-enabled")
    for key in ("dataset_version", "model_provider", "model_version", "execution_environment"):
        _require_nonempty_string(record, key)
    if not isinstance(record["manifest_sha256"], str) or not SHA256.fullmatch(record["manifest_sha256"]):
        raise ValueError("manifest_sha256 must be a lowercase SHA-256 digest")
    for key in ("public_commit", "evaluator_commit"):
        if not isinstance(record[key], str) or not SHA1.fullmatch(record[key]):
            raise ValueError(f"{key} must be a full lowercase Git commit SHA")
    if not isinstance(record["sampling_parameters"], dict):
        raise ValueError("sampling_parameters must be an object")
    if not isinstance(record["enabled_tools"], list) or not all(isinstance(x, str) for x in record["enabled_tools"]):
        raise ValueError("enabled_tools must be an array of strings")
    for key in ("exclusions", "failures"):
        record.setdefault(key, [])
        if not isinstance(record[key], list) or not all(isinstance(x, str) for x in record[key]):
            raise ValueError(f"{key} must be an array of strings")
    started_at = record.get("started_at") or datetime.now(timezone.utc).isoformat()
    if not isinstance(started_at, str):
        raise ValueError("started_at must be an ISO-8601 date-time string")
    try:
        parsed = datetime.fromisoformat(started_at.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            raise ValueError("started_at must include a timezone")
    except ValueError as exc:
        raise ValueError("started_at must be an ISO-8601 date-time string with timezone") from exc
    record.update({
        "publication_state": "PRIVATE",
        "started_at": started_at,
        "prompt_sha256": digest(prompt),
        "raw_output_sha256": digest(raw_output),
        "ground_truth_accessed_before_freeze": False,
    })
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")
    record["record_sha256"] = hashlib.sha256(canonical).hexdigest()
    return record

def ensure_private_output_path(output: Path) -> Path:
    resolved = output.resolve()
    public_root = Path(__file__).resolve().parents[2]
    if resolved.is_relative_to(public_root):
        raise ValueError("run records must be written outside the public repository")
    return resolved

def write_record(output: Path, record: dict) -> None:
    """Create a new frozen record exclusively; never overwrite an existing record."""
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(record, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\n")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"), parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f"Invalid JSON constant: {value}")))
        record = build_record(metadata, args.prompt, args.raw_output)
        args.output = ensure_private_output_path(args.output)
        write_record(args.output, record)
        print(json.dumps({"run_id": record["run_id"], "publication_state": "PRIVATE",
                          "prompt_sha256": record["prompt_sha256"],
                          "raw_output_sha256": record["raw_output_sha256"]}, indent=2))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"EXPERIMENT_FREEZE_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
