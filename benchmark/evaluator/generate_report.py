#!/usr/bin/env python3
"""Render a Markdown report from metrics JSON."""
from __future__ import annotations
import argparse
import sys
from pathlib import Path
from common import load_json

def render(data: dict, title: str) -> str:
    def fmt(value): return "N/A" if value is None else f"{value:.3f}"
    lines = [f"# {title}", "", "> Pilot results are descriptive only; five cases do not certify V1 thresholds.", "",
             "## Counts", "", "| Measure | Count |", "| --- | ---: |"]
    for key, value in data["counts"].items(): lines.append(f"| {key.replace('_', ' ').title()} | {value} |")
    lines += ["", "## Metrics", "", "| Metric | Value |", "| --- | ---: |"]
    for key, value in data["metrics"].items(): lines.append(f"| {key.replace('_', ' ').title()} | {fmt(value)} |")
    lines += ["", "## Interpretation", "", data.get("interpretation", "Review raw matches and adjudicate ambiguity."), ""]
    return "\n".join(lines)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("metrics_json"); parser.add_argument("output_markdown")
    parser.add_argument("--title", default="Code Review Benchmark Results")
    args = parser.parse_args()
    try:
        report = render(load_json(args.metrics_json), args.title)
        target = Path(args.output_markdown); target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(report, encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr); return 1
    print(f"Report written to {args.output_markdown}"); return 0

if __name__ == "__main__": sys.exit(main())
