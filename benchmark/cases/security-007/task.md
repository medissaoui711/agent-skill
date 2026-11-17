# Review task: Stored document download

Review the supplied Go HTTP handler for filesystem path safety.

## Contract
- The name query parameter is untrusted.
- Downloads must be restricted to files located inside the configured storage root.
- Parent-directory segments and absolute paths must not permit access to other filesystem locations.
- Return concrete findings with an attack path, impact, and practical remediation. Do not modify files or claim tests were run.
