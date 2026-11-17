# Review task: Payment capture handler

Review the supplied Go HTTP handler for correctness and failure behavior.

## Contract
- A payment is considered captured only after the payment provider confirms success.
- If capture fails, the client must receive a non-success response and the failure must be recorded.
- The handler must not report a successful capture when the provider operation failed.
- Return actionable findings only, with exact evidence, triggering conditions, impact, and a practical fix. Do not modify files or claim tests were run.
