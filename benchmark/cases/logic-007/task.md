# Review task: Customer list pagination

Review the supplied Django view for pagination correctness.

## Contract
- Page numbers are one-based.
- Page 1 returns the first PAGE_SIZE records, page 2 returns the next PAGE_SIZE, and so on.
- The response must preserve the requested page number and must not skip or repeat records between adjacent pages.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
