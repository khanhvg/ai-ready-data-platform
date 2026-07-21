---
type: independent-plan-validation
issue: 9
date: "2026-07-21"
inputSha: "de66ad3da6a4f6ed49059e547689462f8269bca5"
verdict: PASS_WITH_FIXES
readiness: NOT_RUN_DEPENDENCY_BLOCKED
implementationDependency: issue-8-released-stage-a-sha
---

# Independent Validation: Issue #9 Privileged Local Runner

## Summary

`PASS_WITH_FIXES` for plan validation only. The six-phase plan is traceable, TDD-first,
fail-closed and scoped to Issue #9 after five objective defect classes were corrected. This is
`INDEPENDENT_VALIDATION_PASS_NOT_READINESS`: no runner/test/config/product behavior was
implemented, no readiness/red-team audit was run, and no phase may enter cook while the exact
released Issue #8 Stage A SHA remains absent.

## Authority and Non-Authority

- Validation input: `de66ad3da6a4f6ed49059e547689462f8269bca5`.
- Integration/implementation base: `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Branch: `plan/issue-9-privileged-local-runner`.
- Plan: `plans/260721-009-privileged-local-runner/plan.md`.
- Planner handoff: <https://github.com/khanhvg/ai-ready-data-platform/issues/9#issuecomment-5036406242>.
- Planning-only parallelization authority: <https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770>.
- Scope allowed here: Issue #9 plan and validation artifacts only.
- Scope not exercised: runner/tests/config/product implementation, Issue #8 contract ownership,
  readiness/red-team, portal/framework, sudo/container privilege, host-destructive action,
  cloud/AWS/Terraform, PR creation, merge or other issues/worktrees.

## Exact Input Proof

| Check | Observed result |
|---|---|
| Worktree branch | `plan/issue-9-privileged-local-runner` |
| Initial local HEAD | `de66ad3da6a4f6ed49059e547689462f8269bca5` |
| Initial upstream tracking SHA | `de66ad3da6a4f6ed49059e547689462f8269bca5` |
| Fresh live branch SHA (`git ls-remote`) | `de66ad3da6a4f6ed49059e547689462f8269bca5` |
| Initial worktree | Clean |
| Integration base ancestry | `24be3b34c6b0fcdbd07c5800dcab349054e34713` is an ancestor of the validation input |
| Diff from integration base | Exactly the ten original Issue #9 plan files |
| Issue #9 | OPEN |
| Required classification | `risk:high`, `tdd`, `security:S3`, `backend` present |
| Workflow label at input | Exactly `ready for plan validation` among workflow-state labels |
| Planner handoff | Exact branch/SHA/plan/dependency and `PLANNER_ONLY_NOT_VALIDATED` confirmed |
| Issue #8 contemporaneous state | OPEN, plan-only, `ready for plan validation`; no released Stage A SHA/handoff |
| Current shared runner recipes | Three I5-04 registry rows are `future-owner`; no `mk/issue-5/i5-04.mk` exists |

## Validation Workflow

The requested `ck:plan validate` workflow was exposed and used in both forms:

1. Full workflow-equivalent validation: read the plan, all six phase files, all companion files,
   repository docs and existing entrypoints; apply Full-tier Fact Checker, Flow Tracer, Scope
   Auditor and Contract Verifier roles; propagate confirmed constraints; reread every plan file;
   run a whole-plan consistency sweep.
2. CLI structural gate:
   `ck plan validate plans/260721-009-privileged-local-runner/plan.md --strict`.

Interactive questions were unnecessary because the owner supplied eleven authoritative validation
constraint groups and directed objective fixes. Those constraints were treated as the validation
answers; no missing dependency value or security relaxation was inferred.

## Objective Fixes Applied

1. **Provenance separation:** renamed the ambiguous implementation `inputSha` to
   `integrationBaseSha`, recorded the exact validation input separately, and made the pass status
   explicitly non-readiness and `BLOCKED_FOR_COOK`.
2. **Exact TDD evidence:** replaced prefix-only RED planning with 44 stable assertion IDs and exact
   pre-behavior oracles covering interpreter/import/startup/argv/path/env/network/quota/output/
   descendant/base/browser/race/crash/idempotency/release behavior.
3. **Transport and contract exactness:** split bearer/CSRF secret files, bound both to one listener
   launch, denied prior-launch replay and ambiguous/oversized framing, and required exact-set Issue
   #8 version negotiation with no implicit latest/range/downgrade/alias.
4. **Evidence privacy consistency:** resolved the conflict between “exact argv” and “no absolute
   private paths” by requiring the exact public gate command, canonical role-based child argv and
   actual-argv digest; raw absolute child argv is never persisted. Issue #8 must support that shape
   or dependency admission stops.
5. **Feasibility and exact admissions:** made rapid double-fork/reparent/`setsid` accounting a
   non-poll-only Darwin capability gate before RED/product cook; expanded exact future paths,
   current inputs, commands and tool admissions; and added the required nine-row S3 scan matrix.

## Required Validation Matrix

| # | Boundary | Result | Evidence in the fixed plan |
|---:|---|---|---|
| 1 | Requirements/risk/threat/architecture/test/evidence/rollback traceability and exact paths/commands | PASS | `requirements-risk-threat-traceability.md`, all phase files, `planned-paths-and-admissions.md`, `verification-evidence-and-rollback.md` |
| 2 | Issue #8 dependency and ownership boundary | PASS | Phase 1 remains plan-only now; all cook is blocked on an exact released Stage A SHA; Phase 2 consumes shared contracts read-only and forbids fake/local substitutes |
| 3 | Private transport/browser boundary | PASS | Owner-only UDS default, explicit ephemeral loopback fallback, exact Host, empty Origin allow-list, bearer+CSRF, launch binding, request framing, no CORS/cookie/browser-direct execution |
| 4 | Typed allow-list and version negotiation | PASS | Eight semantic IDs are conditional on the released matrix; strict unknown command/field/version/arg/env denial and no implicit negotiation |
| 5 | Workspace containment | PASS | Private owner-bound roots, read-only base, directory-FD/no-follow identity, symlink/hardlink/special/path traversal/TOCTOU tests, no writable startup/import roots |
| 6 | Process controls | PASS | Pinned Python/entrypoints/lock, fixed argv and empty env, no credentials/network/cloud/Terraform, exact wall/CPU/RSS/disk/file/FD/output/descendant bounds, cleanup/audit; descendant feasibility now fail-closed |
| 7 | Concurrency | PASS | Runner-wide/workspace locks, monotonic fence epochs, expert/learner separation, deterministic cross-entrypoint barriers, SQLite/manifest/pointer crash points and replay/idempotency rules |
| 8 | Stable contemporaneous RED IDs | PASS | 44 exact IDs with intended-fixture markers and pre-behavior failure oracles; required missing tools/skips cannot count as RED |
| 9 | Real verification and 16 GiB admission | PASS | Exact four-command future gate; current `data-contracts-check` exists; three runner recipes are admitted future commands; real host/tool/import/path observations are recorded |
| 10 | S3/evidence/redaction/rollback/human gate | PASS | Nine required S3 scan rows, schema/hash closure, private-path/PII/secret rejection, narrow owner-only rollback, exact-head independent review and human approval |
| 11 | Destructive/privilege/scope exclusions | PASS | No sudo, container privilege, package install at runtime, destructive host cleanup, portal/framework, root/shared-path drift, PR or merge authority |

## Full-Tier Verification Results

Six phases require Full tier. Sixteen plan-accuracy claims per phase were sampled and traced for
96 total claims. “Verified” includes proof that a future-create path/command is intentionally
absent now and has a precise dependency/tool admission; it does not claim future behavior exists.

| Phase | Claims | Fact/flow/scope/contract evidence sampled | Result |
|---:|---:|---|---|
| 1 | 16 | Generator `--profile/--seed/--out`; loader raw/DB args and close; Airflow explicit paths; exporter args; 51 dbt SQL models; 11 curated assets; expert Make defaults; host tuple; master trace IDs; future fixtures absent/admitted | 16 verified |
| 2 | 16 | Issue #8 OPEN/plan-only; no release SHA; base ancestry; runner registry `future-owner`; evidence owner currently I5-01; current schemas/registry/migration inputs; read-only ownership; exact release/version/generator/activation STOP rules | 16 verified |
| 3 | 16 | Future test roots absent/admitted; all 44 stable IDs; fixture-marker and no-skip semantics; deterministic TOCTOU/race/crash barriers; browser pre-allocation oracles; protected/base/foreign invariants | 16 verified |
| 4 | 16 | macOS 26.5.1/25F80 arm64/16 GiB; Python 3.12.3; `LOCAL_PEERCRED`, no-follow and rlimit APIs; `sandbox-exec` presence vs functional admission; pinned entrypoints/imports; transport/argv/env/quota boundaries | 16 verified |
| 5 | 16 | Existing curated manifest/current-pointer schema and ordered assets; SQLite/fence/audit split; stale-owner CAS; reset/export/verify conflicts; Airflow guard scope; crash/fsync/rename/reader and idempotency semantics | 16 verified |
| 6 | 16 | Root wildcard Make-fragment include; existing I5-01 gate; exact future recipes; S3 commands/tool admission; evidence root/schema/hash/redaction; rollback ownership; protected paths; exact-head review/human approval | 16 verified |

- **Tier:** Full
- **Claims checked:** 96
- **Verified after fixes:** 96
- **Failed:** 0
- **Unverified:** 0

The Issue #8 release identity is not counted as an unverified plan claim: its absence is verified
external state and is intentionally modeled as the hard implementation blocker.

## Repository and Tool Reality

- Existing entrypoints and manifests verified at the integration base and validation input:
  `data-generator/generate.py`, `ingestion/load_raw.py`,
  `orchestration/airflow/callables/pipeline.py`, `transform/dbt/dbt_project.yml`,
  `transform/dbt/profiles.yml`, `serving/export_marts_snapshot.py`,
  `lake/curated_assets.json`, `contracts/data/curated-release-manifest.schema.json`, and the three
  referenced `scripts/golden/` helpers.
- Root `Makefile` includes `mk/issue-5/*.mk`; `data-contracts-check` exists in
  `mk/issue-5/i5-01.mk`. The three runner targets do not exist and remain registry `future-owner`,
  so they were not executed or faked during this plan-only validation.
- Current host matches the planned narrow tuple. `/usr/bin/sandbox-exec` exists, but the plan
  correctly requires functional containment and descendant-control admissions before readiness.
- Bandit and pip-audit are absent from the global validation shell. This is not a skip: the fixed
  plan requires exact versions/hashes in the future app lock and fails the future gate if either is
  missing. Global pytest exists but grants no future runtime authority.

## Strict Checks

The final artifact set is required to pass all of the following from the repository root:

```bash
ck plan validate plans/260721-009-privileged-local-runner/plan.md --strict
ck plan status plans/260721-009-privileged-local-runner/plan.md
git diff --check
git diff --name-only de66ad3da6a4f6ed49059e547689462f8269bca5
git status --short
```

Additional deterministic checks cover local Markdown targets/anchors, exact existing/planned path
classification, future-command admission, placeholder markers, duplicate stable RED/S3 IDs,
required phrase consistency, secret/private-path patterns and whole-plan stale terms. Final result:
zero structural errors, broken local links/anchors, unexplained placeholders, duplicate IDs,
unowned changed paths or unresolved contradictions.

The SHA-256 closure for every validated plan/report artifact except the checksum file itself is in
`plans/260721-009-privileged-local-runner/validation/artifact-sha256.txt`. The containing Git
output SHA is intentionally not embedded in an artifact that would recursively change it; it is
reported in the validation handoff after commit/push.

## Whole-Plan Consistency Sweep

- Reread `plan.md`, all six phases, `implementation-boundary-and-design.md`,
  `requirements-risk-threat-traceability.md`, `verification-evidence-and-rollback.md` and
  `planned-paths-and-admissions.md` after propagation.
- Checked provenance terms, dependency wording, secret paths, version/fallback behavior,
  canonical/raw argv wording, descendant guarantees, RED IDs, S3 IDs, exact commands, path
  ownership, rollback and phase order.
- Reconciled contradictions: 5 classes.
- Unresolved contradictions: 0.
- No implementation recommendation is made; the fresh readiness phase must remain
  dependency-aware and return blocked while Issue #8's exact released Stage A SHA is absent.

## Verdict

`PASS_WITH_FIXES` for independent plan validation. Transitioning Issue #9 from
`ready for plan validation` to `ready for plan audit` is valid because that label represents the
next plan gate, not implementation readiness. Cook remains hard-blocked on
`issue-8-released-stage-a-sha`.

## Unresolved Questions

None for plan validation. The exact released Issue #8 Stage A SHA/version/operation matrix is an
explicit future readiness admission. The Darwin descendant-control functional proof is an exact
Phase 1 admission before RED or behavior work. Neither is a value this validation may invent or
waive.
