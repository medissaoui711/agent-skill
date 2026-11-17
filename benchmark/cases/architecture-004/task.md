# Review task: Report application service boundary

Review the supplied Django application service.

## Contract
- The application service is shared by HTTP views and scheduled management commands.
- Application services must accept explicit application inputs, not framework transport objects.
- HTTP authentication and query parsing belong in the Django adapter; the service must remain callable without an HttpRequest.
- Report actionable architectural defects only when supported by the supplied code and contract. Do not modify files or claim tests were run.
