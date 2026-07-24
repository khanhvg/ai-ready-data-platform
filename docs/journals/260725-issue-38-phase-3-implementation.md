---
type: journal
date: 2026-07-25
issue: 38
branch: feature/issue-38-phase-3-deterministic-engine-report
status: publication-pending
authority: historical-record
---

# Issue 38 Phase 3 implementation

## Context

Phase 3 began from immutable Phase 2 input
`b6659e1b1e4f4b2a050e9a106a6a10946e0ec3ad`. Scope was limited to the
deterministic assessment engine, canonical report generation, explicit-root
CLI, packaged framework assets, tests, documentation, and verification. This
journal records work history and is not product or decision authority.

## What happened

- The first focused test collection produced the genuine RED state: six
  `ModuleNotFoundError` collection errors and pytest exit `2`.
- Added pure maturity and coverage aggregation, independent confidence
  summaries, all-rule operand traces for the pinned seven-gate bundle,
  deterministic cap selection, findings, priorities, recommendations, and
  architect review state kept separate from engine truth.
- Added packaged framework assets and deterministic `evaluate` and `report`
  commands. Both require explicit engagement and output roots.
- `evaluate` writes canonical `assessment-result.json`. `report` writes the
  canonical 12-section `report.json`, byte-stable standalone `report.html`, and
  a last-written manifest binding the required artifacts. Publication failure
  restores the prior coherent artifact set.
- Source documents and their snapshot are read coherently under the engagement
  writer lock. Generated output is excluded from the canonical source-state
  digest, and demo illustrations cannot affect scores, confidence, priority,
  gates, or readiness.

## Review history

The initial edge-case scout reported `1 Critical / 7 Important`. All eight
findings were corrected in the pending diff, including source snapshot
coherence, descriptor-bound filesystem handling, safe output-root validation,
machine-readable CLI failures, coherent report publication, and complete
determinism and safety coverage.

The final pending-diff specification review passed at `0 Critical / 0 Important
/ 0 Minor`. The subsequent code-quality review also passed at `0 Critical / 0
Important / 0 Minor`. A fresh independent exact-head review remains a
post-publication responsibility.

## Verification

- Full suite: `141 passed, 1 skipped`; the skip is the intentional
  documentation-only S3/object-store contract placeholder.
- Contract, engine, scenario, and report checks: `25`, `28`, `6`, and `7`
  tests passed.
- All `36` prototype artifacts remained byte-stable; calibration remained
  `117/119` (`98.3%`).
- Ruff passed; strict mypy passed over `37` files; the build contained all `50`
  required packaged files.
- Focused specification re-review, schema/store/migration/import-export/
  portability/security checks, source compilation, Compose configuration, and
  `git diff --check` passed.
- Repeated evaluation and report runs left engagement source bytes unchanged
  and produced byte-identical artifacts.
- Verification used the network-denying assessment wrapper where defined,
  started no service or container, and performed no cloud action.

## Reflection and decisions

- Keep maturity, coverage, confidence, gate evaluation, and architect review as
  separate concerns so incomplete evidence and human judgment remain visible.
- Reconstruct every result from pinned framework content plus one coherent
  engagement snapshot; omit wall-clock and generated-output state from
  deterministic inputs.
- Evaluate every gate without short-circuiting, retain triggered and
  untriggered operand provenance, and select the most restrictive cap.
- Treat canonical JSON as report authority and HTML as an escaped,
  self-contained presentation with no script, remote resource, or manual edit.
- Require explicit roots and fail closed on source/output aliasing, symlinked
  output paths, malformed inputs, or incomplete publication.

## Residual limitations

Publication, the immutable tested implementation SHA, remote branch SHA, pull
request, checks state, and detached exact-head verification are still pending.
The object-store boundary remains documentation-only; no S3 implementation or
cloud behavior exists. Deterministic byte identity is verified on the pinned
Python and platform runtime represented by the evidence.

## Next

- Publish the exact pending diff and record its immutable implementation SHA.
- Run a fresh detached exact-head verification against that published state.
- Record the remote branch, pull request, and actual checks state only after
  they exist.
