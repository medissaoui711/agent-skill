# Performance Review Task — Go proxy handler

## Contract
The handler forwards an upstream response to the client. The HTTP client returns a response whose body must be closed on every path after a successful request. The handler must preserve upstream status and body bytes.

## Review scope
Inspect the supplied handler. Report concrete resource-lifecycle defects only; do not assume the upstream server behavior or request volume.
