import hashlib, sys, tempfile, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "experiments"))
from freeze_run import build_record

class FreezeRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.prompt=self.root/"prompt"; self.prompt.write_bytes(b"exact prompt bytes")
        self.raw=self.root/"raw"; self.raw.write_bytes(b"exact raw output bytes")
        self.metadata={"run_id":"run-001","case_id":"logic-001","arm":"baseline",
          "dataset_version":"v1.0.0","manifest_sha256":"a"*64,"public_commit":"b"*40,
          "model_provider":"provider","model_version":"model-v1","evaluator_commit":"c"*40,
          "sampling_parameters":{"temperature":0},"enabled_tools":[],"execution_environment":"isolated",
          "ground_truth_accessed_before_freeze":False}
    def tearDown(self): self.tmp.cleanup()
    def test_hashes_exact_prompt_and_raw_output_bytes(self):
        record=build_record(self.metadata,self.prompt,self.raw)
        self.assertEqual(record["prompt_sha256"],hashlib.sha256(b"exact prompt bytes").hexdigest())
        self.assertEqual(record["raw_output_sha256"],hashlib.sha256(b"exact raw output bytes").hexdigest())
        self.assertEqual(record["publication_state"],"PRIVATE")
    def test_rejects_ground_truth_access_before_freeze(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata,ground_truth_accessed_before_freeze=True),self.prompt,self.raw)
    def test_rejects_invalid_arm(self):
        with self.assertRaises(ValueError):
            build_record(dict(self.metadata,arm="other"),self.prompt,self.raw)
    def test_record_digest_detects_metadata_or_fingerprint_tampering(self):
        record=build_record(self.metadata,self.prompt,self.raw)
        original=record["record_sha256"]
        record["raw_output_sha256"]="0"*64
        import json
        import hashlib as h
        altered=dict(record); altered.pop("record_sha256")
        digest=h.sha256(json.dumps(altered,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
        self.assertNotEqual(original,digest)
    def test_freeze_refuses_existing_record(self):
        record=build_record(self.metadata,self.prompt,self.raw)
        self.assertEqual(record["publication_state"],"PRIVATE")
if __name__=="__main__": unittest.main()
