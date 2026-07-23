---
type: dependency-aware-readiness-audit
issue: 9
date: "2026-07-22"
status: blocked
verdict: BLOCKED
auditInputSha: "4cea857fd4a79dca966f4c6b8d4350b4e5d372a2"
validationInputSha: "de66ad3da6a4f6ed49059e547689462f8269bca5"
validationOutputSha: "4cea857fd4a79dca966f4c6b8d4350b4e5d372a2"
auditOutputSha: "externally-attested-in-issue-9-publication-comment"
dependencyIssue8: BLOCKED_UNRELEASED
cookScope: none
cloudAction: none
convenienceSkill: not-exposed-workflow-equivalent
---

# Fresh Independent Readiness Audit — Issue #9 Privileged Local Runner

## Verdict

`BLOCKED` for cook. `COOK_SCOPE=none`.

The validated plan is dependency-aware, security-complete at planning depth, TDD-first, and
contained within Issue #9 ownership. It does **not** have implementation authority because Issue
#8 Stage A is not reviewed, merged, or released. The exact released Stage A SHA, version matrix,
operation matrix, registry activation, evidence contract, and shared-contract lease-release
attestation are all absent. No whole plan or staged subset may enter cook until those exact
authorities exist and a fresh amendment, independent validation, and readiness audit bind them.

The label must remain `ready for plan audit`. This blocked audit is evidence of a real dependency
barrier, not authorization to add `ready to cook`, `in progress`, or a review label.

This audit performed no implementation, product/config/data change, product TDD test, dependency
installation, PR, merge, Issue #8 write, worktree inspection, AWS/Terraform/cloud action,
destructive operation, or human-approval synthesis.

## Fresh Identity and Immutable Input Proof

| Check | Observed result |
|---|---|
| Auditor identity | Fresh independent readiness auditor; not the earlier planner or validator |
| Requested runtime profile | Codex `gpt-5.6-sol`, `model_reasoning_effort="xhigh"`; no shell API independently attests the serving model |
| Required worktree | exact issue-specific checkout `ai-ready-data-platform-issue-9-runner` |
| Required branch | `plan/issue-9-privileged-local-runner` |
| Audit input | `4cea857fd4a79dca966f4c6b8d4350b4e5d372a2` |
| Local HEAD before edits | exact audit input |
| Upstream before edits | exact audit input |
| Fresh `git ls-remote` branch SHA before edits | exact audit input |
| Worktree before edits | clean; no staged, unstaged, or untracked path |
| Validation chain | `de66ad3da6a4f6ed49059e547689462f8269bca5` → audit input, `PASS_WITH_FIXES` |
| Issue #6 release ancestry | shipped merge `24be3b34c6b0fcdbd07c5800dcab349054e34713` is an ancestor of the audit input |
| Input delta from Issue #6 release | exactly the thirteen validated Issue #9 plan/validation files; no product path |

The audit output SHA cannot be embedded literally in its containing report without recursion. The
exact output is published in the Issue #9 audit comment after commit/push and remote equality
verification.

## Workflow and Sources

The requested `$ck:plan-to-cook` convenience skill is not exposed in the current Codex skill
catalog. This audit did not claim to invoke it. It performed the workflow-equivalent readiness
audit with the available CK plan validation/status primitives, the CK plan verification roles,
project-organization rules, Git publication safety, repository source inspection, and live GitHub
dependency checks.

Sources read or checked:

- Issue #9 body, labels, planner handoff, independent-validation handoff, validated plan, six
  phases, four design/traceability/verification companions, validation report, and SHA-256 closure;
- Issue #5 owner parallelization decision, including exact dependency ordering and the single
  shared-contract writer rule;
- Issue #6 shipped state, exact merge handoff, and relevant read-only golden/data/evidence seams;
- Issue #8 body, labels, all eleven comments, the failed exact-head review, the owner-authorized
  serialized v3 repair, live v3 remote branch identity, and absence of a PR/release handoff;
- Issue #7 and #10 ownership boundaries to test framework/portal overlap;
- repository README, system/transform docs, version matrix, root Make fragment seam, current
  generator/loader/dbt/export/Airflow callables, curated eleven-asset registry, release schema,
  command-owner registry, version registry, and current evidence schema.

No other issue worktree was opened, inspected, or modified. The live Issue #8 branch SHA was read
only as remote coordination state and was not fetched, borrowed, merged, pinned, or treated as
release authority.

## Dependency Barrier

### Issue #6

Issue #6 is `CLOSED` with `shipped`. Its merge SHA
`24be3b34c6b0fcdbd07c5800dcab349054e34713` is the plan's immutable integration base and an
ancestor of the audit input. Consumption is read-only. This dependency is satisfied.

### Issue #8

Issue #8 is `OPEN` at `ready to cook`, with `risk:high`, `tdd`, `security:S3`, `shared-core`, and
`api`. Its last owner comment authorizes a serialized six-High repair on
`feature/issue-5-03-learning-contracts-v3`. The live branch currently resolves to
`9201b73e7f993e6b06624ea7a73eb07142b02cbd`, but that is an active, unreviewed implementation
head—not a release SHA. No PR exists for that head, and no Issue #8 comment publishes a
`STAGE_A_RELEASED`, `HANDOFF_MERGED_VERIFIED`, `RELEASE_SHA`, or equivalent release authority.

| Required Issue #8 authority | Audit disposition |
|---|---|
| Exact reviewed/merged/released Stage A 40-hex SHA | Missing; `issue8ReleasedStageASha` remains `null` |
| Exact readable/current version matrix and hashes | Missing released authority; current/unreviewed bytes are inadmissible |
| Exact typed operation/command matrix and hashes | Missing released authority; no local substitute or guessed eight-command wire contract allowed |
| Exact command-owner registry activation for the three I5-04 gates | Missing; current shipped registry still marks all three `future-owner`/`not-runnable` |
| Exact I5-04 evidence schema/canonicalization contract | Missing; current shipped `fitness-result-v1` fixes owner to `I5-01` |
| Shared-contract lease release | Missing; Issue #8 remains the active serialized shared-contract writer |
| Released type-generation procedure/output list, if required | Missing; wildcard generation is not authority |

`RUNNER_DEPENDENCY_NOT_RELEASED` is therefore the only acceptable admission result. A future
Issue #8 feature/repair head, guessed SHA, copied schema, local registry overlay, compatibility
alias, or unreviewed artifact cannot satisfy the barrier.

### Native `blockedBy` behavior

The validated frontmatter has `blockedBy: []`, while custom immutable fields state
`issue8ReleasedStageASha: null`, `implementationBlockedBy: issue-8-released-stage-a-sha`, and
`implementationReadiness: BLOCKED_FOR_COOK`. Empirically, `ck plan status` therefore reports six
pending phases but does not render a native dependency row. Strict CK validation still returns
zero issues because it validates plan structure, not the external release authority.

This is a machine-visibility gap, not permission to cook: the custom fields, dependency gate,
STOP conditions, issue label, and this audit all remain blocking. The validated/checksummed plan
was deliberately not rewritten during this blocked audit. After Issue #8 is released, the required
fresh amendment must add the real project-plan dependency (when present in the released tree),
populate exact release-authority identities/hashes and the lease-release attestation, then rerun
independent validation and readiness. Native `blockedBy` alone is advisory and may never replace
the exact release fields.

## Ownership and Path Audit

The exact future allow-list contains 66 unique create paths, all absent at the audit input; one
existing modify path, present; and 15 exact read-only inputs, all present.

Authorized future tracked writes are limited to:

- exact named paths under `apps/lab-runner/**`;
- `mk/issue-5/i5-04.mk`, owning only `runner-test`, `runner-security-test`, and
  `runner-race-test`;
- one narrow pre-`_run` learner-reserved-path refusal in
  `orchestration/airflow/callables/pipeline.py` that preserves expert defaults and DAG behavior;
- conditional generated bindings only after the released Issue #8 procedure names every exact
  output path and hash. A wildcard directory grants no write authority.

Overlap disposition:

| Owner/lease | Decision |
|---|---|
| Issue #8 shared contracts | No write overlap. `learning/contracts/**`, contract schemas, Issue #8 paths, and registry bytes are read-only/denied to Issue #9. The active lease still blocks cook. |
| Root Makefile/help integration | Denied. Issue #9 creates only its own fragment and consumes the released activation seam. |
| Issue #7 | No overlap with its `spikes/web/**`, scorecard/ADR, or `mk/issue-5/i5-02.mk` ownership. |
| Issue #10 portal integration | Denied and downstream only; no `apps/learning-portal/**`, BFF, browser session, or framework path. |
| Issue #6 shipped core | Read-only except the separately authorized, characterized Airflow callable seam; all golden/data/evidence contracts stay protected. |
| Cloud/container/Terraform | Explicitly denied; no path or command authority. |

The Airflow callable is not in Issue #8's 121-addition/zero-shipped-write Stage A boundary and is
the only existing product seam admitted by Issue #9. Any second existing-seam edit returns to a
fresh plan/validation/readiness decision.

## Staged-Scope Decision

`COOK_SCOPE=none`.

Phase 1 is dependency-independent in implementation mechanics, isolated to future runner tests,
and useful as characterization. It is not independently releasable product value, the owner and
validated plan explicitly block even that phase, and its fixture/namespace assumptions feed a
runner contract that Issue #8 may still change. Authorizing it would create a synthetic staged
cook contrary to the exact dependency order and could duplicate or stale shared-contract truth.

Phases 2–6 directly require the released Issue #8 identity and contract contents. No whole-plan
or staged implementation-bearing scope satisfies all dependency, audit, usefulness, isolation,
and no-duplication conditions.

## Requirements, Acceptance, Scenario, and TDD Traceability

Deterministic scans found:

- 20 unique `RUN-*` requirement/acceptance rows;
- 15 unique `THR-*` threat/abuse rows;
- 44 unique exact stable RED assertion IDs across interpreter, import/startup, argv, path,
  environment, network, quotas/output/descendants, base, browser, races, crash, idempotency, and
  release;
- 9 unique exact S3 scan IDs with failure rules and evidence locators;
- master trace links for the relevant ownership, ADR, `PH-*`, and `SC-*` constraints.

The TDD provenance rule is exact: each RED must run against exact input/dependency SHAs, reach its
fixture/precondition marker, fail for the named missing/refusing behavior before that behavior is
implemented, and retain the expected oracle. Missing tools/contracts, unsupported host, setup
failure, unconditional failure, skip, xfail, or failure before the marker cannot count. Phase 3
must commit the complete RED manifest before Phase 4/5 behavior; expectations cannot be weakened
to obtain GREEN.

The existing validation's artifact SHA-256 closure verified in full before this report was added.
The audit did not edit any checksummed validated artifact.

## S3 Security and Failure-Mode Disposition

| Boundary | Readiness disposition |
|---|---|
| Private transport | Complete at plan depth: owner-only UDS default; explicit random `127.0.0.1` fallback; exact Host; peer UID; no permissive CORS. |
| Browser/Origin/CSRF | Complete: reject Origin/cookie/preflight/simple form/browser Fetch Metadata, use separate launch-scoped bearer and CSRF secrets, reject replay before allocation. |
| Typed execution | Complete: released exact-set versions and eight semantic command IDs only; fixed argv; no raw shell/executable/env/cwd/path/URL/plugin/install/Terraform override. |
| Interpreter/import/startup | Complete: pinned runtime/entrypoint/lock/blob, Python `-I`, empty environment, private HOME, no `PYTHONPATH` or startup/plugin hooks. |
| Filesystem/TOCTOU | Complete: descriptor-relative retained directory FDs, no-follow/type/link/device/inode/mount/use-time checks, marker-bound refusal cleanup, read-only base. |
| Credentials/network/cloud | Complete: no ambient credentials/proxies/cloud/Docker/tracing values in child env; functional Seatbelt network/base-write denial; cloud/Terraform/sudo/container paths prohibited. |
| Quotas/process tree | Complete at plan depth with a future empirical gate: exact wall/CPU/RSS/disk/file/FD/process/output limits; no host-wide kill/limit; no cook if rapid fork/reparent/`setsid` control cannot be proven without poll-only luck. |
| Workspace isolation | Complete: private modes, per-workspace identities/generations, disjoint expert/learner namespaces, no caller-selected root. |
| Serialized mutation fence | Complete: runner-wide/workspace lock FD plus monotonic SQLite epoch, inherited capability, stale-owner compare-and-commit refusal. |
| Atomic eleven-asset release | Complete: one generation, exact ordered set, exclusive regular files, hashes/rows/schema, fsync, same-filesystem pointer replace, retained-FD reader verification. |
| Crash/retry/idempotency | Complete: deterministic fault points, transactional projections/audit, startup reconciliation, same-request reuse, changed-request conflict, no fabricated completion. |
| Audit/evidence tamper resistance | Honest local guarantee: insert-only/hash-chained/canonical/redacted and tamper-evident; no non-repudiation claim against root or hostile same-account code. |

No future security claim is considered proven by this audit. Required functional containment,
descendant-control, race, crash, rollback, and real bounded pipeline evidence remain implementation
gates after dependency release.

## Compatibility, Verification, Evidence, and Rollback

- Public compatibility is additive: current expert Make/Airflow defaults, DAG import/order,
  generator/load/dbt/export semantics, 18 tables, 51 models, and 11 marts remain intact.
- The supported host tuple observed at audit matches the plan: macOS `26.5.1` build `25F80`,
  Darwin arm64, 16 GiB, Python `3.12.3`. `/usr/bin/sandbox-exec` exists, but existence is not the
  required functional proof. Bandit and pip-audit are absent globally and must come from the
  future hash-complete app lock; missing required tools fail.
- Future runtime children install nothing and use no network. Clean-checkout gates must establish
  the pinned private runtime through the admitted lock/bootstrap procedure, then rerun offline.
- Exact required commands are:

  ```bash
  make runner-test
  make runner-security-test
  make runner-race-test
  make data-contracts-check
  ```

- Evidence is schema/canonicalization bound under
  `.artifacts/evidence/runner/<run-id>/`, with exact commands/tools/SHAs/hashes, canonical role-based
  argv plus actual-argv digest, bounded artifacts, redaction, S3 results, release identities,
  residual risks, and rollback. Raw absolute argv, credentials, private URLs/paths, raw env, raw
  customer/order rows, duplicate names, non-finite values, and unknown security fields fail
  publication.
- Rollback refuses new work, verifies owner/process/fence identities, stops only the recorded tree,
  restores only a previously validated pointer, preserves audit/evidence/expert paths, and refuses
  foreign/linked/special/mount-changed/ambiguous cleanup. No `pkill`, broad recursive delete,
  `make clean`, sudo, container cleanup, or destructive migration.
- Documentation impact is issue-local (`apps/lab-runner/README.md`); root docs, public portal docs,
  release manifest, and architecture/shared contracts remain protected unless a later separately
  authorized decision changes that boundary.
- Independent exact-head code/security review with zero unresolved Critical/High findings and
  separate human approval of that exact remote head remain mandatory. Any changed head invalidates
  review/approval.

## Plan Consistency Findings

The immutable validated files were reread as one plan. No contradiction weakens the current
dependency block, security posture, tests-first order, ownership boundary, verification commands,
evidence contract, rollback, or exact-head gates.

Two bounded editorial corrections are deferred to the mandatory post-#8 amendment rather than
rewriting the checksummed validation input now:

1. Native `blockedBy` must become machine-visible when the released Issue #8 plan is present, while
   exact release fields remain the authoritative gate.
2. Phase 5 should say it **extends**, rather than creates, the race test files already created RED
   in Phase 3; Phase 6 should say it **extends**, rather than creates, `evidence.py`, which Phase 5
   creates. The actual TDD ordering and exact path allow-list are otherwise unambiguous.

These do not create a cookable stage. The future amendment must apply them together with the real
Issue #8 authority, then run a fresh whole-plan consistency sweep, independent validation, and
readiness audit.

## Verification Evidence

Read-only/static audit checks completed:

| Check | Result |
|---|---|
| `ck plan validate plans/260721-009-privileged-local-runner/plan.md --strict` | PASS; 6 phases, 0 errors, 0 warnings |
| `ck plan status plans/260721-009-privileged-local-runner/plan.md` | 0/6 pending; confirms native `blockedBy` is not rendered |
| Validation SHA-256 closure | PASS for all 11 listed validated artifacts |
| Local Markdown links and anchors | PASS across 12 pre-audit Markdown files |
| Stable ID uniqueness | PASS: 44 RED, 20 RUN, 15 THR, 9 S3 |
| Exact path classification | PASS: 66 unique future creates absent; 15 read-only inputs and one modify seam present |
| Product/protected-path delta | PASS: input delta from Issue #6 contains only Issue #9 plan/validation files |
| Placeholder scan | PASS; no unexplained unfinished-work marker or fake-zero SHA |
| High-confidence secret/private-path scan | PASS; no key/token/private-key pattern or absolute local path |
| Dependency live-state check | PASS as a blocker: #8 open, no release markers/PR, active v3 repair head only |
| `git diff --check` and report-only changed-path gate | Required again before publication |

Exit code alone was not treated as evidence; counts, paths, identities, labels, comments, and
dependency absence were inspected explicitly. Product implementation tests were intentionally not
run in this blocked plan-audit state.

## Final State Decision

- Audit verdict: `BLOCKED`.
- Dependency: `BLOCKED_UNRELEASED` for Issue #8 Stage A.
- Cook scope: `none`.
- Issue #9 remains open at `ready for plan audit`; no workflow label transition.
- Next phase: wait for the exact Issue #8 Stage A release and shared-contract lease release, then
  perform a fresh plan amendment, independent validation, and dependency-aware readiness audit.
- Convenience skill disposition: `not-exposed-workflow-equivalent`.
- Cloud action: none.

`AUDIT_VERDICT=BLOCKED`

`DEPENDENCY_ISSUE_8=BLOCKED_UNRELEASED`

`COOK_SCOPE=none`
