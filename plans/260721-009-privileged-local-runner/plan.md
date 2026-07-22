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
originalPlanningBaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
amendmentInputSha: "5cea5ce248b49ff8741af1b1e65f8ac2eb64698f"
issue6ReleaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue8Pr23MergeSha: "5c2244c2c860234d0df49cf0a42ad950c6495717"
issue8ReleasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
issue8ReleaseTree: "27fc3667ef37892dad5c3fbfd76769f65a0760be"
requiredImplementationAncestorSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
dependencyCompatibility: "PASS"
runnerActivationInstancePath: "apps/lab-runner/config/command-owner-activation-i5-04-v1.json"
runnerRequestBodyLimitBytes: 16384
implementationHeadPolicy: "record-the-actual-clean-remote-equal-descendant-after-it-exists"
priorValidationInputSha: "de66ad3da6a4f6ed49059e547689462f8269bca5"
validationStatus: "PASS"
validationReport: "validation/capability-amendment-validation-report.md"
readinessAuditReport: "audit/capability-readiness-audit-2026-07-22.md"
implementationReadiness: "BLOCKED_DEPENDENCY_BACKEND_IN_PROCESS_UNAVAILABLE"
cookScope: "none"
capabilityAmendmentInputSha: "dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090"
blockedCookInputSha: "9eb31075aeb0e7b974ad15645460ab4987570f20"
hostForkPrevention: "PASS_7_OF_7"
setsidExactWorkerReap: "PASS"
releasedOperationFeasibility: "FAIL_7_OF_8_DBT_RESOURCE_TRACKER_CHILD"
sharedContractLease: "NO_WRITE_OVERLAP_READ_ONLY_STAGE_A_CONSUMPTION"
---

# I5-04 — Build isolated privileged local runner

## Overview

Plan an issue-owned, Docker-free privileged runner for the existing retail pipeline on the
verified 16 GiB Darwin/arm64 host. The runner defaults to a private Unix-domain socket, rejects
browser-originated calls, executes only released typed commands through pinned read-only
entrypoints, confines children with a functional macOS Seatbelt (`sandbox-exec`) gate, and keeps
all mutation below an owned private workspace. Unsupported containment means disabled runner,
never a weaker fallback.

The dependency-release amendment and prior validation/readiness reports remain immutable
historical evidence. The current [host capability amendment](./capability-amendment.md) supersedes
their cook-readiness decision: descendant prevention and exact single-worker reap pass, but the
released `retail.dbt-build` operation requires a Python resource-tracker child and fails under the
required fork-denied profile. The plan is therefore blocked before RED/source cook. Readiness does
not narrow the released eight-command contract, accept a private dbt startup hook, authorize a
shared-contract write, or approve a future implementation head.

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
  `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- **Released:** Issue #8/I5-03 Stage A is released at integration SHA
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, tree
  `27fc3667ef37892dad5c3fbfd76769f65a0760be`. Its ordered parents are PR #23 merge
  `5c2244c2c860234d0df49cf0a42ad950c6495717` and PR #25 approved head
  `734cf637a20ae186597e23d96a194ed4e30220ea`; the live integration branch points to the release.
- **Dependency compatibility:** PASS for read-only command-owner activation, version, operation,
  completion, lab, OpenAPI, and evidence seams. `fitness-result-v2` is reusable by I5-04 through an
  I5-04-owned activation instance; no shared-contract write or generated binding is required.
- **Plan-only ancestry:** this plan branch intentionally remains at the requested plan lineage and
  does not yet descend from Stage A. Exact planning reads use the immutable release object. A
  future dependency-resolved implementation base must pass the existing clean remote-equal
  Stage-A-descendant gate before any RED/source write; this blocked amendment does not merge or
  rebase release history.
- **Runner-local bindings:** the activation instance is exactly
  `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`; it binds the released registry
  hash to the actual I5-04 fragment hash only after that fragment exists. The private transport
  rejects any body over exactly 16,384 bytes before JSON parsing or operation/audit allocation.
  These are stricter Issue #9-owned policies, not shared-contract changes or invented future SHAs.
- **Lease:** Issue #8 Stage B planning ended blocked without a commit or write. Issue #9 consumes
  released Stage A read-only and writes only its own runner paths. There is no real write overlap;
  any later overlapping write lease is a fresh STOP.
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
- [Dependency-release amendment](./release-amendment.md)
- [Host capability and operation readiness amendment](./capability-amendment.md)
- [Independent validation report](./validation/independent-validation-report.md)
- [Release-amendment validation](./validation/release-amendment-validation-report.md)
- [Fresh release readiness audit](./audit/release-readiness-audit-2026-07-22.md)
- [Capability-amendment validation](./validation/capability-amendment-validation-report.md)
- [Current capability readiness audit](./audit/capability-readiness-audit-2026-07-22.md)

## Phase Split and Cook Gate

- `COOK_SCOPE=none`: no phase may resume until an owner-approved released backend runs all eight
  commands in process under fork denial, or another documented no-sudo lifetime primitive is
  independently proven. A shared-contract rerelease is required for any staged command scope.
- The planning-only host probe already proves seven child-creation denials and exact same-process
  `setsid` cleanup. It also proves the exact pinned dbt API fails closed, so that partial host
  result cannot authorize Phase 1 RED or source changes.
- Phase 3 must commit contemporaneous RED assertions through the real public runner paths before
  any Phase 4/5 behavior. Every later phase remains gated by its predecessor; readiness is not
  permission to skip, parallelize, or weaken those gates.

## Success Criteria

- All `RUN-*` requirements and threats have tests, evidence, rollback, owner, and dependency.
- The exact stable RED catalog and pre-behavior failure oracles precede behavior changes; no fake
  contract, future SHA, or shared schema.
- Exact future gate is
  `make runner-test runner-security-test runner-race-test data-contracts-check` plus the S3 scans
  and evidence checks defined in the verification companion.
- Two fresh independent exact-head reviews and separate human approval of that same exact head are
  mandatory before merge; any byte change invalidates all three attestations.

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
- **Decision at that historical input:** Plan validation passed with objective fixes and recorded
  the then-unreleased dependency state. The dependency-release amendment supersedes that external
  fact and invalidates the prior validation for the amended bytes.
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
- Historical external dependency finding: unresolved at the 2026-07-21 validation input; superseded
  by the exact Stage A release pin below.

### Dependency-Release Amendment — 2026-07-22

- **Input:** exact clean plan/audit head `5cea5ce248b49ff8741af1b1e65f8ac2eb64698f`.
- **Released dependency:** Issue #8 Stage A integration
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; PR #23 merge
  `5c2244c2c860234d0df49cf0a42ad950c6495717`; composition-fix PR #25 merge and
  release tree `27fc3667ef37892dad5c3fbfd76769f65a0760be`.
- **Compatibility:** PASS for the released generic activation/version/evidence seam without a
  shared-contract write. The exact read-only files, versions, schema IDs, hashes, commands and
  boundaries are pinned in Phase 2 and the design companion.
- **Resolved runner policy:** activation path
  `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`; private body ceiling 16,384
  bytes. Its content hash and the fragment hash are recorded from actual future bytes, never
  fabricated in advance. Stage A contains no generated-binding procedure or output list, so no
  generated path is allowed.
- **Historical reports:** `validation/independent-validation-report.md` and
  `audit/readiness-audit-report.md` describe their exact earlier inputs and are not rewritten.
- **Historical validation/readiness at that input:** strict amendment validation and a fresh
  dependency-aware audit passed and then authorized the whole ordered plan. The later host
  capability amendment supersedes that cook decision.
- **Boundary:** plan/audit only; implementation, product tests, PR/merge, credentials, and
  cloud/AWS/Terraform actions were not performed.
- **Historical next step:** `$ck:cook` Phase 1 was attempted from the exact input and stopped
  before RED/source. It is not the current next step.

### Host Capability Amendment — 2026-07-22

- **Input:** exact clean local/upstream/live plan head
  `dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090` after the first cook stopped before RED/source.
- **Host primitive:** Seatbelt `deny process-fork` passed 7/7 child-creation negatives; exact
  PID/start cleanup passed for a TERM-ignoring same-process `setsid` worker and direct image
  replacement; before/after inventories were empty.
- **Operation preservation:** seven fixed in-process command adapters are feasible. Exact
  `dbtRunner` requires a resource-tracker child and fails `EPERM`; a private multiprocessing
  override is explicitly rejected.
- **Current result:** `BLOCKED`, `COOK_SCOPE=none`, next decision is owner/platform backend or
  upstream contract scope. See the capability amendment and current validation/audit reports.
