---
phase: 7
title: "Data Pipeline Guided Labs"
status: pending
priority: P1
dependencies: [1, 3, 4, 5]
effort: "L"
---

# Phase 7: Data Pipeline Guided Labs

<!-- Updated: Validation Session 1 - placed lab expansion after the runnable journey and pinned shared contracts. -->

## Overview

Turn the preserved retail spine into guided labs for deterministic ingestion, dbt modeling and
quality, orchestration/retry, metrics/BI, Iceberg commit/recovery and OpenMetadata governance.
The labs expose real failure modes without changing golden semantics.

## Context Links

- Existing architecture/docs and `docs/verification/GH-3-full-flow-evidence.md`
- [Curriculum data competencies D01-D06](./curriculum-and-competency-map.md)
- PH-H03/H04/H09/H13 and SC-03/07/09/10/18
- Phase 1 data contracts, Phase 3 lab schema, Phase 4 command registry

## Requirements

- Preserve generator bytes/anomaly meanings, raw/dbt/mart/lineage/metric contracts and existing
  expert commands.
- Reuse the exact Phase 1 `retail-golden-v1.json`. Under a sequential shared-core lease, release
  `local-aws-data-product-equivalence-v1.yaml`, `iceberg-lifecycle-v1.yaml`, and
  `openmetadata-asset-identity-v1.yaml`; local results are the first executable oracle for P11.
- Each lab has starter, controlled failure, reset, verify, solution, evidence and reflection.
- Initial labs:
  1. deterministic grain/anomaly/manifest;
  2. dbt layering and warning-versus-error;
  3. weighted metric correctness and data-product contract;
  4. Airflow stage/retry/idempotency and read-only workspace;
  5. Iceberg staged/atomic-or-rebuild publish and snapshot pointer recovery;
  6. OpenMetadata logical/physical assets plus rename/delete reconciliation.
- Rill remains local BI default; OpenMetadata and MinIO/Lakekeeper remain optional profiles.
- Fail loud on partial publish or stale catalog; never silently “fix” controlled anomalies.
- Reuse the Phase 1 schema and Phase 4 local all-11 staged `CuratedReleaseManifest` behavior;
  extend the same release ID/current-pointer invariant to Iceberg, serving and governance
  consumers.
- Namespace OpenMetadata managed objects by workspace/release, preserve unmanaged entities, and
  reconcile exact FQN/owner/tag/lineage sets rather than counts.
- Use bounded small fixtures by default; `demo-large` is an explicit scale lab.

## Architecture

Labs live outside product SQL and execute through adapter/verifier interfaces. Where current
behavior is unsafe for a lab—non-atomic Iceberg drop/create or Airflow root RW mount—write
characterization/fault tests first, then add a safe staged/workspace seam. Existing direct
workflow remains compatible until migration evidence supports switching defaults.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `learning/labs/data-platform/{determinism,dbt-quality,metric-contract,airflow-recovery,iceberg-commit,metadata-reconcile}/**` | 1,500-2,500 lines | Six labs |
| Create | `scripts/labs/data-platform/**` | 800-1,200 LOC | Typed verifiers/fault injectors |
| Create | `tests/labs/data-platform/**` | 1,200-1,800 LOC | E2E/reset/evidence |
| Create | `tests/data/{metrics,iceberg,metadata,airflow}/**` | 1,000-1,500 LOC | Contract/fault/race |
| Create | `contracts/data/{local-aws-data-product-equivalence-v1,iceberg-lifecycle-v1,openmetadata-asset-identity-v1}.yaml` | 390-650 lines | Sequential shared-core contract release before AWS adapters |
| Modify | `lake/publish_iceberg.py` | bounded | Staged/fail-loud/recovery seam |
| Modify | `governance/openmetadata/ingestion/**`, `verify_catalog.py` | bounded | Reconciliation/reset |
| Modify | `orchestration/airflow/**`, `docker-compose.yml` | bounded | Read-only base/scoped output |
| Create/modify | `mk/issue-5/i5-07.mk` and docs | 50-100 lines | Lab/fault targets via root include |
| Preserve | dbt SQL/YAML, Rill metrics, curated list unless approved contract change | 0 | Golden regression |

## Interface Checklist

- [ ] `DataProductContract` and engine-neutral assertion IDs
- [ ] `CuratedReleaseManifest`/`PublishAttempt` with all 11 assets, staged/current pointer and idempotency key
- [ ] `CatalogReconciler` with namespace, managed marker, adoption/tombstone policy and exact identity/edge set
- [ ] Airflow callable workspace config, no repository RW need
- [ ] lab fault injector scoped to workspace/profile
- [ ] reset/recovery oracle for every lab

## Dependency Map

- Requires golden contracts, lab/evidence schema, runner, and the passing Phase 5 real journey.
- May run alongside Phase 6 with exclusive content/path ownership.
- Feeds Phase 8 resource profiles and Phase 11 cross-engine/AWS adapters.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Generator/refactor semantic drift | Golden fails on bytes/anomalies/schema/lineage |
| Critical | Reset during publish | Serialize or recover previous/current snapshot; no false success |
| Critical | Object write succeeds, catalog commit times out | Idempotent resume/rollback and explicit not-ready |
| Critical | Failure after any of 11 projection writes | No consumer sees a mixed release; prior release stays current |
| Critical | Direct Make/Airflow mutation overlaps runner | Shared namespace fence serializes or refuses the mutation |
| High | Metric aggregate reintroduces unweighted average | Query/metric contract fails |
| High | dbt expected warning treated as error/ignored | Warning oracle/remediation distinguishes it |
| High | Model rename/delete leaves stale metadata | Reconcile/reset test proves expected catalog |
| High | Airflow task writes base repo | Negative mount/write test |
| High | Corrupt backup/read-back | Restore/rebuild verifier blocks ready |

## Tests Before

Characterize existing commands, Rill expressions, Airflow graph/mount behavior, Iceberg
drop/create fault window and OpenMetadata rename/delete behavior. Write learner E2E that initially
fails for controlled reasons.

## Refactor

Add lab-safe adapters, workspace paths, staged publish/recovery and catalog reconciliation only
where tests prove a real failure. Keep current asset names and old adapter available for rollback.

## Tests After

Run each lab start→failure→diagnose→reset→verify→evidence; inject boundary faults/races; rerun
golden/data contracts; validate optional profile absent behavior.

## Regression Gate

```bash
make data-contracts-check
make data-labs-e2e
make lake-fault-test
make metadata-reconcile-test
make runner-race-test
make golden-clean PROFILE=small SEED=42
```

## Implementation Steps

1. Write lab manifests and failing E2E/fault fixtures for six bounded labs.
2. Implement deterministic/data-model/metric labs using current behavior.
3. Add Airflow workspace/read-only protection and recovery lab.
4. Add Iceberg staged/rebuild publication contract and fault lab.
5. Add OpenMetadata reconcile/reset manifest and rename/delete lab.
6. Connect verifiers/evidence/deep links and remediation.
7. Run golden regressions, optional-tool absent paths and profile handoff to Phase 8.

## Success Criteria

- [ ] Six hands-on labs satisfy the full contract and deterministic evidence.
- [ ] Existing golden data, marts, lineage, metrics and direct workflows remain compatible.
- [ ] Iceberg partial publish and metadata staleness are observable/recoverable.
- [ ] Airflow learner execution cannot edit the repository.
- [ ] No Kafka/Spark/Flink/Kubernetes or duplicate BI engine is added without a lesson gate.

## Risk, Security, and Rollback

Fault injection must never target the base checkout or non-lab volumes. Use disposable workspaces
and explicit profile names. Rollback switches adapters to the preserved direct path, restores
previous snapshot/catalog manifest and removes new lab content without deleting learner evidence.

## Next Steps

Phase 8 measures every admitted lab/profile combination. Phase 11 reuses the data-product
contract, not local topology.
