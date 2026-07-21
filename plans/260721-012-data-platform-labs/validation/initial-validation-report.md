# Fresh independent initial plan validation — Issue #12 / I5-07

**Verdict: PASS WITH FIXES.** Seven bounded plan defects were corrected. No unresolved plan defect
remains, but implementation readiness is still dependency-blocked by unreleased Issue #8
contracts, unreleased Issue #9 private runner plus an exact serialized data lease, and an unmerged
Issue #10 passing real journey.

This was an isolated `$ck:plan validate` full-tier session. It did **not** run a readiness audit,
implement labs/verifiers/pipeline seams, start optional services, create fixtures, alter golden
SQL/views, create a PR, merge, or perform AWS/Terraform/cloud actions.

## Inputs and authority

| Input | Verified value / disposition |
|---|---|
| Repository/branch | `khanhvg/ai-ready-data-platform`, `plan/issue-12-data-labs` |
| Initial validation input | `24ff21db72e0d08d34b62c3280e76ab6329665eb` |
| Initial input equality | Clean local HEAD = tracking ref = fresh live remote branch |
| Planner/product input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` |
| Issue #6 authority | Same `24be3b34c6b0fcdbd07c5800dcab349054e34713`; closed with `shipped` |
| Planner handoff | [Comment `5038067548`](https://github.com/khanhvg/ai-ready-data-platform/issues/12#issuecomment-5038067548), `PLANNER_ONLY_NOT_VALIDATED` |
| Issue #6 merged proof | [Comment `5030452888`](https://github.com/khanhvg/ai-ready-data-platform/issues/6#issuecomment-5030452888), `HANDOFF_MERGED_VERIFIED` |
| Issue #12 entry state | Open; `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `data-platform`, `recovery` |
| Runtime request | Codex `gpt-5.6-sol`, `model_reasoning_effort="xhigh"`; recorded as user-specified validator identity |

The validator independently observed Issue #8 open at `ready to cook`, Issue #9 open at `ready
for plan audit`, and Issue #10 open at `ready for plan audit`. None is a released dependency
handoff. No branch head, plan SHA, label or future command declaration was accepted as current
authority.

## Method

Five phases require the full verification tier. All four roles were applied:

- Fact checker: paths, labels, SHAs, hashes, counts, exact IDs and current absences.
- Flow tracer: Make fragment include, Airflow TaskFlow delegates, curated-asset consumers,
  sequential Iceberg drop/create/read-back and count-only OpenMetadata verification.
- Scope auditor: plan-only diff, absent current Issue #12 roots, immutable Issue #6 trees and
  lease-bounded future mutation.
- Contract verifier: Issue #6 readers/contracts, future command declarations, stage dependency
  gates, final command contract and every downstream authority boundary.

The full-tier sample checked 86 plan claims: Phase 1 = 19, Phase 2 = 16, Phase 3 = 19, Phase 4 =
15, Phase 5 = 17. After the bounded corrections below: **86 verified, 0 failed, 0 unverified**.
Static verification separately checked 46 local Markdown links, 12 protected Git objects, seven
critical SHA-256 values, all empty authority fields and the exact 12-file planner-only diff.

## Adversarial contract results

| Validation contract | Result | Evidence |
|---|---|---|
| Business/learning/FR/NFR/data/threat/test/evidence/recovery trace; Vietnamese-first hands-on, not docs dump | PASS after fix | Added business outcomes and learner-action/expected-actual gate; existing trace/recovery rows remain linked |
| Stage A static/non-mutating/non-runnable; Stage B exact runner+lease only; Stage C sole portal E2E completion | PASS | Stage matrices, STOP gates, empty resolution table and stage-specific success criteria |
| Issue #6 immutable oracle including exact source/model/test/grain/fixture/hash and six-view semantics | PASS after fix | `small`/42, 18/6,812, 18/51/141, 179/7/0/186, exact 11, fixture hashes, exact six view IDs/manifest/render pairs |
| Determinism, orchestration, weighted metric, atomic 11 release, Iceberg, exact OpenMetadata and failure-pattern evidence | PASS | Stable behavior matrices, crash/recovery data flow and failure admission map |
| Genuine behavior-specific TDD | PASS after fix | Per-ID characterization→RED→GREEN→refactor/regression expected/actual sequence; fake/ignored/missing-tool RED rejected |
| #8/#9/#10 consumed read-only only after releases; no duplicate truth/browser privilege/invented adapter | PASS after fix | Dependency register and authority boundary now state the prohibition explicitly |
| Full S3 threat coverage | PASS after fix | Added FIFO/socket/device/other special-file rejection to link/TOCTOU/path controls |
| Final commands, serialized 16GB profile, honest optional services, fail-closed dependency gates, N-1 and run-owned cleanup | PASS | Final contract and resource/migration/recovery/evidence requirements |
| Ownership/leases and protected root/shared/contracts/views/portal/runner/golden scope; no AWS/Terraform resources | PASS | Exact future templates, protected object manifest and no-cloud scope ID |
| Fresh implementation/security review plus human exact-head approval | PASS after fix | `DL-REV-001` and `DL-HUM-001`; any head drift invalidates both gates |

## Issue #6 oracle verification

The protected manifest was recomputed against
`24be3b34c6b0fcdbd07c5800dcab349054e34713`:

- all 12 listed Git objects match, including `architecture/` =
  `cd020fce1d525dd6fe414d5db28748911b7cf300`, `transform/dbt/` =
  `28932692fc20e079eecbe7ab1c9f93b2a94a8bbf`, `serving/rill/` =
  `27bda8a14222cae083d480275453659adb85b3ff` and ordered curated assets =
  `fc4b04aca3d4941d06658f27c58d078299301200`;
- all seven critical SHA-256 values match, including retail golden
  `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` and fixture
  `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5`;
- `small`/42 is 18 files and 6,812 rows; dbt is 18 sources, 51 models, 141 generic tests and
  179 pass/7 warn/0 fail/186 total; the graph hash is
  `9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df`;
- the mart/curated set is the exact ordered 11 and the normative summary hash is
  `4b8a16acd83064c374061a0f1eb4737e6b9fd6fe2fcaae3ec45a659dc684c84b`;
- the exact six architecture IDs are `C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`,
  `DEP-LOCAL`, `DYN-JOURNEY`; all six retain audience/concern/scope semantics plus SVG/text hashes.

Repository source confirms the current publisher is a sequential `DROP TABLE`/`CREATE TABLE`
loop with count-only read-back, not an atomic release. Current OpenMetadata verification only
checks non-zero service populations and lineage-count context, not exact reconciliation. The plan
correctly retains both as gaps.

## Findings and fixes

| ID | Severity | Objective defect | Bounded plan-only correction | State |
|---|---|---|---|---|
| VAL-01 | High | `24be3b…` was ambiguously called the current repository input although validation starts at `24ff21d…` | Separated planner/product input, validation input and golden authority in frontmatter/register/Phase 1 | Resolved |
| VAL-02 | Medium | Learning/FR trace existed, but no explicit business/not-a-docs-dump outcome | Added BUS-01..03 and learner-action/expected-actual criteria | Resolved |
| VAL-03 | High | Architecture tree was protected, but exact six-view semantics lacked a characterization/stable test trace | Added `DL-CHAR-ARCH`, `DL-ARCH-001`, six IDs and semantic/render oracle | Resolved |
| VAL-04 | High | S3 link/TOCTOU controls omitted FIFO/socket/device/special-file reads and writes | Extended threat, reset, NFR and negative-test contracts | Resolved |
| VAL-05 | High | TDD rules did not require retained per-behavior expected-vs-actual sequencing or explicitly reject ignored/missing-tool RED | Added exact per-ID sequence and invalid RED classifications | Resolved |
| VAL-06 | Medium | Read-only dependency consumption/no-duplicate-truth rule was distributed rather than explicit | Added one authority rule for #8/#9/#10, parallel registries, adapters and browser fallback | Resolved |
| VAL-07 | Medium | Fresh implementation review existed in Phase 5 but lacked end-to-end stable trace | Added NFR and `DL-REV-001`, bound to exact 40-hex reviewed head | Resolved |

No Critical finding and no unresolved High finding remain. No fix adds a dependency SHA, path,
command, schema, runner, renderer or implementation authority.

## Strict checks

| Check | Result |
|---|---|
| `ck plan validate plans/260721-012-data-platform-labs/plan.md --strict` | PASS; five phases, zero errors/warnings |
| Plan status | Pending, 0/5; correct branch and risk/TDD/S3/data-platform/recovery tags |
| Relative link resolution | PASS; 46 links, repo-contained |
| Authority emptiness | PASS; three dependency SHAs, three stage rows, current paths and current commands empty |
| Placeholder/stale-authority scan | PASS; no placeholder tokens; future templates explicitly non-authoritative |
| Exact #6 facts and protected hashes | PASS; 12 Git objects and seven SHA-256 values |
| Current-path check | PASS; no `learning/labs/data-platform`, `mk/issue-5/i5-07.mk`, `portal` or `runner` implementation |
| Planner changed-path scope | PASS; exact 12 Markdown artifacts under the Issue #12 plan directory |
| Golden mutation check | PASS; no product, SQL, view, fixture, reader, runner or renderer change |
| Sensitive/private/cloud/destructive scan | PASS; no credential/private locator/PII or executable AWS/Terraform action |

## Whole-plan consistency sweep

- Files reread: `plan.md`, all five `phase-*.md` files and all six companion plan artifacts.
- Decision deltas checked: 7.
- Reconciled stale/implicit references: 19.
- Unresolved contradictions: 0.
- Stage A remains contract/static candidate only; Stage B alone may use the released runner and
  exact lease; Stage C alone may claim a complete learner journey.
- The final four commands remain the user/Issue #6 future contract, not current runnable authority.
- All exact current dependency/path/command/schema/runner/renderer resolution fields remain empty.

## Remaining dependency blockers

1. Stage A: exact released Issue #8 learning/completion/evidence contracts and handoff SHA.
2. Stage B: exact released Issue #9 private runner plus exact serialized data-contract/pipeline
   lease with owner, paths, input SHA and non-overlap window.
3. Stage C: passing merged Issue #10 real journey/renderer/API handoff.
4. Every stage still requires a new exact-SHA amendment, independent revalidation and fresh
   dependency-aware readiness audit before cook.

## Decision

The corrected plan passes independent initial validation and may move to `ready for plan audit`.
This is **not** readiness acceptance. A fresh dependency-aware readiness audit is the next phase
and must remain blocked until the applicable exact dependency release and lease exist.
