# Review task: Notification preference update

Review the supplied Express route for correctness, authorization, and input handling.

## Contract
- An authenticated user may update only their own notification preference.
- The only accepted preference values are `email`, `sms`, and `none`.
- Invalid values must be rejected without changing stored state.
- The update must use the authenticated principal rather than a caller-controlled identity.
- Report only actionable defects supported by the supplied code. Do not invent issues outside the declared scope. Do not modify files or claim tests were run.
