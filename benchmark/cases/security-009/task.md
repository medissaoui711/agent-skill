# Review task: Webhook request error handling

Review the supplied Express handler.

## Contract
- Request headers may contain bearer credentials and provider secrets.
- Application logs are accessible to operational staff and log aggregation services that are not authorized to receive authentication credentials.
- Error diagnostics must not persist authorization headers, cookies, API keys, or other secrets.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
