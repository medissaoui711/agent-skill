# CI Checks audit

## GitHub exposes two distinct commit-status surfaces

- **Legacy commit statuses** (`/commits/{sha}/status`) report status contexts posted through the Status API. An empty list or `total_count: 0` means no legacy status contexts were posted; it does not prove that GitHub Actions did not run.
- **Check runs** (`/commits/{sha}/check-runs`) include GitHub Actions checks. Inspect their `name`, `app`, `status`, and `conclusion` to determine what actually ran.

## Recorded example: Phase 5F merge

For merge commit `33b11d53d0628f178a70ff6ca964dce909aa9b9e`, the maintainer's recorded API inspection reported:

- Legacy Status API: `total_count=0`.
- Checks API: one GitHub Actions check, **Validate skill format and repository references**, with conclusion `success`.
- The benchmark workflow was not triggered for that README-only change because its path filter did not include the root README.

This is a documented maintainer observation, not a live assertion about the current commit. The distinction is intentional: always inspect Checks API check-runs in addition to legacy combined status before describing CI.

## Operational rule

A successful check proves only the steps that check executed. It does not establish private Ground Truth correctness, independent adjudication, experiment completion, or V1 scoring readiness.
