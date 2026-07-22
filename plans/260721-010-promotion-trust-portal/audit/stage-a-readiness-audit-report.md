---
title: "Issue #10 Stage A exact-release readiness audit"
auditDate: "2026-07-22"
startHead: "4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7"
integrationReleaseSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
verdict: STAGE_A_READY
stageB: blocked-on-issue9
cloudAction: none
---

# Issue #10 Stage A Exact-Release Readiness Audit

## Verdict

`STAGE_A_READY` for one bounded runner-independent cook from pristine integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. The authority is exactly the 34 new tracked files,
18 admitted command surfaces, released #7/#8 dependency bytes, protected identities, and gates in
the [Stage A release amendment](../stage-a-release-amendment.md). Stage B is
`blocked-on-issue9`; its file, command, and dependency SHA lists are empty.

This is planning/cook readiness only. It does not claim that the portal was implemented, built,
executed, reset, verified, evidenced, completed, reviewed, approved, or merged.

## Audit Scope and Independence

- Worktree: `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-10-portal`
- Required branch: `plan/issue-10-promotion-portal`
- Exact clean starting head: `4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7`
- Auditor runtime: Herdr agent `audit-issue10-stage-a-readiness`, terminal
  `term_6572e6691c2beb3`, pane `w2:p5A`
- Herdr process argv independently reported Codex model `gpt-5.6-sol` with
  `model_reasoning_effort="xhigh"` and danger-full-access sandbox in the required worktree.
- `$ck:plan-to-cook` was not exposed. The workflow-equivalent used CK plan strict validation,
  exact-release amendment, dependency-aware readiness, whole-plan reconciliation, Git safety,
  and GitHub handoff gates.
- No dependency feature worktree or ignored/generated artifact was used as release evidence.
- No portal implementation, product/config/data edit, credential access, merge, AWS, Terraform,
  cloud, or destructive action occurred.

The older independent validation and blocked readiness reports remain immutable historical
snapshots. This audit supersedes only their stale #7/#8 dependency-state conclusion.

## Remote Release Proof

| Authority | Exact result | Audit disposition |
|---|---|---|
| Issue #7 approval | Feature head `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9`, tree `8ebd0f9a8ead8a6f3c382088cf172f28742a9c0b`, owner approval comment `5041125607` | PASS |
| Issue #7 PR #22 | Merge `1806b6d515f2f7a2ace2be7077af84a745ff221f`; ordered parent 2 is approved head; trees equal | PASS |
| Issue #8 Stage A PR #23 | Merge `5c2244c2c860234d0df49cf0a42ad950c6495717`; parent 1 contains #7 merge | PASS |
| Composition PR #25 | Merge `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; parent 2 `734cf637a20ae186597e23d96a194ed4e30220ea`; composed tree equality | PASS |
| Current integration | `refs/heads/integration/issue-5-local-learning` at `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | PASS |
| Released tree | Tree `27fc3667ef37892dad5c3fbfd76769f65a0760be`; 903 entries; listing SHA-256 `4b95afd87ee7702f74df4a4b09198e13b8fa7ba45434c8a6a511a3ff1c580018` | PASS |
| Issue #8 evidence | Comment `5043195549`: release checks 56/56, invalid 65/65, API 16, final 4/4, inherited 19/19, 1/1, 13/13; no CI-success claim | PASS |
| Issue #9 | OPEN and unreleased | Stage B BLOCKED |

The 73-file release catalogue recomputes every admitted file from the fetched integration Git object and
records Git blob, bytes, and SHA-256. Issue #7 toolchain values and Issue #8 validators, registry,
lesson/lab/manifest, OpenAPI, progress/completion/evidence contracts were read from those objects.

## Dependency and Protected-Identity Binding

- Exact #7 package graph: Node `22.22.3`, npm `10.9.8`, lock v3, Vite `8.1.5`, React/React DOM
  `19.2.7`, Playwright `1.61.1`, axe Playwright `4.12.1`, React plugin `6.0.1`.
- Exact #8 direct validator/command and contract catalogue: 49 files plus its two exact runtime
  admission inputs; exact lesson
  reads `listLessons` and `getLesson` bound for compatibility but neither called nor exposed.
- Seven protected Issue #6/release paths match their exact blob, byte, and SHA-256 identities.
- Root Make's sorted `mk/issue-5/*.mk` include seam exists; all nine I5-05 command registry rows
  remain `future-owner/not-runnable` with owner `mk/issue-5/i5-05.mk` at the release input.
- The 34-file cook scope includes an app-owned released-schema activation instance that binds the
  final fragment hash and all nine recipes to truthful `fitness-result-v2` output without a shared
  registry edit.
- All 34 Stage A tracked paths are absent at the released input, so authority is create-only.
- No `apps/learning-portal`, `mk/issue-5/i5-05.mk`, or runner app exists in the released tree.

`DEPENDENCY_BINDING=pass`.

## Stage A Product and Trust Closure

The amended plan preserves the product direction: a Vietnamese-first foundation-to-mid learning
portal shell, with promotion-trust as the first vertical slice rather than the whole curriculum.
Its provider/catalog/router/static-render seams accept later released #11/#12 manifests only
through exact registered contracts and hashes, without inventing their content or redesigning the
shell.

Stage A is one Vite-built React/static document app and one GET/HEAD-only loopback static server.
It has no BFF/API, runner import/probe/start/call, host-command surface, database, session, cookie,
browser storage, service worker, cloud action, or completion authority. Static/no-JavaScript and
React rendering share one escaped safe view model. Released #8 validators remain the contract
truth; Issue #7 spike files remain toolchain evidence rather than copied architecture.

The PTP-S3-01..14 catalogue is unique and complete. Stage B-only threats are proved by capability
absence in Stage A rather than skipped. Exact CSP uses `connect-src 'none'` and
`form-action 'none'`; output/process/request/artifact bounds and marker/PID/path cleanup are
fail-closed. `S3=pass` for planning readiness.

## TDD and Verification Closure

The plan defines:

- 11 Stage A requirements (`SA-R01..11`) and 10 scenarios (`SA-SC01..10`);
- 14 explicit Stage A RED IDs plus the 14-row S3 RED range;
- real RED paths through release adapter, provider/catalog, router, static/React render, server,
  lifecycle, and Chromium—not missing-tool or retrospective failures;
- exact frozen install, released validator, unit/contract/security, production build, audit,
  public lifecycle/test, and required Stage B-negative commands;
- one Chromium journey at 1280x800 and 360x800, one worker/no retries, axe zero
  Critical/Serious, JavaScript-disabled navigation, history/reload, storage/network inspection,
  and runner-unavailable/non-completion checks;
- exact output/artifact ceilings, fixture identity, cleanup twice, rollback, two independent
  exact-head reviews, bounded human UAT, and human exact-head pre-merge approval.

The plan explicitly excludes superseded Next/Astro/framework comparison, Firefox/WebKit/native OS
automation, performance contests, timers, and automated full-conformance claims.

## Findings and Amendments

| Finding | Severity | Amendment | Result |
|---|---|---|---|
| Prior normative files still treated #7/#8 as unreleased | High | Replaced with exact PR #22/#23/#25 and integration authorities | Closed |
| Stage A inherited a BFF/API architecture despite runner independence | High | Reframed Stage A as static GET/HEAD documents only; BFF deferred to blocked Stage B | Closed |
| Stage A implementation authority was empty | High | Added exact 34-file, 18-command, dependency-byte, toolchain, activation, and protected-identity closure | Closed |
| Initial lesson could be mistaken for full course | Medium | Added generic catalog/module/lesson/step seams and explicit vertical-slice copy | Closed |
| TDD/browser/security bounds were partly deferred or historical | Medium | Added real RED paths, exact viewports, no-JS/unavailable/S3/output/cleanup/review gates | Closed |

No unresolved Critical, High, or Stage A-blocking Medium finding remains. Issue #9 remains a
deliberate Stage B blocker.

## Validation Record

| Check | Result |
|---|---|
| `ck plan validate ... --strict --json` | PASS: valid, zero issues, seven phases resolved |
| CK parse/status | PASS: seven pending phase files; Stage B marked blocked in the normative plan |
| Local Markdown links and anchors | PASS |
| Placeholder/future-SHA scan | PASS: no unresolved placeholder or invented future identity in current normative artifacts |
| Released path/blob/byte/SHA-256 recomputation | PASS |
| Protected hashes and released-tree identity | PASS |
| 34-path ownership/create-only closure | PASS |
| 18-command allowlist and nine-command owner closure | PASS |
| SA requirement/scenario, RED, and PTP-S3 catalog uniqueness | PASS |
| Stage B file/command/dependency lists empty and Issue #9 block consistent | PASS |
| `git diff --check` and plan-directory-only diff | PASS |
| Whole-plan stale-state/architecture/claim sweep | PASS |
| High-confidence secret/private-key/credential scan | PASS |

## Handoff Decision

On publication of this exact plan-only amendment commit, Issue #10 may remove
`ready for plan audit` and add `ready to cook`. Cook scope is Stage A only: create exactly the 34
listed files from pristine integration `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; implement the
static Vietnamese-first portal slice and exact tests/gates; perform no Stage B, release merge, or
cloud action.

Any change to release identity, path/command list, protected hash, contract/version, product claim,
or Issue #9 state requires a fresh audit. Stage B cannot inherit this PASS.
