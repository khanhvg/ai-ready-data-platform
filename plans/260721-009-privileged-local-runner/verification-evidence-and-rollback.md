# Issue #9 Verification, Evidence, and Rollback

## TDD Order

1. Record exact implementation input, Issue #6 release, Issue #8 released Stage A SHA, contract
   versions/hashes, tested host tuple, and protected-path hashes.
2. Commit Phase 1 characterization and test fixtures before behavior.
3. Commit all Phase 3 security/race/crash/idempotency assertions RED with stable IDs. A test is
   valid RED only when it reaches the intended missing/refusing behavior and cannot pass because a
   tool, fixture, command, contract, or setup silently skipped.
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
| `RED-QUOTA-001` | Wall/CPU spin | Deadline or aggregate CPU bound terminates and reaps the owned tree; state/pointer does not advance |
| `RED-QUOTA-002` | RSS allocator | Aggregate RSS bound terminates and reaps the owned tree with bounded evidence |
| `RED-QUOTA-003` | Logical/allocated disk, sparse/large file, FD/process fan-out | First exact bound breach fails the operation; outside/base state and current pointer are unchanged |
| `RED-OUT-001` | stdout/stderr flood | Crossing either 2 MiB stream cap terminates the operation; retained preview is at most 128 KiB per stream |
| `RED-OUT-002` | Binary, secret and private-path output canaries | Publication refuses raw content; only permitted digest/count/typed reason can remain |
| `RED-DESC-001` | TERM-ignore grandchild | TERM then KILL reaps every admitted descendant; postcheck finds none |
| `RED-DESC-002` | Rapid double-fork/reparent plus `setsid` barrier | Phase 1-admitted mechanism accounts for and reaps it without a lucky poll; otherwise readiness fails |
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

- `runner-test`: released-contract pin/type generation check, registry/unit/state/idempotency,
  existing seam characterization, one bounded real `small`/`42`
  prepare→generate→load→dbt→export→verify→reset integration, and final no-child/no-base-diff.
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
  artifacts/{junit,red-manifest,s3-scan,resource,process-tree,transport,race,crash,release,rollback}/**
```

The Issue #8 released evidence schema is authoritative. Phase 2 must prove it supports I5-04 and
the issue body; otherwise STOP. At minimum the manifest must carry:

- `schemaVersion: fitness-result-v1`, command ID, owner, status/failure code/remediation;
- exact public gate command; canonical child argv expressed only with released typed values,
  repository-relative entrypoint/runtime IDs and workspace-role locators; digest of the actual
  executed argv; UTC start/finish/duration; tool/runtime/OS/architecture/memory versions;
- immutable issue input, Issue #6 release, Issue #8 Stage A release, tested-tree/output and future
  attestation/merge identities without recursive containing-commit claim;
- contract/schema/registry/entrypoint/runtime-lock/fixture/config hashes;
- generated run/workspace/operation/release IDs and sanitized parameters;
- assertion IDs/results, process/resource quota summary, current/previous release digests;
- artifacts with repository-relative or evidence-root-relative locator, media type, size, SHA-256;
- redaction/retention class, secret/private-path scan result, rollback result, and residual risks.

Canonicalization follows the released contract. Unknown security-sensitive fields, duplicate JSON
names, non-finite values, invalid UTF-8, absolute host paths, private URLs, credentials, raw env,
raw customer/order rows, and unbounded output fail publication. Store a digest and typed reason,
not the rejected secret/content.

The raw executed child argv is never persisted because it contains absolute private runtime and
workspace paths. Phase 2 must prove the released evidence contract can carry the canonical argv,
role locators and actual-argv digest above without a local extension; otherwise the dependency is
incompatible and cook remains blocked.

Logical command-owner `evidenceRoot` values may remain registry identifiers, but the physical
canonical root is the issue-authorized `runner/<run-id>/`; Phase 2 must confirm the released
mapping rather than editing the shared registry locally.

## Evidence Acceptance

- A passing manifest validates against the exact released Issue #8 schema and all referenced
  artifacts exist with matching hashes/sizes.
- The tested tree is clean except allow-listed untracked `.artifacts/`; protected hashes and
  absent/present state match preflight.
- RED manifest proves every required family ran before implementation and reports no skip.
- S3 scans, no-network/base-write/browser/cross-entrypoint/process-leak tests all pass.
- Release evidence proves an old complete pointer or new complete eleven-asset pointer at every
  injected failure; never a mixed/partial current release.
- Rollback rehearsal passes twice and does not delete evidence or expert/unrelated state.

## Rollback Procedure

Rollback is a future implementation/review operation, not authorization in this plan:

1. Refuse new operations and verify the service owner marker, launch ID, PID/start time, process
   group/tree, contract lock, workspace owner nonce and fence epoch.
2. TERM/KILL/reap only the recorded runner-owned process tree. Verify no owned descendant/socket
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

- Fresh independent plan validation and readiness audit completed after this planner artifact.
- Readiness stays `BLOCKED_FOR_COOK` until exact Issue #8 Stage A release is merged and pinned.
- Implementation RED/GREEN evidence and all exact commands pass on a clean exact tested tree.
- Fresh independent code/security review reports zero unresolved Critical/High findings.
- Remote PR head equals reviewed head; available checks/mergeability are green.
- A human explicitly approves that exact head. Any subsequent change requires fresh review and
  re-attestation before merge.
- No AWS/cloud/Terraform, container privilege, sudo, destructive host action, shared-contract
  mutation, portal/framework change, PR creation, or merge is implied by this plan.

## Unresolved Questions

None. Issue #8 release data is an explicit implementation dependency and may not be guessed.
