# Review task: Account profile update flow

Review the supplied modules for correctness, authorization, and data integrity.

## Contract
- The authenticated user may update only their own profile.
- The request body may contain only displayName and locale.
- The repository performs a parameterized update scoped by user ID.
- A missing profile returns 404; invalid fields return 400.
- The controller and service are part of the supplied execution path.

Report only actionable defects supported by the supplied code. Avoid speculative concerns about omitted infrastructure. Do not modify files or claim tests were run.
