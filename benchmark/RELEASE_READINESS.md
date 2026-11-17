# Dataset V1 — Public Fixture Readiness

## Structural inventory

The public fixture set contains exactly 40 review scenarios:

| Category | Cases |
| --- | ---: |
| Logic & Runtime | 10 |
| Security | 10 |
| Architecture | 6 |
| Performance & Reliability | 6 |
| Clean / Control | 8 |
| **Total** | **40** |

The public validator checks the exact case inventory, category distribution, manifest field contract, task/project file existence, safe project paths, schema presence, and forbidden Ground Truth path names.

## Release boundary

A successful public fixture validation establishes structural integrity only. It does not establish the correctness or independent adjudication of private reference findings, nor does it certify evaluator precision, recall, F1, severity accuracy, or localization accuracy.

Private Ground Truth remains in the separate private repository. No expected findings, answer keys, or adjudication labels belong in this public repository.

## Validation

```bash
python benchmark/evaluator/validate_dataset.py
python -m unittest discover -s benchmark/tests -v
```

The current 40-case fixture set is ready for continued technical evaluation. Official Benchmark V1 scoring remains gated by the separate private adjudication and release process.
