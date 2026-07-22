# Issue #9 Requirements, Risks, and Threat Traceability

Current capability status is `BLOCKED` by the exact operation table in
[capability-amendment.md](./capability-amendment.md): descendant prevention passes, but the pinned
dbt API requires a child. The prevention language below is conditional on a future approved
all-eight-command backend and grants no cook scope now.

## Traceability Rules

- Every row is future implementation work unless marked planning/preflight.
- A requirement passes only with its named negative/positive tests, evidence artifact, rollback,
  and exact dependency identity. Prose or a skipped required tool cannot pass.
- `security:S3` means the issue-specific privileged local boundary. It does not mean Amazon S3
  and grants no cloud authority.
- The local guarantee is tamper-evident corruption detection inside the accepted single-actor
  model. It is not non-repudiation against root or a hostile same-account process.

## Requirement Crosswalk

| ID | Requirement and acceptance | Test/evidence | Master trace | Dependency / rollback |
|---|---|---|---|---|
| RUN-DEP-01 | Future implementation base descends from released Stage A `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` and locks the Phase 2 contract/registry/operation/evidence hashes; runtime refuses drift | dependency preflight JSON, Git ancestry/tree, contract mutation negatives | I5-03→I5-04; PH-C06; SC-20 | Hard block on mismatch; never create a local shared contract or generated binding |
| RUN-BND-01 | Writes remain inside `apps/lab-runner/**`, runner tests, app-owned runtime config, `mk/issue-5/i5-04.mk`, and the one characterized Airflow callable guard | changed-path manifest, protected-path hashes, default/DAG compatibility, `git diff --check` | OWN-01; ADR-001; issue #9 authority | Revert issue-owned paths/guard; preserve unrelated/user files |
| RUN-TRN-01 | UDS default with same-effective-UID peer credential, or explicit random loopback fallback; exact Host, empty Origin allow-list, bearer, CSRF, content-type, Fetch Metadata, no-CORS policy, and 16,384-byte body ceiling apply before parse/operation allocation | peer UID, Host/origin/CSRF/rebinding/preflight/cookie/duplicate-header/oversize/browser negatives; transport evidence | PH-C05; ADR-002/006; SC-02/08 | Disable transport/runner; no weaker loopback mode |
| RUN-TRN-02 | Browser never receives runner credentials and cannot request privileged execution directly | real HTTP browser-shaped requests prove zero operation/audit allocation; secret/output scans | ADR-002; PH-C05; SC-08 | Keep future portal static/direct-expert fallback |
| RUN-CMD-01 | Exactly eight released zero-argument lab command IDs resolve; API `learning-platform-v1`, operation `v1`, request `*-request-v1`, lab `1.0.0`, and fitness v2 are exact. No command-version field exists. Unknown schema/API/command or any raw argv/env/cwd/path/URL override fails with no implicit default/range/downgrade | registry/schema/version/unknown-field/property tests; lock/hash artifact | PH-C05; SC-02; released lab/operation contract | Dependency STOP; disable runner on mismatch |
| RUN-CMD-02 | Python/dbt entrypoints, interpreter, runtime lock, Git blob and file digest are pinned; isolated imports/startup hooks cannot alter execution | interpreter/import/sitecustomize/usercustomize/plugin/hash-swap negatives | PH-C05; PH-H02; SC-02 | Refuse readiness; restore exact reviewed runtime |
| RUN-FS-01 | Private per-run workspace, read-only base, descriptor/no-follow containment, type/link/identity checks and use-time revalidation prevent path/symlink/hardlink/TOCTOU escape | path fuzz, parent/symlink swap, hardlink, FIFO/device/socket, base-write and cleanup races | PH-C05; PH-H13; SC-02 | Quarantine owned state; disable runner; never delete foreign target |
| RUN-ENV-01 | Child env starts empty and contains only fixed policy values; no ambient credentials, home config, proxy, plugin, Docker, cloud, or trace variables | canary/env-dump/import tests and persisted-output scan | PH-C05; SC-06/11 | Kill operation; retain only typed hash/reason |
| RUN-NET-01 | The one operation worker has no outbound/listen network and can create zero descendants; runner itself exposes only UDS or explicit 127.0.0.1 ephemeral fallback | DNS/TCP/UDP/listen negatives, fork-denial inventory, containment probe | PH-C05; SC-06 | `RUNNER_CONTAINMENT_UNAVAILABLE`; static/direct mode only |
| RUN-RES-01 | Conditional 16 GiB policy enforces the released 120-second, 536,870,912-byte worker-memory and 268,435,456-byte workspace ceilings plus CPU/file/FD/output caps; `deny process-fork` requires zero descendants and parent ownership of one PID/start identity. Exact dbt currently violates the no-child precondition, so readiness is blocked | CPU spin, memory, sparse/disk, file-size, FD, output flood, all seven child-creation denials, same-worker TERM-ignore/setsid/exec-image exact reap, before/after inventory | PH-H01; PH-C05; SC-04 | Backend admission STOP or exact worker TERM→KILL→wait; no state/pointer advancement |
| RUN-FEN-01 | One per-workspace and runner-wide mutation uses OS lock + monotonic fence epoch; stale owner cannot commit | two-runner barriers, stale epoch, lock swap, crash/restart | PH-C06; SC-03/14 | Typed conflict/reconcile; prior state remains current |
| RUN-FEN-02 | Direct Make/Airflow expert namespace cannot overlap learner namespace; any learner-targeted direct callable lacks the inherited fence capability and refuses before write | runner-vs-Make non-overlap, runner-vs-callable denial, DuckDB/current-pointer oracles | PH-C06; PH-H13; SC-03 | Preserve direct expert tools; disable runner integration |
| RUN-STA-01 | Released state transitions and idempotency survive duplicate, conflicting, crash and restart paths; runner never writes portal completion | request digest replay/conflict, kill at transactions, startup reconciliation | ADR-007; PH-C06; SC-03/14/16 | Recover last commit or reset; no fabricated completion |
| RUN-AUD-01 | Audit events are insert-only, hash-chained, fsync-backed, redacted and sequence-complete | UPDATE/DELETE denial, chain tamper/truncation, crash and secret-canary tests | ADR-018; PH-H11; SC-11/16 | Quarantine corrupt log; live re-verification; no non-repudiation claim |
| RUN-REL-01 | `retail.export` stages/verifies exactly eleven assets and advances one same-filesystem current pointer atomically under a live fence | missing/duplicate/mixed asset, kill at every fsync/rename, concurrent export/reset/verify | PH-C06; SC-03/07 | Keep/restore previous pointer; quarantine incomplete stage |
| RUN-EVD-01 | Every required gate emits a closed `fitness-result-v2` envelope below `.artifacts/evidence/runner/<run-id>/`; runner detail is carried only by hashed referenced artifacts. Learner verification uses `learning-evidence-v1` | released schema/activation verifier, canonicalization/tamper/unknown-field/private-path tests | PH-H11; released Issue #8 evidence contract | Evidence failure fails gate; preserve sanitized failure artifacts |
| RUN-TDD-01 | Interpreter/import/startup-hook/argv/path-TOCTOU/env/quota/output/descendant/base-write/browser-request/cross-entrypoint-race/crash/idempotency negatives traverse real public runner Make targets and are committed RED before behavior | RED manifest lists stable assertion IDs, fixture markers, public target, and expected absence/failure against exact dependency SHAs | I5-04 TDD; PH-C05/06; SC-02/03/14 | No behavior change until exact public-path RED evidence is retained |
| RUN-GATE-01 | Exact future command set passes: `make runner-test runner-security-test runner-race-test data-contracts-check`; required S3 scans also pass | four result manifests plus aggregate evidence index | issue #9; master command registry | Any required failure blocks review/merge |
| RUN-ROL-01 | Rollback disables runner, stops only owner-recorded processes, restores previous release pointer, and removes only marker-owned transient workspace; evidence and expert paths remain | rollback rehearsal twice, foreign marker/symlink refusal, final process/status checks | PH-C05/06; SC-03/14 | Manual inspection on ownership ambiguity; never broad clean |
| RUN-APP-01 | Exact independently reviewed head receives human pre-merge approval; changed head invalidates approval | issue/PR attestation, remote head equality, zero Critical/High | issue #9 mandatory gate | No merge until re-review/re-attestation |

## Threat Model

### Actors and trust levels

| Actor | Trust | Allowed | Explicitly denied / out of claim |
|---|---|---|---|
| Browser JavaScript / malicious site | Untrusted | Call future portal only | Runner token, socket/port discovery, runner CORS, privileged mutation |
| Future portal BFF | Authenticated local caller | Released operations over private transport | Raw argv/env/path, shared-contract mutation, completion forgery |
| Local learner | Untrusted inputs, same product actor | Released typed values and workspace-scoped results | Host/repository paths, package install, arbitrary binary/shell/network/cloud |
| Allow-listed child process | Contained | Read pinned base/runtime; write declared workspace set | Runtime secrets, home/credentials, base writes, network, other workspace |
| Direct expert Make/Airflow user | Trusted expert namespace | Existing repository-local direct workflow | Learner namespace mutation without inherited fence capability |
| Runner daemon | Application-level local authority; OS process remains unprivileged | Workspace state, audit, process and release commits | Sudo/elevation, portal completion, shared contract writes, cloud/AWS/Terraform |
| Same-account external process/root | Outside cryptographic assurance | None granted by product | Local non-repudiation/isolation claim; root can defeat host controls |

### Protected assets and boundaries

- Immutable Git base/entrypoint bytes and Issue #6/#8 contract identities.
- User home, credentials, agents, private URLs, host processes, and repository files.
- Workspace owner identity, state/idempotency projection, append-only audit chain, current release,
  retained evidence, and resource availability.
- Boundaries: browser→future portal; BFF→runner transport; runner→contained child;
  read-only base→mutable workspace; runner namespace→expert namespace; active fence→commit.

## Threat and Abuse-Case Matrix

| Threat ID | Attack / failure | Prevention | Required negative and safe result | Residual |
|---|---|---|---|---|
| THR-RCE-01 | Unknown command, metacharacters, flag smuggling, malicious selector | Released typed registry; fixed argv; `shell=False` | argv spy sees exact list or zero process; typed denial | Compromised reviewed entrypoint is a supply-chain issue caught by hash/review |
| THR-IMP-01 | Workspace module shadows dependency; startup/site/dbt plugin hook executes | Python `-I`, empty env, private HOME, pinned venv/entry points | canary hook/import never executes; expected module origin recorded | Approved dependency plugins remain trusted pinned code |
| THR-PTH-01 | Traversal, Unicode/alternate separator, symlink/hardlink/special file escape | component grammar, directory FDs, no-follow, type/link/identity checks | no outside read/write/delete; typed path failure | Host kernel/filesystem defect outside claim |
| THR-TOC-01 | Parent/output/pointer swapped after validation | retained FDs, same-filesystem atomic replace, use-time identity, Seatbelt write set | safe original inode or typed failure; attacker target unchanged | Hostile root can replace kernel-visible state |
| THR-ENV-01 | AWS/token/proxy/PYTHONPATH/home config leaks or changes behavior | env from empty map; child cannot read service secret/home | canary absent from child/evidence; persistence fails on match | Same-account process outside child sandbox remains out of claim |
| THR-NET-01 | Child exfiltrates or starts listener | Seatbelt default network deny; no proxy/env | TCP/UDP/DNS/listen fail; no network artifact | Runner loopback/UDS transport itself is intended local IPC |
| THR-BRW-01 | CSRF, DNS rebinding, CORS, forged Host/Origin, browser direct request | UDS, exact Host, reject Origin/cookies/preflight, bearer + CSRF | every browser-shaped mutation rejected before allocation | Future BFF compromise handled by later portal issue |
| THR-RES-01 | CPU/memory/disk/FD/output bomb; fork/spawn/setsid escape attempt | conditional `deny process-fork` + exact single-worker rlimits/measurement + PID/start identity + TERM/KILL/wait | every child attempt denied before first marker; same-process setsid worker reaped; zero survivors; pointer unchanged | Exact dbt is incompatible and keeps the runner disabled; generic process-exec denial cannot launch Python |
| THR-RAC-01 | reset/export/verify or two runners commit mixed state | OS lock, monotonic fence, transactional CAS | one commit or typed conflict; old/new complete state only | Filesystem/SQLite corruption requires quarantine/manual recovery |
| THR-XEP-01 | Make/Airflow writes learner paths during runner operation | disjoint expert namespace; learner fence requires inherited descriptor | expert path may proceed independently; learner-targeted direct call refuses | Expert with same UID can intentionally bypass outside product API; not a browser capability |
| THR-CRS-01 | Crash between audit/state/blob/manifest/pointer boundaries | transaction/fsync/atomic replace; startup reconciliation | last committed state visible; incomplete owned state quarantined | Crash may leave bounded owned state for manual cleanup |
| THR-IDM-01 | Duplicate/replayed key runs twice or changed body reuses key | unique key + canonical request digest + committed result reuse | same returns same result; changed body conflicts | Key secrecy is not relied on for authorization |
| THR-AUD-01 | Audit row edit/delete/truncation or secret persistence | insert-only triggers, hash chain, canonical allow-list, scan | mutation denied/tamper detected; no secret bytes retained | Same-account owner can alter code/database and recompute; no non-repudiation claim |
| THR-REL-01 | Mixed/missing eleven assets become current | staged exact set, manifest validation, live fence, atomic pointer | prior pointer remains on every injected partial failure | Downstream remote catalog publication is Issue #7, out of scope |
| THR-SUP-01 | Runtime/entrypoint/contract replaced between plan and use | exact SHA/blob/hash/lock and clean-source checks | readiness false before execution | OS update intentionally requires re-attestation |

## Risk Register

| Risk | Likelihood / impact | Mitigation and release gate | Owner / evidence |
|---|---|---|---|
| Stage A generic seam is mis-pinned or locally forked | Low / Critical | Pin release/tree/hashes; use generic activation plus fitness v2 read-only; no shared write | Phase 2 release table + contract lock |
| I5-04 activation bytes drift from their exact owned path | Low / Critical | Allow only `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`; measure and lock actual base/fragment/instance hashes | Activation/lock evidence |
| Oversized or ambiguous private request reaches allocation | Low / High | Exact 16,384-byte pre-parse ceiling plus duplicate/framing/streaming negatives | Transport RED evidence |
| `sandbox-exec` is unavailable or behavior changes on a macOS update | Medium / Critical | Exact tested host tuple + functional startup probes; runner stays disabled | S3 containment evidence |
| Existing CLI performs undeclared write despite explicit path args | Medium / High | Phase 1 syscall/path characterization; do not broaden write set; re-plan narrow seam if proven | characterization manifest |
| Exact released operation requires child creation under fork-denied worker | Observed / Critical | Keep cook blocked; require released fixed in-process backend, separately proven lifetime primitive, or owner-approved upstream contract rerelease | 7/7 child denials + 7/8 operation feasibility + exact dbt `EPERM` evidence |
| Same-UID expert intentionally tampers with local state | Medium / High | Honest local threat statement, hash detection, fresh live verification, later hosted authority | audit/evidence residual statement |
| SQLite/filesystem crash leaves ambiguous partial state | Low / High | FULL sync, transactions, fsync/rename, fence epochs, quarantine and repeated recovery | crash matrix |
| Evidence leaks a token/private path through output | Medium / Critical | secret absent from child, structured allow-list, fail-on-detection scan, bounded previews | S3 scan + canary report |
| Quotas harm 16 GiB laptop or are too small for dbt | Medium / High | one global mutation, explicit caps, RED/real bounded run; any later policy revision requires owner decision and fresh validation | resource manifest |
| Plan drifts into portal/framework or shared contracts | Low / High | changed-path allow-list and protected-path hash gate | boundary manifest |
| Human approval is applied to a changed head | Low / Critical | bind approval to exact remote PR head; changes require fresh independent review/attestation | issue/PR comment |

## STOP Conditions

- Wrong/dirty input, active overlapping shared-contract lease, or changed protected path.
- Stage A SHA/tree/ancestry or any pinned contract/registry/operation/evidence hash mismatches.
- I5-04 activation is absent from its exact owned path, any measured registry/fragment/instance
  hash mismatches, the 16,384-byte request ceiling is not active, or the implementation head does
  not descend from the release.
- Required host containment, filesystem no-follow/atomicity, all-eight in-process adapter closure,
  zero-descendant prevention, exact single-worker reap, or exact runtime lock cannot be proven.
- Any required RED assertion is missing, passes before behavior for the wrong reason, or lacks a
  stable ID and exact SHA.
- Any path escape, base write, credential/network leak, descendant leak, mixed release, stale-fence
  commit, fabricated completion, required gate failure, or unresolved Critical/High finding.
- Any request for sudo, container privilege, Terraform/AWS/cloud action, destructive host cleanup,
  shared-contract write, portal/framework change, PR/merge without exact-head human approval.

## Unresolved Questions

One owner/platform question blocks readiness: which separately reviewed backend preserves
`retail.dbt-build` without child/exec/private-startup manipulation, or whether the upstream
released command contract will be deliberately rereleased. Stage A identity, activation path,
private request ceiling, and write ownership otherwise remain exact.
