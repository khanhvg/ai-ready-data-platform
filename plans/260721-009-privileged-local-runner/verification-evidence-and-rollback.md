# Issue #9 Verification, Evidence, and Rollback

> Current readiness is `BLOCKED`; see [capability-amendment.md](./capability-amendment.md). The
> exact future commands and 44 RED / 9 S3 IDs remain unchanged, but the descendant oracles below
> require prevention before first child and exact single-worker reap. They cannot run as product
> RED until all eight released operations have an admitted in-process backend.

## TDD Order

1. Record exact implementation input, Issue #6 release, Stage A release
   `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, release tree, contract versions/hashes, tested host
   tuple, and protected-path hashes.
2. Commit Phase 1 characterization and test fixtures before behavior.
3. Invoke all Phase 3 security/race/crash/idempotency assertions through the real public
   `make runner-test`, `make runner-security-test`, or `make runner-race-test` path and commit the
   test-only RED tree/evidence before runner behavior. A valid RED reaches its intended fixture
   marker and missing/refusing behavior; a helper-only invocation or missing tool, fixture,
   command, contract, setup, skip, or early failure cannot count.
4. Implement the smallest Phase 4/5 behavior to turn each class GREEN. Do not weaken expectations,
   mark required tests optional, or use a fake local Issue #8 contract.
5. Run Phase 6 focused gates, then the exact aggregate gate and S3 scans. Preserve failures.

## RED Assertion Families

| Family | Stable ID prefix | Minimum cases |
|---|---|---|
| Interpreter/entrypoint | `RED-INT-*` | unapproved binary/interpreter, wrong blob/hash, runtime-lock drift |
| Import/startup hook | `RED-IMP-*` | workspace shadow module, `PYTHONPATH`, `PYTHONSTARTUP`, `sitecustomize`, `usercustomize`, dbt plugin/config hook |
| Argv/type registry | `RED-ARGV-*` | shell metacharacters, unknown option/field/command, selector/env/cwd/path/URL override, Terraform-like flags |
| Path/TOCTOU | `RED-PATH-*` | absolute/parent/NUL/alternate separator, component/child/pointer swap, hardlink, FIFO/device/socket, parent rename, temp replace |
| Environment/network | `RED-ENV-*`, `RED-NET-*` | AWS/token/proxy/SSH/Docker/home canaries, env dump, TCP/UDP/DNS/listen |
| Quotas/output/descendants | `RED-QUOTA-*`, `RED-OUT-*`, `RED-DESC-*` | CPU, RSS, logical/allocated disk, sparse/large file, FD/process count, stdout/stderr/binary/canary flood, TERM-ignore/grandchild/setsid |
| Base immutability | `RED-BASE-*` | create/modify/rename/chmod/delete/hardlink/symlink against Git base and protected files |
| Browser transport | `RED-BROWSER-*` | forged/missing/duplicate Host/auth/CSRF, Origin, cookie, Fetch Metadata, CORS preflight, simple form, DNS rebinding, stable-port assumption |
| Cross-entrypoint race | `RED-XRACE-*` | runner-vs-runner, reset/export/verify, runner-vs-Make expert non-overlap, learner-targeted Airflow/direct denial, stale fence |
| Crash/idempotency/release | `RED-CRASH-*`, `RED-IDEMP-*`, `RED-REL-*` | kill at transaction/fsync/rename/ack boundaries, same/different request replay, eleven-asset partial/mixed/duplicate/missing |

## Stable RED Assertion Catalog

These IDs are fixed by the independently validated plan and must appear unchanged in the future
machine-readable RED manifest. They name app-test assertions, not Issue #8 wire problem codes. The
exact released typed problem/status for each denial is bound in Phase 2; absence of a compatible
mapping blocks cook. Every row must first fail after its fixture/precondition marker is reached and
before the owning runner behavior exists. A missing tool, unsupported host, absent dependency,
fixture/setup failure, skip, xfail, or failure before the named marker is not valid RED evidence.

| Stable ID | Fixture or barrier | Exact pre-behavior RED oracle |
|---|---|---|
| `RED-INT-001` | Unapproved interpreter/binary | Descriptor resolution refuses before spawn; argv probe records zero child |
| `RED-INT-002` | Entrypoint byte/blob swap | Hash/blob preflight refuses before workspace mutation or spawn |
| `RED-INT-003` | Runtime-lock/interpreter-version drift | Service remains not-ready and allocates no operation/workspace |
| `RED-IMP-001` | Workspace shadow module and `PYTHONPATH` canary | Canary is never imported; module origin is the pinned runtime or execution refuses |
| `RED-IMP-002` | `PYTHONSTARTUP`, `sitecustomize`, `usercustomize` canaries | No startup canary executes or reaches output/evidence |
| `RED-IMP-003` | Unapproved dbt plugin/profile/package hook | Hook is absent from the admitted entry-point set and execution refuses before dbt starts |
| `RED-ARGV-001` | Unknown command/field/version/argument | Strict released decoding refuses before descriptor lookup or process allocation |
| `RED-ARGV-002` | Metacharacter, flag smuggling, selector or Terraform-like option | Argv probe sees zero child or the one exact fixed list; injected token never appears |
| `RED-ARGV-003` | Environment/CWD/path/URL/executable override | Strict decoding refuses; no caller value reaches descriptor, env, CWD, or child |
| `RED-PATH-001` | Absolute, parent, NUL, Unicode/alternate-separator input | Path admission refuses before filesystem mutation |
| `RED-PATH-002` | Symlink, hardlink, FIFO/device/socket destination | Descriptor/type/link identity refuses; outside inode is unchanged |
| `RED-PATH-003` | Parent/child/output/pointer/temp swap barrier | Use-time identity selects the retained safe inode or returns typed failure; attacker inode is unchanged |
| `RED-PATH-004` | Foreign marker, mount/device change, ambiguous cleanup root | Reset/rollback refuses cleanup and preserves the complete tree for inspection |
| `RED-ENV-001` | AWS/cloud/token/password/key/proxy/SSH/Docker/tracing canaries | Child env contains none of the canary names/values and evidence scan finds none |
| `RED-ENV-002` | Writable HOME/config/cache/startup path and env dump | Writes stay in generated private roles; raw env/home/private path is not persisted |
| `RED-NET-001` | DNS, TCP and UDP outbound probes | Every network operation fails inside containment and produces no external side effect |
| `RED-NET-002` | TCP/UDP listener probe | Child cannot bind/listen; runner exposes only its admitted private listener |
| `RED-QUOTA-001` | Wall/CPU spin | Deadline or worker CPU bound terminates and reaps the exact PID/start worker; state/pointer does not advance |
| `RED-QUOTA-002` | RSS allocator | Worker RSS bound terminates and reaps the exact PID/start worker with bounded evidence |
| `RED-QUOTA-003` | Logical/allocated disk, sparse/large file and FD fan-out | First exact bound breach fails the operation; outside/base state and current pointer are unchanged |
| `RED-OUT-001` | stdout/stderr flood | Crossing either 2 MiB stream cap terminates the operation; retained preview is at most 128 KiB per stream |
| `RED-OUT-002` | Binary, secret and private-path output canaries | Publication refuses raw content; only permitted digest/count/typed reason can remain |
| `RED-DESC-001` | `fork`, `posix_spawn`, subprocess, multiprocessing fork/spawn/forkserver and TERM-ignore child attempts | Each attempt is denied before the first child marker; exact worker PID/start cleanup and final inventory find zero survivors |
| `RED-DESC-002` | Rapid double-fork/reparent/`setsid` attempt plus separate same-process `setsid` worker | First fork is denied before any child marker; TERM-ignoring same-process `setsid` worker retains identity, is KILLed and waited, and leaves zero survivors |
| `RED-BASE-001` | Create/modify/chmod/delete/rename against Git base | Containment denies every mutation and protected hashes remain exact |
| `RED-BASE-002` | Hardlink/symlink from workspace to base/protected file | Link operation/use refuses and both source and target identities/hashes remain exact |
| `RED-BROWSER-001` | Forged/missing/duplicate Host and DNS-rebinding host | Request is rejected before body read and operation/audit allocation |
| `RED-BROWSER-002` | Origin, cookie, browser Fetch Metadata, CORS preflight/simple form | Request is rejected; no permissive CORS response and no operation/audit allocation |
| `RED-BROWSER-003` | Missing/duplicate/wrong bearer or mutation CSRF | Request is rejected before typed body allocation; credentials are never echoed |
| `RED-BROWSER-004` | Prior-launch token, chunked/ambiguous length, invalid/oversized body | Exact listener/session/framing admission rejects before operation/audit allocation |
| `RED-XRACE-001` | Two runner mutations at the same barrier | One live fence may commit; the other conflicts/reconciles and stale state cannot advance |
| `RED-XRACE-002` | Reset/export/verify pair barriers | Operations serialize or conflict; database/generation/current pointer is old-or-new complete |
| `RED-XRACE-003` | Expert default Make during learner mutation | Expert repository namespace and learner private namespace remain disjoint with no mixed artifact |
| `RED-XRACE-004` | Learner-targeted Airflow/direct callable | Guard refuses before `_run`, import, child, or write without inherited fence capability |
| `RED-XRACE-005` | Stale lock identity/fence epoch owner | Compare-and-commit refuses every stale state/audit/evidence/pointer write |
| `RED-CRASH-001` | Kill before/after SQLite state and audit commit | Restart exposes only the last committed transition and complete audit prefix |
| `RED-CRASH-002` | Kill around asset/manifest write and fsync | Incomplete marker-owned stage is non-current and quarantinable; prior release remains current |
| `RED-CRASH-003` | Kill before/after pointer rename and parent fsync | Reader observes only prior or new verified complete pointer, never partial/mixed state |
| `RED-CRASH-004` | Kill after result commit and before response acknowledgment | Replay returns the committed result and reconciliation creates no duplicate execution |
| `RED-IDEMP-001` | Same key + same canonical request before/after restart | Original operation/result identity is returned; no second child or release |
| `RED-IDEMP-002` | Same key + different canonical request | Typed conflict occurs before child/state/release mutation |
| `RED-IDEMP-003` | Duplicate in-flight request across restart/reconcile | One execution owns the fence; replay resolves to committed or typed recoverable state |
| `RED-REL-001` | Missing/duplicate/reordered/mixed/wrong-generation asset set | Manifest/current-pointer validation refuses; prior pointer remains exact |
| `RED-REL-002` | Same release replay and concurrent pointer reader | Replay is idempotent and every reader resolves one complete eleven-asset manifest |

## Exact Future Commands

Run from the issue implementation root and record each exact command, exit code, duration,
toolchain, input/output/tested-tree SHAs, and evidence locator:

```bash
make runner-test
make runner-security-test
make runner-race-test
make data-contracts-check
```

`mk/issue-5/i5-04.mk` owns only the first three recipes. The fourth remains the shipped I5-01
target. All are required and non-interactive; missing tools or dependencies are `fail`, never
`not-run-optional`.

### Gate contents

- `runner-test`: released-contract pin/direct-reader/activation check, registry/unit/state/idempotency,
  existing seam characterization, one bounded real `small`/`42`
  prepare→generate→load→dbt→export→verify→reset integration through eight reviewed in-process
  adapters, and final zero-descendant/no-base-diff. This gate is blocked by current dbt.
- `runner-security-test`: all interpreter/import/startup/argv/path/env/network/quota/output/
  descendant/base/browser negatives; containment probe; secret/private-path evidence scan;
  dependency and static S3 scans.
- `runner-race-test`: deterministic barrier tests for runner/runner, reset/export/verify,
  Make/Airflow expert separation, stale fence, crash/restart/reconciliation, idempotency and all
  eleven-asset pointer boundaries.
- `data-contracts-check`: unchanged I5-01 18-table/51-model/11-mart/shared-contract regression.

## S3 Static and Dependency Scans

The app lock must pin the scanner versions and hashes. `runner-security-test` invokes them from the
private test environment and records full commands/versions/results:

```bash
python -m compileall -q apps/lab-runner/src apps/lab-runner/tests
python -m bandit -q -r apps/lab-runner/src
python -m pip_audit --disable-pip --no-deps -r apps/lab-runner/requirements/runner-py312-macos-arm64.lock
```

Also run app-owned deterministic AST/policy checks that fail on `shell=True`, `os.system`,
`eval`/`exec`, unapproved `subprocess`/`socket` call sites, wildcard CORS, cookie auth, raw
environment merge, broad delete/glob cleanup, non-constant entrypoint resolution, missing
`-I`, or an unowned Make recipe. Run changed/protected-path, Git credential/private-key/token,
absolute home/private URL, runtime secret-canary, evidence unknown-field, and no-Terraform/no-cloud
command scans. Online scanning is not required during child execution; runtime children remain
network-denied.

Any scanner suppression requires a code-adjacent rationale, issue-specific independent review,
and evidence that it narrows a false positive without weakening a test. No blanket skip/exclude.

### Required S3 scan matrix

Every row is required inside `runner-security-test`. The future evidence locator is exact relative
to `.artifacts/evidence/runner/<run-id>/`; missing tools, inputs, result files, or hashes fail the
gate. Bandit and pip-audit are intentionally absent from the current global shell and must come
only from the future hash-complete app lock.

| Scan ID | Exact command or owned check | Failure rule | Evidence locator |
|---|---|---|---|
| `S3-SYN-001` | `python -m compileall -q apps/lab-runner/src apps/lab-runner/tests` | Any syntax/import compilation failure or missing tree | `artifacts/s3-scan/S3-SYN-001.json` |
| `S3-CODE-001` | `python -m bandit -q -r apps/lab-runner/src` | Any unsuppressed finding or unpinned/missing Bandit | `artifacts/s3-scan/S3-CODE-001.json` |
| `S3-DEP-001` | `python -m pip_audit --disable-pip --no-deps -r apps/lab-runner/requirements/runner-py312-macos-arm64.lock` | Any advisory, lock mismatch, dependency resolution attempt, or missing pinned tool | `artifacts/s3-scan/S3-DEP-001.json` |
| `S3-POL-001` | App-owned deterministic AST/policy checker over exact runner source | Any forbidden shell/eval/exec/subprocess/socket/CORS/env/delete/entrypoint/import policy | `artifacts/s3-scan/S3-POL-001.json` |
| `S3-SRC-001` | Git changed-path allow-list plus protected blob/hash comparison | Any unowned/shared/root/portal/cloud path or protected byte drift | `artifacts/s3-scan/S3-SRC-001.json` |
| `S3-SEC-001` | Credential/private-key/token/private-path/URL and runtime-canary byte scan | Any raw secret, credential name/value, absolute private path/URL, raw env or customer row | `artifacts/s3-scan/S3-SEC-001.json` |
| `S3-EVD-001` | Released schema/canonicalization plus artifact size/SHA-256 closure check | Unknown/duplicate/invalid field, missing artifact, hash/size mismatch, or recursive commit claim | `artifacts/s3-scan/S3-EVD-001.json` |
| `S3-CLOUD-001` | No-Terraform/no-cloud/no-container/no-sudo command and import policy scan | Any runtime path to Terraform, AWS/GCP/Azure, Docker/Compose, package install or privilege | `artifacts/s3-scan/S3-CLOUD-001.json` |
| `S3-RUN-001` | Containment, process-leak, base-write, browser and cross-entrypoint negative summary | Any skipped assertion, surviving listener/child, base write, browser allocation or mixed namespace | `artifacts/s3-scan/S3-RUN-001.json` |

## Evidence Layout and Manifest

Each public gate generates a collision-resistant run ID and writes only below:

```text
.artifacts/evidence/runner/<run-id>/
  manifest.json
  gates/<command-id>/result.json
  artifacts/{junit,red-manifest,s3-scan,resource,single-worker-process,transport,race,crash,release,rollback}/**
```

The released evidence contracts are authoritative and compatible without a shared write:

- Each public runner gate emits a closed `fitness-result-v2` envelope with owner `I5-04`, an exact
  activated command ID, requested subject/parameters, pass/fail code/remediation, `inputSha`,
  `testedTreeSha`, Stage A/Issue #6 `dependencyMergeShas`, sorted contract/fixture/schema hashes,
  toolchain, lock hash, exact public argv, canonical role-based child argv, actual-child-argv digest,
  timestamps/duration, artifact locators, redaction/retention, rollback, RFC 8785 and payload hash.
- The I5-04 activation instance at
  `apps/lab-runner/config/command-owner-activation-i5-04-v1.json` must validate against
  `command-owner-activation-v1`, bind base registry SHA-256
  `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80`, owner `I5-04`, the exact
  measured fragment hash, only the three reserved commands, and `fitness-result-v2`. Its own hash
  is measured from actual bytes and included in the lock/evidence.
- The envelope's `durationMs` is at most `120000`; each referenced artifact is at most
  `10485760` bytes. A gate that exceeds the released bounds fails rather than widening the schema.
- Runner-specific assertion IDs, process/resource summaries, release/current-pointer digests,
  S3 results, cleanup details and residual risks live in bounded hashed artifacts such as
  `gates/<command-id>/result.json`; they are not invented top-level fitness fields.
- A verified learning run additionally emits `learning-evidence-v1` with exact lesson/lab/actor/
  workspace/run/operation/provenance/transitions/commands/assertions/artifacts/timing/integrity
  fields and the released 120-second timing boundary.

Canonicalization follows the released contract. Unknown security-sensitive fields, duplicate JSON
names, non-finite values, invalid UTF-8, absolute host paths, private URLs, credentials, raw env,
raw customer/order rows, and unbounded output fail publication. Store a digest and typed reason,
not the rejected secret/content.

The raw executed child argv is never persisted because it contains absolute private runtime and
workspace paths. `fitness-result-v2` provides `canonicalChildArgv` plus
`actualChildArgvSha256`, so this requirement is satisfied without a local extension.

The immutable base registry retains logical identifiers `runner-test`, `runner-security`, and
`runner-race`. The verifier accepts an explicit artifact root, so physical evidence remains below
the Issue #9-owned `runner/<run-id>/` and uses relative locators; no shared registry edit is needed.

## Evidence Acceptance

- A passing manifest validates against the exact released Issue #8 schema and all referenced
  artifacts exist with matching hashes/sizes.
- The tested tree is clean except allow-listed untracked `.artifacts/`; protected hashes and
  absent/present state match preflight.
- RED manifest proves every required family ran through a real public Make target before
  implementation, at an exact retained RED commit, and reports no skip.
- S3 scans, no-network/base-write/browser/cross-entrypoint/process-leak tests all pass.
- Release evidence proves an old complete pointer or new complete eleven-asset pointer at every
  injected failure; never a mixed/partial current release.
- Rollback rehearsal passes twice and does not delete evidence or expert/unrelated state.
- The full gate is reproduced from a fresh clean checkout at the exact candidate head with no
  borrowed `.venv`, ignored fixture, generated runtime state, or historical worktree artifact.

## Rollback Procedure

Rollback is a future implementation/review operation, not authorization in this plan:

1. Refuse new operations and verify the service owner marker, launch ID, exact worker PID/start
   identity, contract lock, workspace owner nonce and fence epoch.
2. Apply bounded TERM→KILL→wait only to the recorded exact worker. Verify no descendant/socket
   remains. Never use broad `pkill`, recursive workspace-root deletion, `make clean`, sudo, or
   container cleanup.
3. Disable/remove only `mk/issue-5/i5-04.mk` and app-owned startup integration in the reviewed
   rollback change. Existing direct expert Make/Airflow commands remain unchanged.
4. For each workspace, keep immutable evidence/audit. If current release is invalid or belongs to
   the rolled-back generation, atomically restore only a previously validated complete pointer
   under a fresh live fence and fsync the parent.
5. Remove/quarantine only transient directories whose descriptor identity, marker schema, owner
   nonce, device/inode, workspace/generation ID and purpose all match. Refuse foreign, linked,
   special, mount-changed, ambiguous, or evidence-referenced state for manual inspection.
6. Re-run `make data-contracts-check`, protected-path/secret scans, Git cleanliness, pointer
   validation, evidence retention and direct expert-path characterization.

## Pre-Merge Handoff Gate

- The release amendment has passed fresh strict validation and dependency-aware readiness audit;
  any later plan-byte change requires both gates again.
- Implementation RED/GREEN evidence and all exact commands pass on a clean exact tested tree.
- Two fresh independent reviews in separate contexts/checkouts—correctness/contracts/TDD/recovery
  and S3/containment/race/evidence/rollback—each report zero unresolved Critical/High findings at
  the same exact remote head.
- Remote PR head equals both reviewed heads; available checks/mergeability are green.
- A human explicitly approves that exact head. Any subsequent change requires fresh review and
  re-attestation before merge.
- No AWS/cloud/Terraform, container privilege, sudo, destructive host action, shared-contract
  mutation, portal/framework change, PR creation, or merge is implied by this plan.

## Unresolved Questions

One owner/platform backend decision blocks readiness, as recorded by the capability amendment.
The activation path and 16,384-byte private request ceiling are otherwise exact; future
content/head hashes are measured only after the bytes exist. No generated binding or
shared-contract change is authorized, and no current gate may claim all-eight execution.
