---
title: "Issue #13 — Local Profiles and Resource Budgets"
description: "TDD plan for deterministic local profile admission, 16 GiB resource budgets, measured evidence, and ownership-safe teardown without changing the Docker-free core."
status: pending
priority: P1
issue: 13
branch: "plan/issue-13-local-profiles"
tags: [feature, infra, critical, compose, performance, security-s3, tdd]
blockedBy:
  - "260721-010-promotion-trust-portal"
  - "260721-012-data-platform-labs"
blocks: []
created: "2026-07-21T19:42:06.747Z"
createdBy: "ck:plan"
source: skill
planningMode: "fresh-plan-only-tdd"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
validationInputSha: "a23a0b77ac06dd6635f3b6a250432783cb9e2e04"
validationStatus: "independent-pass-with-fixes"
dependencyState: "implementation-blocked"
stageADependency: "issue-10-passing-merged-and-issue-12-released-labs"
stageBDependency: "stage-a-exact-head-and-admitted-engine-images"
---

# Issue #13 — Local Profiles and Resource Budgets

## Overview

Plan only. Preserve the shipped Docker-free retail core and admit current heavy Compose groups
through a fail-closed static contract before any container starts. Static configured limits are
the primary oracle; one cold plus two warm runs per admitted scenario provide corroborating
resource evidence. No implementation, container start, cloud action, PR, merge or readiness audit
is authorized by this artifact. Independent plan validation is complete and grants no
implementation or dependency authority.

Planning may proceed at the immutable input. Implementation cannot: the exact passing merged
Issue #10 journey and released/admitted Issue #12 labs do not exist. Stage A starts only after an
exact dependency/authority amendment is independently revalidated and audited. Stage B additionally
requires the exact Stage A head and an admitted local engine, platform-resolved images, and tools.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Amend Exact Dependencies and Characterize Baseline](./phase-01-amend-exact-dependencies-and-characterize-baseline.md) | Pending |
| 2 | [Write Static Admission and Security RED Tests](./phase-02-write-static-admission-and-security-red-tests.md) | Pending |
| 3 | [Implement Stage A Static Profile Admission](./phase-03-implement-stage-a-static-profile-admission.md) | Pending |
| 4 | [Run Stage B Cold Warm Resource Evidence](./phase-04-run-stage-b-cold-warm-resource-evidence.md) | Pending |
| 5 | [Prove Recovery Blast Radius and Release Handoff](./phase-05-prove-recovery-blast-radius-and-release-handoff.md) | Pending |

## Dependencies

- Shipped planner baseline: `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Independent validation input: `a23a0b77ac06dd6635f3b6a250432783cb9e2e04`.
- Stage A: exact passing merged Issue #10 plus exact released/admitted Issue #12 labs; future
  portal/runner image digests, lab allowlist, command authority, completion/evidence authority,
  and implementation input SHA must be recorded, never inferred.
- Stage B: exact Stage A head plus admitted engine allocation, image digests/SBOM/signature or
  provenance decisions, Compose/tool versions, and host normalization.
- Native `blockedBy` entries name the exact published dependency plan directories for discovery
  only. Missing local copies remain `not found`; neither plan head is merge/release authority.
- The historical Issue #5 master plan is the audited source, not a same-scope CLI plan blocker.
  Its pending metadata and older plans are not edited by this issue plan.

## Supporting Contracts

- [Repository and Compose inventory](./inventory.md)
- [Requirements and traceability](./requirements-and-traceability.md)
- [Resource and measurement model](./resource-model.md)
- [S3 threat model](./threat-model.md)
- [TDD, fitness, evidence, migration, and recovery](./tdd-fitness-evidence-recovery.md)

## Acceptance Boundary

- `make health`, `make dbt`, and `make bi` remain Docker/cloud/privilege-free.
- `orchestration`, `lake`, and `governance` are the only current heavy groups. Exact future
  dependency outputs may amend the inventory; this plan names no absent service or image.
- Each single group is configured at no more than 6 GiB/4 CPUs; only `lake+governance` may co-run,
  at no more than 10 GiB/6 CPUs; all three are denied before supported Compose startup.
- Required heavy acceptance is `blocked`, never synthetic or passed, when the admitted engine,
  images, tools, or normalized evidence are unavailable.
- Teardown acts only on exact run-owned resources and retained evidence survives.

## Plan Status

Independently validated with objective fixes. Dependency absence still blocks implementation.
The next authorized phase is a fresh dependency-aware readiness audit at the exact validation
output head; it cannot manufacture or waive any empty Stage A/B authority.

## Validation Log

### Independent Validation — 2026-07-22

- Validation input: `a23a0b77ac06dd6635f3b6a250432783cb9e2e04`; shipped baseline:
  `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- User questions asked: 0. The validation directive supplied the aggregate thresholds, stage
  boundaries, TDD/security/evidence decisions and authority-empty requirements.
- Result: `PASS_WITH_FIXES`; report: [independent validation report](./reports/independent-validation-report.md).

### Verification Results

- Tier: Full; Fact Checker, Flow Tracer, Scope Auditor and Contract Verifier applied.
- Claims checked: 92.
- Before correction: Verified 85 | Failed 7 | Unverified 0.
- After correction: Verified 92 | Failed 0 | Unverified 0.
- Corrections: reproducible protected aggregate hash and exact image locators; explicit service
  stop/parent teardown ceilings; complete host/engine reserve formulas; practical evidence caps;
  stable over-budget behavior ID/traceability; exact-head human approval binding.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all five `phase-*.md` files, `inventory.md`,
  `requirements-and-traceability.md`, `resource-model.md`, `threat-model.md`, and
  `tdd-fitness-evidence-recovery.md`.
- Decision deltas checked: 7 defect classes.
- Reconciled stale references: all affected requirements, phases, TDD, resource, threat, inventory
  and validation-status references.
- Unresolved contradictions: 0.
