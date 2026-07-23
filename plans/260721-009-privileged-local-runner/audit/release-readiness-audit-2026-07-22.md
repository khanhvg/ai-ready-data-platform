---
type: dependency-aware-readiness-audit
issue: 9
date: "2026-07-22"
status: ready
verdict: READY_TO_COOK
auditInputSha: "5cea5ce248b49ff8741af1b1e65f8ac2eb64698f"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
cookScope: whole-plan
dependencyBinding: PASS
ownership: PASS
s3: PASS
cloudAction: none
---

# Fresh Dependency-Aware Readiness Audit — Issue #9

## Verdict

`READY_TO_COOK`; `COOK_SCOPE=whole-plan`.

The exact Issue #8 Stage A release resolves the historical external blocker, and its generic
activation/version/evidence seam supports I5-04 without a shared-contract write. The two remaining
runner-local policy questions are now exact and compatible: one Issue #9-owned activation path and
a 16,384-byte private request limit. No useful dependency-safe staged subset is needed; the entire
six-phase plan is ready only in its documented order.

This verdict authorizes planning handoff to cook, not implementation in this audit. No runner,
source/config/data, shared contract, runtime artifact, PR/merge, credential, AWS/Terraform,
container, or cloud action was performed.

## Dependency Binding

Fresh remote and Git-object proof established:

- current `integration/issue-5-local-learning` and released Stage A are exactly
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` with tree
  `27fc3667ef37892dad5c3fbfd76769f65a0760be`;
- PR #23 merge `5c2244c2c860234d0df49cf0a42ad950c6495717` is the ordered first parent and an ancestor;
- the Issue #7 Make-fragment composition fix is shipped at the same integration SHA;
- release evidence records Stage A `56/56`, invalid fixtures `65/65`, operation matrix `16`, final
  `4/4`, inherited `19/19 + 1/1 + 13/13`, zero owned leaks, and no cloud action.

The exact contract set closes 21/21. The plan's 38 unique required read-only interface hashes all
recompute from the release object. Version/operation/command/completion/state/OpenAPI/evidence
semantics are compatible. Stage A deliberately exposes no generated-binding procedure; direct
read-only consumption is the pinned procedure.

`DEPENDENCY_BINDING=pass`.

## Lease and Ownership

Issue #8 Stage B's latest plan-only attempt ended blocked with `OUTPUT_SHA=none` and no amended
path. Issue #9 has no write to Issue #8's shared-contract surface. Read-only consumption of the
released Stage A bytes is not a conflict.

Authorized future writes are exactly 66 named create paths under the runner ownership (including
`apps/lab-runner/config/command-owner-activation-i5-04-v1.json`), `mk/issue-5/i5-04.mk`, and one
existing Airflow callable seam limited to a pre-`_run` learner-reserved-path refusal if Phase 1
still proves it necessary. All 66 creates are absent at release; the one modify seam and all 50
read-only inputs exist. Root Make, portal, shared contracts, golden core, data semantics,
cloud/Terraform, containers, and every other existing path remain denied.

Any later real overlapping write lease blocks. The current lease disposition is no overlap.

`OWNERSHIP=pass`.

## Security and TDD Readiness

The amended plan preserves all required gates:

- owner-only UDS with same-effective-UID peer checks, or explicit random-loopback fallback;
- exact private Host, rejected Origin/cookies/browser Fetch Metadata/CORS, launch-scoped bearer and
  CSRF, strict framing, and 16,384-byte pre-parse body ceiling;
- exactly eight released zero-argument semantic commands and fixed `shell=False` argv; no caller
  shell, executable, env, CWD, path, URL, selector, plugin, install, Terraform, or cloud override;
- pinned Python 3.12.3 runtime/entrypoint/lock, `-I`, empty child environment, private HOME/config,
  no ambient credential/proxy/startup/import hooks;
- descriptor-relative directory-FD operations, no-follow/type/link/device/inode/mount/use-time
  checks, mode-0700 workspaces, read-only base, and marker-bound refusal cleanup;
- functional Seatbelt network/base-write denial; no sudo/container privilege;
- released 120-second, 536,870,912-byte command memory, and 268,435,456-byte workspace ceilings,
  plus CPU/file/FD/process/output limits and TERM/KILL/reap of the complete tree including rapid
  reparented and `setsid` descendants;
- runner/workspace locks, monotonic fences, CAS/idempotency, insert-only hash-chained audit,
  crash reconciliation, reset safety, exact eleven-asset release, atomic pointer, evidence, and
  narrow rollback.

Phase 1 must prove a non-poll-only Darwin descendant-control mechanism and functional containment
on the exact admitted host or stop. Phase 3 must then retain the exact test-only RED commit and run
all 44 stable assertions through real public runner Make targets after fixture markers and before
any production behavior. Missing tools/commands/contracts, skips, helper-only failures, and early
setup failures cannot count as RED. This is sufficiently exact for cook; the empirical results are
execution gates, not claims already proven.

The nine-row S3 scan matrix remains mandatory and includes syntax, Bandit, pip-audit, deterministic
policy/AST, protected source, credential/private-path, evidence closure, no-cloud, and runtime
containment summaries. Plan-only scans find no credential, private absolute path, source-scope
escape, generated contract, or cloud authority.

`S3=pass`.

## Whole-Plan Versus Staged Scope

The whole plan is selected because all six phases now share one released, immutable dependency and
no phase requires a shared write. A staged-only scope would not reduce dependency or ownership
risk and would fragment the required RED-before-GREEN provenance. Ordering remains strict:

1. characterize seams and admit containment/descendant control;
2. bind and mutation-test exact release bytes;
3. commit public-path RED tests and gate scaffolding;
4. implement fail-closed execution;
5. implement fencing/state/audit/atomic release; and
6. prove exact commands, S3, evidence, rollback, independent reviews, and human approval.

`COOK_SCOPE=whole-plan` does not authorize parallel behavior before Phase 3 RED or waive a STOP.

## Audit Closure

- CK strict validation: 0 errors, 0 warnings, six phases.
- CK status: pending, 0/6 complete, expected before cook.
- Contract/pin/path/catalog closures: PASS.
- Local links/anchors, placeholders/future SHA, protected scope, private path, diff, and stale
  blocked-dependency sweep: PASS.
- Only Issue #9 plan/audit artifacts changed from the exact starting head.
- Historical blocked audit remains unchanged and correctly describes its older input.
- Output commit is intentionally published after commit/push rather than embedded recursively.

## Next Phase

Remove `ready for plan audit`, add `ready to cook`, and begin `$ck:cook` Phase 1 from an exact
clean implementation base containing released Stage A. Any plan-byte change, release drift,
write-lease overlap, host mismatch, or failed phase admission requires a fresh stop/audit.
