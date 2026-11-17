# Review task: Customer email lookup

Review the supplied Django data-access function for query safety and scope.

## Contract
- The email value is supplied by an authenticated user and must be treated as untrusted data.
- Lookup must use the database adapter's parameterized query mechanism.
- User input must not alter SQL syntax or predicates.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
