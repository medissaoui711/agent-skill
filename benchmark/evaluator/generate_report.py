#!/usr/bin/env python3
"""Render an integrity-aware Markdown report from metrics JSON."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from typing import Any
from common import load_json


def _cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def _format_metric(value: Any) -> str:
    if value is None:
        return "N/A (undefined)"
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("Metric values must be numbers or null.")
    return f"{value:.3f}"


def render(data: dict, title: str) -> str:
    if not isinstance(data, dict) or not isinstance(data.get("counts"), dict) or not isinstance(data.get("metrics"), dict):
        raise ValueError("Metrics document must contain counts and metrics objects.")
    lines = [f"# {_cell(title)}", "",
             "> Pilot results are descriptive only; five cases do not certify V1 thresholds.", "",
             "## Counts", "", "| Measure | Count |", "| --- | ---: |"]
    for key, value in sorted(data["counts"].items()):
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            raise ValueError(f"Count {key} must be a non-negative integer.")
        lines.append(f"| {_cell(key.replace('_', ' ').title())} | {value} |")
    lines += ["", "## Metrics", "", "| Metric | Value |", "| --- | ---: |"]
    for key, value in sorted(data["metrics"].items()):
        lines.append(f"| {_cell(key.replace('_', ' ').title())} | {_format_metric(value)} |")

    diagnostics = data.get("diagnostics", {})
    if not isinstance(diagnostics, dict):
        raise ValueError("diagnostics must be an object when provided.")
    lines += ["", "## Evaluation diagnostics", ""]
    lines.append(f"- Ambiguous findings not scored as TP: **{diagnostics.get('ambiguous_finding_count', 0)}**")
    lines.append(f"- Conflicting duplicate groups quarantined: **{diagnostics.get('conflicting_duplicate_group_count', 0)}**")
    lines.append(f"- Unmatched candidate findings: **{diagnostics.get('unmatched_finding_count', 0)}**")
    optimal = diagnostics.get("optimal_assignment")
    if optimal is not None:
        if not isinstance(optimal, dict):
            raise ValueError("diagnostics.optimal_assignment must be an object or null.")
        lines += ["", "### Optimal assignment versus scored matches", "",
                  "| Measure | Count |", "| --- | ---: |",
                  f"| Maximum achievable cardinality | {optimal.get('maximum_cardinality', 'N/A')} |",
                  f"| Localized pairs in selected optimum | {optimal.get('localized_pair_count', 'N/A')} |",
                  f"| Forced matches actually scored | {optimal.get('scored_forced_matches', 'N/A')} |",
                  f"| Total line distance | {optimal.get('total_line_distance', 'N/A')} |"]
    if diagnostics.get("ambiguity_reasons"):
        lines += ["", "### Ambiguity reasons", ""]
        reasons = diagnostics["ambiguity_reasons"]
        if not isinstance(reasons, dict):
            raise ValueError("ambiguity_reasons must be an object.")
        for reason, count in sorted(reasons.items()):
            if isinstance(count, bool) or not isinstance(count, int) or count < 0:
                raise ValueError("Ambiguity reason counts must be non-negative integers.")
            lines.append(f"- {_cell(reason)}: {count}")
    lines += ["", "## Interpretation", "",
              str(data.get("interpretation", "Review raw matches and adjudicate ambiguity.")), ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_json")
    parser.add_argument("output_markdown")
    parser.add_argument("--title", default="Code Review Benchmark Results")
    args = parser.parse_args()
    try:
        report = render(load_json(args.metrics_json), args.title)
        target = Path(args.output_markdown)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(report, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Report written to {args.output_markdown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
