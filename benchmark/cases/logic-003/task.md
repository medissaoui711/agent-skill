# Review task: Optional delivery instructions

Review the supplied FastAPI endpoint and service for correctness.

## Contract
- A request may omit `delivery_note` or provide a string, including an empty string.
- Omitted notes should preserve the customer's existing note.
- An explicitly supplied empty string should clear the existing note.
- The endpoint must distinguish omitted fields from explicitly supplied values.
- Return actionable findings only. Include evidence, triggering input, impact, and a practical fix. Do not modify files or claim tests were run.
