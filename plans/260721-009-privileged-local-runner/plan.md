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
integrationBaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue6ReleaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue8ReleasedStageASha: null
implementationBlockedBy: "issue-8-released-stage-a-sha"
validationInputSha: "de66ad3da6a4f6ed49059e547689462f8269bca5"
validationStatus: "INDEPENDENT_VALIDATION_PASS_NOT_READINESS"
validationReport: "validation/independent-validation-report.md"
implementationReadiness: "BLOCKED_FOR_COOK"
---

# I5-04 — Build isolated privileged local runner

## Overview

Plan an issue-owned, Docker-free privileged runner for the existing retail pipeline on the
verified 16 GiB Darwin/arm64 host. The runner defaults to a private Unix-domain socket, rejects
browser-originated calls, executes only released typed commands through pinned read-only
entrypoints, confines children with a functional macOS Seatbelt (`sandbox-exec`) gate, and keeps
all mutation below an owned private workspace. Unsupported containment means disabled runner,
never a weaker fallback.

This is an independently validated planning artifact, not a readiness or implementation
authorization. No phase authorizes implementation. Even dependency-independent
characterization/fixture work may not enter `$ck:cook` until Issue #8 publishes an exact
merged/released Stage A SHA and this issue subsequently passes a fresh dependency-aware readiness
audit.

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
- [Exact planned paths and admission gates](./planned-paths-and-admissions.md)
- [Independent validation report](./validation/independent-validation-report.md)

## Phase Split and Cook Gate

- Phase 1 is dependency-independent characterization and malicious-fixture design in this plan.
  It defines tests and proves existing seams; it does not change behavior. Validation does not
  authorize cooking it while the Issue #8 release is absent.
- Phases 2-6 are hard-blocked on the exact released Issue #8 Stage A SHA.
- Readiness must report **BLOCKED_FOR_COOK** while that SHA is absent, even if planning and
  independent validation pass.

## Success Criteria

- All `RUN-*` requirements and threats have tests, evidence, rollback, owner, and dependency.
- The exact stable RED catalog and pre-behavior failure oracles precede behavior changes; no fake
  contract, future SHA, or shared schema.
- Exact future gate is
  `make runner-test runner-security-test runner-race-test data-contracts-check` plus the S3 scans
  and evidence checks defined in the verification companion.
- Human approval remains bound to the exact independently reviewed head before merge.

## Validation Log

### Session 1 — 2026-07-21

- **Trigger:** Fresh independent Issue #9 privileged-local-runner plan validation at exact input
  `de66ad3da6a4f6ed49059e547689462f8269bca5`.
- **Questions asked interactively:** 0. The owner's eleven validation constraint groups were
  supplied with the invocation and treated as authoritative answers; no scope or dependency
  relaxation was inferred.
- **Verification tier:** Full (six phases; Fact Checker, Flow Tracer, Scope Auditor, Contract
  Verifier).
- **Claims checked:** 96; **verified after fixes:** 96; **failed:** 0; **unverified:** 0.
- **Decision:** Plan validation passes with objective fixes. This is
  `INDEPENDENT_VALIDATION_PASS_NOT_READINESS`; Issue #8's exact released Stage A SHA remains null
  and implementation remains `BLOCKED_FOR_COOK`.
- **Phase propagation:** Phases 1-4 and the design/verification companions now carry exact
  dependency, transport, version, descendant-control, RED-ID, evidence-redaction, path, and tool
  admissions. Phases 5-6 retain the existing fencing/release/rollback boundary and consume the
  strengthened exact catalogs.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all six `phase-*.md` files, and all four plan companions.
- Decision deltas checked: 5 objective defect classes.
- Reconciled stale or ambiguous references: validator/base provenance, secret layout, version
  negotiation, raw-vs-canonical argv evidence, and descendant accounting admission.
- Unresolved contradictions: 0.
- External implementation dependency: intentionally unresolved and machine-blocking;
  `issue-8-released-stage-a-sha`.
