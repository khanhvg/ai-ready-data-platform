---
title: "Recovery Readiness Amendment III — Chromium Typed-Route Feasibility Re-audit"
issue: 7
phase: fresh-independent-chromium-preflight-recovery-reaudit
status: blocked
readinessVerdict: BLOCKED
currentRecoveryInputSha: "610eed48941437feaa7472fb6d371067c238c088"
cookSourceAndTestedSha: "02051ed94d4e2c920f8a65a4ecab0e08a82b946a"
retainedEvidenceAttestationSha: "1d3cdf769e9c0b3ee1fa0238309f7328c0908346"
newRecoveryInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: none
preflightObservationRoute: none
discardedProbe: fail
remainingSharedSeconds: "5518.988924583"
barrierB: closed
auditedAt: "2026-07-21"
---

# Recovery Readiness Amendment III — Chromium Typed-Route Feasibility Re-audit

## Additive verdict

`BLOCKED`. The prior recovery cook stopped on an Amendment II requirement that is incompatible
with the current official CuaDriver Chromium contract: a process-level native AX tree is not the
page-content semantic authority for a supported Chromium page. Exact native window state proves
window identity, browser chrome structure, and a real screenshot. Exact-bound typed
`semantic_v2` browser state proves labelled page controls, page focus, and page state.

That classification does not by itself reauthorize another cook. The one owner-directed,
discarded outside-repository feasibility probe required by this re-audit failed before exact
page binding or any page keyboard action: the approved official isolated-profile preparation
route changed the system-frontmost application from the recorded foreign app to the prepared
Chrome process. A strict `window` session cannot accept that focus change, and this audit was
forbidden to retry, foreground, activate, or relax the route.

Accordingly, this amendment does **not** activate the proposed Chromium replacement, does not
supersede Amendment II's live recovery gate, and grants no next-cook scope. Issue #7 remains
blocked, the retained no-winner remains binding, and Barrier B remains closed.

## Exact recovery input and repository proof

Before the discarded probe and before this amendment was written, a fetch plus a separately
queried live ref proved exact equality:

```text
local HEAD:  610eed48941437feaa7472fb6d371067c238c088
tracking:    610eed48941437feaa7472fb6d371067c238c088
fresh live:  610eed48941437feaa7472fb6d371067c238c088
branch:      feature/issue-5-02-web-spike
```

The tracked tree and index were clean, `.artifacts` was absent, ports `4174` through `4178` were
free, and there was no candidate server, preview server, Gate C runner, or candidate observation
process. The audit controller/logger processes were control-plane processes, not candidate or
manual-evidence processes, and were not signalled.

Exact Issue #6 M2 `24be3b34c6b0fcdbd07c5800dcab349054e34713`, frozen candidate
source/tested `02051ed94d4e2c920f8a65a4ecab0e08a82b946a`, and retained cook
attestation `1d3cdf769e9c0b3ee1fa0238309f7328c0908346` are ancestors. Git produced an
empty diff from frozen source/tested through the recovery input across candidate sources,
manifests, locks, common, preview, modes, Issue #6 fixtures, and score anchors. Git separately
produced an empty diff from the retained attestation through the recovery input across retained
evidence, the retention index, ADR-005, scorecards, and the issue-local Make fragment.

### Revalidated frozen identities

| Surface | Exact identity |
|---|---|
| all candidates | Git tree `f2ec341820db157e6bc7fb12e75844ee2730ec12` |
| Astro candidate | Git tree `4b352a31354cc12bebcad9f0a461000c167e5f11`; lock SHA-256 `78677d1a272fdc5c9758810343f89e82f2914625a03259a575208fe1fafef760` |
| Next candidate | Git tree `85777043224f7f00ec944642e3531c1d891e5ec3`; lock SHA-256 `4939388a7e7290ec640e418afac94dc68cfba7bf6b5692df61317b4c95de2e8b` |
| Vite candidate | Git tree `f3b87dab9a43f41c8a31d67fb44f709b28f7e377`; lock SHA-256 `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` |
| candidate modes | SHA-256 `2957c84624ef16d0ebb037ea3fde66d20a0d2dae6d0d049b1e9c4bb7a8ce3181` |
| common | Git tree `f00fe97715df5dd469302994349fb95c9412482b` |
| neutral preview | Git tree `21376a30fe5f2b5b08f79eeb289bcd1e89663d79` |
| retained evidence | Git tree `15bef78b9b2390ad30ded1bab729e21eca61c7bd` |
| retained Gate A | Git tree `76751df92c6bb9e8b0417e9023bb97cf6273355f` |
| retained Gate C | Git tree `b10d77b72039278f05fa84d3472d5cdfd82c35a7` |
| retention index | blob `026cd7b3d0bd54d6981cdaa1aa7b6ae67cfeba3e`; SHA-256 `58d46e55e21bf02b3abf65a3aaef0442c8e823ef2cb5ffc1da75e2441c262ee6` |
| score anchors | blob `0de35b53685ef6d4d30b8d0486b416f563be9cb8`; SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` |

All candidate files and the mode registry retain Git mode `100644`. The retention index again
rehashed `106/106` entries with exact byte counts and SHA-256 values, binds both source and tested
to `02051ed94d4e2c920f8a65a4ecab0e08a82b946a`, and retains `no-winner`.

The four Issue #6 fixtures remain exact:

| Path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

## Timer identity

The immutable closed timer remains blob `78b04abed94b5ba97250451282666124621535ad`,
SHA-256 `d1b452256c1f89a3721f98856c1c1e9fb465249dcc4b4de4b716a0a45ecccbb0`.
It records budget `7200.000000000`, monotonic start `217149772843083`, monotonic end
`218830783918500`, no pauses, and active time exactly `1681.011075417` seconds.

```text
7200.000000000 - 1681.011075417 = 5518.988924583
```

This re-audit created no additive timer. Waiting, diagnostics, the discarded probe, cleanup, and
publication consume no timer credit and cannot reset the closed record. Remaining shared/final
time is still exactly `5518.988924583` seconds.

## Recovery-cook v2 stop classification

The audited v2 log is
`.hermes/logs/claudekit/issue-7-manual-gate-c-recovery-cook-v2.log`; its public Issue #7 report is
comment `5031406988`. They agree on the following bounded facts:

- the sole input was `610eed48941437feaa7472fb6d371067c238c088`;
- replacement diagnostics passed, `health_report` was not called, and the daemon remained
  `standard (built_in_default)` with no user, managed, or session policy;
- the disposable strict-window page used isolated Chrome PID `39182`, native window `13112`, and
  loopback port `4199`;
- exact native `get_window_state` returned a real screenshot and a non-degraded process-level AX
  tree;
- that native process tree did not contain the two labelled neutral page controls, while it did
  contain Chrome/macOS menu and recent-item metadata unrelated to the neutral page;
- no Tab, activation, timer, candidate action, or repository write occurred; and
- the session, browser, server, profile, capture, and root were fully cleaned.

The stop was honest under Amendment II's literal wording, but its inference was too broad. A real
native screenshot proves capture. A populated, non-degraded native tree proves process-level AX
delivery. Neither result promises that a supported Chromium renderer's labelled page controls
will appear in that process tree. The unrelated menu/recent-item text is browser/OS metadata, not
page evidence. It is private/unrelated content that must never be retained raw, quoted, indexed,
or used to satisfy a page assertion.

Fresh live diagnostics in this re-audit independently matched the replacement baseline. The CLI
resolved to `/Applications/CuaDriver.app/Contents/MacOS/cua-driver`; CLI and bundle versions were
`0.10.0`; bundle identifier was `com.trycua.driver`; Team ID was `YCK386LBJ7`; strict codesign
verification passed; and Gatekeeper accepted a Notarized Developer ID application. The daemon
remained PID `7384` in `standard (built_in_default)` with no configured/active user, managed, or
session policy. `doctor --json` returned `ok: true` with every probe `ok`. `permissions status
--json` and daemon `check_permissions(prompt=false)` agreed exactly on Accessibility `true`,
Screen Recording `true`, capturable `true`, `driver-daemon` attribution, daemon PID `7384`, and
the signed executable path. The forced uncached release check reported current/latest `0.10.0`,
`update_available=false`, source `github_releases`. `health_report` was not called. No daemon,
policy, permission, or release state was changed.

## Current official Chromium contract

The loaded CuaDriver `SKILL.md`, `MACOS.md`, and `BROWSER.md` establish this route for supported
Chromium page content:

1. select an exact native `(pid, window_id)`;
2. bind with typed `get_browser_state` and require `status: ok`,
   `binding_quality: exact`, and `mutation_allowed: true`;
3. obtain fresh tab/session-scoped `semantic_v2` snapshots, following any opaque continuation to
   completeness;
4. use native `get_window_state` for window identity, browser chrome structure, and the actual
   native screenshot; and
5. use real CuaDriver window-scoped background key delivery to the exact PID for OS keyboard
   evidence, with a fresh native screenshot and fresh exact-bound `semantic_v2` state after every
   action.

A sparse Chromium native tree may be retried once, but it is not the labelled page-content
authority. Typed browser pointer/click/type mutation, Playwright, a trusted CDP pointer route, or
a synthetic DOM event cannot substitute for the required native background keyboard event.

If independently proven without a frontmost change, this hybrid would be the correct narrow
replacement for Amendment II's process-tree label requirement. Raw process AX output would be
discarded; only reduced role/count/window structure could be recorded. The feasibility probe did
not reach that proof, so this amendment does not put the replacement into force.

## One discarded outside-repository feasibility probe

### Bounded setup

The probe used only disposable state outside the repository:

| Item | Exact fact |
|---|---|
| strict session | `issue7-chromium-hybrid-610eed48`; `capture_scope=window`, effective scope `window`, desktop locked |
| neutral server | PID `81856`; `127.0.0.1:4207`; deterministic page SHA-256 `c4fbbc268c43ea8393d5e20edda5ede2ca314a9a061b18615cd221827dcfb5f1` |
| disposable root | `/tmp/issue7-chromium-hybrid.YI8TDP`, mode `0700`, removed after the probe |
| recorded foreign frontmost | Hermes PID `19888`, bundle `com.nousresearch.hermes`; on-screen window `6813`, recorded z-index `105` |
| bootstrap isolated Chrome | PID `2108`, native window `13130`, exact neutral title; driver launch reported `self_activation_suppressed=true` |
| prepared driver-owned Chrome | PID `22962`, native window `13133`, driver-managed isolated profile |

Before launch, Google Chrome was not running. The bootstrap process used a private profile under
the disposable root, `--no-first-run`, `--no-default-browser-check`, disabled sync/background
networking, and only the neutral loopback URL. Its native window belonged to PID `2108`; the
foreign Hermes process remained frontmost after this launch. A typed bind against the bootstrap
window correctly refused with `browser_requires_setup` and performed no mutation.

The audit did not bypass the CLI's approval gate: a non-interactive approval attempt was refused
with `browser-approve requires an interactive terminal`, and no token was minted, exposed, or
persisted. It then used the installed CuaDriver MCP's official host-approved
`browser_prepare(profile.mode=isolated_new, allow_launch=true)` route. The response reported:

```text
prepared=true
prepared_pid=22962
endpoint owner PID=22962, method=spawned_by_driver
created_profile=true
copied_profile_data=false
changed_preferences=false
displayed_consent_prompt=false
foregrounded_window=false
injected_global_input=false
```

### Fail-closed result

Immediately after preparation, a fresh native `list_apps` identified Google Chrome PID `22962`
as the system-frontmost application instead of the recorded Hermes PID `19888`. The prepared
Chrome window was exact PID `22962` / window `13133`, on-screen, and reported at z-index `292`.
Thus the live native frontmost result contradicted the preparation response's
`foregrounded_window=false` claim and violated the required unchanged foreign identity/z-order.

The audit stopped at that first strict-window failure. It did not bind the prepared window, did
not obtain a `binding_quality=exact`/`mutation_allowed=true` capability, did not request a
`semantic_v2` page snapshot, and delivered no page Tab, Shift+Tab, Enter, or Space. It used no
Playwright, browser click/type/pointer mutation, trusted CDP pointer route, synthetic DOM event,
desktop scope, foreground delivery, activation script, `open`, mutating AppleScript, System
Events mutation, raw CGEvent helper, personal profile/tab, candidate page, timer, or repository
evidence write.

Because the single authorized probe failed before the exact hybrid observation/action loop, this
audit cannot assert `native-window-screenshot-plus-exact-bound-semantic-v2` feasibility and cannot
reauthorize the next Vite manual Gate C cook.

## Cleanup and post-probe proof

Cleanup used only recorded owned resources. Fresh native snapshots before cooperative quit wrote
real `1036 x 777` PNG captures inside the disposable root; raw process/menu trees were never
persisted or retained. CuaDriver background `Cmd+Q` was sent only to exact owned Chrome PIDs. No
foreground retry was taken even when the action response recommended it.

- bootstrap Chrome PID `2108` exited and window `13130` disappeared;
- prepared Chrome PID `22962` exited and window `13133` disappeared;
- the CuaDriver session ended;
- the driver-managed isolated prepared profile auto-removed;
- server PID `81856` stopped cooperatively;
- exact root `/tmp/issue7-chromium-hybrid.YI8TDP`, bootstrap profile, page, and captures were
  removed;
- port `4207` is free and no Google Chrome process remains;
- `.artifacts` is absent and the tracked tree/index remain clean.

The originally recorded foreign-frontmost identity/z-order cannot be claimed unchanged: after
the preparation failure and cooperative Chrome shutdown, fresh observations showed other foreign
user applications becoming frontmost. This audit did not activate or mutate those apps. That
uncontrolled/changed native state is itself a failed strict-posture assertion, not evidence to be
normalized away.

## Preserved gates and exclusions

Amendments I and II remain binding because the replacement route was not proven. Any later owner
decision must start from a new exact audit input and independently resolve the isolated-browser
frontmost discrepancy before another candidate cook. It may not reuse this discarded probe as a
pass.

All other gates remain unchanged: diagnostics and neutral cleanup; timer creation only after a
complete preflight; surviving order `Vite -> Next`; Astro eliminated; actual macOS keyboard;
observable actual VoiceOver output/caption; actual Chrome 200%; actual macOS Reduce Motion;
actual no-JS; equal evidence; frozen bytes; full restoration; fail-closed Gate D; ADR-005
`Proposed`/`no-winner`; and fresh independent exact-head review.

No Issue #8+ work, candidate/manual retained evidence, scoring, winner, ADR/scorecard, source,
manifest, lock, mode, common, fixture, anchor, retained-evidence, root `Makefile`/`.gitignore`,
runner, portal, AWS/cloud/Terraform, publisher, signing, tag, release, PR, or merge is authorized
or performed. Issue #7 remains `blocked-dependency`; Barrier B remains closed.
