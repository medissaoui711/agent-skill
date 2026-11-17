# Review task: Inventory reservation updates

Review the supplied TypeScript service for correctness under concurrent requests.

## Contract
- Each reservation must be applied against the latest available inventory.
- Inventory must never become negative.
- A reservation succeeds only when enough units remain.
- The service may be called concurrently by multiple request handlers.
- Return actionable findings only, with file, line, severity, triggering conditions, impact, and a practical fix. Do not modify files or claim tests were run.
