#!/usr/bin/env python3
"""Freeze prompt and raw-output hashes into a private experiment run record.

This utility never accepts or reads Ground Truth. Invoke it immediately after
capturing raw output and before any evaluator/reference access.
"""
from __future__ import annotations
import argparse, hashlib, json, re, sys
from datetime import datetime, timezone
from pathlib import Path

SHA256 = re.compile(r"^[a-f0-9]{64}$")
SHA1 = re.compile(r"^[a-f0-9]{40}$")

def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def build_record(metadata: dict, prompt: Path, raw_output: Path) -> dict:
    required = ("run_id", "case_id", "arm", "dataset_version", "manifest_sha256",
                "public_commit", "model_provider", "model_version", "evaluator_commit",
                "sampling_parameters", "enabled_tools", "execution_environment")
    missing = [key for key in required if key not in metadata]
    if missing:
        raise ValueError("Missing metadata fields: " + ", ".join(missing))
    if metadata.get("ground_truth_accessed_before_freeze") is not False:
        raise ValueError("ground_truth_accessed_before_freeze must be explicitly false")
    record = dict(metadata)
    record.update({
        "publication_state": "PRIVATE",
        "started_at": metadata.get("started_at") or datetime.now(timezone.utc).isoformat(),
        "prompt_sha256": digest(prompt),
        "raw_output_sha256": digest(raw_output),
        "ground_truth_accessed_before_freeze": False,
        "exclusions": metadata.get("exclusions", []),
        "failures": metadata.get("failures", []),
    })
    if not SHA256.fullmatch(record["manifest_sha256"]):
        raise ValueError("manifest_sha256 must be a lowercase SHA-256 digest")
    if not SHA1.fullmatch(record["public_commit"]) or not SHA1.fullmatch(record["evaluator_commit"]):
        raise ValueError("public_commit and evaluator_commit must be full Git commit SHAs")
    if record["arm"] not in ("baseline", "skill-enabled"):
        raise ValueError("arm must be baseline or skill-enabled")
    canonical = json.dumps(record, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
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
    with output.open("x", encoding="utf-8", newline="\\n") as stream:
        json.dump(record, stream, indent=2, sort_keys=True, allow_nan=False)
        stream.write("\\n")

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
        record = build_record(metadata, args.prompt, args.raw_output)
        args.output = ensure_private_output_path(args.output)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        if args.output.exists():
            raise ValueError("Refusing to overwrite an existing frozen run record")
        args.output.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"run_id": record["run_id"], "publication_state": "PRIVATE",
                          "prompt_sha256": record["prompt_sha256"],
                          "raw_output_sha256": record["raw_output_sha256"]}, indent=2))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        print(f"EXPERIMENT_FREEZE_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
