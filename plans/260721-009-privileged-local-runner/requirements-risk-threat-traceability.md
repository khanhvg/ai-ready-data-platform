# Requirements, Risk and Threat Traceability

## Requirement Crosswalk

| ID | Requirement | Verification authority | Fail-closed response |
|---|---|---|---|
| RUN-DEP-01 | Implementation head is a clean remote-equal descendant of released Stage A fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9 and the 38-pin/21-member closures match | ancestry, blob and SHA-256 recomputation | Stop before any build/write |
| RUN-OWN-01 | Writes are exactly apps/lab-runner/** and mk/issue-5/i5-04.mk; the app-owned ignore rule covers only marker-owned .local-state; Issue #13 only consumes released image/launcher | changed-path, ignored-inclusive status, protected-hash and overlap scans | Reject unlisted/overbroad ignore path; replan |
| RUN-TRN-01 | Owner-only UDS or explicit random loopback admission validates peer/Host/Origin/bearer/CSRF/content/framing/Fetch Metadata/body before allocation | transport RED suite | Reject with bounded problem; allocate nothing |
| RUN-TRN-02 | Browser receives no engine/container credential and never contacts Docker or runner container | browser-shaped integration and secret scans | Keep API private; no CORS/fallback |
| RUN-CMD-01 | Exactly eight released zero-argument commands map to fixed descriptors; no shell/executable/argv/env/path/URL/SQL/plugin/install/image/Docker override | schema/registry/property/argv tests | Reject before Engine access |
| RUN-ENG-01 | Only an allow-listed effective-UID-owned local Unix Engine socket and minimal fixed lifecycle/archive API are used; ambient Docker/proxy config is ignored | stopped, wrong-owner, remote and API-spy tests | RUNNER_ENGINE_UNAVAILABLE |
| RUN-IMG-01 | Runtime uses the actual admitted linux/arm64 image manifest digest with pull-never; no plan-predicted/tag-only identity | build lock, inspect, offline runtime test | RUNNER_IMAGE_UNADMITTED |
| RUN-SUP-01 | Base, wheels, context, SBOM, provenance, license and Critical/High vulnerability gates are measured and closed | supply-chain catalog and reproducibility evidence | Stop build/release |
| RUN-CNT-01 | Effective state is non-root 65532, read-only root, private tmpfs, network none, private PID/IPC, init, cap-drop ALL, no-new-privileges, seccomp, no added host devices/device requests, privilege, ports, socket or source mounts | requested-versus-inspect policy test | RUNNER_CONTAINMENT_UNAVAILABLE |
| RUN-PID-01 | PID namespace, init/subreaper, pids cgroup and stop/TERM/KILL/wait/remove contain rapid double-fork, reparent, setsid, daemon and dbt tracker descendants | real adversarial lifecycle tests and zero-residue evidence | Tear down exact container; no commit |
| RUN-FS-01 | Input/output archives allow only normalized declared directories and single-link regular files with exact owner/mode/count/size/hash; root/base is immutable | traversal/link/special/swap/root-write tests | RUNNER_INPUT_INVALID or RUNNER_OUTPUT_INVALID |
| RUN-ENV-01 | Container env is an explicit closed map without host home, cloud, credential, proxy, Docker, Python/dbt plugin or tracing state | canary dump and artifact scan | Kill/remove; retain hashes only |
| RUN-NET-01 | Network none denies DNS/TCP/UDP/listen/cloud metadata and publishes zero ports | real probes plus inspect | RUNNER_CONTAINMENT_UNAVAILABLE |
| RUN-RES-01 | One container; pids 64, aggregate cgroup memory 536870912 bytes/zero swap, CPU 2, workspace/output 256 MiB, tmp/run/shm 64+16+16 MiB, file 128 MiB/4096, FD 256 and host reserves 6 GiB memory/disk | effective cgroup/rlimit/quota probes and peak budget | Refuse/terminate without commit |
| RUN-OUT-01 | stdout/stderr cap 2 MiB each, preview 128 KiB each, protocol 64 KiB; total wall is 110 s execute + 5 s TERM + 5 s KILL/wait/remove | flood and TERM-ignore tests | Bounded failure; remove container |
| RUN-FEN-01 | One global active-container lock plus workspace lock and monotonic fence prevent stale commits | deterministic barriers and restart tests | Conflict/reconcile; prior state current |
| RUN-STA-01 | Released CAS/idempotency/reset semantics survive duplicate, conflict, crash and lost acknowledgement | canonical digest, fault injection and replay tests | Last committed state; never rerun committed result |
| RUN-AUD-01 | Audit is insert-only, hash-chained, fsync-backed, sequence-complete, redacted and linked to bounded evidence | mutation/tamper/truncation/canary tests | Quarantine audit; disable mutation |
| RUN-REL-01 | retail.export admits exact ordered eleven assets and atomically advances one same-filesystem current pointer under live fence | asset matrix and kill-at-boundary tests | Prior complete release remains current |
| RUN-EVD-01 | The three activated I5-04 gate verifiers emit fitness-result-v2 within 120000 ms from fresh hash-closed shard sets; protected I5-01 data-contracts-check remains fitness-result-v1; learner verification emits learning-evidence-v1 | released registry/validators, canonicalization, duration and closure scan | Gate fails; no version conflation or unsupported claim |
| RUN-OPS-01 | All eight real commands run in the same locked container backend; dbt uses pinned dbtRunner and contained tracker; golden expert behavior is unchanged | all-eight and expert comparison suite | Any result below 8/8 blocks release |
| RUN-TDD-01 | Public-path adversarial tests and fixtures are committed RED before production launcher/image behavior | RED manifest and Git history | No production cook until corrected |
| RUN-ROL-01 | Rollback disables admission, removes only exact recorded containers, restores previous verified pointer and deletes only marker/inode-owned transient state | two rollback rehearsals including stale identity | Refuse ambiguous cleanup |
| RUN-APP-01 | Two independent strict reviews and human approval bind the same clean remote-equal implementation head | exact-head attestations and zero Critical/High | Changed head invalidates approval |

## Exact Operation Catalog

| Operation | Baked entrypoint authority | State/output boundary | Cook proof |
|---|---|---|---|
| workspace.prepare | Released workspace helper | New private ready workspace | Real small-42 result and exact hashes |
| retail.generate | data-generator/generate.py | Generated input state | Seed 42 determinism and expert equality |
| retail.load | ingestion/load_raw.py | DuckDB workspace generation | Real schema/row contract |
| retail.dbt-build | Pinned dbtRunner plus released dbt project | Models/tests in workspace | Real dbt build, tracker in namespace, zero residue |
| retail.export | serving/export_marts_snapshot.py plus release contract | Exact eleven-asset output stage | Exact ordered set and atomic host publication |
| promotion.configure | Released learner workspace adapter | Configured learner state | Controlled-failure setup without golden change |
| promotion.verify | Released verifier/contracts | learning-evidence-v1 | Required assertion and deterministic evidence |
| workspace.reset | Released reset semantics | New ready generation | Atomic, idempotent, progress/evidence preserved |

Every row uses zero caller arguments, network denied, 120 seconds and 536870912 worker bytes. No
row has a host semantic implementation or Airflow substitute.

## Protected Boundaries

- Released learning/OpenAPI/data contracts and readers are read-only.
- Golden generator/load/dbt/export/workspace semantics are read-only.
- Root Make, docker-compose.yml, all profiles/Compose, orchestration/airflow/**, cloud, Terraform and
  Kubernetes are denied.
- The host engine socket is a powerful owner capability and is never shared with browser/container.
- The container output archive is hostile until exact host validation completes.
- Issue #13 may consume only the released launcher/image record and cannot own runner internals.

## Threat Catalog

| ID | Threat | Controls | Adversarial proof | Residual boundary |
|---|---|---|---|---|
| THR-RCE-01 | Unknown command, metacharacter or option smuggling reaches execution | Closed schema/enum, fixed descriptor, no shell | zero-or-exact argv spy | Compromised reviewed baked code is supply chain |
| THR-BRW-01 | CSRF, DNS rebinding, CORS or browser direct request triggers container | UDS/random secret, exact Host, empty Origin, bearer+CSRF, no CORS | full browser-shaped matrix before allocation | Future portal/BFF is Issue #10 scope; Issue #13 owns local profiles |
| THR-ENG-01 | Remote/wrong socket or ambient Docker config redirects privileged control | fixed local socket/type/UID and ignored environment | remote/TCP/context/proxy/wrong-owner negatives | Same-user malicious engine is outside app isolation claim |
| THR-SOC-01 | Docker socket/credentials enter runtime and enable sibling control | no socket/config/home mount; closed env; image scan | in-container socket/config probes fail | Host launcher legitimately owns narrow engine access |
| THR-SUP-01 | Base, wheel or context substitution adds malicious code | observed digests, hashed offline wheels/context, SBOM/provenance/license/CVE gates | drift, tag-only, untracked and reproducibility tests | Newly disclosed issue follows normal revocation |
| THR-ENV-01 | Credential/proxy/plugin/home canary leaks or changes behavior | empty closed env, baked runtime, private tmpfs | canary dump/import/output scans | Baked approved config remains trusted input |
| THR-NET-01 | Operation exfiltrates, listens or reaches metadata | network none, no ports/proxies | DNS/TCP/UDP/listener/metadata probes | Engine host networking is outside container and never exposed |
| THR-PTH-01 | Traversal, link, special file, sparse file or archive confusion escapes roles | normalized manifest, tar preflight, no-follow FDs, type/link/owner/size/hash checks | symlink/hardlink/FIFO/socket/device/swap matrix | Host kernel defect outside claim |
| THR-ROF-01 | Operation mutates baked root/source | read-only root and no source mount | create/write/chmod/rename/delete/link probes | Approved tmpfs roles are intentionally writable |
| THR-PID-01 | Double-fork/reparent/setsid/daemon survives timeout or main crash | private PID ns, PID1 init, subreaper, cgroup and whole-container removal | rapid real descendants and zero survivor/ns evidence | Polling is evidence, never authority |
| THR-FRK-01 | Fork bomb exhausts host | pids-limit 64, one container, container lifecycle | real bounded bomb, cgroup event and removal | Engine/kernel overhead covered by host reserve |
| THR-RES-01 | CPU/memory/disk/file/FD/output/wall exhaustion harms host | exact cgroup/rlimit/tmpfs/file/output/deadline limits and reserves | enforcement/flood/TERM-to-KILL matrix | 16 GiB host admits only one active operation |
| THR-STL-01 | Stale/reused container identity is killed or commits foreign output | durable ID+labels+image+fence; exact inspection only | reuse/mismatch/interrupted cleanup tests | Unknown objects are preserved, requiring manual inspection |
| THR-RAC-01 | Two operations/reset/export/verify commit mixed state | locks, monotonic fence, CAS, staging and atomic rename | deterministic barriers | Filesystem corruption leads to quarantine |
| THR-CRS-01 | Crash across Engine/archive/fsync/rename/ack loses truth | durable lifecycle, reconciliation, commit ordering | kill every boundary | Bounded owned residue may need manual inspection |
| THR-IDM-01 | Replay runs twice or changed request reuses key | JCS request digest and unique key | same/different replay before/after restart | Key is not authorization |
| THR-AUD-01 | Audit is edited, truncated or stores secrets | insert-only triggers, hash chain, fsync, allow-list | mutation/tamper/canary tests | Same-account owner can alter code; no non-repudiation claim |
| THR-REL-01 | Missing/mixed/duplicate eleven assets become current | exact manifest/order/hash, fence, atomic pointer | complete failure matrix/readers | Remote catalog publication is outside Issue #9 |
| THR-OVR-01 | Issue #9 and #13 duplicate or mutate runner/profile responsibility | exact path ownership and protected hashes | changed-path/remote-plan overlap scan | Later scope change requires both plans amended |
| THR-AVL-01 | Missing engine triggers host fallback or silent weakening | typed preflight and no alternate backend | stopped/socket-absent test | Local app start is explicit prerequisite side effect |

## Risk Priority

RUN-PID-01, RUN-CNT-01, RUN-OPS-01, RUN-SUP-01 and RUN-REL-01 are release-critical. Any failure,
skip, unverifiable effective runtime field, 7/8 operation result, predicted digest, unresolved
Critical/High finding or ownership overlap blocks the whole cook. No polling-only containment,
waiver synthesis or partial operation release is permitted.
