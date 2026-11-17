#!/usr/bin/env python3
"""Freeze prompt and raw-output hashes into a private experiment run record.

This utility never accepts or reads Ground Truth. Invoke it immediately after
capturing raw output and before any evaluator/reference access.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SHA256 = re.compile(r"^[a-f0-9]{64}$")
SHA1 = re.compile(r"^[a-f0-9]{40}$")
SCHEMA_PATH = Path(__file__).with_name("run.schema.json")


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def _reject_non_json_constant(value: str):
    raise ValueError(f"Invalid JSON numeric constant: {value}")


def validate_record(record: dict) -> None:
    """Validate the complete final record; never skip JSON Schema format checks."""
    try:
        from jsonschema import Draft202012Validator, FormatChecker
    except ImportError as exc:
        raise RuntimeError(
            "Missing required dependency 'jsonschema[format]==4.25.1'. "
            "Install it with: python -m pip install -r "
            "benchmark/experiments/requirements.txt"
        ) from exc

    schema = json.loads(
        SCHEMA_PATH.read_text(encoding="utf-8"),
        parse_constant=_reject_non_json_constant,
    )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(record), key=lambda error: list(error.absolute_path))
    if errors:
        details = "; ".join(
            f"{'/'.join(str(part) for part in error.absolute_path) or '<root>'}: {error.message}"
            for error in errors
        )
        raise ValueError(f"Run record does not match run.schema.json: {details}")


def build_record(metadata: dict, prompt: Path, raw_output: Path) -> dict:
    if not isinstance(metadata, dict):
        raise ValueError("Run metadata must be a JSON object")
    required = (
        "run_id", "case_id", "arm", "dataset_version", "manifest_sha256",
        "public_commit", "model_provider", "model_version", "evaluator_commit",
        "sampling_parameters", "enabled_tools", "execution_environment",
    )
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
    if not isinstance(record["manifest_sha256"], str) or not SHA256.fullmatch(record["manifest_sha256"]):
        raise ValueError("manifest_sha256 must be a lowercase SHA-256 digest")
    if (
        not isinstance(record["public_commit"], str)
        or not SHA1.fullmatch(record["public_commit"])
        or not isinstance(record["evaluator_commit"], str)
        or not SHA1.fullmatch(record["evaluator_commit"])
    ):
        raise ValueError("public_commit and evaluator_commit must be full Git commit SHAs")
    if record["arm"] not in ("baseline", "skill-enabled"):
        raise ValueError("arm must be baseline or skill-enabled")

    try:
        canonical = json.dumps(
            record, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
        ).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Run metadata is not strict JSON: {exc}") from exc
    record["record_sha256"] = hashlib.sha256(canonical).hexdigest()

    # Validate the exact final object, including generated hashes and metadata.
    validate_record(record)
    return record


def ensure_private_output_path(output: Path) -> Path:
    resolved = output.resolve()
    public_root = Path(__file__).resolve().parents[2]
    if resolved.is_relative_to(public_root):
        raise ValueError("run records must be written outside the public repository")
    return resolved


def write_record(output: Path, record: dict) -> None:
    """Atomically publish a fully written record without ever replacing an existing path."""
    output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(record, indent=2, sort_keys=True, allow_nan=False) + "\n"
    fd, temporary_name = tempfile.mkstemp(
        prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        # Hard-link creation is atomic and fails if output already exists.
        # The temporary file is in the same directory/filesystem by construction.
        os.link(temporary, output)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--metadata", type=Path, required=True)
    parser.add_argument("--prompt", type=Path, required=True)
    parser.add_argument("--raw-output", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        metadata = json.loads(
            args.metadata.read_text(encoding="utf-8"),
            parse_constant=_reject_non_json_constant,
        )
        record = build_record(metadata, args.prompt, args.raw_output)
        output = ensure_private_output_path(args.output)
        write_record(output, record)
        print(json.dumps({
            "run_id": record["run_id"],
            "publication_state": "PRIVATE",
            "prompt_sha256": record["prompt_sha256"],
            "raw_output_sha256": record["raw_output_sha256"],
        }, indent=2, allow_nan=False))
    except (OSError, ValueError, TypeError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"EXPERIMENT_FREEZE_FAILED: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
