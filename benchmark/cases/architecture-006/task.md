# Review task: Go worker lifecycle and cancellation ownership

Review the supplied Go worker.

## Contract
- Run receives the lifecycle context owned by the worker host.
- Every job-processing operation must inherit that context so shutdown cancellation and deadlines propagate through the complete job call tree.
- The processor must not be detached from the worker lifecycle by creating a new root context.
- Report actionable architectural defects only when supported by the supplied code and contract. Do not modify files or claim tests were run.
