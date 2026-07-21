# Data Architecture and Recovery

## Nguyên tắc

Issue #6 là immutable oracle. Labs tạo state mới trong private run root; không sửa golden SQL,
views, fixture, contract semantics hoặc repository data. Migration additive-first, reader N-1 còn
hoạt động và mỗi switch có prior complete rollback point.

## Planned flow

```text
read-only Issue #6 inputs/readers
        |
        v
private run root (starter -> task -> controlled failure)
        |
        +--> raw/warehouse/dbt/export state scoped by run ID
        |
        v
immutable release staging for exactly 11 assets
        |
        v
validated CuratedReleaseManifest + canonical manifest SHA-256
        |
        v
single atomic current-pointer transition (old OR complete new)
        |
        +--> local Iceberg snapshot/catalog commit + read-back/conflict/orphan oracle
        |
        +--> exact OpenMetadata managed namespace/FQN set reconcile
        |
        v
immutable evidence artifacts -> hash index -> tested-tree/dependency/content/verifier binding
```

Exact storage/API operations are unresolved until #8/#9 and the serialized pipeline lease are
released. The diagram states invariants, not an invented API.

## Data authorities

| Authority | Owner | Allowed mutation | Reader behavior |
|---|---|---|---|
| Golden generator/dbt/marts/Rill/fixtures/contracts | Issue #6 | None in Issue #12 without new exact serialized lease | Read-only characterization and verification |
| Lab workspace | Issue #12 run | Run-scoped data, starter/solution copy, generated artifacts | Only released #9 runner/workspace reader |
| Curated staged release | Issue #12 under data lease | Immutable new release; exact 11-set only | Invisible until manifest validates and pointer switches |
| Current pointer | Serialized publisher | One atomic transition | Reader sees prior or complete new; never mixed |
| Iceberg/catalog | Run namespace + admitted seam | Exact run-owned snapshot/object operations | Snapshot/version precondition and read-back required |
| OpenMetadata | Exact managed namespace/FQN set | Policy-driven create/update/delete of managed objects only | Unmanaged and neighboring namespace preserved |
| Evidence | Issue #12 run | Append new immutable run artifacts/index | Tamper/replay/tree mismatch rejects completion |

## Exact eleven-asset invariant

Consume the Issue #6 ordered IDs and `CuratedReleaseManifest` reader unchanged. Every new release:

- has exactly eleven unique assets in the current order;
- binds one release/data-run/tested-tree/lock/contract/engine identity;
- includes logical/physical identity, schema hash, logical content hash, row count and immutable
  staged locator per asset;
- validates canonical manifest SHA-256 before pointer transition;
- retains prior complete manifest/pointer long enough to prove rollback;
- never uses “11 loop iterations succeeded” as atomicity evidence.

## Crash and concurrency boundaries

Fault matrix must cover before/after each meaningful boundary, including every asset write,
manifest finalization, pointer switch, object-store write, Iceberg catalog commit, OpenMetadata
mutation and evidence-index finalization. Required result:

- pre-switch crash: current remains prior complete release; new run state is resumable or
  quarantined;
- post-switch crash: current resolves to complete/hash-valid new release; retry is idempotent;
- stale writer: loses with explicit conflict or is prevented by the admitted serialized writer;
- unknown ownership: cleanup refuses;
- evidence crash: no completion until index and every artifact hash verify.

## Iceberg recovery

Stage B first records exact local object-store/catalog versions and empirically verifies commit,
snapshot visibility, conflict behavior and orphan listing/deletion semantics. No semantics are
assumed from product names or docs alone.

Recovery policy:

1. Bind attempt to expected base snapshot/catalog state.
2. Stage objects under run-owned scope.
3. Commit through the verified catalog primitive.
4. Read back exact asset identities/content/schema/rows against manifest.
5. On conflict, do not overwrite winner; retry only after re-read with the same immutable input.
6. Orphans are listed and cross-checked against run ownership; delete only exact run-owned bytes.
7. Retain prior snapshot/pointer until rollback rehearsal passes.

If the actual local catalog lacks a required conflict/atomic primitive, implementation must stay
single-writer under the admitted lease and document the limitation; it may not claim concurrent
atomicity.

## OpenMetadata reconciliation and rollback

Expected state is an exact set, not a count:

- canonical namespace and exact FQNs;
- managed marker/ownership policy derived from released contracts;
- exact owner/tag/lineage/asset identity set;
- explicit create/update/delete policy;
- deletion allowed only for exact previously managed members of this run namespace;
- no prefix/glob/broad-service deletion or adoption of unmanaged entities.

Two identical reconcile runs must produce the same state. Collision namespace and unmanaged
sentinels must survive. On interrupted reconcile, journal/manifest replay either completes the
same target set or restores the prior managed set; count-only “looks right” evidence is invalid.

## Reset and cleanup

Reset is not repository clean. It must:

1. Acquire the released workspace/operation fence.
2. Preserve immutable evidence and prior complete release unless explicit evidence deletion is a
   separately authorized operation.
3. Replace starter workspace atomically.
4. Remove only bytes/objects/entities whose ownership descriptor matches the exact run.
5. Refuse symlink/hardlink, FIFO/socket/device/other special file, unknown marker, mismatched
   device/inode/namespace/FQN or foreign sentinel before read/write/delete.
6. Re-run post-reset oracle and protected hash scan.

## Resource profile

- Core labs: serial, 16GB-safe, local Python/DuckDB/dbt/Rill readers, no Docker/cloud prerequisite.
- Optional real-service labs: one heavy profile at a time. Absence/error is a typed environmental
  state, never a controlled failure or pass.
- Publication of Iceberg/OpenMetadata lab as verified requires retained evidence from actual
  local services; Docker is one possible runtime only if the amended dependency contract names it.
