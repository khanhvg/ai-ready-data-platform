---
title: "I5-06 — Architecture curriculum, templates, and fitness functions"
description: "Plan a Vietnamese-first foundation-to-mid architecture learning product in two exact-dependency stages without inventing contracts, renderer seams, or cook authority."
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
readinessVerdict: blocked-dependencies
implementationAuthority: none
stageAStatus: blocked-on-issue-8-released-contracts-and-additions-only-view-seam
stageBStatus: blocked-on-stage-a-and-issue-10-passing-merged-real-journey
currentImplementationFileAllowList: []
currentImplementationCommandAllowList: []
---

# I5-06 — Architecture curriculum, templates, and fitness functions

## Overview

Plan a Vietnamese-first, foundation-to-mid, hands-on architecture learning product. Every module
must trace a business outcome through capability, stakeholder concern, FR/NFR, design options,
C4/data/integration/security/deployment views, an ADR or admitted pattern, implementation intent,
automated evidence, and operations/resilience/security/cost/governance consequences. A topic list
or Markdown dump is not a release.

Planning is complete at exact clean input
`24be3b34c6b0fcdbd07c5800dcab349054e34713`; implementation is not authorized. Stage A may become
cookable only after Issue #8 publishes exact released learning contracts and this plan receives a
fresh exact-SHA amendment, independent revalidation, and fresh readiness authorization. Stage A
may create only a curriculum/template/static architecture-expansion candidate. It cannot claim
portal delivery, an executable lab, completion, reset, or fresh learner evidence. Stage B alone
may become cookable after the exact passing merged Issue #10 real journey and released portal
renderer SHA is pinned through the same amendment/revalidation/readiness sequence. Only Stage B
may claim the controlled failure → reset → verify → evidence journey.

No text in this plan assigns a future dependency SHA, released contract path/version, portal
renderer module, fitness-schema implementation path, fixture path, architecture extension seam,
or concrete implementation command/file allow-list. Those values must be copied from real
released handoffs by later amendments; a guessed equivalent is a hard STOP.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Freeze authority and dependency gates](./phase-01-freeze-authority-and-dependency-gates.md) | Pending |
| 2 | [Stage A tests-first contract and preservation](./phase-02-stage-a-tests-first-contract-and-preservation.md) | Pending |
| 3 | [Stage A curriculum templates and static expansion](./phase-03-stage-a-curriculum-templates-and-static-expansion.md) | Pending |
| 4 | [Stage A evidence and bounded handoff](./phase-04-stage-a-evidence-and-bounded-handoff.md) | Pending |
| 5 | [Stage B exact renderer and journey amendment](./phase-05-stage-b-exact-renderer-and-journey-amendment.md) | Pending |
| 6 | [Stage B executable architecture lab and publication](./phase-06-stage-b-executable-architecture-lab-and-publication.md) | Pending |
| 7 | [Final verification rollback and exact-head approval](./phase-07-final-verification-rollback-and-exact-head-approval.md) | Pending |

## Dependencies

- Same-scope `blockedBy` is empty because the Issue #8 and Issue #10 plan directories are not
  present in this exact input tree and plan branches are not release artifacts. External release
  gates are normative in [Dependency and Release Gates](./dependency-and-release-gates.md).
- **Stage A:** exact released Issue #8 learning contracts. Issue #8 is currently OPEN; its
  latest repair candidate is awaiting a fresh exact-head review. It has no passing review,
  human approval, merge, release, or downstream authority. Stage A also requires an admitted
  additions-only architecture seam and exact view lease.
- **Stage B:** passing Stage A plus the exact passing merged Issue #10 real journey and released
  portal renderer SHA. Issue #10 is currently OPEN at `ready for plan audit`; its blocked
  readiness audit authorizes no cook scope, and no implementation PR or merged real-journey
  release exists.
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

The Issue #11 ownership ceiling is `learning/curriculum/**`, the architecture lab, Issue/P6-owned
AWS/publish architecture expansion sources/renders, implementation ADR templates,
`mk/issue-5/i5-06.mk`, and an additions-only view lease. This ceiling is not present cook
authority. At this planner output:

```yaml
implementationFileAllowList: []
implementationCommandAllowList: []
dependencyReleaseShas: []
portalRendererPaths: []
fitnessSchemaBindings: []
```

No root `Makefile`, `docs/code-standards.md`, `release-manifest.json`, portal/shared-contract,
Issue #6 local-view, cloud/AWS/Terraform, other plan, or other worktree write is allowed.
`README.md`, other `docs/**`, and release metadata are also outside future Issue #11 cook
authority. Any user-facing documentation or release-note impact discovered during a staged
implementation requires a separate owner-authorized serialized handoff; it cannot broaden the
Stage A or Stage B allow-list.

## Workflow and Exit

- Workflow: `ck:plan` fast/TDD/no-task equivalent. Accepted master discovery/planning/readiness
  supplied research; the user reserved independent validation and audit for fresh later phases.
- Checks in this planner: plan status, frontmatter/static structure, local links/anchors,
  dependency state, protected hashes/blobs, staged scope, formatting, and S3 secret/private-path
  scans only.
- Not run by the planner: plan validation, red-team/readiness, curriculum/architecture commands, renderer,
  lab/portal tests, native GUI/manual matrix, cook, PR, merge, cloud, AWS, or Terraform.
- Validation completed with bounded fixes at the exact planner input. The fresh dependency-aware
  readiness audit at exact input `1287fe35aa9ab29a97daa541f39a624d01a77d31` is
  `BLOCKED_DEPENDENCIES` with no implementation authority. The next phase is dependency release,
  then an exact-SHA amendment, fresh independent revalidation, and fresh readiness. No partial
  cook is authorized.

## Unresolved Questions

None for planning. Exact dependency releases and the implementation authorities derived from
them are intentionally absent and block cook, not completion of this planner-only artifact.

## Validation Log

### Session 1 — 2026-07-22 — Fresh independent initial validation

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
