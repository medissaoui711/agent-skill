# Reliability Review Task — FastAPI product cache

## Contract
The process-local cache stores product representations by product ID. Product updates must become visible to subsequent reads handled by the same process. The service is single-process for this exercise; do not assume a distributed cache or external invalidation mechanism. Existing cache TTL is a fallback, not the primary consistency mechanism.

## Review scope
Inspect the supplied service. Identify any cache invalidation or stale-read defect supported by the code and contract. Do not claim cross-process behavior.
