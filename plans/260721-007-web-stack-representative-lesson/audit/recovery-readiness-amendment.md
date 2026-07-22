---
title: "Recovery Readiness Amendment — Issue #7 Manual Gate C"
issue: 7
phase: fresh-post-no-winner-recovery-readiness-audit
status: waiting-for-owner-permission
recoveryVerdict: WAITING_FOR_OWNER_PERMISSION
priorImplementationInputSha: "8869b9238704719caff5140d9412bb7bebcecc6f"
cookSourceAndTestedSha: "02051ed94d4e2c920f8a65a4ecab0e08a82b946a"
retainedEvidenceAttestationSha: "1d3cdf769e9c0b3ee1fa0238309f7328c0908346"
newRecoveryInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: next-vite-manual-gate-c-and-gate-d
barrierB: closed
auditedAt: "2026-07-21"
---

# Recovery Readiness Amendment — Manual Gate C

## Verdict and exact authority

`WAITING_FOR_OWNER_PERMISSION`. The retained no-winner is honest and remains binding. A future
recovery cook may proceed only after the owner manually grants and confirms the two CuaDriver
macOS permissions and the new cook passes every preflight in this amendment. This audit does not
grant permission and did not perform manual Gate C, candidate work, scoring, winner selection,
ADR/scorecard updates, PR, or merge.

The sole new recovery input is the exact commit that first contains this amendment as its only
change. Its full 40-character SHA is attested in the Issue #7 publication comment. A commit cannot
contain its own SHA without a recursive hash claim, so no predecessor, branch name, abbreviation,
tag, descendant, or `HEAD` substitution is valid. Before recovery, the new cook must fetch and
prove local HEAD, tracking ref, and a fresh live feature ref all equal that attested SHA.

Issue #7 remains open with `blocked-dependency`; this is the repository's current blocked label.
Barrier B remains closed. Neither changes until the owner confirms the manual permission action
and a new recovery cook passes the complete permission and functional preflight below.

## Independently verified current state

| Item | Exact result |
|---|---|
| Branch | `feature/issue-5-02-web-spike` |
| Prior implementation input | `8869b9238704719caff5140d9412bb7bebcecc6f`; verified ancestor |
| Cook source and tested | `02051ed94d4e2c920f8a65a4ecab0e08a82b946a`; verified ancestor |
| Retained-evidence attestation/current pre-amendment head | `1d3cdf769e9c0b3ee1fa0238309f7328c0908346` |
| Git equality | local, tracking, and freshly queried live feature ref all exactly `1d3cdf769e9c0b3ee1fa0238309f7328c0908346` |
| Worktree | tracked tree and index clean; `.artifacts` absent |
| Runtime | ports `4174`–`4178` free; no candidate server, preview server, or candidate observation process |
| External audit processes | audit-control logger/watcher and the CuaDriver daemon are not candidate processes and were not signalled |
| Issue #7 | open; `blocked-dependency`; cook report `issuecomment-5030936524` says `BLOCKED` / `no-winner` |
| Decision state | ADR-005 `Proposed`; decision `no-winner`; all candidate scores null; Barrier B closed |
| Toolchain | Node `22.22.3`; npm `10.9.8` |

The pre-amendment head contains only retained evidence and no candidate source change after the
cook source/tested commit. This audit fetched before comparison and used a fresh remote-ref query,
not a cached tracking ref alone.

## Frozen inputs and byte identities

No future recovery action may edit the candidate source, manifests, locks, modes, common tree,
Issue #6 inputs, score anchors, or retained automated evidence. Empty Git diffs from the prior
implementation input to the current pre-amendment head independently proved the common tree,
neutral preview, retained Gate A evidence, and score anchor unchanged.

| Frozen input | Current identity |
|---|---|
| `spikes/web/common` | Git tree `f00fe97715df5dd469302994349fb95c9412482b` |
| `spikes/web/preview` | Git tree `21376a30fe5f2b5b08f79eeb289bcd1e89663d79` |
| `spikes/web/evidence/retained/gate-a` | Git tree `76751df92c6bb9e8b0417e9023bb97cf6273355f` |
| `spikes/web/harness/score-anchors.json` | blob `0de35b53685ef6d4d30b8d0486b416f563be9cb8`; SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` |

Exact Issue #6 M2 is `24be3b34c6b0fcdbd07c5800dcab349054e34713`, verified as an
ancestor. Each current fixture identity equals M2:

| Path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

The Gate A review-fix index independently revalidated 19/19 non-self-indexed records. The Gate A
recovery index independently revalidated 16/16. SHA-256, byte count, uniqueness, and locator
checks all passed.

## Retained evidence and timer audit

The Barrier B checker passed again against exact M2 and all four identities. Its conclusion is
`insufficient-evidence` with reason `no-common-grain`; the portable fixture is explicitly
`local-artifact-integrity-only`, contains all four grains, and makes no publisher-authenticity or
cross-grain attribution claim. Barrier B is complete and closed, not reopened by this recovery.

Foundation records are internally consistent and retain honest TDD transitions: each candidate
recorded an intended 0/3 RED before 3/3 GREEN. Candidate active durations remain immutable:

| Candidate | Active seconds | Foundation | Current Gate C consequence |
|---|---:|---|---|
| Astro | `231.113422042` | pass | eliminated after serious target-size failures in both browsers; score null |
| Next | `140.908233250` | pass | automated Gate C pass, manual record incomplete; score null |
| Vite | `144.071145875` | pass | automated Gate C pass, manual record incomplete; score null |

The automated Gate C order was `Vite -> Astro -> Next`. The retained index contains six valid
trace archives and 48 screenshots: eight screenshots for each candidate/browser pair. Chrome
`150.0.7871.129` and Firefox `151.0` are recorded. Vite and Next pass the automated result in both
browsers. Astro has ten serious WCAG target-size nodes in each browser and is eliminated.

The automated suite used Playwright keyboard injection, a `640`-pixel viewport, reduced-motion
emulation, and a JavaScript-disabled browser context. Those are valid automated evidence only.
The separate manual record says `manualComplete: false`, lists every actual manual facet as
missing, declares no substitution, and forces no-winner. The OS probe likewise makes no actual
keyboard, VoiceOver, zoom, reduced-motion, or no-JS claim. No automation or axe output was
misrepresented as manual evidence.

The retention index independently revalidated 106/106 records by SHA-256 and byte count, with
unique safe locators and no self-indexing. It binds source/tested SHA
`02051ed94d4e2c920f8a65a4ecab0e08a82b946a`. Retained Gate D tests pass and correctly require
no-winner. The retained evidence has no numeric cold/warm/RSS/authoring score sample set; therefore
manual completion alone cannot create a score or winner. Gate D must remain fail-closed unless the
complete binding raw score inputs already required by the plan are present and valid.

The closed shared/final timer records monotonic start `217149772843083`, monotonic end
`218830783918500`, no pause, and used duration `1681.011075417` seconds. Exact decimal arithmetic
was performed with integer nanoseconds:

```text
7200.000000000 - 1681.011075417 = 5518.988924583
```

The remaining shared/final budget is exactly `5518.988924583` seconds. The old record is immutable.
Owner permission waiting may pause before the new recovery segment begins, but it must never
reset, restart, replace, or credit elapsed time. All recovery work after a successful preflight is
additive, starts from cumulative used `1681.011075417`, and consumes this same remainder.

## Fresh verification performed by this audit

- Harness plus common tests: 68/68 pass.
- Candidate clean verification, serialized Astro then Next then Vite: exact-lock
  `npm ci --ignore-scripts`, production build, and 3/3 foundation tests pass for each candidate.
- Retention, continuation-authority, Barrier B, Gate D no-winner, scorecard no-winner, S3
  protected-path, changed-path allowlist, immutable-byte, and rollback checks pass.
- All three lockfiles are version 3 and registry/integrity closed: Astro 352, Next 59, Vite 58
  package entries. Clean installs executed no lifecycle scripts.
- `npm audit` reports zero vulnerabilities for Astro and Vite. Next retains two moderate findings
  in the already disclosed PostCSS advisory family, with zero high or critical findings. This
  audit made no dependency or lock change.
- Credential, private-key, credentialed-URI, private absolute-path, and PII scans of the changed
  tracked text found no issue. All six trace archives passed the same sensitive-data scan; their
  recorded network URLs are loopback-only and result records contain no cookies or storage data.
- Rollback remains deletion of the isolated candidate/evidence surface; the previously deferred
  `apps/learning-portal` and `apps/lab-runner` paths remain absent. Root `Makefile` and
  `.gitignore` are unchanged.
- Generated `node_modules`, build output, and cache directories created by verification were
  removed only at exact candidate paths. They are reproducible and were not retained. The final
  tracked tree returned clean, `.artifacts` remained absent, and ports `4174`–`4178` remained free.

## External owner permission gate

CuaDriver `0.10.0` is installed at `~/.local/bin/cua-driver` with the signed application at
`/Applications/CuaDriver.app`. The audited application identity is:

```text
bundle identifier: com.trycua.driver
team identifier: YCK386LBJ7
```

The global Codex MCP entry `cua-driver` is enabled and invokes `~/.local/bin/cua-driver mcp`.
`cua-driver doctor --json` passed its non-interactive installation/session checks.

The supplied post-cook fact says driver-owned Accessibility and Screen Recording were not granted.
During this audit, two read-only, non-prompting queries unexpectedly reported both permissions
`true`, `capturable: true`, source `driver-daemon`, and executable `/Applications/CuaDriver.app`:
`permissions status --json` and `check_permissions` with `prompt: false`. This discrepancy is not
treated as a grant or as readiness. TCC can change outside Git, a status bit does not prove the
required capabilities, and the owner has not confirmed a manual grant. This audit did not invoke
`permissions grant`, reset TCC, click a permission dialog, launch a browser, capture a screen,
inspect AX, send a key, or run manual Gate C.

The owner must manually open macOS System Settings, go to Privacy & Security, enable
`CuaDriver.app` / `com.trycua.driver` for both Accessibility and Screen & System Audio Recording,
complete any required relaunch manually, and explicitly tell the recovery controller that this
action is complete. The recovery cook must never automate the grant, click a TCC dialog, reset
TCC, or infer authorization from this audit's read-only status result.

## Mandatory recovery-cook preflight

The future recovery cook may start the timered recovery segment only after all steps pass in this
order:

1. Fetch and prove local HEAD, tracking ref, and freshly queried live feature ref equal the exact
   amendment output SHA attested in the Issue #7 comment. Require a clean tracked/index state,
   `.artifacts` absent, ports `4174`–`4178` free, and no candidate-owned process.
2. Revalidate exact M2/four fixture identities, common/preview/Gate A/anchor identities, frozen
   candidate source/manifests/locks/modes, and retained automated evidence/index. Any drift stops.
3. Receive the owner's explicit confirmation that the two manual macOS grants for exact identity
   `com.trycua.driver` are complete.
4. Re-prove CuaDriver version `0.10.0`, signed bundle/team identity, enabled MCP command, and both
   read-only permission checks. Require Accessibility `true`, Screen Recording `true`, and
   `capturable: true`. Require `doctor` success and a read-only `health_report` with `overall: ok`
   and passing session, bundle identity, TCC, AX capability, and screen-capture capability checks.
5. Create a disposable neutral local page and isolated browser profile in a private temporary
   directory outside the repository. Bind only an exact loopback port and open a separate
   CuaDriver-owned Chrome window; do not inspect or change personal tabs, profiles, windows, or
   foreign applications/processes.
6. Bind a standard CuaDriver session to the exact disposable Chrome PID and window. Prove a fresh
   screenshot capture and non-degraded AX tree for a labeled neutral control. Capture a snapshot
   immediately before and after each probe action.
7. Keep a neutral foreign app frontmost, deliver a trusted background key event through
   CuaDriver's exact target PID/window and AX element, and prove both the page's recorded key/focus
   change and that the frontmost app did not change. Foreground fallback, browser automation,
   DOM dispatch, AppleScript substitution, or an inferred key event does not satisfy this probe.
8. Stop the disposable session/server, remove only its exact temporary profile/root, and prove
   the port free, no owned process, repository clean, and every frozen input/evidence identity
   unchanged.

Failure of any preflight item leaves the verdict `WAITING_FOR_OWNER_PERMISSION` or `BLOCKED` and
does not start manual candidate observations.

## Minimum authorized recovery scope

Astro remains eliminated. The binding candidate plan says an eliminated candidate is never
resurrected or scored without a separately authorized new spike. No existing authority permits an
Astro tests-first source fix within untouched candidate time, so this amendment grants none.

Only the surviving frozen candidates may receive new manual evidence, in the surviving subsequence
of the frozen rotated order: `Vite -> Next`. Existing candidate source, manifests, lockfiles,
modes, common/fixture inputs, score anchors, automated Gate C output, and old retained evidence are
read-only.

For each candidate, the recovery cook must obtain fresh actual OS-level evidence for the same
manual protocol:

1. Actual background macOS keyboard events through CuaDriver, with visible focus and behavior
   proven by bracketed screenshots/AX state and exact target PID/window.
2. Named macOS VoiceOver traversal with OS/browser/VoiceOver versions and actual spoken output
   made observable through VoiceOver Caption Panel or Speech History together with AX and visual
   state. A written synthetic transcript or inferred accessible name is not spoken evidence.
3. Actual Chrome 200% native browser zoom and narrow reflow/comprehension review. A viewport size,
   device scale, CSS transform, screenshot enlargement, or Playwright emulation is not zoom.
4. Actual macOS Reduce motion setting enabled and reviewed, with the prior value recorded and
   restored. Playwright `reducedMotion` emulation is not manual evidence.
5. Actual JavaScript-disabled Chrome setting/profile and comprehension review. A Playwright
   JavaScript-disabled context, request blocking, CSP injection, or DOM mutation is not manual
   evidence.

Use one isolated browser profile/window and only the two local candidate pages. Record exact
versions, candidate/source/fixture identities, times, target window/PID, actions, observable
results, screenshots/AX/spoken-output artifacts, and cleanup. Restore VoiceOver, browser zoom,
JavaScript, Reduce motion, frontmost application, and every other changed OS/browser setting on
success, failure, timeout, or interruption. Never touch personal tabs or foreign processes.

New writes are limited to the smallest additive Issue #7 recovery surface:

- a new retained manual Gate C run directory and its index for Vite and Next;
- strictly necessary tests-first manual-evidence validation code/tests under
  `spikes/web/harness/`, plus the minimum live stage/decision wiring needed to validate the new
  additive record;
- a new retained Gate D recomputation record and retention-index update;
- ADR-005 and the three candidate scorecards only after complete, equal, valid evidence permits a
  fail-closed recomputation;
- the Issue #7 audit/plan status and Issue #7 comment needed to attest the recovery result.

No old retained artifact may be overwritten or relabelled. If a validator can consume the
additive format without source changes, no validator change is authorized. Candidate files,
locks, common inputs, fixtures, modes, anchors, automated evidence, root files, applications, and
out-of-scope plans remain forbidden.

If the manual records are complete and equal, Gate D may be recomputed from the full retained
evidence. A winner is allowed only if every binding numeric input is present and all gates pass.
Otherwise retain explicit no-winner, null scores, and ADR-005 `Proposed`. This amendment does not
preselect a framework and does not authorize filling absent score samples retrospectively.

## Safe cleanup and stop conditions

Cleanup must use recorded exact PIDs, window IDs, session IDs, profile directory, temporary root,
and ports. Stop only owned candidate/disposable servers, close only the isolated recovery window,
restore recorded OS/browser values, end the CuaDriver session, and remove only exact generated or
temporary paths after validating them. Never kill by broad pattern, signal a foreign listener,
use personal browser state, run `git clean`, reset/checkout history, or delete retained evidence.

Stop fail-closed and publish no-winner without fabrication if any of these occurs:

- owner confirmation is absent, either permission is false, identity/version differs, or
  doctor/health/capture/AX/background-key proof fails;
- the test changes foreground focus, cannot isolate a window/profile, exposes personal data, or
  would require control of a foreign app/process;
- Git equality, cleanliness, immutable identities, evidence indexes, ports, or process ownership
  fail; a frozen input or old evidence would need an edit;
- Astro resurrection or any candidate source/manifest/lock change becomes necessary;
- actual VoiceOver speech cannot be observed, any manual facet is simulated/inferred, candidate
  records are incomplete or unequal, or a changed setting cannot be restored;
- the cumulative shared/final budget reaches 7200 seconds; no timer reset or extra candidate time
  is allowed;
- complete raw Gate D score inputs are absent or invalid, even if the new manual record passes.

Missing evidence must stay missing and be named. Never backfill a timestamp, spoken phrase,
keystroke, zoom state, OS setting, observation, score sample, or pass result that was not actually
observed and retained.

## Preserved exclusions

This amendment grants no Issue #8+ work; cloud, AWS, Terraform, root `Makefile`/`.gitignore`,
runner, portal, publisher, signing, tag, release, PR, merge, Astro resurrection, candidate source
fix, dependency update, fresh automated candidate observation, or time reset. A fresh independent
review of the exact eventual recovery head remains mandatory before any later integration action.
