import hashlib
import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from freeze_run import build_record, ensure_private_output_path, write_record

class FreezeRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.prompt = self.root / "prompt"
        self.prompt.write_bytes(b"exact prompt bytes")
        self.raw = self.root / "raw"
        self.raw.write_bytes(b"exact raw output bytes")
        self.metadata = {
            "run_id": "run-001", "case_id": "logic-001", "arm": "baseline",
            "dataset_version": "v1.0.0", "manifest_sha256": "a" * 64,
            "public_commit": "b" * 40, "model_provider": "provider",
            "model_version": "model-v1", "evaluator_commit": "c" * 40,
            "sampling_parameters": {"temperature": 0}, "enabled_tools": [],
            "execution_environment": "isolated",
            "ground_truth_accessed_before_freeze": False,
        }

    def tearDown(self):
        self.tmp.cleanup()

    def test_hashes_exact_prompt_and_raw_output_bytes(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        self.assertEqual(record["prompt_sha256"], hashlib.sha256(b"exact prompt bytes").hexdigest())
        self.assertEqual(record["raw_output_sha256"], hashlib.sha256(b"exact raw output bytes").hexdigest())
        self.assertEqual(record["publication_state"], "PRIVATE")

    def test_rejects_ground_truth_access_before_freeze(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata, ground_truth_accessed_before_freeze=True), self.prompt, self.raw)

    def test_rejects_invalid_arm(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata, arm="other"), self.prompt, self.raw)

    def test_rejects_unknown_metadata_fields(self):
        with self.assertRaisesRegex(ValueError, "Unknown metadata fields"):
            build_record(dict(self.metadata, notes="unexpected"), self.prompt, self.raw)

    def test_rejects_invalid_case_id_and_run_id(self):
        for key, value in (("case_id", "bogus"), ("run_id", "x")):
            with self.subTest(key=key), self.assertRaises(ValueError):
                build_record(dict(self.metadata, **{key: value}), self.prompt, self.raw)

    def test_rejects_invalid_datetime(self):
        with self.assertRaisesRegex(ValueError, "started_at"):
            build_record(dict(self.metadata, started_at="not-a-date"), self.prompt, self.raw)

    def test_rejects_non_finite_json_numbers(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata, sampling_parameters={"temperature": math.nan}), self.prompt, self.raw)

    def test_record_digest_detects_metadata_or_fingerprint_tampering(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        original = record["record_sha256"]
        record["raw_output_sha256"] = "0" * 64
        altered = dict(record)
        altered.pop("record_sha256")
        canonical = json.dumps(altered, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode()
        self.assertNotEqual(original, hashlib.sha256(canonical).hexdigest())

    def test_output_path_must_be_outside_public_repository(self):
        with self.assertRaises(ValueError):
            ensure_private_output_path(ROOT / "public-run.json")
        self.assertTrue(ensure_private_output_path(self.root / "private-run.json").is_absolute())

    def test_freeze_refuses_existing_record(self):
        record = build_record(self.metadata, self.prompt, self.raw)
        output = self.root / "frozen.json"
        write_record(output, record)
        before = output.read_bytes()
        with self.assertRaises(FileExistsError):
            write_record(output, record)
        self.assertEqual(output.read_bytes(), before)

if __name__ == "__main__":
    unittest.main()
