# Review task: Customer search endpoint

Review the supplied Django view for security and data-access correctness.

## Contract
- The search term is supplied by an authenticated user and is untrusted.
- Search must match customer names using the database's supported parameterized query mechanism.
- The endpoint must not allow input to alter SQL structure or predicates.
- Return only concrete, actionable findings. Explain exploit prerequisites and impact. Do not modify files or claim execution.
