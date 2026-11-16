# Review Workflow

## Phase A — Intake and baseline

Record:

- Review objective and requested depth.
- Base and head references, commit range, and repository state.
- Changed files and change size.
- Project-specific instructions and coding/security standards.
- Relevant runtime, framework, deployment model, and data stores.

If the base/head relationship is unknown, do not guess. State the limitation and review only the material actually provided.

## Phase B — System context

Read the nearest relevant instructions and documentation. Identify:

- Application entry points and request/event lifecycle.
- Module boundaries and dependency direction.
- Authentication and authorization mechanisms.
- Data ownership, tenant boundaries, and persistence model.
- External APIs, queues, caches, file/object storage, and background workers.
- Configuration and secret-management approach.
- Test layers and CI/release gates.

## Phase C — Change impact map

For each changed file, record:

| Area | Questions |
|---|---|
| Callers | Who invokes this code? Are all call sites compatible? |
| Inputs | Can input be malformed, untrusted, oversized, or missing? |
| State | What state changes? Is it shared or concurrent? |
| Data | Are schema, constraints, ownership, and migrations correct? |
| Access | Are authentication, authorization, and tenant checks enforced? |
| Outputs | Are response contracts, events, and UI states preserved? |
| Failure | What happens on timeout, retry, partial failure, or rollback? |
| Operations | Does this affect configuration, deployment, logs, or monitoring? |

## Phase D — Focused technical review

Review in this order:

1. Functional correctness and regressions.
2. Security, privacy, and authorization.
3. Data integrity and transaction behavior.
4. Architecture and contract compatibility.
5. Reliability, concurrency, and failure handling.
6. Performance and resource consumption.
7. Tests and observability.
8. Maintainability and documentation.

Use the specialized reference checklists. Follow execution paths across file boundaries where needed.

## Phase E — Verify

For every potential issue:

1. Reproduce mentally from the actual code path or execute a safe targeted test.
2. Confirm reachability and triggering conditions.
3. Check for existing mitigations.
4. Confirm the issue is introduced by the reviewed change, or label it pre-existing.
5. Capture exact evidence and location.
6. Assign severity based on impact and confidence based on evidence.

Do not infer that an absent test means the behavior is broken. Report a test gap only when the gap creates meaningful risk.

## Phase F — Report and decision

Present:

1. Overall recommendation: Approve, Approve with follow-up, or Request changes.
2. Findings ordered Critical → High → Medium → Low.
3. Positive verification and checks actually executed.
4. Important unverified areas and assumptions.
5. Scope limitations.

A recommendation is advisory. The repository owner retains merge authority.
