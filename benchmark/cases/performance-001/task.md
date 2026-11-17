# Review task: Order summary aggregation

Review the supplied module for performance and reliability issues.

## Contract
- Input is an array of orders, each with a customerId.
- The database adapter supports getCustomerById(id) and getCustomersByIds(ids).
- The summary includes each order and its customer's display name.
- Assume input may contain thousands of orders and repeated customer IDs.

Identify measurable or structurally evident performance risks. Distinguish confirmed code-path issues from workload-dependent impact. Do not modify files or claim execution.
