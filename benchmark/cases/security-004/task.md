# Review task: Remote avatar import

Review the supplied Spring service for server-side request security.

## Contract
- The service imports an avatar image from a URL submitted by an authenticated user.
- Only public HTTPS image endpoints are permitted.
- Internal services, loopback interfaces, link-local addresses, and private network destinations must not be reachable through this feature.
- Redirect behavior must not bypass destination restrictions.
- Return concrete findings with prerequisites, impact, and practical remediation. Do not modify files or claim tests were run.
