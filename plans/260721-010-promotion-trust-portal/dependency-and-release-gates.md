# Dependency and Release Gates

## Current Exact-Release State

Rechecked on 2026-07-23 from clean v3 correction input
`2f278eb25aaff9e050314b01d1be155b76793f11` using fetched remote Git objects and live GitHub
issue, pull-request, review, and release-evidence records. Dependency worktrees and ignored
artifacts were not inputs.

| Dependency | Released/live fact | Stage consequence |
|---|---|---|
| Issue #6 | CLOSED/`shipped`; merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Seven protected data/contract identities remain read-only |
| Issue #7 | CLOSED/`shipped`; approved feature head `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9`; PR #22 merge `1806b6d515f2f7a2ace2be7077af84a745ff221f` | Exact Vite/React toolchain is usable by Stage A; spike product architecture is not |
| Issue #8 | CLOSED/`shipped`; final release merge `5644f01b4c0443a81f3af0bcce80f44c847cd986`; parents `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, `12e17427076fb31de85534bfbbbedca7e901e76c`; handoff `5047964988` | Exact validators, contracts, binding, adapters, and fixtures are read-only Stage A authorities; shared-contract lease released |
| Final integration | `5644f01b4c0443a81f3af0bcce80f44c847cd986`, tree `a38594d420fe7df2b30265a8a72bb5fad1698012` | Mandatory Stage A cook base |
| Issue #9 | OPEN/`ready to cook`; remote plan head `308c736f8811ac9aeaf41ad5b27dea07d2e60b2e`; first cook stopped unchanged at `9eb31075aeb0e7b974ad15645460ab4987570f20`; no feature branch is published and no reviewed/merged/pristine release exists | No Stage B runner authority; Stage B remains blocked |

The released integration has 921 tracked entries; the canonical `git ls-tree -r --full-tree`
listing has SHA-256 `a6681b3e7ee932fbd29728bc3f649017e57e6980871a3de9def9cb3ac318d9fe`.
The exact per-file blob, byte, and SHA-256 catalogue is in the
[Stage A release amendment](./stage-a-release-amendment.md#released-read-only-dependency-binding).

## Issue #7 Scope Reconciliation

Stage A promotes only the released Node/npm/package-lock/Vite/React/Playwright/axe foundation:
Node `22.22.3`, npm `10.9.8`, lockfile v3, Vite `8.1.5`, React/React DOM `19.2.7`, Playwright
`1.61.1`, axe Playwright `4.12.1`, and React plugin `6.0.1` with the released transitive lock and
integrity fields.

The Issue #7 spike page, lesson contract, copied fixture, timer/score harness, retained spike
evidence, and file layout are evidence of toolchain fitness only. They are not the portal
architecture. Firefox/WebKit, VoiceOver/System Settings/native browser automation, performance
sampling, timer scorecards, and Gate-D framework comparison are historical and not I5-05 gates.

## Exact Implementation Authority

| Stage | File authority | Command authority | Dependency authority | Cookable |
|---|---|---|---|---|
| A | Exactly 33 new tracked paths; no modifies/deletes | Exactly 18 release, install, test, build, audit, lifecycle, visual, and required-negative commands | Final integration plus 85 enumerated consumed paths | `false` pending fresh readiness audit |
| B | `[]` | `[]` | `[]` | `false` |

The exact lists in the amendment are normative. A path, command, dependency, version, route,
operation, or artifact not listed there is denied even if it sits beneath the issue-level
ownership ceiling.

## Ownership and Writer-Overlap Decision

- Stage A creates only the enumerated subset of `apps/learning-portal/**` and
  `mk/issue-5/i5-05.mk`; root Make already includes sorted `mk/issue-5/*.mk` fragments.
- Issue #7/#8 sources, shared contracts, root `release-manifest.json`, Issue #6 fixtures, root
  Make, runner source, `README.md`, `docs/**`, CI, cloud, AWS, Terraform, and other issue files are
  read-only or denied.
- The app consumes released #8 validators and maps a closed safe view model. It does not copy,
  reinterpret, fork, or become a second owner of shared contract truth. One validated released
  descriptor registry drives catalog/app/router/static/React output; the app consumes the shared
  Vite binding directly and creates no portal-local alias/mapping/schema/default-route authority.
- A conflicting active lease, changed path, release drift, or protected-hash drift is a hard
  STOP. No concurrency is assumed for shared surfaces.

## Gate A — Static Portal Authority

Gate A is not currently satisfied. Fresh independent validation has accepted this correction, but
the separate fresh readiness audit must still pass. A later v3 cook must begin from pristine
`5644f01b4c0443a81f3af0bcce80f44c847cd986` and re-prove every row before the first product write.

| ID | Required proof | Failure disposition |
|---|---|---|
| GA-01 | #7 approval/head/merge ancestry and tree equality; exact released toolchain and lock | Stop on any identity, lock, integrity, tool, or ancestry mismatch |
| GA-02 | #8 final release; exact shared binding/schema/adapter/invalid fixtures; contract set, registry, lesson/lab/manifest, validators, OpenAPI 16-operation matrix | Stop rather than create a local alias, mapping, schema, type, route, or operation truth |
| GA-03 | Cook HEAD, upstream, and fresh integration ref equal the pristine integration; clean tree; no overlap | Stop on wrong base, dirty input, or lease/path conflict |
| GA-04 | Seven Issue #6/protected identities match `requirements-and-risk-traceability.md` | Stop on byte, blob, or digest drift |
| GA-05 | Planned and final changed paths are exactly within the 33-path allowlist | Stop on additions, modifications, deletions, generated tracked output, or root changes |
| GA-06 | Commit chronology is exact 22-path scaffold → eight-path tests → contemporaneous RED → semantics | Stop on any early semantic, retrospective/missing real-path RED, test weakening, or v2 byte reuse |
| GA-07 | One released descriptor registry and one closed current evidence generation | Stop on duplicate/test authority, stale/failed hash, missing sources-excluded trace, or partial publication |

### Gate A Claim Boundary

Allowed:

- Vietnamese-first Vite/React catalog → module → lesson → narrative-step shell.
- One promotion-trust vertical slice derived from exact released #8 contracts.
- Read-only history navigation, deterministic static/no-JavaScript pages, and accessibility.
- Explicit `runner unavailable`, offline, and environmental-failure explanations.
- Issue #6 fixture facts labelled as retained baseline reference only.

Forbidden:

- Importing, starting, probing, or emulating Issue #9.
- A BFF/API, proxy, mutation route, generic command/path/URL/SQL surface, or host command exposure.
- Execution, reset, fresh evidence, progress, completion, or course-completion claims.
- Browser storage/cookie/session/service-worker truth, credentials, cloud action, or external
  content fetch.
- Copying Issue #7 spike product code or duplicating Issue #8 schema/registry/content truth.

## Gate B — Real Journey Authority

Stage B stays disabled. Its file, command, and dependency lists remain empty until a separate
exact-SHA amendment proves an accepted Stage A head and a released Issue #9 runner with its API,
registry, transport/client, containment, idempotency, problem, reset, verifier, immutable-evidence,
readiness, conformance, security, race, crash, cleanup, and rollback contracts. The #9 release
must explicitly bind a compatible #8 release. Missing capability is a STOP, never an adapter
guess or portal-owned implementation.

The commands `make lesson-e2e LESSON=promotion-trust` and `make local-journey-e2e` are registered
Stage B acceptance surfaces but must return non-zero `STAGE_B_DEPENDENCY_UNAVAILABLE` in Stage A
without importing or acting on a runner.

## Runtime Admission and Gate Recording

From a fresh checkout at the released integration, Stage A must:

1. recompute release ancestry, 921-entry tree, all 85 per-path blob/bytes/SHA-256 identities,
   protected identities, command ownership, and the exact lock graph;
2. run the released #8 `learning-contracts-check` including focused binding `11/11` and invalid
   family `8/8`, promotion lesson check, and 16-operation API check through the admitted runtime;
3. use frozen `npm ci --ignore-scripts --no-audit --no-fund`; after acquisition, run build and
   focused checks without undeclared network access or package/runtime fallback;
4. record the implementation input, dependency identities, paths, versions, tools, checks,
   protected hashes, changed-path closure, and stable pass/failure code;
5. keep dependency evidence distinct from learner-run evidence and human approval.

Missing cache/tool, network fallback, lifecycle-script execution, absent measurement, ignored
failure, or alternate package manager is `fail`.

## Stage and Branch Strategy

Preserve failed PR #29, `feature/issue-10-portal-stage-a-v2`, its commits, and its evidence as
immutable negative history. After fresh validation and readiness only, create
`feature/issue-10-portal-stage-a-v3` in a new worktree directly from final integration. Before the
scaffold, allow only this v3 correction output plus its ensuing fresh independent validation and
readiness plan commits; prove every diff is plan-directory-only. Never cherry-pick/copy v2
product, tests, fixtures, logs, traces, manifests, evidence, or generated bytes.

Then execute exact 22-path semantics-free scaffold, exact eight-path tests, contemporaneous real-
path RED, first semantic, later semantic, and final commit/tree binding. The final head requires
all gates, two fresh independent implementation reviews, bounded human UAT, and human exact-head
approval. If Stage A later merges while Stage B is blocked, Issue #10 remains open.

## Current Disposition

`STAGE_A_VALIDATED_PENDING_FRESH_READINESS`: scope and released inputs remain exact, but the prior
readiness was invalidated by failed PR #29 review. Cook scope is none until fresh readiness passes
at its exact output. `STAGE_B_BLOCKED_ON_ISSUE9`: Stage B authority is empty. No
implementation, execution, review approval, merge, or release claim follows from this correction.
