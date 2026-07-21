---
title: "Recovery Readiness Amendment IV — Bounded Foreground with Hermes Restoration"
issue: 7
phase: fresh-independent-bounded-foreground-recovery-reaudit
status: recovery-ready
readinessVerdict: RECOVERY_READY
currentRecoveryInputSha: "ffd248fb413638208702eee259a12ac679127175"
cookSourceAndTestedSha: "02051ed94d4e2c920f8a65a4ecab0e08a82b946a"
retainedEvidenceAttestationSha: "1d3cdf769e9c0b3ee1fa0238309f7328c0908346"
newRecoveryInputSha: "exact-amendment-output-sha-attested-in-issue-7-publication-comment"
authorizedScope: next-vite-manual-gate-c-and-gate-d
foregroundAuthorization: bounded-isolated-surfaces-with-hermes-restoration
discardedProbe: pass
hermesRestoration: pass
remainingSharedSeconds: "5518.988924583"
barrierB: closed
auditedAt: "2026-07-21"
---

# Recovery Readiness Amendment IV — Bounded Foreground with Hermes Restoration

## Additive verdict and exact supersession

`RECOVERY_READY`. The owner explicitly authorized the narrowly bounded foreground transition in
Issue #7 comment
[`5032654106`](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5032654106)
after blocked audit output `ffd248fb413638208702eee259a12ac679127175`. A fresh discarded
outside-repository probe passed the exact native-window, typed-semantic, real-native-key, cleanup,
and Hermes-restoration route defined below.

This fourth additive amendment supersedes only Amendment III's requirement that a foreign
frontmost application remain unchanged while isolated Chromium is prepared and tested. The exact
driver-owned isolated Chrome process/window may be system-frontmost during neutral preflight and
the future Vite/Next manual Gate C browser segments. Actual macOS VoiceOver and the exact System
Settings -> Accessibility -> Display surface may likewise be frontmost only during their required
checks. Before every bounded segment the controller must record the exact current Hermes
PID/window fingerprint, and after every segment and final cleanup it must restore that same window
with CuaDriver `bring_to_front` and verify the fingerprint and system-frontmost identity.

No other Amendment I, II, or III gate is weakened. In particular, exact signed driver identity,
standard policy, dual TCC agreement, current release, disposable isolation, exact browser binding,
`semantic_v2` page authority, exact-window native screenshots, real native keys, actual VoiceOver
output, actual Chrome 200%, actual macOS Reduce Motion, actual no-JS, equal Vite -> Next evidence,
full restoration, frozen bytes, the shared timer, fail-closed Gate D, and fresh independent
exact-head review remain mandatory.

This audit did not run candidate Gate C or Gate D, start a timer, score a candidate, select a
winner, change source/locks/modes/common/fixtures/anchors/evidence/ADR/scorecards, create a PR, or
merge. The retained `no-winner` remains binding until a separately controlled recovery cook
produces complete valid evidence.

The sole new recovery input is the exact commit that first contains this amendment as its only
change. Its full 40-character SHA is attested in the Issue #7 publication comment. A commit cannot
contain its own SHA without a recursive claim, so no parent, abbreviation, branch, tag, `HEAD`, or
later descendant is a valid substitute.

## Exact input, history, and repository proof

The audit fetched before comparison and separately queried the live feature ref. Before this
amendment was written, all three refs were exactly the sole audit input:

```text
local HEAD:  ffd248fb413638208702eee259a12ac679127175
tracking:    ffd248fb413638208702eee259a12ac679127175
fresh live:  ffd248fb413638208702eee259a12ac679127175
branch:      feature/issue-5-02-web-spike
```

Amendments I, II, and III were read from the tracked audit package. Amendment III's v3 route-audit
log is `.hermes/logs/claudekit/issue-7-chromium-preflight-route-reaudit.log`, SHA-256
`157f93a30fd0fdcbfcf407ab981e9b257aa99b826c02d3d1013d8634b12775e1`; its public report is
Issue #7 comment
[`5031566474`](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5031566474).
They agree that the previous official `browser_prepare` route created an isolated Chrome process,
made it system-frontmost, and stopped before exact bind or any key. Its cleanup passed, but the
unchanged-foreign-frontmost rule made that discarded probe fail. The owner comment authorizes only
the bounded transition needed to test that same route with exact restoration.

The tracked tree and index were clean, `.artifacts` was absent, and ports `4174` through `4178`
were free. No candidate server, preview server, Gate C runner, or manual-evidence process existed.
The audit logger/watcher were control-plane processes and were not signalled. Exact Issue #6 M2
`24be3b34c6b0fcdbd07c5800dcab349054e34713`, frozen source/tested
`02051ed94d4e2c920f8a65a4ecab0e08a82b946a`, and retained attestation
`1d3cdf769e9c0b3ee1fa0238309f7328c0908346` are ancestors.

Git produced an empty diff from frozen source/tested through the audit input across every
candidate source/manifest/lock, common, preview, candidate mode, fixture, and score anchor. Git
separately produced an empty diff from the retained attestation through the audit input across
retained evidence, retention index, ADR-005, scorecards, and the issue-local Make fragment.

### Revalidated frozen identities

| Surface | Exact identity |
|---|---|
| all candidates | Git tree `f2ec341820db157e6bc7fb12e75844ee2730ec12` |
| Astro | Git tree `4b352a31354cc12bebcad9f0a461000c167e5f11`; lock SHA-256 `78677d1a272fdc5c9758810343f89e82f2914625a03259a575208fe1fafef760` |
| Next | Git tree `85777043224f7f00ec944642e3531c1d891e5ec3`; lock SHA-256 `4939388a7e7290ec640e418afac94dc68cfba7bf6b5692df61317b4c95de2e8b` |
| Vite | Git tree `f3b87dab9a43f41c8a31d67fb44f709b28f7e377`; lock SHA-256 `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` |
| candidate modes | SHA-256 `2957c84624ef16d0ebb037ea3fde66d20a0d2dae6d0d049b1e9c4bb7a8ce3181` |
| common | Git tree `f00fe97715df5dd469302994349fb95c9412482b` |
| neutral preview | Git tree `21376a30fe5f2b5b08f79eeb289bcd1e89663d79` |
| retained evidence | Git tree `15bef78b9b2390ad30ded1bab729e21eca61c7bd` |
| retained Gate A | Git tree `76751df92c6bb9e8b0417e9023bb97cf6273355f` |
| retained Gate C | Git tree `b10d77b72039278f05fa84d3472d5cdfd82c35a7` |
| retention index | blob `026cd7b3d0bd54d6981cdaa1aa7b6ae67cfeba3e`; SHA-256 `58d46e55e21bf02b3abf65a3aaef0442c8e823ef2cb5ffc1da75e2441c262ee6` |
| score anchors | blob `0de35b53685ef6d4d30b8d0486b416f563be9cb8`; SHA-256 `56a15b9babf3e354d5df8279929df0c12e61c2e2e58bc90a8364038b424c9a75` |

All candidate files and the mode registry retain Git mode `100644`. The retention index
independently rehashed `106/106` unique safe non-self-indexed locators with exact byte counts and
SHA-256 values. It binds source and tested to
`02051ed94d4e2c920f8a65a4ecab0e08a82b946a` and retains `no-winner`.

The four Issue #6 fixture bytes remain exact:

| Path | SHA-256 | Git blob |
|---|---|---|
| `contracts/data/retail-golden-v1.json` | `f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc` | `2bdd653ced3ce3f69652d2b873f21699e1e1fc81` |
| `contracts/data/promotion-trust-v1.yaml` | `c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe` | `876789d549276b44a6e64cc4c9a471886fd2752b` |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | `6b5d8a01a59856cdb93a674a0cce5c2bcc9527e0` |
| `tests/fixtures/learning/promotion-trust/manifest.json` | `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | `a4b32032962f5f787d733f7de8cf657491944e37` |

## Timer identity remains exact

The immutable timer remains blob `78b04abed94b5ba97250451282666124621535ad`, SHA-256
`d1b452256c1f89a3721f98856c1c1e9fb465249dcc4b4de4b716a0a45ecccbb0`. It records budget
`7200.000000000`, monotonic start `217149772843083`, monotonic end `218830783918500`, no pauses,
status `closed-with-gate-d-no-winner`, and used time exactly `1681.011075417` seconds.

```text
7200.000000000 - 1681.011075417 = 5518.988924583
```

Diagnostics, the discarded probe, cleanup, restoration, and this publication created no timer and
consume no timer credit. A recovery cook may create an additive timer segment only after its full
preflight passes. The old timer cannot be reset, replaced, paused retroactively, or credited.

## Replacement driver gates

Fresh non-mutating checks passed before the discarded probe:

| Check | Exact result |
|---|---|
| executable/version | `/Applications/CuaDriver.app/Contents/MacOS/cua-driver`; CLI and bundle `0.10.0` |
| signed identity | `com.trycua.driver`; Team ID `YCK386LBJ7`; strict codesign valid |
| Gatekeeper | accepted; `Notarized Developer ID` |
| daemon | PID `7384`; `standard (built_in_default)` |
| policy | user/managed/session configured or active `false`; all valid; no bypass |
| doctor | exit zero; `ok: true`; every probe `ok` |
| dual TCC | both surfaces agree: Accessibility `true`, Screen Recording `true`, capturable `true`, source `driver-daemon`, PID `7384`, exact executable |
| release | uncached current/latest `0.10.0`; `update_available=false`; source `github_releases` |

`health_report` was not called. No driver policy, permission, daemon mode, release, TCC database,
or global configuration was changed. No unrestricted mode, bounded bypass, approval bypass, or
invented token was used.

## One discarded outside-repository foreground probe

### Original Hermes fingerprint and disposable setup

The system-frontmost application before the probe was the required current Hermes application.
Only an exact Hermes-window screenshot was captured; no desktop image was taken.

| Item | Exact fact |
|---|---|
| Hermes app | PID `19888`; bundle `com.nousresearch.hermes`; active/frontmost |
| Hermes window | window `6813`; bounds `x=0, y=33, width=1512, height=949`; on-screen; z-index `15` |
| title-safe fingerprint | UTF-8 bytes `6`; SHA-256 `66e0988d1198afe049f2a5fedbb6e89c20c12dc3bc01ab3f5c13576d624f6e9b` |
| original exact-window screenshot | `1568 x 984`; SHA-256 `bddc2164e039f467ba3bb1a7de0467118da4088eeb9405536d9d3755d6c8fa8f` |
| strict session | `issue7-bounded-foreground-ffd248fb`; `capture_scope=window`; desktop locked |
| disposable root | `/tmp/issue7-bounded-foreground.T0uBd6`; mode `0700`; removed after probe |
| neutral page | SHA-256 `3bb8f6430491e34300190ff07069a1a3af7ea790d204b760630613173c6be261` |
| loopback server | PID `91246`; `127.0.0.1:4207` only |

Google Chrome was not running before setup. CuaDriver launched a bootstrap Chrome PID `91278` /
window `13661` with a private profile inside the disposable root, no first-run/default-browser
prompts, sync/background networking disabled, and only the neutral loopback URL. Hermes remained
frontmost. Read-only typed binding correctly returned `browser_requires_setup`.

The installed MCP host-approved `browser_prepare` route then launched a separate driver-owned
isolated Chrome PID `11955`. It reported endpoint ownership `spawned_by_driver`, exact owner PID,
`created_profile=true`, `copied_profile_data=false`, `changed_preferences=false`, no consent
prompt, and no global input. Chrome PID `11955` became system-frontmost, exactly as the owner now
permits. Its sole on-screen neutral window was PID `11955` / window `13664`, bounds
`x=22, y=55, width=1200, height=905`; no personal Chrome process, profile, tab, or window existed.

Exact typed binding returned `status=ok`, `binding_quality=exact`,
`binding_route=native_cdp_window`, and `mutation_allowed=true`. The bound tab was navigated only to
`http://127.0.0.1:4207/` as setup. No Playwright, `browser_click`, `browser_type`,
`browser_pointer`, trusted pointer, synthetic DOM event, or browser mutation was used for the
focus/activation proof.

### Hybrid semantic, screenshot, and native-key proof

Every semantic snapshot was fresh, complete, `semantic_v2`, with `12` selected nodes and zero
omissions. Every visual was a fresh native exact-window `1568 x 1183` PNG. Process/menu AX was not
retained; native state was reduced to exact window/capture metadata. All action calls named exact
PID `11955`, window `13664`, and the declared strict-window session. Frontmost checks after each
successful action remained exact Chrome PID `11955`.

An initial background Tab was honestly rejected as proof: the driver returned
`effect=unverifiable` with foreground escalation, the new screenshot hash was
`eba6d424fb114a512d89716a0cdc9004388482bbcf72a3b1a366054de844b4af`, and fresh semantic state
still showed Alpha focused. No no-op was relabelled as success.

The owner-authorized foreground native-key route then passed:

| Step | CuaDriver native action | Fresh `semantic_v2` result | Exact-window screenshot SHA-256 |
|---|---|---|---|
| initial | none | Alpha uniquely focused; activation `untouched` | `6e72fbb3ed6bb77823d38c1730bbecd2bab46a45488e48ad7129d582c13e8370` |
| 1 | foreground native `Tab` | Beta uniquely focused; focus status names Beta; activation `untouched` | `1dc36b2b9d2641331757ce0c052f08b8fc15c89c9bbd2c60f4374b53edaeac00` |
| 2 | foreground native `Shift+Tab` | Alpha uniquely focused; focus status names Alpha; activation `untouched` | `eba6d424fb114a512d89716a0cdc9004388482bbcf72a3b1a366054de844b4af` |
| 3 | foreground native `Tab` | Beta uniquely focused again; activation `untouched` | `1dc36b2b9d2641331757ce0c052f08b8fc15c89c9bbd2c60f4374b53edaeac00` |
| 4 | foreground native `Space` | Beta retains focus; activation becomes `beta-active` | `0b3af7544fde76030e4dbbe98ea4bae39750c1720e5edc8560d74e96d36bd874` |

The key responses used CuaDriver's native `key_events_fg` path. The observable page state changed
only after real native Space activated the focused Beta button. Semantic state plus exact native
window pixels independently prove focus and activation; transport completion alone was not used.

### Exact cleanup and Hermes restoration

Cleanup targeted only the recorded isolated resources. The prepared Chrome window was closed
cooperatively through its exact frontmost native Quit menu after `Cmd+Q` proved insufficient; the
queried Quit-only menu fragment was discarded and no raw process/menu AX was retained. The
bootstrap Chrome exited through exact foreground-delivery `Cmd+Q`. The session ended, the
driver-owned prepared profile was lifecycle-cleaned, server PID `91246` stopped cooperatively,
and the exact disposable root, bootstrap profile, page, and all captures were removed. PIDs
`91246`, `91278`, and `11955` had no live non-zombie process, port `4207` was free, and Chrome was
not running.

Only then was CuaDriver `bring_to_front(pid=19888, window_id=6813)` used. Fresh native state proved
Hermes PID `19888` system-frontmost and the exact original window `6813` on-screen with unchanged
bounds, z-index, title byte count, and title hash. A fresh exact-window screenshot was `1568 x 984`
with SHA-256 `6a6484d9bc1542836fd5bc01125546aeebc67a6b3e861978d42e0a3cc5c0bb08`;
the capture root was removed. The screenshot hash is not required to equal the original because
the live Hermes content can advance, while the stable PID/window/bounds/title fingerprint is exact.

No desktop capture, desktop-scoped action, unrelated-app action, personal browser state, OS
setting, VoiceOver action, credential, messaging, network destination beyond loopback, candidate
page, timer, or repository evidence write occurred. Every mutating GUI call targeted only the two
isolated Chrome PIDs or the exact recorded Hermes restoration target.

Post-probe checks found ports `4174` through `4178` and `4207` free, no owned probe process, no
running Chrome, `.artifacts` absent, a clean tracked/index state, empty frozen-path diffs, and the
same anchor, retention-index, timer, source/tested, fixture, and retained-evidence identities.

## Mandatory recovery-cook preflight after this amendment

The next cook may start an additive timer only after every item below passes:

1. Fetch and prove local HEAD, tracking ref, and a newly queried live feature ref all equal the
   exact Amendment IV output SHA in the Issue #7 publication comment. Require branch
   `feature/issue-5-02-web-spike`, clean tracked/index state, `.artifacts` absent, ports
   `4174`–`4178` free, no issue-owned candidate/manual process, required ancestry, and every frozen
   identity above.
2. Re-prove exact executable, version, bundle, Team ID, codesign, Gatekeeper, standard built-in
   daemon policy, all doctor probes, dual non-prompting TCC agreement, and uncached current release.
   Do not call `health_report`, change policy, change permission mode, use unrestricted/bounded
   bypass, reset TCC, or attach personal browser state.
3. Before each bounded segment, record the current exact Hermes PID/window, bounds, title-safe
   fingerprint, frontmost identity, and exact-window screenshot hash. If the original Hermes
   window is unavailable or differs before work begins, stop for owner direction.
4. For browser preparation and manual browser checks, use only a driver-owned isolated Chrome
   profile/window and owned loopback candidate page. Exact isolated Chrome may be foreground.
   Require exact native `(pid, window_id)` ownership and typed `status=ok`,
   `binding_quality=exact`, `mutation_allowed=true`. A personal Chrome process/profile/tab/window
   is never a fallback.
5. Use complete fresh `semantic_v2` as labelled page/focus/state authority and fresh native exact-
   window screenshots as visual authority. Deliver real CuaDriver native keys to the exact
   frontmost isolated Chrome PID/window. Bracket every action with fresh semantic and screenshot
   state. Playwright, browser click/type/pointer, trusted CDP pointer, DOM dispatch, JavaScript
   mutation, synthetic events, inferred focus, or transport completion cannot substitute.
6. Retain only sanitized exact target-window screenshots and the minimum semantic/manual record.
   Do not retain a desktop capture, raw process/menu AX, personal/foreign app content, cookies,
   storage, credentials, unrelated titles, or profile paths. Never read or act on a personal or
   unrelated foreign window; frontmost verification is reduced to the exact allowed process.
7. Actual VoiceOver may be foreground only for the required named screen-reader check. Retain
   actual spoken output made observable through Caption Panel or Speech History together with the
   exact target page/window state. Synthetic transcripts and inferred accessible names remain
   invalid.
8. System Settings may be foreground only at Accessibility -> Display for the actual Reduce
   Motion check. Record the prior value, change only Reduce Motion, verify actual candidate
   behavior, and restore and verify the exact prior value. Do not inspect or change another
   settings pane.
9. After each browser, VoiceOver, and System Settings segment, cooperatively close only owned
   isolated browser resources as applicable, restore VoiceOver/browser zoom/JavaScript/Reduce
   Motion to their recorded prior values, use CuaDriver `bring_to_front` only for the original
   Hermes PID/window, and re-prove exact Hermes frontmost identity/fingerprint. Any restoration
   failure stops immediately; final cleanup repeats the same verification.
10. End sessions, stop only recorded owned servers/processes, remove only validated exact
    disposable roots/profiles/captures, and re-prove free ports, no owned process, clean repository,
    `.artifacts` absent, and every frozen/evidence identity unchanged.
11. Only after the whole preflight and first Hermes restoration pass may the cook create an
    additive timer segment from cumulative used `1681.011075417` and remaining
    `5518.988924583`, then run the surviving order `Vite -> Next`.

## Manual Gate C and Gate D remain unchanged

Astro remains eliminated and cannot be resurrected, changed, rerun, or scored. Vite and Next
candidate source, manifests, locks, modes, common/fixture inputs, score anchors, automated Gate C,
and old retained evidence remain read-only. New manual evidence must be additive, actual, equal,
and obtained in order `Vite -> Next`.

For each survivor, Gate C still requires:

1. real macOS keyboard events through CuaDriver with exact target and bracketed semantic/visual
   proof;
2. named actual macOS VoiceOver traversal with observable real spoken output;
3. actual Chrome native 200% zoom with reflow/comprehension review;
4. actual macOS Reduce Motion with prior-value recording and verified restoration; and
5. actual JavaScript-disabled Chrome/profile comprehension review.

Viewport changes, device scale, CSS transforms, screenshot enlargement, Playwright reduced-motion
or no-JS contexts, request blocking, CSP injection, DOM mutation, axe output, synthetic speech, or
inference do not satisfy these checks. Vite and Next records must contain the same facets and
comparable evidence. A missing or unequal facet keeps all scoring closed.

Gate D remains fail-closed. Manual completion does not manufacture the absent numeric cold/warm,
RSS, client-JS, or authoring sample set. Numeric scores or a winner are permitted only when every
binding raw input required by the plan is complete, valid, comparable, retained, and within the
unchanged cap. Otherwise ADR-005 remains `Proposed`, the decision remains `no-winner`, and every
numeric score remains null.

## Stop conditions and preserved exclusions

Stop before or during recovery if exact Git equality/cleanliness/ancestry/frozen identity fails;
driver identity, standard policy, doctor, TCC, or release differs; browser/profile/window binding
is not isolated and exact; a foreign/personal surface is exposed; semantic/native-key evidence is
missing; VoiceOver speech is unobservable; a setting cannot be restored; Hermes exact restoration
fails; evidence is unequal; or the cumulative budget expires. Missing evidence remains missing
and must never be backfilled, inferred, or relabelled.

No Issue #8+ work, candidate/source/manifest/lock/mode/common/fixture/anchor change, old-evidence
rewrite, fresh automated candidate rerun, Astro action, score/winner/ADR/scorecard change during
this readiness audit, root `Makefile`/`.gitignore`, runner, portal, AWS/cloud/Terraform, publisher,
signing, tag, release, PR, or merge is authorized. Issue #7 may move from `blocked-dependency` to
`ready to cook` only after this exact amendment is committed, pushed, freshly proven equal, and
published with the owner authorization plus discarded-probe pass. Barrier B remains closed until
the new cook preflight passes.
