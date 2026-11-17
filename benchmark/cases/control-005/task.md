# Clean Security Review Task — Spring document access

## Contract
Every document has an immutable owner ID. The authenticated principal exposes its stable user ID. The repository method returns a document only when both document ID and owner ID match. A missing or non-owned document must produce the same not-found response to avoid disclosing existence.

## Review scope
Review authorization and object access. The repository contract is authoritative. If no actionable defect exists, return an empty findings array.
