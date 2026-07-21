---
title: "Issue #13 — Local Profiles and Resource Budgets"
description: "TDD plan for deterministic local profile admission, 16 GiB resource budgets, measured evidence, and ownership-safe teardown without changing the Docker-free core."
status: pending
priority: P1
issue: 13
branch: "plan/issue-13-local-profiles"
tags: [feature, infra, critical, compose, performance, security-s3, tdd]
blockedBy: []
blocks: []
created: "2026-07-21T19:42:06.747Z"
createdBy: "ck:plan"
source: skill
planningMode: "fresh-plan-only-tdd"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
dependencyState: "implementation-blocked"
stageADependency: "issue-10-passing-merged-and-issue-12-released-labs"
stageBDependency: "stage-a-exact-head-and-admitted-engine-images"
---

# Issue #13 — Local Profiles and Resource Budgets

## Overview

Plan only. Preserve the shipped Docker-free retail core and admit current heavy Compose groups
through a fail-closed static contract before any container starts. Static configured limits are
the primary oracle; one cold plus two warm runs per admitted scenario provide corroborating
resource evidence. No implementation, container start, cloud action, PR, merge, validation, or
readiness audit is authorized by this artifact.

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

- Current planning input: `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Stage A: exact passing merged Issue #10 plus exact released/admitted Issue #12 labs; future
  portal/runner image digests, lab allowlist, command authority, completion/evidence authority,
  and implementation input SHA must be recorded, never inferred.
- Stage B: exact Stage A head plus admitted engine allocation, image digests/SBOM/signature or
  provenance decisions, Compose/tool versions, and host normalization.
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

Plan creation is complete but deliberately unvalidated. Next authorized phase is fresh independent
plan validation. Dependency absence blocks implementation, not plan validation.
