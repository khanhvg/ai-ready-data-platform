# Implementation Boundary and Design

## Authority

This file translates the [platform amendment](./platform-amendment.md) into cook seams. It is not
implementation approval. The implementation base must be a clean remote-equal descendant of
released Stage A fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9, and every measured image/base digest
must be recorded at cook rather than copied from a plan.

## Write Boundary

Cook may create or modify only apps/lab-runner/** and mk/issue-5/i5-04.mk. Shared contracts,
learning content, golden pipeline code, dbt models, data generator/loader/exporter, root Make,
docker-compose.yml, orchestration/airflow/**, portals, profiles, cloud, Terraform and Kubernetes are
read-only or denied. Existing expert commands remain unchanged.

The exact path admission is in [planned-paths-and-admissions.md](./planned-paths-and-admissions.md).
Issue #13 is downstream: it may later call the released launcher and consume the image release
record, but it cannot write any Issue #9-owned path.

## Process and Data Flow

1. The owner launches the host service. It establishes a private UDS or an explicit random-loopback
   listener, creates per-launch admission secrets and validates the released Stage A contract set.
2. A request passes transport, closed-schema, command-enum, idempotency, workspace revision and
   mutation-fence checks. Rejection allocates no container or operation state.
3. The launcher preflights the allow-listed local user socket and effective Engine capabilities.
   Missing/stopped engine returns RUNNER_ENGINE_UNAVAILABLE. There is no host execution fallback.
4. The launcher produces a deterministic bounded input archive from the last committed private
   workspace and fixed metadata. The repository is never mounted.
5. It creates one uniquely named container from the locked image digest with the closed runtime
   policy, records container identity durably, and starts its fixed supervisor in input-wait state.
   It then copies only the exact input archive into the now-mounted private tmpfs.
6. PID 1 init and the supervisor admit the completed input marker, verify the manifest, register
   reaping, map one command enum to one fixed in-image callable, and only then run it inside the
   private PID namespace/cgroup.
7. On terminal status, the launcher copies the declared output archive, validates it before
   extraction, then always stops/kills/waits/removes the recorded container.
8. With a still-live fence, the host commits validated workspace/result/audit/evidence and, for
   retail.export, atomically advances the exact eleven-asset release pointer.
9. Replay returns the committed result. Startup reconciliation converges only recorded owned
   identities and never scans/removes unrelated containers.

## Component Boundaries

| Component | Responsibility | Must not do |
|---|---|---|
| transport | UDS/random-loopback trust boundary, body/framing/admission | Talk to Docker from browser input before full admission |
| registry | Closed eight-command mapping and exact version/hash checks | Accept argv, env, path, URL, SQL, plugin or selector overrides |
| engine client | Minimal fixed local Engine lifecycle and archive API | Read ambient Docker/proxy/registry config or contact TCP engines |
| container backend | Build create specification, durable identity, start-awaiting-input/copy/verify/execute/inspect/teardown | Mount repository/socket, publish ports, weaken failed controls |
| input/output admission | Deterministic archive, path/type/ownership/size/hash checks | Extract links/special files or trust container declarations alone |
| supervisor | Input verification, subreaping, fixed callable dispatch, bounded protocol | Install packages, listen on network or access Docker |
| operation adapters | Invoke exact baked golden modules and pinned dbtRunner | Reimplement or change expert/golden semantics |
| state/fence/audit | CAS, idempotency, monotonic fence, reconciliation, append-only evidence | Execute semantic pipeline work |
| release publisher | Validate and atomically publish exact eleven assets | Publish partial/mixed/unfenced output |

## Container Lifecycle State Machine

The durable states are admitted, creating, created, started-awaiting-input, inputs-copied,
executing, output-ready, tearing-down, removed and terminal. Each transition records operation ID, fence, image digest and
container ID before the corresponding external action. Reconciliation is monotonic:

- no recorded ID means no destructive Engine action;
- created, started-awaiting-input and executing identities are inspected by exact ID and owner labels;
- label/image/fence mismatch is stale identity and cannot commit or be broadly removed;
- an exact owned live container is stopped, KILLed after grace, waited and removed;
- an already absent exact container makes teardown idempotently complete;
- output is never admitted from a container whose identity, image, fence or terminal state differs.

The supervisor returns a small closed result protocol, but a success message is insufficient.
Commit requires container terminal state, admitted archive and successful teardown. Docker init,
the supervisor subreaper, private PID namespace, pids cgroup and remove lifecycle are containment
authority. PID polling is only evidence.

## Fixed Operation Dispatch

The internal registry contains exactly:

- workspace.prepare
- retail.generate
- retail.load
- retail.dbt-build
- retail.export
- promotion.configure
- promotion.verify
- workspace.reset

Every value maps to an immutable callable descriptor baked and hashed in the image. Commands have
zero caller arguments. Python runs isolated from user site/startup configuration. retail.dbt-build
uses the pinned dbtRunner API; expected multiprocessing resource-tracker children remain in the
same namespace/cgroup and are gone when the container is removed. No shell expansion or generic
subprocess API is exposed at the transport boundary.

## Filesystem Model

The image root and baked application are read-only. The operation gets only private tmpfs roles:
input, workspace, output, tmp and run. The launcher copies a closed input archive rather than bind
mounting source. The supervisor checks manifest hash, regular-file type, single-link count, numeric
ownership, mode, count, size and path grammar before use. The operation writes only workspace and
output roles.

Output is copied as an archive stream and treated as hostile. Validation happens before extraction
and again through retained directory descriptors at use time. The state store uses unique staging,
file and directory fsync, live-fence recheck, atomic same-filesystem rename and parent fsync.
Cleanup requires owner marker, nonce, device and inode agreement and refuses ambiguous targets.

## Runtime and Engine Admission

The canonical specification is the table in the platform amendment. Cook must compare requested
and effective Engine inspect state for image digest, UID/GID, read-only root, tmpfs options,
network/ports, PID/IPC modes, init, capabilities, no-new-privileges, seccomp, devices, privilege,
pids, memory/swap and CPU. It also proves cgroup v2 accounting and kernel-enforced limits. An
ignored field is not a warning; it is RUNNER_CONTAINMENT_UNAVAILABLE.

The custom seccomp profile denies AF_INET/AF_INET6/AF_PACKET/AF_NETLINK socket creation and
namespace/mount/ptrace/keyring/BPF surfaces while retaining only required local IPC and normal
process creation. This is layered with network none and zero ports; process creation remains
available because dbt resource-tracker is an admitted in-namespace descendant.

Engine resolution accepts only the installed local Docker-compatible user socket after type and
effective-UID ownership checks. A stopped engine is RUNNER_ENGINE_UNAVAILABLE. The service never
starts it. Cook automation may start OrbStack only after a separately recorded local side-effect
gate and must stop on admin/TCC interaction. No runtime registry access is allowed.

## Resource Accounting

Only one operation container may be active. The hard operation-container envelope is exactly
536870912 bytes aggregate memory with zero swap, 2 CPUs and 64 PIDs. Init, supervisor, the entire
worker descendant tree, page cache and actual tmpfs use share that cgroup ceiling. Before dispatch,
the supervisor also fixes per-process RLIMIT_AS at 536870912, RLIMIT_FSIZE at 134217728 and
RLIMIT_NOFILE at 256. Workspace and its output staging subtree share one 256 MiB tmpfs; temporary
tmpfs is 64 MiB, run state is 16 MiB and private /dev/shm is 16 MiB. Those tmpfs sizes are nested
maxima, not additive memory allowances.
Individual files are 128 MiB, the file count is 4096, stdout/stderr are 2 MiB each, previews are
128 KiB each and protocol is 64 KiB. The 120-second contract is divided into 110 seconds execution,
5 seconds TERM and 5 seconds KILL/wait/remove reserve. Admission requires 6 GiB host memory and
6 GiB disk free.

Cook must empirically prove the real eight-operation peak, including dbt, stays inside the envelope
on the observed 16 GiB host. It may reduce concurrency only to the already-required one; it may not
increase released command/workspace ceilings without owner review.

## Durable Semantics

The host maintains one lock and monotonic fence per workspace plus a runner-wide one-active lock.
The request key is bound to the released canonical request digest. Same key/same request returns one
result; same key/different request conflicts. A stale fence cannot advance workspace, audit,
evidence or release pointers. The append-only audit is hash chained, fsync backed and contains only
typed bounded fields and hashes.

Durable control state uses one owner-private SQLite database with foreign keys, WAL and
synchronous FULL. Unique request-digest constraints, monotonic fence compare-and-update and
insert-only audit triggers share the commit transaction. WAL/database/parent durability and restart
recovery are fault-injected; a filesystem that cannot satisfy the required sync semantics is
RUNNER_RESOURCE_UNAVAILABLE.

workspace.reset creates and validates a new ready-state generation, commits by atomic pointer and
preserves progress/evidence. retail.export produces all eleven assets inside the container. The
host admits the whole archive and publishes one immutable generation plus exact manifest before
advancing current. Kill injection at every transaction, archive, fsync, rename, teardown and ack
boundary must expose only last committed state.

## Build and Release Design

The Dockerfile and its adjacent Dockerfile-specific ignore file live under
apps/lab-runner/container. A deterministic context builder emits only the reviewed allow-list.
The linux/arm64 base is pinned by an observed platform manifest digest; Python wheels are fully
hashed and installed offline. Build output is local OCI, never pushed. The build lock binds the
actual base/image/config digest, context and Dockerfile hashes, platform, dependency locks, SBOM,
provenance, license closure, vulnerability results and reproducibility attempt. The image release
record is written only after all eight real commands and security tests pass against that digest.

## Fail-Closed Errors

Stable problem codes include RUNNER_ENGINE_UNAVAILABLE, RUNNER_CONTAINMENT_UNAVAILABLE,
RUNNER_IMAGE_UNADMITTED, RUNNER_RESOURCE_UNAVAILABLE, RUNNER_INPUT_INVALID,
RUNNER_OUTPUT_INVALID, RUNNER_TIMEOUT, RUNNER_CONTAINER_LOST, RUNNER_STALE_IDENTITY,
RUNNER_CONFLICT and RUNNER_RECONCILIATION_REQUIRED. Responses contain no raw command, environment,
private path, Docker endpoint, archive content or engine diagnostic.

## Out of Scope

- Root Make, Compose/profile integration and Issue #13 UX.
- Any Airflow image, callable or DAG change.
- Cloud, AWS, Terraform, Kubernetes, registry push or remote catalog publication.
- General local shell execution, arbitrary container execution or multi-user/multi-tenant service.
- Approval of a future base/image/release/implementation digest or merge.
