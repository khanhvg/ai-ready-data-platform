---
title: "I5-06 — Architecture curriculum, templates, and fitness functions"
description: "Authorize a bounded Vietnamese-first static Stage A curriculum from the exact released Issue #8 contracts while keeping portal-dependent Stage B blocked."
status: pending
priority: P1
issue: 11
branch: "plan/issue-11-architecture-curriculum"
tags: [issue-5, i5-06, architecture, curriculum, tdd, security-s3, critical]
blockedBy: []
blocks: []
created: "2026-07-21T18:03:55.505Z"
createdBy: "ck:plan"
source: skill
mode: fast-tdd-no-tasks
modelProfile: "gpt-5.6-sol"
modelReasoningEffort: "xhigh"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
validationStatus: passed-with-fixes-not-readiness
validationInputSha: "7620d168fb96cf9ae11e963501f65ea5a416af43"
validationReport: "validation/independent-validation-report.md"
readinessAuditInputSha: "1287fe35aa9ab29a97daa541f39a624d01a77d31"
readinessAuditReport: "audit/readiness-audit-report.md"
stageAAmendmentStartSha: "ab653f6edec73e5ef875723945d2e3cd7814b4e6"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
stageAAmendment: "stage-a-release-amendment.md"
stageAReadinessAudit: "audit/stage-a-readiness-audit-report.md"
readinessVerdict: stage-a-ready
implementationAuthority: stage-a-only
stageAStatus: ready-to-cook-from-exact-released-integration
stageBStatus: blocked-on-issue10
currentStageAFileAuthority: "stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist"
currentStageACommandAuthority: "stage-a-release-amendment.md#exact-command-allowlist"
stageBImplementationFileAllowList: []
stageBImplementationCommandAllowList: []
---

# I5-06 — Architecture curriculum, templates, and fitness functions

## Overview

Plan a Vietnamese-first, foundation-to-mid, hands-on architecture learning product. Every module
must trace a business outcome through capability, stakeholder concern, FR/NFR, design options,
C4/data/integration/security/deployment views, an ADR or admitted pattern, implementation intent,
automated evidence, and operations/resilience/security/cost/governance consequences. A topic list
or Markdown dump is not a release.

The original plan was completed at exact clean input
`24be3b34c6b0fcdbd07c5800dcab349054e34713`. A fresh audit starting from clean plan head
`ab653f6edec73e5ef875723945d2e3cd7814b4e6` now binds Stage A to released integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. The
[Stage A Exact-Release Amendment](./stage-a-release-amendment.md) is the normative authority for
its exact 50 create-only paths, commands, contracts, tests, output bounds, evidence, cleanup, and
rollback gates. It supersedes stale Stage A dependency and empty-authority statements below while
preserving the original validation and blocked audit as historical records.

Stage A is a machine-valid curriculum/template/static-view foundation. It cannot claim portal
delivery, an executable lab, runner, reset, progress, completion, fresh learner evidence, or
learner effectiveness. Issue #8's active Stage B Vite identifier-binding lease is an explicit
non-authority and is not consumed. Stage B remains blocked on a passing merged Issue #10 real
journey and released renderer; its file, command, dependency, and renderer lists remain empty.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Freeze authority and dependency gates](./phase-01-freeze-authority-and-dependency-gates.md) | Ready for Stage A cook preflight |
| 2 | [Stage A tests-first contract and preservation](./phase-02-stage-a-tests-first-contract-and-preservation.md) | Ready for Stage A cook |
| 3 | [Stage A curriculum templates and static expansion](./phase-03-stage-a-curriculum-templates-and-static-expansion.md) | Ready for Stage A cook |
| 4 | [Stage A evidence and bounded handoff](./phase-04-stage-a-evidence-and-bounded-handoff.md) | Ready for Stage A cook |
| 5 | [Stage B exact renderer and journey amendment](./phase-05-stage-b-exact-renderer-and-journey-amendment.md) | Blocked on Issue #10 release |
| 6 | [Stage B executable architecture lab and publication](./phase-06-stage-b-executable-architecture-lab-and-publication.md) | Blocked on Phase 5 |
| 7 | [Final verification rollback and exact-head approval](./phase-07-final-verification-rollback-and-exact-head-approval.md) | Blocked on Phase 6 |

## Dependencies

- Same-scope `blockedBy` is empty because the Issue #8 and Issue #10 plan directories are not
  present in this exact input tree and plan branches are not release artifacts. External release
  gates are normative in [Dependency and Release Gates](./dependency-and-release-gates.md).
- **Stage A:** Issue #8 Stage A is released at exact integration SHA `fecf6bb8…`; its 21-file
  contract set and additional version/command/tool inputs are read-only. The independently derived
  additions-only view lease is confined to exact new `architecture/expansions/i5-06/**` paths. The
  active unreleased Issue #8 Stage B lease `promotion-trust-vite-identifier-binding-v1` is not
  required and grants no authority.
- **Stage B:** exact passing merged Issue #10 real journey and released portal renderer SHA. Issue
  #10 is OPEN and not released, so all Stage B authorities remain empty.
- Owner comment
  [#5036142770](https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770)
  authorizes parallel planning only. It does not bypass either release dependency or a serialized
  contract/view/portal lease.
- Issue #6 local architecture sources, six manifest rows, six SVG/text pairs, render manifest,
  tool lock, and renderer/checker remain read-only. Expansion requires an additions-only lease and
  byte preservation proven against [Protected Architecture Baseline](./verification-evidence-and-protected-assets.md).

## Companion Contracts

- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Architecture and Curriculum Design](./architecture-and-curriculum-design.md)
- [Threat Model and Security](./threat-model-and-security.md)
- [Verification, Evidence, and Protected Assets](./verification-evidence-and-protected-assets.md)

## Stage Claims

| Stage | Earliest honest claim | Prohibited claim |
|---|---|---|
| A | Released-contract-valid Vietnamese curriculum, templates, static view expansion, deterministic render/text, and traceability candidate | Portal delivery, lab execution, reset, completion, fresh learner evidence, or Issue #10 renderer compatibility |
| B | One real architecture lab completes controlled failure, reset, verification, immutable evidence, and portal publication through exact released #8/#10 seams | Hosted/AWS execution, cloud resources, Terraform apply, cross-user security, or cryptographic non-repudiation |

## Current Authority

Present cook authority is Stage A only and is closed by the exact enumeration in the
[amendment](./stage-a-release-amendment.md). It creates 50 paths beneath the isolated architecture
expansion root, `learning/curriculum/**`, `mk/issue-5/i5-06.mk`, and curriculum tests/fixtures.
There are no modifies or deletes. Shared contracts and released validators are read-only.

```yaml
stageAInputSha: fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9
stageAFileAuthority: stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist
stageACommandAuthority: stage-a-release-amendment.md#exact-command-allowlist
stageBImplementationFileAllowList: []
stageBImplementationCommandAllowList: []
stageBDependencyReleaseShas: []
stageBPortalRendererPaths: []
```

No root `Makefile`, `docs/code-standards.md`, `release-manifest.json`, portal/shared-contract,
Issue #6 local-view, cloud/AWS/Terraform, other plan, or other worktree write is allowed.
`README.md`, other `docs/**`, and release metadata are also outside future Issue #11 cook
authority. Any user-facing documentation or release-note impact discovered during a staged
implementation requires a separate owner-authorized serialized handoff; it cannot broaden the
Stage A or Stage B allow-list.

## Workflow and Exit

- Workflow: `ck:plan` plus plan-to-cook-equivalent exact-release amendment and independent
  readiness audit through Herdr using `gpt-5.6-sol` at `xhigh` reasoning.
- Readiness checks cover CK status/strict validation, links/anchors, placeholders/future SHAs,
  dependency release objects, exact allow-list absence/overlap, requirements/scenario/RED/S3
  catalogues, 33 protected identities, architecture tool availability, diff hygiene, and a
  whole-plan sweep.
- The original validation and blocked audit remain historical. The current result is in
  [Stage A Readiness Audit](./audit/stage-a-readiness-audit-report.md).
- Not run: curriculum/product implementation, new renderer execution, portal/lab tests, learner
  journeys, PR/merge, cloud, AWS, or Terraform.

## Unresolved Questions

None for Stage A. Stage B remains intentionally unresolved until Issue #10 publishes its actual
merged journey/renderer contract.

## Validation Log

### Session 1 — 2026-07-22 — Fresh independent initial validation

Historical snapshot: Session 2 supersedes its Stage A dependency and empty-authority conclusions;
its Stage B block and non-runtime claim boundaries remain current.

**Trigger:** Validate exact planner output
`7620d168fb96cf9ae11e963501f65ea5a416af43` adversarially before readiness.

**Questions asked:** 0. The user supplied the exact dependency, stage, ownership, toolchain,
security, verification, transition, and publication decisions. Fresh repository/GitHub evidence
resolved the remaining factual checks; no genuine product decision was reopened.

#### Confirmed Decisions

- Stage A remains blocked on released Issue #8 contracts and may claim only static curriculum,
  template, traceability, and authorized deterministic expansion results.
- Stage B alone may consume the passing merged Issue #10 real journey/renderer and claim the real
  controlled-failure, reset, verify, evidence, completion, and portal lifecycle.
- Current file, command, dependency-release, renderer, fitness/evidence-schema, and view-lease
  authorities remain empty. Issue #6 `fitness-result-v1` is not a fallback for a future Issue #8
  evidence contract.
- The six Issue #6 views, rows, renders, hashes, toolchain, and source closure remain read-only;
  Structurizr wording grants no renderer or migration authority.
- Independent implementation review and repository-authorized human exact-head pre-merge
  approval remain mandatory for every future staged release.

#### Objective Corrections

- Separated the current Issue #6 command-result envelope from the future Issue #8 learning/
  evidence binding and required an exact released compatibility decision rather than a guessed
  direct schema binding.
- Restored accepted competency ID intent, including `J06`, and restored `D02`/`D03` in the
  curriculum graph without claiming I5-07 data-lab runtime delivery.
- Added stable template identity/version/supersession obligations and an explicit rule requiring
  dynamic/sequence plus deployment views for critical flows while keeping L3 concern-driven.
- Made the immutable evidence hash index a required, closed, orphan-rejecting record.

#### Verification Results

- **Tier:** Full (7 phases; Fact Checker, Flow Tracer, Scope Auditor, Contract Verifier)
- **Claims checked:** 105
- **Verified:** 105 | **Failed:** 0 | **Unverified:** 0
- Dependency absence is verified blocked state, not an implementation verification result.
- Full evidence: [Independent Validation Report](./validation/independent-validation-report.md).

#### Impact on Phases

- Phase 1: exact evidence-schema compatibility gate corrected; authority remains empty.
- Phase 2: RED obligations now cover template version/supersession and evidence-index integrity.
- Phase 3: competency IDs/prerequisites, template versioning, and critical-flow view admission
  corrected.
- Phase 4: evidence index and schema compatibility are explicit release criteria.
- Phases 5-7: no authority or execution change; whole-plan terminology rechecked.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all seven `phase-*.md` files, all five companion contracts, and the
  validation report.
- Decision deltas checked: 4.
- Reconciled stale references: 12.
- Unresolved contradictions: 0.
- Recommendation: proceed only to a fresh dependency-aware readiness audit; do not cook while
  either stage authority remains empty.

### Session 2 — 2026-07-22 — Exact-release Stage A amendment and readiness

**Trigger:** Re-audit from clean head `ab653f6edec73e5ef875723945d2e3cd7814b4e6` after Issue #8
Stage A release `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`.

#### Confirmed Decisions

- Stage A is useful and cookable as a static, machine-valid Vietnamese-first foundation-to-mid
  curriculum with deterministic text/SVG expansions and complete business-to-evidence trace.
- The active Issue #8 Stage B Vite identifier-binding lease and unreleased Issue #10 portal are
  explicit non-authorities; neither is consumed by Stage A.
- The Issue #6 exact-six roots and tools remain immutable. Five additions use a separate extension
  root and manifest seam; all 33 protected identities are preserved.
- Stage B remains empty and blocked. Stage A makes no portal, lab, reset, progress, completion,
  fresh learner-evidence, deployment, or cloud claim.

#### Current Authority

- Exact 50 create-only paths and exact command shapes:
  [Stage A amendment](./stage-a-release-amendment.md).
- Fresh audit result and machine-check evidence:
  [Stage A readiness audit](./audit/stage-a-readiness-audit-report.md).
