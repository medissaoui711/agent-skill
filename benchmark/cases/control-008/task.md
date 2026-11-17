# Clean Review Task — Spring audit event

## Contract
The audit event may include actor ID, action, and target ID. Authentication credentials, access tokens, passwords, cookies, and raw request headers must never be logged. The logger supports structured key-value fields. Review the supplied implementation against this contract.

## Review scope
Return an empty findings array if no secret exposure or other actionable defect is present. Do not speculate about logger internals.
