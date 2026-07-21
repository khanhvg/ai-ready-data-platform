---
title: "I5-05 — Promotion-trust portal vertical slice"
description: "Plan a dependency-gated Vite/React portal shell and the later runner-backed promotion-trust journey without inventing unreleased contracts."
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
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
planningValidation: not-run
stageAStatus: blocked-on-issue-7-merged-vite-and-issue-8-released-stage-a
stageBStatus: blocked-on-issue-9-released-runner-sha
---

# I5-05 — Promotion-trust portal vertical slice

## Overview

Plan the full I5-05 vertical slice as a local, 16 GiB-friendly Vite + React modular monolith with
a same-origin BFF and a separate private runner trust boundary. Planning is complete at the exact
Issue #6 merge/input SHA; implementation is not authorized. Stage A may deliver only a
read-only/static promotion-trust lesson shell, navigation, no-JavaScript fallback, and explicit
runner-unavailable behavior. Stage B alone may integrate the real Issue #9 runner, execute the
controlled failure → `insufficient-evidence / no-common-grain` decision → reset → fresh verify
sequence, and claim a complete local journey through the single Issue #8 completion authority.

No plan text assigns a future dependency SHA, contract version, OpenAPI route, runner endpoint, or
registry command. Exact released handoffs must be pinned and verified before each stage.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Stage A exact dependency and contract gate](./phase-01-stage-a-exact-dependency-and-contract-gate.md) | Pending |
| 2 | [Stage A tests-first portal foundations](./phase-02-stage-a-tests-first-portal-foundations.md) | Pending |
| 3 | [Stage A static lesson shell and navigation](./phase-03-stage-a-static-lesson-shell-and-navigation.md) | Pending |
| 4 | [Stage A bounded verification and handoff](./phase-04-stage-a-bounded-verification-and-handoff.md) | Pending |
| 5 | [Stage B runner release and BFF gate](./phase-05-stage-b-runner-release-and-bff-gate.md) | Pending |
| 6 | [Stage B real journey and completion integration](./phase-06-stage-b-real-journey-and-completion-integration.md) | Pending |
| 7 | [Stage B evidence release rollback and approval](./phase-07-stage-b-evidence-release-rollback-and-approval.md) | Pending |

## Dependencies

- Same-scope `blockedBy` is empty because the relevant #7/#8/#9 plans are not present in this
  exact input tree and are not release artifacts. External gates are normative in
  [Dependency and Release Gates](./dependency-and-release-gates.md).
- **Stage A:** exact merged Issue #7 Vite handoff and exact released Issue #8 Stage A contract
  handoff. It has no Issue #9 runner dependency and cannot claim runnable completion.
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

## Stage Claims

| Stage | Earliest honest claim | Prohibited claim |
|---|---|---|
| A | Static lesson is understandable and accessible with runner absent | Lab ran, reset occurred, evidence is fresh, lesson completed |
| B | Real local journey completed against pinned released dependencies | Hosted, cloud, cross-user, signed/non-repudiable, or full WCAG conformance |

## Ownership

Implementation may change only winning `apps/learning-portal/**`, portal tests within that tree,
and `mk/issue-5/i5-05.mk`. It may emit untracked issue-owned runtime/evidence beneath the
registered `.artifacts` roots. Any shared-contract, runner, root Make, architecture-view, fixture,
data-pipeline, cloud, AWS, Terraform, or unrelated-path change is a hard STOP.

## Plan Exit

This artifact is `PLANNER_ONLY_NOT_VALIDATED`. The only next phase is fresh independent plan
validation at the exact published plan head, followed by fresh dependency-aware readiness before
any staged cook. Human exact-head pre-merge approval remains mandatory for every future merge.
