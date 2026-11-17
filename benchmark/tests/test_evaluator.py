from __future__ import annotations
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "evaluator"))
from common import normalize_findings
from match_findings import match
from calculate_metrics import calculate
from validate_dataset import validate

def finding(file="src/example.js", line=10, category="correctness", severity="medium", title="Incorrect condition"):
    return {"title":title,"category":category,"severity":severity,"file":file,"line":line,"description":"Concrete incorrect behavior."}

class DatasetTests(unittest.TestCase):
    def test_manifest_and_references_validate(self): self.assertEqual(validate(), [])
    def test_rejects_unknown_category(self):
        with self.assertRaises(ValueError): normalize_findings({"findings":[finding(category="unknown")]})
    def test_accepts_empty_findings(self): self.assertEqual(normalize_findings({"findings":[]}), [])
    def test_rejects_traversal_path(self):
        with self.assertRaises(ValueError): normalize_findings({"findings":[finding(file="../outside.js")]})

class MatchingTests(unittest.TestCase):
    def test_match_within_line_tolerance(self):
        result=match([finding(line=12)],{"findings":[finding(line=10)]},3)
        self.assertEqual((result["true_positive_count"],result["false_positive_count"],result["false_negative_count"]),(1,0,0))
    def test_category_mismatch(self):
        result=match([finding(category="security")],{"findings":[finding()]})
        self.assertEqual((result["true_positive_count"],result["false_positive_count"],result["false_negative_count"]),(0,1,1))
    def test_duplicate_is_false_positive(self):
        result=match([finding(),finding()],{"findings":[finding()]})
        self.assertEqual(result["false_positive_count"],1); self.assertEqual(result["duplicate_count"],1)
    def test_equal_distance_is_ambiguous(self):
        result=match([finding(line=10)],{"findings":[finding(line=9),finding(line=11)]},3)
        self.assertEqual(result["true_positive_count"],0); self.assertEqual(result["false_negative_count"],2)
    def test_missing_line_does_not_count_as_localized(self):
        result=match([finding(line=None)],{"findings":[finding(line=10)]})
        self.assertEqual(result["true_positive_count"],1)
        self.assertFalse(result["matches"][0]["location_within_tolerance"])

class MetricsTests(unittest.TestCase):
    def test_expected_metrics(self):
        result={"true_positive_count":8,"false_positive_count":2,"false_negative_count":2,"duplicate_count":1,"candidate_count":11,"expected_count":10,
          "matches":[{"severity_exact":True,"location_within_tolerance":True} for _ in range(7)]+[{"severity_exact":False,"location_within_tolerance":True}]}
        m=calculate(result)["metrics"]
        self.assertAlmostEqual(m["precision"],.8); self.assertAlmostEqual(m["recall"],.8)
        self.assertAlmostEqual(m["f1"],.8); self.assertAlmostEqual(m["severity_accuracy"],.875)
        self.assertAlmostEqual(m["localization_accuracy"],1.0)
    def test_undefined_metrics_are_null(self):
        result={"true_positive_count":0,"false_positive_count":0,"false_negative_count":0,"duplicate_count":0,"candidate_count":0,"expected_count":0,"matches":[]}
        m=calculate(result)["metrics"]
        self.assertIsNone(m["precision"]); self.assertIsNone(m["recall"]); self.assertIsNone(m["f1"])

if __name__ == "__main__": unittest.main()
