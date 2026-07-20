# Candidate Protocol

## Status

This is a future execution contract, not proof that any target, package, browser, candidate, or
evidence exists. No command below is run in the planning phase.

## Current Staged Authorization

The fresh readiness audit authorizes Gate 0 and Gate A only. The first cook may expose exactly:

```text
i5-02-authority-check
i5-02-protected-hash-check
i5-02-toolchain-check
i5-02-changed-path-check
i5-02-security-check
i5-02-credential-check
i5-02-non-copy-check
web-common-test
learn-preview
learn-preview-status
learn-preview-reset-check
learn-preview-down
```

The Make fragment must reject every unknown target and contain no candidate, install, build,
browser, barrier, scoring, ADR, retention, winner, or rollback target. Every later target in this
document remains a design contract only and must be absent until a later readiness audit. Candidate
directories/manifests/locks must also be absent. `stage-status.json` makes those states
machine-visible and declares the full issue incomplete.

## Frozen Toolchain and Modes

| Concern | Freeze |
|---|---|
| Host baseline | Node `v22.22.3`; npm `10.9.8`; lockfile version 3; exact equality required |
| Shared browser harness | [Playwright `1.61.1`](https://github.com/microsoft/playwright/releases/tag/v1.61.1); exact managed/current browser versions recorded at Gate C |
| Astro | [`astro@7.1.3`](https://github.com/withastro/astro/releases/tag/astro%407.1.3), [`react@19.2.7`](https://github.com/facebook/react/releases/tag/v19.2.7), `react-dom@19.2.7`; static output + smallest React control island; common static host |
| Next | [`next@16.2.10`](https://github.com/vercel/next.js/releases/tag/v16.2.10), `react@19.2.7`, `react-dom@19.2.7`; self-hosted standalone App Router; prerenderable lesson; narrow client boundary; read-only Route Handler |
| Vite | [`vite@8.1.5`](https://github.com/vitejs/vite/releases/tag/v8.1.5), `react@19.2.7`, `react-dom@19.2.7`; prerendered/MPA static semantic artifact + progressive React; common static host |
| Package policy | Exact top-level versions, one independent lockfile per candidate, clean `npm ci`, reviewed lifecycle scripts; dependency-free common harness with no package manifest/lock; no package workspace that couples candidates |

All remaining packages are pinned exactly in their owning manifest/lock during implementation.
Changing a top-level or transitive lock, candidate mode, common test semantics, fixture digest, or
browser version invalidates affected evidence. It never extends a candidate or total cap.
Root `.gitignore` ignores `package-lock.json`, so a later candidate authorization must use exactly
`git add -f -- spikes/web/candidates/astro/package-lock.json spikes/web/candidates/next/package-lock.json spikes/web/candidates/vite/package-lock.json`
and prove those paths are tracked. Broad force-add, ignore-rule edits, or a root/common lock is a
hard failure.

No package manifest, lockfile, `npm ci`, package install, or browser install is allowed in the
current Gate 0/Gate A cook. The common preview is dependency-free.

## Fairness Boundary

Shared across candidates:

- logical manifest, mart evidence, state, failure, client, evidence-index, and candidate-evidence
  shapes;
- fixture projections and digest rules;
- state transition/failure tables;
- WEB test IDs, roles/labels, and test semantics;
- measurement definitions, timer format, evidence schema, and score anchors.

Not shared or forced:

- components, rendering primitives, layout/style implementation, router APIs, hydration APIs,
  state library, framework lifecycle, content-loader API, or deployment code.

The common static host is measurement/lifecycle infrastructure only. It does not render routes or
become a portal/BFF framework.

## Timer and Kill Behavior

| Budget | Start | Stop/kill |
|---|---|---|
| Gate A common/preview: 3h | First contract/test/preview implementation action after Gate 0 | Stop/replan if logical contract cannot stabilize; reduce polish only |
| Astro: 3h | First candidate install/authoring action after common freeze | Kill at 90m without clean install + static semantic route + common consumption; kill at 3h for any executable must-pass red |
| Next: 3h | Same | Same |
| Vite: 3h | Same | Same |
| Gate C + Gate D: 2h | First real-fixture clean install/build/run action | Stop at 2h or 14h total; no winner on incomplete/invalid evidence |

UTC timer records include candidate/gate, start/end, active seconds, pause start/end/reason,
foundation disposition, must-pass disposition, and cumulative total. Debugging, installs,
authoring, builds, tests, measurements, and fixes count. Only an external registry/browser outage
or required owner decision may pause, with evidence; no candidate receives compensating time.
Gate 0 and Barrier B waiting do no product work and are outside the active budget.

Pre-Barrier-B candidate dispositions use `evidenceScope: foundation`:

- `PROVISIONAL_UNSCORED`: all foundation-scope candidate/common unit, schema, semantic-static,
  lifecycle, content, S3, supply-chain, and non-copy must-passes are green. Browser E2E/manual
  review and the real fixture are enumerated as required `decisionScope` Gate C inputs, not as
  optional, passed, or silently skipped.
- `ELIMINATED`: 90-minute/3-hour kill or a permanent must-pass breach; `numericScore` is null.

No other successful pre-Barrier-B status is permitted.

Candidate `*-a11y` and `*-e2e` targets belong to `evidenceScope: decision` and execute only in
Gate C after Barrier B and the frozen browser environment exist. Invoking them earlier still
exits non-zero; that expected unavailable-gate result does not by itself eliminate an otherwise
green foundation. Gate C invokes all decision-scope targets, and any failure then eliminates the
candidate. `not-run-optional` is never used.

## Environment and Sample Rotation

Record OS/kernel/architecture, CPU/model/count, physical memory, Node/npm, candidate lock/mode,
Playwright/browser, viewport/device scale/fonts, locale/timezone, reduced motion, ports, readiness,
fixture/contract/test-ID digests, measurement order, background load, and command hashes.

Gate C uses complete rounds:

1. Astro → Next → Vite
2. Next → Vite → Astro
3. Vite → Astro → Next

Each round captures one cold and one warm start per surviving candidate, yielding three cold and
three warm samples. Predefined invalidation applies to the whole comparable round/category; no
selective candidate retry. An inability to rerun fairly inside the cap yields no winner.

## Measurement Definitions

- Clean install: exact `npm ci` from an empty candidate `node_modules`; registry time is separate
  from startup but counts candidate/Gate C active time. Inspect lock lifecycle/provenance policy
  before approved script execution.
- Cold app start: built artifact; safely remove only declared candidate-local runtime cache; launch
  new production-like process; stop timing at successful semantic readiness.
- Warm app start: cleanly stop; keep built artifact/cache; launch new process to same readiness.
- RSS: sum the owned server/static-host process tree at readiness and after `WEB-E2E-001`; record
  PID tree and sampling method. Browser memory is separate.
- Client/build: emitted asset manifest, raw/gzip/brotli sizes, initial route JS, lab-opening/lazy
  chunks, browser transfer, source-map policy, and total built artifact size are separate values.
- Authoring task: identical callout + limitation field + prerequisite probe + hint; then remove a
  required field and record error location/clarity/types/editor support/hot reload/glue/active time.
- Visual/E2E: stable Chrome channel plus one additional engine; normalized entry/failure/four-card/
  reset/verify/reflection screenshots; first failure trace; JS-off/offline/reduced/back/reload/reset/
  200% projects.
- Manual accessibility: same build, keyboard checklist, named screen reader/browser/OS, headings/
  landmarks/tables/status/errors, focus after disclosure/reset, 200% reflow, reduced motion, and
  no-JS comprehension. Axe never substitutes.

## Must-Pass and Scoring

The exact 12-item must-pass list is in Phase 7 and the acceptance matrix. Any red candidate is
`ELIMINATED`, never scored. A missing browser/manual record makes the decision evidence incomplete
and prevents scoring/winner publication.

Only complete passing candidates receive 0-5 anchored category scores. Gate 0 must commit and
digest-freeze `spikes/web/harness/score-anchors.json` before any candidate action. It contains all
seven categories and every integer level 0..5, with each level defined by machine-checkable
numeric thresholds and/or a fixed reviewer predicate checklist tied to the raw evidence below.
Missing levels, free-form interpolation, candidate-relative/post-observation criteria, or any edit
after the freeze invalidates all candidate evidence:

| Category | Weight |
|---|---:|
| Authoring/content schema/MDX | 20 |
| Accessibility/static/reduced motion | 20 |
| Lab state/evidence/typed API | 20 |
| Cold/warm startup, RSS, client JS | 15 |
| Unit/E2E/visual evidence | 10 |
| Hosted/ECS evolution/rollback | 10 |
| Maintenance/dependency/supply chain | 5 |

Points equal `weight * anchor / 5`; weights sum to 100. Highest passing total wins. A tie within
five points defaults to Astro only when Astro is a complete passing candidate and every
comparison input is valid. A preference, partial score, killed candidate, or synthetic evidence
cannot trigger the tie rule.

Mandatory no-winner cases:

- no complete passing candidate;
- issue #6 merge/digests absent, mixed, dirty, or drifted;
- current-browser/manual accessibility evidence absent;
- measurement/visual comparability invalid and not equally rerun;
- any required evidence/retention/security/non-copy field incomplete; or
- Gate C/D or total active cap expires.

## Evidence Schema

Canonical generated root:
`.artifacts/evidence/web-spike/<run-id>/`. This is generated run state, not a tracked changed-path
allowance and is not ignored by the repository, so it must never be staged. The Gate A
sanitized/hash-indexed subset is retained under
`spikes/web/evidence/retained/gate-a/<run-id>/` before publication; all transient `.artifacts`
state created by the cook is then removed.

Every `fitness-result-v1` record includes:

```json
{
  "schemaVersion": "fitness-result-v1",
  "issue": 7,
  "runId": "<opaque-safe-id>",
  "gate": "gate-0|gate-a|candidate|barrier-b|gate-c|gate-d",
  "candidate": "common|preview|astro|next|vite|decision",
  "fixtureKind": "synthetic-preview|issue-6-tracked-real|null",
  "notice": "SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE|null",
  "evidenceScope": "foundation|decision|barrier|null",
  "resultStatus": "pass|fail|blocked-tbc|not-run-optional",
  "candidateDisposition": "PROVISIONAL_UNSCORED|ELIMINATED|PASS|WINNER|NO_WINNER|null",
  "numericScore": null,
  "decisionGrade": false,
  "issueComplete": false,
  "opensBarrierB": false,
  "implementationInputSha": "<40-hex>",
  "inputDiscoverySha": "a39251d45a56124322b9143ad16b926b2656073b",
  "testedTreeSha": "<40-hex>",
  "issue6MergeSha": "<40-hex-or-null>",
  "fixtureDigests": {},
  "contractDigest": "<sha256-or-null>",
  "testIdDigest": "<sha256>",
  "modeDigest": "<sha256>",
  "lockDigest": "<sha256-or-null>",
  "environment": {},
  "commands": [],
  "timer": {},
  "mustPass": [],
  "measurements": {},
  "artifacts": [],
  "redactionClass": "public-synthetic|public-sanitized-real",
  "retentionLocator": "<safe-relative-path-or-null>",
  "rollbackResult": {}
}
```

Unknown security-sensitive fields, absolute paths, environment dumps, cookies/headers/tokens,
secrets/PII, raw untrusted HTML/MDX, or recursive self-commit claims are rejected. Raw evidence is
hash-indexed; a sanitized retained subset lives under `spikes/web/evidence/retained/**` through
I5-05. The tracked scorecard stores tested-tree/attestation distinction and never claims its own
containing commit SHA.

Gate A records use `candidate: "common"` or `"preview"`, `fixtureKind: "synthetic-preview"`, the
exact permanent notice, null disposition/score, and `decisionGrade`, `issueComplete`, and
`opensBarrierB` all false. Static/logical accessibility facets may pass; actual browser, keyboard,
named screen-reader, 200% rendering, reduced-motion rendering, and no-JS manual facets remain
`required-pending` and cannot be promoted to a Gate A pass.

## Planned Command Registry

All commands below are future issue-local/direct interfaces and do not exist yet. Every Make
target first invokes Gate 0 and writes/updates the canonical evidence record.

For the current scope, only the twelve targets in [Current Staged Authorization](#current-staged-authorization)
may be implemented. The lifecycle source of truth is also directly callable without Make:

```bash
node spikes/web/harness/scripts/preview-control.mjs start --lesson promotion-trust --port 4174 --implementation-input <sha>
node spikes/web/harness/scripts/preview-control.mjs status --port 4174 --implementation-input <sha>
node spikes/web/harness/scripts/preview-control.mjs reset-check --lesson promotion-trust --implementation-input <sha>
node spikes/web/harness/scripts/preview-control.mjs down --port 4174 --implementation-input <sha>
```

The Node host hardcodes the real preview root and exact routes `/`, `/index.html`, `/preview.css`,
`/preview.mjs`, and `/__i5_02_ready`; rejects symlinks, traversal, dotfiles, directory listings, and
unknown paths; binds only `127.0.0.1`; emits no CORS; and uses a CSP with `default-src 'none'`,
`script-src 'self'`, `style-src 'self'`, `img-src 'self'`, and all connect/object/worker/manifest/
font authority denied. The per-port locator under
`.artifacts/runtime/i5-02/learn-preview/<port>.json` binds PID/process group, process-start
fingerprint, command hash, cwd, real preview root, host/port, run ID, fixture digest, and
implementation input. Status/down never signal a mismatched or foreign process. Start does not
auto-select a port; readiness expires at 10 seconds and timeout stops only the just-started owned
process group.

| Command/target | Expected status and evidence | Non-zero behavior |
|---|---|---|
| `node --test spikes/web/harness/tests/authority.test.mjs` | Unit test report for drift/ownership negatives | Any assertion/tool error |
| `node spikes/web/harness/scripts/authority-check.mjs --implementation-input <full-40-hex-authorized-sha>` | Initial local/tracking/live-remote equality, required ancestry, hashes/path/toolchain/mode/WEB-ID/anchor record | Any input/remote/ancestry/hash/path/freeze/tool mismatch |
| `make -f mk/issue-5/i5-02.mk i5-02-authority-check IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>` | Same normalized Gate 0 record | Same |
| `make -f mk/issue-5/i5-02.mk i5-02-protected-hash-check IMPLEMENTATION_INPUT_SHA=<sha>` | Root/protected/discovery hash/absence report | Any drift/presence violation |
| `make -f mk/issue-5/i5-02.mk i5-02-toolchain-check IMPLEMENTATION_INPUT_SHA=<sha>` | Exact Node/npm/top-level/mode policy report | Range/version/mode/lock-format mismatch |
| `make -f mk/issue-5/i5-02.mk i5-02-changed-path-check IMPLEMENTATION_INPUT_SHA=<sha>` | Allow/deny path report; candidate paths absent now, exact tracked locks in a later candidate scope | Forbidden/shared/protected/discovery path, premature candidate path/lock, broad force-add, or missing input |
| `make -f mk/issue-5/i5-02.mk i5-02-security-check IMPLEMENTATION_INPUT_SHA=<sha>` | S3 content/network/CSP/evidence negative-test index; dependency absence in Gate A | Unsafe content/route/CSP/dependency/evidence or missing required record |
| `make -f mk/issue-5/i5-02.mk i5-02-credential-check IMPLEMENTATION_INPUT_SHA=<sha>` | High-confidence source/header/path canary report | Any credential/private-key/private-URL/absolute-path exposure |
| `make -f mk/issue-5/i5-02.mk i5-02-non-copy-check IMPLEMENTATION_INPUT_SHA=<sha>` | Source/license/principle inventory and reviewer result | Missing inventory/reviewer or derivative prose/asset/layout/style/source |
| `node --test spikes/web/common/tests/*.test.mjs` | Common WEB assertion results | Any applicable WEB failure |
| `make -f mk/issue-5/i5-02.mk web-common-test IMPLEMENTATION_INPUT_SHA=<sha>` | `gate-a/common-tests.json`, test-ID digest | Any WEB failure/missing/duplicate ID |
| `make -f mk/issue-5/i5-02.mk learn-preview LESSON=promotion-trust PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<sha>` | `pass`; loopback URL/PID/digest/label/evidence root; fixed port and 10s readiness deadline | Wrong lesson/host, invalid/occupied port, asset/readiness timeout, stale PID, unsafe route |
| `make -f mk/issue-5/i5-02.mk learn-preview-status PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<sha>` | `pass` only when recorded process and semantic readiness match | Down/stale/wrong process/readiness |
| `make -f mk/issue-5/i5-02.mk learn-preview-reset-check LESSON=promotion-trust IMPLEMENTATION_INPUT_SHA=<sha>` | Reducer applies reset twice; resettable-state/baseline digest is unchanged, audit counter increments once per call, and history is replaced | Wrong fixture/digest, non-baseline state, counter/history mismatch, resettable-state drift |
| `make -f mk/issue-5/i5-02.mk learn-preview-down PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<sha>` | `pass`; idempotent owned-tree shutdown and retained evidence | Foreign target or owned process survives |
| `python3 -m http.server 4174 --bind 127.0.0.1 --directory spikes/web/preview` | Foreground no-build review fallback; no PID/CSP/fitness/score claim | Python/bind/path failure |
| `make -f mk/issue-5/i5-02.mk web-astro-install`<br>`make -f mk/issue-5/i5-02.mk web-next-install`<br>`make -f mk/issue-5/i5-02.mk web-vite-install` | Candidate lock/lifecycle/install/timer evidence | Dirty/mismatched lock, policy/advisory block, install failure, cap/authority breach |
| `make -f mk/issue-5/i5-02.mk web-astro-build`<br>`make -f mk/issue-5/i5-02.mk web-next-build`<br>`make -f mk/issue-5/i5-02.mk web-vite-build` | Frozen mode/build/static semantic manifest | Build/mode/schema/non-semantic/unsafe output failure |
| `make -f mk/issue-5/i5-02.mk web-astro-test`<br>`make -f mk/issue-5/i5-02.mk web-next-test`<br>`make -f mk/issue-5/i5-02.mk web-vite-test` | Candidate-specific plus unchanged common assertion index | Any required unit/schema/static/common failure |
| `make -f mk/issue-5/i5-02.mk web-astro-a11y`<br>`make -f mk/issue-5/i5-02.mk web-next-a11y`<br>`make -f mk/issue-5/i5-02.mk web-vite-a11y` | Gate C `decision` scope: automated semantic/axe/reflow/motion/static results; manual status separate | Barrier/browser/tool/assertion missing/failing; cannot mark manual pass |
| `make -f mk/issue-5/i5-02.mk web-astro-e2e`<br>`make -f mk/issue-5/i5-02.mk web-next-e2e`<br>`make -f mk/issue-5/i5-02.mk web-vite-e2e` | Gate C `decision` scope: fresh deterministic WEB traces/screenshots for merged fixture | Barrier/browser missing, WEB failure, digest/mode drift |
| `make -f mk/issue-5/i5-02.mk web-astro-evidence SCOPE=foundation`<br>`make -f mk/issue-5/i5-02.mk web-next-evidence SCOPE=foundation`<br>`make -f mk/issue-5/i5-02.mk web-vite-evidence SCOPE=foundation` | Foundation record + timer + explicit pending decision-scope list; provisional/eliminated only | Incomplete/unsafe foundation evidence, missing pending-gate inventory, illegal score/winner/status |
| `node --test spikes/web/harness/tests/barrier-b.test.mjs` | Absent/mixed/unmerged/tamper/invalidation results | Any assertion/tool error |
| `make -f mk/issue-5/i5-02.mk web-barrier-b-check I5_01_MERGE_SHA=<sha>` | `pass` only with merged ancestor + four digests/schema/read-only state | Any missing/unmerged/mixed/unsafe/dirty/invalidation failure |
| `make -f mk/issue-5/i5-02.mk web-real-fixture-rerun I5_01_MERGE_SHA=<sha>` | One rotated clean real-fixture run index for survivors | Barrier/browser/env drift, candidate/must-pass/sample/cap failure |
| `make -f mk/issue-5/i5-02.mk web-browser-evidence` | Fresh current Chrome + second-engine screenshot/trace/version index | Missing/stale/unequal/failed browser evidence |
| `make -f mk/issue-5/i5-02.mk web-manual-a11y-check` | Named keyboard/AT/zoom/reduced/no-JS reviewer record | Any checklist/candidate/version/reviewer evidence absent/failing |
| `make -f mk/issue-5/i5-02.mk web-spike-scorecard-check` | Valid complete winner or explicit no-winner schema | Illegal score/tie/winner, missing must-pass/evidence, drift/cap/retention failure |
| `make -f mk/issue-5/i5-02.mk web-retention-check` | Source/lock/command/raw/browser/manual/non-copy hashes through I5-05 | Missing/unhashed/unsafe/prematurely deleted artifact |
| `make -f mk/issue-5/i5-02.mk web-winner-reproduce` | Clean reproduction of complete proposed winner | No-winner, missing winner inputs, build/start/test mismatch |
| `make -f mk/issue-5/i5-02.mk web-local-rollback-check` | Prior complete local artifact restored; selection removed; evidence retained | Failed restore, shared/protected deletion, evidence loss |

Allowed result statuses follow the master registry. `blocked-tbc` is not a substitute for known
issue #6/browser dependencies: their barrier commands simply exit non-zero until satisfied.
`not-run-optional` is never valid for a required candidate/must-pass/browser/manual gate.

## Cleanup and Rollback

- Runtime PID/port/cache/install/build state is candidate-scoped and removable after safe process
  identity checks; sanitized raw evidence is retained under the allowed spike evidence root.
- Losing candidates remain outside default/product builds but keep explicit reproduction commands.
- Source removal before I5-05 is forbidden. Later removal requires separate authority, a source
  bundle/hash, locks/commands/digests/evidence/non-copy retention, clean winner reproduction, and
  changed-path proof.
- Contaminated comparison rollback deletes numeric scores/winner selection, sets ADR-005 back to
  Proposed/no-winner, clears only scoped browser/runtime state, and leaves the neutral preview,
  source, raw evidence, and unrelated data intact.
