---
title: "I5-04 — Build isolated privileged local runner"
description: "Deep/TDD plan for a fail-closed macOS local runner with private transport, released-contract pinning, OS containment, shared fencing, atomic eleven-asset release, crash recovery, and S3 evidence."
status: pending
priority: P1
issue: 9
branch: "plan/issue-9-privileged-local-runner"
tags: [feature, backend, security, critical, tdd, local-runner]
blockedBy: []
blocks: []
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
planningMode: "workflow-equivalent-deep-tdd-planner-only"
planningModel: "gpt-5.6-sol"
modelReasoningEffort: "xhigh"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue6ReleaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue8ReleasedStageASha: null
implementationBlockedBy: "issue-8-released-stage-a-sha"
validationStatus: "PLANNER_ONLY_NOT_VALIDATED"
---

# I5-04 — Build isolated privileged local runner

## Overview

Plan an issue-owned, Docker-free privileged runner for the existing retail pipeline on the
verified 16 GiB Darwin/arm64 host. The runner defaults to a private Unix-domain socket, rejects
browser-originated calls, executes only released typed commands through pinned read-only
entrypoints, confines children with a functional macOS Seatbelt (`sandbox-exec`) gate, and keeps
all mutation below an owned private workspace. Unsupported containment means disabled runner,
never a weaker fallback.

This is a planning artifact only. No phase is validated and no phase authorizes implementation.
Even dependency-independent characterization/fixture work may not enter `$ck:cook` until Issue #8
publishes an exact merged/released Stage A SHA and this issue subsequently passes independent plan
validation plus a fresh readiness audit.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Characterize seams and design RED fixtures](./phase-01-characterize-seams-and-design-red-fixtures.md) | Pending |
| 2 | [Bind released Issue 8 Stage A contract](./phase-02-bind-released-issue-8-stage-a-contract.md) | Pending |
| 3 | [Write transport and containment RED suites](./phase-03-write-transport-and-containment-red-suites.md) | Pending |
| 4 | [Implement fail-closed runner core](./phase-04-implement-fail-closed-runner-core.md) | Pending |
| 5 | [Implement fencing state and atomic release](./phase-05-implement-fencing-state-and-atomic-release.md) | Pending |
| 6 | [Prove S3 evidence rollback and handoff](./phase-06-prove-s3-evidence-rollback-and-handoff.md) | Pending |

## Dependencies

- **Satisfied:** Issue #6/I5-01 is shipped and verified at exact merge
  `24be3b34c6b0fcdbd07c5800dcab349054e34713`, which is this plan's immutable input.
- **Hard implementation block:** Issue #8/I5-03 is OPEN and has no released Stage A SHA. Phase 2
  must bind its exact merge SHA, contract paths/versions/hashes, generated-type procedure,
  operation/command matrix, evidence schema, and command-registry activation seam. Missing or
  incompatible release data is `RUNNER_DEPENDENCY_NOT_RELEASED`; do not create a local substitute.
- **Planning authority only:** owner comment
  <https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770> permits
  parallel planning but not dependency bypass.
- **Downstream only:** Issue #10/I5-05 may consume the released runner later; no portal/framework
  source is selected or changed here.

## Design and Traceability

- [Implementation boundary and design](./implementation-boundary-and-design.md)
- [Requirements, risks, and threat traceability](./requirements-risk-threat-traceability.md)
- [Verification, evidence, and rollback](./verification-evidence-and-rollback.md)

## Phase Split and Cook Gate

- Phase 1 is dependency-independent characterization and malicious-fixture design. It defines
  tests and proves existing seams; it does not change behavior.
- Phases 2-6 are hard-blocked on the exact released Issue #8 Stage A SHA.
- Readiness must report **BLOCKED_FOR_COOK** while that SHA is absent, even if planning and
  independent validation pass.

## Success Criteria

- All `RUN-*` requirements and threats have tests, evidence, rollback, owner, and dependency.
- Required RED negatives precede behavior changes; no fake contract, future SHA, or shared schema.
- Exact future gate is
  `make runner-test runner-security-test runner-race-test data-contracts-check` plus the S3 scans
  and evidence checks defined in the verification companion.
- Human approval remains bound to the exact independently reviewed head before merge.
