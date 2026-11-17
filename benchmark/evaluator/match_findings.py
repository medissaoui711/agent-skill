#!/usr/bin/env python3
"""Conservative matcher. Supply private ground truth only in isolated evaluation."""
from __future__ import annotations
import argparse
import sys
from typing import Any
from common import deduplicate_findings, load_json, normalize_findings, write_json

def match(findings: list[dict[str, Any]], truth_payload: Any, tolerance: int = 3) -> dict[str, Any]:
    if not isinstance(truth_payload, dict) or not isinstance(truth_payload.get("findings"), list):
        raise ValueError("Ground truth must be an object containing a findings array.")
    expected = normalize_findings(truth_payload)
    unique, duplicate_count = deduplicate_findings(findings)
    used, matches, unmatched = set(), [], []
    for candidate in unique:
        possible = []
        for index, reference in enumerate(expected):
            if index in used or candidate["file"] != reference["file"] or candidate["category"] != reference["category"]:
                continue
            a, b = candidate.get("line"), reference.get("line")
            distance = None if a is None or b is None else abs(a - b)
            if distance is None or distance <= tolerance:
                possible.append((float("inf") if distance is None else distance, index, distance))
        possible.sort(key=lambda item: (item[0], item[1]))
        if not possible or (len(possible) > 1 and possible[0][0] == possible[1][0]):
            unmatched.append(candidate)
            continue
        _, index, distance = possible[0]
        used.add(index)
        reference = expected[index]
        location_ok = distance is not None and distance <= tolerance
        matches.append({
            "candidate": candidate,
            "expected": reference,
            "severity_exact": candidate["severity"] == reference["severity"],
            "location_within_tolerance": location_ok,
            "line_distance": distance
        })
    false_negatives = [item for i, item in enumerate(expected) if i not in used]
    return {
        "true_positive_count": len(matches),
        "false_positive_count": len(unmatched) + duplicate_count,
        "false_negative_count": len(false_negatives),
        "duplicate_count": duplicate_count,
        "candidate_count": len(findings),
        "expected_count": len(expected),
        "matches": matches,
        "unmatched_findings": unmatched,
        "false_negatives": false_negatives,
        "matching_policy": {
            "path_and_category_exact": True,
            "line_tolerance": tolerance,
            "missing_line": "may match on path/category but does not count as localized",
            "ambiguous_matches": "unmatched"
        }
    }

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("findings", help="Normalized findings JSON")
    parser.add_argument("ground_truth", help="Private ground-truth JSON; isolated environment only")
    parser.add_argument("output", help="Match result JSON")
    parser.add_argument("--line-tolerance", type=int, default=3)
    args = parser.parse_args()
    if args.line_tolerance < 0:
        parser.error("--line-tolerance must be >= 0")
    try:
        candidates = normalize_findings(load_json(args.findings))
        result = match(candidates, load_json(args.ground_truth), args.line_tolerance)
        write_json(args.output, result)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("Matching complete. Independently adjudicate ambiguous and unmatched findings.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
