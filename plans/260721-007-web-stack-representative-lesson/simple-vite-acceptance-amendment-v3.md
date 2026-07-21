---
title: "Issue #7 Simple Vite Acceptance Amendment v3"
description: "Tests-first plan for the owner-selected Vite candidate using seven minimal acceptance tests and exact-head release governance."
status: validated-pass-with-fixes
priority: P1
issue: 7
branch: "feature/issue-5-02-web-spike"
tags: [frontend, vite, react, accessibility, security-s3, tdd]
acceptanceRevision: "i5-02-simple-vite-v3"
inputSha: "358c305e5988a44ad4261b748aac3ea454c73dad"
plannerOutputSha: "d79ce5638e4a47c5c0963bba1a546448bc0c0ea6"
validationInputSha: "d79ce5638e4a47c5c0963bba1a546448bc0c0ea6"
validationReport: "validation/simple-vite-independent-validation-report-v3.md"
nextPhase: "fresh-simple-readiness-audit"
issue6IntegrationSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
ownerDecision: "https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177"
historicalTimerRemainingSeconds: "3944.836095708"
historicalTimerStatus: "closed-non-binding-for-v3"
phaseCount: 4
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
---

# Issue #7 Simple Vite Acceptance Amendment v3

## Verdict and planning boundary

`i5-02-simple-vite-v3` is the sole current Issue #7 acceptance authority. The owner selected
**Vite + React** and replaced every prior v2 readiness/cook/comparison path with the seven-test
gate below. The selection is an owner decision, not a new comparison or score.

This artifact passed fresh independent validation with fixes from clean local, tracking, and
fresh-live input `d79ce5638e4a47c5c0963bba1a546448bc0c0ea6` on
`feature/issue-5-02-web-spike`. This is `INDEPENDENT_VALIDATION_PASS_NOT_READINESS`: it authorizes
no implementation, install, build, candidate/browser run, score, OS change, ADR transition, PR,
merge, or Issue #8+ write. The only next phase is a fresh simple readiness audit of the exact
published validation head.

## Authority and precedence

1. The [owner decision](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177)
   supersedes all prior Issue #7 v2 readiness/cook plans and blocking clauses.
2. Issue #7 was `triaged` at the planner source and is open with exact workflow label
   `ready for plan validation` at validator input; it retains `risk:high`, `tdd`, and
   `security:S3`.
3. Issue #6 integration/handoff
   `24be3b34c6b0fcdbd07c5800dcab349054e34713` is an ancestor of the planner input. Its four
   tracked fixture identities remain read-only and binding.
4. `/tmp/issue7-readiness-audit-superseded-by-simple-tests.patch` is forensic history only. It
   must not be applied, copied, imported, or cited as authority.
5. Astro, Next, v1/v2 evidence, score anchors, measurements, manual/native attempts, and prior
   timer records remain immutable history. No v3 run may rewrite, relabel, or derive a score from
   them.
6. Parallel downstream planning stays isolated in its existing worktrees. Issue #7 writes only
   the allow-list below and does not touch Issue #8+.
7. The next `fresh-simple-readiness-audit` is limited to this v3 authority, exact validated head,
   ownership, and static tool/path preconditions. It cannot restore a v1/v2 comparison, score,
   timer, native/manual, multi-browser, performance, or portal gate.

## Exact Issue #6 fixture identity

The implementation gate must recompute all values from the tested head and require exact equality:

| Read-only path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

The semantic identity is also exact:

- promotion grain: `promo_name × channel`;
- fulfillment grain: `carrier × region_name`;
- returns grain: `reason × category_name × region_name`;
- data-quality grain: `scenario`;
- conclusion: `insufficient-evidence`;
- reason: `no-common-grain`;
- cross-grain relationships and attribution-bearing fields: zero.

Any identity, ancestry, schema, grain, conclusion, or reason mismatch is a hard failure. Issue #7
never edits or regenerates the four files.

## Seven blocking tests

| ID | Exact acceptance | Evidence |
|---|---|---|
| `V3-01` | From the tracked Vite lock SHA-256 `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c`, run frozen `npm ci --ignore-scripts --no-audit --no-fund`, then `npm run build`; neither manifest nor lock changes. | install/build logs, exit codes, before/after manifest and lock hashes, `dist/**` inventory |
| `V3-02` | A focused dependency-free Node contract/unit suite proves exact fixture identity, the four named independent grains, controlled headline failure, exact conclusion/reason, no attribution, reset baseline, and reflection state. | TAP plus discovered test-name inventory |
| `V3-03` | One tagged Playwright journey, using the stable selectors and exact assertions below, proves entry → controlled failure → all four named grains → exact `insufficient-evidence` / `no-common-grain` conclusion → reset → reflection. | one suite JSON result and bounded checkpoint trace; no broad screenshot matrix |
| `V3-04` | The same journey runs in exactly two Chromium projects: desktop `1280×800` and narrow `360×800`, one worker at a time; keyboard focus is visibly styled and unobscured, and document/body width plus named-element geometry pass at every checkpoint. | per-project focus/overflow assertions and at most one failure screenshot per project |
| `V3-05` | The desktop project invokes the frozen `@axe-core/playwright` API exactly once and has zero `critical` and zero `serious` violations. Lower impacts are retained as non-blocking observations, not hidden. | complete axe JSON with impact counts and scanned URL/head SHA |
| `V3-06` | A real `browser.newContext({ javaScriptEnabled: false })` created only by the desktop project reads the production response and browser-parsed `dist/index.html`; the four named grains, four limitations, exact conclusion/reason, linear review order, reset limitation, and reflection prompt remain visible and understandable. Script interception/removal is not a substitute. | response bytes plus Playwright DOM/locator fact inventory from the no-JS context |
| `V3-07` | Reprove Issue #6 identities; `npm audit` has zero High/Critical; credential, private-path, PII, injection, CSP, same-origin, storage, retained-evidence, owned-server/profile cleanup, and rollback checks pass. | audit JSON, S3 scan JSON, ownership ledger, rollback JSON, retained manifest/hash/index |

The tests are conjunctive. Missing tools, skipped projects, missing artifacts, unexpected retries,
lock drift, an unrelated RED, or a partial run is failure. There is no numeric score and no
alternative-candidate fallback.

## Explicitly retired from blocking scope

V3 does not run or require:

- Firefox or any multi-browser matrix;
- Vite/Next/Astro head-to-head work;
- score anchors, weights, tie rules, or numeric scoring;
- performance, latency, RSS, CPU, or resource sampling;
- timer deadlines or remaining-budget enforcement;
- VoiceOver, native Chrome zoom, or macOS System Settings automation;
- broad screenshot matrices; or
- production-conformance, full-WCAG, or screen-reader-conformance claims.

The historical `3944.836095708` seconds remains preserved in v1/v2 provenance and is explicitly
closed/non-binding for v3. No reset, spend, or timer-based conclusion is recorded.

The existing ADR-005 scorecard Markdown/JSON remains byte-preserved historical v1 evidence until
Phase 4. Its current words `Proposed`, `no-winner`, `acceptance blocked`, fresh Gate C, manual/native,
Firefox, candidate disposition, anchor, and numeric-score fields have zero v3 gating or selection
authority and cannot be imported by the v3 runner/index/matrix. The later authorized ADR-only
update must retain that record under an explicitly historical section/object and add a separate
current v3 owner-selected, unscored decision record; it may not reinterpret or delete history.

Residual risk is concise: Chromium + axe + keyboard/reflow/no-JS automation does not substitute
for production UAT, assistive-technology testing, or a scoped WCAG conformance audit. Those remain
downstream release responsibilities and do not block the Issue #7 Vite decision.

## Stable journey and fallback contract

The pure `lesson-contract.mjs` is the single source of the exact values below. Authored fallback
HTML and React controls expose stable `data-testid` selectors; tests use those selectors for state
and use visible text only to assert the human-readable contract. Renaming a selector or weakening
an expected value is a contract change, not a test repair.

| Checkpoint | Stable selector | Exact expected assertion |
|---|---|---|
| Entry | `[data-testid="lesson-entry"]` | The title is exactly `Can this promotion headline be trusted?`; `TRACKED REAL FIXTURE — UNSCORED — CANNOT COMPLETE` is visible; `[data-testid="lesson-status"]` is exactly `Exploration is reversible and unverified.` |
| Controlled failure | `[data-testid="run-bounded-probe"]` then `[data-testid="lesson-status"]` | Keyboard `Enter` activation leaves the button focused and sets exactly `Controlled failure: no common grain; no answer, attribution, completion, or score saved.` |
| Promotion grain | `[data-testid="grain-promotion"]` and `[data-testid="grain-promotion-limitation"]` | Visible grain is exactly `promo_name × channel`; limitation is exactly `Promotion aggregates cannot identify fulfillment, returns, or data-quality causes.` |
| Fulfillment grain | `[data-testid="grain-fulfillment"]` and `[data-testid="grain-fulfillment-limitation"]` | Visible grain is exactly `carrier × region_name`; limitation is exactly `No shared key permits attribution to a promotion.` |
| Returns grain | `[data-testid="grain-returns"]` and `[data-testid="grain-returns-limitation"]` | Visible grain is exactly `reason × category_name × region_name`; limitation is exactly `No shared key permits attribution to a promotion.` |
| Data-quality grain | `[data-testid="grain-data-quality"]` and `[data-testid="grain-data-quality-limitation"]` | Visible grain is exactly `scenario`; limitation is exactly `Scenario evidence is independent and does not establish a cause.` |
| Conclusion | `[data-testid="lesson-conclusion"]` and `[data-testid="lesson-reason"]` | Values are exactly `insufficient-evidence` and `no-common-grain`; relationships and attribution remain empty. |
| Reset | `[data-testid="reset-lesson"]` then `[data-testid="lesson-status"]` | Keyboard `Space` activation leaves reset focused and sets exactly `Reset: baseline restored; no answer, attribution, completion, or score persisted.`; cookies and all browser storage remain empty. |
| Reflection | `[data-testid="reflection-prompt"]` | Visible text is exactly `Reflection: What additional common-grain evidence would be needed before making a causal claim?`; no completion or score control exists. |

The journey performs those checkpoints in table order. The no-JS source order is entry → four
grains and limitations → conclusion/reason →
`[data-testid="no-js-reset-limitation"]` with exact text
`Without JavaScript, reset is unavailable; all facts remain in their baseline state.` → reflection.
The existing Playwright 1.61.1 browser DOM and locator API is the HTML parser for this check; no
invented parser package, script interception, response rewriting, or transitive dependency import
is allowed.

## One Chromium and executable axe strategy

`playwright.config.mjs` defines exactly two projects and no device/browser matrix:

- `chromium-desktop`: `browserName: 'chromium'`, `channel: 'chrome'`, viewport `1280×800`;
- `chromium-narrow`: the same browser/channel, viewport `360×800`.

Both run the one `@journey` test. Only desktop selects the two `@desktop-only` tests: the single
whole-page axe invocation after the reflection checkpoint and the real no-JS context. Narrow does
not discover them as skipped tests; project
`grep` selects `@journey` for narrow and `@journey|@desktop-only` for desktop. Workers are `1`,
retries are `0`, and the harness starts one existing static host on `127.0.0.1:4175` before the
Playwright process. The config has no `webServer`, alternate port, alternate browser, or browser
installation behavior.

Visible focus is deterministic. The journey reaches run/reset using `Tab`/`Shift+Tab`, proves the
named control is `document.activeElement`, and requires computed `outline-style: solid`, outline
width at least `2px`, and outline offset at least `2px`. The outline-expanded bounding rectangle
must stay inside the viewport, and the focused element must own the center hit-test. At every
checkpoint, both `documentElement` and `body` satisfy `scrollWidth <= clientWidth`; every named
checkpoint rectangle has `left >= 0` and `right <= innerWidth`.

The frozen Vite lock already declares `@axe-core/playwright@4.12.1`,
`axe-core@4.12.1`, and `@playwright/test@1.61.1`. The smoke spec uses the package's real default
export:

```js
import AxeBuilder from '@axe-core/playwright';

const axeResult = await new AxeBuilder({ page }).analyze();
const blocking = axeResult.violations.filter(
  ({ impact }) => impact === 'critical' || impact === 'serious',
);
expect(blocking).toEqual([]);
```

`analyze()` is called exactly once, with no disabled rules, excluded regions, impact relabelling,
or WCAG-tag claim. The complete result is retained; only Critical/Serious impacts block v3. This is
an axe threshold, not a full WCAG or screen-reader assessment.

## Minimal design

```text
Issue #6 tracked fixture (read-only)
  -> existing Vite build-time escaped projection
  -> static production dist
  -> React progressive controls for failure/reset/reflection
  -> one Chromium Playwright suite (two viewport projects + desktop no-JS context)
  -> one desktop axe scan
  -> S3/audit/cleanup/rollback gate
  -> retained v3 manifest + hash index + retention index
  -> reviews -> ADR-005 Accepted/Vite -> final exact-head reviews -> PR/human approval
```

No portal, runner, BFF, mutation API, cloud path, authentication, persistence, or completion
authority is introduced. Vite continues to emit a static document; React adds reversible local
interaction only. `apps/learning-portal/**` remains Issue #10 scope and is not pre-created here.

## Exact future file boundary

### Writable implementation allow-list

| Path | Planned action |
|---|---|
| `spikes/web/candidates/vite/index.html` | Minimal static/no-JS fallback and reflection copy only if build injection cannot express it cleanly |
| `spikes/web/candidates/vite/vite.config.mjs` | Emit escaped four-grain, limitation, conclusion, fallback, and reflection facts into production HTML |
| `spikes/web/candidates/vite/src/main.jsx` | Minimal controlled-failure/reset/reflection states and accessible controls |
| `spikes/web/candidates/vite/src/styles.css` | Visible focus and narrow overflow fixes only |
| `spikes/web/candidates/vite/src/lesson-contract.mjs` | Create one pure lesson/state contract shared by UI and Node tests |
| `spikes/web/candidates/vite/package.json` | Add only `test:unit` and `test:smoke` scripts; dependency versions stay unchanged |
| `spikes/web/candidates/vite/playwright.config.mjs` | Create exactly desktop and narrow Chrome-channel Chromium projects; desktop owns axe/no-JS context; `workers: 1`, retries `0` |
| `spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs` | Create focused Node contract/unit suite |
| `spikes/web/candidates/vite/tests/simple-vite-smoke.spec.mjs` | Create the sole v3 Chromium smoke/axe/no-JS suite |
| `spikes/web/harness/simple-vite-v3.json` | Create exact input, fixture, protected-path, command, and evidence contract |
| `spikes/web/harness/scripts/simple-vite-v3.mjs` | Create serialized authority/gate/scan/retain/cleanup runner |
| `spikes/web/harness/tests/simple-vite-v3.test.mjs` | Create negative tests for authority, evidence, S3, ownership, and rollback |
| `mk/issue-5/i5-02.mk` | Add thin v3 RED/gate/rollback/pristine targets only |
| `spikes/web/evidence/retained/simple-vite-v3/$RUN_ID/**` | Add sanitized exact-run evidence only |
| `spikes/web/evidence/retention-index-v3.json` | Add current v3 run locator and manifest/hash-index digests |
| `docs/decisions/0005-web-stack.md` | After gates and prerequisite reviews only, record Accepted/Vite and claim limits |
| `docs/decisions/evidence/adr-0005-web-stack-scorecard.md` | Preserve the no-winner scorecard as history; append owner-selected, unscored v3 decision evidence |
| `docs/decisions/evidence/adr-0005-web-stack-scorecard.json` | Preserve historical candidate results under an explicit historical object; record v3 without numeric scores |
| `plans/260721-007-web-stack-representative-lesson/{plan.md,acceptance-and-test-matrix.md,simple-vite-acceptance-amendment-v3.md}` | Validation/readiness/gate status and evidence-link sync only at the actual boundary |

The writable table is closed. `spikes/web/candidates/vite/package-lock.json`,
`spikes/web/candidates/vite/src/fixture.mjs`, and
`spikes/web/harness/scripts/candidate-static-host.mjs` are exact read-only dependencies and must
remain byte-identical. If a focused RED proves one must change, stop and amend/revalidate this plan;
reviewer approval alone cannot expand the allow-list.

### Deny-list

No v3 write may touch:

- `spikes/web/candidates/astro/**` or `spikes/web/candidates/next/**`;
- `spikes/web/common/**`, `spikes/web/preview/**`, `spikes/web/harness/score-anchors.json`, or any
  existing v1/v2 harness contract not named above;
- existing `spikes/web/evidence/retained/**` or `spikes/web/evidence/retention-index.json`;
- the four Issue #6 paths, `contracts/**`, `schemas/**`, or any other `tests/fixtures/**` path;
- root `Makefile`, `.gitignore`, `release-manifest.json`, `.github/**`, or absent
  `docs/code-standards.md`;
- `apps/learning-portal/**`, `apps/lab-runner/**`, data/dbt/Rill/Airflow/Iceberg/OpenMetadata,
  Docker, Terraform, AWS, cloud, or Issue #8+ paths;
- `/tmp/issue7-readiness-audit-superseded-by-simple-tests.patch`; or
- any sibling/downstream worktree.

Protected planner-input anchors are `Makefile`
`12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458`, `.gitignore`
`aa93e47707e95286126f47b3d70fe7fc6c047b49c861184533e38b3c5a971316`,
`release-manifest.json` `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539`,
common tree `f00fe97715df5dd469302994349fb95c9412482b`, Astro tree
`4b352a31354cc12bebcad9f0a461000c167e5f11`, Next tree
`85777043224f7f00ec944642e3531c1d891e5ec3`, and historical retained-evidence tree
`7b65d74d4131ed1ac9056ae05f599854215f99f5`.

## Four implementation phases

### Phase 1 — exact authority and contemporaneous RED

1. Begin only from the exact full SHA authorized by the fresh simple readiness audit. Prove branch,
   clean tree,
   local/tracking/fresh-live equality, ancestry from validation input
   `d79ce5638e4a47c5c0963bba1a546448bc0c0ea6`, Issue #6 ancestry and four identities, protected
   anchors, lock hash, and exclusive path ownership.
2. Add the Node and sole Playwright suite plus the v3 harness negative tests before product fixes.
   Commit the tests-only tree so RED has an exact SHA.
3. Run the frozen install and current production build, then execute every planned test. RED must
   be non-zero because named v3 behavior is absent or wrong. Every test must be discovered.
   Missing tools, browser, fixture, import/compile errors, unauthorized paths, or an intentionally
   weakened assertion are invalid RED.
4. Retain the exact test-only SHA, sorted changed-path manifest, commands, TAP/Playwright JSON,
   named failing assertions, and exit codes under the transient run root. RED is contemporaneous;
   it is never reconstructed after GREEN.

Planned command:

```bash
make -f mk/issue-5/i5-02.mk web-vite-v3-red \
  IMPLEMENTATION_INPUT_SHA="$IMPLEMENTATION_INPUT_SHA"
```

Success: valid acceptance-driven RED exists, all unrelated authority/security checks pass, and no
product/ADR/evidence-retention change has been made.

### Phase 2 — minimal Vite GREEN and seven tests

1. Implement only the pure lesson contract, escaped static facts/fallback, reversible React
   states, visible focus, and narrow layout needed by the RED.
2. Remove candidate-local `node_modules`, `dist`, test results, and temporary browser profile from
   the RED run using the ownership ledger. Re-run frozen `npm ci` and the production build from a
   clean candidate runtime.
3. Run `V3-02`, then the one Chromium suite serially. The desktop/narrow projects execute the
   identical journey; only desktop executes axe and creates the real no-JS fallback context.
   Both projects use Playwright `browserName: chromium` with the already installed stable
   `channel: chrome`, the existing static host at `127.0.0.1:4175`, and ephemeral contexts. The
   desktop project alone creates the additional real no-JS context and calls axe once. A missing
   browser channel is a hard STOP; v3 does not install a browser or alter an OS profile.
4. No retry, alternate browser, dev server, visual matrix, measurement, timer, or candidate
   comparison is allowed.

The v3 harness runs this exact inner sequence from the repository root. It spawns and owns the
static host between unit and smoke execution; `playwright.config.mjs` never starts a second server:

```bash
npm --prefix spikes/web/candidates/vite ci --ignore-scripts --no-audit --no-fund
npm --prefix spikes/web/candidates/vite run build
npm --prefix spikes/web/candidates/vite run test:unit
node spikes/web/harness/scripts/candidate-static-host.mjs spikes/web/candidates/vite/dist 4175
BASE_URL=http://127.0.0.1:4175 npm --prefix spikes/web/candidates/vite run test:smoke -- --workers=1 --retries=0
```

The fourth command is shown as the child command owned by `simple-vite-v3.mjs`; the harness waits
for its `READY` line, runs the fifth command, and closes only that recorded child in `finally`.
`package.json` scripts are exact: `test:unit` runs
`node --test tests/foundation.test.mjs tests/promotion-trust-contract.test.mjs`; `test:smoke` runs
`playwright test tests/simple-vite-smoke.spec.mjs --config playwright.config.mjs`.

Canonical gate command:

```bash
make -f mk/issue-5/i5-02.mk web-vite-v3-gate \
  IMPLEMENTATION_INPUT_SHA="$IMPLEMENTATION_INPUT_SHA"
```

Success: all seven test IDs pass against one exact source/tested SHA and production build.

### Phase 3 — S3 evidence, cleanup, and rollback

The gate runs, in the same serialized candidate session:

```bash
cd spikes/web/candidates/vite
npm audit --audit-level=high --json
cd ../../../..
node spikes/web/harness/scripts/simple-vite-v3.mjs scan \
  --implementation-input "$IMPLEMENTATION_INPUT_SHA"
node spikes/web/harness/scripts/simple-vite-v3.mjs retain \
  --implementation-input "$IMPLEMENTATION_INPUT_SHA"
node spikes/web/harness/scripts/simple-vite-v3.mjs rollback \
  --implementation-input "$IMPLEMENTATION_INPUT_SHA"
```

Required scan assertions:

- `npm audit` metadata is complete and both `high` and `critical` counts are zero; no `audit fix`,
  upgrade, or lock rewrite occurs.
- Source, built output, browser results, and retained evidence contain no credential/private-key,
  secret assignment, absolute user/workspace path, private URL, PII-shaped aggregate, source map,
  raw header/cookie, or env dump.
- No `dangerouslySetInnerHTML`, runtime `innerHTML`, `eval`, dynamic `Function`, remote import,
  executable fixture field, unescaped fixture interpolation, or causal attribution is present.
- CSP exists in production response and document, with no wildcard, remote script,
  `unsafe-inline`, `unsafe-eval`, script `data:`/`blob:`, form, object, base, or unexpected connect
  authority.
- Every browser request is same-origin loopback; cookies, local/session storage, Cache Storage,
  IndexedDB databases, service workers, and completion/score state are empty.
- The runner starts one loopback server on one declared port and one Playwright worker. It records
  PID, process group, start fingerprint, cwd, command, real root, port, run ID, and child handle.
  A foreign/reused port or mismatched process is a STOP and is never signalled.
- Browser contexts use ephemeral profiles only. Close contexts/browser first, stop only the owned
  server, remove only run-owned candidate runtime/output, and prove no owned listener/profile or
  transient `.artifacts/runtime/i5-02/$RUN_ID` remains.

The 16GB rule is serialization, not measurement: one candidate, one server, one Playwright worker,
one viewport project at a time, no Docker/heavy profile, and no concurrent downstream
build/browser/heavy-profile execution. Isolated planning may continue without writing this
worktree. V3 does not sample or score resource use.

Success: a sanitized retained run exists; rollback restores tracked source/evidence only, leaves
the tree clean apart from the intentional retained-evidence commit, and changes no denied path.

### Phase 4 — reviews, ADR, PR, merge, and pristine proof

1. Commit source/tests plus retained evidence. The retained manifest names the tested source SHA;
   the commit containing the manifest is necessarily external to it.
2. Two independent read-only reviewers inspect that exact head:
   - reviewer A: TDD RED/GREEN, code/harness, Issue #6 identity, S3, allow/deny paths, cleanup;
   - reviewer B: all seven acceptance results, Chromium/axe/no-JS claims, evidence hashes,
     residual UAT claim, rollback, and downstream boundary.
3. Only after both prerequisite reviews pass may a single ADR-only commit set ADR-005 to
   `Accepted` / `Vite + React`, record owner-selected/unscored decision basis, and preserve the
   former no-winner/scorecard content as historical. It must state explicitly that Issue #7 makes
   no full-WCAG, screen-reader, production-UAT, or production-conformance claim.
4. Because the ADR commit changes HEAD, reviewer A and reviewer B each issue a fresh final report
   against the exact ADR head. These final exact-head reports, stored externally in GitHub/CI so
   they do not mutate HEAD, are the reviews used for PR readiness. Any further commit invalidates
   both.
5. Push and create the PR only after both final reports pass. Any repository-configured required
   checks, if present, must pass the exact PR head; v3 neither creates `.github/**` nor invents a
   required status context. A repository-authorized human must explicitly approve that same
   40-hex head before merge; agent/standing approval cannot satisfy this gate.
6. After merge, fetch the exact merge SHA into a new pristine temporary worktree, run the full
   v3 gate with a new run ID, verify the merge contains the reviewed PR head, then remove only that
   temporary worktree/runtime. Failure triggers a normal reviewed corrective/revert flow; never a
   destructive reset.

Success: exact-head reviews, PR checks, human approval, merge identity, and pristine post-merge
verification all agree. Production UAT remains a separate downstream risk.

## Evidence manifest, hash index, and retention index

Canonical retained layout:

```text
spikes/web/evidence/retained/simple-vite-v3/$RUN_ID/
  manifest.json
  hash-index.json
  tdd/red/{node.tap,playwright.json,result.json}
  green/{install.log,build.log,node.tap,playwright.json,result.json}
  security/{npm-audit.json,scans.json}
  lifecycle/{owned-resources.json,rollback.json}
spikes/web/evidence/retention-index-v3.json
```

`manifest.json` is closed-schema and includes: revision/run ID; implementation input; test-only
RED SHA; tested source SHA; branch; dirty-state result; Issue #6 integration and all four
SHA/blob pairs; Vite manifest/lock hashes; exact commands, tools, exit codes and test-name/project
inventory; viewport/worker/retry/channel; seven test results; audit counts; scan summary; owned
resources; rollback; relative artifact locators; redaction result; and claim limitations.

`hash-index.json` lists every retained file except itself in bytewise path order with byte length
and SHA-256. It includes `manifest.json`; the manifest does not claim its own hash. The root
`retention-index-v3.json` names the one accepted run plus the manifest and hash-index digests. It
does not hash itself or claim the containing commit. Exact reviewed/final/merge SHAs are recorded
externally by reviews, PR metadata, and the post-merge report.

Raw traces/logs remain transient until the S3 scan passes. Only sanitized required evidence is
retained. Success screenshots are unnecessary; Playwright retains a trace and at most one
failure screenshot per desktop/narrow project, and no broad historical matrix is regenerated.

## Rollback

- Before retained evidence: stop only owned child handles/process groups and remove only the
  current run's candidate-local `node_modules`, `dist`, Playwright results/report, ephemeral
  profiles, and `.artifacts` runtime/raw evidence.
- After a failed gate: keep source/test changes for review, retain valid RED, publish no GREEN/ADR
  pass, and leave ADR-005 Proposed/historical no-winner.
- After a failed review: fix only allow-listed findings, rerun all seven tests under a new run ID,
  regenerate evidence, and obtain two new exact-head reports.
- After a failed merge verification: do not rewrite history. Open a normal reviewed corrective or
  revert change; retain both failed and superseding external reports.
- Never delete old candidates/evidence, edit Issue #6, kill foreign processes, clear browser/OS
  profiles, mutate downstream worktrees, or move portal implementation into Issue #7.

## Downstream handoff

After pristine merge verification, the Issue #7 handoff contains only:

- exact merge SHA and reviewed PR head;
- ADR-005 Accepted/Vite path and explicit owner-selected/unscored basis;
- `i5-02-simple-vite-v3` retained manifest/hash-index/retention-index paths and digests;
- Issue #6 integration SHA and four identities;
- production command/build entrypoint for the Vite candidate;
- residual accessibility/UAT limitation; and
- confirmation that no portal, runner, shared contract, AWS/Terraform, or Issue #8+ work was done.

Downstream owners consume that handoff in their own worktrees after the merge SHA is available.
Issue #7 does not pre-stage or integrate portal code.

## Plan checks and next state

Independent validation ran static checks only: strict plan structure, required-term/phase-count,
Markdown link/path, stale-clause, unresolved-placeholder, exact changed-plan allow-list,
credential/private-path diff, and clean local/tracking/fresh-live checks. No implementation or
readiness action ran.

On successful validation publication, comment Issue #7 with
`INDEPENDENT_VALIDATION_PASS_NOT_READINESS` and this report path, then transition exactly
`ready for plan validation` → `ready for plan audit`. Next phase:
`fresh-simple-readiness-audit`.
