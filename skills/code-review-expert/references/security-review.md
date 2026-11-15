# Security and Privacy Review

Use a threat-informed approach. Identify assets, actors, trust boundaries, entry points, and abuse cases relevant to the change.

## Identity and access control

- Is authentication required on protected operations?
- Is authorization checked on the server for every object/action?
- Are role and permission checks deny-by-default?
- Are tenant and ownership filters applied before returning or mutating data?
- Can IDs be substituted to access another user's or tenant's resources (IDOR/BOLA)?
- Are privilege changes and administrative actions protected and audited?

## Input and output handling

- Are inputs validated with strict schemas and safe bounds?
- Are SQL/NoSQL queries parameterized?
- Are shell commands, templates, and dynamic expressions protected from injection?
- Is output context-encoded to prevent XSS?
- Are file paths canonicalized and traversal prevented?
- Are uploads constrained by type, size, storage location, and content inspection where appropriate?
- Are redirects and URL fetches restricted to prevent open redirect and SSRF?

## Secrets and sensitive data

- Are credentials kept out of source, client bundles, logs, errors, and URLs?
- Are secrets stored and rotated through an appropriate secret manager?
- Is sensitive data minimized, encrypted in transit, and protected at rest as required?
- Are logs, analytics, and telemetry scrubbed?
- Are retention, deletion, and export behaviors appropriate?

## Web and API controls

- Are CORS policies explicit and narrow?
- Are CSRF protections appropriate to the authentication model?
- Are cookies configured securely (Secure, HttpOnly, SameSite as appropriate)?
- Are rate limits and abuse controls applied to sensitive endpoints?
- Are webhook signatures, timestamps, and replay windows validated?
- Are security headers and TLS assumptions appropriate?

## Dependencies and infrastructure

- Are new dependencies necessary and trustworthy?
- Are versions constrained and vulnerability checks part of the workflow?
- Are debug endpoints, permissive defaults, and development secrets excluded from production?
- Are network egress and service permissions least-privileged?

## Reporting discipline

Do not claim an exploit without a plausible, evidence-backed path. Describe prerequisites and impact. Avoid including exploit payloads that expose real systems or data. Treat scanner output as leads requiring validation, not proof.
