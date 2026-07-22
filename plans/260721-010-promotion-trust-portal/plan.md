---
title: "I5-05 — Promotion-trust portal vertical slice"
description: "Cook the exact-release Stage A Vite/React learning portal shell while keeping the runner-backed Stage B blocked."
status: pending
priority: P1
issue: 10
branch: "plan/issue-10-promotion-portal"
tags: [feature, frontend, backend, api, critical]
blockedBy: []
blocks: []
created: "2026-07-21T16:49:00.989Z"
createdBy: "ck:plan"
source: skill
mode: fast-tdd-no-tasks
integrationBaseSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
validationInputSha: "4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7"
planningValidation: stage-a-release-amendment-pass
readinessAuditInputSha: "4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7"
readinessVerdict: stage-a-ready
cookScope: issue-10-stage-a
dependencyIssue7: RELEASED_PR22_MERGE_1806B6D
dependencyIssue8: RELEASED_STAGE_A_INTEGRATION_FECF6BB
dependencyIssue9: BLOCKED_UNRELEASED
stageAStatus: ready-from-integration-fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9
stageBStatus: blocked-on-issue-9-released-runner-sha
---

# I5-05 — Promotion-trust portal vertical slice

## Overview

Deliver Stage A as a local, 16 GiB-friendly Vite + React static portal process from pristine
released integration `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. The released #7 toolchain and
#8 Stage A validators, registry, lesson, lab, OpenAPI, progress/completion/evidence and promotion
manifest contracts are now exact authorities. Stage A has no BFF or API: it renders a
Vietnamese-first catalog/module/lesson/step shell, one promotion-trust vertical slice,
read-only navigation, a real no-JavaScript equivalent, and explicit runner-unavailable behavior.

Stage A may be cooked only within the exact file/command/dependency allowlists in
[the release amendment](./stage-a-release-amendment.md). It cannot claim execution, reset, fresh
evidence, progress, or completion. Stage B alone may later integrate a released Issue #9 runner,
execute the controlled failure → `insufficient-evidence / no-common-grain` decision → reset →
fresh verify sequence, and use the single Issue #8 completion authority. Stage B remains blocked
and has empty authority.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Stage A exact dependency and contract gate](./phase-01-stage-a-exact-dependency-and-contract-gate.md) | Pending |
| 2 | [Stage A tests-first portal foundations](./phase-02-stage-a-tests-first-portal-foundations.md) | Pending |
| 3 | [Stage A static lesson shell and navigation](./phase-03-stage-a-static-lesson-shell-and-navigation.md) | Pending |
| 4 | [Stage A bounded verification and handoff](./phase-04-stage-a-bounded-verification-and-handoff.md) | Pending |
| 5 | [Stage B runner release and BFF gate](./phase-05-stage-b-runner-release-and-bff-gate.md) | Blocked on Issue #9 |
| 6 | [Stage B real journey and completion integration](./phase-06-stage-b-real-journey-and-completion-integration.md) | Blocked on Issue #9 |
| 7 | [Stage B evidence release rollback and approval](./phase-07-stage-b-evidence-release-rollback-and-approval.md) | Blocked on Issue #9 |

## Dependencies

- Same-scope `blockedBy` is empty. Exact external release authorities are normative in
  [Dependency and Release Gates](./dependency-and-release-gates.md) and the
  [Stage A release amendment](./stage-a-release-amendment.md).
- **Stage A:** released Issue #7 PR #22 merge
  `1806b6d515f2f7a2ace2be7077af84a745ff221f`, approved feature head
  `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9`, released Issue #8 Stage A PR #23 merge
  `5c2244c2c860234d0df49cf0a42ad950c6495717`, and pristine composed integration
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. Stage A has no Issue #9 runner dependency and
  cannot claim execution or completion.
- **Stage B:** passing Stage A plus exact released Issue #9 runner API, registry, client/transport,
  idempotency, problem, and evidence handoff SHA.
- Issue #6 data/fixture truth at input `24be3b34c6b0fcdbd07c5800dcab349054e34713`
  remains read-only. Root `release-manifest.json`, shared contracts, runner source, root Makefile,
  and other issue/worktree files remain outside I5-05 ownership.

## Companion Contracts

- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Architecture and API Boundaries](./architecture-and-api-boundaries.md)
- [Threat Model and Security](./threat-model-and-security.md)
- [Verification, Evidence, and UAT](./verification-evidence-and-uat.md)
- [Stage A Exact-Release Amendment](./stage-a-release-amendment.md)
- [Stage A Readiness Audit](./audit/stage-a-readiness-audit-report.md)

## Stage Claims

| Stage | Earliest honest claim | Prohibited claim |
|---|---|---|
| A | Static lesson is understandable and accessible with runner absent | Lab ran, reset occurred, evidence is fresh, lesson completed |
| B | Real local journey completed against pinned released dependencies | Hosted, cloud, cross-user, signed/non-repudiable, or full WCAG conformance |

## Ownership

The maximum Issue #10 ownership ceiling is `apps/learning-portal/**`, portal tests within that
tree, `mk/issue-5/i5-05.mk`, and Issue #10 plan/evidence artifacts. Stage A present cook authority
is narrower: exactly 34 new tracked files, 18 admitted command surfaces, and the release
identities enumerated in the amendment. It has no modifies or deletes. Stage B file, command, and
dependency SHA allow-lists remain `[]`. Any shared-contract, runner, root Make,
architecture-view, fixture, data-pipeline, cloud, AWS, Terraform, or unrelated-path change is a
hard STOP.

`README.md`, `docs/**`, dependency worktrees, and release metadata owned outside Issue #10 are not
future I5-05 write authority. Any user-facing documentation or release-note change discovered at
implementation review must be handed to its owner through a separately authorized serialized
change; it cannot broaden the portal cook allow-list.

## Plan Exit

The Session 1 validation and blocked readiness reports remain immutable historical snapshots.
The exact-release amendment and fresh readiness audit at starting head
`4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7` supersede only their dependency-state conclusions.
Stage A may proceed from pristine released integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` within its closed allowlists. Stage B remains blocked
on Issue #9 and has no cook authority. Stage A still requires two fresh independent exact-head
implementation reviews and human exact-head approval before a human merge; planning readiness is
not implementation, execution, evidence, completion, or merge approval.

## Validation Log

### Session 1 — 2026-07-22 (historical; dependency conclusion superseded)

**Trigger:** Fresh independent Issue #10 plan validation at exact input
`ad87c3f6090129dd30cfb626c6f396567f567a42`.

**Questions asked:** 0. The owner supplied ten exact validation decisions in the invocation; no
unresolved product choice remained and repeating them as an interview would add no information.

#### Confirmed Decisions

- Stage A is runner-independent, static/read-only, explicitly unavailable, and non-completing.
- Stage B alone may consume released #9 and claim the real controlled-failure → four-grain
  decision → reset → verified-evidence journey.
- #8 is the sole completion/evidence authority; #9 is private and server-only.
- At the Session 1 input, both stage file/command/dependency SHA allow-lists were empty pending
  released dependencies. Session 2 now supplies Stage A authority; Stage B remains empty.
- The practical TDD, Chromium desktop+narrow, axe Critical/Serious, no-JS, recovery, S3,
  evidence-integrity, cleanup, residual UAT, independent-review, and human exact-head gates remain.

#### Verification Results

- **Tier:** Full (7 phases; Fact Checker, Flow Tracer, Scope Auditor, Contract Verifier)
- **Claims checked:** 105
- **Verified:** 105 | **Failed:** 0 | **Unverified:** 0
- **Corrections applied:** empty staged authorities; stale dependency state; deferred #7/#8/#9
  routes/modules/viewports/result schema; explicit #8 CAS/version/reconciliation and #9 private
  crash/retry/reset/error/unavailable semantics.

#### Impact on Phases

- At Session 1, Phases 1–4 were Stage A design only and Phases 5–7 were Stage B design only.
  Session 2 supersedes this only for Stage A; Phases 5–7 remain blocked.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, seven phase files, and five companion contracts.
- Decision deltas checked: 8.
- Reconciled stale references: 13 plan files.
- Unresolved contradictions: 0.

### Session 2 — 2026-07-22 Stage A release amendment

**Trigger:** Fresh dependency-release amendment and readiness audit from exact clean plan head
`4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7`, using remote Git objects and live GitHub records.

#### Released authority

- Issue #7 PR #22 is merged at `1806b6d515f2f7a2ace2be7077af84a745ff221f`; its approved feature
  head is `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9`.
- Issue #8 Stage A PR #23 is merged at `5c2244c2c860234d0df49cf0a42ad950c6495717`.
- Composition PR #25 yields pristine released Stage A integration
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; release evidence is Issue #8 comment
  `5043195549`.
- Issue #9 remains unreleased. Stage B stays blocked with empty file, command, and dependency
  lists.

#### Stage A disposition

- Exact dependency bytes, protected identities, toolchain, 34-file write allowlist, command
  allowlist, requirements, scenarios, RED catalogue, S3 controls, cleanup, rollback, and review
  gates are closed in the amendment.
- The useful slice is a Vietnamese-first reusable catalog/module/lesson/step shell with the
  promotion-trust lesson as one vertical slice, no-JavaScript equivalence, and explicit runner
  unavailability. It has no BFF/API, mutation, storage, runner, execution, reset, evidence, or
  completion authority.
- Strict CK validation, link/anchor, placeholder/future-SHA, dependency identity, path/command,
  requirement/scenario/RED/S3, diff-hygiene, and whole-plan results are recorded in the current
  readiness audit.
