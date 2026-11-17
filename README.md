# Agent Skills

**A focused collection of reusable, evidence-driven skills for AI-assisted software engineering.**

[![Validate Agent Skills](https://github.com/medissaoui711/agent-skill/actions/workflows/validate-skills.yml/badge.svg?branch=main)](https://github.com/medissaoui711/agent-skill/actions/workflows/validate-skills.yml)
[![Validate Benchmark](https://github.com/medissaoui711/agent-skill/actions/workflows/validate-benchmark.yml/badge.svg?branch=main)](https://github.com/medissaoui711/agent-skill/actions/workflows/validate-benchmark.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

Agent Skills is a growing repository of structured instructions and supporting resources designed to help AI coding agents perform engineering work with greater consistency, rigor, and transparency.

The repository currently includes **Code Review Expert**: a senior-reviewer-oriented skill for examining pull requests, diffs, repositories, and proposed changes. It prioritizes actionable findings, traceable evidence, and honest reporting over superficial feedback.

A separate **Code Review Benchmark** provides synthetic review cases and a deterministic evaluation harness. Its private answer key is intentionally maintained outside this public repository.

---

## Contents

- [Why this repository](#why-this-repository)
- [Available skills](#available-skills)
- [Code Review Expert](#code-review-expert)
- [Code Review Benchmark](#code-review-benchmark)
- [Installation](#installation)
- [Using the skill](#using-the-skill)
- [Review principles](#review-principles)
- [Repository structure](#repository-structure)
- [Validation and quality](#validation-and-quality)
- [Contributing](#contributing)
- [License and attribution](#license-and-attribution)

## Why this repository

AI-generated engineering output is only useful when it is grounded in the actual codebase, explicit about uncertainty, and safe to act upon. These skills aim to make that standard repeatable.

Each skill is organized as a portable set of instructions with focused reference material and practical templates. The goal is not to replace engineering judgment, but to give AI-assisted workflows a clear operating model.

**Repository principles**

- **Evidence over assumptions:** conclusions must be supported by inspected code, observed behavior, or a clearly identified contract.
- **Actionable outcomes:** explain the condition, impact, and practical remediation—not just what looks unusual.
- **Risk-first thinking:** prioritize correctness, security, data integrity, and reliability.
- **Explicit boundaries:** do not modify code or perform repository actions unless specifically authorized.
- **Honest verification:** distinguish what was inspected, reasoned about, and actually executed.
- **Reusable by design:** keep skills structured, focused, and maintainable.

## Available skills

| Skill | Purpose | Status |
| --- | --- | --- |
| [`code-review-expert`](skills/code-review-expert/SKILL.md) | Evidence-driven review of code changes, pull requests, and repositories. | Available |

New skills may be added as they are documented and validated. The table above reflects the skills currently published in this repository.

## Code Review Expert

**Code Review Expert** acts as a senior, independent software reviewer. It helps inspect proposed changes and identify defects or risks that are concrete, relevant, and supported by evidence.

### Review coverage

- Correctness, regressions, and edge cases
- Security and privacy boundaries
- Architecture and design integrity
- Performance and reliability
- Data integrity and failure handling
- Compatibility and maintainability
- Test coverage and verification gaps

### Review workflow

1. **Establish context** — understand the change, repository instructions, architecture, runtime, and constraints.
2. **Map the change** — identify affected components, data flows, trust boundaries, and dependencies.
3. **Review by risk** — examine correctness and regressions before broader quality concerns.
4. **Validate candidate findings** — trace execution paths, check mitigations, and separate confirmed defects from hypotheses.
5. **Report clearly** — present findings by severity with location, conditions, impact, evidence, and remediation.

### Severity model

| Level | Meaning | Typical decision |
| --- | --- | --- |
| **Critical** | Catastrophic compromise, severe data loss, or broadly exploitable impact. | Block release |
| **High** | Serious security, correctness, integrity, or availability defect. | Block merge until resolved |
| **Medium** | Material defect with constrained conditions or impact. | Fix before release in most cases |
| **Low** | Limited-impact defect or concrete maintainability risk. | Schedule an appropriate fix |
| **Informational** | Non-blocking observation or improvement. | Consider; not a defect by itself |

Severity describes impact, not confidence. Findings should not be inflated to make a review appear more valuable.

## Code Review Benchmark

The public benchmark contains synthetic review cases, schemas, validation tools, and a deterministic evaluation harness. The pilot has five cases; the approved V1 target is 40 cases across logic/runtime, security, architecture, performance/reliability, and clean controls.

**Ground truth and expected answers are not stored in this repository.** Review execution and evaluation are separated to prevent answer-key leakage.

See [benchmark/README.md](benchmark/README.md) for the protocol, case inventory, and local validation. The five-case pilot validates the benchmark pipeline; it does not certify model capability or establish that V1 thresholds have been met.

## Installation

Install the skill with the Skills CLI:

```bash
npx skills add medissaoui711/agent-skill --skill code-review-expert
```

To inspect the skill before installing it, start with its [SKILL.md](skills/code-review-expert/SKILL.md) and its six-file [skill package](skills/code-review-expert/).

## Using the skill

After installation, ask your AI coding agent to perform a review and specify the scope and depth you need.

**Example requests**

```text
Review the current pull request for correctness and security issues.
Use the standard review workflow. Report only actionable findings with
file references, impact, evidence, and recommended fixes. Do not modify files.
```

```text
Perform a deep review of the authentication and authorization changes.
Trace tenant boundaries, permission checks, and failure paths. Clearly
separate confirmed findings from risks that need further verification.
```

```text
Review this diff for performance regressions and missing tests.
Prioritize issues introduced by the change and state which checks you
actually executed versus which ones you could only inspect.
```

### Review depth

- **Quick:** inspect the diff and directly affected code, prioritizing high-impact risks.
- **Standard:** review changed components and relevant integration points. This is the default.
- **Deep:** broaden the review to architecture, threat boundaries, data lifecycle, concurrency, migrations, dependencies, and deployment implications.

## Review principles

Code Review Expert is intentionally conservative about claims and actions:

- It is **read-only by default**. Reviews do not authorize edits, commits, pushes, or pull requests.
- It must not invent file paths, line numbers, vulnerabilities, test results, or execution output.
- It should inspect surrounding code and relevant callers rather than judging isolated lines.
- It should report pre-existing issues separately from regressions introduced by the change.
- It must protect secrets and sensitive data in review output.
- A clean review is not a guarantee that the code is defect-free.

These boundaries help keep review feedback useful, auditable, and safe to act on.

## Repository structure

```text
.
├── skills/
│   └── code-review-expert/
│       ├── SKILL.md
│       ├── review-workflow.md
│       ├── review-checklist.md
│       ├── security-review.md
│       ├── engineering-review.md
│       └── review-report.md
├── benchmark/
│   ├── cases/                    # Public synthetic cases; no answer key
│   ├── evaluator/                # Deterministic post-review evaluator
│   ├── schemas/
│   └── tests/
├── .github/
│   ├── scripts/
│   │   └── validate_skills.py
│   └── workflows/
│       ├── validate-skills.yml
│       └── validate-benchmark.yml
├── LICENSE
├── README.md
└── SOURCE_AND_LICENSE.md
```

### Design of a skill

- `SKILL.md` defines the skill identity, activation context, operating rules, and primary workflow.
- The five companion Markdown files provide workflow, checklist, security, consolidated engineering guidance, and the report template.
- License, source attribution, benchmark materials, and CI files remain outside the installable skill directory.

## Validation and quality

This repository includes separate GitHub Actions workflows:

1. **Validate Agent Skills:** checks Agent Skills format, metadata, naming conventions, and local Markdown links.
2. **Validate Code Review Benchmark:** validates the public pilot manifest and schemas, then runs evaluator unit tests.

Passing these checks verifies only the checks they run. Benchmark CI does not run an AI model, access private ground truth, or certify review quality.

## Contributing

Contributions that improve clarity, correctness, safety, and practical usefulness are welcome.

Before opening a pull request:

1. Keep each skill focused on a clear, reusable task.
2. Include evidence-based instructions and explicit operational boundaries.
3. Keep the installable skill package to six focused Markdown files; consolidate related engineering guidance where appropriate.
4. Update examples and templates when behavior changes.
5. Run the available validation checks and describe any limitations.
6. Preserve source attribution and comply with the applicable licenses.
7. Never commit private benchmark answers, credentials, or sensitive raw review outputs.

Pull requests should explain the problem being addressed, the proposed change, and how it was verified.

## License and attribution

The repository is distributed under the [MIT License](LICENSE), subject to the notices and terms applicable to individual materials.

Code Review Expert is adapted from the upstream [awesome-skills/code-review-skill](https://github.com/awesome-skills/code-review-skill) project. See [SOURCE_AND_LICENSE.md](SOURCE_AND_LICENSE.md) for source attribution and licensing details.

---

**Maintained by [medissaoui711](https://github.com/medissaoui711).**

Found this repository useful? Consider starring it and sharing feedback through GitHub issues or pull requests.
