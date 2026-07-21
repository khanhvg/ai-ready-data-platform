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
- exact command/argv, UTC start/finish/duration, tool/runtime/OS/architecture/memory versions;
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
