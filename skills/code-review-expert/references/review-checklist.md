# General Code Review Checklist

Use only relevant checks; do not mechanically report every unchecked item.

## Correctness

- Are requirements and edge cases handled?
- Are null, empty, invalid, boundary, and oversized inputs handled?
- Are state transitions valid and complete?
- Are errors propagated or handled without hiding failures?
- Are async operations awaited and cancellation handled correctly?
- Are retries idempotent and bounded?
- Are sorting, filtering, pagination, and time-zone semantics correct?
- Are API/UI contracts and backward compatibility preserved?

## Data integrity

- Are database constraints and indexes appropriate?
- Are writes transactional where required?
- Can partial failure leave inconsistent state?
- Are migrations safe for existing production data?
- Are destructive operations guarded and recoverable?
- Are duplicate submissions and concurrent updates handled?
- Are tenant/user ownership constraints applied to every relevant query?

## API and integration

- Are request and response schemas validated?
- Are status codes and error formats consistent?
- Are timeouts, retries, rate limits, and external failures handled?
- Are webhook signatures and replay protections validated?
- Are pagination and API version changes handled?
- Are external dependency assumptions documented and tested?

## Frontend and UX

- Are loading, empty, success, and error states represented?
- Are form validation and server validation consistent?
- Are permissions enforced server-side, not only hidden in UI?
- Are keyboard, focus, labels, and accessible semantics preserved?
- Are stale requests, race conditions, and optimistic updates handled?
- Are user-visible errors safe and useful?

## Tests

- Do tests cover changed behavior and important regressions?
- Are assertions meaningful rather than implementation-specific?
- Are negative and authorization cases covered?
- Are integration boundaries tested where appropriate?
- Are tests deterministic and isolated?
- Do CI scripts actually execute the relevant test suites?

## Operations and maintainability

- Are configuration changes documented?
- Are logs useful without leaking secrets or personal data?
- Are critical failures observable?
- Are resource cleanup and connection lifecycle correct?
- Are dependencies necessary, supported, and pinned appropriately?
- Is complexity justified and consistent with project conventions?
