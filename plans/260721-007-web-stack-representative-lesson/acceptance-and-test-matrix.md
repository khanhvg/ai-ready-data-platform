# Acceptance and Test Matrix

## Purpose

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

## Critical and High Discovery Coverage

Each row is one canonical implementation control. Alias lists cover the web inventory (`WD-*`),
prediction (`PR-*`), scenarios (`SC-*`), and planner-handoff aggregates (`PH-*`).

| Control and all mapped discovery IDs | Owned path(s) | Planned test/evidence | Rollback/removal | Dependency | Preview | ADR | Portal |
|---|---|---|---|---|---|---|---|
| C-01 fixture/provenance: `WD-C01`, `PR-O-C01`, `SC-003`, `SC-012`, `PH-C01` | `spikes/web/harness/fixture-handoff.json`, barrier tests, scorecard JSON | `web-barrier-b-check`; merge SHA + four digests + invalidation log; synthetic score rejection | Remove scores/ADR decision fields; invalidate mixed runs; retain labelled preview | Merged #6 | OPEN-LABELLED | BLOCKS | BLOCKS |
| C-02 grain/causality: `WD-C02`, `PR-A-C01`, `SC-009`, `PH-C02` | Common contracts/tests; preview/candidate four cards | `WEB-CONTRACT-002/003`, `WEB-TRUST-001/002`; DOM/schema/copy/screenshots | Delete composite/join/chart/conclusion and dependent evidence | Existing marts + #6 | BLOCKS | BLOCKS | BLOCKS |
| C-03 completion/browser authority: `WD-C03`, `PR-U-C01`, `SC-005`, `SC-012`, `SC-014`, `PH-C03` | Common state vectors, preview/candidate state adapters | `WEB-PREVIEW-001/002`, `WEB-STATE-001/002`, `WEB-NOSCROLL-001`; tamper trace | Remove completed/mutation/scroll authority; clear scoped stale state; retain preview | Master lesson authority; I5-05 later | BLOCKS | BLOCKS | BLOCKS |
| C-04 unsafe content/credential/privilege: `WD-C04`, `PR-S-C01`, `PR-S-C02`, `SC-002`, `SC-008`, `PH-C04` | Trusted content schemas, bundle/network/CSP scans | Negative hostile strings; `WEB-API-001`; bundle/storage/network and secret canaries | Remove runtime/remote MDX, credential/route/CORS assumption; regenerate/eliminate | Toolchain; future I5-04/I5-05 | BLOCKS | BLOCKS | BLOCKS |
| H-01 candidate comparability/shared edits: `WD-H01`, `PR-A-H01`, `PR-A-H03`, `SC-010`, `PH-H01` | Common logical JSON/tests; candidate adapters only | Contract/test-ID digest equality; changed-path report | Remove fork/workaround/shared edit; reset/eliminate candidate | Gate A + #6 read-only | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-02 accessibility/static/reflow: `WD-H02`, `PR-U-H01`, `PR-U-H02`, `SC-006`, `PH-H02` | Semantic preview/candidates; common a11y projects | `WEB-A11Y-001..004`, `WEB-STATIC-001`; axe + manual keyboard/AT/zoom/reduced/no-JS | Flatten rail/motion; preserve semantic document; withhold pass | Fresh browser/manual AT | Preview may run; acceptance BLOCKS | BLOCKS | BLOCKS |
| H-03 fair measurement/upper bounds: `WD-H03`, `PR-P-H01`, `PR-P-H02`, `PR-P-H03`, `PR-P-H04`, `SC-004`, `SC-013`, `PH-H03` | Measurement harness/raw run evidence | Rotated 3 cold/3 warm; process-tree RSS; build/client manifest; normalized visuals | Invalidate unequal round/category; equal rerun or no winner | Barrier B + frozen host/browser | OPEN-LABELLED | BLOCKS | Decision dependency |
| H-04 timebox/kill/no synthetic score: `WD-H04`, `PR-O-H01`, `SC-013`, `PH-H04` | Timer/kill logs; frozen score-anchor registry; score schema | 90m, 3h, total 14h assertions; pre-candidate anchor digest; eliminated numeric score rejection | Stop, mark `ELIMINATED`/no-winner, retain preview/source | Candidate protocol | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-05 runtime/deployment honesty: `WD-H05`, `PR-A-H02`, `PR-O-H03`, `SC-015`, `PH-H05` | Candidate mode files, start/readiness/shutdown, ECS mapping | Production-like start, artifact hashes, signal/cache/RSS and local rollback evidence | Remove deployment points/score; restore prior static artifact | Frozen modes; later deployment owner | OPEN-LABELLED | BLOCKS | BLOCKS |
| H-06 supply-chain/CSP/evidence sanitation: `WD-H06`, `PR-S-H02`, `PR-S-H03`, `SC-011`, `PH-H06` | Candidate locks, dependency/CSP reports, sanitized evidence | Clean install, lifecycle/provenance/advisory/license, CSP/bundle/credential scans | Remove dependency/config or eliminate; purge/regenerate contaminated evidence | Registry/toolchain/project review | BLOCKS if exploitable | BLOCKS | BLOCKS |
| H-07 ownership/make ambiguity: `WD-H07`, `PR-O-H04`, `PH-H07` | `mk/issue-5/i5-02.mk`, authority/changed-path tests | Issue-local command checks; protected hashes; root Make/.gitignore unchanged | Remove unauthorized path/fragment; use direct spike command | Issue #7 final body authority | Direct preview remains possible | BLOCKS publication if drift | Later root alias handoff |
| H-08 fresh browser and non-copy: `WD-H08`, `WD-H09`, `PR-U-H05`, `PR-O-H05`, `SC-011`, `PH-H08` | `spikes/web/non-copy-inventory.md`, browser/manual artifacts | `WEB-NONCOPY-001`; fresh screenshots/traces/source reviewer attestation | Remove derivative expression; withhold score/ADR | Browser + reviewer | Preview publication BLOCKS non-copy; browser score not claimed | BLOCKS | BLOCKS |
| H-09 novice probes/hints/failure clarity: `WD-H10`, `PR-U-H03`, `PR-U-H04`, `SC-001`, `SC-007`, `PH-H09` | Preview journey content/state/failure vectors | `WEB-FAIL-001`, `WEB-E2E-001`; probe/hint/AT/failure traces | Simplify prose/probes/hints; never lower verifier semantics | Lesson vocabulary | BLOCKS acceptance | BLOCKS | BLOCKS |
| H-10 future BFF/state/evidence tamper compatibility: `PR-S-H01`, `SC-008`, `SC-014`, `PH-H10` | `LabClient`, state/evidence digest tests, S3 disposition | `WEB-API-001`, state tamper/digest binding, empty privileged-route inventory | Remove insecure API/client-authoritative evidence; eliminate candidate | Future I5-04/I5-05 contract | BLOCKS | BLOCKS | N/A-LATER constraint |
| H-11 candidate retention/reproducibility: `PR-O-H02` | Candidate sources/three exact tracked locks and `spikes/web/evidence/retention-index.json` | `web-retention-check`; ignored-lock tracked-state plus source/lock/command/evidence hashes through I5-05 | Restore source from retained bundle; explicitly force-add only exact locks; stop cleanup | I5-05 merge + later cleanup authority | OPEN-LABELLED | BLOCKS handoff | BLOCKS reproducibility |

Coverage inventory (must appear exactly once or in an intentionally cross-cutting row):

- WD: `WD-C01..WD-C04`, `WD-H01..WD-H10`.
- Prediction: `PR-A-C01`, `PR-A-H01..H03`, `PR-S-C01..C02`, `PR-S-H01..H03`,
  `PR-P-H01..H04`, `PR-U-C01`, `PR-U-H01..H05`, `PR-O-C01`, `PR-O-H01..H05`.
- Scenarios: `SC-001..SC-015`.
- Planner handoff: `PH-C01..PH-C04`, `PH-H01..PH-H10`.

## Shared WEB Test Matrix

Planned test sources are under `spikes/web/common/tests/`; candidate-specific tests may verify
framework mode/build details but cannot replace these assertions.

| Test ID | Path/test assertion | Required evidence | Rollback | Dependency | Preview | ADR | Portal |
|---|---|---|---|---|---|---|---|
| `WEB-CONTRACT-001` | `contract-schema.test.mjs`: reject missing/unknown grain, weighting, limitation, evidence, hint, failure fields and executable content | Valid/invalid fixture report + content-schema error locations | Remove unsafe/invalid field/content | Gate A; #6 mirror later | BLOCKS | BLOCKS | BLOCKS |
| `WEB-CONTRACT-002` | `four-grain.test.mjs`: exactly four cards each disclose grain, time, filters, numerator, denominator, weighting, limitations | Schema/DOM snapshot + four normalized screenshots | Restore four independent cards | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-CONTRACT-003` | `four-grain.test.mjs`: no relationship/composite/join/visual edge representing causal cross-mart linkage | Negative schema/DOM/diagram/copy scan | Delete join/composite and dependent evidence | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-PREVIEW-001` | `preview-label.test.mjs`: permanent exact label at entry, rail, verify/evidence, export | Static parser + browser/export snapshots | Restore label; invalidate unlabeled evidence | Synthetic fixture | BLOCKS | Rejects preview score | BLOCKS false authority |
| `WEB-PREVIEW-002` | `preview-authority.test.mjs`: no runner/cloud/completion/mutation/non-static request | Source/route/network/storage inventory | Remove route/state/API | Issue #7 scope | BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATE-001` | `state-navigation.test.mjs`: explicit commit; back/forward/reload restore committed not scroll/transient state | Transition log + URL/storage/browser trace | Remove faulty persistence; restore neutral state | Gate A/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATE-002` | `state-reset.test.mjs`: duplicate reset returns identical baseline digest and visible count | Before/after/repeat state snapshots | Restore idempotent reset | Gate A | BLOCKS | BLOCKS | BLOCKS |
| `WEB-FAIL-001` | `failure-taxonomy.test.mjs`: controlled/environmental/unexpected have distinct codes/copy/recovery/evidence/progression | Unit/DOM/offline/digest-mismatch trace | Restore separate renderers; stop environmental progression | Gate A/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-TRUST-001` | `four-grain.test.mjs`: naive headline rejected; verifier conclusion exactly `insufficient evidence` | Verifier JSON + conclusion screenshot | Delete invalid conclusion/score | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-TRUST-002` | `four-grain.test.mjs`: forbidden-attribution scan finds no carrier/return/DQ fact assigned to promotion | Source/content/DOM/evidence scan and reviewer record | Remove attribution and every dependent artifact | Existing marts/#6 | BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-001` | `a11y-keyboard.spec.ts`: all actions/disclosures/navigation work by keyboard with logical visible focus | Focus trace + manual keyboard checklist | Replace custom widgets/flatten flow | Fresh browser | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-002` | `a11y-semantics.spec.ts`: landmarks/headings/tables/status/errors form understandable AT order | Aria snapshot + named screen-reader record | Restore native semantics/announcements | Fresh browser/manual AT | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-003` | `a11y-reflow.spec.ts`: 200%/narrow reflow, rail in flow, no content/focus cover or 2D narrative scroll | Reflow screenshots + manual zoom record | Remove fixed/sticky layout | Fresh browser | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-A11Y-004` | `a11y-motion.spec.ts`: reduced motion removes nonessential motion without facts/control loss | Media-emulation trace + manual review | Disable motion/transition | Fresh browser | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-STATIC-001` | `static-facts.test.mjs` and JS-off project: all facts/labels/limitations/linear nav readable | Built HTML parser + JS-off screenshots | Restore server/static HTML; eliminate SPA-only candidate | Build/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-NOSCROLL-001` | `state-navigation.test.mjs`: scroll/hover/animation never commits, verifies, or reveals unique evidence | Event/transition trace and DOM comparison | Remove listener/unique hidden content | Gate A/browser | BLOCKS | BLOCKS | BLOCKS |
| `WEB-API-001` | `browser-authority.test.mjs`: no credential, runner/private URL, wildcard CORS, direct privileged request | Bundle/source/storage/network/CSP scan | Remove unsafe seam; eliminate | S3/future BFF | BLOCKS | BLOCKS | BLOCKS |
| `WEB-E2E-001` | `journey.spec.ts`: frame→fail→diagnose→reset→verify→evidence→reflection deterministic and non-completing in preview | Cross-browser trace/screenshots + state/evidence digest | Return to static sequence; fix or eliminate | Browser; #6 for decision run | Preview acceptance BLOCKS | BLOCKS | BLOCKS |
| `WEB-NONCOPY-001` | `non-copy.test.mjs` + reviewer: principles only; no copied prose/assets/layout/style/source | Inventory, file/license/source review, attestation | Remove derivative expression and rebuild | Project reviewer | BLOCKS publication | BLOCKS | BLOCKS |

## Four-Grain Release Invariant

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

## Evidence and Command Rule

Every planned command records exact command/versions/tested tree, Gate 0 and fixture/mode/test-ID
digests, result status, artifacts/hashes/redaction, timer, and rollback result below
`.artifacts/evidence/web-spike/<run-id>/`. Required missing tools/evidence exit non-zero. No
`not-run-optional` status is valid for a must-pass, current-browser, or manual-accessibility gate.
Before Barrier B, candidate records cover only the explicitly enumerated `foundation` scope and
list browser/manual/real-fixture checks as required pending `decision` scope. This is not a skip or
pass: Gate C must execute them, and no score/winner exists until they pass.
