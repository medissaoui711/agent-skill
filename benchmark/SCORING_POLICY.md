# Scoring Policy

## Matching
Automatic matching is conservative and structured. A candidate requires exact normalized file path, exact category, and a line within the configured tolerance (default 3), unless either line is unspecified. Equal-distance ambiguity is not auto-matched.

The matcher does not infer semantic equivalence from prose. Ambiguous or unmatched findings require independent adjudication.

## Metrics
- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 = harmonic mean of precision and recall
- Severity accuracy = exact severity matches / matched findings
- Localization accuracy = matched findings within line tolerance / matched findings
- Duplicate rate = duplicate candidate findings / all candidate findings
- Control-case false alarms = unsupported findings on control cases

Undefined ratios are null, not zero. A clean review with no findings can have null precision; inspect control false alarms separately.

## Full V1 targets
- Precision >= 0.90
- Recall >= 0.85
- F1 >= 0.87
- Severity accuracy >= 0.85
- Localization accuracy >= 0.90
- Duplicate rate <= 0.05

Do not apply these thresholds as pass/fail certification to the five-case pilot.

## Integrity hard stops
A run is invalid if it exposes ground truth before output freeze, fabricates execution evidence, presents unsupported security claims as confirmed, fails to distinguish confirmed findings from hypotheses, or changes experimental conditions without recording the change.

## Reproducibility record
Capture dataset version/hash, repository commit, model/version, date/time, prompt, sampling settings, tool access, run number, raw-output hash, evaluator version, and adjudication notes.
