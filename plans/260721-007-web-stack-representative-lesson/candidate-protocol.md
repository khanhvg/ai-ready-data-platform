# Candidate Protocol

## Status

This is a future execution contract, not proof that any target, package, browser, candidate, or
evidence exists. No command below is run in the planning phase.

## Frozen Toolchain and Modes

| Concern | Freeze |
|---|---|
| Host baseline | Node `v22.22.3`; npm `10.9.8`; lockfile version 3; exact equality required |
| Shared browser harness | [Playwright `1.61.1`](https://github.com/microsoft/playwright/releases/tag/v1.61.1); exact managed/current browser versions recorded at Gate C |
| Astro | [`astro@7.1.3`](https://github.com/withastro/astro/releases/tag/astro%407.1.3), [`react@19.2.7`](https://github.com/facebook/react/releases/tag/v19.2.7), `react-dom@19.2.7`; static output + smallest React control island; common static host |
| Next | [`next@16.2.10`](https://github.com/vercel/next.js/releases/tag/v16.2.10), `react@19.2.7`, `react-dom@19.2.7`; self-hosted standalone App Router; prerenderable lesson; narrow client boundary; read-only Route Handler |
| Vite | [`vite@8.1.5`](https://github.com/vitejs/vite/releases/tag/v8.1.5), `react@19.2.7`, `react-dom@19.2.7`; prerendered/MPA static semantic artifact + progressive React; common static host |
| Package policy | Exact top-level versions, independent lockfile per common harness/candidate, clean `npm ci`, reviewed lifecycle scripts; no package workspace that couples candidates |

All remaining packages are pinned exactly in their owning manifest/lock during implementation.
Changing a top-level or transitive lock, candidate mode, common test semantics, fixture digest, or
browser version invalidates affected evidence. It never extends a candidate or total cap.

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

Pre-Barrier-B candidate dispositions:

- `PROVISIONAL_UNSCORED`: all currently executable candidate/common must-passes are green; real
  fixture, fresh comparison, and manual Gate C review are still pending.
- `ELIMINATED`: 90-minute/3-hour kill or a permanent must-pass breach; `numericScore` is null.

No other successful pre-Barrier-B status is permitted.

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

Only complete passing candidates receive 0-5 anchored category scores:

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
allowance. The sanitized/hash-indexed raw decision subset is retained under
`spikes/web/evidence/retained/<run-id>/` before publication.

Every `fitness-result-v1` record includes:

```json
{
  "schemaVersion": "fitness-result-v1",
  "issue": 7,
  "runId": "<opaque-safe-id>",
  "gate": "gate-0|gate-a|candidate|barrier-b|gate-c|gate-d",
  "candidate": "common|preview|astro|next|vite|decision",
  "resultStatus": "pass|fail|blocked-tbc|not-run-optional",
  "candidateDisposition": "PROVISIONAL_UNSCORED|ELIMINATED|PASS|WINNER|NO_WINNER|null",
  "numericScore": null,
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

## Planned Command Registry

All commands below are future issue-local/direct interfaces and do not exist yet. Every Make
target first invokes Gate 0 and writes/updates the canonical evidence record.

| Command/target | Expected status and evidence | Non-zero behavior |
|---|---|---|
| `node --test spikes/web/harness/tests/authority.test.mjs` | Unit test report for drift/ownership negatives | Any assertion/tool error |
| `node spikes/web/harness/scripts/authority-check.mjs --base a39251d45a56124322b9143ad16b926b2656073b` | Exact SHA/hash/path/toolchain/mode/WEB-ID record; `pass` only on equality | Any mismatch/missing required tool |
| `make -f mk/issue-5/i5-02.mk i5-02-authority-check` | Same normalized Gate 0 record | Same |
| `make -f mk/issue-5/i5-02.mk i5-02-protected-hash-check` | Root/protected/discovery hash/absence report | Any drift/presence violation |
| `make -f mk/issue-5/i5-02.mk i5-02-toolchain-check` | Exact Node/npm/top-level/mode policy report | Range/version/mode/lock-format mismatch |
| `make -f mk/issue-5/i5-02.mk i5-02-changed-path-check BASE_SHA=<sha>` | Allow/deny path report | Forbidden/shared/protected/discovery path or missing base |
| `make -f mk/issue-5/i5-02.mk i5-02-security-check` | S3 content/bundle/network/CSP/dependency/evidence negative-test index | Unsafe content/route/CSP/dependency/evidence or missing required record |
| `make -f mk/issue-5/i5-02.mk i5-02-credential-check` | High-confidence source/bundle/source-map/trace/header/cookie/path canary report | Any credential/private-key/private-URL/absolute-path exposure |
| `make -f mk/issue-5/i5-02.mk i5-02-non-copy-check` | Source/license/principle inventory and reviewer result | Missing inventory/reviewer or derivative prose/asset/layout/style/source |
| `node --test spikes/web/common/tests/*.test.mjs` | Common WEB assertion results | Any applicable WEB failure |
| `make -f mk/issue-5/i5-02.mk web-common-test` | `gate-a/common-tests.json`, test-ID digest | Any WEB failure/missing/duplicate ID |
| `make -f mk/issue-5/i5-02.mk learn-preview LESSON=promotion-trust` | `pass`; URL/PID/fixture digest/label/evidence root; synthetic only | Wrong lesson/host/port/assets/readiness/stale PID/unsafe route |
| `make -f mk/issue-5/i5-02.mk learn-preview-status` | `pass` only when recorded process and semantic readiness match | Down/stale/wrong process/readiness |
| `make -f mk/issue-5/i5-02.mk learn-preview-down` | `pass`; idempotent owned-tree shutdown and retained evidence | Foreign target or owned process survives |
| `python3 -m http.server 4173 --bind 127.0.0.1 --directory spikes/web/preview` | Foreground no-build review fallback; no fitness/score claim | Python/bind/path failure |
| `make -f mk/issue-5/i5-02.mk web-astro-install`<br>`make -f mk/issue-5/i5-02.mk web-next-install`<br>`make -f mk/issue-5/i5-02.mk web-vite-install` | Candidate lock/lifecycle/install/timer evidence | Dirty/mismatched lock, policy/advisory block, install failure, cap/authority breach |
| `make -f mk/issue-5/i5-02.mk web-astro-build`<br>`make -f mk/issue-5/i5-02.mk web-next-build`<br>`make -f mk/issue-5/i5-02.mk web-vite-build` | Frozen mode/build/static semantic manifest | Build/mode/schema/non-semantic/unsafe output failure |
| `make -f mk/issue-5/i5-02.mk web-astro-test`<br>`make -f mk/issue-5/i5-02.mk web-next-test`<br>`make -f mk/issue-5/i5-02.mk web-vite-test` | Candidate-specific plus unchanged common assertion index | Any required unit/schema/static/common failure |
| `make -f mk/issue-5/i5-02.mk web-astro-a11y`<br>`make -f mk/issue-5/i5-02.mk web-next-a11y`<br>`make -f mk/issue-5/i5-02.mk web-vite-a11y` | Automated semantic/axe/reflow/motion/static results; manual status separate | Required browser/tool/assertion missing/failing; cannot mark manual pass |
| `make -f mk/issue-5/i5-02.mk web-astro-e2e`<br>`make -f mk/issue-5/i5-02.mk web-next-e2e`<br>`make -f mk/issue-5/i5-02.mk web-vite-e2e` | Deterministic WEB E2E traces/screenshots for declared fixture | Browser missing, WEB failure, digest/mode drift |
| `make -f mk/issue-5/i5-02.mk web-astro-evidence`<br>`make -f mk/issue-5/i5-02.mk web-next-evidence`<br>`make -f mk/issue-5/i5-02.mk web-vite-evidence` | Complete candidate record + timer + retention index; pre-B is provisional/eliminated | Incomplete/unsafe evidence, illegal score/winner/status |
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
