# Review task: Order placement transaction

Review the supplied Spring service for business correctness and failure handling.

## Contract
- Creating an order and reserving its inventory form one atomic business operation.
- If inventory reservation fails, no order may remain persisted.
- Successful completion must mean both order persistence and reservation succeeded.
- Report only actionable defects supported by the supplied code. Do not modify files or claim tests were run.
