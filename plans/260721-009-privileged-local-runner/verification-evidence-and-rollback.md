# Verification, Evidence and Rollback

## TDD Order

Phase 3 commits the complete RED manifest and inert fixtures before Phase 4 production launcher,
supervisor or Dockerfile behavior. Fast verifier tests enter the public Make targets; real
container cases enter the fixed no-argument shard harness. A RED result is valid only when the
case collects and fails at the intended missing policy/behavior. Engine absence may prove only the
dedicated RUNNER_ENGINE_UNAVAILABLE cases; it cannot stand in for real container coverage.

## RED Catalog

| ID | Adversarial case | Required assertion |
|---|---|---|
| RED-TRN-001 | Missing/forged/duplicate Host or DNS-rebinding host | Reject before body, operation, audit or Engine allocation |
| RED-TRN-002 | Non-empty Origin, cookie, browser Fetch Metadata, preflight or simple form | Reject; emit no permissive CORS response |
| RED-TRN-003 | Wrong/stale/missing/duplicate bearer or mutation CSRF | Reject before typed body allocation; never echo secret |
| RED-TRN-004 | Wrong content type, chunked/ambiguous length, invalid JSON or body over 16384 bytes | Bounded rejection before operation allocation |
| RED-TRN-005 | Wrong UDS peer or predictable/stable loopback listener | Refuse launch/request; use effective UID or random per-launch trust |
| RED-CMD-001 | Unknown schema/API/command/field/version or command argument | Reject before Engine lookup |
| RED-CMD-002 | Shell metacharacter, executable/argv/env/cwd/path/URL/SQL/plugin/install override | Engine spy sees no create or one fixed enum-derived spec only |
| RED-CMD-003 | Python startup/user site/dbt plugin/import shadow canary | Canary never imports; baked pinned origin or refusal |
| RED-ENG-001 | Engine stopped or socket absent | RUNNER_ENGINE_UNAVAILABLE; no state/container/host execution |
| RED-ENG-002 | Remote/TCP, wrong-owner, non-socket or symlink endpoint; ambient context/proxy/TLS | Refuse endpoint and expose no diagnostic secret |
| RED-ENG-003 | Effective runtime inspect omits/changes any mandatory control | RUNNER_CONTAINMENT_UNAVAILABLE and exact container teardown |
| RED-IMG-001 | Tag-only/wrong-platform/unlocked/replaced image or pull attempt | RUNNER_IMAGE_UNADMITTED; no operation start |
| RED-IMG-002 | Context has untracked/additional/link/special/case-collision/path-drift entry | Context build fails before Docker build |
| RED-IMG-003 | Unhashed wheel, sdist/online install, SBOM/provenance/license/Critical-High gap | Supply-chain gate fails; release record absent |
| RED-PID-001 | Rapid double-fork and reparent to PID 1 | All descendants remain namespace/cgroup-bound and are absent after remove |
| RED-PID-002 | setsid plus daemonized TERM-ignoring grandchild | TERM then KILL/wait/remove yields zero host survivors |
| RED-PID-003 | Supervisor/main process crashes while descendants run | Host reconciles exact identity; container/namespace disappears; no commit |
| RED-PID-004 | Real dbt multiprocessing resource tracker | Tracker exists only inside namespace, is expected, and is absent after removal |
| RED-PID-005 | Fork bomb | Effective pids-limit 64 produces bounded failure/cgroup event; host remains responsive |
| RED-PID-006 | PID polling disabled/delayed | Lifecycle still contains descendants; polling changes evidence only |
| RED-TIM-001 | Worker ignores TERM past 110 seconds | TERM grace then KILL/wait/remove completes by 120 seconds; no commit |
| RED-NET-001 | DNS, TCP and UDP outbound probes | All fail under network none with no external side effect |
| RED-NET-002 | AF_INET/AF_INET6 listener and published-port probe | Seccomp rejects Internet sockets and inspect reports zero published ports |
| RED-NET-003 | 169.254.169.254 and conventional cloud metadata host probes | Unreachable without DNS/proxy fallback |
| RED-FS-001 | Write/create/chmod/rename/delete/link against image root/base | All fail; baked hashes and read-only flag remain exact |
| RED-FS-002 | Absolute/parent/NUL/alternate/collision/overlong archive path | Reject before extraction or mutation |
| RED-FS-003 | Symlink, hardlink, FIFO, socket, block/char device or multi-link output | Reject whole archive; outside/prior state unchanged |
| RED-FS-004 | Sparse/oversize/too-many/wrong-owner/wrong-mode/wrong-hash file | Reject against logical and allocated quotas before commit |
| RED-FS-005 | Parent/output/pointer swapped after validation | Retained descriptor identity selects safe inode or typed failure |
| RED-ENV-001 | Cloud/token/key/password/proxy/SSH/Docker/home/tracing canaries | Container env/output/evidence contains neither name nor value |
| RED-ENV-002 | Docker socket/config/credential helper access from container | Paths absent; no mount/device/Engine reachability |
| RED-OUT-001 | stdout or stderr flood | Terminate at 2 MiB stream cap; retained preview at most 128 KiB |
| RED-OUT-002 | Protocol/output archive flood or binary/private-path/canary content | 64 KiB protocol and archive quotas hold; raw bytes never persist |
| RED-RES-001 | Aggregate worker/descendant/tmpfs allocator and swap pressure | Container cgroup 536870912-byte/zero-swap limit enforces bounded failure |
| RED-RES-002 | CPU spin | Effective 2-CPU cgroup and wall deadline bound use |
| RED-RES-003 | Workspace/tmp/file-count/file-size/FD fan-out | Exact tmpfs, 128 MiB, 4096 and FD 256 boundaries enforce |
| RED-REC-001 | Interrupt create/start-awaiting-input/copy/verify/execute/inspect/archive/stop/KILL/remove | Restart converges exact owned identity or returns typed stale state |
| RED-REC-002 | Missing/reused/label-image-fence-mismatched container identity | Cannot commit; unrelated identity is never removed |
| RED-REC-003 | Client disconnect or host crash after result before teardown | Reconciliation removes exact container before any replay commit |
| RED-FEN-001 | Two admitted mutations at deterministic barrier | One live fence commits; stale owner conflicts |
| RED-FEN-002 | reset/export/verify interleavings | Old-or-new complete workspace/release only |
| RED-IDM-001 | Same idempotency key and same canonical request before/after crash | One operation/result identity, no second container effect |
| RED-IDM-002 | Same key and different canonical request | Conflict before container allocation |
| RED-AUD-001 | Audit UPDATE/DELETE, truncation, reorder or chain edit | Mutation denied or tamper detected; runner disables commit |
| RED-CRS-001 | Kill before/after state/audit transaction and fsync | Last committed state and complete audit prefix only |
| RED-CRS-002 | Kill around output/manifest fsync and pointer rename | Previous or next complete pointer, never partial/mixed |
| RED-CRS-003 | Kill after durable result before response acknowledgment | Replay returns committed result without re-execution |
| RED-REL-001 | Missing/duplicate/reordered/mixed/wrong-generation asset | Exact eleven-set validation fails; previous pointer exact |
| RED-REL-002 | Concurrent release reader and same release replay | Every reader resolves one complete manifest; replay idempotent |
| RED-OPS-001 | Each of eight commands executed against locked digest | Eight real successes; no stub/fake/host/Airflow path |
| RED-OPS-002 | Expert golden comparison | Golden expert outputs/contracts remain unchanged |
| RED-ROL-001 | Rollback with live, absent, stale and foreign identities | Only exact owned identity/state affected; previous release restored |

## Container Residue Oracle

Every terminal success/failure test records the exact container ID, namespace PID identities,
mounts, cgroup, ports and Engine state. Acceptance is:

- exact container absent after remove;
- no recorded host PID/start identity remains;
- no operation PID/mount/network namespace remains reachable;
- no operation mount, cgroup task or published port remains;
- private staging is either committed or marker-owned/quarantined;
- unrelated pre-existing Engine objects and host processes are unchanged.

PID/process polling supplies before/after evidence. It is never credited as the action that
contains or reaps a descendant.

## Exact Public Commands

The long-running real test phase first executes exactly:

    python3.12 apps/lab-runner/tools/run-gate.py

The harness accepts no selector and must execute all 52 RED and 14 S3 declarations into fresh
hash-closed shard artifacts. The registered Make commands are bounded verifiers, not a dishonest
single duration envelope around the long sequential suite.

| Command | Coverage | Release condition |
|---|---|---|
| make runner-test | Verify fresh contract/unit/all-eight/dbt/expert/state/release shards | v2 verifier under 120000 ms; no stale/skip/fake; 8/8 |
| make runner-security-test | Verify fresh transport/Engine/supply-chain/PID/network/fs/env/resource/S3 shards | v2 verifier under 120000 ms; all required rows green |
| make runner-race-test | Verify fresh fencing/reconciliation/crash/idempotency/release/rollback shards | v2 verifier under 120000 ms; deterministic barriers |
| make data-contracts-check | Released I5-01 data/shared-contract regression | Existing v1 target unchanged and green |

## S3 Catalog

Every command is pinned in the Issue #9 tool/dependency lock or is a released repository command.
Evidence paths shown are runtime roles, not pre-created plan files.

| ID | Gate | Failure condition | Evidence role |
|---|---|---|---|
| S3-SYN-001 | Compile exact runner source/tests and validate JSON/TOML/Dockerfile/seccomp syntax | Any syntax/parse error or missing declared path | s3/S3-SYN-001.json |
| S3-CODE-001 | Pinned static security scan over host and container Python | Any unsuppressed High/Critical or unsafe exception | s3/S3-CODE-001.json |
| S3-DEP-001 | Offline audit of exact linux/arm64 lock, wheels, base OS and build tools | Advisory, hash mismatch, resolution attempt or unresolved High/Critical | s3/S3-DEP-001.json |
| S3-LIC-001 | SPDX/license/notice policy closure | Unknown/unlicensed/denied license or unclosed copyleft obligation | s3/S3-LIC-001.json |
| S3-PROV-001 | Base/platform/image/config/context/SBOM/provenance/reproducibility closure | Tag-only/predicted/missing/mismatched digest or artifact | s3/S3-PROV-001.json |
| S3-POL-001 | Deterministic source/Dockerfile/seccomp/Engine policy checker | Shell/eval/raw exec, ambient env/endpoint, socket/source mount, weak runtime field | s3/S3-POL-001.json |
| S3-CNT-001 | Requested-versus-effective container policy and adversarial summary | Ignored flag, survivor/residue, network/root/limit failure or polling authority claim | s3/S3-CNT-001.json |
| S3-SRC-001 | Changed-path allow-list, exact app-owned ignore rule, ignored-inclusive baseline delta, protected Stage A hashes and Issue #13 overlap | Any unowned/overbroad-ignore/unrelated-ignored/root/profile/Compose/Airflow/shared/cloud drift | s3/S3-SRC-001.json |
| S3-SEC-001 | Actual secret/private-path/URL/env/output canary scan | Raw secret/value/private absolute path/customer row or Engine diagnostic | s3/S3-SEC-001.json |
| S3-EVD-001 | Released fitness v2/v1, canonicalization and artifact size+SHA closure | Version conflation, duration breach, unknown/duplicate/missing field/artifact, hash mismatch or unsupported claim | s3/S3-EVD-001.json |
| S3-OPS-001 | All-eight exact operation and golden equality aggregate | Any command skipped/stubbed/faked/host-run; dbt tracker proof absent | s3/S3-OPS-001.json |
| S3-RES-001 | Peak/resource/reserve budget aggregate on 16 GiB host | Limit not effective, reserve crossed, more than one active runner | s3/S3-RES-001.json |
| S3-RAC-001 | Race/crash/idempotency/reconciliation/rollback aggregate | Any mixed state, duplicate effect, foreign cleanup or unresolved residue | s3/S3-RAC-001.json |
| S3-CLOUD-001 | No cloud/AWS/Terraform/Kubernetes/registry-push/admin path scan | Any cloud action, credential use, remote endpoint, privilege or runtime pull/install | s3/S3-CLOUD-001.json |

## Resource Budget Oracle

| Resource | Admission | Measurement |
|---|---|---|
| Active runner | One operation container total | runner lock plus Engine inspect |
| Host memory reserve | At least 6 GiB free before create; reserve never crossed | host before/peak/after |
| Host disk reserve | At least 6 GiB free in state/build filesystem | logical+allocated before/peak/after |
| Operation memory | Aggregate cgroup 536870912 bytes and zero swap | effective memory/swap values, events and peak; polling supplementary only |
| CPU | 2 CPUs | effective quota and usage |
| PIDs | 64 | effective pids.max/events and fork-bomb peak |
| Workspace/output | One shared 268435456-byte tmpfs | effective size plus logical/allocated usage |
| Temporary roles | 64 MiB tmp, 16 MiB run, 16 MiB private shm | inspect and usage |
| Files/FD | 128 MiB each, 4096 files, FD 256 | boundary fixtures and kernel errors |
| Output/protocol | 2 MiB streams, 128 KiB previews, 64 KiB protocol | exact counters and retained sizes |
| Wall | 110 s execution, 5 s TERM, 5 s KILL/wait/remove | monotonic timestamps, at most 120 s |

The released 512 MiB is the entire operation-container cgroup, including init, supervisor, worker
descendants, page cache and actual tmpfs use. Workspace/output 256 MiB and tmp/run/shm 96 MiB are nested
role maxima, not additional memory. If OrbStack cannot expose effective aggregate cgroup-backed
accounting and zero-swap enforcement, the gate fails; the plan does not raise limits or adopt
polling as authority.

## Evidence Closure

The fixed harness emits closed app-owned per-shard artifacts. Each of the three activated I5-04
verifiers checks a complete fresh exact-head/image/policy set and emits one closed fitness-result-v2
envelope within its own 120000 ms duration cap. Protected I5-01 data-contracts-check remains
fitness-result-v1. Detailed JSON, logs, process/namespace inventories, inspect snapshots, SBOM,
provenance and scan results are bounded referenced artifacts with exact size and SHA-256. Learner
proof remains learning-evidence-v1. Canonicalization is the released JCS profile. Unknown fields,
raw env/output, private absolute paths, recursive commit claims or unobserved digests fail closure.

The aggregate index binds implementation head/tree, Stage A closure, image digest, build lock,
runtime policy, activation, shard manifest, all four commands with their released evidence
versions, RED/S3 IDs, resource peaks, rollback attempts and independent exact-head reviews. A
changed source/image/head/policy invalidates the dependent evidence.

## Rollback Rehearsal

1. Disable admission and acquire the runner-wide lock.
2. Read only durable owner records; validate container ID, labels, image digest and fence.
3. Stop, KILL after grace, wait and remove only an exact owned live identity. Treat absent as
   idempotent; preserve mismatched/foreign identity for manual inspection.
4. Reconcile incomplete results to last committed state and restore the previous verified release
   pointer with fsync.
5. Remove only transient state whose marker, nonce, device and inode match. Preserve audit,
   evidence, immutable releases and unrelated state.
6. Re-run residue oracle, idempotency replay and expert/data-contract regression.

Rehearse once from a normal live operation and once from an interrupted cleanup/stale identity.
Never prune Docker, stop the engine, delete broad roots, alter cloud state or synthesize success.

## Final Acceptance

- Four exact public commands green on one clean remote-equal head.
- All 52 RED rows and all 14 S3 rows green with no required skip.
- Operation feasibility measured 8/8 against actual released image digest.
- Effective S3 containment and 16 GiB resource budget pass.
- Exact Issue #9 write set and Issue #13 non-overlap pass.
- Two independent strict implementation reviews and separate human exact-head approval remain
  required before merge.
