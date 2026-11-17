import builtins
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "experiments" / "freeze_run.py"
sys.path.insert(0, str(ROOT / "experiments"))
from freeze_run import build_record, ensure_private_output_path, write_record


class FreezeRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.prompt = self.root / "prompt.txt"
        self.prompt.write_bytes(b"exact prompt bytes")
        self.raw = self.root / "raw-output.txt"
        self.raw.write_bytes(b"exact raw output bytes")
        self.metadata = {
            "run_id": "run-001",
            "case_id": "logic-001",
            "arm": "baseline",
            "dataset_version": "v1.0.0",
            "manifest_sha256": "a" * 64,
            "public_commit": "b" * 40,
            "model_provider": "provider",
            "model_version": "model-v1",
            "evaluator_commit": "c" * 40,
            "sampling_parameters": {"temperature": 0},
            "enabled_tools": [],
            "execution_environment": "isolated",
            "ground_truth_accessed_before_freeze": False,
        }
        self.metadata_path = self.root / "metadata.json"
        self.write_metadata()

    def tearDown(self):
        self.tmp.cleanup()

    def write_metadata(self, metadata=None):
        self.metadata_path.write_text(
            json.dumps(self.metadata if metadata is None else metadata),
            encoding="utf-8",
        )

    def cli(self, output):
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--metadata", str(self.metadata_path),
                "--prompt", str(self.prompt),
                "--raw-output", str(self.raw),
                "--output", str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

    def test_hashes_exact_prompt_and_raw_output_bytes(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        self.assertEqual(
            record["prompt_sha256"],
            hashlib.sha256(b"exact prompt bytes").hexdigest(),
        )
        self.assertEqual(
            record["raw_output_sha256"],
            hashlib.sha256(b"exact raw output bytes").hexdigest(),
        )
        self.assertEqual(record["publication_state"], "PRIVATE")

    def test_rejects_ground_truth_access_before_freeze(self):
        with self.assertRaises(ValueError):
            build_record(
                dict(self.metadata, ground_truth_accessed_before_freeze=True),
                self.prompt,
                self.raw,
            )

    def test_rejects_invalid_arm(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata, arm="other"), self.prompt, self.raw)

    def test_record_digest_detects_metadata_or_fingerprint_tampering(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        original = record["record_sha256"]
        record["raw_output_sha256"] = "0" * 64
        altered = dict(record)
        altered.pop("record_sha256")
        digest = hashlib.sha256(
            json.dumps(
                altered, sort_keys=True, separators=(",", ":"), ensure_ascii=False
            ).encode()
        ).hexdigest()
        self.assertNotEqual(original, digest)

    def test_output_path_must_be_outside_public_repository(self):
        with self.assertRaises(ValueError):
            ensure_private_output_path(ROOT / "public-run.json")
        self.assertTrue(
            ensure_private_output_path(self.root / "private-run.json").is_absolute()
        )

    def test_schema_rejects_invalid_identifiers_types_and_unknown_fields(self):
        invalid_records = [
            dict(self.metadata, run_id="x"),
            dict(self.metadata, case_id="unknown-001"),
            dict(self.metadata, enabled_tools="not-an-array"),
            dict(self.metadata, unexpected_metadata="not allowed"),
            dict(self.metadata, started_at="not-a-date-time"),
            dict(self.metadata, model_provider=""),
        ]
        for metadata in invalid_records:
            with self.subTest(metadata=metadata):
                with self.assertRaises(ValueError):
                    build_record(metadata, self.prompt, self.raw)

    def test_schema_rejects_invalid_calendar_date_time(self):
        metadata = dict(self.metadata, started_at="2026-02-30T00:00:00Z")
        with self.assertRaises(ValueError):
            build_record(metadata, self.prompt, self.raw)

    def test_missing_jsonschema_fails_with_install_instruction(self):
        real_import = builtins.__import__

        def import_without_jsonschema(name, *args, **kwargs):
            if name == "jsonschema" or name.startswith("jsonschema."):
                raise ModuleNotFoundError("simulated missing jsonschema")
            return real_import(name, *args, **kwargs)

        with patch("builtins.__import__", side_effect=import_without_jsonschema):
            with self.assertRaisesRegex(
                RuntimeError, "benchmark/experiments/requirements.txt"
            ):
                build_record(self.metadata, self.prompt, self.raw)

    def test_cli_fails_closed_when_jsonschema_is_unavailable(self):
        output = self.root / "missing-dependency-record.json"
        result = subprocess.run(
            [
                sys.executable, "-S", str(SCRIPT),
                "--metadata", str(self.metadata_path),
                "--prompt", str(self.prompt),
                "--raw-output", str(self.raw),
                "--output", str(output),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("EXPERIMENT_FREEZE_FAILED", result.stderr)
        self.assertIn("Missing required dependency", result.stderr)
        self.assertIn("benchmark/experiments/requirements.txt", result.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(list(self.root.glob(f".{output.name}.*.tmp")), [])

    def test_schema_rejects_missing_required_fields(self):
        metadata = dict(self.metadata)
        metadata.pop("model_version")
        with self.assertRaises(ValueError):
            build_record(metadata, self.prompt, self.raw)

    def test_non_finite_numbers_are_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf")):
            with self.subTest(value=value):
                metadata = dict(self.metadata, sampling_parameters={"value": value})
                with self.assertRaises(ValueError):
                    build_record(metadata, self.prompt, self.raw)

    def test_cli_refuses_existing_file_without_changing_it(self):
        output = self.root / "existing-record.json"
        original = b"pre-existing immutable content\n"
        output.write_bytes(original)
        result = self.cli(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(output.read_bytes(), original)

    def test_cli_writes_a_schema_valid_record(self):
        output = self.root / "valid-record.json"
        result = self.cli(output)
        self.assertEqual(result.returncode, 0, result.stderr)
        record = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(record["run_id"], self.metadata["run_id"])
        self.assertEqual(record["publication_state"], "PRIVATE")

    def test_cli_does_not_create_final_file_for_invalid_schema(self):
        output = self.root / "invalid-record.json"
        self.write_metadata(dict(self.metadata, run_id="x"))
        result = self.cli(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        self.assertEqual(list(self.root.glob(f".{output.name}.*.tmp")), [])

    def test_two_cli_processes_cannot_overwrite_each_other(self):
        output = self.root / "raced-record.json"
        command = [
            sys.executable, str(SCRIPT),
            "--metadata", str(self.metadata_path),
            "--prompt", str(self.prompt),
            "--raw-output", str(self.raw),
            "--output", str(output),
        ]
        first = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        second = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        first_out, first_err = first.communicate(timeout=15)
        second_out, second_err = second.communicate(timeout=15)
        self.assertEqual(
            sorted([first.returncode, second.returncode]),
            [0, 1],
            msg=f"first: {first_out} {first_err}; second: {second_out} {second_err}",
        )
        record = json.loads(output.read_text(encoding="utf-8"))
        self.assertEqual(record["run_id"], self.metadata["run_id"])
        self.assertEqual(list(self.root.glob(f".{output.name}.*.tmp")), [])

    def test_atomic_writer_refuses_existing_record(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        output = self.root / "frozen.json"
        write_record(output, record)
        before = output.read_bytes()
        with self.assertRaises(FileExistsError):
            write_record(output, record)
        self.assertEqual(output.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
