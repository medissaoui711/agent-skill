# Review task: Project document endpoint

Review the supplied Go HTTP handler for authorization vulnerabilities.

## Contract
- Users may read documents belonging to projects where they are active members.
- The authenticated principal is available in the request context.
- Project and document identifiers in the URL are untrusted.
- A user must not access another project's documents by changing an identifier.
- Return actionable findings with a concrete attack path, impact, and practical fix. Do not modify files or claim tests were run.
