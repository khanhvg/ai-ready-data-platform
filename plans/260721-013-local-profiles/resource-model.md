---
title: "Issue #13 Resource and Measurement Model"
status: planned-unvalidated
targetHost: "16 GiB Mac"
created: "2026-07-22"
---

# Issue #13 Resource and Measurement Model

## Decision Hierarchy

1. Static service allowlist, dependency closure, configured ceilings, and combination rules are
   primary pass/fail gates.
2. Live preflight applies the same ceilings to the observed host/engine allocation and fails
   closed before supported Compose startup.
3. One cold plus two warm repetitions corroborate capacity/readiness and may block acceptance,
   but one noisy sample can never be the sole pass oracle.
4. Tags, historical README measurements, Compose `mem_limit`, or synthetic samples alone never
   satisfy Stage B.

## Owner-Approved Aggregate Baseline

| Gate | Deterministic rule |
|---|---|
| Host reserve | Preserve at least 4 GiB host memory and 2 logical CPUs |
| One heavy group | Configured aggregate `<=6 GiB` and `<=4 CPUs` |
| Exact guarded pair | Only `lake+governance`; configured aggregate `<=10 GiB` and `<=6 CPUs` |
| All three | `orchestration+lake+governance` denied before supported Compose startup |
| Other pair/combination | Denied unless a future exact allowlist amendment names it |

Static admission evaluates both absolute and host-relative formulas:

```text
group_memory <= group_or_pair_memory_ceiling
group_cpus   <= group_or_pair_cpu_ceiling
group_memory <= physical_memory - 4 GiB
group_cpus   <= logical_cpus - 2
host_available_memory_at_preflight >= group_memory + 4 GiB
engine_allocated_memory >= group_memory + declared_engine_overhead
engine_allocated_cpus >= group_cpus
```

Missing or unparseable host/engine allocation is a typed denial. Stage B additionally requires
the engine allocation to leave the host reserve in the observed normalized snapshot. No swap,
compression, or overcommit is counted as reserved physical memory.

## Actual Group Mapping and Initial Stage A Ceilings

Memory values preserve current Compose limits. CPU allocations are the initial deterministic
Stage A design; they remain within the owner aggregate and may change only by exact amendment.

| Group | Services | Memory | Planned CPU | Admission |
|---|---|---:|---:|---|
| `orchestration` | `airflow` | 4 GiB | 4.00 | Single only |
| `lake` | five current lake services | 3.25 GiB | 2.50 | Single; or guarded pair |
| `governance` | three current governance services | 4 GiB | 3.50 | Single; or guarded pair |
| `lake+governance` | exact union/closure | 7.25 GiB | 6.00 | Explicit guarded co-run only |
| all three | exact union/closure | 11.25 GiB | 10.00 | Always denied |

No `learning` group is admitted at the planning input because its services/images do not exist.
The dependency amendment must inventory actual released portal/runner/lab outputs before adding,
renaming, or budgeting any future group.

## Per-Service Configured Bounds

These are the initial Stage A values for actual services. Static tests require every field.
Persistent disk ceilings are admission-enforced byte-growth hard stops; tmpfs limits are Compose
hard limits. If the admitted engine cannot enforce/observe a required disk bound, the profile is
blocked rather than treated as measured.

| Service | Memory | CPU | PID cap | Writable disk ceiling | Log cap | Hard ready/exit deadline |
|---|---:|---:|---:|---:|---:|---:|
| `airflow` | 4 GiB | 4.00 | 512 | `airflow-home` 2 GiB; admitted workspace aggregate max 3 GiB | 3 x 10 MiB | 240 s |
| `minio` | 1 GiB | 0.75 | 128 | `minio-data` 3 GiB | 3 x 10 MiB | 90 s |
| `minio-init` | 256 MiB | 0.25 | 64 | 64 MiB tmpfs/writable layer | 3 x 10 MiB | 90 s exit |
| `lakekeeper-db` | 512 MiB | 0.50 | 128 | `lakekeeper-db-data` 512 MiB | 3 x 10 MiB | 90 s |
| `lakekeeper-migrate` | 512 MiB | 0.25 | 64 | 64 MiB tmpfs/writable layer | 3 x 10 MiB | 120 s exit |
| `lakekeeper` | 1 GiB | 0.75 | 256 | 128 MiB tmpfs/writable layer | 3 x 10 MiB | 150 s |
| `openmetadata-db` | 1 GiB | 0.75 | 256 | `openmetadata-db-data` 1 GiB | 3 x 10 MiB | 120 s |
| `openmetadata-search` | 1 GiB | 1.25 | 512 | `openmetadata-es-data` 2 GiB | 3 x 10 MiB | 210 s |
| `openmetadata-server` | 2 GiB | 1.50 | 512 | 256 MiB tmpfs/writable layer | 3 x 10 MiB | 300 s |

Additional required bounds:

- Explicit `restart: "no"` for acceptance runs; any restart count above zero fails the run.
- Read-only root filesystems where actual images pass characterization; every writable path must
  map to a named run-owned volume or size-bounded tmpfs.
- No unbounded build/pull/start/workload/health/measure/teardown subprocess. Parent timeout always
  includes a bounded termination grace and records escalation.
- Logs use local/json rotation with `max-size=10m`, `max-file=3`; evidence retains bounded command
  logs separately with redaction and byte caps.
- Volume and temp ceilings are declared per service and as an aggregate; growth beyond a ceiling
  stops the run and triggers ownership-scoped teardown.
- Port and volume ownership are required even when no collision is observed.

Exact per-service values must be rechecked against the dependency-amended Compose render before
Stage A implementation. A service/image change is not silently absorbed.

## Port, Volume, Project, and Network Ownership

- Current published ports remain the initial service ports but must bind `127.0.0.1`, never `*`.
- Admission checks requested host ports before startup and records `{service, containerPort,
  hostIp, hostPort, projectId, runId}`. An occupied, duplicate, missing, wildcard, or unknown
  binding denies admission.
- Named volumes remain project-scoped and receive run/project/purpose labels. Retained data must
  be explicitly classified; everything else is ephemeral run-owned state.
- Fixed current container names are collision-prone. The implementation may parameterize them for
  admitted runs while preserving the existing default expert path, but it must not change root
  Make ownership. Collision always denies rather than deleting or adopting the foreign object.
- Explicit project-private networks replace an implicit unclassified network. Published web UIs
  remain loopback-only. Backend data stores are not published unless an actual host command needs
  the current port and the allowlist records that need.
- No Compose file, environment input, or request may select an external network/volume/project.

## Minimal Measurement Matrix

There is no 3x3 cross-product. After Stage A GREEN, the exact actual admitted scenarios are:

| Scenario | Cold reps | Warm reps | Workload source | Acceptance role |
|---|---:|---:|---|---|
| `orchestration` | 1 | 2 | Exact released command/lab mapped by amendment | Corroborating |
| `lake` | 1 | 2 | Exact released command/lab mapped by amendment | Corroborating |
| `governance` | 1 | 2 | Exact released command/lab mapped by amendment | Corroborating |
| `lake+governance` | 1 | 2 | Exact released guarded ingest/lab | Required guarded-pair evidence |
| all three | 0 | 0 | None; static denial only | Required denial |

If an actual dependency-amended group has no real released workload, that scenario is blocked.
No noop, sleep, generated sample, expected-code echo, or profile-name-only run substitutes.

### Repetition State

- Pre-pull/build is outside readiness timing and must use only admitted digests. Pull duration is
  recorded separately; acceptance runs use `--pull never` or exact equivalent.
- Cold: no run-owned containers/network/temp bytes; fresh run-owned mutable volumes unless the
  released workload requires a declared retained seed. Image cache may remain and is recorded.
- Warm 1/2: containers/network recreated from the same exact config; only explicitly retained
  service data/cache persists. Inputs, image digests, limits, workload, and engine allocation stay
  identical.
- Sampling starts before Compose invocation and ends after teardown/residue inspection. Workload
  metrics begin only after all required health/one-shot readiness gates pass.
- Repetitions run sequentially. No parallel matrix and no unrelated workload on the target host.

## Normalization Record

Every run records, without secrets/private paths:

- OS/kernel, host architecture, physical memory, logical CPU count, host free/available memory,
  swap/compression state, filesystem and free disk;
- engine and Compose versions, engine architecture/storage driver, allocated memory/CPU/disk,
  cgroup mode, project ID, and measurement tool versions/hashes;
- exact input/tested-tree/Stage A/dependency SHAs, config/render hashes, image registry index and
  resolved platform digests, SBOM/signature/provenance verification results;
- cold/warm classification, repetition index, monotonic/wall-clock timing, sampling interval, and
  declared retained state.

If engine memory/CPU allocation or platform digest cannot be resolved exactly, the heavy result is
blocked. Docker-free core results remain independently runnable.

## Metrics and Attribution

Capture per repetition:

- peak per-service working set and RSS/cgroup memory plus configured memory limit;
- container CPU time/normalized utilization and host CPU pressure;
- wall time to each readiness gate, workload duration, total duration, and timeout/escalation;
- per-volume/writable-layer/log/temp disk growth and final retained bytes;
- readiness transitions, health output digest, one-shot exit status, restart/OOM count;
- teardown duration and residue for container/network/volume/temp/process/port.

Do not add container memory to Docker VM/process RSS and present it as one total. Report layers
separately: service/cgroup sum, engine VM/process footprint, and host available-memory delta.
Static configured aggregates remain the admission oracle.

## Result Rules

- Static omission, over-budget closure, unknown dependency, collision, wildcard port, missing
  deadline, or forbidden combination: deny before supported Compose invocation.
- All three: deny even if an operator changes numeric values below a ceiling.
- Guarded pair: admit only the exact `lake+governance` set, exact service closure, exact workload,
  Airflow absent, and all normalized authorities present.
- One failed static gate fails the scenario. One failed/blocked live repetition blocks heavy
  acceptance; do not average away OOM, restart, timeout, residue, or bound violation.
- Timing/RSS variation within hard bounds is reported as distribution/raw values. It is not a
  flaky millisecond equality test.
- Engine absent/unreachable: static Stage A checks may pass; Stage B and final required heavy
  fitness are blocked, never synthetic and never marked pass.
