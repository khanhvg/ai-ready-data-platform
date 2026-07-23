---
title: "I5-06 — Architecture curriculum, templates, and fitness functions"
description: "Stage A v4 passed fresh readiness with bounded plan-only environment and byproduct closure."
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
inputSha: "287dc08546f7013ca8c187b318e0a2f7cf832e55"
integrationReleaseSha: "5644f01b4c0443a81f3af0bcce80f44c847cd986"
integrationReleaseTree: "a38594d420fe7df2b30265a8a72bb5fad1698012"
validationStatus: passed-independent-stage-a-v4-with-bounded-plan-fix
validationInputSha: "dfd8e4c7704de5e1392d1028f5a25757a3e77166"
currentValidationReport: "validation/260723-stage-a-v4-independent-validation-report.md"
readinessVerdict: ready-to-cook-stage-a-v4
readinessInputSha: "68bfc6b53ced963997266dbc4960aff4a8ca52d4"
currentReadinessReport: "audit/stage-a-readiness-audit-report.md"
implementationAuthority: stage-a-v4-whole-plan
cookScope: stage-a-v4-whole-plan
stageAStatus: ready-to-cook-stage-a-v4
stageBStatus: blocked-on-passing-merged-issue-10-journey
stageAAmendment: "stage-a-release-amendment.md"
stageAFileAuthority: "stage-a-release-amendment.md#exact-stage-a-tracked-write-allowlist"
stageACommandAuthority: "stage-a-release-amendment.md#exact-command-allowlist"
stageBImplementationFileAllowList: []
stageBImplementationCommandAllowList: []
historicalValidationReport: "validation/260722-stage-a-v3-independent-validation-report.md"
historicalReadinessAudit: "audit/260722-stage-a-v3-readiness-audit-report.md"
postReviewAuthority: "https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239"
v4Authorization: "https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064"
correctionReport: "reports/260723-stage-a-v4-post-review-correction-report.md"
---

# I5-06 — Architecture curriculum, templates, and fitness functions

## Outcome

This corrected v4 plan withdraws every prior Issue #11 Stage A readiness or cook claim and has now
passed fresh independent validation plus a separate fresh readiness audit. It defines a plan-only
lineage rooted directly at released integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986`, repository-level TDD for all 22 RED families and 82
codes, one exact 16-command runtime contract, a closed 12-template lifecycle, source-derived
visible render parity, meaningful lifecycle content for exactly 20 modules, the corrected local
OpenMetadata bridge, and truthful raw/sanitized evidence retention.

The exact review finding authority is
[PR #30 comment 5050486239](https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239).
The recovery authority is
[Issue #11 comment 5050513064](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064).
The complete normative contract is the
[Stage A v4 amendment](./stage-a-release-amendment.md); the
[correction report](./reports/260723-stage-a-v4-post-review-correction-report.md) records the
author's checks. Neither document is the readiness verdict; the separate current result is the
[Stage A v4 readiness report](./audit/stage-a-readiness-audit-report.md).

## Frozen scope

- Stage A remains exactly 50 create-only product/test paths, 16 top-level command shapes, 33
  protected identities, 21 released contracts, 20 distinct modules, 12 useful templates, 11
  flows, eight conceptual bridges, and five useful views.
- The promotion example remains exactly `decision=insufficient-evidence` and
  `reason=no-common-grain`.
- Stage A is static curriculum, templates, traceability, and deterministic view expansion only.
  It cannot claim a portal, executable learner lab, reset execution, progress, completion, fresh
  learner evidence, or learner effectiveness.
- OpenAPI/golden-runtime/S3/resource boundaries stay mandatory. AWS is conceptual only. No cloud,
  container, AWS, Terraform, deployment, merge, approval, or feature action is authorized.
- Stage B has empty file/command/renderer authority and remains blocked until Issue #10 has a
  passing merged real journey and released renderer.

## Lineage and authority

The v4 plan branch is reconstructed so exact integration `5644f01b…` is its ancestor and every
commit after integration is plan-only. The correction author may publish plan and report commits
only. Fresh independent validation and then fresh readiness may add later plan-only commits on the
same lineage. The eventual cook input is the exact pushed readiness head; implementation may begin
only if the direct integration-to-cook diff contains plan paths under this plan directory and no
product/test path, while all 50 future paths are absent and the protected/released bytes match.

The cook then creates the exact 50 allow-listed paths. At every implementation gate:

```text
integration -> cook input       = plan provenance only
cook input -> Stage A candidate = exactly 50 create-only product/test paths
integration -> candidate        = plan provenance union the exact 50 paths
```

No commit based on `c07c9a080be7be88447aac497bdf0a2b5fddd020`, no failed v1/v2/v3 product,
test, render, evidence, branch, PR, worktree, or commit, and no cherry-pick/copy of those bytes is
an input. Local, upstream, freshly fetched remote, and live GitHub branch identities must agree at
each validation, readiness, and cook handoff.

## Phases

| Phase | Name | Status |
|---|---|---|
| 1 | [Freeze authority and dependency gates](./phase-01-freeze-authority-and-dependency-gates.md) | Readiness passed; cook preflight pending |
| 2 | [Repository-level scaffold-first TDD](./phase-02-stage-a-tests-first-contract-and-preservation.md) | Blocked on Phase 1 |
| 3 | [Curriculum, templates, and source-derived views](./phase-03-stage-a-curriculum-templates-and-static-expansion.md) | Blocked on recorded repository RED |
| 4 | [Truthful evidence and bounded handoff](./phase-04-stage-a-evidence-and-bounded-handoff.md) | Blocked on Phases 1–3 |
| 5 | [Stage B dependency amendment](./phase-05-stage-b-exact-renderer-and-journey-amendment.md) | Blocked on passing merged Issue #10 journey |
| 6 | [Stage B executable lab and publication](./phase-06-stage-b-executable-architecture-lab-and-publication.md) | Blocked on Phase 5 |
| 7 | [Final verification and exact-head approval](./phase-07-final-verification-rollback-and-exact-head-approval.md) | Blocked on Phase 6 |

## Companion contracts

- [Requirements and risk traceability](./requirements-and-risk-traceability.md)
- [Dependency and release gates](./dependency-and-release-gates.md)
- [Architecture and curriculum design](./architecture-and-curriculum-design.md)
- [Threat model and security](./threat-model-and-security.md)
- [Verification, evidence, and protected assets](./verification-evidence-and-protected-assets.md)

Each companion document defers to the amendment for exact paths, commands, RED codes, lifecycle,
render, evidence, and lineage rules. A contradiction is a validation failure; it cannot broaden
the amendment.

## Validation and handoff gates

The fresh independent validator bound input `dfd8e4c7704de5e1392d1028f5a25757a3e77166`
and completed CK 4.5.2 strict validation/status, link and anchor checks,
placeholder/future-SHA checks, exact path/command/RED/template/render/trace/evidence counts,
S3/private-path/secret scans, protected/released identity comparisons, and the direct integration
diff. The result and one bounded template-instance correction are recorded in the
[Stage A v4 independent validation report](./validation/260723-stage-a-v4-independent-validation-report.md).
A separate fresh readiness reviewer bound exact pushed validation head
`68bfc6b53ced963997266dbc4960aff4a8ca52d4`, closed the literal controller environment and actual
released-command byproduct/cleanup layouts with bounded plan-only fixes, and returned
`READY_TO_COOK` for the whole Stage A v4 scope. The containing readiness output is attested after
push rather than self-referenced in a tracked file.

The next authorized phase is `cook-issue11-stage-a-v4`. The Issue may move only from
`ready for plan audit` to `ready to cook`. This grants no product result, independent
implementation review, approval, merge, release, Stage B, runner, container, cloud, AWS, or
Terraform authority.

## Validation log

### Sessions 1–5 — historical v1/v2/v3 work

The existing reports under `validation/` and `audit/` are immutable historical evidence for their
recorded SHAs. PR #30 invalidated their current authority. They are not copied, edited, or reused
as v4 validation/readiness evidence.

### Session 6 — 2026-07-23 — v4 post-review author correction

- Started from exact clean local/upstream/live input
  `287dc08546f7013ca8c187b318e0a2f7cf832e55` on the required branch.
- Reconstructed the eight plan-only commits directly onto exact integration `5644f01b…`; no
  product/test/evidence bytes or failed feature ancestry were imported.
- Corrected all eight PR #30 findings while preserving the frozen Stage A counts and Stage B block.
- Performed author/self plan checks only. Fresh independent validation and readiness remain future
  work and no implementation authority is claimed.

### Session 7 — 2026-07-23 — fresh independent Stage A v4 validation

- Bound exact clean local/upstream/live input
  `dfd8e4c7704de5e1392d1028f5a25757a3e77166` and direct integration `5644f01b…` ancestry.
- Reproduced the closed counts, 50-path absence, 33/33 protected and 21/21 released identities,
  repository-level RED implementability, 16-command simulation, visible parity, governance,
  evidence, S3, resource, Stage B, and active-lane separation checks.
- Added the missing stable per-instance ID and exact compatibility binding to the template
  lifecycle and its real repository mutations; frozen counts and public scope did not change.
- Returned PASS for plan validation only. Fresh readiness remains separate and implementation
  authority remains `none`.

### Sessions 8–9 — 2026-07-23 — recovered and completed Stage A v4 readiness

- Session 8 bound exact clean local/upstream/live input
  `68bfc6b53ced963997266dbc4960aff4a8ca52d4` in a role-separated Herdr/Codex xhigh session.
- Reproduced integration derivation, active-lane separation, all frozen catalogues, protected and
  released bytes, repository-level RED cookability, template/module/render/governance/evidence
  closure, S3/resource bounds, and empty blocked Stage B authority.
- Literal-admitted all 16 command shapes with one mode-0700 `$I11_RUNTIME`, the full hash-locked
  Python install, released admission, current target resolution, and exact future route seams.
- Added only the exact `env -i` controller table and the real released `.artifacts` byproduct
  copy/cleanup contract discovered during literal replay; product scope and counts are unchanged.
- Session 8 ended at context compaction before a semantic verdict or publication. Session 9
  preserved and reviewed all eight edits, fixed the two bounded scanner findings, repeated the
  exact current validation matrix and live lease/release audit, and finalized the tracked report.
- Returned `READY_TO_COOK` only for `stage-a-v4-whole-plan`; exact output identity is external.
