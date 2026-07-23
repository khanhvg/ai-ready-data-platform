# Dependency and Release Gates

## Current Immutable Register

This register supersedes the pre-release Stage B rows. Historical Stage A plans/reports keep their
original statements.

| Dependency | Reviewed head | Released/merge SHA | Verified immutable fact | Stage B authority |
|---|---|---|---|---|
| Portal Stage A / PR #31 | `473f54c2e0879d3037cbed25b2e7a3f0626d558d` | `041d4ca866e927a331e159fdf8216838b481a595` | Merge tree equals reviewed tree `1ad11b31c45b282bd179f76054ad215484f81060`; focused review Critical/Important = 0; clean-checkout post-merge browser smoke PASS | Accepted portal base |
| Runner / Issue #9 / PR #32 | `86a6c259ad384591777cf1d46f2f6c9ea6327361` | `671201f78024786a9f2eba5e9e5fce7c78b4443d` | Merge tree equals reviewed tree `e2c5166d549d5e8d4a3f6962afe0a2567f6b9566`; 66/66; all eight operations; dbt multiprocessing; evidence/reset; clean-checkout smoke; zero residue | Accepted runner release |
| Stage B implementation base | N/A | `671201f78024786a9f2eba5e9e5fce7c78b4443d` | First parent is Stage A merge `041d4ca…`; second parent is reviewed runner head `86a6c25…` | Exact cook base |
| Readiness audit input | N/A | `8c77957ad3be84dc97e4633cdafd898ea9e431fa` | Required clean plan input on `plan/issue-10-promotion-portal` | Amendment provenance |

Live evidence:

- Lane S authority:
  <https://github.com/khanhvg/ai-ready-data-platform/issues/10#issuecomment-5056144073>
- Stage A merge and post-merge smoke:
  <https://github.com/khanhvg/ai-ready-data-platform/issues/10#issuecomment-5056334157>
- Runner shipped handoff:
  <https://github.com/khanhvg/ai-ready-data-platform/issues/9#issuecomment-5056615622>
- PR #31: <https://github.com/khanhvg/ai-ready-data-platform/pull/31>
- PR #32: <https://github.com/khanhvg/ai-ready-data-platform/pull/32>

## Released Runner Contract

The release is an owner CLI/private transport, not a portal HTTP API:

- CLI: `python3.12 -m lab_runner run <closed-operation> --idempotency-key <key>`.
- Private request schema: exactly `operationId`, `idempotencyKey`, `workspaceRevision`.
- Registry: exactly eight zero-argument operations, 110-second execution limit each.
- Runtime: linux/arm64, non-root `65532:65532`, read-only root, network none, all capabilities
  dropped, no-new-privileges, 64 PIDs, 512 MiB memory/no swap, two CPUs, 256 MiB workspace.
- Evidence: owner-private `0700` run directory containing only `0600` `result.json` and
  `index.json`; result is at most 65,536 bytes; index binds locator, size, and SHA-256; publication
  is atomic and immutable; reconciliation verifies exact bytes.
- State: durable SQLite CAS plus append-only hash-chained audit; one current workspace revision;
  same idempotency key with the same exact request replays the committed result, changed request
  conflicts.
- Reset: `workspace.reset` preserves runner `progress.json` and `evidence.json`, restores
  deterministic `ready`/`small`/`42`, and runner audit/evidence history remains immutable.

The portal must not call the currently unused runner loopback helper or claim the general
learning-platform OpenAPI surface is implemented by Issue #9. The Stage B adapter invokes only
the released owner CLI, serializes mutations, uses fixed server-owned paths/environment, captures
bounded stdout/stderr, and reconciles any pending call from the runner's immutable evidence
index/result before retrying.

## Gate A — Static Portal Authority

Historical Gate A is completed by PR #31. Its exact 33-path/18-command/85-input recovery contract
remains in the Stage A amendment and Phase 1–4; it is not reopened or altered by Stage B.

## Exact Released Operations

| Order | Fixed portal action | Released operation ID | Required result |
|---:|---|---|---|
| 1 | `prepare` | `workspace.prepare` | `state=ready`, `profile=small`, `seed=42` |
| 2 | `generate` | `retail.generate` | 18 tables and deterministic small/42 manifest |
| 3 | `load` | `retail.load` | 18 loaded tables |
| 4 | `build` | `retail.dbt-build` | 51 models; released `dbtRunner` path |
| 5 | `export` | `retail.export` | validated golden release assets/manifest |
| 6 | `fail` | `promotion.configure` | `controlledFailure=headline-revenue-overweighted` |
| 7 | `verify` | `promotion.verify` | exact decision and both released assertions |
| 8 | `reset` | `workspace.reset` | ready small/42 plus preserved progress/evidence |

Browser input may choose only the fixed portal action and, at the lesson decision step, one of
`claim-common-grain` or `retain-independent-grains`. The controller map above is closed and
server-owned. Unknown actions, fields, methods, paths, content types, origins, hosts, sessions,
CSRF tokens, and concurrent mutations fail without invoking the runner.

## Promotion-Trust Binding

The controlled failure is not an infrastructure failure. `promotion.configure` commits the
released `headline-revenue-overweighted` starter and its expected
`METRIC_REFUND_NOT_ACCOUNTED` evidence. The learner first selects `claim-common-grain`; the
controller records that bounded learner action but does not pass it to the runner. The learner
then fixes the decision to `retain-independent-grains`.

`promotion.verify` is admitted only after that learner action and the five deterministic
small/42 setup operations. Verification passes only when:

1. decision is exactly `insufficient-evidence/no-common-grain`;
2. `four-independent-grains` passes with `observedCommonKeys=[]`;
3. `METRIC_REFUND_NOT_ACCOUNTED` passes with the independent returns-grain observation;
4. the runner result and immutable index agree on run ID, operation, revision, size, and SHA-256;
5. released contract, fixture, verifier, portal merge, runner release, and implementation SHA
   identities are retained in the learning-evidence envelope.

Environmental errors (`RUNNER_ENGINE_UNAVAILABLE`, resource/containment failures, timeout,
conflict, corrupt/missing evidence) are separate unavailable/error states and never satisfy the
controlled failure or completion.

## Progress, Evidence, Reset, and Completion

- `progress-v1` is the only learner progress document.
- `learning-progress-authority-v1` is the only completion authority.
- Browser route, URL, storage, reflection, hint, displayed evidence, or raw runner result cannot
  complete.
- The portal progress repository persists with atomic write/fsync/rename under one owner-private,
  fixed Issue #10 state root. Browser state is presentation-only.
- The controller materializes one schema-valid `learning-evidence-v1` envelope from the
  hash-verified committed `promotion.verify` result. It never edits runner evidence.
- Evidence display is a bounded text projection of immutable fields only; no absolute locator,
  raw environment, credential, command path, HTML, or unbounded log reaches the browser.
- `workspace.reset` runs after evidence publication. It must return ready small/42 and confirm
  preserved `progress.json`/`evidence.json`. Repeating the browser reset returns the stored
  successful outcome and does not issue a second runner mutation.
- Completion occurs only after successful verify, verified evidence publication, successful
  truthful reset, and the learner's fixed decision. It uses expected progress revision and a
  stable server-owned idempotency key. Repeated completion returns the stored completion.
- A post-completion reset preserves evidence and immutable completion. Starting a new attempt
  requires an explicit new local attempt/session in future scope; Stage B does not silently erase
  completed truth.

The only narrow shared-core dependency is read-only import of
`scripts/learning_contracts/{canonical,schema,state,completion,evidence}.py` plus the released
progress/completion/evidence schemas. No shared-core write is required. The portal-owned fixed
Python adapter calls those functions; it does not clone them. If cook proves the imports cannot be
invoked from the pinned local runtime, that exact runtime/import failure is a blocker and does not
authorize a portal-local clone or shared-contract change.

## Gate B — Real Journey Authority

Gate B is open for `stage-b-promotion-trust` only when all rows pass:

| ID | Predicate | Fail action |
|---|---|---|
| GB-01 | Cook starts at exact clean `671201f78024786a9f2eba5e9e5fce7c78b4443d` | Stop |
| GB-02 | Changed paths equal the 18-path Phase 6 write set | Stop |
| GB-03 | Runner release identities/image/registry/evidence semantics match this register | Stop |
| GB-04 | Browser cannot select runner operation/host command/path/URL/SQL or obtain runner credentials | Stop |
| GB-05 | Session cookie/capability, CSRF, Host/Origin, method/path/body/content-type/output/time/concurrency limits pass | Stop |
| GB-06 | Real OrbStack operation and full fixed journey pass with zero container/process/port residue | Stop |
| GB-07 | Controlled failure is distinct from environment failure and requires the learner fix | Stop |
| GB-08 | Verify/evidence/reset/completion rules above pass, including replay/idempotency and persistence | Stop |
| GB-09 | Desktop+narrow, keyboard/focus/live region, axe Critical/Serious=0, and truthful no-JS fallback pass | Stop |
| GB-10 | Focused exact-head code review has Critical=0 and Important=0 | Stop |

Lane S requires no separate red-team/security/human ceremony. Functional request/auth/allowlist,
runner containment, evidence, reset, browser, and cleanup tests are release behavior and remain
mandatory.

## Rollback

Rollback is local and evidence-preserving:

1. authenticated `make learn-down` closes the portal/controller and child operation;
2. wait for bounded child cleanup; prove no owned port, runner container, or pending Issue #10
   runtime record remains;
3. keep runner audit/evidence and portal learning evidence/progress;
4. disable Stage B by reverting only the Phase 6 paths;
5. rebuild and verify the merged Stage A static/no-JS route remains truthful;
6. never delete runner state, shared evidence, unrelated artifacts, or OrbStack state.

## Current Verdict

`STAGE_B_READY`: dependencies are released, the adapter is compatible with the actual CLI and
evidence semantics, the journey is deterministic, and exact paths/commands are bounded. Cook
scope is only `stage-b-promotion-trust`; no implementation, merge, Issue completion, or cloud
authority follows.
