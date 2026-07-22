---
title: "Issue #14 — Decide AWS state, cost, persistence, and readiness"
description: "Planner-only TDD contract for evidence-backed AWS state, topology, FinOps, scheduling, persistence, recovery, and apply-blocking decisions without cloud action."
status: pending
priority: P1
issue: 14
branch: "plan/issue-14-aws-decisions"
tags: [infra, critical, aws, finops, recovery, tdd, security-s3, decision-gate]
blockedBy: []
blocks: []
created: "2026-07-22T00:31:34.633Z"
createdBy: "ck:plan"
source: skill
planningMode: "planner-only-tdd-no-tasks"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
implementationDependency: "issue-11-released-architecture-concern-ids"
---

# Issue #14 — Decide AWS state, cost, persistence, and readiness

## Outcome

This is the fresh initial plan for GitHub Issue #14. It defines how a later implementation will
produce decision models, ADRs, tests, and compact evidence for AWS state authority, cost,
persistence, office-hour scheduling, recovery, and security. The planner creation step performed
no implementation, independent validation, readiness audit, AWS call, Terraform action, resource
creation, PR, or merge.

The current planning input is the clean Issue #6 release merge
`24be3b34c6b0fcdbd07c5800dcab349054e34713`. Issue #11 is not release authority: its current
plan/audit branch is dependency-blocked and has not published the exact released architecture or
curriculum concern IDs required by this issue. Planning may proceed, but implementation may not.

## Planner boundary and current authority

| Authority | Current value | Consequence |
|---|---|---|
| Implementation file allow-list | `[]` | No product, test, model, ADR, Make, or configuration file may be implemented yet. |
| Runnable command allow-list | `[]` | The three issue-owned target names remain registry declarations with `future-owner` / `not-runnable`. |
| Released Issue #11 concern IDs | `[]` | Legacy epic concern references are provenance only; no topology or BOM can claim current concern coverage. |
| Dependency release SHAs | `[]` | An Issue #11 branch, planner SHA, validator SHA, or blocked audit SHA is not a release. |
| Current pricing snapshot | `[]` | No rate, region-specific estimate, price freshness, or budget pass is claimed. |
| Current BOM/topology/resources | `[]` | No AWS service or Terraform resource is selected by implication. |
| Region/account/environment | `[]` | No account data is read; region must later be caller-supplied. |
| Owner budget/contingency | `[]` | `monthlyBudgetUsd` and contingency remain required caller inputs; no owner value is invented. |
| Apply/human cloud approval | `[]` | Planning and future offline implementation do not authorize plan/apply/destroy. |
| Cloud action | `none` | No credential, pricing API, AWS API, Terraform, or resource action is permitted. |

The YAML `blockedBy` field stays empty because Issue #11 has no released project-plan artifact to
reference. The external implementation dependency is still binding and is tracked by the explicit
`implementationDependency` field and the amendment gate below. Issue #14 does not block local
issues.

## Scope challenge result

- Existing code: Issue #6 supplies protected golden contracts, architecture views, evidence
  schemas, command registry, and the additions-only Make fragment seam. Issue #5 supplies the
  audited Phase 9 intent and non-authoritative historical concern references.
- Minimum change: issue-owned decision docs, state/cost models and tests, plus
  `mk/issue-5/i5-09.mk`, only after an exact allow-list amendment. No Terraform, adapter, portal,
  runner, lab, root Makefile, shared-contract, or architecture-view edit belongs here.
- Complexity: seven sequential implementation phases are justified by the independent state,
  cost, recovery/security, and dependency-reconciliation failure boundaries.
- Selected scope: **HOLD SCOPE**. The user-supplied decision and threat requirements are binding;
  no service is added for pattern symmetry.

## Stakeholders and decision rights

| Stakeholder role | Decision / evidence responsibility | May authorize AWS apply? |
|---|---|---|
| AWS architecture owner | Topology, network segmentation, state authority, ADR outcome, concern mapping | No; contributes design approval only |
| FinOps owner | Budget, contingency, price-source freshness, scenario assumptions, exclusions | No; contributes cost approval only |
| Operations / DR owner | Schedule, readiness, drain, backup consistency, RPO/RTO, restore and break-glass | No; contributes operational approval only |
| Security owner | IAM/KMS/backend/secret/network/evidence controls and residual S3 risks | No; contributes security approval only |
| Data/application owners | ClickHouse, Iceberg/catalog, OpenMetadata, Superset, search, agent/evidence ownership | No; accepts state and recovery responsibilities |
| Named cloud/apply approver | Exact account, environment, region, saved plan, expiry, identity and action | Yes, but only in a later separately authorized workflow |
| Human exact-head reviewer | Pre-merge review of the exact implementation head | Merge gate only; never cloud authority |

All named people, account identifiers, owner budgets, RPO/RTO values, and approval identities are
`TBC` until explicitly supplied. A role label is not a fabricated approval.

## In scope

1. A strict state/key/config authority model covering Terraform backend and lock, application
   config/secrets, ClickHouse, S3/Iceberg/catalog, OpenMetadata, Superset, search/index, agent
   state, CostGuard state, scheduler state, and evidence.
2. Option/ADR analysis for ECS on EC2 topology and segmentation, storage and catalog choices,
   metadata/search dependencies, BI persistence, and optional AI. NAT, endpoints, load balancer,
   EBS, EFS, RDS, OpenSearch, cache/broker, or AgentCore enter a selected BOM only when an exact
   released concern/NFR and measured need require them.
3. A plan-reconcilable BOM contract in which every future row maps to one future Terraform
   resource/data source/module variable/output and one or more released deployment concern IDs.
4. A current-source, provenance-rich, deterministic cost model with 730-hour and scheduled-demo
   scenarios, residual/fixed charges, exclusions, growth, contingency, and a fail-closed CostGuard.
5. Start/stop state machines, readiness, manual override, holidays/timezone, persistence/DR,
   teardown preserve/destroy modes, observability, security, rollback, and compact evidence.
6. Tests-first implementation and the future public target declarations
   `state-matrix-check`, `cost-model-check`, and `aws-decision-check`.

## Out of scope

- Terraform modules, plan/apply/destroy, backend bootstrap, AWS API or Pricing API calls, account
  discovery, credentials, resources, live compatibility tests, or real restore drills.
- AWS production/readiness, cost-approval, scale-to-zero, zero-cost, backup-validity, or
  compatibility claims.
- Implementation against unreleased Issue #11 plan/audit artifacts or invented concern IDs.
- Shared contracts, six protected Issue #6 views/renders, portal, runner, labs, adapters,
  root `Makefile`, root `release-manifest.json`, `.gitignore`, `docs/code-standards.md`, or golden
  behavior.
- A hardcoded region, account, environment, schedule, owner budget, contingency, RPO/RTO,
  retention, apply approver, or service selection.

## Required plan companions

- [Current source and authority inventory](./current-source-inventory.md)
- [Requirements, concern, and risk traceability](./requirements-and-risk-traceability.md)
- [Decision, state, BOM, and cost contracts](./decision-state-and-cost-contract.md)
- [Security, recovery, observability, rollback, and evidence](./security-recovery-and-evidence.md)
- [Implementation amendment and execution handoff](./implementation-handoff.md)
- [Protected input baseline](./protected-input-baseline.md)
- [Independent validation report](./validation/independent-validation-report.md)

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Authority and TDD Gate](./phase-01-authority-and-tdd-gate.md) | Pending |
| 2 | [State Key and Config Authority](./phase-02-state-key-and-config-authority.md) | Pending |
| 3 | [Topology Persistence Options and ADRs](./phase-03-topology-persistence-options-and-adrs.md) | Pending |
| 4 | [Cost Model CostGuard and Scheduling](./phase-04-cost-model-costguard-and-scheduling.md) | Pending |
| 5 | [Recovery Security and Observability](./phase-05-recovery-security-and-observability.md) | Pending |
| 6 | [BOM Terraform Concern Reconciliation](./phase-06-bom-terraform-concern-reconciliation.md) | Pending |
| 7 | [Verification Evidence Rollback and Human Gates](./phase-07-verification-evidence-rollback-and-human-gates.md) | Pending |

## Phase dependency graph

Implementation is single-writer and tests-first:

```text
Issue #11 released exact concern IDs
  -> exact-SHA plan amendment + non-empty validated allow-lists
  -> fresh independent revalidation -> fresh readiness audit
  -> P1 authority/RED contracts -> P2 state matrix -> P3 option ADRs
  -> P4 cost/CostGuard/schedule -> P5 recovery/security/observability
  -> P6 exact BOM/Terraform/concern reconciliation -> P7 evidence/rollback/human gates
```

Phases 2-5 may be designed independently, but they must be executed sequentially because they
converge on shared decision schemas and the same exact implementation allow-list. Phase 6 cannot
populate resource mappings until released Issue #11 concern IDs exist. Phase 7 cannot claim pass
while any apply-blocking `TBC`, stale price source, unreconciled BOM row, failed restore oracle,
or human exact-head review is outstanding.

## Decision outcome vocabulary

Every option and gate uses exactly one of:

- `selected`: evidence and decision owner accept the option for the bounded scenario.
- `rejected`: evidence shows the option violates a force, NFR, threat control, or cost guard.
- `deferred`: optional/non-blocking; no current implementation or cost claim.
- `blocked-tbc`: required value, dependency, compatibility result, or approval is missing.

`blocked-tbc` is never normalized to pass. Unknown numeric values remain absent/TBC rather than
zero. A selected decision is still not AWS apply authority.

## Binding quality gates

- Strict schemas reject incomplete, duplicate, contradictory, orphaned, or hidden-TBC state,
  option, BOM, price, cost, teardown, and evidence rows.
- Deterministic core tests run with no network, AWS SDK/CLI, account, credentials, or current-time
  dependency. Optional live source refresh only creates a candidate snapshot and cannot satisfy
  release by itself.
- Cost tests cover 730 hours, scheduled demo hours, stopped-but-not-zero, storage growth,
  requests, data transfer, backups, logs, NAT/endpoint alternatives, contingency, rounding,
  stale provenance, region/unit/currency mismatch, and over-budget denial.
- State tests cover writer/reader authority, encryption key/config dependencies, backup,
  restore/rebuild, RPO/RTO, retention, deletion, migration, lock/backend, teardown modes, and
  every minimum component row.
- S3 tests cover malicious snapshot/formula/unit/currency/URL/path input, duplicate keys,
  non-finite/overflow numbers, credential/account/private-path/PII leakage, IAM/KMS/backend/lock,
  destructive teardown, backup corruption, evidence tamper/replay, command/path injection,
  symlink, hardlink, and special-file attacks.
- Exact Issue #6 and released Issue #11 blast radii, protected tree digests, changed paths, and
  absent protected paths remain unchanged.
- Genuine RED evidence binds stable behavior IDs to exact expected-versus-actual status, failure
  code and invariant while production/model behavior is absent; offline price/cost goldens are
  labelled synthetic test inputs, never current price evidence.

## Future public command contract

The immutable command registry declares these I5-09 target names, but they are currently
`future-owner` and `not-runnable`:

```text
make state-matrix-check
make cost-model-check
make aws-decision-check
```

Only a later exact-SHA amendment may place them in a non-empty command allow-list. That amendment
must bind each target to exact scripts/tests/models, bounded runtime, typed failures, evidence
root, and protected-path check. The issue owns only `mk/issue-5/i5-09.mk`; root Makefile edits are
forbidden.

## Acceptance criteria

- Every stakeholder, FR, NFR, legacy concern provenance row, S3 threat, test, evidence artifact,
  rollback action, dependency, owner role, and STOP condition is traceable.
- The complete minimum state component set cannot pass with missing or contradictory authority,
  key, backup, RPO/RTO, retention, deletion, migration, or teardown fields.
- Option scorecards state forces and measurable admission/rejection evidence; optional services
  cannot appear through pattern theater.
- Every selected future BOM line has exact cost dimensions and an exact Terraform/concern mapping;
  every Terraform mapping is priced or carries an owner-approved explicit exclusion.
- CostGuard requires caller-supplied finite positive `monthlyBudgetUsd`, region, schedule, and
  contingency; compares unrounded total plus contingency; blocks over budget; reports stable top
  drivers and only pre-authored alternatives.
- Baseline and demo scenarios disclose all persistent/fixed costs while compute is stopped.
- Start/stop and restore state machines never mark ready before dependency health, hydration,
  migration, backup/restore, catalog/search/dashboard/query, and evidence oracles pass.
- Preserve/destroy teardown modes are explicit, default-preserving, separately authorized, and
  incapable of deleting evidence, keys, state, or durable data through a hidden default.
- Evidence is compact and hash-indexed below `.artifacts/evidence/aws-decisions/<run-id>/`, with
  no credentials, account IDs, account-specific values, private paths, or PII.
- No production/readiness/apply claim exists until Issue #11 release, exact amendment,
  independent revalidation, fresh readiness audit, human exact-head review, and a separate named
  cloud/apply authorization all exist.

## STOP conditions

Stop before implementation or publication of implementation authority on any wrong/dirty base,
missing Issue #11 release, invented concern/resource/path/SHA/rate/owner, conflicting lease,
protected-path mutation, non-empty cloud credential context used by a test, untrusted pricing
input, unresolved apply-blocking TBC, failed required test, state that cannot restore, destructive
default, stale/unreconciled cost, evidence leak/tamper, or absent human exact-head review.

## Planner handoff and self-verdict

At the published planner SHA, the next permitted phase was a **fresh independent plan validation**
at that exact SHA. It could correct plan artifacts only and could not perform readiness,
implementation, AWS/Terraform actions, PR, or merge.

Planner self-verdict: `PASS` for plan creation only. This verdict asserts scope, traceability, and
planner-static checks; it is explicitly `PLANNER_ONLY_NOT_VALIDATED` and grants no implementation
or cloud authority.

## Validation Log

### Session 1 — 2026-07-22

**Trigger:** Fresh independent initial `$ck:plan validate` workflow-equivalent at exact input
`51a45b54633e3c34ff39876ed9ddb8b9e675b3d1`.

**Questions asked:** `0`. The immutable user/GitHub authorities resolved every current decision;
missing dependency, owner, pricing, region/account, budget, recovery, review, and apply values must
remain TBC rather than be solicited or invented during initial validation.

#### Confirmed decisions

- Validation may pass while implementation remains blocked on released Issue #11 concern IDs.
- Issue #6 is released read-only authority; Issue #11 head is discovery-only.
- Implementation/cloud authority stays empty; future commands remain non-runnable names.
- Exact-head human merge review and separate named cloud authorization remain mandatory.

#### Objective corrections

- [x] Ground current sources in exact Git bytes and distinguish released, discovery-only, and
  future ownership classes.
- [x] Make option operability, residual cost, rollback, and exit dispositions explicit.
- [x] Bind genuine RED evidence to stable behavior IDs and expected-versus-actual results.
- [x] Label offline cost goldens synthetic and add clean-checkout/S3 future verification gates.

#### Impact on phases

- Phase 1: genuine RED provenance contract clarified.
- Phase 3: per-option outcome and evidence completeness clarified.
- Phase 4: synthetic offline golden boundary clarified.
- Phase 7: fresh clean-checkout replay and S3 scans made explicit.
- Other phases: reread with no propagation change required.

### Verification Results

- **Tier:** Full
- **Claims checked:** 105
- **Verified:** 105 | **Failed:** 0 | **Unverified:** 0

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all seven phase files, all six original companion contracts, and the
  independent validation report.
- Decision deltas checked: 6.
- Reconciled stale or incomplete references: 6 fix groups.
- Unresolved contradictions: 0.

The verdict is `PASS_WITH_FIXES_NOT_READINESS`. Implementation authority, released Issue #11
concern IDs, pricing, BOM, region/account, budget, RPO/RTO/retention, review, apply approval, and
cloud authority remain empty/TBC. The next workflow state is plan audit; the later dependency-
release amendment, fresh independent revalidation, and fresh dependency-aware readiness audit
remain mandatory before any cook scope can exist.
