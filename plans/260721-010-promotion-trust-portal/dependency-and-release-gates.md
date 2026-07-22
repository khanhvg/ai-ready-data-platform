# Dependency and Release Gates

## Current Exact-Release State

Rechecked on 2026-07-22 from clean plan head
`4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7` using fetched remote Git objects and live GitHub
issue, pull-request, review, and release-evidence records. Dependency worktrees and ignored
artifacts were not inputs.

| Dependency | Released/live fact | Stage consequence |
|---|---|---|
| Issue #6 | CLOSED/`shipped`; merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Seven protected data/contract identities remain read-only |
| Issue #7 | CLOSED/`shipped`; approved feature head `b219ba2d3843934c3bce2fbbec2a844b48b2dfa9`; PR #22 merge `1806b6d515f2f7a2ace2be7077af84a745ff221f` | Exact Vite/React toolchain is usable by Stage A; spike product architecture is not |
| Issue #8 | Stage A PR #23 merge `5c2244c2c860234d0df49cf0a42ad950c6495717`; release evidence comment `5043195549` | Exact validators, registries, lesson/lab/manifest, OpenAPI, progress/completion/evidence contracts are read-only Stage A authorities |
| Composition | PR #25 merge and pristine released integration `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, tree `27fc3667ef37892dad5c3fbfd76769f65a0760be` | Mandatory Stage A cook base |
| Issue #9 | OPEN and unreleased | No Stage B runner authority; Stage B remains blocked |

The released integration has 903 tracked entries; the canonical `git ls-tree -r --full-tree`
listing has SHA-256 `4b95afd87ee7702f74df4a4b09198e13b8fa7ba45434c8a6a511a3ff1c580018`.
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
| A | Exactly 34 new tracked paths; no modifies/deletes | Exactly the release, install, test, build, audit, lifecycle, visual, and required-negative commands in the amendment | #7/#8/#25 identities above and their enumerated bytes | `true` |
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
  reinterpret, fork, or become a second owner of shared contract truth.
- A conflicting active lease, changed path, release drift, or protected-hash drift is a hard
  STOP. No concurrency is assumed for shared surfaces.

## Gate A — Static Portal Authority

Gate A is satisfied for planning/cook readiness only when the cook begins from pristine
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` and re-proves every row before the first product
write.

| ID | Required proof | Failure disposition |
|---|---|---|
| GA-01 | #7 approval/head/merge ancestry and tree equality; exact released toolchain and lock | Stop on any identity, lock, integrity, tool, or ancestry mismatch |
| GA-02 | #8 PR #23 plus PR #25 composition; exact release comment, schemas, registry, lesson/lab/manifest, validators, OpenAPI 16-operation matrix | Stop rather than create a local schema, type, route, or operation truth |
| GA-03 | Cook HEAD, upstream, and fresh integration ref equal the pristine integration; clean tree; no overlap | Stop on wrong base, dirty input, or lease/path conflict |
| GA-04 | Seven Issue #6/protected identities match `requirements-and-risk-traceability.md` | Stop on byte, blob, or digest drift |
| GA-05 | Planned and final changed paths are exactly within the 34-path allowlist | Stop on additions, modifications, deletions, generated tracked output, or root changes |

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

1. recompute release ancestry, tree, per-path blob/bytes/SHA-256, protected identities, command
   ownership, and the exact lock graph;
2. run the released #8 `learning-contracts-check`, promotion lesson check, and 16-operation API
   check through their admitted runtime;
3. use frozen `npm ci --ignore-scripts --no-audit --no-fund`; after acquisition, run build and
   focused checks without undeclared network access or package/runtime fallback;
4. record the implementation input, dependency identities, paths, versions, tools, checks,
   protected hashes, changed-path closure, and stable pass/failure code;
5. keep dependency evidence distinct from learner-run evidence and human approval.

Missing cache/tool, network fallback, lifecycle-script execution, absent measurement, ignored
failure, or alternate package manager is `fail`.

## Stage and Branch Strategy

Stage A cooks on a new branch from the pristine released integration, never from this planning
branch or a feature worktree. Its exact implementation head requires focused tests, S3, two fresh
independent reviews, bounded human visual/keyboard UAT, and human exact-head approval before a
human merge. If Stage A merges while Stage B remains blocked, Issue #10 stays open and the portal
retains its non-executing/non-completing claim.

## Current Disposition

`STAGE_A_READY`: the released authorities and exact bounded cook scope are closed by the amendment
and current readiness audit. `STAGE_B_BLOCKED`: Issue #9 remains unreleased and Stage B authority
is empty. Planning readiness does not claim that the portal was built, tested, executed, reviewed,
approved, or merged.
