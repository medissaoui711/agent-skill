# Repository contract for this fixture

The controller passes the authenticated user ID to the service. The repository implementation is represented by this contract:
- updateByUserId(userId, changes) uses a parameterized statement.
- Its update predicate is WHERE user_id = :userId.
- It returns the updated row, or null when no row exists.
- It independently rejects unknown columns.

Treat these guarantees as part of the reviewed system contract. Do not infer SQL injection or cross-user access without contradictory evidence.
