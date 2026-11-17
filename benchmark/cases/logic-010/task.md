# Review task: Payment capture worker

Review the supplied TypeScript worker used by a Node.js job processor.

## Contract
- The queue may deliver the same job more than once, including concurrently.
- A given idempotency key must cause at most one external payment capture.
- A worker crash or retry between the external capture and local completion persistence must not create a second charge.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
