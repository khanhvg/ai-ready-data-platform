# Acceptance and Test Matrix

## Current Revision

The binding current revision is
[`i5-02-simple-vite-v3`](./simple-vite-acceptance-amendment-v3.md), planned from exact input
`358c305e5988a44ad4261b748aac3ea454c73dad` after the
[owner selected Vite + React](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177).
It passed independent validation with fixes from exact input
`d79ce5638e4a47c5c0963bba1a546448bc0c0ea6`; a fresh simple readiness audit of the published
validation head is the only next phase. V3 replaces all prior v2 blocking/readiness/cook/comparison
scope. The owner selection is unscored, and validation is not implementation readiness.

## V3 Blocking Acceptance Matrix

| ID | Planned source | Exact assertion | Required evidence | Failure/rollback |
|---|---|---|---|---|
| `V3-01` | tracked `spikes/web/candidates/vite/{package.json,package-lock.json}` | Frozen `npm ci --ignore-scripts --no-audit --no-fund`; production build passes; lock SHA-256 remains `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` | install/build logs, exit codes, manifest/lock before-after hashes, dist inventory | Stop; remove owned install/build output; no lock repair/upgrade |
| `V3-02` | `spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs` | Focused Node suite proves four independent named grains, controlled failure, exact conclusion/reason, no attribution, reset baseline, reflection | TAP and discovered test names bound to exact source SHA | Keep valid RED; fix only allow-listed Vite behavior; rerun full gate |
| `V3-03` | `spikes/web/candidates/vite/tests/simple-vite-smoke.spec.mjs` | Sole tagged Chromium journey uses the v3 selector registry for entry → controlled failure → four named grains → `insufficient-evidence` / `no-common-grain` → reset → reflection | one Playwright suite JSON result and bounded trace | No retry/alternate browser; stop and rerun with new run ID after fix |
| `V3-04` | same smoke suite; exactly desktop `1280×800` and narrow `360×800` projects | Same journey in both projects; deterministic keyboard focus style/geometry/hit-test; document/body and named-element overflow assertions at every checkpoint | focus/overflow assertions; failure-only screenshots | Fix focus/layout only; no broad visual matrix |
| `V3-05` | desktop project in same suite | Exactly one `new AxeBuilder({ page }).analyze()` call using frozen `@axe-core/playwright@4.12.1`; zero `critical`, zero `serious`; retain lower impacts | complete axe JSON with counts, URL, exact source SHA | Any Critical/Serious blocks; no rule disable/exclusion/tag claim/impact relabel |
| `V3-06` | desktop-only test creates a real no-JS context; no third project | `browser.newContext({ javaScriptEnabled: false })`, response bytes, and browser DOM/locator parsing preserve four grains, four limitations, exact conclusion/reason, linear order, reset limitation, reflection | no-JS response/body/DOM fact inventory | Restore static HTML facts; interception/rewriting/script removal/invented parser dependency is invalid |
| `V3-07` | `spikes/web/harness/{simple-vite-v3.json,scripts/simple-vite-v3.mjs,tests/simple-vite-v3.test.mjs}` | Exact Issue #6 SHA/blob identities; zero High/Critical npm audit; credential/private-path/PII/injection/CSP/same-origin/storage/evidence checks; owned server/profile cleanup and rollback | audit/scans/ownership/rollback JSON; retained manifest/hash/index | Stop, quarantine raw evidence, signal no foreign PID, clean owned runtime only |

All and only the seven `V3-01..07` rows are blocking test groups. They are conjunctive and
non-scoring; missing/skipped/partial evidence is failure.

## Release Governance Conditions — Not a Test Group

Contemporaneous RED and S3 evidence are outputs of the seven groups. Two prerequisite independent
reviews must pass before ADR-005 becomes Accepted/Vite; the ADR head then receives two fresh
independent exact-head reviews. Any repository-configured PR checks, repository-authorized human
approval of that same head, and pristine post-merge rerun remain release conditions; v3 creates no
CI context. Any post-review commit invalidates the final reports, and recovery uses a normal
reviewed corrective/revert flow. These conditions do not create an eighth test group.

## V3 Four-Grain Invariant

The Node and Chromium suites must agree on exactly:

```text
promotion       promo_name × channel
fulfillment     carrier × region_name
returns         reason × category_name × region_name
data quality    scenario
conclusion      insufficient-evidence
reason          no-common-grain
relationships   none
attribution     none
```

The source files are the four exact Issue #6 tracked handoff paths at integration
`24be3b34c6b0fcdbd07c5800dcab349054e34713`; the SHA-256 and Git-blob pairs in the v3 amendment
must match before any acceptance result is valid.

## V3 Retired Scope and Claim Limit

Firefox/multi-browser work, Next/Astro comparison, score anchors/weights/ties, performance/resource
sampling, timer deadlines, VoiceOver/native zoom/System Settings, broad screenshot matrices, and
production-conformance claims are non-blocking historical context. Timer provenance
`3944.836095708` is preserved but closed/non-binding. V3 claims only the stated Chromium, axe,
keyboard/overflow, no-JS, fixture, S3, cleanup, and rollback results—not full WCAG, screen-reader,
or production-UAT conformance.

## Historical V1/V2 Matrix — Non-Binding for V3

Every row below is retained as discovery and historical test-ID provenance. Its words
`BLOCKS`, scoring rules, browser matrices, timers, manual/native gates, and portal columns do not
define v3 acceptance. Only the v3 matrix above is current.

> `HISTORICAL_NON_BINDING_V1_V2`: no row, `BLOCKS` cell, index, scorecard term, timer value,
> manual/native clause, browser matrix, or portal column below is executable under v3.

### Historical Purpose

Map every issue #7 discovery Critical/High finding and every shared `WEB-*` assertion to planned
owned paths, executable tests, retained evidence, rollback, dependency, and the three distinct
boundaries: early preview acceptance, ADR scoring/winner, and later I5-05 portal cook. The IDs are
immutable test semantics; candidate adapters may not rename or weaken them.

Boundary vocabulary:

- `BLOCKS`: the finding/test must be resolved for that boundary.
- `OPEN-LABELLED`: the neutral preview may run, but only with the permanent synthetic/unscored/
  non-completing label; it is not accepted decision evidence.
- `N/A-LATER`: issue #7 does not implement the later portal/runner behavior, but records a
  compatibility constraint.

For the historical v2 boundary only, `BLOCKS` on browser/accessibility rows meant the corresponding
fresh automated Gate C assertion blocked v2 decision-grade acceptance and scoring—not creation and
retention of the permanently labelled static preview. Actual VoiceOver spoken traversal/Caption
Panel, native Chrome-menu 200%, and the macOS System Settings Reduce Motion toggle were
`deferred-owner-uat`. This paragraph is provenance, not a v3 gate or claim.

### Historical Critical and High Discovery Coverage

Each row is one canonical implementation control. Alias lists cover the web inventory (`WD-*`),
prediction (`PR-*`), scenarios (`SC-*`), and planner-handoff aggregates (`PH-*`).

| Control and all mapped discovery IDs | Owned path(s) | Planned test/evidence | Rollback/removal | Dependency | Historical Preview | Historical ADR | Historical Portal |
|---|---|---|---|---|---|---|---|
| C-01 fixture/provenance: `WD-C01`, `PR-O-C01`, `SC-003`, `SC-012`, `PH-C01` | `spikes/web/harness/fixture-handoff.json`, barrier tests, scorecard JSON | `web-barrier-b-check`; merge SHA + four digests + invalidation log; synthetic score rejection | Remove scores/ADR decision fields; invalidate mixed runs; retain labelled preview | Merged #6 | OPEN-LABELLED | BLOCKS | BLOCKS |
| C-02 grain/causality: `WD-C02`, `PR-A-C01`, `SC-009`, `PH-C02` | Common contracts/tests; preview/candidate four cards | `WEB-CONTRACT-002/003`, `WEB-TRUST-001/002`; DOM/schema/copy/screenshots | Delete composite/join/chart/conclusion and dependent evidence | Existing marts + #6 | BLOCKS | BLOCKS | BLOCKS |
| C-03 completion/browser authority: `WD-C03`, `PR-U-C01`, `SC-005`, `SC-012`, `SC-014`, `PH-C03` | Common state vectors, preview/candidate state adapters | `WEB-PREVIEW-001/002`, `WEB-STATE-001/002`, `WEB-NOSCROLL-001`; tamper trace | Remove completed/mutation/scroll authority; clear scoped stale state; retain preview | Master lesson authority; I5-05 later | BLOCKS | BLOCKS | BLOCKS |
| C-04 unsafe content/credential/privilege: `WD-C04`, `PR-S-C01`, `PR-S-C02`, `SC-002`, `SC-008`, `PH-C04` | Trusted content schemas, bundle/network/CSP scans | Negative hostile strings; `WEB-API-001`; bundle/storage/network and secret canaries | Remove runtime/remote MDX, credential/route/CORS assumption; regenerate/eliminate | Toolchain; future I5-04/I5-05 | BLOCKS | BLOCKS | BLOCKS |
| H-01 candidate comparability/shared edits: `WD-H01`, `PR-A-H01`, `PR-A-H03`, `SC-010`, `PH-H01` | Common logical JSON/tests; candidate adapters only | Contract/test-ID digest equality; changed-path report | Remove fork/workaround/shared edit; reset/eliminate candidate | Gate A + #6 read-only | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-02 accessibility/static/reflow: `WD-H02`, `PR-U-H01`, `PR-U-H02`, `SC-006`, `PH-H02` | Semantic preview/candidates; versioned common a11y projects | `WEB-A11Y-001..004`, `WEB-STATIC-001`; complete Playwright journey, deterministic keyboard/focus/no-trap, axe + semantic/ARIA snapshots, 200%-equivalent/narrow reflow assertions, reduced-motion emulation, no-JS browser + static parser; manual owner UAT tracked separately | Flatten rail/motion; preserve semantic document; withhold automated pass | Fresh equal browser automation; deferred owner UAT before production release | Preview may run; automated acceptance BLOCKS | BLOCKS | BLOCKS |
| H-03 fair measurement/upper bounds: `WD-H03`, `PR-P-H01`, `PR-P-H02`, `PR-P-H03`, `PR-P-H04`, `SC-004`, `SC-013`, `PH-H03` | Measurement harness/raw run evidence | v2: four paired rounds with rotated `V→N`, `N→V`, `V→N`, `N→V` order, producing 4 cold + 4 warm samples per candidate after one discarded warmup; process-tree RSS; build/client manifest; normalized visuals | Invalidate unequal round/category; no retry or partial score; equal full rerun under a new run ID or no winner | Barrier B + frozen host/browser | OPEN-LABELLED | BLOCKS | Decision dependency |
| H-04 timebox/kill/no synthetic score: `WD-H04`, `PR-O-H01`, `SC-013`, `PH-H04` | Timer/kill logs; frozen v1 and additive v2 score-anchor registries; score schema | Preserve historical caps and assert v2 starts with cumulative used `3255.163904292` / remaining `3944.836095708` seconds, no reset; pre-observation v2 anchor digest; eliminated numeric score rejection | Stop at zero, mark `ELIMINATED`/no-winner, retain preview/source/evidence | Candidate protocol + v2 timer contract | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-05 runtime/deployment honesty: `WD-H05`, `PR-A-H02`, `PR-O-H03`, `SC-015`, `PH-H05` | Candidate mode files, start/readiness/shutdown, ECS mapping | Production-like start, artifact hashes, signal/cache/RSS and local rollback evidence | Remove deployment points/score; restore prior static artifact | Frozen modes; later deployment owner | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-06 supply-chain/CSP/evidence sanitation: `WD-H06`, `PR-S-H02`, `PR-S-H03`, `SC-011`, `PH-H06` | Candidate locks, dependency/CSP reports, sanitized evidence | Clean install, lifecycle/provenance/advisory/license, CSP/bundle/credential scans | Remove dependency/config or eliminate; purge/regenerate contaminated evidence | Registry/toolchain/project review | BLOCKS if exploitable | BLOCKS | BLOCKS |
| H-07 ownership/make ambiguity: `WD-H07`, `PR-O-H04`, `PH-H07` | `mk/issue-5/i5-02.mk`, authority/changed-path tests | Issue-local command checks; protected hashes; root Make/.gitignore unchanged | Remove unauthorized path/fragment; use direct spike command | Issue #7 final body authority | Direct preview remains possible | BLOCKS publication if drift | Later root alias handoff |
| H-08 fresh browser and non-copy: `WD-H08`, `WD-H09`, `PR-U-H05`, `PR-O-H05`, `SC-011`, `PH-H08` | `spikes/web/non-copy-inventory.md`, automated browser artifacts, separately retained deferred UAT | `WEB-NONCOPY-001`; fresh screenshots/traces/source reviewer attestation; deferred UAT excluded from automated pass/score | Remove derivative expression; withhold score/ADR | Browser + reviewer | Preview publication BLOCKS non-copy; browser score not claimed | BLOCKS | BLOCKS |
| H-09 novice probes/hints/failure clarity: `WD-H10`, `PR-U-H03`, `PR-U-H04`, `SC-001`, `SC-007`, `PH-H09` | Preview journey content/state/failure vectors | `WEB-FAIL-001`, `WEB-E2E-001`; probe/hint/automated semantic/failure traces | Simplify prose/probes/hints; never lower verifier semantics | Lesson vocabulary | BLOCKS acceptance | BLOCKS | BLOCKS |
| H-10 future BFF/state/evidence tamper compatibility: `PR-S-H01`, `SC-008`, `SC-014`, `PH-H10` | `LabClient`, state/evidence digest tests, S3 disposition | `WEB-API-001`, state tamper/digest binding, empty privileged-route inventory | Remove insecure API/client-authoritative evidence; eliminate candidate | Future I5-04/I5-05 contract | BLOCKS | BLOCKS | N/A-LATER constraint |
| H-11 candidate retention/reproducibility: `PR-O-H02` | Candidate sources/three exact tracked locks and `spikes/web/evidence/retention-index.json` | `web-retention-check`; ignored-lock tracked-state plus source/lock/command/evidence hashes through I5-05 | Restore source from retained bundle; explicitly force-add only exact locks; stop cleanup | I5-05 merge + later cleanup authority | OPEN-LABELLED | BLOCKS handoff | BLOCKS reproducibility |

Coverage inventory (must appear exactly once or in an intentionally cross-cutting row):

- WD: `WD-C01..WD-C04`, `WD-H01..WD-H10`.
- Prediction: `PR-A-C01`, `PR-A-H01..H03`, `PR-S-C01..C02`, `PR-S-H01..H03`,
  `PR-P-H01..H04`, `PR-U-C01`, `PR-U-H01..H05`, `PR-O-C01`, `PR-O-H01..H05`.
- Scenarios: `SC-001..SC-015`.
- Planner handoff: `PH-C01..PH-C04`, `PH-H01..PH-H10`.

### Historical Shared WEB Test Matrix

Planned test sources are under `spikes/web/common/tests/`; candidate-specific tests may verify
framework mode/build details but cannot replace these assertions.

| Test ID | Path/test assertion | Required evidence | Rollback | Dependency | Historical Preview | Historical ADR | Historical Portal |
|---|---|---|---|---|---|---|---|
| `WEB-CONTRACT-001` | `contract-schema.test.mjs`: reject missing/unknown grain, weighting, limitation, evidence, hint, failure fields and executable content | Valid/invalid fixture report + content-schema error locations | Remove unsafe/invalid field/content | Gate A; #6 mirror later | BLOCKS | BLOCKS | BLOCKS |
| `WEB-CONTRACT-002` | `four-grain.test.mjs`: exactly four cards each disclose grain, time, filters, numerator, denominator, weighting, limitations | Schema/DOM snapshot + four normalized screenshots | Restore four independent cards | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-CONTRACT-003` | `four-grain.test.mjs`: no relationship/composite/join/visual edge representing causal cross-mart linkage | Negative schema/DOM/diagram/copy scan | Delete join/composite and dependent evidence | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-PREVIEW-001` | `preview-label.test.mjs`: permanent exact label at entry, rail, verify/evidence, export | Static parser + browser/export snapshots | Restore label; invalidate unlabeled evidence | Synthetic fixture | BLOCKS | Rejects preview score | BLOCKS false authority |
| `WEB-PREVIEW-002` | `preview-authority.test.mjs`: no runner/cloud/completion/mutation/non-static request | Source/route/network/storage inventory | Remove route/state/API | Issue #7 scope | BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATE-001` | `state-navigation.test.mjs`: explicit commit; back/forward/reload restore committed not scroll/transient state | Transition log + URL/storage/browser trace | Remove faulty persistence; restore neutral state | Gate A/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATE-002` | `state-reset.test.mjs`: repeated reset returns the identical resettable-state/baseline digest; visible audit counter increments exactly once per explicit invocation | Before/after/repeat state snapshots | Restore idempotent reset | Gate A | BLOCKS | BLOCKS | BLOCKS |
| `WEB-FAIL-001` | `failure-taxonomy.test.mjs`: controlled/environmental/unexpected have distinct codes/copy/recovery/evidence/progression | Unit/DOM/offline/digest-mismatch trace | Restore separate renderers; stop environmental progression | Gate A/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-TRUST-001` | `four-grain.test.mjs`: naive headline rejected; verifier conclusion exactly `insufficient evidence` | Verifier JSON + conclusion screenshot | Delete invalid conclusion/score | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-TRUST-002` | `four-grain.test.mjs`: forbidden-attribution scan finds no carrier/return/DQ fact assigned to promotion | Source/content/DOM/evidence scan and reviewer record | Remove attribution and every dependent artifact | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-001` | v2 `keyboard.spec.mjs`: all actions/disclosures/navigation work by deterministic keyboard automation with logical/visible focus, Enter/Space parity, reverse traversal, and no trap | Per-action focus/state trace, computed focus visibility, occlusion assertions, checkpoint screenshots | Replace custom widgets/flatten flow in a future separately authorized candidate spike, or eliminate under this frozen-source run | Fresh equal browser automation | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-002` | v2 `semantics.spec.mjs`: landmarks/headings/controls/status/error/live targets and four grain labels/conclusion/reset/reflection match the versioned schema | Axe results plus normalized ARIA snapshots in Chrome and Firefox; VoiceOver UAT status is separate | Restore native semantics in a future separately authorized candidate spike, or eliminate | Fresh equal browser automation | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-003` | v2 `reflow.spec.mjs`: declared 640×400/device-scale-2 200%-equivalent and separate 320px narrow reflow in Chrome and Firefox have no page overflow, target overlap, clipping, offscreen target, occlusion, or hidden focus | Labelled baseline/equivalent/narrow screenshots plus font/raster/bounding-box/scroll/focus assertions; native Chrome-menu zoom remains deferred UAT | Remove fixed/sticky layout in a future separately authorized candidate spike, or eliminate | Fresh equal browser automation | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-004` | v2 `reduced-motion.spec.mjs`: emulated reduced motion preserves the fact/control inventory while removing nonessential motion | Media-emulation trace, computed animation/transition assertions, inventory digest, screenshots; System Settings toggle remains deferred UAT | Disable nonessential motion in a future separately authorized candidate spike, or eliminate | Fresh equal browser automation | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATIC-001` | v2 `no-js.spec.mjs` plus dependency-free static parser: all facts, limitations, four grains, conclusion, reset, reflection, linear review path, and interaction-degradation message remain understandable | Real `javaScriptEnabled: false` response bytes, independent parser result, normalized fact inventory, and JS-disabled screenshots; script interception/removal is rejected | Restore server/static HTML in a future separately authorized candidate spike, or eliminate SPA-only candidate | Build/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-NOSCROLL-001` | `state-navigation.test.mjs`: scroll/hover/animation never commits, verifies, or reveals unique evidence | Event/transition trace and DOM comparison | Remove listener/unique hidden content | Gate A/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-API-001` | `browser-authority.test.mjs`: no credential, runner/private URL, wildcard CORS, direct privileged request | Bundle/source/storage/network/CSP scan | Remove unsafe seam; eliminate | S3/future BFF | BLOCKS | BLOCKS | BLOCKS |
| `WEB-E2E-001` | v2 `journey.spec.mjs`: frame→fail→diagnose→reset→verify→evidence→reflection deterministic and non-completing in preview | Cross-browser trace/screenshots + state/evidence digest | Return to static sequence; fix or eliminate | Browser; #6 for decision run | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-NONCOPY-001` | `non-copy.test.mjs` + reviewer: principles only; no copied prose/assets/layout/style/source | Inventory, file/license/source review, attestation | Remove derivative expression and rebuild | Project reviewer | BLOCKS publication | BLOCKS | BLOCKS |

### Historical Four-Grain Release Invariant

The four-grain rule passes only when all four tests below pass together:

```text
WEB-CONTRACT-002  exactly four independently labelled cards with complete calculation metadata
WEB-CONTRACT-003  zero causal relationship/join/composite representation
WEB-TRUST-001     conclusion is insufficient evidence
WEB-TRUST-002     zero promotion attribution of fulfillment/returns/global-DQ facts
```

Required evidence is the validated logical fixture, semantic DOM snapshot, four normalized card
screenshots, verifier result, source/content/evidence forbidden-attribution scan, and manual
reviewer attestation. Any failure invalidates preview acceptance, the candidate must-pass, its
numeric score, and later portal handoff.

### Historical Evidence and Command Rule

Every historical command recorded exact command/versions/tested tree, Gate 0 and fixture/mode/test-ID
digests, result status, artifacts/hashes/redaction, timer, and rollback result below the historical
`.artifacts/evidence/web-spike/$HISTORICAL_RUN_ID/` template. Required missing tools/evidence exited
non-zero. No
No `not-run-optional` status was valid for a must-pass or historical current-browser automated gate.
The three deferred manual UAT checks used only `pending|pass|fail` in the separate UAT record and
never satisfied or altered an automated result or score.
Before Barrier B, candidate records cover only the explicitly enumerated `foundation` scope and
listed browser/real-fixture checks as required pending `decision` scope. Under historical v2, Gate C
required the revised automated checks, and no score/winner existed until they passed. Deferred
manual UAT did not block the historical Issue #7 stack decision or PR creation, but a
pending/failing UAT record blocked a production-release claim. None of these sentences defines v3.
