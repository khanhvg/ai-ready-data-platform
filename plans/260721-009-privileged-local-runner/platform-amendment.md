---
title: "Issue #9 local container platform amendment"
status: ready-to-cook
date: "2026-07-22"
startHead: "4774c711208ef9cb7050b72c88106dffc7016f04"
releasedStageA: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
backend: "local-rootless-container-pid-namespace"
containerPlatform: "linux/arm64"
operationFeasibility: "8/8-planned"
securityClass: "S3"
cloudAction: "none"
containerAction: "none"
---

# Local Container Platform Amendment

## Decision

Issue #9 will implement one dedicated local Docker-compatible runner backend. Every admitted
semantic command runs in a fresh operation container made from the same locked linux/arm64 image;
only one operation container may exist at a time. The host process is an owner-only launcher and
control plane. It validates the released API, owns CAS/idempotency/audit, creates and destroys the
container through fixed Engine API calls, imports verified outputs, and publishes committed state.
It does not execute any of the eight semantic operations.

This amendment supersedes the host-execution decision in
[capability-amendment.md](./capability-amendment.md). That report remains immutable evidence that
Seatbelt denied seven unwanted child-creation cases and reaped one exact worker, but the real
retail.dbt-build command necessarily starts Python multiprocessing resource-tracker state. A
strategy that forbids all descendants therefore supports only 7/8 operations and cannot be
weakened. A private Linux PID namespace, container cgroup, PID 1 init/subreaper and whole-container
stop/kill/remove lifecycle are the narrow fit: the expected dbt helper may exist only inside the
operation namespace while escaped descendant survival remains impossible at namespace teardown.

No future image, base-image or implementation SHA is approved or guessed here. Cook must measure
and bind each one before it can be used.

## Observed Local Readiness

Read-only inspection on the amendment start head observed:

| Item | Observation | Planning effect |
|---|---|---|
| Host | Darwin arm64, 16 GiB memory, 8 logical CPUs | Select linux/arm64 and the bounded small profile |
| Docker CLI | /usr/local/bin/docker, 29.4.0, client API 1.54, arm64 | Client prerequisite present |
| OrbStack | /usr/local/bin/orb and OrbStack.app 2.2.1 build 20628 | Local engine implementation present |
| Context | orbstack selected | Only its resolved user-owned local socket may be admitted |
| State | OrbStack stopped; user socket absent; docker version/info cannot reach the engine | Return RUNNER_ENGINE_UNAVAILABLE; never fall back |

The stopped engine is a cook/runtime prerequisite, not an unresolved platform choice. Cook may
start the installed local app only after recording a separate local-side-effect gate. An admin or
TCC prompt, a socket not owned by the effective user, a remote/TCP endpoint, or missing effective
runtime controls stops cook. This amendment did not start the engine, pull/build an image, or
create/start a container.

## Existing Asset Reuse Decision

The existing Airflow image and root Compose service are not a runner base. They use a tag-only
Airflow base, online pip install, shared profile network and ports, service credentials, and a
writable whole-repository mount. Those are intentional expert/profile properties but incompatible
with this runner's digest, offline, no-network, no-source-mount and ownership boundary. Reusing or
hardening them here would also overlap Issue #13.

Issue #9 instead reuses only read-only semantic assets: the released contracts/readers, golden
workspace/process/release helpers, generator, loader, dbt project and exporter. Their exact bytes
are copied by the deterministic context builder and baked into the dedicated image; none is
modified. The existing root Make wildcard already discovers a new mk/issue-5/i5-04.mk, so the root
Makefile is also left unchanged. This is the maximum reuse that preserves both containment and
ownership.

## Exact Operation Contract

The only semantic selector is one of the eight zero-argument command IDs released in
learning/labs/promotion-trust/lab-v1.json at Stage A. Every command has a 120-second wall ceiling,
536870912-byte worker-memory ceiling and denied network. The workspace quota is 268435456 bytes.

| Command | Real container behavior that cook must prove | Required result |
|---|---|---|
| workspace.prepare | Create the marker-owned small-42 workspace from baked, hash-locked inputs | Ready workspace bundle |
| retail.generate | Run the pinned deterministic seed-42 retail generator | Exact generated inputs |
| retail.load | Run the pinned DuckDB loader against the imported workspace | Exact database state |
| retail.dbt-build | Invoke pinned dbtRunner in-process; its multiprocessing tracker may run only inside the namespace | Real models/tests complete; tracker gone at teardown |
| retail.export | Produce and validate the exact ordered eleven Parquet assets | Complete release bundle, never partial |
| promotion.configure | Apply the released learner workspace configuration | Exact configured state |
| promotion.verify | Run the released verifier and controlled-failure/golden assertions | Real learning-evidence-v1 result |
| workspace.reset | Atomically create the released ready-state workspace while preserving progress/evidence on the host | Idempotent reset result |

No command may be dropped, stubbed, faked, rerouted to the host, or replaced with an Airflow
callable. The expert Make/Airflow behavior and golden semantics remain byte-for-byte unchanged.

## Architecture and Trust Boundaries

### Host control plane

The host service listens on an owner-only Unix-domain socket by default. A random loopback port is
allowed only where UDS peer credentials are unavailable, with an unguessable per-launch bearer and
CSRF secret communicated out of band to the owner process. Admission rejects before parsing or
allocation on wrong/duplicate Host, non-empty Origin, browser Fetch Metadata, cookies, preflight,
wrong content type, ambiguous length, body over 16384 bytes, stale bearer, missing CSRF, or schema
drift. There is no permissive CORS response. The browser never receives Docker credentials and
never talks to Docker or the operation container.

After released request validation and a durable fence, the host maps the enum to one fixed internal
container command. There is no raw shell, executable, argv, environment, working-directory, path,
URL, SQL, selector, plugin, package-install, profile, image, Docker flag, or cloud override. The
Engine client ignores DOCKER_HOST, DOCKER_CONTEXT, DOCKER_TLS_VERIFY, proxy and registry
environment. It resolves only the allow-listed local user socket, verifies it is a socket owned by
the effective UID, and uses a minimal fixed create/start/inspect/copy/stop/kill/remove API surface.

The host creates and durably records a unique container identity from the locked image digest,
starts its fixed supervisor in input-wait state so private tmpfs mounts exist, copies the exact hash
manifest plus prior validated workspace bundle, and signals one completed input marker. Only then
may the supervisor execute. The host later imports only the declared output archive. It never
mounts the repository or arbitrary host paths and never passes its environment, home, Docker
config, engine socket or engine credentials into the container.

### Per-operation container

Each request gets a fresh private PID/IPC/mount namespace and a new tmpfs workspace. Docker init is
PID 1 and the app supervisor registers as a child subreaper before launching the one fixed worker.
The supervisor may admit expected operation descendants, including dbt resource-tracker, but it
does not rely on a polled PID list for containment. Completion requires the worker tree to exit and
the supervisor to report a closed result. On success, failure, timeout, main-process crash, client
disconnect or host restart, the host converges on stop, TERM grace, KILL if needed, wait, and forced
remove of the recorded identity. Linux namespace teardown and cgroup/container lifecycle are the
authority that eliminates double-fork, reparented, setsid and daemonized descendants. Polling and
before/after inventories are evidence only.

The container has no Docker socket, added host devices, credentials, ports, DNS or external
network access.
It cannot create another container or contact the engine. Runtime package installation is absent.

## Effective Runtime Policy

Cook writes a closed policy document and proves the effective inspect state, not merely the launch
arguments. Any ignored or unavailable field is RUNNER_CONTAINMENT_UNAVAILABLE.

| Control | Required effective value |
|---|---|
| Image | Exact admitted linux/arm64 manifest digest; pull policy never |
| Identity | Numeric UID:GID 65532:65532, no supplementary groups, no ambient capabilities |
| Root | Read-only root filesystem; no writable image layer use |
| Input | Exact regular-file archive copied to private tmpfs and verified by path/type/mode/size/SHA-256 |
| Workspace/output | One private 256 MiB tmpfs; output is an exact bounded subtree inside that quota |
| Temporary/runtime | /tmp 64 MiB, /run 16 MiB and private /dev/shm 16 MiB tmpfs with nodev,nosuid/noexec where compatible |
| Network | none; no port publication; DNS, TCP, UDP and cloud metadata unreachable |
| Namespaces | Private PID, IPC, mount and network; never host PID/IPC/network; init enabled |
| Privilege | cap-drop ALL, no-new-privileges, no added host devices/device requests, no privileged mode, fixed custom seccomp |
| Process limit | pids-limit 64; fork bomb must hit the kernel/cgroup boundary |
| Memory | Container/cgroup hard limit 536870912 bytes and zero swap for init, supervisor, worker tree, page cache and tmpfs in aggregate |
| CPU | 2 CPUs maximum; one active operation container; worker CPU accounting retained |
| Files | Workspace 256 MiB, individual regular file 128 MiB, 4096 files, no links/special files |
| Descriptors | Worker RLIMIT_NOFILE 256; closed inherited descriptors |
| Output | stdout and stderr 2 MiB each, retained preview 128 KiB each, result protocol 64 KiB |
| Wall | Operation deadline 110 s, TERM grace 5 s, KILL/wait/remove reserve 5 s; total no more than 120 s |
| Host reserves | Refuse admission below 6 GiB free host memory or 6 GiB free state/build disk |

The released 536870912-byte command limit is the aggregate operation-container cgroup envelope,
not a per-process allowance. Init, supervisor, worker descendants, page cache and actual tmpfs
usage are all charged to it; memory.swap.max is zero. The 256 MiB workspace/output and 96 MiB
tmp/run/shm values are role maxima inside that same envelope, not additive reservations. Before
dispatch, the supervisor also sets per-process RLIMIT_AS to 536870912, RLIMIT_FSIZE to 134217728
and RLIMIT_NOFILE to 256 as defense in depth. Cook proves the aggregate cgroup limit and real peak
on OrbStack. If a real operation cannot run under these boundaries, cook stops rather than
revising the released contract or using polling as authority.

The custom seccomp profile is a reviewed deny-by-default delta over Docker's supported baseline.
It denies namespace creation/join, mount, ptrace, keyring, BPF/performance and raw-packet surfaces;
it also rejects AF_INET, AF_INET6, AF_PACKET and AF_NETLINK socket creation while permitting only
the minimal local IPC needed by the pinned runtime. Thus network-none and zero port publication are
not the only network layers. The profile must still allow ordinary process creation so the real
dbt resource tracker can run; pids/cgroup/namespace lifecycle, not a fork ban, contains it.

## Input and Output Admission

The image bakes the exact reviewed application/runtime inputs. Operation-specific mutable input is
a deterministic archive created under the Issue #9 private state root, never a repository bind
mount. Both ends validate the closed manifest. Only normalized relative UTF-8 paths are allowed;
absolute, parent, NUL, alternate-separator, duplicate/case-collision and overlong paths fail.

The host imports output through the Engine archive endpoint or the equivalent fixed docker copy
archive stream. It validates tar headers before extraction and accepts only declared directories
and single-link regular files with exact numeric ownership, mode, count, logical and allocated
size, and SHA-256. Symlink, hardlink, FIFO, socket, device, sparse/quota ambiguity, unexpected path,
extra file, missing file or ownership mismatch fails the operation and leaves current state
unchanged. Extraction uses directory descriptors, no-follow and same-filesystem atomic rename.

retail.export must contain exactly these eleven asset IDs in released order:

1. mart_daily_revenue
2. mart_top_products
3. mart_customer_cohorts
4. mart_fulfillment_performance
5. mart_returns_analysis
6. mart_promotion_effectiveness
7. mart_channel_geography
8. mart_inventory_health
9. mart_web_funnel_conversion
10. mart_supplier_purchasing
11. mart_data_quality

The container creates and validates the release manifest. The host revalidates the exact set,
ownership, size, schema/content hashes and generation/fence before fsyncing the immutable stage and
atomically replacing the same-filesystem current pointer. At every crash point readers see the old
complete release or the new complete release, never a mixed set.

## Image, Build and Supply-Chain Admission

Issue #9 owns apps/lab-runner/container/runner.Dockerfile and the adjacent
runner.Dockerfile.dockerignore. The specific ignore file must make the deterministic context
independent of the root ignore file. An Issue #9 context builder emits only a normalized tar of an
explicit allow-list: the Dockerfile, locked linux/arm64 wheelhouse, runner package, fixed container
policy, exact released source modules/contracts required for the eight operations, license files
and notices. It rejects untracked files, links, special files, path collisions and hash drift.

Cook performs these gates in order:

1. Resolve an official supported Python slim/Debian linux/arm64 base tag to its actual platform
   manifest digest and record registry, repository, tag, platform and digest. No tag-only FROM is
   admitted.
2. Fetch approved wheels under the separately recorded network/supply-chain gate, verify hashes,
   then build offline with no index and require-hashes. Runtime has no installer path.
3. Build with the locked Dockerfile/context and network disabled after inputs exist. Export an OCI
   artifact; do not push to a registry.
4. Record actual image manifest/config digests from build metadata, platform, Dockerfile/context
   hashes and reproducibility result in container-build-lock-v1. Never synthesize a digest.
5. Generate SPDX SBOM and provenance, inventory base OS and Python licenses, scan OS/Python
   packages for known Critical/High vulnerabilities, and close every finding or stop.
6. Deny unknown/unlicensed direct dependencies and AGPL, SSPL, noncommercial or source-available
   runtime terms. MIT, BSD, Apache, ISC, PSF and MPL are admissible with notices; LGPL is admitted
   only with dynamic-link/notice obligations recorded; GPL may appear only as an unmodified distro
   runtime package with source/notice obligations explicitly closed. Any ambiguity blocks release.
7. Run all eight operations and adversarial acceptance tests against the actual digest. Only then
   write runner-image-release-v1 binding actual image/build/SBOM/provenance/test evidence hashes.

Runtime uses that exact digest with pull-never. Issue #13 may consume the released identity but may
not choose a tag, rebuild it or substitute another image.

## Durable State, Recovery and Rollback

The host retains the released SHA-256 plus JCS idempotency contract, one workspace mutation lock,
monotonic fence epoch, last-committed state, insert-only hash-chained audit and referenced bounded
evidence. Container IDs are random and stored with owner marker, image digest, operation ID, fence
and start time before start. Startup reconciliation inspects only recorded identities. A missing,
changed or reused identity is stale and cannot commit; an owned live identity is stopped/removed;
unknown containers are never touched.

Interrupted create/start-awaiting-input/copy/verify/execute/inspect/archive/stop/remove paths are
idempotent. The supervisor cannot leave input-wait state until the completed input marker and
manifest pass verification. A result becomes committable only after container exit, full output
admission, live-fence recheck and durable audit intent. A crash before commit leaves the previous
state current. A crash after commit and before ack returns the committed result on replay. Reset
and rollback remove only marker-owned private state after descriptor/inode checks. Rollback
disables admission, converges recorded containers to removed, restores the previous verified
pointer, preserves audit/evidence, and never performs broad Docker or filesystem cleanup.

## Issue #9 and Issue #13 Ownership

| Area | Issue #9 | Issue #13 |
|---|---|---|
| apps/lab-runner/** | Sole owner: package, tests, container build/context/lock, policy, image release and launcher | Read-only consumer; no duplicate or modification |
| mk/issue-5/i5-04.mk | Sole owner: exact runner test targets | No modification |
| Root Makefile | Denied | May own only under its separately approved plan |
| Compose/profile files and local profile UX | Denied | Downstream owner |
| Airflow Dockerfile/callables/DAGs | Denied | No authority inherited from Issue #9 |
| Released shared contracts/golden source | Read-only exact inputs | Read-only unless separately authorized |

Issue #13 profiles may call the released launcher and consume runner-image-release-v1. They may not
mount over runner code, expose its API to a browser, inject flags/env, mount the Docker socket into
the container, or duplicate build/runtime policy. Root Make, docker-compose.yml and unrelated
profile files are not part of Issue #9 cook.

### Downstream engine-availability contract

The owner's explicit platform direction here supersedes any older cross-plan wording that could
be read to require a real semantic runner journey while Docker is unavailable. There is no
remaining backend choice:

- Issue #10 may keep an engine-unavailable negative test, but its real portal/runner journey has
  the admitted local engine and released runner image as prerequisites. With the engine absent,
  the only successful assertion is the typed RUNNER_ENGINE_UNAVAILABLE response with no fallback
  or allocation.
- Issue #13 may keep its Docker-unavailable host-core check only as that same fail-closed preflight
  assertion. A green check does not mean a semantic command ran. Its runnable runner profiles
  consume the released Issue #9 launcher/image and therefore require the local engine.
- The Issue #10 and #13 owners must carry this clarification into their own plan artifacts before
  their respective cooks. Issue #9 does not modify those downstream plans, profiles or tests.

This precedence is part of the owner authorization for the local container backend, not a future
implementation-head, image-digest or merge approval.

## Mandatory Cook Proof

The verification catalog in [verification-evidence-and-rollback.md](./verification-evidence-and-rollback.md)
is required, including real rapid double-fork, reparent, setsid, daemon, fork-bomb, timeout,
main-crash, network/DNS/metadata, read-only root, link/special-file, canary, output-flood, cgroup,
stop/remove, interrupted-cleanup and stale-identity cases. Polling may report evidence but cannot be
the mechanism that makes any descendant safe.

All eight real operations must pass against the final digest. retail.dbt-build must use the pinned
dbtRunner and demonstrate its multiprocessing tracker inside the namespace and zero namespace,
process, mount, port and container residue after removal. No owner choice remains open. The plan is
ready for whole-plan cook; any failure above is fail-closed and requires a new reviewed amendment.
