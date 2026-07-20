---
phase: 11
title: "AWS Analytics BI Governance and Iceberg Adapters"
status: pending
priority: P1
dependencies: [7, 9]
effort: "L"
---

# Phase 11: AWS Analytics BI Governance and Iceberg Adapters

<!-- Updated: Validation Session 1 - pinned shared divergence contracts and removed Terraform ownership overlap. -->

## Overview

Build and contract-test the AWS-facing adapters for S3/Iceberg catalog, disposable ClickHouse
projection, Superset, OpenMetadata and durable metadata/search dependencies. Use local/disposable
or mocked infrastructure by default; real AWS compatibility/restore tests remain separately
credential- and authorization-gated. No cloud resource is created here.

## Context Links

- Phase 9 state/decision interfaces; Phase 10 Terraform outputs
- Existing `lake/`, `serving/rill/`, `governance/openmetadata/`, data contracts
- Source register S09-S16
- PH-C03/C04, PH-H04/H05/H09 and SC-05/07/10/18

## Requirements

- Preserve DuckDB/Rill local path and define exact shared versus platform-specific contracts.
- Consume the exact Phase 1/P7 versions of `local-aws-data-product-equivalence-v1.yaml`,
  `iceberg-lifecycle-v1.yaml`, and `openmetadata-asset-identity-v1.yaml`; an AWS deviation requires
  a versioned ADR and cannot silently fork learning/data/evidence semantics.
- Validate current client compatibility before accepting Glue Iceberg REST: writer, ClickHouse,
  OpenMetadata, auth, v1/v2 create/read/evolve/time-travel/rename/delete/recovery.
- Implement ClickHouse projection hydration/readiness with empty-start, interrupted retry,
  idempotency and row/schema/query/metric equivalence.
- Keep S3/Iceberg as durable truth under disposable hypothesis. Do not declare ready before
  equivalence/SLO.
- Superset task is stateless; metadata DB backup/restore and dashboard/datasource verification are
  explicit. Cache/broker exists only if selected features require it.
- OpenMetadata server is replaceable; DB authority and search rebuild/snapshot are explicit.
  Validate supported current version/DB/search path before pinning.
- Portal adapters expose absent/starting/hydrating/ready/degraded/error and deep links using shared
  vocabulary.
- All AWS credentials/real lifecycle tests are opt-in, account-bound, least-privilege and
  non-default. No apply is authorized.

## Architecture

Adapter interfaces:

```text
IcebergCatalogAdapter: lifecycle/current-pointer
AnalyticsProjectionAdapter: hydrate/status/query/equivalence/reset
BIAdapter: datasource/dashboard/status/export/restore-check
GovernanceAdapter: ingest/reconcile/search/status/restore-check
```

Local implementations remain Lakekeeper/DuckDB/Rill/OpenMetadata. AWS implementations target
Glue REST/S3, ClickHouse, Superset and OpenMetadata with Phase 9-selected durable dependencies.
Contracts expose divergence instead of pretending identical topology/auth.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `platform/adapters/contracts/**` | 500-800 LOC | Engine-neutral interfaces/vectors |
| Create | `platform/adapters/aws/{iceberg,clickhouse,superset,openmetadata}/**` | 1,800-2,800 LOC | AWS adapters/config |
| Create | `platform/images/{clickhouse-hydrator,superset,openmetadata}/**` | 500-900 lines | Reproducible images/health |
| Create | `tests/adapters/{iceberg,analytics,bi,governance}/**` | 1,500-2,200 LOC | Lifecycle/equivalence/recovery |
| Create | `tests/fixtures/engine-equivalence/**` | 300-500 lines | Null/timezone/type/query/metric vectors |
| Create | `scripts/aws/{hydrate-clickhouse,verify-aws-adapters}.py` | 500-800 LOC | Readiness/evidence |
| Modify | Portal status adapter registry | bounded | AWS tool states |
| Create/modify | Adapter-owned deployment descriptors under `platform/adapters/aws/**` only | bounded | Validate against read-only Phase 10 output schema; never edit Terraform paths |
| Modify | version/compatibility docs and ADRs | 200-350 lines | Pin evidence |

## Interface Checklist

- [ ] Iceberg lifecycle/auth/capability matrix
- [ ] projection hydration checkpoint/idempotency/readiness
- [ ] query/schema/metric equivalence assertion IDs
- [ ] Superset asset export/import and metadata restore verifier
- [ ] OpenMetadata DB restore/search rebuild/reconcile verifier
- [ ] adapter status/deep-link/problem mapping
- [ ] version/cost/source evidence and exit path

## Dependency Map

- Depends on Phase 7 local contract evidence and Phase 9 accepted interfaces; can consume Phase
  10 outputs read-only when present.
- Reuses Phase 1/7 data contracts.
- Does not block local release. Blocks any AWS readiness claim and optional cloud AI.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Empty ClickHouse after EC2 zero | Hydrate from current Iceberg; equivalence before ready |
| Critical | Hydration interrupted/retried | Idempotent resume/restart; no duplicate/partial ready |
| Critical | Catalog pointer/object mismatch | Fail loud; recover/rollback |
| Critical | Metadata backup corrupt | Empty restore test fails readiness; previous good retained |
| High | DuckDB/ClickHouse null/timezone/type/metric divergence | Contract fails or versioned deviation ADR |
| High | Glue/client/auth operation unsupported | Catalog candidate rejected; no topology freeze |
| High | Superset/OpenMetadata server restarts without metadata/search | Restore/rebuild verifier |
| High | External UI starting/error | Portal remains usable with accurate status |

## Tests Before

Encode local DuckDB/Rill/Iceberg/OpenMetadata outputs as engine-neutral vectors; add unsupported
catalog/auth, interrupted hydration, empty metadata, corrupt backup and stale search fixtures.

## Refactor

Extract adapter contracts without moving/changing local business logic. Implement AWS adapters
behind separate packages/images/config. Any current-version upgrade gets characterization and
rollback.

## Tests After

Run local disposable ClickHouse/Superset/OpenMetadata one at a time, contract/equivalence/fault
tests and mock catalog auth/lifecycle. Real Glue/S3 and empty-environment restore drills wait for
explicit account/resource authority and record exact cost/region/version.

## Regression Gate

```bash
make aws-adapters-contract
make engine-equivalence
make metadata-contracts-check
make data-contracts-check
make golden-clean PROFILE=small SEED=42
```

## Implementation Steps

1. Write engine-neutral contract/failure fixtures from local golden outputs.
2. Spike exact ClickHouse/dbt/Iceberg, OpenMetadata and Superset versions locally.
3. Implement S3/catalog adapter and retain Glue acceptance as credential-gated gate.
4. Implement ClickHouse hydration/readiness/equivalence adapter.
5. Implement Superset asset/metadata and OpenMetadata DB/search adapters.
6. Add portal status/deep links and evidence.
7. Run local/mocked suites; update ADRs with supported/unsupported operations and retained apply
   blockers.

## Success Criteria

- [ ] Local path remains green and contract-authoritative.
- [ ] ClickHouse disposable hypothesis has measurable local admission evidence or is rejected.
- [ ] Catalog, Superset and OpenMetadata persistence/recovery contracts are explicit.
- [ ] Cross-engine deviations cannot be silent.
- [ ] No AWS resource, apply or unsupported “validated” claim occurs.

## Risk, Security, and Rollback

Vendor versions/auth/topologies change. Pin only after spikes, keep credentials outside evidence,
and bind real tests to approved account/region. Rollback disables AWS adapters and restores local
adapter/version; durable data remains S3/Iceberg only after future accepted deployment.

## Next Steps

Once human apply gates clear in a separate authorized issue, run real catalog/restore/readiness
tests before any AWS release. Phase 12 consumes only governed, admitted products.
