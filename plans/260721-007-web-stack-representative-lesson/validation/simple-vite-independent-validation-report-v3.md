---
type: plan-validation
date: 2026-07-21
issue: 7
acceptanceRevision: i5-02-simple-vite-v3
verdict: PASS_WITH_FIXES
inputSha: d79ce5638e4a47c5c0963bba1a546448bc0c0ea6
publicationOutputSha: recorded-externally-because-a-commit-cannot-self-identify
nextPhase: fresh-simple-readiness-audit
---

# Issue #7 Simple Vite Independent Plan Validation v3

## Summary

`i5-02-simple-vite-v3` passes fresh independent plan validation after nine objective plan defects
were fixed. The result selects Vite + React directly, has four implementation phases and exactly
seven blocking test groups, and is executable from the frozen repository contracts without a new
comparison, score, timer, browser matrix, native/manual gate, or portal scope.

This is `INDEPENDENT_VALIDATION_PASS_NOT_READINESS`. It authorizes no install, build, browser run,
implementation, evidence run, ADR transition, PR, merge, OS action, cloud action, or Issue #8+
write. The only next phase is a fresh simple readiness audit of the exact published validation
head.

## Immutable Inputs

| Field | Verified value/result |
|---|---|
| Repository/branch | `khanhvg/ai-ready-data-platform`; `feature/issue-5-02-web-spike` |
| Validation input | `d79ce5638e4a47c5c0963bba1a546448bc0c0ea6`; local = tracking = fresh-live and clean at start |
| Issue state | Issue #7 OPEN; workflow label `ready for plan validation`; `risk:high`, `tdd`, `security:S3` retained |
| Owner decision | `https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177`; Vite + React, seven minimal groups, old comparison path retired |
| Planner publication | `https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036342155`; `PLANNER_ONLY_NOT_VALIDATED`; output equals validation input |
| Issue #6 authority | `24be3b34c6b0fcdbd07c5800dcab349054e34713`; verified ancestor |
| Fixture identity | All four planned SHA-256 and Git-blob pairs match tracked files exactly |
| Vite lock | SHA-256 `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c`; exact Playwright/axe packages verified |
| Historical timer | `3944.836095708`; preserved and explicitly closed/non-binding for v3 |

## Method

- Invoked the exposed `ck plan validate` surface on the exact v3 amendment with `--strict --json`:
  valid, four phases, zero issues.
- Applied the `ck:plan validate` workflow-equivalent Standard tier: Fact Checker and Contract
  Verifier, ten claims per phase. Final result: `40 VERIFIED`, `0 FAILED`, `0 UNVERIFIED`, plus
  twelve cross-cutting authority, stale-clause, and release-boundary checks.
- Questions asked: `0`. The owner comment and the validator's exact acceptance contract resolve all
  material decisions; no comparison or architecture choice was reopened.
- Inspected tracked manifests, locks, existing Vite imports, the static host interface, current
  Make seam, ADR/scorecard state, Issue #6 identities, and planned path parents. No dependency or
  browser was installed or executed.
- Ran only strict plan, Markdown link/anchor/path, stale-clause, unresolved-placeholder, hash,
  changed-path, secret/private-path diff, and whitespace checks.

## Findings and Fixes

| ID | Severity | Input defect | Fix |
|---|---|---|---|
| `V3-VAL-01` | High | The journey named states but had no stable selector registry or exact per-checkpoint assertions. | Added exact entry, failure, four-grain, conclusion/reason, reset, and reflection selectors, text, state, focus, and storage assertions in journey order. |
| `V3-VAL-02` | High | Desktop, narrow, and no-JS were described as three projects, leaving room for matrix growth. | Closed the config to exactly two Chrome-channel Chromium projects; both run one tagged journey, and desktop alone owns axe and a child no-JS context. |
| `V3-VAL-03` | High | The axe threshold lacked an exact import/API contract and could drift into tagged/full-WCAG language. | Bound the frozen default `AxeBuilder` import and one `analyze()` call; retain all findings, block only Critical/Serious, and forbid rule/tag/exclusion relabelling. |
| `V3-VAL-04` | Important | Static fallback named a fact inventory but not the real parser/API used to obtain it. | Bound `response.body()` plus the existing Playwright/browser DOM and locator API in a pre-navigation `javaScriptEnabled: false` context; no invented/transitive parser dependency. |
| `V3-VAL-05` | High | The current matrix displayed seven product rows plus a separately numbered eighth blocking governance gate. | Removed the eighth row and retained governance as explicitly non-test release conditions. All and only `V3-01..07` are blocking test groups. |
| `V3-VAL-06` | High | Two read-only dependencies could become writable when RED plus reviewer opinion expanded scope. | Closed the writable table; lock, fixture adapter, and existing static host are read-only. Any required change stops for plan amendment and revalidation. |
| `V3-VAL-07` | High | Phase 1 could begin from validator authority without the requested fresh simple readiness audit. | Bound implementation input only to the future audit-authorized full SHA; validation remains explicitly not readiness. |
| `V3-VAL-08` | Important | Shell commands contained unresolved angle-bracket values and did not make single-server ownership explicit. | Replaced them with validated runtime variables, exact `npm --prefix` commands, one existing host child, one smoke process, and `finally` cleanup ownership. |
| `V3-VAL-09` | Important | Historical matrix prose still said “current v2” and left active-looking Preview/ADR/Portal headings. | Marked the entire section `HISTORICAL_NON_BINDING_V1_V2`, changed the wording to historical past tense, and renamed the columns as historical. |

No Critical finding remained. Only the current Issue #7 plan/index/matrix and this validation report
were changed. Candidate source, locks, harness, tests, Makefile, ADR/scorecards, prior evidence,
Issue #6 files, OS state, and downstream worktrees were not mutated.

## Acceptance Validation

| Required property | Result |
|---|---|
| Direct Vite decision | PASS: Vite + React is owner-selected and unscored; Next/Astro are immutable history with no comparison, tie, score, performance, or timer gate. |
| Plan/test simplicity | PASS: four phases; exactly seven blocking groups; governance remains release conditions, not group eight. |
| Exact journey | PASS after fix: stable selectors and exact assertions cover entry → controlled failure → promotion, fulfillment, returns, data-quality grains → exact conclusion/reason → reset → reflection. |
| Chromium/viewports/focus/overflow | PASS after fix: exactly desktop and narrow Chrome-channel projects, one worker/zero retries, one tagged journey, deterministic focus style/geometry/hit-test and width/element bounds. |
| Axe | PASS after fix: frozen `@axe-core/playwright@4.12.1` default API, one scan, zero Critical/Serious threshold, complete result retained, no full-WCAG/screen-reader claim. |
| No-JS/static fallback | PASS after fix: real JS-disabled child context, original response bytes, browser DOM parser/locator inventory, four exact grains and limitations, conclusion/reason, reset limitation, reflection, linear order. |
| TDD/S3/evidence/governance | PASS: contemporaneous exact test-only RED, closed allow/deny paths, fixture hashes, zero High/Critical audit, scans, manifest/hash/retention indexes, owned cleanup, rollback, reviews, configured PR checks, human exact-head approval. |
| Minimal write boundary | PASS after fix: only named Vite candidate, focused tests/config, v3 harness/Make seam, v3 evidence, ADR surfaces, and plan status links; portal remains Issue #10. |
| ADR transition | PASS: Accepted/Vite occurs only after all seven groups, S3/RED, and two prerequisite independent reviews; production accessibility/UAT risk and claim limits are mandatory. |
| Historical non-reentry | PASS after fix: v1/v2/manual/native/multi-browser/timer/score terms are explicitly immutable, historical, and non-binding across amendment, index, matrix, and future scorecard instructions. |
| 16GB/no cloud | PASS: serialized one-candidate/server/worker/project execution; no concurrent heavy run, Docker, AWS, Terraform, or cloud action. |

## Executable Traceability

- Tracked `package.json`/lock pin React `19.2.7`, Vite `8.1.5`, Playwright `1.61.1`,
  `@axe-core/playwright` `4.12.1`, and axe-core `4.12.1`; no new dependency or lock change is
  planned.
- Existing `gate-c-run.mjs` proves the default `AxeBuilder` import pattern; the v3 plan uses the
  package-root default import available to the candidate package.
- Existing `candidate-static-host.mjs` accepts exact root/port arguments, restricts candidate ports
  to `4174..4178`, binds loopback exclusively, emits `READY`, serves CSP headers, and is read-only.
- Existing `mk/issue-5/i5-02.mk` is the real issue-local seam; the plan adds only named v3 targets
  and does not touch root `Makefile`.
- Every existing path named as an input was found. Every planned create path has an existing allowed
  parent. The four Issue #6 SHA/blob pairs, Vite lock, protected hashes, and protected Git tree IDs
  match the exact validation input.
- Runtime variables are closed: readiness publishes the 40-hex `IMPLEMENTATION_INPUT_SHA`; the
  runner emits schema-validated `$RUN_ID`. There are no unresolved placeholder markers in current
  v3 authority.

## Planning and Static Checks

| Check | Result |
|---|---|
| `ck plan validate .../simple-vite-acceptance-amendment-v3.md --strict --json` | PASS: valid; four phases; zero issues |
| Current Markdown links/anchors and local path targets | PASS: four files, 28 links, 25 local targets, zero missing files/anchors |
| Required terms/counts | PASS: phase count `4`; blocking rows `7`; selector and exact conclusion/reason coverage complete |
| Stale-clause sweep | PASS: no active Firefox/Next/Astro comparison, score/tie/performance/timer/native/manual/portal gate; historical hits are behind explicit non-binding markers |
| Placeholder sweep | PASS: zero unresolved placeholders; only defined `$IMPLEMENTATION_INPUT_SHA`, `$RUN_ID`, and historical `$HISTORICAL_RUN_ID` variables remain |
| Hash/ancestry/package/API/path checks | PASS: all exact values and parents found; frozen axe package manifest exports its default ESM/CJS entry; no planned import or command depends on an unowned package surface |
| Changed-path allow-list | PASS: exactly four Issue #7 plan/index/matrix/report artifacts |
| `git diff --check` and credential/private-path diff scan | PASS |

## Whole-Plan Consistency Sweep

- Files reread: current `plan.md`, v3 amendment, acceptance matrix, all eight historical
  `phase-*.md` files, v2 amendment, current ADR/scorecards, and prior validation report.
- Decision deltas checked: `9`.
- Current stale/contradictory references reconciled: `9`.
- Historical v1/v2 terms retained as immutable/non-binding provenance: yes.
- Unresolved contradictions: `0`.

## Recommendation

Proceed only to `fresh-simple-readiness-audit` on the exact published validation head. That audit
may verify exact-head authority, ownership and static tool/path availability for v3; it may not
restore the retired comparison, scoring, timer, native/manual, multi-browser, performance, or
portal path. Do not infer implementation readiness from this report.

## Unresolved Questions

None.
