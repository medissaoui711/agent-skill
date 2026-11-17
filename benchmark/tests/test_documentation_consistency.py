"""Keep public benchmark documentation aligned with the authoritative manifest."""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "benchmark/cases/manifest.json"
ROOT_README = ROOT / "README.md"
BENCHMARK_README = ROOT / "benchmark/README.md"

CATEGORY_LABELS = {
    "logic": "Logic / Runtime",
    "security": "Security",
    "architecture": "Architecture",
    "performance": "Performance / Reliability",
    "control": "Clean / Control",
}
class DocumentationConsistencyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        cls.cases = cls.manifest["cases"]
        cls.root_readme = ROOT_README.read_text(encoding="utf-8")
        cls.benchmark_readme = BENCHMARK_README.read_text(encoding="utf-8")

    def test_manifest_has_expected_v1_development_inventory(self) -> None:
        self.assertEqual(len(self.cases), 40)
        self.assertEqual({case["category"] for case in self.cases}, set(CATEGORY_LABELS))
        self.assertEqual(len({case["id"] for case in self.cases}), 40)

    def test_root_readme_case_count_marker_matches_manifest(self) -> None:
        matches = re.findall(r"<!--\s*benchmark:public-case-count\s*=\s*(\d+)\s*-->", self.root_readme)
        self.assertEqual(len(matches), 1)
        self.assertEqual(int(matches[0]), len(self.cases))

    def test_root_readme_describes_40_public_fixtures_not_five_case_pilot(self) -> None:
        self.assertRegex(self.root_readme, r"40 public synthetic review cases")
        self.assertIn("10 logic/runtime", self.root_readme)
        self.assertIn("10 security", self.root_readme)
        self.assertIn("6 architecture", self.root_readme)
        self.assertIn("6 performance/reliability", self.root_readme)
        self.assertIn("8 clean/control", self.root_readme)
        self.assertNotIn("The pilot has five cases; the approved V1 target is 40", self.root_readme)

    def test_benchmark_inventory_table_matches_manifest_exactly(self) -> None:
        table = self.benchmark_readme.split("## Complete case inventory", 1)[1].split(
            "## Review protocol", 1
        )[0]
        rows = re.findall(r"^\| ([a-z]+-\d{3}) \| ([^|]+) \| ([^|]+) \|$", table, re.M)
        documented = {
            case_id: (category.strip(), title.strip())
            for case_id, category, title in rows
        }
        expected = {
            case["id"]: (CATEGORY_LABELS[case["category"]], case["title"])
            for case in self.cases
        }
        self.assertEqual(documented, expected)

    def test_stale_batch_inventory_and_validator_claims_are_absent(self) -> None:
        self.assertNotIn("12-case Batch A inventory", self.benchmark_readme)
        self.assertNotIn("validator requires exactly 21", self.benchmark_readme)
        self.assertNotIn("validator requires exactly 40", self.benchmark_readme)
        self.assertNotIn("not a representative 40-case benchmark", self.benchmark_readme)

    def test_experiment_statement_is_evidence_gated(self) -> None:
        self.assertIn("no claim that baseline/skill-enabled trials have been completed", self.benchmark_readme)
        self.assertIn("NOT_RUN_OR_NOT_EVIDENCED", self.benchmark_readme)
        self.assertNotIn("has reached 40 cases and run repeated baseline/skill-enabled trials", self.benchmark_readme)


if __name__ == "__main__":
    unittest.main()
