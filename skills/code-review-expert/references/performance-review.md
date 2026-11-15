# Performance and Reliability Review

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
