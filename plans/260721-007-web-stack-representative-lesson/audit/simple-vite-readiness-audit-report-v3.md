---
title: "Issue #7 Simple Vite Readiness Audit v3"
issue: 7
phase: fresh-simple-readiness-audit
status: ready-with-gates
auditInputSha: "aa93dfac5cd4a5f4d351ad045b634bbd42254902"
acceptanceRevision: "i5-02-simple-vite-v3"
validationReport: "../validation/simple-vite-independent-validation-report-v3.md"
ownerDecision: "https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177"
issue6IntegrationSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
auditOutputSha: "externally-attested-in-issue-7-publication-comment"
implementationInputSha: "same-as-audit-publication-output"
blockingTestGroups: 7
browserToolchain: ready
barrierB: open
nextPhase: serialized-simple-tdd-cook
auditedAt: "2026-07-21"
---

# Issue #7 Simple Vite Readiness Audit v3

## Verdict

`READY_WITH_GATES` for the owner-selected, unscored Vite + React path in
[`i5-02-simple-vite-v3`](../simple-vite-acceptance-amendment-v3.md). The plan is practically
cookable as four serialized TDD phases with exactly seven blocking test groups.

The containing audit commit cannot name its own SHA without creating a recursive identity. After
publication, the exact 40-hex output attested in the Issue #7 comment is the only valid
`IMPLEMENTATION_INPUT_SHA`. Readiness is not implementation: this audit did not install, build,
launch a browser, run candidate acceptance, implement product/tests/evidence, change ADR or
scorecards, create a PR, merge, mutate the OS, access cloud infrastructure, or touch Issue #8+.

## Exact Authority

| Check | Verified observation | Result |
|---|---|---|
| Repository/branch | `khanhvg/ai-ready-data-platform`; `feature/issue-5-02-web-spike` | Pass |
| Audit input | local HEAD, tracking ref, and fresh `ls-remote` all exactly `aa93dfac5cd4a5f4d351ad045b634bbd42254902` | Pass |
| Clean input | zero staged, unstaged, or untracked paths; ahead/behind `+0/-0` | Pass |
| Validation relation | `d79ce5638e4a47c5c0963bba1a546448bc0c0ea6` is the audit input's first parent and an ancestor | Pass |
| Issue #6 relation | `24be3b34c6b0fcdbd07c5800dcab349054e34713` is an ancestor | Pass |
| Live Issue #7 | OPEN with `ready for plan audit`, `risk:high`, `tdd`, `security:S3`, `frontend`, `accessibility`, `decision-gate`, and `preview-runnable` | Pass |
| Owner/validation comments | exact IDs `5036142177` and `5036544355`; owner chooses Vite and validator reports `PASS_WITH_FIXES` | Pass |
| Writer isolation | no Git lock; no issue assignee or implementation workflow label; process inspection shows one serialized audit runtime plus its monitor/tool helpers and no competing Issue #7 writer | Pass |
| Runtime identity | actual process arguments select Codex `gpt-5.6-sol` with `model_reasoning_effort="xhigh"` | Pass |

The live feature ref remained unchanged at the audit input through the read-only inspection. It is
rechecked immediately before staging and again before publication; any drift is a hard stop.

## Issue #6 Fixture and Barrier B

Issue #6 is CLOSED and labelled `shipped`. Its authoritative merge has parents
`b6482e0e435422b526fe06193c7276e834abef1b` and
`707ca6ef698f54afaa3ddd62e47caafd2d5f2ba8`. All four tracked identities match the live shipped
handoff and the v3 plan:

| Read-only path | SHA-256 | Git blob | Result |
|---|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` | Pass |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` | Pass |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` | Pass |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` | Pass |

Barrier B is open for this exact ancestry and these identities. Any later drift closes it. Issue #7
continues to consume all four paths read-only.

## Toolchain and Non-Drifting Install Route

| Surface | Verified route | Result |
|---|---|---|
| Node test | Node `v22.22.3`; built-in `node:test`; Vite 8 engine `^20.19.0 || >=22.12.0` satisfied | Ready |
| npm/Make | npm `10.9.8`; GNU Make `3.81`; `npm audit` command present | Ready |
| Vite/React | package lock v3; React/React DOM `19.2.7`, Vite `8.1.5`, plugin-react `6.0.1` | Ready |
| Browser test | Playwright/test/core `1.61.1`; cached executable CLI; installed stable Chrome channel at executable version `150.0.7871.129` | Ready |
| axe | `@axe-core/playwright` and `axe-core` `4.12.1`; cached package exports default `AxeBuilder`; `analyze()` exists | Ready |
| no-JS/static API | cached Playwright types expose `Browser.newContext`, `javaScriptEnabled`, `Response.body(): Promise<Buffer>`, locator/DOM parsing, project workers/retries/timeouts | Ready |
| Security/audit | npm registry ping passes; `npm audit --audit-level=high --json` has an exact route; Node built-ins plus tracked v3 harness own deterministic scans/hashes/process cleanup | Ready |
| Static host | tracked `candidate-static-host.mjs` binds loopback exclusively, restricts ports to `4174..4178`, emits `READY`, serves CSP, and accepts exact root/port arguments | Ready |

Candidate `node_modules` is absent, as expected at a clean input. Readiness did not install it.
Instead it proved the exact route:

- lock SHA-256 is `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c`;
- `npm ci --offline --ignore-scripts --no-audit --no-fund --dry-run` succeeds;
- all 33 packages compatible with `darwin/arm64` are cached and match their lock integrities;
- the 24 absent cache entries are foreign OS/CPU optional bindings and none is compatible with
  this host; and
- all critical React/Vite/Playwright/axe tarballs and the darwin-arm64 Rolldown/Lightning CSS
  bindings are present. The lock's exact integrity and resolved registry routes remain the
  non-drifting online fallback.

No Firefox, WebKit, Next, Astro, browser download, OS profile, or native driver is needed.

## Implementation and API Trace

The existing candidate can be fixed without comparison or scoring:

| Path/API | Current/future role | Audit disposition |
|---|---|---|
| `spikes/web/candidates/vite/index.html` | static entry/CSP/no-JS authored fallback | Existing; minimal allow-listed edit |
| `spikes/web/candidates/vite/vite.config.mjs` | React plugin plus escaped build-time projection from the four tracked files | Existing; imports resolve from frozen lock |
| `spikes/web/candidates/vite/src/fixture.mjs` | `node:crypto`, `node:fs`, `node:path`; reads exactly four Issue #6 paths | Existing and byte-read-only |
| `spikes/web/candidates/vite/src/main.jsx` | React local controlled failure/reset state | Existing; minimal allow-listed edit |
| `spikes/web/candidates/vite/src/styles.css` | focus and narrow layout | Existing; already has a strong focus baseline and single-column narrow rule |
| `spikes/web/candidates/vite/src/lesson-contract.mjs` | pure exact lesson/state values shared by UI and Node tests | Planned create under existing parent |
| `spikes/web/candidates/vite/package.json` | add only exact `test:unit` and `test:smoke` scripts | Planned metadata-only change; versions unchanged |
| `spikes/web/candidates/vite/playwright.config.mjs` | two Chrome-channel projects, one worker, zero retries, explicit test/expect ceilings | Planned create under existing parent |
| two focused Vite test files | Node contract suite and sole Playwright smoke/axe/no-JS suite | Planned creates under existing parent |
| `spikes/web/harness/simple-vite-v3.json` | closed authority, path, fixture, command, scan, evidence, and ceiling contract | Planned create |
| `spikes/web/harness/scripts/simple-vite-v3.mjs` | serialized Node child runner, hash/scan/retain/rollback, owned cleanup | Planned create using only Node built-ins and tracked inputs |
| `spikes/web/harness/tests/simple-vite-v3.test.mjs` | negative authority/evidence/S3/ownership/rollback tests | Planned create |
| `mk/issue-5/i5-02.mk` | add thin v3 RED/gate/rollback/pristine targets | Existing issue-local seam; root Makefile untouched |

The current source contains none of the v3 `data-testid` registry and has shorter status/reset
strings than the exact contract. The authored tests can therefore produce a valid, named RED
before GREEN without an import error or artificial assertion. The tests-only commit includes the
focused suites, config/scripts, and negative harness tests but no product, ADR, or retained GREEN
evidence. RED records exact test-only SHA, discovery inventory, named assertion failures, commands,
exit codes, and changed paths before the minimal source repair.

## Closed Write Boundary

Future cook writes are limited to:

1. the exact Vite files and focused tests/config listed above;
2. `spikes/web/harness/{simple-vite-v3.json,scripts/simple-vite-v3.mjs,tests/simple-vite-v3.test.mjs}`;
3. `mk/issue-5/i5-02.mk`;
4. `spikes/web/evidence/retained/simple-vite-v3/$RUN_ID/**` and
   `spikes/web/evidence/retention-index-v3.json`;
5. `docs/decisions/0005-web-stack.md` and the existing Markdown/JSON ADR-005 scorecards only at
   the authorized historical/current decision boundary; and
6. current v3 plan/index/matrix status or evidence links.

The lock, fixture adapter, and static host remain byte-read-only. Astro, Next, common/preview,
existing evidence and score anchors, Issue #6/contracts/schemas/fixtures, root/shared config,
`.github/**`, portal/runner, data/platform/cloud paths, sibling worktrees, and Issue #8+ are denied.
`apps/learning-portal/**` and `apps/lab-runner/**` are absent. No shared contract write is needed.

## Seven Blocking Test Groups

| ID | Executable route and sufficiency | Result |
|---|---|---|
| `V3-01` | frozen `npm ci`, Vite production build, before/after manifest/lock hashes and dist inventory | Cookable |
| `V3-02` | dependency-free `node --test` contract suite for identities, four grains, failure, exact conclusion/reason, reset, reflection | Cookable |
| `V3-03` | one tagged Chrome-channel Chromium journey with stable selectors and exact checkpoint assertions | Cookable |
| `V3-04` | same journey in desktop `1280×800` and narrow `360×800`; deterministic focus, hit-test, and overflow geometry | Cookable |
| `V3-05` | desktop-only default `AxeBuilder`, exactly one `analyze()`, retain all findings, block Critical/Serious only | Cookable |
| `V3-06` | desktop child context with real `javaScriptEnabled: false`, original response bytes, browser DOM/locator fact inventory and linear fallback | Cookable |
| `V3-07` | fixture/hash, zero High/Critical audit, S3 scans, evidence/index integrity, owned cleanup, rollback | Cookable |

All seven are conjunctive. Groups 3–6 share one smoke file and one Playwright process; they do not
create extra projects or a hidden matrix. Only desktop discovers axe/no-JS tests. Missing tools,
projects, artifacts, unexpected skips/retries, foreign ports, or partial results fail the gate.

## S3, Evidence, Cleanup, and Rollback Bounds

- The tracked v3 JSON contract closes scan roots, forbidden path/content patterns, exact commands,
  evidence schema, and time ceilings. The Node harness uses `node:fs`, `node:path`, `node:crypto`,
  `node:child_process`, and monotonic timers; npm supplies the advisory API.
- Source, build, browser output, and retained evidence are checked for credentials/private keys,
  secret assignments, private/absolute paths, PII-shaped data, source maps, raw headers/cookies,
  unsafe HTML/eval/dynamic code, remote imports, executable fixture fields, unescaped projection,
  causal attribution, CSP violations, cross-origin requests, and persisted browser state.
- Raw evidence stays transient until scans pass. Retention uses a closed manifest, byte-sorted
  hash index, and root retention index without recursive self-hashes or containing-commit claims.
- The ownership ledger records PID/process group/fingerprint/cwd/command/root/port/run ID/child
  handle. Cleanup closes contexts/browser first, signals only a revalidated owned group, and never
  kills a foreign/reused process.
- Rollback removes only the current run's candidate `node_modules`, dist/results/report, ephemeral
  profiles, and transient runtime/raw evidence. It preserves tracked source, valid RED, prior
  evidence/history, foreign processes, OS/browser profiles, Issue #6, and downstream worktrees.
- A pristine post-merge rerun uses a new temporary worktree and normal reviewed correction/revert
  on failure; no destructive reset or history rewrite is permitted.

## 16GB Serialization and Command Ceilings

The run is one candidate, one server, one worker, and one viewport project at a time. No Docker,
heavy profile, concurrent downstream build/browser work, performance sampling, RSS scoring, or
resource comparison is allowed.

The plan now sets exact fail-closed ceilings: 60 seconds for authority, 300 for install, 180 for
build, 120 for Node, 15 for host readiness, 300 for the full Playwright process, 60 per Playwright
test, 5 per assertion wait, 180 for npm audit, 120 per scan/retain/rollback verb, 900 for RED, and
1200 for gate or pristine rerun. These are operational hang bounds only. The historical
`3944.836095708`-second timer is closed, unread by v3, and has no budget, score, or selection role.

## CI, Review, and Human Gates

The repository has no tracked `.github/**` workflow, `gh workflow list` is empty, main branch
protection is absent, and repository rulesets are empty at audit time. This is recorded as
`CI_ABSENT_EXTERNAL_GATE`; it does not block local cook or PR creation and does not authorize
creating CI, required contexts, or shared workflow changes.

Two prerequisite independent exact-head reviews still gate the ADR-only commit; two fresh external
reviews gate the final ADR head. A repository-authorized human must approve that exact 40-hex PR
head before merge. CI absence cannot waive human approval. Production UAT/accessibility remains a
downstream risk, not an Issue #7 native/manual gate and not a conformance claim.

## Checks Executed

| Check | Result |
|---|---|
| `ck plan validate .../simple-vite-acceptance-amendment-v3.md --strict --json` | Pass before corrections: valid, four phases, zero issues; repeated after corrections |
| Local links/anchors/path parents | Pass for current plan/index/matrix/validation/audit surfaces |
| Phase/test counts | Pass: exactly four `## Phase` headings and seven `V3-01..07` rows |
| Stale/hidden-matrix sweep | Pass: no active Firefox/Next/Astro comparison, score/tie/performance/timer/native/manual/portal gate |
| Lock/cache/API/registry/Chrome checks | Pass without install, build, or browser launch |
| Issue #6 hashes/blobs/ancestry/live state | Pass |
| Existing fixture contract probe | Three focused promotion-trust/retail tests pass |
| Optional broader Issue #7 Python probe | Not used for verdict: it collected three passing tests then hit missing audit-host-only `rfc8785`; v3 imports no Python/rfc8785 and reproves the handoff with exact hashes/blobs plus its Node harness |
| Protected hashes/trees and output allow-list | Pass; only current plan/audit wording artifacts change |
| `git diff --check`, secret/private-path diff scan, clean publication checks | Required pass before commit/push and repeated after publication |

The optional Python diagnostic is recorded rather than hidden. It is outside all seven v3 groups,
does not affect the frozen JavaScript toolchain, and does not weaken the exact Issue #6 identity
proof.

## Gate Disposition

| Gate | State after publication |
|---|---|
| Barrier B / Issue #6 fixture | Open at exact authority and identities |
| Serialized simple TDD cook | Open only from the audit publication output SHA |
| ADR-005 Accepted/Vite | Closed until seven groups, S3, RED, evidence, and prerequisite reviews pass |
| PR | Allowed after exact-head final reviews; CI absence is named, not expanded |
| Merge | Closed until repository-authorized human exact-head approval and any configured checks |
| Native/manual UAT, conformance, cloud/AWS/Terraform | Not an Issue #7 gate and not authorized |

## Whole-Plan Consistency Sweep

- Files reread: current plan index, v3 amendment, acceptance matrix, v3 validation report, current
  ADR/scorecard surfaces, and historical phase links behind explicit non-binding markers.
- Decision deltas checked: command ceilings, readiness state, Barrier B, CI absence, human gate.
- Historical v1/v2/native/timer/score content changed: no.
- Unresolved contradictions: zero.

## Unresolved Questions

None.

`READINESS_VERDICT=READY_WITH_GATES`

`INPUT_SHA=aa93dfac5cd4a5f4d351ad045b634bbd42254902`

`OUTPUT_SHA=externally-attested-in-issue-7-publication-comment`

`IMPLEMENTATION_INPUT_SHA=same-as-output`

`ACCEPTANCE_REVISION=i5-02-simple-vite-v3`

`BLOCKING_TEST_GROUPS=7`

`BROWSER_TOOLCHAIN=ready`

`BARRIER_B=open`

`ISSUE_STATE=ready to cook`

`NEXT_PHASE=serialized-simple-tdd-cook`
