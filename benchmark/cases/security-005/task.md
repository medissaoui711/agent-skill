# Review task: Administrative report endpoint

Review the supplied Express router for authentication and role enforcement.

## Contract
- Every route under /admin requires an authenticated principal.
- Report retrieval requires the admin role.
- Route registration order must not permit a request to reach a protected handler before the required middleware.
- Return concrete findings with a reachable request path and impact. Do not modify files or claim tests were run.
