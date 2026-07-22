---
phase: 3
title: "Topology Persistence Options and ADRs"
status: pending
priority: P1
dependencies: [2]
effort: "L"
---

# Phase 3: Topology Persistence Options and ADRs

## Context links

- [Required option analysis](./decision-state-and-cost-contract.md#required-option-analysis)
- [Official behavior-source candidates](./current-source-inventory.md#official-behavior-source-candidates)
- [Concern crosswalk status](./requirements-and-risk-traceability.md#concern-crosswalk-status)

## Overview

Produce evidence-driven option rows and ADRs for topology, segmentation and persistence. Services
enter a selected design only when an exact released concern/NFR and measurable failure boundary
require them. No Terraform resource path or compatibility claim is created here.

## Requirements

- Functional: FR-003..009.
- Non-functional: NFR-002/005..008/012..014.
- Compare forces/trade-offs, state/cost/security/recovery consequences and exit/migration.
- Current mutable product documentation must be refreshed at implementation time and pinned to
  exact tested versions before `selected`.
- NAT/endpoints/load balancer/EBS/EFS/RDS/OpenSearch/cache/workflow/AgentCore are optional
  candidates, not a reference architecture checklist.

## Architecture

```text
released concerns + state obligations + failure/NFR forces
  -> bounded option scorecards -> compatibility/recovery/cost evidence
  -> selected/rejected/deferred/blocked-tbc ADR outcome
  -> candidate topology interfaces (not Terraform resources)
```

ECS on EC2 segmentation is evaluated as the user-required topology frame. Durable truth,
replaceable compute, metadata/search authorities and readiness dependencies remain distinct.

## Related code files

- Current implementation allow-list: `[]`.
- Exact ADR/model/test files: `TBC` after Issue #11 release and amendment.
- Candidate docs family: `docs/decisions/aws/**`.
- No Terraform, adapter, architecture-view, portal, runner or lab file belongs to this phase.

## Tests before

- Option missing forces/trade-offs/failure/cost/state/security/recovery/exit evidence.
- Selected option with TBC, no released concern, no owner evidence, or incompatible state row.
- Multiple selected authorities for one scope.
- Service appears in topology/BOM only through symmetry or “best practice.”
- Unsupported/mismatched client/server/catalog/DB/search version promoted to selected.
- Public ingress, static credentials, unfenced writers, local-only durable truth, false-zero or
  destructive-default candidates accepted.

## Refactor

ADRs remain short projections over the canonical option/state models. Do not duplicate matrices
or introduce a generic architecture framework. Reuse only exact released concern IDs.

## Tests after

- All required decision scopes have a valid outcome and explicit reopen trigger.
- Every selected option has complete state/cost/security/recovery and released concern links.
- Every rejected option has evidence-based rejection; every deferred option contributes no BOM.
- Cross-option incompatibilities and double ownership fail.
- Exact versions/compatibility remain `blocked-tbc` unless measured in authorized conditions.

## Regression gate

```text
make state-matrix-check
make aws-decision-check
```

`cost-model-check` begins once Phase 4 has accepted price inputs.

## Implementation steps

1. Refresh official behavior docs and record exact versions/retrieval hashes without calling AWS.
2. Map released concern/NFR forces to each required decision scope.
3. Compare ECS/EC2 segmentation and network-egress/ingress alternatives.
4. Compare ClickHouse durable/disposable/object/managed options against state and recovery tests.
5. Compare S3/Iceberg catalog options with an exact client/auth/operation capability matrix.
6. Compare OpenMetadata DB/search and Superset metadata/cache/session choices against selected
   features and restore/readiness needs.
7. Keep search/workflow/AgentCore and every extra managed service deferred unless exact evidence
   admits it.
8. Record ADR outcomes and migration/exit triggers; do not populate actual Terraform resources.

## Success criteria

- [ ] Option analysis is force/evidence based and complete for every required scope.
- [ ] No service is selected for pattern theater or local/AWS symmetry.
- [ ] Selected outcomes reconcile with Phase 2 state ownership and recovery.
- [ ] Compatibility/version gaps remain explicit `blocked-tbc`.
- [ ] No production, readiness, cost, resource or apply claim is made.

## Risk assessment

Mutable product/version behavior can make a plausible option invalid. Mitigation is exact-version
compatibility evidence, short-lived source provenance, and `blocked-tbc` until tested. Rollback
reopens the ADR, invalidates dependent BOM/cost outputs, and preserves the local platform.

## Security considerations

Network and managed-service convenience can silently broaden data/control exposure. Each option
must enumerate flows, IAM/KMS/config/secret ownership, public IPv4/ingress, logs and deletion.

## Next steps

Phase 4 prices only selected candidates and explicitly costed alternatives; deferred/rejected
services cannot leak into the estimate.
