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

## Controlled expansion status

The original five pilot cases remain unchanged. Phase 5D Batch A adds seven cases:
- logic-002: concurrent inventory reservation.
- logic-003: optional delivery note semantics.
- logic-004: payment capture failure propagation.
- security-002: Django SQL query construction.
- security-003: project document authorization.
- security-004: server-side avatar URL retrieval.
- control-002: notification preference allowlist.

The public manifest validator must validate the complete 12-case set. The private reference records remain separate and are not part of this repository.

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


## Phase 5D Batch B implementation scope

Batch B adds nine fixtures to the existing 12-case public set, bringing the manifest target for this development slice to 21 cases. The additions cover Spring transaction boundaries, React state mutation, Django pagination, Express middleware ordering, unsafe deserialization, Go filesystem containment, Go service-layer coupling, Spring circular dependencies, and a clean parameterized-query control. Private expected findings remain outside this repository. The 21-case inventory is not a representative 40-case benchmark and does not authorize capability claims or scoring.


## Phase 5D Batch C implementation scope

Batch C adds nine fixtures to the existing 21-case inventory, bringing the public development slice to 30 cases. The additions cover Go integer overflow, Spring promotion-policy composition, Node.js payment retry idempotency, Spring mass assignment, Express secret-bearing logs, FastAPI refresh-token purpose validation, Django application-service request coupling, Prisma persistence-type leakage, and Go worker cancellation-context ownership. Private expected findings remain in the restricted repository. This 30-case development slice is not a representative 40-case benchmark and does not authorize capability claims or scoring.


## Phase 5D Batch D implementation scope

Batch D completes the controlled public fixture expansion from 30 to 40 cases. It adds five performance/reliability fixtures (Django ORM query amplification, Spring executor saturation, Node.js repeated rule compilation, Go response-body lifecycle, and FastAPI cache invalidation) and five clean/control fixtures (Go cancellation propagation, Spring object ownership authorization, React immutable memoization, FastAPI bounded batch processing, and Spring structured audit logging). The public validator enforces the exact 40-case inventory. Private expected findings remain restricted; this completion does not establish independent adjudication, scoring eligibility, or achievement of target metrics.
