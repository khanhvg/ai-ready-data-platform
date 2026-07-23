---
title: I5-05 — Promotion-trust portal vertical slice
description: >-
  Stage A is merged and the released runner now enables one bounded Stage B
  promotion-trust journey.
status: in-progress
priority: P1
issue: 10
branch: plan/issue-10-promotion-portal
tags:
  - feature
  - frontend
  - security
  - tdd
  - critical
blockedBy: []
blocks: []
created: '2026-07-21T16:49:00.989Z'
createdBy: 'ck:plan'
source: skill
mode: fast-tdd-no-tasks
integrationBaseSha: 671201f78024786a9f2eba5e9e5fce7c78b4443d
correctionInputSha: 2f278eb25aaff9e050314b01d1be155b76793f11
planningValidation: v3-independent-validation-pass
readinessVerdict: stage-b-ready
cookScope: stage-b-promotion-trust
dependencyIssue7: RELEASED_PR22_MERGE_1806B6D
dependencyIssue8: RELEASED_FINAL_INTEGRATION_5644F01
dependencyIssue9: RELEASED_PR32_MERGE_671201F
stageAStatus: merged-pr31-post-merge-smoke-pass
stageBStatus: ready-to-cook
stageBReadinessInputSha: 8c77957ad3be84dc97e4633cdafd898ea9e431fa
portalStageAMergeSha: 041d4ca866e927a331e159fdf8216838b481a595
portalStageAReviewedHead: 473f54c2e0879d3037cbed25b2e7a3f0626d558d
runnerReleaseSha: 671201f78024786a9f2eba5e9e5fce7c78b4443d
runnerReviewedHead: 86a6c259ad384591777cf1d46f2f6c9ea6327361
---

# I5-05 — Promotion-trust portal vertical slice

## Stage B Readiness Amendment

Stage A shipped through PR #31 at merge
`041d4ca866e927a331e159fdf8216838b481a595`, reviewed head
`473f54c2e0879d3037cbed25b2e7a3f0626d558d`, with a passing clean-checkout
post-merge browser smoke. Issue #9 shipped through PR #32 at integration
`671201f78024786a9f2eba5e9e5fce7c78b4443d`, reviewed head
`86a6c259ad384591777cf1d46f2f6c9ea6327361`, with 66/66 release gates, all eight
operations, dbt multiprocessing, clean-checkout evidence/reset smoke, and zero runner-container
residue. The exact Stage B implementation base is `671201f…`.

Lane S authorizes one local-only cook scope:
`lesson → controlled failure → fixed released operations → verify → immutable evidence → reset →
completion/progress`. The exact authority is the 18-path write set and 15-command set in
[Phase 6](./phase-06-stage-b-real-journey-and-completion-integration.md). The browser submits only
fixed journey actions and a two-value learner decision; it never supplies an operation ID,
command, argv, environment, path, URL, SQL, image, package, plugin, or Docker option. The
portal-owned loopback controller wraps the released owner CLI and immutable evidence store; it
does not assert a runner HTTP API.

No runner, released/shared contract, root Make, golden-data, README, docs, CI, container, cloud,
AWS, or Terraform file is writable in this scope.

## Historical Stage A Overview

Recover Stage A from exact released integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986` after the independent review of failed PR #29 found
three Medium blockers: incomplete contemporaneous RED provenance, duplicated/invented content
authority, and an invalid retained-evidence publication with no required Chromium trace.

The correction preserves the exact final boundary: 33 create-only product/test paths, 18 command
shapes, and 85 released read-only inputs. It changes chronology and proof, not product scope.
Stage A remains a meaningful Vietnamese-first catalog → module → lesson → step static portal
slice with the released promotion-trust lesson and
`insufficient-evidence/no-common-grain`; runner, progress, completion, fresh learner evidence,
and the full product remain unavailable. Stage B remains blocked on Issue #9.

This output now includes its fresh independent validation and readiness audit. The audit made two
bounded plan-only corrections: a deterministic correction-subtree seed/delta proof for the fresh
integration-based worktree, and exact Chrome 150 product/version/executable-digest admission.
Stage A v3 was ready to cook only at the published readiness output and subsequently shipped as
PR #31. Historical statements below retain their original Stage A attribution; this amendment,
the dependency register, and Phase 6 are the current Stage B authority.

## Review Findings and Corrections

| Finding | Root correction |
|---|---|
| RED chronology was incomplete | One semantics-free callable scaffold commit, one complete tests-only commit, contemporaneous raw/sanitized RED through real unit/build/Make/Chromium paths, then semantic commits; commit/tree/log bindings are mandatory |
| Content authority was duplicated/invented | One validated released descriptor registry drives production catalog, app, router, static routes, and React routes; test-only structural descriptors are non-authoritative pure-function inputs and production-rejected |
| Evidence was stale and trace-free | One atomic current generation per tested head, complete non-self hash closure, all entries verified, one real Chromium trace with sources excluded, and stale generations classified as negative history |

The normative details are in the
[Stage A v3 recovery amendment](./stage-a-release-amendment.md) and
[post-review correction report](./audit/stage-a-v3-post-review-correction-report.md).

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Stage A exact dependency and callable scaffold gate](./phase-01-stage-a-exact-dependency-and-contract-gate.md) | Completed |
| 2 | [Stage A complete tests and contemporaneous RED](./phase-02-stage-a-tests-first-portal-foundations.md) | Completed |
| 3 | [Stage A released-registry semantics and portal slice](./phase-03-stage-a-static-lesson-shell-and-navigation.md) | Completed |
| 4 | [Stage A closed evidence and exact-head handoff](./phase-04-stage-a-bounded-verification-and-handoff.md) | Completed |
| 5 | [Stage B runner release and BFF gate](./phase-05-stage-b-runner-release-and-bff-gate.md) | Completed by PR #32 + this audit |
| 6 | [Stage B real journey and completion integration](./phase-06-stage-b-real-journey-and-completion-integration.md) | Ready to cook |
| 7 | [Stage B evidence release rollback and review](./phase-07-stage-b-evidence-release-rollback-and-approval.md) | Pending Phase 6 |

## Dependencies and Recovery Input

- Stage A consumes only the released Issue #7/#8 ancestry and exact final integration enumerated
  in [Dependency and Release Gates](./dependency-and-release-gates.md).
- Failed PR #29, branch `feature/issue-10-portal-stage-a-v2`, its commits, and its retained evidence
  are immutable negative history. They are not a source, fixture, replay target, or evidence
  authority for v3.
- After this correction receives a fresh independent validation and a separate fresh readiness
  audit, recovery creates `feature/issue-10-portal-stage-a-v3` in a new worktree directly from
  exact integration. Before the scaffold commit, seed only the exact correction subtree
  `92b620712d6fdbf69eb0901554dcf27ae357bc7e`, apply the exact `a9e5ee2…df013a3`
  validation delta, then apply the exact readiness delta from `df013a3…` to the 40-hex output
  named by the Issue #10 handoff. Prove the intermediate validation subtree is
  `60e9f41b517cf7ecfda9f85ce5038f8fadd8d981`, the final subtree equals the published readiness
  output, and every pre-scaffold delta is plan-directory-only.
- No v2 product, test, log, trace, manifest, evidence, or generated byte may be cherry-picked,
  copied, regenerated from a v2 artifact, or used as an oracle.
- Current Stage B dependency and implementation authority is pinned in
  [Dependency and Release Gates](./dependency-and-release-gates.md) and Phase 6. Historical Stage A
  amendments/reports are records of the earlier blocked state, not current authority.

## Companion Contracts

- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Architecture and API Boundaries](./architecture-and-api-boundaries.md)
- [Threat Model and Security](./threat-model-and-security.md)
- [Verification, Evidence, and UAT](./verification-evidence-and-uat.md)
- [Stage A v3 Recovery Amendment](./stage-a-release-amendment.md)
- [Historical Stage A Readiness Audit](./audit/stage-a-readiness-audit-report.md)
- [V3 Post-Review Correction Report](./audit/stage-a-v3-post-review-correction-report.md)
- [V3 Independent Validation Report](./validation/stage-a-v3-independent-validation-report.md)
- [V3 Readiness Audit Report](./audit/stage-a-v3-readiness-audit-report.md)

## Exact Stage Claims

| Stage | Earliest honest claim | Prohibited claim |
|---|---|---|
| A | Static lesson is understandable, navigable, accessible, and truthful with runner absent | Lab ran, reset occurred, evidence is fresh, progress persisted, lesson completed, or full product exists |
| B | One local promotion-trust journey using the exact released runner and learning contracts | Arbitrary runner input, browser-to-runner access, duplicate completion/evidence authority, unrelated lesson/full-product, or cloud claim |

## Stage A Invariants

1. Final product scope is exactly 33 creates, zero released modifies, and zero deletes.
2. The 18 command shapes and 85 released-input rows remain byte-exact.
3. The first product commit contains only the exact 22 callable, semantics-free scaffold paths.
4. The next commit contains all eight final tests; valid controls and one-field mutations use
   released inputs or private run-owned temporary bytes, never a fallback fixture.
5. RED is produced immediately at that tests-only head through the callable scaffold. Missing
   imports, expected echoes, unconditional failures, mocks, skips, predicate-only tests, and
   retrospective reconstruction are invalid.
6. Production has one hash-bound released descriptor registry. There is no `defaultCatalog`,
   `STEP_IDS`, duplicate route table, promotion switch, or test descriptor admitted as release
   authority.
7. The final tested head has one current evidence generation with all hashes valid, one
   sources-excluded Chromium trace, exact closure and privacy scans, and atomic publication.
8. The seven defensive requirements remain mandatory: authenticated child self-shutdown without
   mutable PID authority; schema-valid blocked `fitness-result-v2`; closed build inventory and
   request policy; exact runtime/lock/environment admission; generic seam; bounded artifacts; and
   complete defensive RED/S3 coverage.

## Ownership and Non-Overlap

Stage A created only its published 33 paths. Stage B may change only the 18 paths enumerated in
Phase 6. Root Make, released contracts and data, Issue #9 runner, Issue #11 curriculum, Issue #12
labs, Issue #13 profiles, README/docs, CI, container definitions, cloud, AWS, and Terraform remain
denied. The only Make change is the existing Issue #10-owned `mk/issue-5/i5-05.mk` fragment.

## Validation State

Historical validation and readiness records remain attributable to their original inputs. The
Stage A readiness conclusion at `2f278eb25aaff9e050314b01d1be155b76793f11` was invalidated by
the failed PR #29 review and cannot authorize v3.

### Session 4 — Stage A v3 post-review correction

- Exact correction input: `2f278eb25aaff9e050314b01d1be155b76793f11`.
- Review findings addressed: 3/3 at plan level.
- Scope retained: 33/33 paths, 18/18 commands, 85/85 released inputs.
- Product paths absent from v3 base: 33/33.
- Stage B: blocked on Issue #9.
- Required next gates: fresh independent plan validation, then fresh independent readiness audit.
- Cook authority: none.

### Session 5 — Fresh independent Stage A v3 validation

- Exact validation input: `a9e5ee26eacaec1b07ce9a25ac4b86da15f0b9a1`.
- Review findings independently accepted: 3/3 at plan level.
- Bounded validation fixes: exact same-run Chrome identity admission; explicit author-versus-
  independent evidence roles and PII/raw-record/remote-import privacy scans; removal of stale
  mutable-PID wording from the blocked Stage B phase.
- Scope unchanged: 33/33 paths = 22/22 scaffold + 8/8 tests + 3/3 later creates; 18/18 commands;
  85/85 released read-only inputs.
- Validation verdict: PASS. Readiness and cook authority: none until the separate fresh readiness
  audit passes at its exact output.

### Session 6 — Fresh independent Stage A v3 readiness audit

- Exact readiness input: `df013a3fd2cc87085eb1f7f264e6d25937a5ad13`.
- Exact integration/released input: `5644f01b4c0443a81f3af0bcce80f44c847cd986`.
- Bounded readiness fixes: deterministic correction/validation/readiness subtree replay before
  product writes; exact Chrome `150.0.7871.181` and executable SHA-256
  `b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85` across RED/GREEN.
- Scope unchanged: 33/33 = 22/22 + 8/8 + 3/3, 18/18 commands, 85/85 released inputs.
- Readiness verdict: Stage A v3 ready to cook at the published audit output. Stage B remains
  blocked on Issue #9.

### Whole-Plan Consistency Sweep

- Decision deltas: v3 branch/recovery, scaffold-first chronology, released-registry authority,
  authenticated self-shutdown, blocked result schema, same-run Chrome admission, truthful evidence
  roles/privacy classes, and current-generation trace/evidence closure.
- Files in scope: all 19 Markdown artifacts in this plan directory: `plan.md`, all seven phase
  files, current companion contracts, superseded historical reports, the v3 correction report,
  and the current independent validation report.
- Unresolved contradictions permitted before publication: zero.

### Session 7 — Standard-lane Stage B dependency amendment and readiness

- Audit input: `8c77957ad3be84dc97e4633cdafd898ea9e431fa`.
- Stage A: PR #31 merge `041d4ca866e927a331e159fdf8216838b481a595`, reviewed head
  `473f54c2e0879d3037cbed25b2e7a3f0626d558d`, post-merge browser smoke PASS.
- Runner: PR #32 integration `671201f78024786a9f2eba5e9e5fce7c78b4443d`, reviewed head
  `86a6c259ad384591777cf1d46f2f6c9ea6327361`, release and clean-checkout smoke PASS.
- Exact implementation base: `671201f78024786a9f2eba5e9e5fce7c78b4443d`.
- Exact authority: 18 Stage B paths, 15 commands, eight released runner operations.
- Adapter: portal-owned authenticated loopback BFF around the released owner CLI and immutable
  evidence store; no invented runner API and no runner/shared-core write.
- Journey: small/42 starter; released `headline-revenue-overweighted` controlled failure; learner
  changes from `claim-common-grain` to `retain-independent-grains`; verify
  `insufficient-evidence/no-common-grain` plus `METRIC_REFUND_NOT_ACCOUNTED`; display hash-verified
  immutable evidence; run `workspace.reset`; complete once through
  `learning-progress-authority-v1`.
- Lane S: focused code review with Critical/Important = 0 plus functional safety tests. No
  separate red-team/security/human ceremony.
- Cloud action: none.

### Stage B Whole-Plan Consistency Sweep

- Normative files reread: `plan.md`, `dependency-and-release-gates.md`,
  `architecture-and-api-boundaries.md`, `requirements-and-risk-traceability.md`, and all seven
  phase files.
- Decision deltas checked: 9.
- Reconciled current Stage B references: dependency status, base SHA, adapter boundary, exact
  operations, write set, commands, journey order, completion/reset rules, and Lane S review gate.
- Historical Stage A blocked statements remain historical rather than current authority.
- Unresolved contradictions: 0.

## Plan Exit

The Stage B dependency amendment/readiness audit has passed after strict CK validation/status,
links/anchors, scope, command, evidence, protected/privacy/diff, exact-input, feasibility, and
live-state checks. Move Issue #10 to `ready to cook` only after this output is committed, pushed,
and local/upstream/live equality is proved. Cook must begin at exact integration
`671201f78024786a9f2eba5e9e5fce7c78b4443d`. This authorizes only
`stage-b-promotion-trust`; it is not implementation review, merge, release, Issue completion, or
cloud authority.
