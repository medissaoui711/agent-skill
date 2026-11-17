# Code Review Benchmark

A public, evidence-oriented **development dataset** for Code Review Expert. The repository contains 40 synthetic review cases, deterministic evaluator tooling, schemas, and regression tests. Public case materials intentionally omit expected findings and answer keys.

## Dataset status and boundaries

- The manifest is the authoritative public fixture inventory.
- The 40 fixtures are distributed across logic/runtime (10), security (10), architecture (6), performance/reliability (6), and clean/control (8).
- Structural validation confirms fixture inventory, schema shape, referenced files, and repository safety constraints.
- Structural validation does not establish private Ground Truth correctness, independent adjudication, model capability, or achievement of scoring targets.
- The private Ground Truth repository remains separate. The review environment must not access it; only the isolated evaluator may receive eligible reference data after raw review output is frozen.
- Official Benchmark V1 scoring remains blocked pending the private adjudication and release process.

## Safety

- Projects are synthetic fixtures, not production software. Some intentionally contain defects; do not deploy them.
- Never store ground truth, expected locations, answer keys, or answer-revealing outputs here.
- Never execute candidate fixture code as part of dataset validation or release-readiness auditing.
- Preserve raw review output before any reference data is made available to the evaluator.

## Complete case inventory

The table below is generated and regression-checked against `cases/manifest.json`. Category names are normalized for readability; the manifest remains authoritative.

| ID | Category | Case |
| --- | --- | --- |
| logic-001 | Logic / Runtime | Subscription shipping eligibility |
| logic-002 | Logic / Runtime | Concurrent inventory reservation |
| logic-003 | Logic / Runtime | Optional delivery note update |
| logic-004 | Logic / Runtime | Payment capture failure propagation |
| logic-005 | Logic / Runtime | Atomic order placement and inventory reservation |
| logic-006 | Logic / Runtime | React cart state mutation and derived total |
| logic-007 | Logic / Runtime | One-based customer pagination |
| logic-008 | Logic / Runtime | Integer subtotal calculation |
| logic-009 | Logic / Runtime | Promotion eligibility policy composition |
| logic-010 | Logic / Runtime | Payment capture retry idempotency |
| security-001 | Security | User document download endpoint |
| security-002 | Security | Customer search query handling |
| security-003 | Security | Project document authorization |
| security-004 | Security | Remote avatar import |
| security-005 | Security | Administrative report middleware ordering |
| security-006 | Security | Client-controlled report state deserialization |
| security-007 | Security | Document download path containment |
| security-008 | Security | Self-service user update accepts privileged fields |
| security-009 | Security | Authorization credentials included in request logs |
| security-010 | Security | Refresh endpoint accepts access tokens as refresh tokens |
| architecture-001 | Architecture | Invoice service shared by HTTP and worker |
| architecture-002 | Architecture | HTTP framework leakage into project service |
| architecture-003 | Architecture | Circular Spring service constructor dependency |
| architecture-004 | Architecture | Django request object crosses application service boundary |
| architecture-005 | Architecture | Persistence ORM type leaks through invoice service contract |
| architecture-006 | Architecture | Worker discards cancellation context during job processing |
| performance-001 | Performance / Reliability | Order summary aggregation |
| performance-002 | Performance / Reliability | Django customer list query amplification |
| performance-003 | Performance / Reliability | Spring report export executor saturation |
| performance-004 | Performance / Reliability | Repeated pricing rule compilation |
| performance-005 | Performance / Reliability | Go upstream response body lifecycle |
| performance-006 | Performance / Reliability | FastAPI stale product cache after mutation |
| control-001 | Clean / Control | Account profile update flow |
| control-002 | Clean / Control | Notification preference allowlist |
| control-003 | Clean / Control | Parameterized customer email lookup |
| control-004 | Clean / Control | Go request cancellation propagation |
| control-005 | Clean / Control | Spring document ownership authorization |
| control-006 | Clean / Control | React immutable selection memoization |
| control-007 | Clean / Control | FastAPI bounded batch processing |
| control-008 | Clean / Control | Spring structured audit logging |

## Review protocol

Give the reviewer only the case task and files listed in `cases/manifest.json`, using identical baseline instructions. Record model/version, date/time, prompt, tools, sampling settings, raw output, and run number. Do not expose ground truth before freezing the output.

## Finding interchange

A JSON object contains a `findings` array. Each finding requires `title`, `category`, `severity`, `file`, and `description`. Recommended: `line` (1-based), `impact`, `recommendation`. Categories: correctness, security, architecture, performance, reliability, maintainability. Severities: critical, high, medium, low, informational.

## Local validation

Python 3.11+ is required. The experiment freeze utility and its tests also require the pinned JSON Schema runtime dependency:

```bash
python -m pip install -r benchmark/experiments/requirements.txt
python benchmark/evaluator/validate_dataset.py
python -m unittest discover -s benchmark/tests -v
```

The dependency file pins `jsonschema[format]==4.25.1`. The format extra is required for strict JSON Schema `date-time` validation; the freeze utility fails with an actionable error if the dependency is unavailable and never skips format checks.

The evaluator pipeline is composed of four explicit CLI stages:

```bash
python benchmark/evaluator/normalize_findings.py <raw-review.json> <normalized.json>
python benchmark/evaluator/match_findings.py <normalized.json> <isolated-ground-truth.json> <matches.json>
python benchmark/evaluator/calculate_metrics.py <matches.json> <metrics.json>
python benchmark/evaluator/generate_report.py <metrics.json> <report.md>
```

Run matching only in the isolated evaluation environment after raw review output is frozen. The integration suite invokes these real CLI entry points using synthetic inputs in temporary directories; it never reads the private ground-truth repository and never writes generated artifacts into the checkout.

See [SCORING_POLICY.md](SCORING_POLICY.md) for matching and scoring semantics.

## Experimental evidence status

The earlier statement that repeated baseline/skill-enabled trials had been run is withdrawn from this documentation until reproducible run records can be produced and audited. During this documentation audit, no experiment artifacts or reproducibility records sufficient to substantiate that statement were identified in either repository's searchable contents.

Accordingly, this repository currently makes **no claim that baseline/skill-enabled trials have been completed**, and publishes no model-performance measurements from such trials. A future experiment report must include, at minimum:

- Dataset version and manifest hash, plus the public repository commit.
- Model/provider and exact model version; date/time and run identifier.
- Identical task inputs and recorded baseline/skill prompts.
- Sampling parameters, enabled tools, and execution environment.
- Frozen raw outputs and their cryptographic hashes.
- Evaluator version, metric artifacts, and any exclusions or failures.
- Confirmation that Ground Truth was not exposed before output freeze.

If records are unavailable, the correct status is `NOT_RUN_OR_NOT_EVIDENCED`, not a presumed successful experiment.

## Scoring and release interpretation

The full V1 target thresholds are documented in [SCORING_POLICY.md](SCORING_POLICY.md). They are targets, not achieved results. Do not apply them as pass/fail certification to the pilot or infer that a 40-case structural validation establishes those metrics.

Private Ground Truth currently remains provisional: findings have not been independently adjudicated and are not scoring-eligible. The public fixture set is suitable for continued evaluator engineering and calibration work, but **Official Benchmark V1 remains NO-GO and scoring remains BLOCKED_PENDING_ADJUDICATION**.

## Expansion history

The 40-case inventory was assembled incrementally: the original five-case pilot was expanded through Batches A, B, C, and D. This history describes fixture authoring sequence only; it does not imply that any batch was independently representative, adjudicated, or experimentally evaluated.
