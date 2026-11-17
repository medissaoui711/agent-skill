# Review task: Project archival service

Review the supplied Go application service and repository boundary.

## Contract
- The application service must be independent of HTTP frameworks.
- Transport handlers authenticate requests and pass an explicit actor identifier and standard context to the application layer.
- The same service must be callable from HTTP and background-job entry points.
- Report actionable architectural defects supported by the supplied code. Do not modify files or claim tests were run.
