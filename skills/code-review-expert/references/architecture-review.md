# Architecture and Design Review

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
