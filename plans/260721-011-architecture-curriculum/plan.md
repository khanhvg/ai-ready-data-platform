---
title: "I5-06 — Architecture curriculum, templates, and fitness functions"
description: "Authorize one bounded scaffold-first Stage A cook while keeping portal-dependent Stage B blocked."
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
inputSha: "1c62b68159ffc48cc2f063c137cb9072d8ed741f"
originalPlanInputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
validationStatus: passed-fresh-independent-plan-validation
currentValidationReport: "validation/260722-stage-a-v3-independent-validation-report.md"
validationOutputAttestation: "external-issue-comment-on-containing-commit"
validationOutputSha: "4add8e1b45c62279141c018a9748b473b49b2b2f"
historicalValidationInputSha: "7620d168fb96cf9ae11e963501f65ea5a416af43"
historicalValidationReport: "validation/independent-validation-report.md"
historicalReadinessAuditInputSha: "1287fe35aa9ab29a97daa541f39a624d01a77d31"
historicalReadinessAuditReport: "audit/readiness-audit-report.md"
stageAAmendmentStartSha: "ab653f6edec73e5ef875723945d2e3cd7814b4e6"
postReviewAmendmentStartSha: "1c62b68159ffc48cc2f063c137cb9072d8ed741f"
v3CleanBaseSha: "c07c9a080be7be88447aac497bdf0a2b5fddd020"
validatedAmendmentSha: "4add8e1b45c62279141c018a9748b473b49b2b2f"
auditedAmendmentSha: null
stageAImplementationInputSha: null
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
integrationReleaseSha: "5644f01b4c0443a81f3af0bcce80f44c847cd986"
integrationReleaseTree: "a38594d420fe7df2b30265a8a72bb5fad1698012"
stageAAmendment: "stage-a-release-amendment.md"
historicalStageAReadinessAudit: "audit/stage-a-readiness-audit-report.md"
currentReadinessAudit: "audit/260722-stage-a-v3-readiness-audit-report.md"
readinessOutputAttestation: "external-issue-comment-on-containing-commit"
readinessVerdict: ready-to-cook-stage-a-whole-plan
implementationAuthority: stage-a-whole-plan-after-exact-derived-input
stageAStatus: ready-to-cook
stageBStatus: blocked-on-issue10
stageAFileAuthority: "stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist"
stageACommandAuthority: "stage-a-release-amendment.md#exact-command-allowlist"
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
`ab653f6edec73e5ef875723945d2e3cd7814b4e6` bound Stage A to released integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, but independent review of failed v2 proved that
amendment's tests-only chronology impossible. Starting from exact clean local/upstream/live plan
head `1c62b68159ffc48cc2f063c137cb9072d8ed741f`, the
[post-review scaffold-first amendment](./stage-a-release-amendment.md) now proposes the corrected
50 create-only paths, 16 commands, requirements, tests, resource/visual/evidence/cleanup bounds,
and rollback gates. Fresh independent validation passed after bounded plan-only corrections to
live Issue #8 state, exact RED entrypoints/outcome codes/controls, and closed controller child-tool
admission. This fresh readiness audit then reconciled the terminal PR #28 release, passed the
whole corrected Stage A plan, and authorized the exact whole-Stage-A cook scope after the
derived-input handoff.

Future v3 implementation uses the existing clean worktree at
`c07c9a080be7be88447aac497bdf0a2b5fddd020`. It applies, with recorded `-x` provenance, exact plan
commits `788ea45331a34e34b0d330e568a39ee6c6566e63`,
`4add8e1b45c62279141c018a9748b473b49b2b2f`, and the externally attested readiness output commit,
then creates one non-fast-forward reconciliation merge with exact released integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986`. No reset, rebase, rewrite, force-push, worktree
replacement, or failed product/test/evidence reuse is allowed. Failed v1 `0f765d3…`, failed v2
`482591d…`, PR #27, and their retained evidence remain immutable negative evidence and are not
ancestors or inputs to v3.

Stage A is a machine-valid curriculum/template/static-view foundation. It cannot claim portal
delivery, an executable lab, runner, reset, progress, completion, fresh learner evidence, or
learner effectiveness. Issue #8's released Stage B Vite identifier-binding bytes are present only
through integration ancestry; they remain an explicit read-only non-authority and are not consumed
by Issue #11. Stage B remains blocked on a passing merged Issue #10 real
journey and released renderer; its file, command, dependency, and renderer lists remain empty.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Freeze authority and dependency gates](./phase-01-freeze-authority-and-dependency-gates.md) | Ready to execute at exact derived v3 input |
| 2 | [Stage A scaffold-first TDD contract and preservation](./phase-02-stage-a-tests-first-contract-and-preservation.md) | Blocked on Phase 1; scaffold-first protocol proposed |
| 3 | [Stage A curriculum templates and static expansion](./phase-03-stage-a-curriculum-templates-and-static-expansion.md) | Blocked on recorded public-path RED |
| 4 | [Stage A evidence and bounded handoff](./phase-04-stage-a-evidence-and-bounded-handoff.md) | Blocked on Phases 1-3 |
| 5 | [Stage B exact renderer and journey amendment](./phase-05-stage-b-exact-renderer-and-journey-amendment.md) | Blocked on Issue #10 release |
| 6 | [Stage B executable architecture lab and publication](./phase-06-stage-b-executable-architecture-lab-and-publication.md) | Blocked on Phase 5 |
| 7 | [Final verification rollback and exact-head approval](./phase-07-final-verification-rollback-and-exact-head-approval.md) | Blocked on Phase 6 |

## Dependencies

- Same-scope `blockedBy` is empty because the Issue #8 and Issue #10 plan directories are not
  present in this exact input tree and plan branches are not release artifacts. External release
  gates are normative in [Dependency and Release Gates](./dependency-and-release-gates.md).
- **Stage A:** Issue #8 Stage A contract authority remains exact SHA `fecf6bb8…`; its 21-file
  contract set and additional version/command/tool inputs are read-only. The independently derived
  additions-only view lease is confined to exact new `architecture/expansions/i5-06/**` paths.
  PR #28 is released at integration `5644f01b…`, but its
  `promotion-trust-vite-identifier-binding-v1` bytes are not required and grant no Issue #11
  authority.
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

The fresh [readiness audit](./audit/260722-stage-a-v3-readiness-audit-report.md) authorizes one
whole Stage A cook after the exact derived-input handoff. The
[amendment](./stage-a-release-amendment.md) closes exactly 50 final create-only paths and 16
command shapes, partitioned into a 7-path
semantics-free public scaffold, a direct-child 5-path complete tests/fixture commit, and a
38-path semantic complement after recorded RED. There are no final modifies or deletes relative
to the v3 input. Shared contracts and released validators remain read-only.

```yaml
stageAContractAuthoritySha: fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9
integrationReleaseSha: 5644f01b4c0443a81f3af0bcce80f44c847cd986
integrationReleaseTree: a38594d420fe7df2b30265a8a72bb5fad1698012
v3CleanBaseSha: c07c9a080be7be88447aac497bdf0a2b5fddd020
validatedAmendmentSha: 4add8e1b45c62279141c018a9748b473b49b2b2f
auditedAmendmentSha: null
stageAImplementationInputSha: null
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

- Workflow: `ck:plan` post-review author correction through Herdr using `gpt-5.6-sol` at `xhigh`
  reasoning, followed by completed separate fresh xhigh independent plan validation and readiness
  audit.
- Readiness checks cover CK status/strict validation, links/anchors, placeholders/future SHAs,
  dependency release objects, exact allow-list absence/overlap, requirements/scenario/RED/S3
  catalogues, 33 protected identities, architecture tool availability, diff hygiene, and a
  whole-plan sweep.
- The original validation, blocked audit, and prior Stage A readiness audit remain immutable
  historical snapshots. Their stale readiness/tests-only rules are explicitly superseded in the
  current amendment; none is current cook authority.
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

Historical snapshot: independent v2 review comments `5046838991` and `5046839495` supersede the
readiness and tests-only chronology below. The 50-path, 33-protected-identity, Stage B, S3, and
non-runtime boundaries remain useful inputs; the cookability conclusion does not.

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

- Historical exact 50 create-only paths and command shapes:
  [Stage A amendment](./stage-a-release-amendment.md).
- Superseded audit snapshot:
  [Stage A readiness audit](./audit/stage-a-readiness-audit-report.md).

### Session 3 — 2026-07-22 — Post-review scaffold-first author correction

**Trigger:** Correct all seven findings from the independent PR and Issue reviews while preserving
the exact 50-path final scope, 33 protected identities, released contracts/OpenAPI/Make/golden
data, S3, and blocked Stage B.

#### Decision Deltas

- Replaced impossible tests-only-from-pristine chronology with an exact 7-path semantics-free
  scaffold, direct-child 5-path complete tests/fixture commit, contemporaneous public-path
  semantic RED, and only then the 38-path semantic complement.
- Froze promotion `decision=insufficient-evidence` and `reason=no-common-grain` against the exact
  released schema; completed template compatibility/registry/reciprocal binding rules.
- Defined 11 distinct critical-flow step vectors, dynamic-relation/deployment-topology binding,
  and conceptual-only local/AWS bridge semantics.
- Added exact 120 s/180 s process-group resource control, aggregate RSS/output/file/process
  bounds, TERM→KILL→wait, measured evidence, static visual gates, and honest ignored-root cleanup.
- Changed future v3 base to clean `c07c9a080be7be88447aac497bdf0a2b5fddd020` plus only the
  eventual independently validated/audited plan diff. Failed v1/v2 remain negative evidence.

#### Current Disposition

- Historical author self-check only at `788ea45331a34e34b0d330e568a39ee6c6566e63`; Session 4 is
  the current independent validation disposition.
- Implementation authority: `none`.
- Required next phase: fresh plan-readiness audit at the exact pushed validation output.

### Session 4 — 2026-07-22 — Fresh independent post-review validation

**Trigger:** Validate exact clean local/upstream/live correction input
`788ea45331a34e34b0d330e568a39ee6c6566e63` against PR #27 review comment `5046838991`, author
correction comment `5047513123`, released integration `fecf6bb8…`, and clean v3 base `c07c9a0…`.

#### Bounded Validation Corrections

- Reconciled live Issue #8 twice: first from stale `ready to cook` to reviewed PR #28, then to its
  during-validation merge `5644f01b…`. The merge has `fecf6bb8…` as first parent, no post-merge
  release handoff at validation time, and zero overlap with the 50/33/21 Issue #11 closures, so it
  remains an explicit non-authority while `fecf6bb8…` stays the pinned released dependency.
- Named the exact four callable RED entrypoint IDs, required a parse/reach-valid control for every
  case family, and closed 82 exact stable outcome codes across the 22 RED families. Fixture/test
  metadata is stripped before the same final public callable is invoked.
- Clarified that the exact 16 commands are top-level operator shapes and closed the controller's
  internal Python/`ps`/Node/npm/LikeC4 child-tool admission without adding a command shape.

#### Verification Results

- **Tier:** Full (7 phases; all four verification roles plus semantic/security/resource review).
- **Claims checked:** 105 phase claims plus exact catalog/identity/ancestry/link/status checks.
- **Verified:** all after bounded fixes | **Failed:** 0 | **Unverified:** 0.
- Detailed evidence: [Stage A v3 independent validation report](./validation/260722-stage-a-v3-independent-validation-report.md).

### Whole-Plan Consistency Sweep — Session 4

- Files reread: `plan.md`, all seven phase files, five companion contracts, the amendment, and
  the current validation report.
- Decision deltas checked: 4.
- Reconciled stale references: live Issue #8 state, validation/readiness status, exact entrypoint
  naming, and exact outcome/tool-admission language.
- Unresolved contradictions: 0.
- Recommendation: proceed only to a fresh plan-readiness audit; do not cook or begin Stage B.

### Session 5 — 2026-07-22 — Fresh independent Stage A v3 readiness

**Trigger:** Audit exact clean local/upstream/live validation output
`4add8e1b45c62279141c018a9748b473b49b2b2f` after Issue #8 / PR #28 completed its canonical
merge and pristine release.

#### Readiness Decisions

- PR #28 is merged as `5644f01b4c0443a81f3af0bcce80f44c847cd986`, ordered parents
  `fecf6bb8…` and `12e1742…`, tree `a38594d…`; Issue #8 is closed with `shipped`, and release
  comment `5047954510` is terminal PASS.
- The released 28-path delta has zero overlap with the Issue #11 50 future paths, 33 protected
  identities, and 21 Stage A contract paths. Its Vite binding stays read-only and outside Issue
  #11 authority.
- The clean v3 worktree remains at `c07c9a0…`, with no upstream, ignored bytes, active writer, or
  failed feature ancestry. Its plan directory equals `1c62b681…` and its non-plan tree equals
  `fecf6bb8…`.
- Derive the exact implementation input without rewrite: apply `788ea453…`, `4add8e1b…`, and the
  externally attested readiness output with `git cherry-pick -x`, then merge exact integration
  `5644f01b…` using `--no-ff`. Record every resulting commit/parent and re-run the full preflight
  before the first scaffold write.
- Stage A whole-plan cook scope passes. Stage B remains empty and blocked on Issue #10 plus a
  released Stage A implementation.

#### Verification Results

- Exact 7/5/38 chronology, four public RED entrypoints, 22 valid-control/mutation families, and 82
  unique outcome codes pass.
- All seven PR #27 findings pass; 50 paths, 16 commands, 33 protected identities, 21 contracts,
  16 OpenAPI operations, S3, resource feasibility, evidence/cleanup, and ownership overlap pass.
- Detailed evidence: [Stage A v3 readiness audit](./audit/260722-stage-a-v3-readiness-audit-report.md).
