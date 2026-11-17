# Scoring Policy

## Matching v2

The evaluator constructs eligible candidate/reference edges only when normalized repository-relative file paths and categories match exactly. A specified line must be within the configured tolerance (default 3); if either side omits a line, the edge remains eligible but is unlocalized.

The assignment objective is lexicographic:

1. Maximize matching cardinality.
2. Among maximum-cardinality assignments, maximize the number of localized pairs (both line numbers present).
3. Among those, minimize total absolute line distance.

The implementation uses a standard-library min-cost maximum-flow solver. It does not use prose similarity, model judgments, or arbitrary input order as a matching signal.

### Conservative ambiguity policy

A candidate/reference edge is scored only when it occurs in every globally optimal assignment and the candidate is matched in every optimal assignment. If multiple optimal references are possible, or the candidate can be unmatched in another optimal assignment, the candidate is reported under `ambiguous_findings` and is not scored as a true positive. The corresponding reference remains a false negative unless another forced edge accounts for it. This is deliberately conservative and may understate detection when the available evidence cannot uniquely identify the reference.

The `optimal_assignment` object reports the best achievable cardinality and localization/distance objective separately from the number of forced matches actually scored. These values must not be conflated.

## Duplicate handling

Candidate findings are grouped by normalized file, line, category, and whitespace/case-normalized title. Exact duplicate copies are collapsed deterministically and counted as duplicates. If a duplicate key contains conflicting payload variants (for example, different severity or description), the group is quarantined from matching; its representative remains an unmatched finding, all additional copies count as duplicates, and the full conflict is reported under `conflicting_duplicate_groups`. This prevents a lexical tie-break from silently selecting a severity or description for scoring.

## Metrics

- Precision = TP / (TP + FP)
- Recall = TP / (TP + FN)
- F1 = harmonic mean of precision and recall
- Severity accuracy = exact severity matches / forced matched findings
- Localization accuracy = localized forced matches / forced matched findings
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
