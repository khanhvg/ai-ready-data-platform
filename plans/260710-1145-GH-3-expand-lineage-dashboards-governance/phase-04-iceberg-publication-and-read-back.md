---
phase: 4
title: "Iceberg publication and read-back"
status: pending
priority: P2
dependencies: [2]
effort: "M"
---

# Phase 4: Iceberg publication and read-back

## Overview

Publish **≥ 8 curated assets** to Iceberg via Lakekeeper/MinIO and verify each with a write→read-back row count. Establish a **single shared curated-asset list** (source of truth) reused by the publisher, the read-back check, the Rill export (Phase 3), and OpenMetadata Iceberg ingestion (Phase 6) so the sets never drift.

## Requirements

- **Functional**
  - Expand `lake/publish_iceberg.py` `MARTS` from 3 to a curated list of **≥ 8** assets. Default set: the 8 core business marts from Phase 2. Optionally include a small number of core assets (`dim_customers`, `fct_orders`) **only if justified** for the catalog demo — document why in `lake/README.md`.
  - Publish selected staging/core assets **only when justified**; the issue explicitly prefers curated marts. Keep the published set curated and explainable.
  - Read-back verification counts rows for **every** published asset (extend the existing `read_back`), and the run fails loudly if any asset is missing or count is 0.
  - Extract the curated-asset list into one place as a **data file** `lake/curated_assets.json` (not a Python module), read by `publish_iceberg.py`, `serving/export_marts_snapshot.py` (Phase 3), and the OpenMetadata Iceberg ingestion YAML renderer (Phase 6). Each consumer resolves the file by an **absolute path derived from its own `__file__`** (`<repo>/lake/curated_assets.json`), so it works when scripts are run standalone (`python lake/publish_iceberg.py`) without relying on `lake` being an importable package or the repo root being on `sys.path`. Record each asset's DuckDB source schema (e.g. `main_marts.mart_x`, `main_core.dim_customers`) so publish and export resolve correctly.

- **Non-functional**
  - Runs only under the `lake` profile (`make lake-up`), single-writer safe (reads `warehouse/retail.duckdb` read-only).
  - Credentials (MinIO keys) come from env; no secrets committed.

## Architecture

```text
warehouse/retail.duckdb (read-only)
   └─ publish_iceberg.py ──ATTACH iceberg via Lakekeeper REST──► MinIO (s3://retail-lake)
        namespace: lake.retail.<asset>
        └─ read_back(): re-attach, SELECT count(*) per asset  (write→read-back smoke test)
```

Keep the existing `ATTACH ... TYPE iceberg, ENDPOINT <lakekeeper>/catalog` + `CREATE SECRET` S3 pattern. Only the asset list and its source-schema resolution change; the connection mechanics are already proven (issue #1 R1 resolved).

### Shared curated-asset contract (sketch)

`lake/curated_assets.json` — the single source of truth, a plain data file read by path (no Python import):

```json
{
  "assets": [
    {"name": "mart_daily_revenue",           "schema": "main_marts"},
    {"name": "mart_top_products",            "schema": "main_marts"},
    {"name": "mart_customer_cohorts",        "schema": "main_marts"},
    {"name": "mart_fulfillment_performance", "schema": "main_marts"},
    {"name": "mart_returns_analysis",        "schema": "main_marts"},
    {"name": "mart_promotion_effectiveness", "schema": "main_marts"},
    {"name": "mart_channel_geography",       "schema": "main_marts"},
    {"name": "mart_inventory_health",        "schema": "main_marts"},
    {"name": "mart_supplier_purchasing",     "schema": "main_marts"}
  ]
}
```

Each consumer loads it via `Path(__file__).resolve().parents[N] / "lake" / "curated_assets.json"` so standalone script execution resolves the path deterministically. Optional core assets (`dim_customers`, `fct_orders`) may be appended only if justified for the catalog demo — documented in `lake/README.md`.

## Related Code Files

- Create: `lake/curated_assets.json` — shared curated-asset list + source schema (data file, read by path).
- Modify: `lake/publish_iceberg.py` — load `curated_assets.json` by `__file__`-relative path; publish + read-back all; fail on missing/zero.
- Modify: `serving/export_marts_snapshot.py` (Phase 3) — load the same JSON by path for exports.
- Modify: `lake/README.md` — updated asset list, justification for any non-mart assets, read-back evidence format.
- Reference (read-only): existing `publish_iceberg.py` ATTACH/secret pattern, `docker-compose.yml` lake services, `versions.md` (Lakekeeper v0.13.1, MinIO pin).

## Implementation Steps

1. Create `lake/curated_assets.json` with the ≥8 curated assets + source schemas.
2. Refactor `publish_iceberg.py` to load the JSON by `__file__`-relative path and iterate the shared list (both `publish` and `read_back`); resolve `<schema>.<asset>`.
3. Make read-back strict: assert every asset present and count > 0; print `lake.retail.<asset>: N rows`.
4. Point Phase 3 export at the same list.
5. `make lake-up`, `make dbt` (data present), `make lake-publish`; capture publish + read-back output for P7 (AC6/AC8).
6. `make down` to release lake resources.

## Success Criteria

- [ ] ≥ 8 curated assets published to `lake.retail.*` (printed list).
- [ ] Read-back reports a non-zero row count for **every** published asset (AC6).
- [ ] Publisher, Rill export, and (Phase 6) OM ingestion all reference the same curated-asset list.
- [ ] Run fails loudly if any asset is missing/zero (negative-path check documented).
- [ ] No MinIO/Lakekeeper credentials committed; env-driven only.

## Risk Assessment

- **R7 (list drift):** mitigated by `lake/curated_assets.json` as the single source of truth, read by path by publisher, Rill export, and the Phase-6 Iceberg-ingestion YAML renderer; a Phase-6 check asserts the rendered YAML matches it.
- **Iceberg write mechanics:** already proven in issue #1; risk is limited to the larger asset count and source-schema resolution. Verify each asset's schema (`main_marts` vs `main_core`) matches Phase 2 output.
- **Resource:** `lake` profile only; do not co-run with `governance` except in the guarded Phase 6 window.
- **Rollback:** revert `publish_iceberg.py`/`curated_assets.json`; drop the `retail` namespace or remove the MinIO bucket via documented cleanup; Docker volumes are ignored/removable.
