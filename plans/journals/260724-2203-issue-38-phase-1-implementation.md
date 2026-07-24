---
type: journal
date: 2026-07-24
issue: 38
branch: feature/issue-38-phase-1-rubric-calibration
status: publication-pending
authority: historical-record
---

# Issue 38 Phase 1 implementation

## Context

Implementation began from the audited plan input
`0b5335d907397bb8fd4f7a8c794ff2e930b6fe6b` and remained limited to the
Phase 1 rubric, deterministic runner, synthetic calibration, local report
artifacts, isolated Python 3.12 bootstrap, tests, and evidence. This journal is
chronological work history, not current product or decision authority.

## What happened

- Added the versioned `0.1.0-prototype` content: 10 domains, 50 domain anchors,
  30 questions, 150 question anchors, readiness math, independent confidence,
  seven traced gates, finding rules, recommendations, and architecture
  placeholders.
- Added four synthetic personas with two architect fixtures each, deterministic
  JSON/HTML report generation, semantic and safety validation, frozen migration
  inputs, and additive offline assessment commands.
- Recomputed calibration from source fixtures: 117 of 119 comparable ratings
  were within one level (`98.3%`); the shared Not-assessed response remained a
  separate coverage result, giving 119 of 120 comparable slots.
- Found an audited-plan prose error for Enterprise Architect B. Its domain
  scores sum to 19, so the specified formula yields pre-gate/final readiness
  `1/1`, not `2/1`. The fixtures and tests preserve the ratings and formula.
- The first spec-compliance review reported 0 Critical and 5 Important
  findings. Fixes made diagnostic and finding semantics content-driven, added
  confidence-validation actions and cap mutation coverage, restored existing
  `make clean` behavior, tracked evidence, and enforced offline verification.
  The final spec recheck passed with 0 Critical and 0 Important.
- The code-quality stage then reported 0 Critical and 2 Important findings.
  Exact semantic validation and mutation tests closed freeze gaps in readiness
  labels, question order, integer anchors, and question-to-domain bindings.
  Template and artifact assertions made structured gate and finding evidence
  visible in HTML. The final rerun passed with 0 Critical and 0 Important:
  32 tests, 48 contract assertions, 36 byte-stable artifacts, Ruff, strict
  mypy, build, and all 8 packaged assets passed.
- AgentWiki publication was skipped because no AgentWiki CLI or MCP capability
  was available in the implementation environment.

## Reflection

The thin, data-driven prototype was enough to expose issues that scaffolding
would have hidden: inconsistent prose arithmetic, the need to distinguish
Not-assessed coverage from rating agreement, and the need for executable
offline and safety boundaries. Recomputing expectations from source fixtures
kept the goldens subordinate to the rubric rather than turning them into
hard-coded outputs.

## Decisions

- Treat the versioned content and formulas as the scoring source of truth; use
  the journal and evidence report only as historical records.
- Keep maturity, confidence, and coverage independent.
- Preserve all seven gate traces, including non-triggered explanations, and
  apply the most restrictive triggered cap.
- Keep dependency acquisition as the only network-enabled assessment step;
  verification remains local and network-denied on the audited macOS runtime.
- Do not extend the prototype into Phase 2+ services or alter the data platform,
  golden pipeline, cloud infrastructure, or customer-data boundaries.

## Next

- Complete exact-head verification, commit, push, PR creation/update, CI wait,
  and the Issue #38 evidence comment.
- Keep Issue #38 open and leave merge to a separate owner action.
- Defer storage/migration services, import/export, web workflow, catalog,
  golden-pipeline, S3/cloud/deployment, customer data, and learning/lab work to
  Phase 2 or later.
