# Code Review Benchmark

A public, evidence-oriented benchmark for Code Review Expert. The original five-case pilot is retained and Phase 5D Batch A adds seven synthetic cases (12 public cases total). Public case materials intentionally omit expected findings and answer keys.

## Safety and separation
- Projects are synthetic fixtures, not production software. Some intentionally contain defects; do not deploy them.
- Never store ground truth, expected locations, answer keys, or answer-revealing outputs here.
- The review environment must not access the private ground-truth repository.
- Only the isolated evaluator receives ground truth after raw review output is frozen.

## Case inventory

| ID | Area | Purpose |
| --- | --- | --- |
| logic-001 | Logic | Boolean business-rule reasoning |
| logic-002 | Logic | Concurrent inventory reservation |
| logic-003 | Logic | Optional field update semantics |
| logic-004 | Logic | Payment failure propagation |
| security-001 | Security | Path traversal and filesystem boundaries |
| security-002 | Security | Safe SQL query construction |
| security-003 | Security | Project document authorization |
| security-004 | Security | Server-side URL retrieval boundary |
| architecture-001 | Architecture | Request-context coupling across entry points |
| performance-001 | Performance | N+1 database access |
| control-001 | Control | Clean implementation / false-positive restraint |
| control-002 | Control | Allowlist validation and authenticated identity |

The manifest is the authoritative list of currently implemented public cases. Batch A is a controlled expansion slice, not a representative 40-case benchmark.

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

## Development-stage limitation
The 12-case set validates the expanding pipeline, not general model capability. Do not publish capability claims or claim V1 thresholds from these cases. Continue the controlled expansion toward 40 cases and run repeated baseline/skill-enabled trials. Independent human adjudication remains a pre-commercial readiness requirement; current provisional labels are not independently adjudicated or scoring-eligible.


## Phase 5D Batch B

Batch B adds nine synthetic cases to the 12-case Batch A inventory (21 public fixtures total):
- Logic: logic-005 (Spring transaction boundary), logic-006 (React state mutation), logic-007 (Django pagination).
- Security: security-005 (Express middleware ordering), security-006 (unsafe Django deserialization), security-007 (Go path containment).
- Architecture: architecture-002 (Go HTTP coupling), architecture-003 (Spring circular dependency).
- Control: control-003 (parameterized Django query).

The validator requires the exact 21-case inventory. This remains a development dataset, not an independently adjudicated or scoring-eligible benchmark.


### CI workflow
The benchmark validation workflow also runs for pull requests targeting `feat/phase-5d-batch-a`, so the chained Batch B PR receives the same Python 3.11/3.12 dataset and evaluator checks. The workflow uses read-only repository permissions and does not execute fixture project code.
