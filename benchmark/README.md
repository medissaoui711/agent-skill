# Code Review Benchmark

A public, evidence-oriented benchmark for Code Review Expert. The pilot contains five synthetic review cases. Public case materials intentionally omit expected findings and answer keys.

## Safety and separation
- Projects are synthetic fixtures, not production software. Some intentionally contain defects; do not deploy them.
- Never store ground truth, expected locations, answer keys, or answer-revealing outputs here.
- The review environment must not access the private ground-truth repository.
- Only the isolated evaluator receives ground truth after raw review output is frozen.

## Pilot inventory
| ID | Area | Purpose |
| --- | --- | --- |
| logic-001 | Logic | Boolean business-rule reasoning |
| security-001 | Security | Path traversal and filesystem boundaries |
| architecture-001 | Architecture | Request-context coupling across entry points |
| performance-001 | Performance | N+1 database access |
| control-001 | Control | Clean implementation / false-positive restraint |

The control case is not labelled as clean in its task. Its expected result is private.

## Review protocol
Give the reviewer only the case task and files listed in `cases/manifest.json`, using identical baseline instructions. Record model/version, date, prompt, tools, sampling settings, raw output, and run number. Do not expose ground truth before freezing the output.

## Finding interchange
A JSON object contains a `findings` array. Each finding requires `title`, `category`, `severity`, `file`, and `description`. Recommended: `line` (1-based), `impact`, `recommendation`. Categories: correctness, security, architecture, performance, reliability, maintainability. Severities: critical, high, medium, low, informational.

## Local validation
Requires Python 3.11+ and the standard library:
```bash
python benchmark/evaluator/validate_dataset.py
python -m unittest discover -s benchmark/tests -v
```

The evaluator pipeline is composed of four explicit CLI stages:
```bash
python benchmark/evaluator/normalize_findings.py <raw-review.json> <normalized.json>
python benchmark/evaluator/match_findings.py <normalized.json> <isolated-ground-truth.json> <matches.json>
python benchmark/evaluator/calculate_metrics.py <matches.json> <metrics.json>
python benchmark/evaluator/generate_report.py <metrics.json> <report.md>
```
Run matching only in the isolated evaluation environment after raw review output is frozen. The integration suite invokes these real CLI entry points using synthetic inputs in temporary directories; it never reads the private ground-truth repository and never writes generated artifacts into the checkout.

See [SCORING_POLICY.md](SCORING_POLICY.md) for matching and scoring semantics.

## Pilot limitation
Five cases validate the pipeline, not general model capability. Do not publish capability claims or claim V1 thresholds from this pilot. Expand to 40 cases, independently review ground truth, and run repeated baseline/skill-enabled trials.
