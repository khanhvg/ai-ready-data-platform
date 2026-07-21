---
title: "Recovery Readiness Amendment II — CuaDriver Health-Report Supersession"
issue: 7
phase: fresh-independent-recovery-blocker-reaudit
status: recovery-ready
readinessVerdict: RECOVERY_READY
currentRecoveryInputSha: "adf7d7808b754bd8a89ebc17675718c972cb0e89"
cookSourceAndTestedSha: "02051ed94d4e2c920f8a65a4ecab0e08a82b946a"
retainedEvidenceAttestationSha: "1d3cdf769e9c0b3ee1fa0238309f7328c0908346"
newRecoveryInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: next-vite-manual-gate-c-and-gate-d
healthReportDisposition: superseded-by-equivalent-and-functional-preflight
remainingSharedSeconds: "5518.988924583"
barrierB: closed
auditedAt: "2026-07-21"
---

# Recovery Readiness Amendment II — CuaDriver Health-Report Supersession

## Additive verdict and exact supersession

`RECOVERY_READY`. This second additive amendment supersedes exactly one prerequisite in
[the first recovery amendment](./recovery-readiness-amendment.md): the requirement that CuaDriver
`health_report` itself execute and return `overall: ok`. CuaDriver `0.10.0` registers and documents
that read-only diagnostic, but the release's standard-mode built-in risk registry has no reviewed
classification for it. The authorization coordinator therefore denies the call before the
diagnostic implementation executes.

The replacement is mandatory in full: exact signed application identity, standard daemon policy
posture, all `doctor --json` probes, exact agreement between the two independent non-prompting TCC
status surfaces, and a disposable isolated functional preflight that proves real screenshot, AX,
background Tab delivery, focus movement, control activation, and post-action state without a
foreground fallback. This is stronger than accepting a diagnostic-only aggregate and does not
waive any actual manual Gate C evidence.

Every other clause of the first amendment remains binding without reinterpretation, including its
owner/controller authorization boundary, Git and immutable-byte gates, cleanup rules, timer,
surviving order `Vite -> Next`, Astro elimination, actual macOS keyboard and observable VoiceOver
requirements, actual Chrome 200%, actual macOS Reduce Motion, actual no-JS review, equal evidence,
OS restoration, fail-closed Gate D, Proposed-only ADR authority, and fresh independent exact-head
review. This audit performed no GUI action, candidate action, manual Gate C, scoring, winner
selection, ADR/scorecard change, PR, or merge.

The owner-directed re-audit request is the narrow recovery reauthorization contemplated here. It
does not assert how TCC changed and grants no authority to edit a policy, switch permission mode,
use a bypass flag, weaken GUI evidence, or operate a personal browser profile. The new cook must
still re-prove every live condition below before starting work.

The sole new recovery input is the exact commit that first contains this amendment as its only
change. Its full 40-character SHA is attested in the Issue #7 publication comment. A Git commit
cannot contain its own SHA without a recursive hash claim, so no predecessor, branch name,
abbreviation, tag, or later descendant is a valid substitute.

## Exact repository and recovery-input proof

The re-audit fetched before comparison and separately queried the live remote ref. Before this
amendment was written, all three refs were exactly the current and sole recovery input:

```text
local HEAD:  adf7d7808b754bd8a89ebc17675718c972cb0e89
tracking:    adf7d7808b754bd8a89ebc17675718c972cb0e89
fresh live:  adf7d7808b754bd8a89ebc17675718c972cb0e89
branch:      feature/issue-5-02-web-spike
```

The tracked tree and index were clean, `.artifacts` was absent, ports `4174` through `4178` were
free, and the process inventory contained no candidate server, preview server, Gate C runner, or
candidate observation process. Exact M2
`24be3b34c6b0fcdbd07c5800dcab349054e34713`, frozen source/tested
`02051ed94d4e2c920f8a65a4ecab0e08a82b946a`, and retained-evidence attestation
`1d3cdf769e9c0b3ee1fa0238309f7328c0908346` are all ancestors.

There is an empty Git diff from frozen source/tested through the current recovery input across all
candidate sources, manifests, locks, common files, candidate modes, Issue #6 fixture inputs, and
score anchors. There is separately an empty Git diff from the retained-evidence attestation
through the current recovery input across retained evidence, retention index, ADR-005, scorecards,
and the issue-local Make fragment.

### Frozen identities

| Surface | Exact current identity |
|---|---|
| all candidates | Git tree `f2ec341820db157e6bc7fb12e75844ee2730ec12` |
| Astro candidate | Git tree `4b352a31354cc12bebcad9f0a461000c167e5f11`; lock SHA-256 `78677d1a272fdc5c9758810343f89e82f2914625a03259a575208fe1fafef760` |
| Next candidate | Git tree `85777043224f7f00ec944642e3531c1d891e5ec3`; lock SHA-256 `4939388a7e7290ec640e418afac94dc68cfba7bf6b5692df61317b4c95de2e8b` |
| Vite candidate | Git tree `f3b87dab9a43f41c8a31d67fb44f709b28f7e377`; lock SHA-256 `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` |
| candidate modes | SHA-256 `2957c84624ef16d0ebb037ea3fde66d20a0d2dae6d0d049b1e9c4bb7a8ce3181`; Astro `static-react-island`, Next `standalone-app-router`, Vite `static-mpa-progressive-react` |
| common | Git tree `f00fe97715df5dd469302994349fb95c9412482b` |
| neutral preview | Git tree `21376a30fe5f2b5b08f79eeb289bcd1e89663d79` |
| retained evidence | Git tree `15bef78b9b2390ad30ded1bab729e21eca61c7bd` |
| retained Gate A | Git tree `76751df92c6bb9e8b0417e9023bb97cf6273355f` |
| retained Gate C | Git tree `b10d77b72039278f05fa84d3472d5cdfd82c35a7` |
| retention index | blob `026cd7b3d0bd54d6981cdaa1aa7b6ae67cfeba3e`; SHA-256 `58d46e55e21bf02b3abf65a3aaef0442c8e823ef2cb5ffc1da75e2441c262ee6` |
| score anchors | blob `0de35b53685ef6d4d30b8d0486b416f563be9cb8`; SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` |

All candidate files and the mode registry retain Git mode `100644`. The retention index
independently rehashed 106/106 unique safe locators with exact byte counts and SHA-256 values,
binds source/tested to `02051ed94d4e2c920f8a65a4ecab0e08a82b946a`, and retains decision
`no-winner` with no failure.

The four Issue #6 fixture identities remain exact M2 bytes:

| Path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

## Timer identity remains exact

The immutable closed timer is blob `78b04abed94b5ba97250451282666124621535ad`, SHA-256
`d1b452256c1f89a3721f98856c1c1e9fb465249dcc4b4de4b716a0a45ecccbb0`. It records:

```text
budget:                    7200.000000000 seconds
start monotonic ns:        217149772843083
end monotonic ns:          218830783918500
elapsed:                   1681011075417 ns = 1681.011075417 seconds
pauses:                    []
status:                    closed-with-gate-d-no-winner
remaining:                 5518988924583 ns = 5518.988924583 seconds
```

The failed recovery cook stopped before a replacement timer, repository/browser/OS/manual action,
source/tested tree, or output existed. The latest cook log at
`.hermes/logs/claudekit/issue-7-manual-gate-c-recovery-cook.log` and Issue comment
[`5031147063`](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5031147063)
agree on `SOURCE_SHA=none`, `TESTED_TREE_SHA=none`, `OUTPUT_SHA=none`, no neutral-page preflight,
and the unchanged remainder. The next timer starts only after every diagnostic and functional
replacement item below passes and cleanup/revalidation completes. Waiting and preflight add no
credit, cannot reset the clock, and cannot increase the remainder.

## CuaDriver 0.10.0 diagnosis

### Signed identity, install health, permissions, and release

Fresh read-only diagnostics independently established:

| Check | Exact result |
|---|---|
| CLI resolution | `~/.local/bin/cua-driver` resolves to `/Applications/CuaDriver.app/Contents/MacOS/cua-driver` |
| version/bundle metadata | CLI `0.10.0`; `CFBundleIdentifier=com.trycua.driver`; `CFBundleShortVersionString=0.10.0`; `CFBundleVersion=0.10.0` |
| signature | `codesign --verify --deep --strict` passes; identifier `com.trycua.driver`; Team ID `YCK386LBJ7`; Developer ID Application `Cua AI, Inc. (YCK386LBJ7)` |
| notarization | Gatekeeper accepts the app as `Notarized Developer ID` |
| daemon | running as PID `7384`; `standard (built_in_default)` |
| policy layers | user configured/active `false/false`; managed `false/false`; session configured/approved `false/false`; all reported valid |
| doctor | exit `0`, `ok: true`; every binary/install/home/telemetry/legacy-layout probe is `ok` |
| `permissions status --json` | Accessibility `true`; Screen Recording `true`; capturable `true`; attribution `driver-daemon`; exact signed executable path above |
| daemon `check_permissions({prompt:false})` | byte-for-byte the same permission booleans and source identity; exit `0` |
| forced release check | cache bypassed; current `0.10.0`; latest `0.10.0`; `update_available=false`; source `github_releases` |

The official [installation contract](https://cua.ai/docs/how-to-guides/driver/install) states that
the application bundle identity is the macOS TCC authority and that daemon-backed permission
status reports that driver's grants. The live results therefore do not describe a terminal or IDE
grant. No permission grant, TCC reset, policy edit, daemon restart, or mode change was performed.

### Reproduced blocker and classification

The prior cook recorded the same failure on MCP and CLI. This re-audit reproduced it live through
both direct CLI spellings:

```text
$ cua-driver call health_report '{}'
Permission denied: tool 'health_report' has no reviewed risk classification
exit 1

$ cua-driver health_report '{}'
Permission denied: tool 'health_report' has no reviewed risk classification
exit 1
```

At the same time, `cua-driver list-tools` registers `health_report`, and `cua-driver describe
health_report` describes a single-call end-to-end diagnostic over binary version, platform,
session, bundle identity, TCC, AX capability, and screen capture. The official generated
[MCP tool reference](https://cua.ai/docs/reference/cua-driver/mcp-tools) describes the same stable,
read-only health model. The official [CLI contract](https://cua.ai/docs/reference/cua-driver/cli-reference)
states that `cua-driver call` invokes a tool through the running daemon, while the official
[process model](https://cua.ai/docs/reference/cua-driver/process-model) states that MCP and CLI
are adapters around that same daemon implementation.

The official [permission-mode contract](https://cua.ai/docs/reference/cua-driver/permission-modes)
states that the reviewed built-in tool/risk map is the first authorization layer, an unknown tool
without a reviewed risk class is denied, and the authorization decision precedes dispatch. The
live standard-mode status rules out a user policy, managed policy, or bounded session manifest as
the source of this denial. Thus CuaDriver `0.10.0` has a registration/authorization-metadata defect:
the documented read-only tool exists, but its built-in reviewed risk classification is absent.
The handler never runs.

This is not a failed TCC, driver identity, installation, AX, or screen-capture result:

- exact signed identity, daemon attribution, and installation probes pass;
- both independent TCC surfaces execute and agree on Accessibility, Screen Recording, and live
  ScreenCaptureKit capturability;
- `health_report` returns no schema, `overall`, or per-check result at all because authorization
  rejects it first;
- no AX or screenshot probe was attempted by this re-audit, so no failed AX/capture result exists.

Switching to `bounded` or `unrestricted`, using `--dangerously-bypass-approvals`, asserting an
unreviewed human session manifest, changing global/user/managed policy, or weakening the GUI
evidence would not repair the missing built-in classification and is forbidden.

## Mandatory replacement preflight

This section replaces only step 4's requirement for an executing `health_report` in the first
amendment. All other steps, ordering, ownership checks, cleanup, and stop conditions remain. A
fresh recovery cook must complete every item below before its additive timer starts:

1. Fetch and prove local HEAD, tracking ref, and a newly queried live feature ref all equal the
   exact new amendment output SHA from the Issue #7 publication. Prove clean tracked/index state,
   `.artifacts` absent, ports `4174`–`4178` free, no issue process, required ancestry, and every
   frozen identity above.
2. Re-prove exact executable resolution and CLI/bundle versions. Run `codesign --verify --deep
   --strict`, inspect bundle identifier/version metadata and Team ID, and require exact identity
   `com.trycua.driver` / `YCK386LBJ7` / `0.10.0` at the signed application path.
3. Require `cua-driver status` to report the running daemon in `standard (built_in_default)` with
   no active/configured user policy, managed policy, or session policy. Do not restart into another
   mode and do not create or claim a reviewed bounded manifest.
4. Run `doctor --json` and require exit zero, `ok: true`, and every reported probe `ok`. Run
   `permissions status --json` and daemon `check_permissions` with `prompt:false`; require both to
   exit zero and agree exactly on Accessibility `true`, Screen Recording `true`, capturable `true`,
   `driver-daemon` attribution, daemon PID, and signed executable path. Any disagreement stops.
5. Run a forced `check-update --no-cache --json`; require installed/current/latest consistency.
   A newer release is a context change and stops for a new audit rather than silently updating.
6. Outside the repository, create a private disposable temporary root, deterministic neutral local
   page, isolated browser profile, and owned loopback server on an exact free port. The page must
   expose at least two labeled focusable controls and an AX-visible status whose value changes only
   when the second control receives a real keyboard activation.
7. Start a declared strict `window` CuaDriver session (or `auto` only if the current live schema
   requires it, with effective scope remaining `window` and no escalation). Create/launch a new
   driver-owned isolated browser instance in the background. Never attach to, copy, inspect,
   restart, close, or mutate a personal profile, personal tab, or foreign browser process.
8. Record a neutral foreign frontmost application and prove it remains frontmost throughout.
   Resolve the isolated browser's exact PID and `window_id`, prove that window belongs to that PID,
   bind only that native window, and refuse heuristic/ambiguous binding. Typed browser state may be
   used read-only to prove the exact local page; typed browser mutation and DOM dispatch may not
   substitute for the native functional probe.
9. Call `get_window_state` on the exact PID/window and require a real screenshot plus a
   non-degraded AX tree containing the labeled neutral controls. Snapshot immediately before and
   after every action. Establish initial focus on the first neutral control through a window-scoped
   CuaDriver AX action, then deliver an actual background `Tab` key through CuaDriver to the exact
   target PID/window. Require the action response and after-snapshot to show focus moved to the
   second labeled control while the foreign frontmost app did not change.
10. Deliver the control's real background keyboard activation (`Space` or `Enter`, whichever its
    native semantics require) through CuaDriver, still against the exact PID/window. Require a new
    screenshot and AX state to show the deterministic status change and retained focus. Transport
    completion, an inferred accessible name, a DOM event, Playwright, JavaScript, or an unchanged
    snapshot is not evidence.
11. End the session; stop only the recorded owned browser/server processes; remove only the exact
    disposable profile/root; and prove the temporary port free, no owned process remains, the
    foreign frontmost app is unchanged, repository tracked/index state is clean, `.artifacts` is
    absent, and all frozen identities/evidence still match.
12. Only after steps 1–11 pass may the cook create/start the additive shared/final timer segment
    from cumulative used `1681.011075417` and remaining `5518.988924583` seconds, then begin the
    already-authorized surviving manual Gate C order `Vite -> Next`.

No `delivery_mode:"foreground"`, desktop scope, `escalate_session`, activation script, `open`,
mutating AppleScript, raw CGEvent/click shim, synthetic DOM event, Playwright substitution, or
personal browser state is permitted. A denied `health_report` is no longer a stop condition by
itself after this exact replacement passes; no other diagnostic failure is waived.

## Replacement stop conditions

Stop before the timer and retain the current no-winner if any of the following occurs:

- Git/ref equality, clean state, absence, port/process ownership, ancestry, frozen identity, or
  retained-index verification fails;
- signed identity/version differs, codesign/Gatekeeper/doctor fails, daemon mode/policy posture
  differs, a new release exists, either permission is false, capturability is false, or the two
  permission surfaces disagree in any field;
- the browser/profile/page is not disposable and isolated, PID/window/page binding is not exact,
  screenshot or AX state is missing/degraded, or any personal/foreign browser state is exposed;
- background Tab is not actually delivered, focus movement is not observed in the bracketed AX
  and screenshot state, keyboard activation is not observed, or the frontmost app changes;
- any step would require foreground delivery, desktop escalation, a synthetic/DOM/browser
  automation substitute, unrestricted mode, approval bypass, policy mutation, or a claimed human
  bounded policy;
- cleanup, exact OS/browser restoration, owned-process shutdown, or final repository/frozen-state
  revalidation fails.

After preflight, every original recovery stop condition still applies: missing or unequal Vite and
Next evidence, unobservable real VoiceOver spoken output, simulated/inferred keyboard or manual
facets, failure to restore actual Chrome zoom/JavaScript or macOS VoiceOver/Reduce Motion/frontmost
state, exhausted budget, missing raw scoring inputs, or any need to edit a frozen surface retains
explicit no-winner with all scores null.

## Preserved recovery and decision boundary

Astro remains eliminated and cannot be resurrected, changed, rerun, or scored. Vite and Next
candidate source, manifests, locks, modes, common/fixture inputs, score anchors, old automated
evidence, and old retained evidence remain read-only. New evidence must be additive, equal, and
actual. The required surviving order remains `Vite -> Next`.

For each survivor, manual Gate C still requires actual background macOS keyboard with bracketed
visual/AX proof; named macOS VoiceOver with observable real spoken output through Caption Panel or
Speech History; actual Chrome 200% native zoom/reflow; actual macOS Reduce Motion with recorded
prior value and restoration; and actual JavaScript-disabled Chrome/profile comprehension. No axe,
Playwright emulation, viewport change, CSS transform, request blocking, CSP injection, DOM
mutation, synthetic transcript, or inferred result can substitute.

Gate D remains fail-closed. Complete equal manual records do not create missing numeric cold/warm,
RSS, client-JS, or authoring samples. A winner and numeric scores are permitted only if every
binding raw input already required by the plan is complete, valid, comparable, retained, and
within the unchanged cap. Otherwise ADR-005 remains `Proposed`, decision remains `no-winner`, and
all scores remain null. A fresh independent exact-head review is mandatory after any recovery
output and before a PR or merge.

Barrier B remains closed. Moving Issue #7 from `blocked-dependency` to `ready to cook` authorizes
only this exact recovery attempt; it does not assert that the new cook preflight or manual Gate C
has passed and does not open Barrier B, score, selection, acceptance, PR, or merge authority.

## Preserved exclusions

No Issue #8+ work, cloud, AWS, Terraform, root `Makefile`/`.gitignore`, runner, portal, publisher,
signing, tag, release, candidate/source/lock/mode/common/fixture/anchor change, old-evidence rewrite,
fresh automated candidate run, Astro action, scoring, winner selection, PR, or merge is authorized
by this audit. Global CuaDriver policies and daemon permission mode remain untouched.
