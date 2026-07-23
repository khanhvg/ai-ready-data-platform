---
phase: 6
title: "Stage B real journey and completion integration"
status: pending
priority: P1
dependencies: [5]
effort: "M"
---

# Phase 6: Stage B Real Journey and Completion Integration

## Overview

Implement one Vietnamese promotion-trust journey from exact clean integration
`671201f78024786a9f2eba5e9e5fce7c78b4443d`:

`lesson → controlled failure → fixed released operations → verify → immutable evidence → reset →
completion/progress`.

This is the entire cook scope. It is local-only and uses the released rootless OrbStack runner.
No cloud, shared-core, runner, golden-data, root-Make, README/docs, CI, or container change is
allowed.

## Requirements

### Functional

1. Preserve the shipped Stage A Vietnamese catalog/module/lesson/ten-step routes.
2. Establish deterministic runner state with `small`/seed `42` through the five fixed setup
   operations.
3. Require the learner to select the invalid `claim-common-grain` decision before the controller
   runs released `promotion.configure`.
4. Display the controlled failure as
   `headline-revenue-overweighted` / `METRIC_REFUND_NOT_ACCOUNTED`; infrastructure failures must
   use a separate unavailable/error state.
5. Require the learner to fix the decision to `retain-independent-grains`.
6. Run released `promotion.verify` and require exact
   `insufficient-evidence/no-common-grain`, `four-independent-grains`, empty common keys, and
   `METRIC_REFUND_NOT_ACCOUNTED`.
7. Validate the runner's immutable evidence index/result before creating one bounded,
   schema-valid `learning-evidence-v1` envelope and display only its safe immutable projection.
8. Run released `workspace.reset`; prove ready small/42 and preserved runner progress/evidence.
9. Complete exactly once through `learning-progress-authority-v1`, only after the learner fix,
   successful verify/evidence, and truthful reset.
10. Persist progress/evidence deterministically across reload/controller restart; browser storage
    and route state are never authoritative.

### Security and Resource

- Public listener and lifecycle control listener bind random/fixed test ports on `127.0.0.1`
  only.
- Lifecycle remains authenticated by its existing private control record and child-owned
  self-shutdown; PID values never become signal authority.
- The browser session uses an HttpOnly `SameSite=Strict` cookie plus per-session CSRF. Mutation
  requests require exact loopback Host and exact same Origin.
- Public API paths/methods are closed. JSON bodies are UTF-8, exact-field, duplicate-key-rejected,
  `Content-Type: application/json`, fixed-length, and at most 512 bytes. No transfer encoding.
- Only one mutation may be active. Extra calls return conflict without starting a child.
- Each runner child receives fixed server-owned executable, cwd, argv, and minimal environment.
  Child time is bounded to 125 seconds around the runner's 110-second execute + cleanup contract.
- Captured stdout/stderr are capped at 256 KiB/128 KiB; response bodies are capped at 128 KiB;
  no raw log, absolute path, runner credential, environment, container ID, or private locator is
  returned.
- Shutdown rejects new work, aborts/waits for its owned child, closes public/control ports, removes
  only its owned runtime control/pending records, and preserves progress/evidence.

## Exact Stage B Write Set

Exactly 18 paths are writable:

| # | Action | Path | Purpose |
|---:|---|---|---|
| 1 | Modify | `apps/learning-portal/package.json` | Register fixed Stage B unit/integration/browser scripts; no dependency change |
| 2 | Modify | `apps/learning-portal/scripts/portal-lifecycle.mjs` | Enable Stage B for Issue #10 commands; retain authenticated start/status/down |
| 3 | Modify | `apps/learning-portal/scripts/serve-built-portal.mjs` | Compose static server, authenticated session API, controller, and cleanup |
| 4 | Create | `apps/learning-portal/scripts/verify-stage-b-release.mjs` | Closed write-set/bundle/runtime/evidence verification |
| 5 | Modify | `apps/learning-portal/src/app/app-shell.jsx` | Pass canonical controller state to status/lab UI |
| 6 | Modify | `apps/learning-portal/src/app/portal-status.jsx` | Vietnamese live region for ready/running/failure/verified/reset/completed/unavailable |
| 7 | Modify | `apps/learning-portal/src/contracts/safe-view-model.mjs` | Truthful no-JS/static Stage B-unavailable message |
| 8 | Modify | `apps/learning-portal/src/features/promotion-trust/promotion-trust-lesson.jsx` | Fixed learner controls and safe evidence projection |
| 9 | Modify | `apps/learning-portal/src/main.jsx` | Session bootstrap, fixed requests, reload recovery; no browser authority |
| 10 | Create | `apps/learning-portal/src/server/progress-authority.py` | Atomic adapter importing released progress/completion/evidence functions |
| 11 | Create | `apps/learning-portal/src/server/promotion-trust-controller.mjs` | Closed journey state machine and request admission |
| 12 | Create | `apps/learning-portal/src/server/runner-cli-adapter.mjs` | Fixed operation map, bounded child, pending/evidence reconciliation |
| 13 | Modify | `apps/learning-portal/src/styles.css` | Accessible desktop/narrow interaction/evidence states |
| 14 | Create | `apps/learning-portal/tests/e2e/stage-b.spec.mjs` | Desktop+narrow/keyboard/axe/no-JS real journey |
| 15 | Create | `apps/learning-portal/tests/integration/stage-b-runner.test.mjs` | Real OrbStack operation/evidence/reset/cleanup |
| 16 | Create | `apps/learning-portal/tests/unit/stage-b-controller.test.mjs` | Request/auth/allowlist/failure/recovery negatives |
| 17 | Create | `apps/learning-portal/tests/unit/stage-b-progress.test.mjs` | Progress/evidence/reset/completion/persistence semantics |
| 18 | Modify | `mk/issue-5/i5-05.mk` | Replace Stage B blockers with thin Issue #10 delegates |

Any 19th path, delete, package-lock change, dependency addition, generated tracked output, or
write outside this table stops cook.

Read-only inputs include the shipped portal; `apps/lab-runner/**`;
`learning/{contracts,labs,lessons,manifests,bindings}/**`; `scripts/learning_contracts/**`;
`contracts/data/**`; root `Makefile`; golden data/code; and the integration Git objects.

## Exact Stage B Commands

Exactly 15 command shapes are authorized for implementation/verification:

| # | Command |
|---:|---|
| 1 | `npm --prefix apps/learning-portal ci --ignore-scripts` |
| 2 | `npm --prefix apps/learning-portal run test:unit` |
| 3 | `npm --prefix apps/learning-portal run test:stage-b-controller` |
| 4 | `npm --prefix apps/learning-portal run test:stage-b-runner` |
| 5 | `npm --prefix apps/learning-portal run build` |
| 6 | `npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0` |
| 7 | `npm --prefix apps/learning-portal run test:stage-b -- --workers=1 --retries=0` |
| 8 | `make runner-test` |
| 9 | `make runner-security-test` |
| 10 | `make runner-race-test` |
| 11 | `make data-contracts-check` |
| 12 | `make portal-test portal-a11y` |
| 13 | `make lesson-e2e LESSON=promotion-trust` |
| 14 | `make local-journey-e2e` |
| 15 | `make learn LESSON=promotion-trust learn-status learn-down learn-down` |

`git diff --check`, exact-path diff checks, protected-tree comparisons, secret/private-path scans,
`git status --short`, and local/tracking/live equality are audit checks rather than product command
authority.

## Controller and Request Contract

### Browser Surface

The loopback server exposes only:

- `GET /_stage-b/session`: issue/read local session; return safe controller/progress state and
  CSRF token.
- `GET /_stage-b/state`: authenticated safe state/evidence projection.
- `POST /_stage-b/action`: exact body selected from:
  - `{"action":"prepare"}`
  - `{"action":"generate"}`
  - `{"action":"load"}`
  - `{"action":"build"}`
  - `{"action":"export"}`
  - `{"action":"fail","decision":"claim-common-grain"}`
  - `{"action":"fix","decision":"retain-independent-grains"}`
  - `{"action":"verify"}`
  - `{"action":"reset"}`

The browser never sends an operation ID or idempotency key. The server owns the fixed action map,
expected progress revision, runner workspace revision, and stable idempotency key.

### Runner Mapping

The server invokes the released owner CLI only. It sets a fixed app cwd, fixed source import path,
minimal fixed environment, and exactly one registry operation from this map:

`prepare→workspace.prepare`, `generate→retail.generate`, `load→retail.load`,
`build→retail.dbt-build`, `export→retail.export`, `fail→promotion.configure`,
`verify→promotion.verify`, `reset→workspace.reset`.

The `fix` action is a learning decision only and starts no runner process. Unknown/out-of-order
actions fail before runner invocation. The Node controller invokes fixed actions in
`progress-authority.py`; that helper imports the released `scripts.learning_contracts` functions
directly and accepts no browser-controlled module, path, command, or family.

Before a child starts, the adapter atomically writes an owner-private pending record containing
only action, exact operation ID, expected runner revision, and server idempotency key. After
success it validates stdout against the runner evidence `result.json`/`index.json` and commits the
controller record atomically. On restart/response loss it scans only the fixed runner evidence
root with file/count/size/type/link limits and attaches the unique matching committed
operation/revision; zero or multiple matches fail closed. It never parses runner SQLite or edits
runner state.

## Deterministic Journey

1. Initial portal progress is schema-valid `progress-v1`, state `not-started`, revision 0,
   completion null. Runner workspace may have prior immutable history; current content becomes
   deterministic through the fixed sequence and final reset.
2. `prepare` starts progress and returns ready small/42. `generate`, `load`, `build`, and `export`
   must return their released semantic counts/hashes.
3. Learner selects `claim-common-grain`; `fail` invokes `promotion.configure`. The UI announces
   the released controlled failure and `METRIC_REFUND_NOT_ACCOUNTED`. Runner/environment failure
   cannot enter this state.
4. Learner selects `retain-independent-grains`; no runner call occurs.
5. `verify` invokes `promotion.verify`. Exact decision/assertions and immutable runner evidence
   are validated. Progress becomes `verified`; one `learning-evidence-v1` envelope is fsynced and
   atomically renamed.
6. UI renders only immutable evidence ID, run ID, operation ID, decision, assertion statuses,
   dependency SHAs, artifact sizes, and SHA-256 values as text.
7. `reset` invokes `workspace.reset` once. Ready small/42 and preserved
   `evidence.json`/`progress.json` are mandatory.
8. Only then does the progress authority CAS from verified to completed with the verified
   evidence ID. Duplicate reset/completion returns the stored result. Evidence/completion survive
   reload, restart, and later reset.

## Tests Before and After

Fresh tests must first fail against exact integration for missing Stage B behavior, then pass:

- request: wrong method/path/content type/length, transfer encoding, oversized/malformed/duplicate
  JSON, extra/missing fields, foreign Host/Origin, absent/wrong cookie/CSRF, unknown/out-of-order
  action, direct operation ID, command/path/URL/SQL fields, duplicate concurrent mutation;
- runner: one real OrbStack operation plus the complete eight-operation journey, released image
  identity, fixed argv/environment, bounded output/time, evidence index/result verification,
  failure/timeout/conflict, pending-response reconciliation, zero container residue;
- journey: deterministic small/42 state, genuine controlled failure, environment-failure
  separation, required learner fix, exact verify decision/assertions, no completion from hints,
  URL, browser storage, reflected body, raw result, evidence presence, or reset alone;
- evidence/progress: schema and semantic validation through released readers, atomic persistence,
  corrupt/missing/ambiguous evidence rejection, reset preservation, idempotent replay, expected
  revision conflict, completion exactly once;
- browser: one real desktop journey; narrow layout and keyboard-only path; focus and polite live
  status; axe Critical/Serious = 0; reload recovery; safe text-only evidence; no runner credential,
  external request, browser storage authority, or arbitrary input;
- no JavaScript: shipped static Vietnamese lesson/navigation/decision remains usable and explicitly
  states interactive Stage B is unavailable without JavaScript; it never claims completion;
- lifecycle: status while idle/busy, authenticated down, down twice, child timeout/termination,
  public/control port closure, pending-record cleanup, evidence/progress preservation;
- clean checkout: exact `671201f…`, apply only the implementation commits, install/build, run
  focused gates and one real journey, run authenticated down twice, prove zero owned process/port/
  runner-container residue and a clean tracked tree.

## Implementation Steps

1. Create a clean implementation branch/worktree directly from exact `671201f…`; prove clean,
   local/tracking identity, and the 18-path ceiling before the first write.
2. Add all four fresh test files and package/Make delegates; retain intended failing results
   before behavior.
3. Implement the bounded runner CLI adapter and pending/evidence reconciliation.
4. Implement the sole progress/evidence/completion repository as the fixed Python adapter that
   imports released schemas/semantics; do not translate them into a second Node authority.
5. Implement request/session/CSRF/Host/Origin/body/method/concurrency admission and lifecycle
   cleanup in the loopback controller.
6. Connect the shipped Vietnamese lesson UI to fixed actions and canonical server state.
7. Make focused unit/integration tests pass, then the real browser journey and no-JS fallback.
8. Run all 15 commands at one exact head; run scope/protected/privacy/secret/cleanup checks.
9. Run focused code review; fix until Critical=0 and Important=0.
10. Re-run affected gates and clean-checkout smoke after the final fix.

## Acceptance Criteria

- [ ] Exact base is `671201f78024786a9f2eba5e9e5fce7c78b4443d`.
- [ ] Final diff equals the 18-path write set; protected trees are byte-identical.
- [ ] Browser cannot address the runner or select command/operation/path/URL/SQL.
- [ ] All eight released operations run in the fixed order with real OrbStack containment.
- [ ] Controlled failure, learner fix, verify, evidence, reset, and completion order is enforced.
- [ ] Completion requires successful post-action verify and truthful reset; reset is idempotent.
- [ ] One released progress/completion authority persists; evidence is immutable and hash-valid.
- [ ] Request/auth/allowlist, real runner, failure, evidence, reset, persistence, browser, no-JS,
  lifecycle, cleanup, and clean-checkout tests pass.
- [ ] Focused review has Critical=0 and Important=0.
- [ ] No cloud action or unrelated implementation occurs.

## Rollback

Use authenticated `learn-down`, wait for the owned child, prove both loopback ports and runner
containers are absent, preserve progress/evidence, and revert only the 18 Stage B paths. Rebuild
and smoke the shipped Stage A static/no-JS portal. Never delete runner audit/evidence, completed
progress, unrelated artifacts, OrbStack state, or shared contracts.

## Next Steps

After Phase 6 is green, Phase 7 performs only exact-head Lane S review/evidence/PR readiness. It
does not add product scope.
