# Independent Initial Plan Validation Report

## Result

**Verdict: PASS after bounded planning fixes.**

The 13-phase plan now satisfies the independent `$ck:plan validate` full-tier gate. No unresolved
plan contradiction or traceability omission remains. Owner-set and compatibility TBCs remain
visible at their exact boundaries: they block AWS apply, unsupported cost/readiness claims, or
optional admissions, but do not block credential-free local planning or the Phase 5 local core.

This was the independent Herdr/Codex initial validation phase in a fresh context, distinct from
the planner session. It did not run plan red-team, readiness/plan-to-cook audit, `$ck:cook`,
implementation, product/config/data changes, Terraform apply, destructive migration, cloud
creation, implementation branches, or implementation worktrees.

## Inputs and Drift Gate

| Input | Required SHA | Validation result |
|---|---|---|
| Immutable planner branch input | `8ec96f92245c679d019ac3648c5c2d77a49f0429` | Local HEAD, tracking ref and remote branch matched before the first edit; worktree was clean |
| Official golden main | `3cd3d41f71582774e8d9656a51d1044035f4503c` | `origin/main` matched and is an ancestor of planner input |
| Reviewed tree head | `d0273731a5077cc17c2f4398057623b83a50bb65` | Merge commit tree and reviewed-tree commit both resolved to `283d7751196034e27e2557c65ce980d3d0c72f06` |
| Discovery | `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430` | Ancestor of planner input; every discovery artifact read; raw discovery left unchanged |
| Planning sync | `b04ff80486de8a9c008c6320669212f27df80182` | Ancestor of planner input |

Ignore probing confirmed `.gitignore:62` ignores `plans/**/*`. Publication therefore must use
`git add -f plans/260721-005-enterprise-learning-sandbox` and no broader force-add target.

## Questions and Checks

No user question was required. The issue body and all six owner comment threads already fixed the
binding scope, golden input, risk/TDD/security/human gates, local/AWS defaults, TBC boundaries,
first narrative, and publication state transition. Asking again would have reopened explicit
owner decisions.

The validator read in full:

- issue #5 body and every comment;
- `plan.md`, all 13 phase files, and all six required companion artifacts;
- all seven discovery documents/data artifacts under `discovery/`;
- current README, architecture/data/runbook/version/Compose/Make contracts and the relevant
  generator, loader, exporter, Airflow, Iceberg, OpenMetadata, dbt, Rill and curated-asset files.

Repository claims checked against the immutable input include:

- generator ownership of 18 raw tables and deterministic anomaly/checksum evidence;
- 18 staging, 6 intermediate, 7 dimension, 9 fact and 11 mart dbt models (51 total);
- 11 Rill models, 11 metrics, 11 explores, including weighted promotion/fulfillment/return
  formulae;
- 11 curated assets and the four promotion-trust marts;
- current Iceberg `DROP` then `CREATE` non-atomic risk;
- current OpenMetadata 11 physical-Iceberg/45 logical-dbt identity intent and missing
  rename/delete reconciliation;
- current Airflow repository-root read-write mount, current venv-sentinel behavior, and absence
  of portal/API/Terraform product code at the input SHA;
- absence of tracked `docs/code-standards.md` in this worktree while preserving the owner’s stated
  user-owned-file boundary.

Primary-source checks were also made for C4 minimum-useful views, current OpenAPI status, ECS/ASG
zero-capacity behavior, Glue REST/SigV4, Terraform S3 lockfiles, Astro islands, Next static-export
constraints and AgentCore ephemeral session state. A fresh in-app browser was unavailable in this
validator environment. That does not convert discovery’s prior clean-browser observation into new
evidence: Phase 2 still requires a real-browser, identical-candidate scorecard before ADR-005 can
pass, and Phase 5 remains blocked until then.

## Full-Tier Verification Result

The plan has 13 phases, so the validation used the Full tier and the four required review roles:
Implementation Feasibility, Architecture, Domain Expert, and QA/Security. The minimum sample was
15 claims per phase, for 195 claims.

| Stage | Verified | Failed | Explicitly gated/unverified | Interpretation |
|---|---:|---:|---:|---|
| Immutable planner input | 178 | 12 | 5 | Twelve correctable planning gaps; five genuine owner/compatibility decisions |
| Post-fix recheck | 190 | 0 | 5 | All plan defects resolved; five unknowns remain honestly gated, not asserted as facts |

The five gated claim classes are: Phase 2 stack winner; owner-approved laptop resource
thresholds; current-version Glue/ClickHouse/Superset/OpenMetadata compatibility; the six AWS
apply-gate groups; and optional AI admission. Each has an owner, blocker, evidence command,
failure behavior and fallback.

## Findings and Exact Fixes

### High — resolved

1. **Binding and scenario traceability was incomplete.** The PH tables carried most fields, but
   bounded phase/scope was implicit, SC-01..SC-20 lacked acceptance/owner/dependency detail, and
   issue-owner requirements had no normative crosswalk.
   - Fixed `requirements-traceability.md` with OWN-01..OWN-10, an exact PH scope map, and expanded
     SC rows containing scope, owner/phase, acceptance/failure, evidence, rollback and dependency.

2. **Curriculum/data expansion could outrun the first usable product.** P6 depended only on P3 and
   P7 only on P1/P3/P4, permitting expansion before the real portal journey.
   - Added P5 to P6/P7 frontmatter, dependency text, waves and I5-06/I5-07 blockedBy rules. P5 is
     now the earliest usable product and `make local-journey-e2e` is the Wave 1 exit.

3. **Local/AWS equivalence was conceptual rather than versioned at exact paths.**
   - Added planned shared-core contracts
     `contracts/data/local-aws-data-product-equivalence-v1.yaml`,
     `contracts/data/iceberg-lifecycle-v1.yaml`, and
     `contracts/data/openmetadata-asset-identity-v1.yaml`; P7 proves the local oracle and P11
     consumes the same versions with explicit deviations.

4. **The issue graph had overlapping write authority.** I5-01/I5-03 could edit shared contracts
   from separate worktrees, and I5-11 could modify P10 Terraform task definitions.
   - Made I5-03 a sequential same-owner/same-worktree lease; made I5-11 own only adapter
     descriptors and consume Terraform outputs read-only; added a complete blockedBy/blocks
     matrix and exact-SHA handoff rules.

5. **AWS S3/state and human apply gates were not exact enough.**
   - Required public-access block, `BucketOwnerEnforced`, `aws:SecureTransport=false` deny,
     SSE-KMS, versioning, Terraform `use_lockfile = true`, least-privilege prefixes/actions, no
     static credentials, lifecycle/retention/deletion, logging/monitoring, version restore,
     account/region/environment/plan-SHA binding, Security approval and named apply approval.

### Medium — resolved

1. **Web-learning selection lacked exact decision evidence and fail behavior.**
   - Fixed exact Markdown/JSON scorecard paths, identical real-fixture candidate assertions,
     progressive disclosure, reversible navigation, controlled/environmental failure distinction,
     reset/verify/evidence flow, no-scroll completion, static/reduced-motion equivalence,
     source/non-copy inventory, and non-zero/no-ADR behavior.

2. **Planned file/command language was vague.** All phase inventory headers now say “Planned
   path”; the master contract distinguishes verified existing paths from future owned paths and
   requires Make help, exact evidence roots, typed failure and non-zero exit behavior.
   `make learn LESSON=promotion-trust` is the stable future local entry command.

3. **The owner’s `docs/code-standards.md` preservation boundary was not explicit.**
   - P1/P13, ADR-001, master acceptance and I5-01 now require byte-hash preservation when present,
     an explicit absent record otherwise, and no create/overwrite/delete without a separate owner
     decision.

4. **TBC wording differed across overview, views and phases.**
   - Normalized monthly/residual budget, retention by data class, cold-start/readiness SLO,
     production RTO/RPO, account/environment and named apply approver. Numeric TBCs are assigned
     to Product/FinOps/operations, S3/IAM to Security, and one exact plan to the named approver.

### Critical or unresolved validation defects

None.

## Requirements and Architecture Quality Result

- BO/CAP/FR/NFR/ASR, architecture views, ADRs, patterns, API/data/network/security/operations/cost
  and evidence commands are traceable. The five API categories remain logical taxonomy; actual
  initial deployment remains portal modular monolith plus isolated privileged runner.
- The retail promotion-trust narrative uses the four verified marts and requires real controlled
  failure, diagnosis, reset, verifier evidence and reflection. Rill/other heavy tools enhance but
  do not gate local completion.
- DuckDB/Rill local and ClickHouse/Superset AWS do not pretend topology equivalence. They share
  learning, data-product, Iceberg lifecycle, OpenMetadata identity and evidence versions; local
  MinIO/Lakekeeper/OpenMetadata prove the oracle before AWS adapters. AWS state ownership and
  residual-cost honesty remain explicit.
- The plan preserves exact generator/anomaly/dbt/mart/metric/lineage/evidence contracts and uses
  additive seams, dual-read/versioning, exact-SHA rollback and feature/adapter disable paths.
- The implementation graph has one shared-core authority, non-overlapping product paths,
  inherited risk:high/TDD/security:S3/human gates, exact input/output/merged-SHA handoffs, and a
  realistic I5-01/I5-02 first wave followed by I5-03→I5-04→I5-05.

## Remaining TBCs and Blockers by Boundary

These are preserved intentionally and are not validation failures:

| TBC / decision | Owner | Blocks | Does not block |
|---|---|---|---|
| Monthly total and residual budget ceilings | Product + FinOps | AWS apply and numeric cost/readiness claims | Local planning/release |
| Retention by S3 versions/backups/logs/traces/evidence/plans | Product + security + operations | AWS apply/hosted retention claim | Credential-free local core |
| Cold-start/readiness SLO | Product + operations | Disposable ClickHouse/ECS readiness acceptance and apply | Local journey |
| Production RTO/RPO | Product + operations/data owner | AWS apply and production recovery claim | Non-applying design/local release |
| Account/environment layout and current price/region inputs | Security + FinOps + platform | Real AWS plan/apply assertion | Static/mock/offline checks |
| Named apply approver and exact non-stale account/region/environment/plan SHA | Owner-designated human approver | Every AWS apply | All planning and non-applying work |
| Phase 2 web winner and exact implementation path | Portal owner after identical scorecard | I5-05 | P1/shared contracts |
| Current catalog/adapter versions and compatibility | Data/platform owners after spikes | AWS readiness/topology claim | Local Lakekeeper/OpenMetadata path |
| Optional AI use case/classification/eval/cost admission | Product/security/AI governance | Phase 12 add-on | Entire local core |

## Commands and Mechanical Results

| Command/check | Result |
|---|---|
| Branch/local/tracking/remote SHA preflight plus `git ls-remote` | PASS before edits; all planner inputs matched `8ec96f9…` |
| Main/discovery ancestry and reviewed-tree equality | PASS |
| `gh issue view 5 --comments` review | PASS; body and all comments read |
| `ck plan status` from the issue plan directory | PASS; 13 pending phases |
| YAML frontmatter/phase/dependency DAG sweep | PASS; 13 phases, unique 1..13, no cycle/missing dependency |
| Relative Markdown link sweep | PASS |
| ID/row sweep | PASS: 10 critical, 14 high, 20 scenarios, 10 owner crosswalk rows |
| Phase validation markers | PASS: 13/13 |
| Exactness/legacy-language sweep | PASS: no `Likely path`, `plans/...`, stale P6/P7 dependencies or P10/P11 ownership overlap |
| `git diff --check` | PASS |
| Changed-path scope | PASS; issue-plan directory only; raw `discovery/**` unchanged |

## Whole-Plan Consistency Result

**PASS.** Phase count/status/frontmatter/links, IDs, terminology, exact paths, defaults,
dependencies, waves, issue graph, release/rollback, preservation rules and planner/validator
self-reports agree. P11 now declares P7/P9 in frontmatter, matching its local-contract and AWS
decision inputs. P13’s local release dependency remains P1-P8 transitively; AWS/AI evidence is
optional or TBC-blocked and cannot be mislabeled pass.

The plan is ready for the distinct readiness/plan-audit phase. This report does not assert
implementation readiness and does not authorize implementation or AWS activity.
