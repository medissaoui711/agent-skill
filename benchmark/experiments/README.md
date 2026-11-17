# Experiment run evidence format

This public directory contains the versioned run-record schema and a hash-freeze utility. **Run records, raw prompts/outputs, match artifacts, and metrics remain private by default** in the separate Ground Truth archive.

## Freeze workflow

1. Execute a baseline or skill-enabled review using public synthetic fixtures only.
2. Persist the raw output privately.
3. Before any evaluator or Ground Truth access, run:

```bash
python benchmark/experiments/freeze_run.py --metadata run-metadata.json --prompt prompt.txt --raw-output raw-output.txt --output private-run-record.json
```

The metadata must include run/case IDs, arm, dataset version and manifest SHA-256, public commit, model provider/version, evaluator commit, sampling parameters, enabled tools, execution environment, and the explicit assertion `ground_truth_accessed_before_freeze: false`. The tool computes prompt/output SHA-256 and a canonical record digest, refuses overwrite, and sets `publication_state=PRIVATE`.

The tool accepts no Ground Truth path. The false access field is an operator attestation, not proof that the runner was isolated; enforce separation at the execution environment level. The record digest detects ordinary post-freeze edits but is not a digital signature against an attacker able to rewrite both the record and digest.

## Publication gate

Publication is opt-in only after owner approval and review for secrets, PII/sensitive data, answer leakage, and benchmark contamination. Raw reviews can function as answer keys. Default: PRIVATE.
