---
phase: 1
title: "Immutable Golden Baseline and Architecture Contract"
status: pending
priority: P1
dependencies: []
effort: "L"
---

# Phase 1: Immutable Golden Baseline and Architecture Contract

<!-- Updated: Validation Session 1 - made preservation and local/AWS shared contracts exact. -->

## Overview

Freeze the shipped issue #3 behavior at exact main SHA `3cd3d41…`, create a credential-free
clean-checkout command, and define the shared architecture/data/evidence seams before any
refactor or implementation branch fans out.

## Context Links

- [Discovery inventory](./discovery/repository-inventory.md)
- [Prediction and STOP gates](./discovery/prediction-report.md)
- [Architecture decisions](./architecture-decisions.md)
- `README.md`, `Makefile`, `docs/verification/GH-3-full-flow-evidence.md`
- Current contracts: `data-generator/generate.py`, `transform/dbt/`,
  `lake/curated_assets.json`, `serving/rill/`, `orchestration/airflow/`

## Requirements

- Record golden main, reviewed tree, discovery, approved plan and implementation SHAs.
- Preserve 18 CSV schemas, deterministic bytes/checksums, anomaly meanings, dbt warning oracle,
  51-model lineage, 11 mart schemas, curated-list membership, weighted Rill metrics, Airflow task
  graph, logical/physical OpenMetadata identities, and unrelated files.
- Hash and preserve `docs/code-standards.md` byte-for-byte if it exists at the implementation input
  SHA; if absent, record `absent`. Never create, overwrite or delete it in this epic without a
  separate owner decision.
- Add `make golden-clean PROFILE=small SEED=42`; it must work with no prior venv, data, volume or
  cache and emit schema-valid evidence from two runs.
- Key environment rebuild to dependency/lock hashes; do not use the current
  `.venv/bin/python3` sentinel alone.
- Parameterize only the path seams needed for isolated workspaces; characterization tests precede
  every refactor.
- Create the initial Structurizr model/view IDs and contract registries. Do not invent services.

## Architecture

The current data spine remains authoritative. A golden harness runs it in a generated workspace,
captures tool and exact-SHA provenance, validates stable/allowed-drift fields, and writes a
canonical evidence envelope. Shared contracts version behavior; adapters may diverge physically
only when the contract says which results remain equivalent.

Planned golden flow:

```text
clean checkout -> lock-hash environment -> two deterministic fixture dirs
  -> compare 18 CSVs/anomalies -> load DuckDB -> dbt build/docs
  -> export 11 marts -> validate Rill/curated/lineage contracts
  -> canonical evidence.json + artifact hashes -> schema/tamper check
```

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `scripts/golden/run-golden-baseline.py` | 300-450 LOC | Orchestrates bounded clean run/evidence |
| Create | `scripts/golden/environment-fingerprint.py` | 80-150 LOC | Stable tool/lock/SHA capture |
| Create | `requirements/locks/core.txt` and lock-hash stamp contract | generated/managed | Reproducibility |
| Create | `contracts/data/retail-golden-v1.json` | 150-250 lines | Expected schemas/anomalies/marts/metrics |
| Create | `contracts/data/local-aws-data-product-equivalence-v1.yaml` | 150-250 lines | Engine-neutral result/deviation vectors |
| Create | `contracts/data/iceberg-lifecycle-v1.yaml` | 120-200 lines | Local/AWS lifecycle/fault behavior |
| Create | `contracts/data/openmetadata-asset-identity-v1.yaml` | 120-200 lines | Logical/physical/reconciliation identity |
| Create | `learning/contracts/evidence.schema.json` | 150-250 lines | Evidence validation |
| Create | `tests/golden/**`, `tests/contracts/**` | 500-800 LOC | Characterization, clean run, tamper |
| Create | `architecture/structurizr/workspace.dsl`, `architecture/structurizr/includes/**` | 250-400 lines | Model/view ID fitness |
| Modify | `Makefile` | 40-80 lines | Golden/contract/architecture targets |
| Modify | `data-generator/generate.py`, `ingestion/load_raw.py` | narrow seams | Workspace output/input without semantic drift |
| Modify | `serving/export_marts_snapshot.py`, `orchestration/airflow/callables/pipeline.py` | narrow seams | Explicit workspace paths/clean env |
| Modify | `.gitignore` | <30 lines | Keep runtime evidence ignored; allow tracked schemas/locks |
| Preserve | `release-manifest.json`, discovery, issue #3 plan/evidence, `docs/code-standards.md` when present | 0 | Assert byte hash or explicit absent state unchanged |

## Interface Checklist

- [ ] `GoldenRun(profile, seed, workspace, input_sha) -> EvidenceRecord`
- [ ] data-contract IDs for every raw table/anomaly/mart/metric/lineage invariant
- [ ] local/AWS equivalence, Iceberg lifecycle and OpenMetadata identity contract versions
- [ ] canonical evidence serialization and SHA-256 verifier
- [ ] path/config objects rather than implicit repository-root writes
- [ ] make targets are non-interactive, credential-free and discoverable
- [ ] architecture element/view IDs are stable and referenced from traceability

## Dependency Map

- Input: exact shipped main and discovery only.
- Blocks: Phases 3, 4, 7 and every migration/refactor; Phase 2 may prototype in parallel but its
  final score uses this phase's real evidence fixture.
- Does not depend on AWS/AI decisions.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Clean checkout has no venv/data/cache/volume | Bounded golden run recreates inputs and passes |
| Critical | Generator bytes/anomaly or mart/lineage/metric drifts | Named contract assertion fails |
| Critical | Input SHA/tree differs from approved golden | Fan-out/refactor stops with exact mismatch |
| High | Stale dependency environment exists | Lock-hash mismatch forces rebuild |
| High | Evidence/verifier/artifact is tampered | Integrity check rejects completion |
| High | User/discovery/historical file changes during run | Base-tree/allow-list check fails |
| High | Expected dbt warning disappears/becomes error | Warning oracle reports semantic drift |

## Tests Before

- Characterize two generator runs, all anomaly counters, loader counts, dbt result statuses,
  manifest/catalog graph, mart schemas/queries, Rill weighted expressions, curated-list consumers,
  Airflow task IDs/order and OpenMetadata identity counts.
- Add failure fixtures for stale venv, absent generated files, dirty checkout, wrong base,
  tampered evidence, missing tool and unexpected dbt warning.

## Refactor

- Add explicit workspace/output configuration at current entrypoint seams while keeping defaults
  compatible.
- Replace the venv sentinel with a lock-hash stamp/rebuild rule.
- Add golden/evidence/architecture wrappers without changing business SQL or anomaly generation.

## Tests After

- Run twice from clean generated state; compare deterministic outputs and canonical evidence.
- Prove default current commands still work.
- Prove no tracked/unrelated file changes and no credential appears in evidence.
- Mutation tests: change one checksum, anomaly, mart column, Rill weight or lineage ID and see the
  appropriate contract fail.

## Regression Gate

```bash
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make architecture-check
docker compose config --quiet
git diff --check
```

## Implementation Steps

1. Capture immutable SHAs/tree equality and generate the preservation inventory.
2. Write failing characterization and mutation fixtures around every protected contract.
3. Select and commit a reproducible Python lock workflow; key venv recreation to lock hashes.
4. Add isolated path seams one at a time; run characterization after each.
5. Implement the clean golden orchestrator and evidence schema/canonicalization.
6. Add Make targets and architecture skeleton with required local/AWS view IDs.
7. Run two clean bounded executions and retain machine-readable evidence in CI/artifact storage.
8. Record migration/rollback mapping and shared-core ownership.

## Success Criteria

- [ ] Exact SHA/tree/discovery provenance is machine-checked.
- [ ] `make golden-clean` passes twice without pre-existing ignored assets or credentials.
- [ ] Evidence validates, detects tampering, and contains commands/tools/resources/artifact hashes.
- [ ] Current generator/dbt/mart/lineage/Rill/Airflow/Iceberg/OpenMetadata contracts are protected.
- [ ] Workspace seams do not change default behavior.
- [ ] `release-manifest.json`, discovery artifacts, issue #3 plan/evidence,
  `docs/code-standards.md` state and user files are
  unchanged.
- [ ] Rollback to exact main removes only new tracked seams and generated state.

## Risk, Security, and Rollback

Risk: a “testability” refactor changes semantics while preserving counts. Mitigate with byte,
anomaly, lineage, schema, query and metric characterization plus mutation tests. The harness
sanitizes environment output and never captures secrets/absolute personal paths. Rollback reverts
the additive harness/path seams and returns to exact SHA; ignored workspaces are deleted
separately.

## Next Steps

Release shared contract versions to Phases 2-4. Do not authorize implementation fan-out until the
independent readiness audit accepts this baseline contract.
