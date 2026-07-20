---
phase: 9
title: "AWS State Cost and Persistence Decisions"
status: pending
priority: P1
dependencies: [1, 6]
effort: "L"
---

# Phase 9: AWS State Cost and Persistence Decisions

## Overview

Produce owner-ready AWS state, cost, persistence, networking-egress and office-hours decision
records before Terraform topology or adapter assumptions harden. This phase makes no AWS call and
does not apply infrastructure.

## Context Links

- [ADR-010 through ADR-016](./architecture-decisions.md)
- Discovery technology decision inputs: AWS state/cost/ClickHouse/office-hours sections
- Official source register S06-S18
- PH-C03/C04/C09, PH-H07/H08/H09 and SC-05/12/13/17/18

## Requirements

- Planning defaults: configurable `ap-southeast-1`; weekdays 08:00-18:00
  `Asia/Ho_Chi_Minh`.
- Explicit TBC apply gates: monthly total/residual ceiling, retention by data class, exact
  cold-start/readiness SLO, production RTO/RPO, account/environment layout and apply approver.
- State matrix owns authority, backup, restore/rebuild, zero behavior, residual cost and operator
  for every stateful component.
- Compare ClickHouse disposable projection, fenced EBS and supported object/managed alternatives.
- Compare Glue Iceberg REST with viable catalog fallback; compare managed vs self-hosted
  Superset/OpenMetadata DB/search persistence.
- Price active office hours, compute-zero/off-hours, one classroom, failure/retry storm, retained
  backup/log growth and forgotten teardown. Never call EC2-zero “zero cost.”
- Compare network egress options (NAT, endpoints, controlled public egress) against security/cost.
- Decide whether AWS orchestration has a learning/runtime need; no local/AWS symmetry decision.

## Architecture

A machine-readable decision model feeds ADRs, Terraform variables/policies, C4 annotations and
cost tests. Unknown owner thresholds stay `TBC` with `blocks: aws-apply`; parsers reject
numeric pass/fail or marketing claims while TBC remains.

Required state rows: S3/Iceberg objects and metadata, catalog pointers, ClickHouse, Superset
metadata/cache/jobs, OpenMetadata DB/search, portal identity/progress/evidence, orchestration,
Terraform state, and optional AI workflow state.

## File Inventory

| Action | Likely path | Rough size | Test impact |
|---|---|---:|---|
| Create | `docs/decisions/aws/{state-ownership,clickhouse-role,iceberg-catalog,metadata-persistence,office-hours,network-egress}.md` | 800-1,200 lines | ADR completeness |
| Create | `infra/aws/decisions/state-matrix.yaml` | 200-300 lines | Schema/owner/gate |
| Create | `infra/aws/decisions/cost-model.yaml` | 250-400 lines | Cost scenarios/source timestamps |
| Create | `infra/aws/decisions/apply-gates.yaml` | 100-180 lines | TBC blocker enforcement |
| Create | `scripts/aws/check-decisions.py`, `scripts/aws/cost-model.py` | 500-800 LOC | Deterministic model |
| Create | `tests/aws/decisions/**`, `tests/aws/cost/**` | 700-1,000 LOC | Incomplete/TBC/golden cases |
| Modify | AWS Structurizr view annotations | 80-150 lines | State/cost/readiness boundaries |
| Modify | `Makefile` | 20-40 lines | Decision/cost targets |

## Interface Checklist

- [ ] `StateOwner(authority, persistence, backup, recovery, rto, rpo, zeroBehavior, cost, owner)`
- [ ] `CostScenario(region, hours, learners, retention, failureMode, lineItems, sourceDate)`
- [ ] `ApplyGate(id, value|TBC, owner, blocks, evidence)`
- [ ] ClickHouse/catalog/metadata option scorecards
- [ ] office open/close/readiness/drain state machine
- [ ] next-run/override/timezone semantics

## Dependency Map

- Requires golden contract and AWS architecture concern IDs.
- Does not block local Phases 2-8.
- Blocks accepted production topology/apply. Phase 10 may build parameterized non-applying modules
  and Phase 11 may run local contract spikes while apply TBCs remain.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Stateful row missing authority/restore/RTO/RPO | Decision check fails |
| Critical | Cost claim while ceiling/retention/SLO TBC | Claim/apply gate fails |
| Critical | Backup succeeds but restore oracle fails | Not ready; scale-down/migration blocked |
| High | EC2/tasks zero with residual RDS/search/LB/NAT/log cost | Residual inventory remains visible |
| High | Retry storm/forgotten teardown | Quota/alarm/kill-switch scenario exceeds and flags |
| High | Timezone/holiday/active session | Next run/drain/override behavior explicit |
| High | Disposable ClickHouse misses readiness/equivalence | Hypothesis rejected |

## Tests Before

Create incomplete state/TBC-hidden/zero-cost/failed-restore/price-stale fixtures and golden cost
calculations. Tests must fail any unowned state or unattributed price.

## Refactor

No product refactor. Update architecture annotations and decision inputs only.

## Tests After

Validate every matrix row, reproduce cost cases, sensitivity-test hours/region/retention/network,
and trace decisions into Terraform/adapters/apply gates.

## Regression Gate

```bash
make state-matrix-check
make cost-model-check
make aws-decision-check
make architecture-check
```

## Implementation Steps

1. Define schemas and failing incomplete/false-claim fixtures.
2. Inventory state and cost line items with dated authoritative sources.
3. Model ClickHouse, catalog, metadata/search and network options.
4. Define office open/readiness and close/drain/checkpoint workflows.
5. Produce active/off-hours/failure/retention sensitivity tables.
6. Present TBC values to product/FinOps/operations owners; record decisions or retain blockers.
7. Export accepted interfaces/defaults to Phase 10/11 without authorizing apply.

## Success Criteria

- [ ] Every stateful component has an owned authority/recovery/cost row.
- [ ] Cost model itemizes residual services and records source date/assumptions.
- [ ] ClickHouse disposable role remains a hypothesis until measurable admission passes.
- [ ] Region/hours defaults are configurable; TBC gates are machine-visible.
- [ ] No AWS apply, cloud resource, or false cost/readiness claim occurs.

## Risk, Security, and Rollback

AWS prices/service support drift; version inputs and source dates, require refresh before approval.
Decision artifacts contain no account IDs/credentials. Rollback reopens the ADR and blocks
dependent apply; local release is unaffected.

## Next Steps

Pass parameterized interfaces to Phases 10/11. If owners do not resolve TBCs, those phases stay
non-applying and the issue still may ship the local release.
