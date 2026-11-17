from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EVALUATOR = ROOT / "benchmark" / "evaluator"


def finding(*, line=10, title="Incorrect condition", severity="medium",
            description="A concrete behavior violates the stated requirement."):
    return {
        "title": title,
        "category": "correctness",
        "severity": severity,
        "file": "src/example.py",
        "line": line,
        "description": description,
    }


class EvaluatorCliIntegrationTests(unittest.TestCase):
    """Exercise the actual CLI boundaries with synthetic, temporary inputs only."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="benchmark-e2e-")
        self.work = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def write_json(self, name, value):
        path = self.work / name
        path.write_text(json.dumps(value, ensure_ascii=False) + "\n", encoding="utf-8")
        return path

    def run_cli(self, script, *args, expected_returncode=0):
        command = [sys.executable, str(EVALUATOR / script), *(str(arg) for arg in args)]
        completed = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        self.assertEqual(
            completed.returncode,
            expected_returncode,
            msg=(
                f"Command failed: {command}\n"
                f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}"
            ),
        )
        return completed

    def run_pipeline(self, candidate_payload, truth_payload, *, tolerance=2):
        raw_path = self.write_json("raw-review.json", candidate_payload)
        truth_path = self.write_json("synthetic-ground-truth.json", truth_payload)
        normalized_path = self.work / "normalized.json"
        match_path = self.work / "matches.json"
        metrics_path = self.work / "metrics.json"
        report_path = self.work / "report.md"

        self.run_cli("normalize_findings.py", raw_path, normalized_path)
        self.run_cli(
            "match_findings.py", normalized_path, truth_path, match_path,
            "--line-tolerance", str(tolerance),
        )
        self.run_cli("calculate_metrics.py", match_path, metrics_path)
        self.run_cli(
            "generate_report.py", metrics_path, report_path,
            "--title", "Synthetic E2E Integration Report",
        )

        for artifact in (normalized_path, match_path, metrics_path, report_path):
            self.assertTrue(artifact.is_file(), f"Missing pipeline artifact: {artifact.name}")
            self.assertGreater(artifact.stat().st_size, 0, f"Empty pipeline artifact: {artifact.name}")

        return {
            "normalized": json.loads(normalized_path.read_text(encoding="utf-8")),
            "matches": json.loads(match_path.read_text(encoding="utf-8")),
            "metrics": json.loads(metrics_path.read_text(encoding="utf-8")),
            "report": report_path.read_text(encoding="utf-8"),
        }

    def test_full_cli_pipeline_preserves_duplicate_accounting(self):
        item = finding()
        output = self.run_pipeline(
            {"findings": [item, dict(item)]},
            {"findings": [finding(description="Expected reference behavior.")]},
        )
        match_result = output["matches"]
        metrics = output["metrics"]

        self.assertEqual(output["normalized"]["finding_count"], 2)
        self.assertEqual(match_result["true_positive_count"], 1)
        self.assertEqual(match_result["false_positive_count"], 1)
        self.assertEqual(match_result["duplicate_count"], 1)
        self.assertEqual(match_result["candidate_count"], 2)
        self.assertEqual(match_result["expected_count"], 1)
        self.assertEqual(metrics["counts"]["true_positives"], 1)
        self.assertEqual(metrics["counts"]["false_positives"], 1)
        self.assertEqual(metrics["counts"]["duplicates"], 1)
        self.assertAlmostEqual(metrics["metrics"]["precision"], 0.5)
        self.assertIn("Maximum achievable cardinality", output["report"])
        self.assertIn("Forced matches actually scored", output["report"])

    def test_full_cli_pipeline_preserves_conservative_ambiguity(self):
        output = self.run_pipeline(
            {"findings": [finding(line=10)]},
            {"findings": [
                finding(line=9, title="Reference left"),
                finding(line=11, title="Reference right"),
            ]},
        )
        result = output["matches"]
        metrics = output["metrics"]

        self.assertEqual(result["optimal_assignment"]["maximum_cardinality"], 1)
        self.assertEqual(result["true_positive_count"], 0)
        self.assertEqual(result["false_positive_count"], 1)
        self.assertEqual(result["false_negative_count"], 2)
        self.assertEqual(len(result["ambiguous_findings"]), 1)
        self.assertEqual(metrics["diagnostics"]["ambiguous_finding_count"], 1)
        self.assertIn("Ambiguous findings not scored as TP: **1**", output["report"])

    def test_empty_input_completes_and_keeps_undefined_metrics_null(self):
        output = self.run_pipeline({"findings": []}, {"findings": []})
        self.assertEqual(output["matches"]["true_positive_count"], 0)
        self.assertEqual(output["matches"]["candidate_count"], 0)
        self.assertIsNone(output["metrics"]["metrics"]["precision"])
        self.assertIsNone(output["metrics"]["metrics"]["recall"])
        self.assertIn("N/A (undefined)", output["report"])

    def test_invalid_normalization_input_stops_pipeline_without_artifact(self):
        invalid_path = self.work / "invalid.json"
        invalid_path.write_text(
            json.dumps({"findings": [finding(category="not-a-supported-category")]}),
            encoding="utf-8",
        )
        output_path = self.work / "must-not-exist.json"
        completed = self.run_cli(
            "normalize_findings.py", invalid_path, output_path,
            expected_returncode=1,
        )
        self.assertIn("unsupported category", completed.stderr)
        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
