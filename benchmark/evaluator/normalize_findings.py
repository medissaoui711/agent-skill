#!/usr/bin/env python3
"""Normalize model review JSON into the evaluator interchange format."""
from __future__ import annotations
import argparse
import sys
from common import load_json, normalize_findings, write_json

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Review output JSON")
    parser.add_argument("output", help="Normalized JSON destination")
    args = parser.parse_args()
    try:
        findings = normalize_findings(load_json(args.input))
        write_json(args.output, {"findings": findings, "finding_count": len(findings)})
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Normalized {len(findings)} finding(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
