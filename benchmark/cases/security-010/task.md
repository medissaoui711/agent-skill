# Review task: FastAPI token refresh lifecycle

Review the supplied token refresh helper.

## Contract
- Only tokens explicitly issued with token_type="refresh" may be presented to the refresh operation.
- Access and refresh tokens use the same signing key in this service.
- Signature and expiration validation are required but are not sufficient to establish a token's purpose.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
