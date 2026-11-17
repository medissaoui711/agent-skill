# Clean Review Task — FastAPI batch endpoint

## Contract
The endpoint accepts up to 200 identifiers. The service processes them in batches of at most 25, preserves input order in the returned results, and rejects requests above the documented limit before repository work. The repository method is asynchronous and accepts a list of IDs.

## Review scope
Review bounds, batching, and order preservation. The implementation below is intended to satisfy the contract. Return no findings unless a concrete violation exists.
