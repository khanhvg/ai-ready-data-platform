# Issue #9 Implementation Boundary and Design

> **Current capability authority:** [capability-amendment.md](./capability-amendment.md) supersedes
> the earlier process-tree cook route. Fork prevention and exact single-worker reap pass, but no
> implementation strategy is admitted because `retail.dbt-build` requires a resource-tracker
> child. `COOK_SCOPE=none`; the conditional single-worker/zero-descendant design becomes active
> only after a separately approved backend preserves all eight released commands.

## Context and Non-Authority

- Original planning base / Issue #6 release: `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Immutable dependency-release amendment input:
  `5cea5ce248b49ff8741af1b1e65f8ac2eb64698f`.
- Fresh `origin/main` observed during planning: `3cd3d41f71582774e8d9656a51d1044035f4503c`.
- Fresh `origin/integration/issue-5-local-learning` and fresh live ref equal released Stage A SHA
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`.
- Issue #6 is shipped. Issue #8 Stage A is released by owner comment `5043195549`; PR #23 merge is
  `5c2244c2c860234d0df49cf0a42ad950c6495717`, PR #25 merge/current integration head is the Stage A
  SHA, and the exact release tree is `27fc3667ef37892dad5c3fbfd76769f65a0760be`.
- At amendment input, Issue #9 is OPEN with `ready for plan audit`, `risk:high`, `tdd`,
  `security:S3`, and `backend`.
- This document plans future work. It does not validate, audit, implement, authorize cook, create a
  PR, merge, or waive exact-head human approval.

## Owned and Denied Paths

### Planned tracked writes

| Action | Path | Purpose |
|---|---|---|
| Create | `apps/lab-runner/pyproject.toml` | Python 3.12 package metadata and console entrypoints |
| Create | `apps/lab-runner/requirements/runner-py312-macos-arm64.{in,lock,metadata.json}` | Wheel-only, hash-complete runtime/test toolchain |
| Create | `apps/lab-runner/config/runtime-policy-v1.toml` | Host tuple, transport, command quotas, environment, and containment policy |
| Create | `apps/lab-runner/config/released-contract-lock.json` | Exact Issue #6 and released Stage A SHA/tree/path/version/hash references; never copies contracts |
| Create | `apps/lab-runner/config/command-owner-activation-i5-04-v1.json` | Issue #9-owned activation instance binding the actual I5-04 fragment hash to the three reserved commands and `fitness-result-v2` |
| Create | `apps/lab-runner/src/lab_runner/{__init__,__main__,contract,registry,transport,containment,launcher,adapters,workspace,fence,process,state,release,evidence,service}.py` | Framework-independent runner implementation; `adapters.py` remains blocked until all eight fixed in-process adapters pass |
| Create | `apps/lab-runner/tools/run-gate.py` | Non-interactive pinned bootstrap and `make` gate dispatcher |
| Create | `apps/lab-runner/tests/{characterization,unit,security,race,integration}/**` | RED-first and regression suites |
| Create | `apps/lab-runner/tests/fixtures/**` | Harmless malicious import/process/path/browser/fault helpers |
| Create | `apps/lab-runner/README.md` | Issue-local startup, disabled state, evidence, and rollback contract |
| Create | `mk/issue-5/i5-04.mk` | Only `runner-test`, `runner-security-test`, `runner-race-test` recipes |
| Conditional modify | `orchestration/airflow/callables/pipeline.py` | Only if Phase 1 still proves the seam necessary: preserve default expert behavior and reject explicit runner-reserved learner paths before `_run`/import/write |

### Runtime-only generated state

```text
.artifacts/workspaces/runner/
  service/<launch-id>/{runner.sock,launch.json,containment-probe.json}
  service/<launch-id>/secrets/{bearer-token,csrf-token}
  namespaces/<workspace-id>/
    .runner-owner.json
    state.sqlite3
    audit/
    generations/<generation-id>/{home,tmp,raw,warehouse,dbt,export,config}/
    releases/<release-id>/{manifest.json,assets/*.parquet}
    current-release.json
.artifacts/evidence/runner/<run-id>/{manifest.json,gates/**,artifacts/**}
```

All directories are `0700`; mutable/secret files are `0600`; the socket is owner-only. Public
commands generate IDs. No production interface accepts an arbitrary filesystem root or run ID.
Runtime state and evidence remain untracked; tests use private temporary roots or remove only
marker-verified issue-owned state.

### Explicitly denied writes

- `learning/contracts/**`, `contracts/**`, `scripts/golden/**`, root `Makefile`, root
  `release-manifest.json`, `.gitignore`, `docs/code-standards.md`, portal/framework paths,
  Docker/Compose, Airflow DAGs, every other Airflow file, Terraform/AWS/cloud paths, migrations,
  and other plans/issues.
- The Airflow callable is the only conditionally admitted existing-seam edit. If Phase 1 proves
  no edit is necessary, it stays byte-identical. Any additional Phase 1 RED
  characterization failure must name one smallest seam and return to plan validation/readiness
  for scope confirmation; it may not trigger an opportunistic edit.

## Existing Seam Characterization

| Existing read-only seam at input | Proven capability to preserve | Runner use |
|---|---|---|
| `data-generator/generate.py` | `--profile`, `--seed`, `--out`, bounded order/event caps | Pinned Python `-I` invocation; output below generation root |
| `ingestion/load_raw.py` | Explicit `--raw-dir` and `--duckdb-path`; closes writer | Pinned paths below one generation |
| `orchestration/airflow/callables/pipeline.py` | Explicit raw/DB/dbt target/log/export arguments currently accept caller paths | Add one pre-spawn guard: defaults stay expert; lexical or resolved runner-reserved paths fail `RUNNER_LEARNER_NAMESPACE_RESERVED`; runner does not import Airflow |
| `transform/dbt/dbt_project.yml` and `profiles.yml` | Stable 51-model project; default profile is expert namespace | Read-only project plus generated workspace-local profiles directory |
| `serving/export_marts_snapshot.py` | Explicit DuckDB/export paths; exact curated list | Stage into a unique release, never repository `serving/export/` |
| `contracts/data/curated-release-manifest.schema.json` | Exact ordered 11-asset manifest/current-pointer schema | Consume read-only at Issue #6 SHA |
| `scripts/golden/workspace.py`, `process.py`, `release_contract.py` | Descriptor/identity, process-group, and manifest reference behavior | Characterization reference only; no shared rewrite or generalized-runner claim |

Direct `make seed/load/dbt/bi` and default Airflow callables remain the **expert namespace** at
repository paths. Runner commands can mutate only a learner namespace below the private runtime
root. The narrow Airflow guard checks every explicit raw/DB/dbt-profile/target/log/export path
before `_run`, rejects lexical and resolved paths under the runner-reserved root, and leaves
default call signatures, argv, environment behavior and DAG import/order unchanged. Tests prove
namespace non-overlap and denial before child/import/write. The runner never invokes root Make
recipes.

## Released Dependency Assimilation Without Contract Invention

Phase 2 consumes only exact Git-tree bytes at Stage A release
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. The full pins are in Phase 2; the critical boundary is:

1. `learning-contract-set-v1.json` content SHA-256 is
   `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`; version-registry SHA-256
   is `a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb`.
2. The immutable base command registry SHA-256 is
   `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80`. It reserves the three
   I5-04 Make commands and `mk/issue-5/i5-04.mk` while retaining `future-owner` base rows.
3. `command-owner-activation-v1` is a generic hash-bound activation schema; `fitness-result-v2`
   accepts I5-04 and `verify_fitness(..., activation=...)` enforces exact owner/command/
   `implemented`/v2 selection. The version overlay keeps fitness v1 readable/current in the base,
   adds readable v2, and defines no emission fallback.
4. The released lab declares exactly eight zero-argument semantic commands, `small-42`, 120-second
   and 512 MiB command bounds, 256 MiB workspace quota, denied network, and unprivileged local
   execution. The operation/OpenAPI contracts define 16 synchronous endpoints and five mutations,
   exact auth/CSRF/idempotency/CAS/problem/evidence metadata, and API `learning-platform-v1`.
5. Stage A exposes no generated-binding command, path list, or output hash. Direct released
   schema/reader use is authoritative; any `generated/**` path is denied.

Compatibility is PASS without a shared-contract write. Issue #9 owns the exact activation-instance
path `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`; its content and fragment
hashes are computed from the actual future files and then locked, never predicted in this plan.
The future implementation head must be recorded only after it exists and must descend from the
release. No duplicate schema, guessed version, fake SHA, local registry fork, or synthetic
command-version field is allowed.

## Shared-Contract Lease Reconciliation

At `2026-07-22T08:05:02Z`, Issue #8 Stage B's latest handoff
<https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043335319> records a
blocked plan-only attempt with `OUTPUT_SHA=none` and no amended path. Issue #9 reads immutable
Stage A bytes at `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` and writes only the paths admitted in
this plan. Read-only consumption is not a lease conflict. Any later real write to an Issue #9-owned
path, or any requested Issue #9 write to `learning/contracts/**`, `contracts/**`, root Make,
golden core, portal, cloud, or container paths, blocks cook pending a new ownership decision.

## Private Transport

- Default: HTTP/1.1 over a Unix-domain socket in the `0700` service directory. Socket mode
  `0600`; macOS `LOCAL_PEERCRED` must report the runner's effective UID; fixed exact
  `Host: runner.internal`; listener never binds a public interface.
- Optional fallback: explicit opt-in `127.0.0.1:0` only. The kernel-selected port becomes the one
  exact allowed Host value. `localhost`, alternate IP spellings, IPv6, forwarded hosts, and DNS
  names are rejected. No stable port.
- Authentication: two independent launch-scoped 256-bit values. One bearer credential and one
  mutation CSRF value are written to separate `0600` files outside child-readable roots. They are
  delivered only to the future server-side BFF; never returned in a response, URL, cookie,
  browser bundle, log, evidence, child environment, or workspace.
- Session boundary: both credentials are bound to the exact launch ID and exact UDS inode or
  kernel-selected loopback port, become invalid when that listener exits, and are replaced on
  every restart. A credential or request from a prior launch is rejected before body parsing or
  operation/audit allocation.
- Origin policy: BFF calls are server-to-server and must omit `Origin`. Any `Origin` header,
  `Cookie`, browser `Sec-Fetch-Site` value other than `none`/absent, CORS preflight, form/simple
  content type, missing/duplicate auth header, or missing/duplicate CSRF header on a mutation is
  rejected before body parsing and before operation allocation. Responses emit no permissive
  CORS headers.
- Request framing is fail-closed. The released request objects are closed, but minimum-only integer
  fields mean Stage A does not define a finite maximum serialized HTTP-body size. Issue #9 therefore
  sets the stricter private-transport policy `RUNNER_REQUEST_BODY_LIMIT_BYTES=16384`. The limit is
  checked while reading and before JSON parsing, audit allocation, operation allocation, or
  workspace allocation. Ambiguous/duplicate length, transfer-encoding/chunked bodies, invalid
  UTF-8/JSON, trailing bytes, and over-limit headers/body are rejected.
- Only exact released runner-authority operations are routable. Health is read-only. Every
  mutation requires released typed body validation, bearer, CSRF, correlation, and idempotency.
  The browser has no direct privileged execution path.

The private listener is not the public OpenAPI server. Its exact `Host: runner.internal` (or the
launch-recorded ephemeral loopback host) and rejected `Origin` policy are intentionally stricter
than the released public profile's `Host: localhost` / `Origin: http://localhost` boundary. Issue
#10's future BFF owns that public mapping; Issue #9 consumes the released semantic bodies,
operations, state, problems, and evidence without exposing the runner directly to a browser.

## Typed Command Registry and Pinned Execution

The initial semantic allow-list remains exactly:

`workspace.prepare`, `retail.generate`, `retail.load`, `retail.dbt-build`, `retail.export`,
`promotion.configure`, `promotion.verify`, `workspace.reset`.

The wire shapes, versions, argument names, state transitions, and evidence fields come only from
the released Issue #8 contract. If the release differs, the dependency gate decides; this plan
does not guess a schema.

Version handling follows the release exactly: API responses advertise
`learning-platform-v1`; operation rows use `apiVersion: v1`; mutation bodies use their exact
`*-request-v1` schemaVersion; the lab document is `lab-v1`/`1.0.0`; and public gate fitness uses
`fitness-result-v2` through the eventual I5-04 activation. Stage A defines no command-version
field, so Issue #9 must not add one. Unknown schema/API versions and command IDs fail before
descriptor lookup; there is no implicit latest, range, downgrade, coercion, or alias.

Each resolved descriptor contains an app-owned execution policy: exact command ID/contract
version, absolute interpreter and fixed in-process adapter, Git blob/SHA-256, fixed argument template,
allowed typed values, fixed CWD role, exact environment keys, timeout/resource class, write-set,
network=`deny`, and expected artifacts. There is no raw executable, shell, free-form selector,
working-directory, path, URL, environment, plugin, package-install, Terraform, Docker, or cloud
override. Fork, spawn, subprocess, multiprocessing process primitives and exec are unavailable in
the conditional worker design. The current dbt adapter does not satisfy this rule, so no
descriptor set is admitted.

The one operation worker runs through the pinned private runtime as
`python -I <absolute-worker-entrypoint>` and imports only fixed reviewed adapter modules from
verified read-only roots. Startup verifies the reviewed worker/adapter blobs and hashes, Python
`3.12.3`, complete wheel-only lock,
absence of unapproved `sitecustomize.py`/`usercustomize.py` and unexpected entry points, and the
exact Issue #6/#8 contract digests. dbt uses the read-only project with generated workspace-local
profiles, target, log, home, and package/cache paths; selectors are enums from the released
contract, never raw CLI text.

## Host Containment and Process Quotas

Initial supported host is intentionally narrow: Darwin arm64, macOS `26.5.1` build `25F80`,
physical memory exactly 16 GiB, Python `3.12.3`, and `/usr/bin/sandbox-exec` passing the functional
probe suite. An OS/Python/build change is unsupported until re-attested. No Linux/Windows claim.

The app-owned operation worker is the parent's one allowed child. Before capability handoff it
receives only pre-opened workspace/fence descriptors, applies rlimits, `fchdir`s to the owned
generation, closes all other descriptors, starts a new session, and replaces its own image with
`/usr/bin/sandbox-exec` plus the fixed reviewed worker/profile. No adapter may create another
process after the fork-denied profile is active.
The profile denies network, home/runtime-secret reads, and all writes outside the generation and
staging/evidence write-set; the Git base and entrypoints are read-only. A startup probe must prove
network denial, base-write denial, workspace write success, child cleanup, and required pipeline
imports. Probe failure sets readiness false with `RUNNER_CONTAINMENT_UNAVAILABLE`.

The exact host proves a stronger candidate than discovery: `deny process-fork` prevents all tested
descendant-creation paths before the first child. The parent can own and reap one worker by exact
PID/start identity after normal execution, `setsid`, image replacement, crash or timeout. Generic
`deny process-exec` blocks Python bootstrap, so fixed adapters and static policy must reject any
operation requiring exec. This candidate is not admitted because exact dbt creates a Python
resource tracker; process-group cleanup, launchd and polling do not repair that incompatibility.

One runner-wide mutation and one mutation per workspace are allowed concurrently. Exact hard
bounds for a child operation on the 16 GiB host:

| Resource | Bound | Enforcement |
|---|---:|---|
| Wall time | 120 s per each of the eight released lab commands | monotonic deadline, TERM 5 s, KILL/reap 5 s; no command exceeds the released ceiling |
| Worker CPU | 600 CPU-seconds maximum; descriptor may lower | conditional exact single-worker `RLIMIT_CPU`; blocked until eight adapters pass |
| Worker RSS | 536,870,912 bytes per command | conditional exact single-worker measurement; blocked until eight adapters pass |
| Workspace mutable allocation | 268,435,456 bytes logical **and** allocated; 6 GiB host free-space preflight | released lab quota; walk opened generation only; no file may exceed the workspace quota |
| Descendants | 0 | conditional Seatbelt `deny process-fork`; any fork/spawn need fails readiness before allocation |
| File descriptors | 256/worker | `RLIMIT_NOFILE` |
| stdout/stderr | 2 MiB each; retained sanitized preview 128 KiB each | descriptor-backed files, overflow kills run; full hash/count retained |

`RLIMIT_AS` is defense in depth on Darwin; exact single-worker measurement is the conditional
authority. No
`RLIMIT_NPROC` because it could affect unrelated same-UID host processes. Quota breach is typed,
kills/reaps the exact PID/start-identity worker, retains bounded sanitized failure evidence, and never
advances state or release pointer.

The environment is built from an empty mapping. Allowed keys are policy-generated `PATH`,
`HOME`, `TMPDIR`, `TZ=UTC`, verified locale, `PYTHONHASHSEED=0`, `PYTHONDONTWRITEBYTECODE=1`,
`PYTHONNOUSERSITE=1`, `PIP_CONFIG_FILE=/dev/null`, and command-specific workspace dbt paths.
`PYTHONPATH`, startup hooks, proxies, SSH agent, Docker, tracing exporters, cloud/AWS/GCP/Azure,
GitHub, MinIO/OpenMetadata, and matching token/password/secret/key/credential variables are absent.

## Workspace, Fencing, State, and Audit

- Allocate workspace/generation/release/evidence directories through retained directory FDs with
  no-follow, owner nonce, device/inode/mode/link-count/type checks. Reject absolute, parent, NUL,
  alternate separator, symlink, hardlink, device/FIFO/socket, foreign destination, mount change,
  and pre-existing unowned state.
- Hold an OS advisory lock FD for the full mutating operation. A SQLite transaction increments a
  monotonic namespace fence epoch. Every state/release/evidence commit compares workspace ID,
  owner nonce, operation request digest, lock identity, and current epoch; stale owners cannot
  commit after crash/restart.
- Expert Make/Airflow paths are a distinct namespace. A callable targeting a learner path without
  the inherited pre-opened fence capability fails before mutation. No path-only token suffices.
- SQLite stores mutable operation/idempotency projections separately from an insert-only
  hash-chained `audit_event` table. Database triggers reject event UPDATE/DELETE; `FULL` sync and
  transactional inserts make transitions crash-safe. Exported audit evidence is canonical,
  append-only by sequence/hash, and claims corruption detection only.
- Idempotency key uniqueness is scoped to workspace + released operation. Same key/same canonical
  request returns the original operation/result, including after restart. Same key/different
  request is a typed conflict. In-flight reset/export/verify conflicts serialize or fail without
  duplicate work.
- Startup reconciles only the recorded worker PID/start identity, marks interrupted operations with a
  typed recoverable state, quarantines only marker-owned incomplete generations/releases, verifies
  committed evidence, and never fabricates completion. Repeated reconciliation/reset is safe.

## Atomic Eleven-Asset Release

`retail.export` reads one committed DuckDB generation and stages each of the exact ordered eleven
assets into a unique release directory. It fsyncs and verifies every regular single-link Parquet
file, schema hash, content hash, and row count; validates one released
`CuratedReleaseManifest`; writes/fsyncs the manifest; then atomically replaces
`current-release.json` in the same filesystem and fsyncs the directory.

The pointer records current manifest digest and prior complete release ID. Readers open and verify
the pointer and manifest through retained descriptors before use. A partial/mixed release, crash,
quota failure, stale fence, wrong generation, duplicate asset, or missing asset leaves the prior
pointer unchanged. Same operation replay returns the committed release. Unpointed marker-owned
staging is quarantined/reconciled; evidence is retained.

## Exclusions

- No portal, selected web framework, browser session implementation, completion transaction, or
  user-facing UI. Issue #10 owns that future integration.
- No AWS/cloud/network dependency, Terraform command, Docker/Compose, container privilege, sudo,
  package installation at runtime, arbitrary shell, Iceberg/OpenMetadata mutation, hosted identity,
  signing/non-repudiation, or multi-user claim.
- No modification of the eleven-mart/data semantics or Issue #8 shared contracts.

## Unresolved Questions

One owner/platform decision blocks readiness: an approved backend must preserve
`retail.dbt-build` without child/exec/private-startup manipulation, another documented no-sudo
lifetime primitive must be proven, or the upstream contract must be deliberately rereleased.
The activation path and request ceiling are otherwise exact. Hashes of Issue #9-owned future files
and the implementation head are evidence captured after those bytes exist; they are deliberately
not future placeholders and may never be synthesized. Host containment,
descendant control, RED/GREEN behavior, and exact-head review remain execution gates inside the
ordered cook, not unresolved planning dependencies.
