#!/usr/bin/env python3
"""Validate matcher output and calculate integrity-checked benchmark metrics."""
from __future__ import annotations
import argparse
import sys
from typing import Any
from common import load_json, write_json

COUNT_KEYS = ("true_positive_count", "false_positive_count", "false_negative_count",
              "duplicate_count", "candidate_count", "expected_count")


def _non_negative_int(value: Any, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be a non-negative integer.")
    return value


def validate_match_result(result: Any) -> dict[str, Any]:
    if not isinstance(result, dict):
        raise ValueError("Matcher result must be a JSON object.")
    counts = {key: _non_negative_int(result.get(key), key) for key in COUNT_KEYS}
    matches = result.get("matches")
    if not isinstance(matches, list):
        raise ValueError("matches must be an array.")
    if len(matches) != counts["true_positive_count"]:
        raise ValueError("matches length must equal true_positive_count.")
    if counts["candidate_count"] != (counts["true_positive_count"] +
                                      counts["false_positive_count"]):
        raise ValueError("candidate_count must equal TP + FP; duplicates are already included in FP.")
    if counts["duplicate_count"] > counts["false_positive_count"]:
        raise ValueError("duplicate_count cannot exceed false_positive_count.")
    if counts["expected_count"] != (counts["true_positive_count"] +
                                     counts["false_negative_count"]):
        raise ValueError("expected_count must equal TP + FN.")
    for index, item in enumerate(matches):
        if not isinstance(item, dict):
            raise ValueError(f"matches[{index}] must be an object.")
        for field in ("severity_exact", "location_within_tolerance"):
            if not isinstance(item.get(field), bool):
                raise ValueError(f"matches[{index}].{field} must be a boolean.")

    ambiguous = result.get("ambiguous_findings", [])
    conflicts = result.get("conflicting_duplicate_groups", [])
    unmatched = result.get("unmatched_findings", [])
    false_negatives = result.get("false_negatives", [])
    for name, value in (("ambiguous_findings", ambiguous),
                        ("conflicting_duplicate_groups", conflicts),
                        ("unmatched_findings", unmatched),
                        ("false_negatives", false_negatives)):
        if not isinstance(value, list):
            raise ValueError(f"{name} must be an array when provided.")
    optimal = result.get("optimal_assignment")
    if optimal is not None:
        if not isinstance(optimal, dict):
            raise ValueError("optimal_assignment must be an object.")
        for key in ("maximum_cardinality", "localized_pair_count",
                    "total_line_distance", "scored_forced_matches"):
            if key not in optimal:
                raise ValueError(f"optimal_assignment.{key} is required.")
            _non_negative_int(optimal[key], f"optimal_assignment.{key}")
        if optimal["scored_forced_matches"] != counts["true_positive_count"]:
            raise ValueError("optimal_assignment.scored_forced_matches must equal TP.")
        if optimal["maximum_cardinality"] < counts["true_positive_count"]:
            raise ValueError("optimal maximum cardinality cannot be lower than scored TP.")
    return {**counts, "matches": matches, "ambiguous": ambiguous,
            "conflicts": conflicts, "unmatched": unmatched,
            "false_negatives": false_negatives, "optimal": optimal}


def ratio(a: int, b: int) -> float | None:
    return a / b if b else None


def calculate(result: Any) -> dict[str, Any]:
    valid = validate_match_result(result)
    tp, fp, fn = valid["true_positive_count"], valid["false_positive_count"], valid["false_negative_count"]
    matches = valid["matches"]
    precision, recall = ratio(tp, tp + fp), ratio(tp, tp + fn)
    if precision is None or recall is None:
        f1 = None
    elif precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    reasons: dict[str, int] = {}
    for item in valid["ambiguous"]:
        reason = item.get("ambiguity_reason", "unspecified") if isinstance(item, dict) else "invalid"
        reasons[reason] = reasons.get(reason, 0) + 1
    diagnostics = {
        "ambiguous_finding_count": len(valid["ambiguous"]),
        "ambiguity_reasons": dict(sorted(reasons.items())),
        "conflicting_duplicate_group_count": len(valid["conflicts"]),
        "unmatched_finding_count": len(valid["unmatched"]),
        "false_negative_record_count": len(valid["false_negatives"]),
        "optimal_assignment": valid["optimal"],
        "scoring_note": "Only forced matches contribute to TP and classification/localization accuracy.",
    }
    metrics = {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "severity_accuracy": ratio(sum(x["severity_exact"] for x in matches), len(matches)),
        "localization_accuracy": ratio(sum(x["location_within_tolerance"] for x in matches), len(matches)),
        "duplicate_rate": ratio(valid["duplicate_count"], valid["candidate_count"]),
    }
    return {
        "counts": {
            "true_positives": tp, "false_positives": fp, "false_negatives": fn,
            "duplicates": valid["duplicate_count"], "candidates": valid["candidate_count"],
            "expected": valid["expected_count"],
        },
        "metrics": metrics,
        "diagnostics": diagnostics,
        "interpretation": (
            "null means undefined; pilot metrics are descriptive and do not certify V1 thresholds. "
            "Ambiguous assignments are not scored as true positives."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("match_result")
    parser.add_argument("output")
    args = parser.parse_args()
    try:
        write_json(args.output, calculate(load_json(args.match_result)))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Metrics calculated and matcher-result integrity validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
