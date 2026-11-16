# Engineering Review: Architecture, Performance, and Reliability

This reference consolidates architecture/design review and performance/reliability review. Preserve both perspectives during assessment; do not treat this document as an architecture-only checklist.

---

## Part I — Architecture and Design

## Boundaries and coupling

- Does the change respect established module and service boundaries?
- Are dependencies directed consistently?
- Is business logic placed in the appropriate layer?
- Does the change introduce circular dependencies or duplicate sources of truth?
- Are abstractions justified by real variation rather than speculation?

## Contracts and evolution

- Are public APIs, events, schemas, and shared types compatible?
- Are versioning and deprecation handled safely?
- Are database migrations compatible with rolling deployments?
- Can old and new application versions coexist during rollout?
- Are feature flags and rollback paths safe?

## Multi-tenancy and ownership

- Is tenant context derived from a trusted identity, not user-controlled input?
- Are tenant constraints enforced in repositories/queries and background jobs?
- Are caches, object keys, queues, and search indexes tenant-scoped?
- Can asynchronous tasks execute with the correct tenant and actor context?

## Resilience and operations

- Are service boundaries protected by timeouts and bounded retries?
- Are idempotency and deduplication addressed?
- Are critical workflows observable with correlation identifiers?
- Are health/readiness signals meaningful?
- Are new operational dependencies documented?

## Design quality

- Is the design simpler than reasonable alternatives?
- Is state ownership explicit?
- Are side effects visible and controlled?
- Are domain invariants enforced at the correct boundary?
- Does the design fit the project's existing architecture rather than introduce an unnecessary parallel system?


---

## Part II — Performance and Reliability

## Algorithms and data access

- Is algorithmic complexity appropriate for expected input sizes?
- Are database queries bounded and indexed?
- Are N+1 queries, repeated serialization, or redundant network calls introduced?
- Are pagination and batch sizes bounded?
- Are large collections streamed or processed incrementally where appropriate?

## Resource lifecycle

- Are connections, files, streams, and subscriptions closed?
- Can memory grow without bound?
- Are caches bounded, invalidated correctly, and scoped safely?
- Are background jobs limited by concurrency and queue capacity?
- Are expensive operations moved off latency-sensitive paths when justified?

## Concurrency and reliability

- Are shared writes race-safe?
- Are locks, transactions, and optimistic concurrency used appropriately?
- Are retries bounded with backoff and jitter where appropriate?
- Are timeouts and cancellation propagated?
- Can duplicate events or at-least-once delivery corrupt state?
- Are overload and dependency outages handled predictably?

## Measurement

- Distinguish measured regressions from theoretical risks.
- State workload assumptions and expected scale.
- Do not invent latency, throughput, memory, or cost numbers.
- Recommend profiling or load testing when static inspection cannot establish impact.
