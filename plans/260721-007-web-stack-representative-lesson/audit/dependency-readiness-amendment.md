---
title: "Dependency Readiness Amendment — Issue #7 Remaining Phases"
issue: 7
phase: fresh-post-issue-6-dependency-readiness-audit
status: ready-with-gates
auditVerdict: READY_WITH_GATES
dependencyMergeSha: "7e7853d3005decf16076a6b3b6d96995c2702ffd"
issue6IntegrationMergeSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
newImplementationInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: barrier-b-through-gate-d
barrierB: open
futureBranch: "feature/issue-5-02-web-spike"
auditedAt: "2026-07-21"
---

# Dependency Readiness Amendment — Remaining Issue #7 Phases

## Verdict and exact authority

`READY_WITH_GATES`. The Issue #6 dependency condition is satisfied and dependency Barrier B is
open. This amendment authorizes only the remaining Issue #7 work: phases 3–8, comprising the
tests-first executable Barrier B integration, the three equal candidate foundations, Gate C, and
Gate D. The serialized execution order is defined below.

The only valid `IMPLEMENTATION_INPUT_SHA` is the exact commit that first contains this amendment
as its only non-merge change. Its full 40-character SHA is published in the Issue #7 readiness
comment. A literal SHA cannot be embedded in its own containing commit without a recursive hash
claim; no predecessor, dependency merge, branch name, tag, descendant, abbreviation, or `HEAD`
substitution is valid.

Before the first continuation write, fetch and prove:

```text
local HEAD == upstream tracking ref == freshly queried live feature ref == IMPLEMENTATION_INPUT_SHA
```

Also prove exact M2 is an ancestor, the four identities below still match, the tracked worktree is
clean, no owned preview process is active, and the requested loopback port is free. Any failure
closes Barrier B and requires a new independent readiness audit; it is not an implementation fix.

This is not a score, framework selection, ADR acceptance, PR, merge, release, or authority for
Issue #8+. The standing owner authorization through Issue #14 does not replace the later
exact-head independent review and manual decision gates.

## Independently verified Git and GitHub state

| Item | Exact result |
|---|---|
| Feature ref before dependency merge | local, tracking, and freshly queried live ref all `171c235d3fd2dd5333457e28e9a351ca11bac446`; tracked status clean |
| Reviewed Gate A source / head | source and tested `6ce2fc9d6af77ed9f9c722791811c6474973cf3b`; reviewed head `171c235d3fd2dd5333457e28e9a351ca11bac446`; `PASS_AFTER_FIXES`; 54/54 |
| Gate A recovery input | `0c73f4712c8ac7902042735ff1da96ef1e5285a3`, ancestor of source |
| Earlier plan / validation / audits | `0890c4abab46f81d110be6cbd6de3560e631a735`; `0486642528b9a6ba8e96cee18d6eda76c3b5deb9`; `e8ca5f3ee9e8976a4b92915fd7d7dc687609f7a9`; `0c73f4712c8ac7902042735ff1da96ef1e5285a3` |
| Issue #6 integration M2 | `24be3b34c6b0fcdbd07c5800dcab349054e34713`; live integration ref equal |
| M2 parents | prior integration `b6482e0e435422b526fe06193c7276e834abef1b`; reviewed fix head `707ca6ef698f54afaa3ddd62e47caafd2d5f2ba8`; both verified ancestors |
| Issue #6 state | closed with canonical `shipped` label |
| Issue #7 pre-audit state | open; `blocked-dependency`; handoff comment `issuecomment-5030453486` says `HANDOFF_MERGED_VERIFIED` and leaves Barrier B to this audit |
| Normal dependency merge | `7e7853d3005decf16076a6b3b6d96995c2702ffd`; parents `171c235d3fd2dd5333457e28e9a351ca11bac446` then M2; normal `ort` merge, no conflict, rebase, reset, force, squash, or cherry-pick |
| Preflight / merged tree | conflict-free synthetic and committed tree `ba1a7dc5b8ab29dce15a0ba2797b4477a2adbaa8` |
| Gate A byte preservation | `spikes/web` tree `32b2b148fee37b6856ceb6066992ed497b45fa53`; `mk/issue-5/i5-02.mk` blob `d234feed70dd755d0cfcc00627161dc7ecc7bb97`; no diff from `171c235…` after the merge |
| Retained Gate A integrity | 19/19 non-self-indexed retained artifacts matched both SHA-256 and byte count; source/tested/tree fields match the reviewed record |
| Runtime preflight | `.artifacts` absent after cleanup; no issue-owned preview; `127.0.0.1:4174` free; exclusive bind/close probe passed and left the port free |

## Exact Issue #6 dependency identities

M2 and the dependency merge tree contain these exact tracked bytes:

| Path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

The manifest is `promotion-trust-fixture-manifest-v2`. Its portable attestation is explicitly
`local-artifact-integrity-only`, records two sequential equal runs against tested tree
`b9a654d8fc3321e4e8a4df2a365f7904de41ed7c`, and does not claim publisher authenticity. The v2
schema is current, v1 remains readable/rollback-only, and the migration to v2 requires
republication from strict owner-bound runs. The default third reader passed from this merged tree
without `.artifacts`; explicit strict owner-bound replay correctly failed
`RUN_BUNDLE_DIRECTORY_UNSAFE` because private owner bundles were absent. Continuation may consume
the tracked portable fixture but may not claim, simulate, weaken, or republish owner authenticity.

## Merged-tree verification

- Historical Gate A unit sets: authority 10 + lifecycle 17 + common 27 = 54/54 pass. These are the
  reviewed tests, executed from the merged tree without editing Gate A source or evidence.
- Issue #6 exact hash-locked Python 3.12 graph: 56 distributions verified.
- Portable third reader: pass, `mode=portable-clean`, 89 rows, no `.artifacts` before or after.
- Complete Issue #6 modules: 61/61 pass.
- Strict owner-bound replay without private bundles: required non-zero
  `RUN_BUNDLE_DIRECTORY_UNSAFE`.
- Final tracked status after verification: clean.

The old Gate A authority file intentionally lists the four Issue #6 paths as `requiredAbsent` and
the old stage record intentionally says Barrier B is closed. Those statements were correct for
the reviewed historical Gate A tree. They are now stale controls, not corrupt evidence. Do not
rewrite or relabel the retained Gate A record. The first continuation change must use genuine RED
tests to replace the live stage rule with exact M2 ancestry and identity checks.

## Stale assumptions and binding amendments

The complete plan, phase files, candidate protocol, score anchors, S3 disposition, validation,
original/recovery audits, Gate A source/evidence, and Issue #6 v2 manifest/schema/reader were read
again. These are the only post-merge corrections:

1. Issue #6 is no longer open/triaged and the four files are no longer absent. M2 is merged and
   Issue #6 is closed/`shipped`.
2. Barrier B dependency readiness is open at the exact identities above. The executable Barrier B
   target remains tests-first work and must pass before a candidate install or real-fixture run.
3. The v2 portable reader makes a clean tracked-fixture consumer valid without private
   `.artifacts`. Strict replay remains an owner/publication control and must not become a consumer
   prerequisite or be weakened into a portable claim.
4. Because the real fixture is already merged, run Barrier B before all candidate foundations and
   make every candidate consume the same real fixture from its first GREEN. Do not create or score
   pre-Barrier-B provisional samples.
5. Gate A source, retained evidence, common contract, neutral synthetic preview, and score anchors
   stay immutable. The live authority/stage checker may change only through new tests that preserve
   the historical record and enforce the new exact identities.

All other requirements remain binding, including fail-closed result states, S3 boundaries,
candidate modes, time limits, no-winner behavior, retention, and the human gate.

## Frozen common and scoring inputs

The following values are immutable for all three candidates and all observations:

| Input | Frozen value |
|---|---|
| Common contract/state/test tree | Git tree `f00fe97715df5dd469302994349fb95c9412482b` at `spikes/web/common` |
| Neutral synthetic preview fixture | `spikes/web/common/fixtures/synthetic-promotion-trust-v1.json`; SHA-256 `5282cc6698c34e5db130162223d90376dacdd8da61041344ddc86e5b76a6a4ac`; preview-only, never score input |
| Real fixture inputs | Exact four M2 identities in the table above |
| Score anchors | `spikes/web/harness/score-anchors.json`; blob `0de35b53685ef6d4d30b8d0486b416f563be9cb8`; SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` |
| Candidate modes | Astro `static-react-island`; Next `standalone-app-router`; Vite `static-mpa-progressive-react` |
| Host tools | Node `22.22.3`; npm `10.9.8`; lockfile version 3 |

No common, fixture, mode, weight, threshold, anchor, or interpretation edit is allowed after any
candidate observation. A necessary correction invalidates all affected observations and requires
a new independent authorization. A candidate lock change invalidates that candidate's evidence
and does not reset its clock.

## Feasibility and exact dependency inputs

Live primary registry metadata and discarded lock-resolution probes confirmed the frozen host is
compatible:

| Tool | Exact version | Engine / result |
|---|---:|---|
| Astro | `7.1.3` | Node `>=22.12.0`, npm `>=9.6.5`; exact registry integrity present |
| `@astrojs/react` | `6.0.1` | Node `>=22.12.0`; React 19 peers accepted; required Astro React-island integration |
| Next.js | `16.2.10` | Node `>=20.9.0`; React/React DOM 19.2.7 peers accepted |
| Vite | `8.1.5` | Node `^20.19.0 || >=22.12.0` |
| `@vitejs/plugin-react` | `6.0.1` | Node `^20.19.0 || >=22.12.0`; Vite 8 peer accepted |
| React / React DOM | `19.2.7` / `19.2.7` | exact peer-compatible pair |
| `@playwright/test` | `1.61.1` | Node `>=18`; owns exact `playwright` 1.61.1 |
| `@axe-core/playwright` | `4.12.1` | exact `axe-core ~4.12.1`; Playwright Core peer accepted |

Every candidate manifest must pin its applicable framework packages above with exact strings and
must include the same exact Playwright and axe versions. Any additional top-level package needed
by that candidate must be justified and pinned exactly before its lock is frozen. No range,
`latest`, scaffold command, hidden auto-install, git dependency, non-registry URL, or shared/root
workspace is allowed.

Three separate npm 10 `--package-lock-only --ignore-scripts` probes resolved lockfile version 3
with 352 Astro, 59 Next, and 58 Vite package entries and no `node_modules`. These disposable counts
and probe lock hashes are feasibility observations, not candidate lock authority. Each real
candidate owns only:

```text
spikes/web/candidates/astro/package-lock.json
spikes/web/candidates/next/package-lock.json
spikes/web/candidates/vite/package-lock.json
```

Generate each lock only from its final exact manifest, verify lockfile v3 and registry/integrity
closure, then force-add only those three exact ignored paths. Never add a root/common lock and
never edit `.gitignore`.

Primary references used for this feasibility decision:

- [Astro React integration](https://docs.astro.build/en/guides/integrations-guide/react/)
- [Next.js installation and Node baseline](https://nextjs.org/docs/app/getting-started/installation)
- [Next.js production start host/port options](https://nextjs.org/docs/app/api-reference/cli/next)
- [Vite 8 Node support](https://vite.dev/blog/announcing-vite8)
- [Vite production build and static-host boundary](https://vite.dev/guide/static-deploy.html)
- [npm clean-install semantics](https://docs.npmjs.com/cli/commands/npm-ci/)
- [Playwright browsers/channels](https://playwright.dev/docs/browsers)
- [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing)
- [WCAG 2.2](https://www.w3.org/TR/WCAG22/)

## Browser, accessibility, and lifecycle gate

A disposable evidence-tooling probe installed no framework and wrote no repository path. Exact
Playwright Core 1.61.1 successfully launched installed Google Chrome
`150.0.7871.129` through `channel: chrome` on macOS `26.5.1` arm64, read semantic content, honored
`prefers-reduced-motion: reduce`, ran axe 4.12.1 with zero violations on the probe document, wrote
a non-empty trace, and closed cleanly. VoiceOver Utility bundle `com.apple.VoiceOverUtility`,
version `10`, is present. This proves tool feasibility only. It is not Issue #7 candidate,
browser, accessibility, or manual evidence.

Gate C must run on a fresh frozen session and retain exact versions, commands, logs, screenshots,
and traces for every surviving candidate:

- current installed Google Chrome via Playwright `channel: chrome`, with the actual version
  recorded at run time;
- one Playwright-managed second engine, Firefox from Playwright 1.61.1, installed explicitly and
  recorded by actual browser version/revision;
- identical viewport, device scale, fonts, locale, timezone, reduced-motion setting, port policy,
  fixture digest, candidate order rotation, and retry policy;
- fresh trace plus normalized screenshots for the same required journey states, including failure,
  reset, evidence, conclusion, reflow, reduced motion, and no-JS;
- automated semantics, keyboard-path assertions, axe WCAG A/AA checks, reflow/overflow checks,
  reduced-motion emulation, network/CSP inventory, and JS-disabled static facts;
- actual manual keyboard traversal; named macOS VoiceOver with OS/browser/VoiceOver versions;
  actual 200% browser zoom and narrow reflow; actual reduced-motion review; and actual no-JS
  comprehension review. Automation and axe never substitute for these manual records.

Any missing, stale, mixed, simulated-as-manual, or unequal record blocks Gate C and forces an
explicit no-winner. Current availability does not pre-approve the later session.

All issue-owned servers bind only `127.0.0.1` and the exact requested port, use exclusive/strict
port behavior with no scanning, publish readiness bound to candidate/mode/fixture/run/input, and
stop only the verified PID/process group named in the candidate-scoped locator. Astro and Vite
serve built static output through the common static measurement host; `vite preview` is diagnostic
only and cannot enter evidence. Next runs the generated standalone production server with
`HOSTNAME=127.0.0.1` and an exact `PORT`. A foreign listener is never signalled. Readiness timeout,
owned cleanup, idempotent down, and final free-port checks are mandatory.

## Serialized tests-first execution contract

Use one writer in this feature worktree. Isolated branches/worktrees are not authorized: all
candidates must update the same authority/stage machine, issue-local Make fragment, fixture-handoff
record, evidence schemas/indexes, and total timer. Combining independent histories would create
avoidable lock/evidence/schema conflict and ambiguous observation order.

Execution is serialized:

1. **Continuation preflight and Barrier B RED/GREEN.** Start the shared/final two-hour timer before
   the first Barrier B test or implementation write. Add failing tests for absent, unmerged,
   crossed, tampered, schema-invalid, non-portable, attribution-bearing, and stale-digest inputs.
   Capture the intended RED preimage digest and full log. Then implement the exact M2/four-identity
   checker, update only the live authority/stage rules, and obtain GREEN. Preserve all old Gate A
   retained bytes. No candidate install precedes this pass.
2. **Astro, then Next, then Vite foundations.** Before each candidate's first test/source/install
   write, start its independent three-hour timer. Write candidate/mode/static-semantic/common-
   consumption/lifecycle/security tests first and retain an intended behavioral RED log. Only
   then create source/manifest/lock and run an inspected clean install. Kill at 90 minutes unless
   clean install, frozen mode build, semantic route, and real common-fixture consumption all pass.
   Kill at three hours for any remaining executable must-pass failure. An eliminated candidate has
   no numeric score and receives no extra time.
3. **Gate C clean rerun.** With locks/modes/common/fixture frozen, clean transient install/build
   state and rerun survivors in rotated order `Vite -> Astro -> Next` so foundation order is not
   reused. Run every automated and manual requirement above against the exact same fixture bytes.
4. **Gate D.** Use only complete reproducible Gate C indexes. ADR-005 remains `Proposed` whether it
   names an evidence-backed winner or an explicit no-winner. Incomplete, invalid, incomparable,
   capped, or missing manual/browser evidence requires no-winner; it never permits a fallback,
   partial score, tie improvisation, or `Accepted` status.

The original issue cap does not reset: Gate A retains its three-hour allocation; Astro, Next, and
Vite retain equal three-hour caps and 90-minute early kills; Barrier B implementation plus Gate C
and Gate D share the remaining two-hour window. Total active issue time is at most 14 hours over at
most two implementation days. Installs, tests, fixes, builds, authoring, and measurements count.
Only evidenced external registry/browser outage or a required owner decision may pause; no pause
or rerun restores a candidate's clock.

For every RED/GREEN/build/evidence command, retain UTC start/end, command and safe environment
digest, exit status, stdout/stderr, source/tree/input/fixture/lock digests, and artifact SHA-256.
Retain sanitized raw logs, screenshots, traces, manual records, timers, and redaction/index files.
An intended RED must be a missing-behavior assertion, not a syntax error, absent test dependency,
or broken harness. No observed result may be recreated after the fact.

## Real fixture and evidence semantics

Each candidate must read the exact merged fixture paths directly through a thin read-only adapter.
No copied JSON/YAML, embedded reformatted object, generated substitute, cross-candidate adapter,
or candidate-owned interpretation is valid. Bind the M2 SHA, four SHA-256 values, four blobs,
manifest v2 payload integrity, common tree, candidate lock, mode, tested tree, and browser session
to every retained decision record.

Render four separate evidence grains with their exact keys and limitations:

1. promotion: `[promo_name, channel]`;
2. fulfillment: `[carrier, region_name]`;
3. returns: `[reason, category_name, region_name]`;
4. data quality: `[scenario]`.

No join, shared key, edge, composite metric, causal language, or attribution across those grains is
allowed. Every candidate must reach the controlled expected conclusion exactly
`insufficient-evidence` / reason `no-common-grain`. A framework that cannot preserve this is
eliminated; shared contracts and fixture bytes are never edited to rescue it.

## Path, supply-chain, security, and cleanup authority

Authorized later write paths are limited to:

- `spikes/web/candidates/{astro,next,vite}/**`;
- new remaining-phase checks/state under `spikes/web/harness/**`, excluding the immutable score
  anchors and existing Gate A retained evidence;
- `spikes/web/evidence/retained/{barrier-b,astro,next,vite,gate-c,gate-d}/**` and
  `spikes/web/evidence/retention-index.json`;
- `mk/issue-5/i5-02.mk`;
- Gate D only: `docs/decisions/0005-web-stack.md` and
  `docs/decisions/evidence/adr-0005-web-stack-scorecard.{md,json}`.

Immutable/read-only paths include `spikes/web/common/**`, `spikes/web/preview/**`,
`spikes/web/evidence/retained/gate-a/**`, `spikes/web/harness/score-anchors.json`, the four M2
handoff files, Issue #6 schemas/scripts/tests, plan discovery, root `Makefile`, and root
`.gitignore`. No portal, runner, publisher, signing, release, migration, AWS, cloud, Terraform,
Docker, privileged runner, service, root workspace, root lock, root Make alias, or Issue #8+ path
is authorized.

Network/install allow-list for the later cook:

- npm metadata/tarballs only from `https://registry.npmjs.org`, with lock integrity and exact
  versions; deny git, local, alternate-registry, arbitrary URL, and unpinned sources;
- inspect lifecycle-script inventory and dependency provenance/license/advisory output before
  execution; first run `npm ci --ignore-scripts`, then permit only reviewed necessary lifecycle
  behavior; never run `npm audit fix`, a scaffold, or an upgrade command;
- Playwright's exact documented Microsoft browser hosts `https://cdn.playwright.dev` and
  `https://playwright.download.prss.microsoft.com` only for the managed Firefox revision; no
  `--with-deps`, package-manager escalation, global browser overwrite, or `sudo`;
- candidate runtime/browser requests only to the exact loopback origin and same-origin assets;
  external browser requests, remote content, telemetry, credentials, runner/cloud endpoints, and
  arbitrary ports are failures.

Run `npm audit --json` without mutation for each exact candidate lock, record all severities and a
reasoned disposition, inventory licenses/provenance/resolved hosts/lifecycle scripts, and scan
source, bundles, source maps, logs, screenshots, traces, storage, and network records for secrets,
private paths, tokens, PII, remote URLs, executable fixture content, and privilege-bearing types.
Any unresolved applicable critical/high security finding eliminates the candidate; never weaken a
gate or fixture to obtain a pass.

Cleanup and rollback stop only verified issue-owned process trees, remove candidate-scoped
`node_modules`, build caches, browser profiles, and runtime locators, and prove all requested ports
free. Retain source, exact locks, RED/GREEN logs, sanitized evidence, screenshots, traces, manual
records, timers, hash indexes, and elimination reasons through I5-05. On contamination, invalidate
numeric scores/winner, restore ADR-005 to `Proposed` explicit no-winner, keep the neutral preview,
and return to a closed Barrier B pending a fresh audit. Do not delete losing source or locks.

## Remaining decision gates

- Barrier B is open for dependency readiness now, but its new executable exact-identity check must
  pass tests-first before a candidate install.
- Candidate foundation and must-pass gates are per candidate, serialized, capped, and non-waivable.
- Gate C remains a manual decision gate until current-Chrome plus second-engine Playwright evidence
  and actual keyboard/VoiceOver/200%-zoom/reduced-motion/no-JS records all pass.
- Gate D may publish only reproducible complete score/no-winner evidence and an ADR-005 with status
  `Proposed`. Human approval and a fresh exact-head independent review remain mandatory afterward.
- No PR, merge, issue close, Issue #8+, cloud, publisher, signing, tag, or release follows this
  readiness audit.

`AUDIT_VERDICT=READY_WITH_GATES`

`COOK_SCOPE=barrier-b-through-gate-d`

`BARRIER_B=open`
