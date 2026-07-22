---
phase: 4
title: "Cost Model CostGuard and Scheduling"
status: pending
priority: P1
dependencies: [3]
effort: "L"
---

# Phase 4: Cost Model CostGuard and Scheduling

<!-- Updated: Validation Session 1 - labelled offline golden values as synthetic test inputs, never current prices. -->

## Context links

- [Pricing, formulas, CostGuard and schedule contract](./decision-state-and-cost-contract.md#pricing-snapshot-schema)
- [Cost scenarios](./requirements-and-risk-traceability.md#cost-scenario-coverage)
- [Pricing-source candidates](./current-source-inventory.md#official-pricing-source-candidates)

## Overview

Implement the strict offline pricing/cost model, 730-hour and scheduled-demo scenarios,
fail-closed CostGuard, and start/stop decision model. No rate is fabricated and no live refresh,
AWS API, account, or cloud scheduler is required by deterministic tests.

Offline golden rates and quantities are synthetic test inputs only. They prove arithmetic and
failure behavior and cannot be presented as a current pricing snapshot or AWS estimate.

## Requirements

- Functional: FR-010..014, FR-019.
- Non-functional: NFR-001..005/008/009/012/013.
- Required caller inputs: finite positive `monthlyBudgetUsd`, explicit region, complete schedule,
  finite non-negative contingency. Missing/invalid/TBC fails closed.
- All selected persistent/fixed dimensions remain visible during stopped compute.
- Support, taxes, discounts/commitments, free tier, private pricing and FX remain explicit
  exclusions unless separately sourced and approved.

## Architecture

```text
checked-in raw/projection pricing snapshot -> strict parser/provenance/freshness
selected BOM + scenario inputs -> unit/formula engine -> raw exact totals
raw total + caller contingency/budget -> CostGuard allow/deny/blocked-tbc
schedule state machine -> active/start/drain/retry/residual quantities
```

The optional network refresh can fetch a candidate snapshot in a separate explicit workflow, but
accepted release tests always replay checked-in bytes offline.

## Related code files

- Current implementation allow-list: `[]`.
- Exact snapshot/schema/model/test/ADR/Make files: `TBC` in amendment.
- Candidate ownership envelope: issue-owned cost/state decision models/tests,
  `docs/decisions/aws/**`, `mk/issue-5/i5-09.mk`.
- AWS/Terraform/account configuration files: forbidden.

## Tests before

- 730-hour, demo, stopped-but-not-zero, growth, transfer, backup/log, network alternative,
  failure/retry/forgotten teardown, contingency/rounding and over-budget goldens.
- Missing/invalid/TBC budget/region/schedule/timezone/holiday/override/contingency/snapshot.
- Stale/unattributed/foreign-region/wrong-currency/wrong-unit/wrong-SKU/duplicate price.
- NaN/Infinity, negative, exponent/precision/quantity/collection overflow and rounding bypass.
- Cost line without BOM/price, selected BOM without all lifecycle costs, hidden exclusions.
- Live-refresh-only evidence or network/account access during core tests.

## Refactor

Use one Decimal-based formula engine and closed unit registry. Cost inputs are immutable data;
never execute formulas from snapshots. Keep scenario derivation, arithmetic, presentation rounding,
and CostGuard decision separate and testable.

## Tests after

- Golden cases reproduce byte/semantic-identically offline.
- Guard compares unrounded total plus contingency and reports stable top drivers/alternative IDs.
- Display uses explicit half-up cents without affecting guard outcome.
- Schedule quantities include opening, hydration, drain, backup, retry, override and cleanup lag.
- Residual inventory names every retained selected EBS/EFS/S3/RDS/OpenSearch/NAT/EIP/ALB/log/
  backup/transfer/KMS dimension.

## Regression gate

```text
make cost-model-check
make state-matrix-check
make aws-decision-check
```

All are future offline/non-applying commands.

## Implementation steps

1. Define strict source/snapshot schema, safe source hosts/APIs, unit and formula registries.
2. Write and prove RED-B/RED-D pricing and cost fixtures.
3. Implement canonical snapshot parsing, provenance/freshness and content hashing.
4. Implement exact Decimal formulas, conversions, raw totals and presentation rounding.
5. Derive baseline-730h and schedule-demo quantities including stopped residuals and failures.
6. Implement CostGuard input binding, deny/blocked behavior, top drivers and authored alternatives.
7. Implement schedule/calendar/open-close state model and quantity emission without cloud action.
8. Run network-denied deterministic replay and optional-refresh isolation tests.

## Success criteria

- [ ] Every numeric output is reconstructable from source, quantity, unit, formula and rounding.
- [ ] Both 730-hour and scheduled-demo scenarios pass complete golden coverage.
- [ ] Stopped compute never hides retained billable dimensions.
- [ ] Missing/invalid/TBC/stale/unreconciled inputs block; over-budget denies.
- [ ] No hardcoded owner budget, region, schedule, rate or compatibility claim exists.

## Risk assessment

Pricing pages and APIs change, and billing units are easy to mis-map. Mitigation is immutable raw
source hashing, exact SKU/dimension/unit provenance, a closed conversion registry, freshness
failure and human snapshot diff review. Rollback restores the prior accepted snapshot/formula
registry and invalidates dependent cost decisions.

## Security considerations

Pricing/schedule inputs are hostile. Enforce bounded strict parsing, URL/path containment, no
shell/eval, no account/credential access, and evidence redaction. A malicious alternative label
cannot inject a command or free-form recommendation.

## Next steps

Phase 5 uses the selected option/state/schedule/cost interfaces to close recovery, security,
observability and residual failure behavior.
