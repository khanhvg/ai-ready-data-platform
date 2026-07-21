---
title: "Issue #7 Automation-First Acceptance Amendment v2"
issue: 7
phase: fresh-automation-first-acceptance-replan
status: pending-independent-validation
priority: P1
acceptanceRevision: "i5-02-acceptance-v2"
inputSha: "abbcb049b33ee0c6190caedfb5f3ca7fc57b8f59"
integrationBaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
testedOutputCommitSha: "bef2d20f9b1d8029900b88aaea2f9991b0547590"
testedTreeSha: "d990cd5f7e4fff2af74d1cd0d8a2967d8f7aa23b"
retainedAttestationSha: "abbcb049b33ee0c6190caedfb5f3ca7fc57b8f59"
ownerDecisionComment: "https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5035256304"
cumulativeUsedSeconds: "3255.163904292"
remainingSeconds: "3944.836095708"
plannerBoundary: "PLANNER_ONLY_NOT_VALIDATED"
created: "2026-07-21"
---

# Issue #7 Automation-First Acceptance Amendment v2

## Verdict and Planning Boundary

`i5-02-acceptance-v2` is the additive automation-first acceptance contract requested by the Issue
#7 owner. This file is a plan only. It is `PLANNER_ONLY_NOT_VALIDATED`: it does not prove any gate,
authorize implementation, run a browser, alter a candidate, apply a score, select a framework,
change ADR-005, create a PR, approve a merge, merge, or authorize a production release.

The next phase is a fresh independent validation against the exact commit that first contains this
amendment. A fresh readiness audit must follow a passing validation before any implementation or
evidence run. The readiness audit must name the exact full `IMPLEMENTATION_INPUT_SHA`, exact v2
paths, the cumulative timer start, and the single-writer lease.

## Immutable Authority and Provenance

| Authority/input | Binding value | v2 treatment |
|---|---|---|
| Owner acceptance decision | [Issue comment 5035256304](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5035256304) | Supersedes the deep native-OS blocking route; no inference beyond its text |
| Planner input / current retained attestation | `abbcb049b33ee0c6190caedfb5f3ca7fc57b8f59` | Required ancestor; local/tracking/fresh-live equality at planner start |
| Issue #6 integration base | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Required ancestor; four handoff files remain read-only |
| Tested output commit | `bef2d20f9b1d8029900b88aaea2f9991b0547590` | Historical tested output; required ancestor |
| Tested tree | `d990cd5f7e4fff2af74d1cd0d8a2967d8f7aa23b` | Historical test identity; never relabelled as v2 evidence |
| Frozen candidate source/test lineage | `02051ed94d4e2c920f8a65a4ecab0e08a82b946a` | Vite/Next/Astro source, manifests, and modes remain byte-preserved |
| Frozen candidate directory tree | `f2ec341820db157e6bc7fb12e75844ee2730ec12` | Exact `spikes/web/candidates` tree at planner input; v2 may execute but never edit it |
| Score anchors v1 | SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` | Immutable historical anchor; never edited or applied to v2 observations |
| Candidate locks | Astro `78677d1a272fdc5c9758810343f89e82f2914625a03259a575208fe1fafef760`; Next `4939388a7e7290ec640e418afac94dc68cfba7bf6b5692df61317b4c95de2e8b`; Vite `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` | Exact tracked files remain immutable; no regeneration or upgrade |
| Historical timer | used `3255.163904292`; remaining `3944.836095708` of `7200.000000000` seconds | Preserved, additive continuation only, no reset |

The prior partial manual evidence remains retained history. It stays `incomplete`, does not become
an automated pass, and does not satisfy any v2 assertion. Every existing file below
`spikes/web/evidence/retained/**`, the v1 retention index, the v1 score anchors, all three candidate
trees and locks, the four Issue #6 handoff files, and the current ADR/scorecards are read-only until
a later specifically authorized Gate D update. New contracts, runs, indexes, and UAT records use
new versioned paths.

## Exact Supersession and Preservation Ledger

### Superseded blocking clauses only

Where the following documents conflict with this amendment, v2 supersedes only clauses that make
one of these deep native-OS techniques block the Issue #7 stack decision, scoring, downstream
local-sandbox work, or PR creation:

1. full named VoiceOver spoken traversal/Caption Panel evidence;
2. an actual macOS System Settings Reduce Motion toggle; and
3. native Chrome-menu 200% proof.

The superseded locations are the manual-accessibility Gate C wording in `plan.md`,
`acceptance-and-test-matrix.md`, `candidate-protocol.md`, `preview-journey-contract.md`,
`implementation-handoff.md`, `security-s3-disposition.md`, Phases 2–8, and these recovery sections:

- `audit/recovery-readiness-amendment.md` — “Minimum authorized recovery scope” and its manual
  stop conditions;
- `audit/recovery-health-report-supersession-amendment.md` — “Mandatory replacement preflight”,
  “Replacement stop conditions”, and “Preserved recovery and decision boundary” where they
  require native manual facets for the decision;
- `audit/recovery-chromium-preflight-route-amendment.md` — “Current official Chromium contract”
  and “Preserved gates and exclusions” for the same native manual facets;
- `audit/recovery-bounded-foreground-amendment.md` — “Mandatory recovery-cook preflight after
  this amendment”, “Manual Gate C and Gate D remain unchanged”, and matching stop conditions.

Those files remain immutable historical records. No desktop-key, CuaDriver, native Chrome menu,
VoiceOver, Caption Panel, System Settings, TCC, personal profile, Hermes foreground, or OS-mutation
technique audit may resume under v2.

### Still binding without reduction

- Shared semantic/contract tests and a complete Playwright journey.
- Deterministic keyboard-only interaction, logical and visible focus, Enter/Space parity, reverse
  traversal, and no-trap assertions.
- Axe plus normalized semantic/ARIA snapshots for headings, landmarks, controls, status/error/live
  targets, four grain labels, conclusion, reset, and reflection.
- Automated 200%-equivalent and narrow-reflow screenshots plus explicit overflow, overlap,
  occlusion, and focus-visibility assertions.
- `prefers-reduced-motion` emulation with fact/control preservation and removal of nonessential
  motion.
- JavaScript-disabled browser execution plus independent static-response parsing for complete
  comprehension.
- Equal Vite/Next fixture, browser, environment, performance/resource, security, retention,
  rollback, and scoring inputs. Astro stays eliminated.
- Issue #6 contract authority, TDD RED provenance, `security:S3`, non-copy, exact locks, frozen
  source, no-cloud, retention through I5-05, rollback, exact-head independent review, and required
  human pre-merge approval.

### Deferred owner UAT, not decision evidence

The three superseded native checks move to an explicit manual UAT checklist and residual
accessibility risk before production release. A missing or failing item:

- does not add or subtract candidate score;
- does not change an automated gate to pass;
- does not block the Issue #7 local-sandbox stack decision or PR creation;
- does block a production-release sign-off; and
- forbids claims of full WCAG conformance, screen-reader conformance, actual OS Reduce Motion
  validation, or native Chrome-menu 200% validation.

## Outcome, Capabilities, and Requirements

### Business outcomes and capabilities

| ID | Outcome/capability | Acceptance signal |
|---|---|---|
| `BO-01` | Select Vite or Next for continued Vietnamese-first local learning-sandbox development, or retain an honest no-winner | Proposed ADR-005 outcome derived only from complete v2 evidence |
| `BO-02` | Stop spending the critical path on fragile native macOS automation | No native-OS technique is invoked by a blocking Gate C command |
| `CAP-01` | A novice can review the promotion-trust lesson with keyboard, reduced motion, reflow, or JavaScript disabled | Automated journey and static-comprehension contracts pass |
| `CAP-02` | Architecture can compare Vite and Next fairly on a 16GB laptop | Serialized equal inputs, bounded workers, comparable raw performance/resource records |
| `CAP-03` | Reviewers can reproduce why a candidate passed, failed, or was eliminated | Versioned contracts, raw indexes, hashes, exact SHAs, and immutable score derivation |

### Concerns

| ID | Concern | Required control |
|---|---|---|
| `CON-01` | Automated evidence is overstated as manual or full conformance | Claim allow-list and explicit deferred UAT record |
| `CON-02` | Framework preference or run order biases the decision | Frozen v2 anchors, paired AB/BA order, no retry, raw samples |
| `CON-03` | Existing source/evidence is rewritten to fit new gates | Frozen path/tree/hash checks; additive v2 paths only |
| `CON-04` | Missing evidence receives a partial score | Binary must-pass before scoring; null scores on incomplete input |
| `CON-05` | Browser work overloads the 16GB host | One candidate server and one Playwright worker at a time; combined RSS record and cap |
| `CON-06` | Browser/content/evidence introduces S3 exposure | Same-origin/CSP/storage/bundle/credential/redaction/retention scans |

### Functional requirements

- `FR-01`: Validate `i5-02-acceptance-v2` and its digest before any v2 test or evidence run.
- `FR-02`: Execute the complete frame → controlled failure → diagnose → reset → verify → evidence
  → reflection journey in Chromium and Firefox for both Vite and Next.
- `FR-03`: Execute the deterministic keyboard action table below for both candidates with exact
  role/name/state/focus evidence.
- `FR-04`: Run axe and produce normalized semantic/ARIA snapshots at every required checkpoint.
- `FR-05`: Capture labelled 200%-equivalent and 320px narrow screenshots and numeric layout/focus
  assertions without a native zoom claim.
- `FR-06`: Emulate reduced motion, preserve all required facts/controls, and prove nonessential
  animations/transitions are absent.
- `FR-07`: Run a dedicated JavaScript-disabled project and dependency-free static parser for the
  complete comprehension inventory.
- `FR-08`: Record equal fixture/source/lock/browser/environment/order/cache/sample/resource inputs.
- `FR-09`: Run equal S3, retention, rollback, and non-copy checks for Vite and Next.
- `FR-10`: Apply immutable score anchors v2 only after complete must-pass evidence; never edit an
  observed raw input.
- `FR-11`: Generate the manual UAT checklist and residual-risk record without affecting score.
- `FR-12`: Enforce Vietnamese as the primary lesson language (`html[lang="vi"]` and primary
  journey/control copy); English may be a secondary aid only. A frozen candidate that fails is
  eliminated, not edited under this recovery.

### Non-functional requirements

- `NFR-01 Determinism`: retries `0`, Playwright workers `1`, fixed locale `vi-VN` with recorded
  fallback, timezone `Asia/Ho_Chi_Minh`, viewport/device scale, ports, browser versions, fixture
  hashes, and exact ordered actions.
- `NFR-02 Accessibility honesty`: automated scope is named exactly; deferred UAT never appears in
  `automatedPass`, `mustPass`, or numeric score fields.
- `NFR-03 Resource safety`: serialized execution; no Docker; no heavy local profile; combined
  candidate + browser process-tree RSS must remain at or below `4096 MiB` or the comparison stops.
- `NFR-04 Security`: `security:S3`; no credential, private URL, service worker, wildcard CORS,
  external asset, unsafe runtime content, raw header/cookie, PII, or absolute path in retained data.
- `NFR-05 Immutability`: frozen candidates/locks/common/fixture/v1 anchors/prior evidence remain
  unchanged; new evidence is content-addressed and non-self-indexing.
- `NFR-06 Local-first`: loopback only; no cloud, AWS, Docker, Terraform, publisher, signing, or
  release operation.
- `NFR-07 Time`: the exact remaining cumulative budget is authoritative and cannot reset.
- `NFR-08 Dependency floor`: use only the frozen candidate toolchains, already locked Playwright
  authority, repository utilities, and Node built-ins; introduce no framework, package, lockfile
  change, browser channel, or service unless a fresh owner decision makes it explicitly required.

## Architecture and Exact Future File Boundary

### Data flow

```text
frozen Vite/Next bytes + Issue #6 fixture + i5-02-acceptance-v2
  -> v2 authority and contract validators
  -> one serialized candidate host
  -> shared Playwright v2 project matrix + static-response parser
  -> normalized per-candidate evidence
  -> equal comparability/security/resource/rollback gates
  -> immutable score-anchors-v2 derivation
  -> Proposed ADR-005 winner/no-winner + deferred-UAT residual risk
  -> two independent exact-head reviews
  -> PR -> exact-head human approval -> merge -> pristine verification
```

### Create after RED

| Path | Purpose |
|---|---|
| `spikes/web/harness/contracts/acceptance-contract-v2.json` | Machine binding for this revision, claims, projects, facts, timer, equality, and state transitions |
| `spikes/web/harness/contracts/gate-c-evidence-v2.schema.json` | Reject incomplete/unequal/overclaimed automated evidence |
| `spikes/web/harness/contracts/semantic-snapshot-v2.schema.json` | Normalize checkpoint roles/names/states/relationships |
| `spikes/web/harness/contracts/manual-uat-v1.schema.json` | Keep deferred UAT outside automation and scoring |
| `spikes/web/harness/authority-v2.json` | New implementation input, immutable identities, exact allow/deny paths |
| `spikes/web/harness/stage-status-v2.json` | Explicit validation/audit/cook/Gate C/Gate D/UAT/release states |
| `spikes/web/harness/score-anchors-v2.json` | Frozen automated-only 0..5 anchors and original weights |
| `spikes/web/harness/playwright.config.mjs` | Serialized project matrix, zero retries, common environment |
| `spikes/web/harness/playwright/candidate-fixture.mjs` | Candidate/base URL binding, normalized checkpoints, evidence writer |
| `spikes/web/harness/playwright/journey.spec.mjs` | Complete journey in Chromium and Firefox |
| `spikes/web/harness/playwright/keyboard.spec.mjs` | Keyboard table, parity, focus, and no-trap assertions |
| `spikes/web/harness/playwright/semantics.spec.mjs` | Axe and semantic/ARIA snapshots |
| `spikes/web/harness/playwright/reflow.spec.mjs` | 200%-equivalent/narrow screenshots and geometry assertions |
| `spikes/web/harness/playwright/reduced-motion.spec.mjs` | Media emulation, inventory equality, animation assertions |
| `spikes/web/harness/playwright/no-js.spec.mjs` | JavaScript-disabled comprehension and screenshots |
| `spikes/web/harness/scripts/static-html-parser-v2.mjs` | Dependency-free tokenizer/parser for saved response bytes |
| `spikes/web/harness/scripts/gate-c-run-v2.mjs` | Equal Vite/Next orchestration, environment, samples, hashes, cleanup |
| `spikes/web/harness/scripts/decision-v2.mjs` | Must-pass, anchors, tie/no-winner, claim and UAT separation |
| `spikes/web/harness/scripts/retention-v2.mjs` | Parent-bound additive retention index and redaction checks |
| `spikes/web/harness/scripts/rollback-v2.mjs` | Exact owned runtime cleanup and prior-state proof |

### Create tests first

| Path | Required RED coverage |
|---|---|
| `spikes/web/harness/tests/acceptance-contract-v2.test.mjs` | Missing/wrong revision, hash, project, claim, timer, frozen identity |
| `spikes/web/harness/tests/semantic-snapshot-v2.test.mjs` | Missing/duplicate role/name/checkpoint/four-grain/status/error/live target |
| `spikes/web/harness/tests/static-comprehension-v2.test.mjs` | Script-only facts, missing limitations/grain/conclusion/reset/reflection/path, malformed HTML |
| `spikes/web/harness/tests/comparability-v2.test.mjs` | Unequal fixture/browser/order/cache/warmup/sample/resource/security input |
| `spikes/web/harness/tests/decision-v2.test.mjs` | Missing gate, eliminated score, post-run anchor edit, tie, Astro, UAT-score leakage |
| `spikes/web/harness/tests/retention-v2.test.mjs` | v1 rewrite, self-indexing, missing artifact, unsafe path/field, bad parent digest |
| `spikes/web/harness/tests/manual-uat-v1.test.mjs` | Only pending/pass/fail, human sign-off semantics, forbidden conformance claims |

### Modify only after the RED record exists

| Path | Additive change |
|---|---|
| `spikes/web/harness/test-ids.json` | Do not edit v1; instead reference the v1 digest from `acceptance-contract-v2.json` and use new v2 IDs in that file |
| `mk/issue-5/i5-02.mk` | Add explicit `*-v2` targets; preserve old targets for historical reproduction |
| `docs/decisions/0005-web-stack.md` | Gate D only: keep `Proposed`, record v2 outcome and residual risk |
| `docs/decisions/evidence/adr-0005-web-stack-scorecard.{md,json}` | Gate D only: derive from v2 indexes; no hand-edited observation |

Generated evidence uses `.artifacts/evidence/web-spike/<run-id>/{tdd,gate-c-v2,gate-d-v2}/**`
and `.artifacts/runtime/i5-02/<run-id>/**`; it is never staged. Sanitized evidence is added only
under `spikes/web/evidence/retained/gate-c-v2/<run-id>/**` and
`spikes/web/evidence/retained/gate-d-v2/<run-id>/**`. The new
`spikes/web/evidence/retention-index-v2.json` records the SHA-256 of the immutable v1 retention
index as its parent and indexes only new or explicitly inherited artifacts without rewriting v1.

### Immutable implementation inputs

Do not modify `spikes/web/candidates/**`, any candidate `package-lock.json`, `spikes/web/common/**`,
`spikes/web/preview/**`, `spikes/web/harness/score-anchors.json`, any existing retained-evidence
path, `spikes/web/evidence/retention-index.json`, the four Issue #6 handoff files, root `Makefile`,
`.gitignore`, release manifest, portal/runner paths, Issue #8+, Docker, AWS, or Terraform. A v2
assertion failure caused by frozen candidate behavior eliminates that candidate; it does not grant
source-fix authority or extra time.

## Tests-First Execution Plan

### Phase 0 — Fresh independent plan gates

1. Fresh validator fetches and proves local/tracking/live equality to the exact planner output.
2. Validator evaluates feasibility, completeness, contradiction, timer, claims, and file authority;
   it does not implement.
3. On validation PASS, change only the workflow label to `ready for plan audit`.
4. Fresh readiness auditor independently rechecks authority, frozen hashes, timer, single-writer
   lease, exact v2 paths, S3/TDD, and rollback; it names the sole implementation input.
5. Only readiness PASS changes the workflow label to `ready to cook`.

Any correction produces a new planner output and requires fresh validation. This planner does not
perform either gate.

### Phase 1 — RED contract and provenance

1. Start the additive timer immediately before the first v2 implementation/test write or timed
   implementation command, whichever occurs first.
2. Add only the seven v2 unit test files and inert invalid test fixtures. Record a binary-safe,
   sorted whole-tree pre-RED manifest, its SHA-256, exact input SHA, monotonic/UTC timer boundary,
   and path list before execution.
3. Run separately and retain full TAP/exit status:

```bash
node --test spikes/web/harness/tests/acceptance-contract-v2.test.mjs
node --test spikes/web/harness/tests/semantic-snapshot-v2.test.mjs
node --test spikes/web/harness/tests/static-comprehension-v2.test.mjs
node --test spikes/web/harness/tests/comparability-v2.test.mjs
node --test spikes/web/harness/tests/decision-v2.test.mjs
node --test spikes/web/harness/tests/retention-v2.test.mjs
node --test spikes/web/harness/tests/manual-uat-v1.test.mjs
```

4. Expected RED is non-zero for absent v2 contracts/scripts, with every planned assertion executed.
   Syntax errors, missing test discovery, skipped/todo assertions, weakened v1 semantics, or a
   candidate/source edit are invalid RED and stop the run.
5. Retain sanitized RED provenance at
   `spikes/web/evidence/retained/gate-c-v2/<run-id>/tdd/red/**` only after GREEN confirms the
   intended failures.

### Phase 2 — GREEN automation harness

1. Add the versioned contracts, anchors, authority/status files, Playwright config/fixture/specs,
   parser, orchestrator, decision, retention, and rollback scripts in small slices.
2. Make each unit suite green before enabling its `mk/issue-5/i5-02.mk` v2 target.
3. Run the existing shared/candidate tests without changing expected results:

```bash
node --test spikes/web/common/tests/*.test.mjs
node --test spikes/web/candidates/vite/tests/*.test.mjs
node --test spikes/web/candidates/next/tests/*.test.mjs
node --test spikes/web/harness/tests/*.test.mjs
make -f mk/issue-5/i5-02.mk web-acceptance-v2-check IMPLEMENTATION_INPUT_SHA=<authorized-sha>
```

4. Create the source/test commit before decision evidence. Record its full SHA as
   `TESTED_SOURCE_SHA`; require its candidate/common/fixture/lock/v1-evidence trees to match the
   frozen identities.

### Phase 3 — Equal automated Gate C v2

Future top-level command:

```bash
make -f mk/issue-5/i5-02.mk web-gate-c-v2 \
  IMPLEMENTATION_INPUT_SHA=<authorized-sha> \
  I5_01_MERGE_SHA=24be3b34c6b0fcdbd07c5800dcab349054e34713
```

It must execute, in order:

1. v2 authority, frozen-hash, Barrier B, timer, S3, credential, non-copy, and port checks;
2. exact-lock `npm ci --ignore-scripts --no-audit --no-fund` for Vite then Next, without changing
   locks; separate `npm audit --json` records, no `audit fix`;
3. clean candidate tests/builds and static-response parser;
4. the shared Playwright project matrix for Vite and Next with the same installed harness/browser;
5. paired performance/resource and disposable authoring measurements;
6. equal security, retention, rollback, and cleanup checks; and
7. a complete or fail-closed v2 index. No step may invoke a native OS/manual technique.

### Phase 4 — Gate D v2, UAT risk, and retained attestation

1. Validate every must-pass/equality/raw input before scoring.
2. Apply `score-anchors-v2.json` by digest; do not mutate raw evidence or anchors.
3. Emit either candidate totals plus a Proposed winner, or explicit `no-winner` and null scores.
4. Generate the deferred UAT checklist and residual-risk JSON at the paths below.
5. Update ADR/scorecards only from the verified Gate D index. ADR stays `Proposed`.
6. Write `retention-index-v2.json`, reproduce the proposed winner or retained no-winner path,
   execute rollback v2, remove only owned transient state, and create the retained attestation
   commit.
7. Re-run non-browser tests/checkers at the retained attestation head. Browser evidence remains
   bound to `TESTED_SOURCE_SHA`; prove the candidate/common/fixture/lock/harness source tree is
   identical between tested source and retained head.

### Phase 5 — Review, PR, approval, merge, and pristine verification

1. Two fresh independent read-only reviewers inspect the same exact retained head:
   - reviewer A: TDD, code/harness, S3, frozen paths, resource/rollback;
   - reviewer B: acceptance v2, browser/static evidence, equality, scoring, claims, UAT risk.
2. Each report names the exact 40-hex reviewed SHA, tested source SHA/tree, v2 contract/anchor/
   retention digests, findings, and `PASS|FAIL`. A change after review invalidates both reports.
3. PR creation is allowed only after both reviews pass and all revised automated/scoring gates pass.
   The PR may carry deferred UAT as pending residual risk.
4. PR merge remains blocked until a repository-authorized human reviews the final exact PR head and
   records explicit approval naming that SHA. Standing auto-approval, the owner planning comment,
   an agent, a score, or a label cannot synthesize this approval.
5. After merge, fetch the merge commit into a pristine temporary worktree and rerun authority,
   shared/unit/v2 contract, clean build, Gate C v2 reproduction, S3, retention, and rollback checks.
   Do not release while deferred UAT is pending/failing. Remove the temporary worktree only after
   recorded clean verification.

## Playwright Project Contract

`spikes/web/harness/playwright.config.mjs` uses `workers: 1`, `retries: 0`,
`fullyParallel: false`, `repeatEach: 1`, traces/screenshots retained on first failure plus required
checkpoints, locale `vi-VN`, timezone `Asia/Ho_Chi_Minh`, device scale `1`, and a fresh browser
context per project. The exact projects are:

| Project | Engine/use | Required specs/claim |
|---|---|---|
| `journey-chromium` | installed stable Chrome channel, `1280x800`, JS on | complete journey, axe, semantic snapshots, network/storage/CSP |
| `journey-firefox` | frozen Playwright Firefox, `1280x800`, JS on | same complete journey, axe, semantic snapshots |
| `keyboard-chromium` | stable Chrome, `1280x800`, JS on | action table, visible focus, parity, no trap |
| `keyboard-firefox` | Firefox, `1280x800`, JS on | identical action table and parity |
| `reflow-200-equivalent-chromium` | Chrome, `640x400`, JS on | CSS-viewport 200%-equivalent only; never native zoom |
| `reflow-narrow-chromium` | Chrome, `320x800`, JS on | narrow linear reflow and focus visibility |
| `reduced-motion-chromium` | Chrome, `1280x800`, `reducedMotion: reduce` | facts/controls unchanged; nonessential motion removed |
| `no-js-chromium` | Chrome, `1280x800`, `javaScriptEnabled: false` | complete comprehension plus saved response/parser |

The config is parameterized only by validated `I5_02_CANDIDATE`, `I5_02_BASE_URL`, `I5_02_RUN_ID`,
and evidence root. The orchestrator supplies exactly `vite` and `next`. An unknown candidate,
different project list, extra browser, retry, parallel worker, changed locale/timezone/viewport,
or missing output is non-zero.

## Deterministic Keyboard Action Table

Each row runs from a fresh context for both Vite and Next in both keyboard projects. Focus evidence
records step, key, active element role/name/state, URL/hash, status text, target rectangle,
viewport, computed outline/box-shadow/contrast inputs, occlusion result, and screenshot digest.

| Step | Action | Required result |
|---|---|---|
| `K-01` | Load and press `Tab` | First reachable interactive item receives one unique logical focus; no scripted focus theft |
| `K-02` | Continue `Tab` through the ordered `Lesson acts` links | Accessible names and order match source/narrative order; each focus indicator is visible and unobscured |
| `K-03` | `Enter` on each act link from a fresh state | URL fragment and visible target change deterministically; no verification/completion state changes |
| `K-04` | `Shift+Tab` through the same sequence | Exact reverse order; no skipped or newly injected control |
| `K-05` | Focus `Run bounded probe`; activate with `Enter` | Controlled-failure status appears, focus remains logical, no completion/score/storage mutation |
| `K-06` | Fresh state; activate `Run bounded probe` with `Space` | Normalized state/status digest equals `K-05` |
| `K-07` | Focus `Reset`; activate independently with `Enter` and `Space` | Each route returns the same baseline status/digest; focus stays on Reset; repeated reset is idempotent |
| `K-08` | Focus `Fixture digest facts`; activate with `Enter` and `Space` | Disclosure open/closed states and accessible state are equivalent; focus stays on summary |
| `K-09` | Press `Escape`, then `Tab`, from each custom/disclosure/control state | Escape never strands focus; next expected target is reachable |
| `K-10` | Traverse until the final tabbable plus two bounded steps | No element repeats unexpectedly, no page-owned focus loop, and focus exits/returns according to browser default |
| `K-11` | Compare keyboard activation with Playwright `click()` in separate clean contexts | Normalized URL, state, status, evidence, and storage digests match; click is parity evidence, not keyboard evidence |

Visible focus requires a nontransparent indicator at least `2 CSS px` thick or an equivalent
area, contrast at least `3:1` against adjacent colors, a positive in-viewport rectangle, and
`elementFromPoint` at center/corners resolving to the target or its descendant. No fixed/sticky
element may cover it. A repeated active element after a navigation key, hidden focus, body-only
focus before the sequence completes, unexpected DOM insertion, or more than
`tabbableCount + 2` steps is a no-trap failure.

## Semantic/ARIA Snapshot Contract

Every normalized record contains:

```text
schemaVersion=i5-02-semantic-snapshot-v2
acceptanceRevision=i5-02-acceptance-v2
candidate, project, checkpoint, testedSourceSha, testedTreeSha
fixture/contract/common/source/lock/browser/anchor digests
roles[]: role, accessibleName, level/state/value, sourceOrder, relationship target
axe[]: rule, impact, target, help URL (no page secret/header data)
factInventoryDigest, controlInventoryDigest, snapshotDigest
```

Required checkpoints are `entry`, `controlled-failure`, `diagnosis`, `reset`, `verify`,
`evidence`, and `reflection`. Each checkpoint schema rejects missing, duplicate, unnamed, hidden,
or out-of-order targets. The required target inventory is:

- landmarks: `banner`, `main`, `navigation` named `Lesson acts`, and `contentinfo`;
- headings: one decision-question `h1`, ten ordered act `h2` headings, and four evidence `h3`
  headings;
- controls: all ten act links, `Run bounded probe`, `Reset`, and `Fixture digest facts`, including
  expanded/pressed/current/disabled state where applicable;
- status/live: initial, controlled-failure, and reset status text with the computed live behavior;
- error target: the unique controlled-failure explanation, its containing act heading, visible
  non-color cue, and any status/description relationship; no alert role is invented if absent;
- grain labels: `mart_promotion_effectiveness — promo_name, channel`,
  `mart_fulfillment_performance — carrier, region_name`,
  `mart_returns_analysis — reason, category_name, region_name`, and
  `mart_data_quality — scenario`;
- conclusion: `insufficient-evidence` with reason `no-common-grain`;
- reset: control, baseline/status result, and non-completion invariant; and
- reflection: the Act 10 heading, reflection/review text, and reachable reset/review controls.

Axe runs WCAG 2 A/AA, 2.1 A/AA, and 2.2 AA tags in both journey engines. Axe is necessary but
not sufficient; a zero-violation result cannot replace any snapshot, focus, reflow, motion,
static, or deferred-UAT record.

## Reflow, Reduced Motion, and No-JS Contracts

### Reflow and false-claim prevention

For both surviving candidates, capture entry, controlled failure, four-grain evidence,
conclusion, reset, and reflection at `640x400` and `320x800`. For every screenshot assert:

- document `scrollWidth <= clientWidth + 1`; a code block may scroll internally but cannot expand
  the page;
- required target rectangles do not overlap each other, leave the document bounds, or intersect a
  fixed/sticky overlay;
- every focused control is fully visible after native focus scrolling and passes the focus
  occlusion test;
- source/narrative order remains linear and no two-dimensional narrative scroll is needed; and
- full-page and viewport screenshot byte hashes are retained.

The evidence record must say:

```text
evidenceKind=css-viewport-200-percent-equivalent
nativeChromeMenuZoomPerformed=false
nativeChromeMenuZoomStatus=deferred-owner-uat
```

“Chrome zoom 200% passed”, “native zoom verified”, or equivalent wording is rejected.

### Reduced motion

Compare a no-preference context with `prefers-reduced-motion: reduce`. Require equal required fact
and control inventory digests, equal journey outcomes, `matchMedia` true, no running nonessential
Web Animations, computed animation duration `0s`/name `none`, transition duration `0s`, and scroll
behavior `auto` for all required targets. Retain screenshots and computed-style records. Evidence
must say `actualSystemSettingsTogglePerformed=false` and `manualUatStatus=pending`; it cannot claim
actual macOS Reduce Motion validation.

### JavaScript-disabled complete comprehension

The `no-js-chromium` project saves the original response bytes before DOM normalization. The
dependency-free static parser and the browser DOM must independently find, in source order:

1. Vietnamese primary language and the permanent non-completion/fixture label;
2. stakeholder/decision question and evidence threshold;
3. controlled failure, explanation, and safe next action;
4. all four exact grain labels, their time/filter/numerator/denominator/weighting/limitation facts;
5. no cross-grain join or promotion-causality claim;
6. conclusion `insufficient-evidence` and reason `no-common-grain`;
7. reset scope/oracle and non-mutation statement;
8. reflection prompt and local-to-hosted limitations without a cloud prerequisite; and
9. a source-ordered linear review path covering all ten acts with reachable native links/controls.

“Complete comprehension” means every item is visible/readable without executing script; no
placeholder, empty mount, `noscript` warning, CSS-generated unique fact, or hidden scripted text
counts. All facts and review controls remain. Browser and parser inventories must have the same
digest. A Vite or Next failure eliminates that frozen candidate. The record says
`manualNoJsUatPerformed=false`; it makes only an automated JS-disabled/static-parser claim.

## Equal Vite/Next Run and Measurement Contract

### Candidate treatment

- Vite and Next receive exactly the same v2 contracts, fixture bytes, browser projects, action
  tables, environment values, security checks, measurement definitions, sample counts, score
  anchors, retention rules, rollback, and time boundary.
- Astro remains `ELIMINATED`, `numericScore: null`, for the retained Chrome/Firefox target-size
  failures. It is not installed, built, launched, rerun, repaired, sampled, scored, or used to
  consume budget. Only its immutable disposition and evidence hashes appear in v2 indexes.
- A deterministic candidate behavior failure eliminates that candidate. A harness, tool, fixture,
  browser, environment, or equality failure invalidates the whole comparison and yields no scores.

### Order, warmup, samples, cache, and retry

| Control | Exact value |
|---|---|
| Browser/test retries | `0` |
| Playwright workers | `1` |
| Candidate concurrency | `1` server, `1` browser context at a time |
| Warmup | `1` discarded build/start/journey warmup per candidate, order Vite → Next |
| Measured paired rounds | `4`: Vite→Next, Next→Vite, Vite→Next, Next→Vite |
| Samples per candidate | `4` cold starts and `4` warm starts; RSS at readiness and post-journey for each |
| Invalid sample | Invalidate its entire Vite/Next paired round; retry count remains `0`; comparison becomes no-winner |
| Port | sequential fixed `4175`; stop if occupied, never scan or auto-select |

Each candidate gets a candidate/sample-scoped runtime root. Clean install starts from absent
`node_modules` using the immutable lock. Build output is created once from the frozen source.
Each cold sample uses a fresh validated copy of the built runtime with only declared runtime cache
absent; each warm sample restarts the same sample copy without clearing cache. Vite uses the common
static host; Next uses its frozen standalone server. Both use the same semantic readiness text and
timeout. No dev server or `vite preview` is evidence.

### Frozen environment record

Record OS/kernel/architecture, CPU model/logical count, physical memory, Node/npm, exact Playwright
and browser versions, candidate Git tree/package/lock/mode hashes, Issue #6 four-file hashes,
common/test-ID/v2 contract/v2 anchor hashes, locale/timezone/fonts, viewport/device scale, motion/
JS state, fixed port, start/readiness/stop commands, order, warmup/sample/retry/worker counts,
background load averages, free memory, and process-tree sampling method. Record an allow-listed
environment object, never a full environment dump.

### Performance/resource and authoring measurements

- Startup uses monotonic time from owned process spawn to identical semantic HTTP readiness.
- RSS sums the owned candidate server/static-host process tree at readiness and after the complete
  journey. Browser RSS is recorded separately. Combined candidate/browser RSS over `4096 MiB`
  stops the comparison.
- Client/build records raw, gzip, and brotli bytes by emitted asset; initial-route JS,
  interactive/lazy JS, browser transfer, source-map policy, and total artifact size are separate.
- The authoring task uses a disposable candidate source copy under `.artifacts/runtime`, never the
  tracked tree: add one Vietnamese explanation callout, one limitation field, one prerequisite
  probe, and one hint; then remove the required limitation and capture the deterministic error.
  Record monotonic build/validation time, files and nonblank lines touched, error path/field/line,
  hot-reload/build result, and framework glue. Delete only the validated disposable copy after
  its hash-indexed evidence is retained.

### Equal S3, retention, and rollback inputs

For each candidate run identical exact-lock/lifecycle/advisory/license/provenance checks, CSP and
route inventory, same-origin request allow-list, empty cookie/local/session/IndexedDB authority,
bundle/source-map credential/private-URL/absolute-path scans, unsafe-content fixtures, non-copy
checks, evidence redaction, and hash indexing. No `npm audit fix`, upgrade, dependency substitution,
remote content, external font/CDN, service worker, wildcard CORS, credential, or private endpoint.

Rollback stops only the exact owned PID/process group after PID/start-fingerprint/command/cwd/port/
run-ID checks, proves port `4175` free, removes only validated candidate/sample runtime roots and
transient `.artifacts`, retains all v1 and v2 evidence, and proves frozen paths unchanged. A
foreign listener or ownership mismatch is reported and never signalled.

## Score Anchors v2 and Decision Rule

Create and digest-freeze `score-anchors-v2.json` before any v2 candidate observation. It copies
the original category weights exactly and uses only predeclared automated/raw predicates. For each
category, anchor is the greatest consecutive level `0..5` whose predicates all pass; no
interpolation or candidate-relative threshold is allowed.

| Category | Weight | Fixed consecutive v2 predicates for levels 1 → 5 |
|---|---:|---|
| Authoring/content schema | 20 | task validates; deterministic missing-field error; ≤6 files/80 nonblank lines and ≤15m; ≤4/50 and ≤10m; ≤3/30 and ≤5m with exact field/line and no framework workaround |
| Automated accessibility/static/motion | 20 | required semantic inventory; axe in both engines; both keyboard tables; both reflow modes + reduced motion; no-JS browser/parser and every v2 accessibility gate pass |
| Lab state/evidence/typed API | 20 | read-only seam; explicit state/reset; fixture-bound evidence; navigation/tamper/digest tests; all authority/non-completion/API predicates pass |
| Startup/RSS/client JS | 15 | valid complete samples; cold≤2000ms/warm≤1000ms/RSS≤512MiB/initial gzip JS≤500KiB; ≤1000/500/384/300; ≤500/250/256/200; ≤250/125/192/120 (all medians, all bounds) |
| Unit/E2E/visual evidence | 10 | unit/shared pass; Chromium journey pass; Firefox journey pass; all required screenshots/traces present; every hash/schema/retention check passes |
| Hosted evolution/rollback | 10 | frozen production-like mode; loopback readiness; exact signal/cache behavior; documented typed local→hosted seam with no cloud execution; reproduction and bounded rollback pass |
| Maintenance/dependency/supply chain | 5 | exact tracked lock; clean install/lifecycle inventory; provenance/license/audit records; zero critical/high and at most two moderate advisories; zero unresolved advisories and all supply-chain predicates pass |

The numeric points are `weight * anchor / 5`; weights total 100. Raw thresholds use milliseconds,
active authoring minutes (`m`), MiB (`1024^2` bytes), and gzip KiB (`1024` bytes). A blocking
must-pass failure yields
`ELIMINATED` and `numericScore: null`; missing/unequal comparison evidence yields
`INCOMPLETE_AUTOMATED` for affected candidates and no scores at all.

Highest complete passing total wins only when the difference is greater than five points. The
original within-five Astro default remains semantically preserved but unavailable because Astro is
eliminated and cannot be reopened. Therefore a Vite/Next difference of five points or less yields
`NO_WINNER_TIE_OWNER_DECISION_REQUIRED`; the runner does not invent a new preference. Deferred
manual UAT is stored outside every anchor and total, so it cannot skew Vite/Next equality.

Once a candidate run begins, v2 anchors and all observed score inputs are immutable. A correction
requires a version v3 contract and a full equal rerun; editing an observed result, threshold,
predicate, timer, sample, disposition, or score in place is a hard failure.

## Timer Contract: Same Budget, No Reset

The owner decision does not grant a timer reset. The sole current values are:

```text
budgetSeconds=7200.000000000
cumulativeUsedSeconds=3255.163904292
remainingSeconds=3944.836095708
```

Planning, fresh independent validation, fresh readiness audit, scheduler serialization wait, and
read-only Git/preflight checks do not consume this active implementation budget and create no
credit. The additive v2 segment starts immediately before the first implementation/test write or
timed implementation command. It includes v2 RED capture/execution, harness/contracts, installs,
builds, browser/static runs, fixes to v2-owned harness/tests only, measurements, scoring,
ADR/scorecard/UAT/retention generation, reproduction, and rollback. It ends when Gate D v2 closes
or the remainder reaches zero.

No retroactive pause, refund, replacement, reset, or extra candidate time is allowed. Only a
documented external registry/browser outage or a required new owner decision may create a
prospective pause under the existing policy; no pause is planned. Independent review, PR wait,
human approval wait, and pristine post-merge verification create no score/timer credit and cannot
reopen a closed Gate D run. At expiry, stop, retain evidence, keep ADR-005 Proposed, and emit
no-winner/null scores.

## Manual UAT and Residual Accessibility Risk

Create after Gate D evidence derivation:

```text
spikes/web/evidence/retained/gate-d-v2/<run-id>/manual-uat-checklist-v1.md
spikes/web/evidence/retained/gate-d-v2/<run-id>/residual-accessibility-risk-v1.json
```

The checklist contains exactly these release checks for the proposed winner/build:

1. named VoiceOver + browser + macOS spoken traversal with Caption Panel evidence;
2. actual macOS System Settings Reduce Motion toggle, observed behavior, and exact restoration;
3. native Chrome-menu 200% proof, reflow/comprehension, and exact restoration.

Each item has `pending|pass|fail`, candidate, exact build/tested SHA, OS/browser/AT versions,
human reviewer identity, timestamp, safe artifact hashes, observation, restoration, and follow-up.
No agent fills human fields. Owner release sign-off requires all three `pass` plus an explicit
human statement naming the exact production candidate/build SHA. `pending` or `fail` blocks only
production release and opens a follow-up risk/fix; it does not retroactively change the Issue #7
score or automated result.

Every ADR, scorecard, issue comment, PR, and handoff must use this non-claim language while UAT is
not fully passed:

> Automated acceptance passed under `i5-02-acceptance-v2`; manual VoiceOver, actual macOS Reduce
> Motion, and native Chrome-menu 200% UAT remain pending residual accessibility risk. This is not
> a claim of full WCAG or screen-reader conformance.

The v2 decision checker rejects “WCAG compliant”, “screen-reader compliant”, “manual AT passed”,
“native 200% passed”, “System Settings Reduce Motion passed”, or equivalent text unless the exact
human UAT record supports that narrow statement. Even completed UAT does not create a general full
WCAG conformance claim without separate conformance scope and audit.

## ADR-005, Review, Merge, and Rollback Rules

- ADR-005 remains `Proposed` during planning, validation, audit, implementation, scoring, review,
  PR, and merge preparation. Automation never writes `Accepted`.
- A Proposed winner requires complete revised automated gates, comparable raw samples, v2 score,
  S3/retention/rollback, and both independent exact-head reviews. The ADR includes the deferred UAT
  checklist/residual risk. Otherwise it remains Proposed/no-winner.
- Both independent reviews and all evidence must bind the exact final head. Any post-review change
  invalidates reviews; any harness/test/anchor/raw-evidence/source change also invalidates affected
  runs and may require a full rerun.
- PR creation is allowed after the automated decision and reviews. PR merge is still blocked by
  explicit human approval of the exact final PR head. Standing auto-approval may advance safe
  plan/validation/audit/cook/review phases but cannot impersonate this human gate.
- Pristine post-merge failure blocks issue completion and downstream release. Preserve evidence,
  return ADR-005 to Proposed/no-winner in a normal reviewed corrective/revert commit, and do not
  use reset/force-push/history rewrite.
- Rollback preserves all source/locks/prior and v2 evidence, removes only owned transient runtime
  state/default selection, retains the neutral preview, and changes no Issue #6/shared/protected/
  cloud state. A merged rollback uses an authorized normal `git revert`, never destructive Git.

## Explicit State Transitions

Only the workflow label changes at each successful boundary; preserve `risk:high`, `tdd`,
`security:S3`, `frontend`, `accessibility`, `decision-gate`, and `preview-runnable` throughout.

| From | Required event | To | Forbidden claim |
|---|---|---|---|
| `triaged` | This plan-only amendment committed/pushed/commented with exact SHA | `ready for plan validation` | No validation/readiness claim |
| `ready for plan validation` | Fresh independent validation PASS at exact head | `ready for plan audit` | No cook authorization |
| `ready for plan audit` | Fresh readiness audit PASS naming implementation input/timer/scope | `ready to cook` | No gate/evidence pass |
| `ready to cook` | v2 cook completes evidence/scoring/retention; two exact-head reviews PASS | `ready to review` | No human approval or merge claim |
| `ready to review` | PR exists and authorized human approves exact final head | `review-passed` or repository-equivalent merge-authorized state | Auto-approval cannot satisfy |
| merge-authorized | Human-controlled merge and pristine post-merge verification PASS | Issue #7 implementation complete; production release still UAT-gated | No production release/full conformance claim |

On validation/audit/cook/review failure, retain the prior workflow state or use
`blocked-dependency` with exact blockers; never advance on partial evidence. This planning phase
performs only the first transition.

## Traceability Matrix

| Outcome/capability/concern | FR/NFR | Architecture/implementation | Required evidence | Operational/release effect |
|---|---|---|---|---|
| `BO-01`, `CAP-02`, `CON-02` | `FR-08`, `FR-10`, `NFR-01`, `NFR-03` | v2 orchestrator, paired rounds, anchors/decision v2 | environment, samples, comparability, anchor/score digests | Proposed winner/no-winner; tie fails closed |
| `BO-02`, `CON-01` | `FR-04..07`, `FR-11`, `NFR-02` | Playwright projects, static parser, UAT schema | automated snapshots/screenshots plus separate pending UAT | local decision may advance; production release remains UAT-gated |
| `CAP-01` | `FR-02..07`, `FR-12` | journey/keyboard/semantics/reflow/motion/no-JS specs | per-project result, trace, snapshot, screenshot, inventory digests | candidate pass/eliminate; Vietnamese-first retained |
| `CAP-03`, `CON-03`, `CON-04` | `FR-01`, `FR-09..11`, `NFR-05`, `NFR-07` | v2 schemas, parent retention index, TDD/decision scripts | RED/GREEN provenance, exact SHAs, raw and derived hashes, timer | reproducible audit trail; no retrospective pass/score |
| `CON-05` | `FR-08`, `NFR-03` | serialized worker/server, RSS sampler, hard cap | process trees, RSS samples, concurrency record | stop/no-winner above cap; safe on 16GB host |
| `CON-06` | `FR-09`, `NFR-04`, `NFR-06` | S3 scans, CSP/network/storage, rollback v2 | audit/license/provenance/CSP/credential/redaction/cleanup records | exploit/leak blocks decision; no cloud mutation |
| Issue #6 authority | `FR-01`, `FR-08`, `NFR-05` | Barrier B and neutral read-only fixture projection | M2 ancestry, four digests/blobs/schema/grain conclusion | drift invalidates both candidates and all v2 score inputs |
| Human governance | `FR-10`, `FR-11` | two exact-head reviews, PR approval gate, Proposed ADR | review reports and explicit human exact-SHA approval | merge blocked until human; release blocked until UAT |

## Planning-Only Verification and Handoff

This planner may run only Markdown/plan/static repository checks: `ck plan status`, link/path
existence, frontmatter/heading checks, supersession-term coverage, timer arithmetic, changed-path
allow-list, `git diff --check`, credential-pattern scan of changed plan text, exact branch/ref
equality, and clean publication verification. It must not run product/unit/e2e/browser/evidence,
candidate, scoring, ADR, rollback, OS, CuaDriver, Docker, cloud, Terraform, PR, or merge commands.

The independent validator must confirm, at minimum:

- all native-OS blocking clauses are covered by the exact supersession ledger;
- no deferred UAT item appears in must-pass or score predicates;
- v1 anchors/evidence/source/locks remain immutable and v2 paths are additive;
- timer, Gate C, Gate D, ADR, review, PR, merge, and release semantics agree;
- every required file/test/command/evidence/state transition is unambiguous; and
- no Issue #8+, root Make/.gitignore, portal/runner, Docker/AWS/cloud/Terraform scope is implied.

## Not in Scope

No product/test/evidence implementation in this planning phase; no candidate source or lock edit;
no prior evidence/index/attestation rewrite; no ADR/scorecard change; no winner; no native OS or
browser execution; no CuaDriver; no System Settings; no VoiceOver; no Chrome-menu zoom; no root
Makefile/.gitignore; no Issue #8+; no Docker/AWS/cloud/Terraform; no publisher/signing/release; no
PR; no merge; and no synthesized human approval.
