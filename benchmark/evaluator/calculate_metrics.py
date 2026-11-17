#!/usr/bin/env python3
"""Calculate metrics from a matcher result."""
from __future__ import annotations
import argparse
import sys
from common import load_json, write_json

def ratio(a: int, b: int):
    return a / b if b else None

def calculate(result: dict) -> dict:
    tp, fp, fn = (int(result[k]) for k in ("true_positive_count", "false_positive_count", "false_negative_count"))
    matches = result.get("matches", [])
    precision, recall = ratio(tp, tp + fp), ratio(tp, tp + fn)
    if precision is None or recall is None: f1 = None
    elif precision + recall == 0: f1 = 0.0
    else: f1 = 2 * precision * recall / (precision + recall)
    metrics = {"precision": precision, "recall": recall, "f1": f1,
      "severity_accuracy": ratio(sum(bool(x.get("severity_exact")) for x in matches), len(matches)),
      "localization_accuracy": ratio(sum(bool(x.get("location_within_tolerance")) for x in matches), len(matches)),
      "duplicate_rate": ratio(int(result.get("duplicate_count", 0)), int(result.get("candidate_count", tp + fp)))}
    return {"counts": {"true_positives": tp, "false_positives": fp, "false_negatives": fn,
      "duplicates": int(result.get("duplicate_count", 0)), "candidates": int(result.get("candidate_count", tp + fp)),
      "expected": int(result.get("expected_count", tp + fn))},
      "metrics": metrics, "interpretation": "null means undefined; pilot metrics are descriptive and do not certify V1 thresholds."}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("match_result"); parser.add_argument("output")
    args = parser.parse_args()
    try: write_json(args.output, calculate(load_json(args.match_result)))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    print("Metrics calculated."); return 0

if __name__ == "__main__": sys.exit(main())
