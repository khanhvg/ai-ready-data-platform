---
phase: 6
title: "BOM Terraform Concern Reconciliation"
status: pending
priority: P1
dependencies: [5]
effort: "M"
---

# Phase 6: BOM Terraform Concern Reconciliation

## Context links

- [BOM/Terraform schema](./decision-state-and-cost-contract.md#bom-and-terraform-reconciliation-schema)
- [FR-009 and TBC register](./requirements-and-risk-traceability.md)
- [Implementation amendment](./implementation-handoff.md#amendment-contents)

## Overview

Create the exact logical BOM and future Terraform interface map only after selected ADRs and
released Issue #11 concern IDs exist. This phase plans resource/data source/variable/output
ownership for Issue #10; it does not create Terraform files, resources, plans, or AWS evidence.

## Requirements

- Functional: FR-003/004/009..012/017/018.
- Non-functional: NFR-002/003/005/008..010/012/013.
- Bidirectional one-to-many mappings are exact and orphan-free.
- Every selected lifecycle/cost dimension is priced or explicitly owner-excluded.
- Deferred/rejected/TBC options contribute no selected resource row.

## Architecture

```text
selected ADR + complete state rows + released concerns
  -> logical BOM rows and lifecycle dimensions
  -> exact future Terraform interface bindings
  -> price/cost/evidence/owner mappings
  -> bidirectional reconciliation report for I5-10
```

Bindings may name an exact future interface schema/address approved by the amendment, but Issue
#14 never writes Terraform. Adapter and Terraform ownership remain separate.

## Related code files

- Current BOM, Terraform binding, concern and implementation allow-lists: `[]`.
- Exact model/test/ADR files: `TBC` after dependency amendment.
- No `infra/aws/**`, Terraform module, provider lock, environment file or adapter descriptor may
  be created by this issue.

## Tests before

- BOM row with missing/duplicate/stale decision/state/concern/owner/lifecycle link.
- Terraform resource/data source/variable/output binding orphan, duplicate, wildcard or invented
  path.
- State or cost line without BOM; selected Terraform binding without state/cost/concern.
- Unpriced request/transfer/backup/log/key/control/data-source dimension.
- Exclusion without owner/reason/source/expiry or used as zero-rate substitute.
- Deferred/rejected/TBC option contributing selected rows.
- Topology and cost model hashes disagree or stale price snapshot remains bound.

## Refactor

Use stable logical IDs independent of implementation file layout, plus an exact mapping layer for
the later I5-10 schema. Do not build a Terraform parser before I5-10 publishes its interface; use
the exact released contract only.

## Tests after

- All selected state/decision/cost/BOM/concern/Terraform interface graphs reconcile both ways.
- Every stopped/preserve/backup/restore/destroy lifecycle exposes its cost/state effects.
- All exclusions are explicit and expire/reopen correctly.
- One compact topology/BOM projection is suitable for human/FinOps review without account data.
- Any change to decision/state/price/concern hash invalidates reconciliation.

## Regression gate

```text
make state-matrix-check
make cost-model-check
make aws-decision-check
```

Future I5-10 composition commands are not guessed or run here.

## Implementation steps

1. Import the exact released Issue #11 concern map and accepted ADR/state/cost hashes.
2. Define logical BOM lifecycle rows for selected options only.
3. Map every state and cost row to BOM; add explicit reviewed exclusions where applicable.
4. Bind each BOM row to exact future I5-10 resource/data source/variable/output interfaces from
   an approved schema, not guessed paths.
5. Implement bidirectional orphan/duplicate/stale reconciliation and hash invalidation.
6. Emit a safe, account-free topology/BOM review projection with residual costs visible.
7. Re-run all upstream gates after any reconciliation correction.

## Success criteria

- [ ] No selected BOM/state/cost/concern/Terraform interface row is orphaned or duplicated.
- [ ] Every selected future resource/data source is priced or explicitly excluded with evidence.
- [ ] No actual Terraform resource/path is invented before its released interface exists.
- [ ] Residual stopped/preserved costs and recovery dependencies remain visible.
- [ ] Handoff to I5-10 is exact, non-applying and account-free.

## Risk assessment

Premature resource naming can freeze an invalid topology or overlap I5-10 ownership. Mitigation is
logical stable IDs plus exact released interface mapping. Rollback invalidates the BOM projection
and reopens affected ADRs; it does not modify Terraform or cloud state.

## Security considerations

Never include account IDs, ARNs, VPC/subnet addresses, state bucket names, resource names or
secrets in tracked models/evidence. The future mapping is schema-level until separately authorized
environment inputs are supplied.

## Next steps

Phase 7 performs the complete offline gate, evidence/rollback proof and exact human handoff.
