# Benchmark V1 — Pilot Specification

## Purpose
Measure whether Code Review Expert improves defect discovery, localization, severity calibration, and restraint compared with a strong generic review baseline.

## Approved V1 target
| Category | Cases |
| --- | ---: |
| Logic and runtime | 10 |
| Security | 10 |
| Architecture | 6 |
| Performance and reliability | 6 |
| Control/clean | 8 |
| **Total** | **40** |

Difficulty target: Easy 30%, Medium 45%, Hard 25%. The pilot is a pipeline-validation subset, not a representative sample.

## Five-case pilot
- logic-001: incorrect boolean business-rule condition.
- security-001: untrusted path segment can escape a configured storage root.
- architecture-001: request-context coupling breaks a service used by a worker.
- performance-001: per-record database access creates an N+1 pattern.
- control-001: valid implementation intended to expose speculative findings.

## Experimental design
Compare a strong generic baseline with the same model plus Code Review Expert. Keep model/version, prompt, files, tools, context budget, sampling settings, and input order constant. The skill package must be the only intended variable. Record unavoidable differences.

Repeat reasoning-sensitive cases at least three times. Preserve raw outputs and metadata; repeated runs are not independent cases.

## Evaluation boundary
Review receives public case files only. Ground truth remains unavailable until raw outputs are frozen. Evaluation is a separate post-review operation in an isolated environment.

## Pilot exit criteria
1. Public manifest and referenced files validate.
2. Evaluator unit and CLI integration tests pass.
3. The real CLI path from raw findings through Markdown report is exercised end-to-end using synthetic test truth.
4. Normalization is deterministic.
5. Matching is conservative and documented.
6. Undefined metrics are null, not silently zero.
7. Reports distinguish measured results from unavailable data.
8. Generated integration artifacts remain in temporary directories; no private ground-truth material is committed publicly.
9. No private answer material is committed publicly.
