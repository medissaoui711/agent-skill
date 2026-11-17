from __future__ import annotations
import itertools
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluator"))
from common import normalize_findings, deduplicate_findings
from match_findings import match
from calculate_metrics import calculate
from validate_dataset import validate


def finding(file="src/example.js", line=10, category="correctness", severity="medium",
            title="Incorrect condition", description="Concrete incorrect behavior."):
    return {"title": title, "category": category, "severity": severity, "file": file,
            "line": line, "description": description}


class DatasetTests(unittest.TestCase):
    def test_manifest_and_references_validate(self):
        self.assertEqual(validate(), [])

    def test_rejects_unknown_category(self):
        with self.assertRaises(ValueError):
            normalize_findings({"findings": [finding(category="unknown")]})

    def test_accepts_empty_findings(self):
        self.assertEqual(normalize_findings({"findings": []}), [])

    def test_rejects_traversal_path(self):
        with self.assertRaises(ValueError):
            normalize_findings({"findings": [finding(file="../outside.js")]})

    def test_negative_tolerance_rejected(self):
        with self.assertRaises(ValueError):
            match([], {"findings": []}, -1)


class MatchingTests(unittest.TestCase):
    def test_match_within_line_tolerance(self):
        result = match([finding(line=12)], {"findings": [finding(line=10)]}, 3)
        self.assertEqual((result["true_positive_count"], result["false_positive_count"],
                          result["false_negative_count"]), (1, 0, 0))

    def test_category_mismatch(self):
        result = match([finding(category="security")], {"findings": [finding()]})
        self.assertEqual((result["true_positive_count"], result["false_positive_count"],
                          result["false_negative_count"]), (0, 1, 1))

    def test_qwen_order_dependence_reproduction(self):
        candidates = [finding(line=12), finding(line=13, title="Second defect")]
        truth = {"findings": [finding(line=10), finding(line=13, title="Reference two")]}
        result = match(candidates, truth, 2)
        self.assertEqual(result["optimal_assignment"]["maximum_cardinality"], 2)
        self.assertEqual(result["true_positive_count"], 2)
        self.assertEqual((result["false_positive_count"], result["false_negative_count"]), (0, 0))

    def test_candidate_and_reference_permutations_are_invariant(self):
        candidates = [finding(line=12), finding(line=13, title="Second defect")]
        truth = [finding(line=10), finding(line=13, title="Reference two")]
        baseline = match(candidates, {"findings": truth}, 2)
        for candidate_order in itertools.permutations(candidates):
            for truth_order in itertools.permutations(truth):
                actual = match(list(candidate_order), {"findings": list(truth_order)}, 2)
                self.assertEqual(actual, baseline)

    def test_equal_cost_alternatives_are_ambiguous(self):
        result = match([finding(line=10)], {"findings": [
            finding(line=9, title="Reference left"), finding(line=11, title="Reference right")
        ]}, 2)
        self.assertEqual(result["optimal_assignment"]["maximum_cardinality"], 1)
        self.assertEqual(result["true_positive_count"], 0)
        self.assertEqual(len(result["ambiguous_findings"]), 1)
        self.assertEqual(result["false_negative_count"], 2)

    def test_localized_edges_take_priority_over_missing_line_edges(self):
        candidates = [finding(line=None), finding(line=10, title="Located candidate")]
        truth = {"findings": [finding(line=None), finding(line=10, title="Located reference")]}
        result = match(candidates, truth, 3)
        self.assertEqual(result["optimal_assignment"]["maximum_cardinality"], 2)
        self.assertEqual(result["optimal_assignment"]["localized_pair_count"], 1)
        self.assertEqual(result["true_positive_count"], 2)

    def test_missing_line_single_reference_is_unlocalized_match(self):
        result = match([finding(line=None)], {"findings": [finding(line=10)]})
        self.assertEqual(result["true_positive_count"], 1)
        self.assertFalse(result["matches"][0]["location_within_tolerance"])

    def test_missing_line_multiple_references_is_ambiguous(self):
        result = match([finding(line=None)], {"findings": [
            finding(line=10), finding(line=20, title="Another reference")
        ]})
        self.assertEqual(result["true_positive_count"], 0)
        self.assertEqual(len(result["ambiguous_findings"]), 1)

    def test_duplicate_identical_candidates_are_order_invariant(self):
        first = finding()
        second = finding()
        unique_a, count_a = deduplicate_findings([first, second])
        unique_b, count_b = deduplicate_findings([second, first])
        self.assertEqual((unique_a, count_a), (unique_b, count_b))
        result = match([first, second], {"findings": [finding()]})
        self.assertEqual(result["duplicate_count"], 1)
        self.assertEqual(result["false_positive_count"], 1)

    def test_conflicting_duplicate_variants_are_quarantined(self):
        candidates = [
            finding(severity="high", description="High impact variant"),
            finding(severity="low", description="Low impact variant"),
        ]
        result = match(candidates, {"findings": [finding()]})
        self.assertEqual(result["true_positive_count"], 0)
        self.assertEqual(result["false_positive_count"], 2)
        self.assertEqual(len(result["conflicting_duplicate_groups"]), 1)
        reversed_result = match(list(reversed(candidates)), {"findings": [finding()]})
        self.assertEqual(result, reversed_result)

    def test_no_eligible_edges(self):
        result = match([finding(line=100)], {"findings": [finding(line=1)]}, 2)
        self.assertEqual((result["true_positive_count"], result["false_positive_count"],
                          result["false_negative_count"]), (0, 1, 1))

    def test_zero_tolerance(self):
        result = match([finding(line=10)], {"findings": [finding(line=10)]}, 0)
        self.assertEqual(result["true_positive_count"], 1)

    def test_independent_components(self):
        candidates = [finding(file="a.js", line=2), finding(file="b.js", line=8)]
        truth = {"findings": [finding(file="b.js", line=8), finding(file="a.js", line=2)]}
        result = match(candidates, truth)
        self.assertEqual(result["true_positive_count"], 2)


class MetricsTests(unittest.TestCase):
    def test_expected_metrics(self):
        result = {"true_positive_count": 8, "false_positive_count": 2, "false_negative_count": 2,
                  "duplicate_count": 1, "candidate_count": 11, "expected_count": 10,
                  "matches": [{"severity_exact": True, "location_within_tolerance": True} for _ in range(7)]
                  + [{"severity_exact": False, "location_within_tolerance": True}]}
        metrics = calculate(result)["metrics"]
        self.assertAlmostEqual(metrics["precision"], .8)
        self.assertAlmostEqual(metrics["recall"], .8)
        self.assertAlmostEqual(metrics["f1"], .8)
        self.assertAlmostEqual(metrics["severity_accuracy"], .875)
        self.assertAlmostEqual(metrics["localization_accuracy"], 1.0)

    def test_undefined_metrics_are_null(self):
        result = {"true_positive_count": 0, "false_positive_count": 0, "false_negative_count": 0,
                  "duplicate_count": 0, "candidate_count": 0, "expected_count": 0, "matches": []}
        metrics = calculate(result)["metrics"]
        self.assertIsNone(metrics["precision"])
        self.assertIsNone(metrics["recall"])
        self.assertIsNone(metrics["f1"])


if __name__ == "__main__":
    unittest.main()
