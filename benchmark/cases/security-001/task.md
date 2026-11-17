# Review task: User document download endpoint

Review the supplied Node.js modules for security and correctness.

## Contract
- Files are stored under configured DOCUMENT_ROOT.
- A user may download only a document whose owner ID matches the authenticated user's ID.
- The route receives an authenticated user object and an untrusted documentName route parameter.
- The application must never read files outside DOCUMENT_ROOT.

Identify concrete exploitable paths and explain required conditions. Do not assume a mitigation unless visible in the supplied code. Do not modify files or claim execution.
