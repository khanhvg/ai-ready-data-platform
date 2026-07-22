---
type: host-capability-and-operation-readiness-amendment
issue: 9
date: "2026-07-22"
inputSha: "dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090"
blockedCookInputSha: "9eb31075aeb0e7b974ad15645460ab4987570f20"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
capabilityVerdict: BLOCKED
forkExecNegatives: "7/7"
setsidPidReap: PASS
operationFeasibility: "7/8"
cookScope: none
cloudAction: none
---

# Issue #9 Host Capability and Operation Readiness Amendment

## Decision

`BLOCKED`; `COOK_SCOPE=none`.

The exact host can fail-closed prevent descendant creation for a fixed already-launched Python
worker: a Seatbelt profile containing `deny process-fork` rejected all seven tested fork/spawn
families with `EPERM` before the first child marker existed. The parent can also own one worker by
exact PID plus kernel start identity and reap that worker after normal execution, same-process
`setsid`, TERM-ignore, image replacement, crash, or timeout.

That primitive cannot yet carry the complete released eight-command contract. The exact pinned
`dbt-core==1.11.12` / `dbt-duckdb==1.10.1` programmatic build constructs a multiprocessing spawn
context lock and starts Python's resource tracker. The fork-denied sandbox refuses that creation
before a descendant exists, so `retail.dbt-build` fails. The released contract requires that
command; removing it or claiming a seven-command runner would weaken released behavior.

No source/RED cook may resume. The former process-tree tracking design is not an alternate route:
the prior cook already proved that no admitted no-sudo Darwin discovery/reaping authority catches
rapid double-fork/reparent/`setsid`, and this investigation found no replacement. The blocker is
recorded at [Issue #9 comment 5043725531](https://github.com/khanhvg/ai-ready-data-platform/issues/9#issuecomment-5043725531).

## Scope and Immutable Facts

- Investigation input, local HEAD, upstream, and fresh live branch ref were exactly
  `dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090` with a clean worktree.
- The first cook input was `9eb31075aeb0e7b974ad15645460ab4987570f20` and stopped in Phase 1
  before any RED or source change.
- Released Stage A remains `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; all 38 Phase 2
  interface pins still recompute from that Git object.
- The current plan-only branch at `dc8b6d2cb46c8101bd8f1309acc7f12e5da7e090` does not descend
  from Stage A. That is expected for this no-cook amendment: exact contract reads use the immutable
  Git object. If the backend dependency is later resolved, the implementation base must first be
  a clean remote-equal descendant of Stage A and retain the amended plan; no merge/rebase is
  authorized in this context.
- The host probe used only bounded throwaway state, public fake canaries, repository-controlled
  code, and the exact pinned Stage A Python lock. It used no sudo/admin/TCC prompt, settings
  change, container, Docker, cloud, AWS, Terraform, privileged install, or private value.
- Only this plan directory may change. Product source, runner source/tests, portal, contracts,
  golden core, Airflow, data callables, other worktrees, PR state, and release history remain
  unchanged.

## Host Capability Evidence

Exact tested tuple: macOS `26.5.1` build `25F80`, Darwin arm64, 16 GiB physical memory, Python
`3.12.3`, and `/usr/bin/sandbox-exec`.

The functional worker profile used the following security properties: default access required by
the already-launched pinned interpreter, `deny process-fork`, `deny network*`, a literal base-file
write denial, and a literal fake-secret read denial. This is an exact-host capability result, not
a general macOS API promise. `sandbox-exec` is deprecated; every supported OS/build/runtime change
must therefore fail readiness until the entire functional suite is re-attested.

| Probe | Unsandboxed negative control | Fork-denied worker | Result |
|---|---|---|---|
| `os.fork` | child marker created | `EPERM`; no marker | PASS |
| `os.posix_spawn` | child marker created | `EPERM`; no marker | PASS |
| `subprocess.run` | child marker created | `EPERM`; no marker | PASS |
| multiprocessing `fork` | child marker created | `EPERM`; no marker | PASS |
| multiprocessing `spawn` | child marker created | `EPERM`; no marker | PASS |
| multiprocessing `forkserver` | child marker created | `EPERM`; no marker | PASS |
| rapid double-fork + reparent + `setsid` | detached child marker created; exact identity cleanup succeeded | first fork returned `EPERM`; no child marker | PASS |

Before and after inventories for probe ID `issue9cap-20260722-final` were both empty. The detached
negative-control process was killed only after its PID and start identity matched. The sandboxed
run ended with zero matching survivors.

Additional functional results:

- a loopback connection succeeded outside the sandbox and failed with `EPERM` inside it;
- workspace write succeeded, while base-sentinel write and fake-secret read failed with `EPERM`;
- the base sentinel remained byte-exact and the fake ambient credential was absent;
- a TERM-ignoring worker called `setsid` in the same process; PID and start identity remained
  exact, TERM was observed ignored, KILL succeeded, `wait` reaped it, and inventory was empty;
- generic `deny process-exec` prevented the initial Python interpreter from launching (exit 71),
  so it cannot be applied to the same bootstrap profile;
- a direct `execve` under `deny process-fork` replaced the image without creating a descendant.
  PID/start identity remained exact, there were no children, and exact KILL plus `wait` reaped it.
  Fixed descriptors and static policy must therefore reject any operation whose reviewed adapter
  can call exec; the OS-level authority for unexpected same-PID replacement is protocol failure
  plus exact identity cleanup, not a claim that Seatbelt denied the exec syscall.

## User Service and Other Darwin Primitives

A bounded per-user launchd service negative control started a rapid double-fork/`setsid` child.
`launchctl bootout` removed the service but did not kill that escaped child. The child was then
removed by exact PID/start-identity cleanup, and the service domain and final process inventory
were empty. This matches the documented launchd process-group boundary: the default cleanup
applies to the service's process group, which `setsid` escapes. User launchd is rejected as the
cleanup authority.

`ktrace`, DTrace, EndpointSecurity, and `NOTE_TRACK` remain unavailable without prohibited
authority or do not provide the required semantics. Coalitions and undocumented service behavior
were not claimed. Process groups and ancestry polling remain defense in depth only; polling is
never sole authority.

## Exact Operation-to-Adapter Feasibility

All probes used the Stage A source Git object, Python `3.12.3`, and the exact hash-complete
`golden-py312-macos-arm64.lock`. Existing Airflow wrappers remain expert-only and byte-identical:
`seed`, `load_raw`, `dbt_build`, and `export_marts_snapshot` intentionally call subprocesses, so
they cannot be learner-worker adapters under `deny process-fork`. The runner would need fixed
direct callables instead.

| Released command | Fixed in-process candidate | Child/exec need | Result |
|---|---|---|---|
| `workspace.prepare` | app-owned descriptor-relative directory/state initialization | none | PASS |
| `retail.generate` | fixed Stage A `generate.main` with fixed `small`/`42` and app-owned output role | none; 18 CSV tables / 6,812 rows observed | PASS |
| `retail.load` | `ingestion.load_raw.load_raw` | none; 18 DuckDB raw tables observed | PASS |
| `retail.dbt-build` | public `dbt.cli.main.dbtRunner.invoke` plus fixed DuckDB profile | **requires resource-tracker child** while constructing spawn-context synchronization; denied `EPERM` | **FAIL** |
| `retail.export` | `serving.export_marts_snapshot.export_marts` in a fresh operation worker | none; exact 11 Parquet marts observed | PASS |
| `promotion.configure` | app-owned fixed state/config write plus atomic `os.replace` | none | PASS |
| `promotion.verify` | released `scripts.golden.promotion_trust.validate_contract` plus fixed read-only four-mart DuckDB checks | none; all four independent grains non-empty | PASS |
| `workspace.reset` | marker/descriptor-verified app-owned reset | none | PASS |

The admissible feasibility score is `7/8`. A diagnostic negative control changed dbt's private
multiprocessing context and the process-wide start method to `fork`; under that non-admissible
startup manipulation, dbt completed 51 models / 186 build nodes with `PASS=179`, `WARN=7`,
`ERROR=0`, and no child. This proves the SQL workload itself can run without a child, but it is
not a released dbt API, relies on private state/startup manipulation, and is forbidden by the
request and existing startup/plugin policy. It cannot count as readiness or future implementation
authority. dbt also performs its adapter load through a dynamic module factory; caller-selected
plugins remain forbidden, and even an exact statically pinned DuckDB allowance would not resolve
the resource-tracker child.

Each semantic command remains separately executed and reaped. dbt leaves process-local DuckDB
adapter state unsuitable for a subsequent read-only export in the same worker; a fresh worker per
operation is therefore also required even after a future approved dbt backend exists.

## Required Decision Before Any Cook

The owner/platform decision must select one independently reviewed route without changing Issue
#9 source in this blocked context:

1. Provide a released, pinned dbt programmatic backend that uses only thread/in-process
   synchronization and no dynamic startup hook, fork, spawn, subprocess, or exec. It must run the
   exact Stage A 51-model/186-node build under `deny process-fork` and the complete containment
   profile.
2. Approve a separate backend design with an equally strong documented no-sudo Darwin lifetime
   primitive that controls every allowed dbt helper including rapid double-fork/`setsid`. No such
   primitive is currently proven; process groups, launchd, and polling do not qualify.
3. Explicitly revise and rerelease the upstream acceptance contract to a useful staged command
   set. This is a shared-contract/product decision, not authority for Issue #9 to silently drop
   `retail.dbt-build`.

Until one route is released and this plan is freshly amended, validated, and audited,
`DEPENDENCY_BACKEND_IN_PROCESS_UNAVAILABLE` keeps readiness false and allocates no runner
operation/workspace.

## Conditional Stronger Invariant After the Dependency Is Resolved

The following design is mandatory if and only if all eight released commands later reproduce
through reviewed fixed in-process adapters:

1. The parent launches exactly one fixed operation worker into a profile containing
   `deny process-fork`; no descendant can be created under that worker sandbox.
2. The parent records the worker's PID and kernel start identity before capability handoff and
   owns the single worker through normal completion, same-process `setsid`, image replacement,
   crash, deadline, TERM 5 seconds, KILL 5 seconds, and `wait`.
3. Any descriptor or reviewed adapter that requires fork, spawn, subprocess, multiprocessing
   process synchronization/resource tracking, or exec is unavailable and fails readiness before
   operation allocation. It cannot be advertised until a separately approved backend exists.
4. Resource authority is per worker: process RSS and CPU, wall time, file/FD/output/workspace
   limits, zero descendants, and bounded evidence. Process-tree aggregation/polling is removed as
   authority.

This conditional invariant is not selected at this input because `retail.dbt-build` fails item 3.
`DESCENDANT_STRATEGY=none` is therefore the honest current disposition.

## Mandatory TDD Capability Tests for a Future Approved Backend

These tests strengthen the existing stable IDs; no existing acceptance or oracle may be weakened:

- `RED-DESC-001`: in an admitted worker, `fork`, `posix_spawn`, subprocess, multiprocessing
  `fork`/`spawn`/`forkserver`, and a TERM-ignore child attempt each return a denial before a first
  child marker; exact worker PID/start cleanup ends with zero survivors.
- `RED-DESC-002`: a rapid double-fork/reparent/`setsid` attempt is denied at the first fork before
  any child marker. Separately, the main worker calls `setsid`, ignores TERM, retains PID/start
  identity, is KILLed and waited, and leaves zero survivors.
- `RED-INT-001` / `RED-IMP-003`: every released descriptor maps to one statically reviewed fixed
  adapter; AST/import/entry-point closure proves no exec/subprocess/dynamic plugin/startup hook.
  `retail.dbt-build` must reproduce the exact build without any private-context override.
- `RED-QUOTA-001..003`: wall/CPU/RSS/disk/file/FD/output limits act on the exact single worker;
  process count is one worker and zero descendants at every barrier.
- `RED-NET-001..002`, `RED-BASE-001..002`, and `RED-ENV-001..002`: the real eight-command
  operation flow reproduces network denial, workspace-only writes, byte-exact base, fake-secret
  denial, credential absence, and sanitized evidence.
- Every child-creation case first passes an unsandboxed negative control, records initial/final
  inventories, and proves zero survivors. Missing Seatbelt, changed host/runtime, missing dbt
  capability, setup failure, skip, xfail, or polling-only evidence is a hard failure.

## Resource, Evidence, S3, and Rollback Effect

- Current future resource tables and `process-tree` language are not implementation authority.
  They become the single-worker/zero-descendant model only after the backend gate above passes.
- Capability evidence must record exact host/build/Python/Seatbelt/profile hashes, worker PID/start
  roles (not raw private paths), negative-control markers, per-case errno, before/after inventory,
  exact operation adapter IDs, dbt result counts, zero survivors, and the dependency decision.
- The existing nine-row S3 catalog remains required. `S3-POL-001` must additionally reject worker
  fork/spawn/subprocess/exec calls, multiprocessing process primitives, caller-selected imports or
  plugins, and any private dbt-context/start-method mutation. `S3-RUN-001` must require the two
  descendant negatives and exact single-worker reap.
- Rollback first refuses new work, validates the service/worker PID and start identity, applies
  bounded TERM→KILL→wait only to that worker, verifies zero descendants/socket, and then follows
  existing marker/descriptor/fence/pointer/evidence rules. launchd, `pkill`, process-group-only
  cleanup, polling discovery, broad recursive cleanup, sudo, and containers remain forbidden.
- No new public command is added and none of the exact four future gate commands is removed. At
  this input they are not runnable implementation gates; `COOK_SCOPE=none`.

## Verification and Publication Gate

The current plan change must pass strict CK structure/status, local links/anchors/placeholders,
exact Stage A 38-pin recomputation, the 8-row adapter table, exact path/command/requirement/threat/
RED/S3 catalogs, diff/protected/private-path scans, checksum closure, and an independent fresh
whole-plan readiness audit. Those planning checks can pass while capability readiness remains
blocked; they may not convert `7/8` into an implementation PASS.
