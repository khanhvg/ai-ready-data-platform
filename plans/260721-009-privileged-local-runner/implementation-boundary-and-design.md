# Issue #9 Implementation Boundary and Design

## Context and Non-Authority

- Immutable planning input: `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Fresh `origin/main` observed during planning: `3cd3d41f71582774e8d9656a51d1044035f4503c`.
- Fresh `origin/integration/issue-5-local-learning` equals the input SHA.
- Issue #6 is shipped at the input SHA. Issue #8 is OPEN with no released Stage A SHA.
- At validation input, Issue #9 is OPEN with `ready for plan validation`, `risk:high`, `tdd`,
  `security:S3`, and `backend`; `triaged` is no longer present.
- This document plans future work. It does not validate, audit, implement, authorize cook, create a
  PR, merge, or waive exact-head human approval.

## Owned and Denied Paths

### Planned tracked writes

| Action | Path | Purpose |
|---|---|---|
| Create | `apps/lab-runner/pyproject.toml` | Python 3.12 package metadata and console entrypoints |
| Create | `apps/lab-runner/requirements/runner-py312-macos-arm64.{in,lock,metadata.json}` | Wheel-only, hash-complete runtime/test toolchain |
| Create | `apps/lab-runner/config/runtime-policy-v1.toml` | Host tuple, transport, command quotas, environment, and containment policy |
| Create | `apps/lab-runner/config/released-contract-lock.json` | Exact Issue #6/#8 SHAs and hashes; references contracts, never copies them |
| Create | `apps/lab-runner/src/lab_runner/{__init__,__main__,contract,registry,transport,containment,launcher,workspace,fence,process,state,release,evidence,service}.py` | Framework-independent runner implementation |
| Create | `apps/lab-runner/tools/run-gate.py` | Non-interactive pinned bootstrap and `make` gate dispatcher |
| Create | `apps/lab-runner/tests/{characterization,unit,security,race,integration}/**` | RED-first and regression suites |
| Create | `apps/lab-runner/tests/fixtures/**` | Harmless malicious import/process/path/browser/fault helpers |
| Create | `apps/lab-runner/README.md` | Issue-local startup, disabled state, evidence, and rollback contract |
| Create | `mk/issue-5/i5-04.mk` | Only `runner-test`, `runner-security-test`, `runner-race-test` recipes |
| Modify | `orchestration/airflow/callables/pipeline.py` | Preserve default expert behavior; reject any explicit runner-reserved learner path before `_run`/import/write |

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
- The Airflow callable is the only scheduled existing-seam edit. Any additional Phase 1 RED
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

## Dependency Assimilation Without Contract Invention

Phase 2 may begin only after an owner-published Issue #8 Stage A handoff identifies an exact
merged/released 40-hex SHA. The implementer must then:

1. Fetch fresh remote refs and prove the release SHA is the reviewed merge/release and an ancestor
   of the implementation base.
2. Read the released paths, schema IDs/versions, operation matrix, typed-generation command,
   command-owner activation rule, migration/backward-reader contract, and recorded file hashes.
3. Verify the released contract can represent I5-04 command authority, typed arguments,
   idempotency/correlation, problem responses, state transitions, and an I5-04
   `fitness-result-v1` evidence owner. The input schema currently fixes owner `I5-01`, and the
   input command registry still marks the runner targets `future-owner`; both require a released,
   owner-approved activation path.
4. Record references and digests only in `released-contract-lock.json`. Generate runner-local
   bindings under `apps/lab-runner/**` only through the released generator/procedure.
5. STOP if a required command/field/operation is absent or incompatible. Return to Issue #8's
   shared-contract owner; do not add a duplicate schema, guessed version, fake SHA, compatibility
   alias, or local registry fork.

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
- Request framing is fail-closed: Phase 2 must derive and pin a finite maximum serialized body
  from the released Issue #8 request schemas and record the accepted media type/framing rules.
  Ambiguous or duplicate length, transfer-encoding/chunked bodies, invalid UTF-8/JSON, trailing
  bytes, and over-limit headers/body are rejected before typed operation allocation. If the
  released request matrix cannot yield an exact bound, Phase 4 is blocked rather than assigning a
  permissive local default.
- Only exact released runner-authority operations are routable. Health is read-only. Every
  mutation requires released typed body validation, bearer, CSRF, correlation, and idempotency.
  The browser has no direct privileged execution path.

## Typed Command Registry and Pinned Execution

The initial semantic allow-list remains exactly:

`workspace.prepare`, `retail.generate`, `retail.load`, `retail.dbt-build`, `retail.export`,
`promotion.configure`, `promotion.verify`, `workspace.reset`.

The wire shapes, versions, argument names, state transitions, and evidence fields come only from
the released Issue #8 contract. If the release differs, the dependency gate decides; this plan
does not guess a schema.

Version negotiation is an exact-set match against the Issue #8 released operation matrix. The
request must identify a released operation/command version exactly as that contract requires;
unknown, retired, malformed, duplicated, or cross-command versions fail before descriptor lookup,
and there is no implicit latest-version default, range match, downgrade, coercion, or compatibility
alias unless the released contract explicitly defines it. Startup advertises only the pinned
readable/current versions and their hashes from `released-contract-lock.json`; an unsupported
matrix keeps readiness false.

Each resolved descriptor contains an app-owned execution policy: exact command ID/contract
version, absolute interpreter/binary and entrypoint, Git blob/SHA-256, fixed argv template,
allowed typed values, fixed CWD role, exact environment keys, timeout/resource class, write-set,
network=`deny`, and expected artifacts. There is no raw executable, shell, free-form selector,
working-directory, path, URL, environment, plugin, package-install, Terraform, Docker, or cloud
override. `shell=False` and list argv are invariant.

Python entrypoints run through the pinned private runtime as `python -I <absolute-entrypoint>`.
Startup verifies the reviewed entrypoint blob/hash, Python `3.12.3`, complete wheel-only lock,
absence of unapproved `sitecustomize.py`/`usercustomize.py` and unexpected entry points, and the
exact Issue #6/#8 contract digests. dbt uses the read-only project with generated workspace-local
profiles, target, log, home, and package/cache paths; selectors are enums from the released
contract, never raw CLI text.

## Host Containment and Process Quotas

Initial supported host is intentionally narrow: Darwin arm64, macOS `26.5.1` build `25F80`,
physical memory exactly 16 GiB, Python `3.12.3`, and `/usr/bin/sandbox-exec` passing the functional
probe suite. An OS/Python/build change is unsupported until re-attested. No Linux/Windows claim.

The app-owned launcher is a separate child process. It receives only pre-opened workspace/fence
descriptors, applies rlimits, `fchdir`s to the owned generation, closes all other descriptors,
starts a new session/process group, and `execve`s `/usr/bin/sandbox-exec` with a generated profile.
The profile denies network, home/runtime-secret reads, and all writes outside the generation and
staging/evidence write-set; the Git base and entrypoints are read-only. A startup probe must prove
network denial, base-write denial, workspace write success, child cleanup, and required pipeline
imports. Probe failure sets readiness false with `RUNNER_CONTAINMENT_UNAVAILABLE`.

Before any runner RED or product cook, Phase 1 must admit one Darwin-native descendant-control
mechanism by proving, with deterministic barriers, that it observes, accounts for, terminates, and
reaps a rapid fork plus double-fork/`setsid` process without relying on a lucky 100 ms ancestry
sample. Process-group cleanup and polling may be defense in depth, but polling alone is not an
accepted capability. If the exact no-sudo/no-container host cannot provide this guarantee, STOP
and re-plan a narrower disabled runner; do not claim aggregate CPU/RSS/process quotas or complete
descendant cleanup.

One runner-wide mutation and one mutation per workspace are allowed concurrently. Exact hard
bounds for a child operation on the 16 GiB host:

| Resource | Bound | Enforcement |
|---|---:|---|
| Wall time | prepare/reset/configure 30 s; generate/load/export/verify 120 s; dbt 300 s | monotonic deadline, TERM 5 s, KILL/reap 5 s |
| Aggregate process-tree CPU | 600 CPU-seconds maximum; descriptor may lower | `RLIMIT_CPU` per child plus admitted descendant accounting at ≤100 ms |
| Aggregate process-tree RSS | 3 GiB | admitted descendant accounting at ≤100 ms; immediate process-tree kill |
| Workspace mutable allocation | 4 GiB logical **and** allocated bytes; 6 GiB free-space preflight | walk opened generation only; `RLIMIT_FSIZE` 1 GiB/file |
| Descendants | 16 live processes | admitted fork/reparent tracking + PID/start identity; kill/reap escaped sessions too |
| File descriptors | 256/process | `RLIMIT_NOFILE` |
| stdout/stderr | 2 MiB each; retained sanitized preview 128 KiB each | descriptor-backed files, overflow kills run; full hash/count retained |

`RLIMIT_AS` is defense in depth on Darwin; the aggregate tree monitor is authoritative. No
`RLIMIT_NPROC` because it could affect unrelated same-UID host processes. Quota breach is typed,
kills/reaps the complete tracked tree, retains bounded sanitized failure evidence, and never
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
- Startup reconciles recorded PID/start-time/process groups, marks interrupted operations with a
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

None for planning. The exact Issue #8 Stage A release identity and contents are a declared external
implementation gate, not a value this planner may resolve.
