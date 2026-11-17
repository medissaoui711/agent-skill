# Review task: Invoice application module boundary

Review the supplied TypeScript invoice service.

## Contract
- The invoice service is an application-layer module consumed by HTTP handlers and background workers.
- Its public contract must expose application/domain types, not generated persistence-client types.
- Persistence adapters own ORM queries and map database records into application contracts.
- Report actionable architectural defects only when supported by the supplied code and contract. Do not modify files or claim tests were run.
