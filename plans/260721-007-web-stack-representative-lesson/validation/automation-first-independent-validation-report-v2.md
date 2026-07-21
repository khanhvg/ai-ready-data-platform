---
type: plan-validation
date: 2026-07-21
issue: 7
acceptanceRevision: i5-02-acceptance-v2
verdict: PASS_WITH_FIXES
inputSha: ae9e2296b971c9134638e66c09302b516f8ad6e6
validatedPlanOutputSha: PENDING_FIRST_VALIDATED_PLAN_COMMIT
publicationOutputSha: recorded-externally-because-a-commit-cannot-self-identify
session: DE5D40FD-9DBB-4B97-85FA-C187E2B41313
---

# Issue #7 Automation-First Independent Plan Validation v2

## Summary

`i5-02-acceptance-v2` passes independent plan validation after ten objective planning defects were
fixed in the current amendment/index/matrix. The corrected plan is testable, fail-closed, additive,
and consistent with the owner decision. It preserves Issue #6 authority, frozen candidate/lock/v1
evidence identities, the exact cumulative timer remainder, S3/TDD, two automated exact-head reviews,
exact-head CI and human approval, pristine post-merge verification, rollback, and the production-
release UAT residual risk.

This is `INDEPENDENT_VALIDATION_PASS_NOT_READINESS`. It does not authorize cook, implementation,
browser/evidence execution, scoring, an ADR decision, PR creation, merge, or release.

## Session and Immutable Inputs

| Field | Exact value/result |
|---|---|
| Repository | `khanhvg/ai-ready-data-platform` |
| Work context | `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-5-02-web-spike` |
| Branch | `feature/issue-5-02-web-spike` |
| Validation input | `ae9e2296b971c9134638e66c09302b516f8ad6e6` |
| Local/tracking/fresh-live at start | all exactly validation input; clean; `+0/-0` |
| Owner decision | `https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5035256304` |
| Planner handoff | `https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5035613841`; `PLANNER_ONLY_NOT_VALIDATED` |
| Plan source base | `abbcb049b33ee0c6190caedfb5f3ca7fc57b8f59`; verified ancestor |
| Issue #6 integration base | `24be3b34c6b0fcdbd07c5800dcab349054e34713`; verified ancestor |
| Tested output/tree | `bef2d20f9b1d8029900b88aaea2f9991b0547590` / `d990cd5f7e4fff2af74d1cd0d8a2967d8f7aa23b`; verified commit/tree/ancestor |
| Candidate source lineage/tree | `02051ed94d4e2c920f8a65a4ecab0e08a82b946a` / `f2ec341820db157e6bc7fb12e75844ee2730ec12`; verified ancestor/current tree |
| V1 anchor SHA-256 | `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75`; verified |
| Astro/Next/Vite lock SHA-256 | `78677d1a272fdc5c9758810343f89e82f2914625a03259a575208fe1fafef760` / `4939388a7e7290ec640e418afac94dc68cfba7bf6b5692df61317b4c95de2e8b` / `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c`; verified |
| Timer provenance | used `3255.163904292`; remaining `3944.836095708`; arithmetic verified exactly; no reset |
| Issue preflight | OPEN; exact labels `ready for plan validation`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `decision-gate`, `preview-runnable` |
| GitHub/auth | authenticated as `khanhvg`; read/write repo scope available |
| Ignore probe | `plans/**/*` and candidate `package-lock.json` are ignored but the existing amendment/plan/matrix/locks are tracked; only exact changed Issue #7 plan paths may be force-added |
| Runtime | Codex agent workspace; requested model `gpt-5.6-sol`; reasoning effort `xhigh` |
| New session/log | session `DE5D40FD-9DBB-4B97-85FA-C187E2B41313`; this report is the validation log |
| Validation start | `2026-07-21T15:03:39Z` (`1784646219`) |
| Validation end/runtime | `2026-07-21T15:29:12Z` (`1784647752`); `1533` wall-clock seconds |

## Method

- Invoked the exposed `ck:plan validate` surface in strict JSON mode on the linked `plan.md`;
  result: valid, eight phases, zero structural issues.
- Performed the full workflow-equivalent independent semantic validation required by `ck:plan
  validate`: Full tier, all eight phases, Fact Checker, Flow Tracer, Scope Auditor, Contract
  Verifier, requirements/scenario trace, and whole-plan consistency sweep.
- Questions asked: `0`. The exact owner decision and this validation contract already resolve the
  decision points; no planner assumption was reused or reopened.
- Claims checked: `136` (`15 × 8` phase claims plus `16` cross-cutting authority/contract claims).
  Final result after fixes: `136 VERIFIED`, `0 FAILED`, `0 UNVERIFIED`.
- Inspected manifests, locks, neighboring imports, existing v1 harness import resolution, and the
  exact Playwright 1.61.1 type surface. Did not install a dependency or browser.
- Ran planning/static verification only. No candidate build, unit/E2E/browser/evidence test, score,
  ADR mutation, OS/CuaDriver action, PR, merge, or Issue #8+ action was performed.

## Findings and Disposition

| ID | Severity | Input defect | Disposition |
|---|---|---|---|
| `V2-VAL-01` | High | The current acceptance matrix superseded `manual no-JS review` in addition to the owner's exact three native checks. | Fixed: supersession is exactly VoiceOver/Caption, actual System Settings Reduce Motion, and native Chrome-menu 200%; automated no-JS remains binding. |
| `V2-VAL-02` | High | The current main-plan phase table still named `fresh browser + manual accessibility` as Gate C runtime. | Fixed: row is explicitly historical v1; current Gate C is equal automation v2 and native checks are non-scoring release UAT only. |
| `V2-VAL-03` | High | Keyboard steps lacked a stable action-ID registry and complete per-action ARIA/screenshot binding; modal behavior was ambiguous. | Fixed: 13 unique action IDs, role/name/fragment/state mapping, observed active-element movement, before/after ARIA+screenshot records, parity, reverse traversal, zero-expected-modal and no-trap rules. |
| `V2-VAL-04` | High | `200%-equivalent` was Chromium-only 640×400 with device scale 1 and no font/raster equivalence; clipping/offscreen checks were incomplete. | Fixed: both engines, 640×400/device-scale-2 against 1280×800 baseline, separate 320px mode, font/raster/overflow/overlap/clipping/offscreen/occlusion/focus geometry, and explicit no-native-zoom wording. |
| `V2-VAL-05` | Important | No-JS did not explicitly reject script-interception/removal shortcuts or require interaction-degradation messaging. | Fixed: pre-navigation `javaScriptEnabled: false`, `response.body()` bytes, independent built-in-only parser, identical Vite/Next inventory, degradation message, and fail-closed parser/browser equality. |
| `V2-VAL-06` | High | Future Playwright files used no actionable module-resolution contract even though the harness intentionally has no package manifest. | Fixed: additive `playwright-deps.mjs` bridge to the frozen Vite install, equal lock checks, exact CLI path, allowed 1.61.1 APIs, and no `npx`/ambient import/new dependency/browser install. |
| `V2-VAL-07` | Important | Gate C schema and profile/cache isolation were described at a summary level, leaving missing-evidence and cross-candidate contamination behavior underspecified. | Fixed: closed required groups, artifact identities, exact cardinality, deterministic `ELIMINATED` versus `INCOMPLETE_AUTOMATED`, and non-persistent context/cache/profile isolation. |
| `V2-VAL-08` | High | Timer/RED order could record a boundary after the first test write, and a top-level missing import could abort before all planned RED assertions ran. | Fixed: timer receipt is the first timed write; nanosecond start/stop/failure/timeout/crash accounting is append-only; every RED case registers before in-test planned imports/reads. |
| `V2-VAL-09` | Important | The file table labelled immutable `test-ids.json` as a modification and the matrix named stale `journey.spec.ts` instead of the planned `.mjs`. | Fixed: v1 IDs are read-only and v2 IDs additive; exact executable path is `journey.spec.mjs`. |
| `V2-VAL-10` | Important | CI was not explicit, while the live repository currently exposes no Actions workflow or protected-branch status context. | Fixed in plan: exact-head CI remains mandatory for merge; current absence is an explicit external merge dependency, never a pass; Issue #7 gains no `.github/**` scope and local cook/PR creation remain separable from merge. |

No Critical finding remained. All High/Important/objective defects were corrected only in the
current amendment, index, matrix, and this validation report. Candidate source/locks, v1 anchors,
prior evidence/attestations, scorecards/ADR, Issue #6 handoff, audit history, and product files were
not edited.

## Adversarial Contract Results

| Check | Result |
|---|---|
| Exact supersession only | PASS: exactly three native techniques move to deferred owner UAT; legacy native commands are non-executable/non-scoring; all other gates remain binding. |
| Keyboard/focus/parity/no trap | PASS after fix: stable action IDs, real keyboard focus transitions, Enter/Space/click parity, reverse traversal, Escape semantics, zero expected dialogs, per-action ARIA/screenshots, equal Vite/Next and Chrome/Firefox. |
| Axe + semantic/ARIA | PASS: exact landmarks/headings/controls/status/error/live/four-grain/conclusion/reset/reflection inventory; `locator.ariaSnapshot()` is authoritative and DOM-only inference is rejected. |
| 200%-equivalent + narrow | PASS after fix: technically bounded viewport/raster method, separate narrow mode, both candidates/engines, full geometry/focus checks, no native-zoom claim. |
| Reduced motion | PASS: browser emulation, equal fact/control/journey outcomes, computed animation/transition/scroll removal, no System Settings claim. |
| No-JS | PASS after fix: real disabled project, saved original response, independent static parser, full fact/limitation/grain/conclusion/reset/reflection/linear-path/degradation inventory for both built artifacts, no new dependency. |
| Candidate equality | PASS after fix: exact fixture/source/lock/tool/browser/environment identities; paired AB/BA order; 1 warmup; 4 cold + 4 warm samples; zero retries; cache/profile isolation; resource/security/retention/rollback parity; deterministic missing evidence. |
| Score anchor v2 | PASS: additive and frozen pre-observation, weights `20/20/20/15/10/10/5=100`, consecutive 0..5 normalization, >5 winner rule, ≤5 no-winner, Astro null/eliminated, incomplete/null, UAT never numeric. |
| Timer | PASS after fix: exact remaining value retained; legal pre-timer boundary; first-write receipt; monotonic/UTC command/failure/timeout/crash accounting; no retrospective pause/refund/fabrication. |
| ADR/Gate D | PASS: ADR-005 remains Proposed; complete revised evidence and two exact-head reviews required; legal residual-risk/UAT wording; no full-conformance claim. |
| Manual UAT | PASS: exact three-item checklist and human exact-build sign-off; non-blocking for local decision/downstream/PR, blocking only production release. |
| Review/CI/merge | PASS after fix: two automated exact-head reviews, S3/TDD, exact-head CI, genuine repository-authorized human exact-head approval, pristine post-merge rerun, rollback; no standing/agent synthesis. |
| Legacy consistency | PASS: immutable v1 clauses remain searchable history but are governed by the explicit current-v2 ledger; no current index/matrix clause can re-block or score native checks. |
| Tool/API feasibility | PASS with risk: exact locks supply Playwright/axe; allowed Playwright APIs verified; no harness package needed; missing browser/tool fails closed and grants no install/dependency authority. |
| 16GB/local scope | PASS: one candidate/one context/one worker, 4096 MiB combined cap, serialized heavy work, loopback only; no Docker/AWS/cloud/Terraform/new framework. |

## Traceability

| Business outcome/capability/concern | FR/NFR | Architecture/implementation | Automated evidence | Operations/rollback |
|---|---|---|---|---|
| Honest Vite/Next decision or no-winner; fair 16GB comparison | `FR-08`, `FR-10`, `NFR-01`, `NFR-03` | exact tool bridge, serialized orchestrator, balanced samples, immutable anchors | environment/fixture/source/lock/browser hashes, raw samples, comparability and score digests | cap or inequality stops with null scores; owned-runtime rollback |
| Novice-accessible complete lesson without fragile native automation | `FR-02..07`, `FR-12`, `NFR-02` | journey, keyboard, semantic, reflow, motion, no-JS specs/parser | action/checkpoint ARIA/screenshots, axe, geometry, computed motion, dual comprehension inventories | candidate eliminates on deterministic failure; native items remain release UAT only |
| Reproducible and non-laundered decision | `FR-01`, `FR-09..11`, `NFR-04..07` | authority/status/schema, S3, parent retention, timer, decision/rollback scripts | RED/GREEN TAP, exact SHAs/digests, raw/index/retention/timer records | no missing-evidence score; ADR stays Proposed; normal reviewed revert only |
| Preserve Issue #6 authority | `FR-01`, `FR-08`, `NFR-05` | read-only Barrier B and identical candidate projection | exact integration ancestry, four blobs/SHA-256 values, schema/grain/conclusion | any drift invalidates both candidates and every v2 score input; Issue #6 files unchanged |
| Human/release governance | `FR-10`, `FR-11`, `NFR-02` | two exact-head reviews, exact-head CI, human approval, separate UAT schema | reports/status contexts/human exact-SHA approval/UAT hashes | CI+human block merge; UAT blocks production release; no auto-synthesized approval/conformance |

The chain `owner decision → BO/CAP/CON → FR/NFR → v2 architecture/files → TDD implementation
tasks → automated evidence/schema → score/Proposed ADR → review/CI/human merge → rollback/UAT`
is complete and testable. Issue #6 remains the immutable data authority rather than an Issue #7
copy or patch surface.

## Planning and Static Verification

| Command/check | Result |
|---|---|
| `git fetch`, local/tracking/`git ls-remote` equality, status | exact input on all refs; clean at start |
| `gh auth status`; Issue/comment API queries | authenticated; issue OPEN; owner/planner comments exact; required label set exact |
| `ck plan validate .../plan.md --strict --json` | valid; 8 phases; 0 issues |
| Markdown link/path scan | 32 Markdown files; 157 links; 86 local links/anchors; 0 missing |
| Commit/tree/ancestor/hash checks | planner base, Issue #6 base, tested output/tree, candidate source/tree, v1 anchor, locks all exact |
| Ignore/tracked probe | plan files and candidate locks match ignored-but-tracked expectations |
| Manifest/lock/import/API checks | Vite/Next locks contain exact Playwright/axe; current v1 harness proves explicit Vite-relative resolution pattern; Playwright 1.61.1 types expose every planned API |
| Project/action/weight static checks | 10 unique projects; 13 unique action IDs; weights sum exactly 100 |
| Timer arithmetic | `7200.000000000 - 3255.163904292 = 3944.836095708` |
| Immutable-path diff | candidate/common/preview/locks/v1 evidence/score/ADR/Issue #6 paths unchanged from planner base |
| `git diff --check` and changed-path allow-list | PASS; only current Issue #7 plan/validation artifacts |

## Whole-Plan Consistency Sweep

- Files reread: `plan.md`, `automation-first-acceptance-amendment-v2.md`,
  `acceptance-and-test-matrix.md`, and all eight `phase-*.md` files.
- Companion/history check: candidate protocol, preview journey, implementation handoff, S3
  disposition, Issue #6 handoff, and recovery-term locations were searched without editing them.
- Decision deltas checked: `10`.
- Reconciled current stale/contradictory references: `10` findings plus exact current status links.
- Legacy v1 references retained as explicitly non-executable history: yes; all covered by the exact
  v2 ledger and excluded from must-pass/score.
- Unresolved contradictions: `0`.

## Feasibility and Preserved Risks

- The remaining implementation budget is only `3944.836095708` seconds for RED through Gate D.
  The plan is feasible as a bounded fail-closed experiment, not as a guaranteed winner: expiry
  retains evidence and produces no-winner/null scores without resetting or fabricating time.
- Static source inspection—not a product test—shows both frozen surviving candidates currently use
  `html[lang="en"]`; Vite exposes only four act links in its authored static nav. The stronger v2
  contract may therefore eliminate one or both candidates. Frozen-source failure is an expected
  legal outcome, not authority to patch source or weaken tests.
- Deep VoiceOver/Caption, actual System Settings Reduce Motion, and native Chrome-menu 200% remain
  pending production-release UAT and residual accessibility risk. Automated passage cannot claim
  full WCAG or screen-reader conformance.
- No repository CI workflow/status context exists at validation time. It does not block local cook
  or PR creation, but exact-head CI remains mandatory before merge and requires repository-owner
  provision outside this Issue #7 plan scope.
- Browser/tool presence was checked only statically. Readiness and timed execution must fail closed
  if the exact frozen browser/tool executables are unavailable; no install/substitution is implied.

## Recommendation

Proceed only to a fresh independent readiness audit at the exact published validation head. The
audit must name the sole implementation input, single-writer lease, timer start, additive v2 paths,
exact tool/browser preflight, and the external CI merge dependency. Do not claim cook readiness from
this report.

## Unresolved Questions

None for plan validation. Execution may legally finish with no winner; CI provision and later UAT
are explicit downstream dependencies, not silent assumptions.
