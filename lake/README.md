# Lake profile: MinIO + Lakekeeper + Iceberg

DuckDB Iceberg writes require an Iceberg REST catalog; writing directly to a raw MinIO path is not enough. This repo uses Lakekeeper as the REST catalog for the optional `lake` profile.

## Start services

```bash
make lake-up
```

Services:

- MinIO API: http://localhost:9000
- MinIO console: http://localhost:9001
- Lakekeeper catalog: http://localhost:8181

## Publish marts

Run the core pipeline first:

```bash
make seed SCALE=small SEED=42
make load
make dbt
```

Then publish marts to Iceberg:

```bash
make lake-publish
```

`lake/publish_iceberg.py` loads DuckDB `iceberg` and `httpfs` extensions, creates the Lakekeeper `retail` warehouse if it doesn't exist yet (a fresh `lake` profile has none), attaches the Lakekeeper REST catalog, writes each curated asset from `lake/curated_assets.json` to `lake.retail.*`, then performs a read-back count smoke test.

### ATTACH details (why the options matter)

The `ATTACH ... (TYPE iceberg, ...)` call needs three options beyond `ENDPOINT`, each addressing a real failure mode observed against this pinned Lakekeeper v0.13.1 + MinIO stack:

- `AUTHORIZATION_TYPE 'none'` — the DuckDB `iceberg` extension defaults to `oauth2` and refuses to attach without a secret/client credentials otherwise, even though this local Lakekeeper deployment has no auth configured.
- `ACCESS_DELEGATION_MODE 'none'` — the extension's default (`vended_credentials`) asks Lakekeeper for storage credentials/locations per request; against this stack it produced unsigned S3 requests that MinIO rejects with `403 Forbidden`. `'none'` makes DuckDB use this script's own `lake_s3` secret directly for all reads/writes instead.
- `READ_ONLY false` (publish only) — the main DuckDB connection opens `warehouse/retail.duckdb` read-only (single-writer discipline); that read-only mode otherwise propagates to the attached Iceberg catalog and blocks `CREATE SCHEMA`/`CREATE TABLE`.

Also: the extension doesn't support `CREATE OR REPLACE TABLE` for Iceberg tables, so re-publishing does `DROP TABLE IF EXISTS` then `CREATE TABLE`.

### Warehouse auto-provisioning

Lakekeeper's Iceberg REST catalog protocol (what `ATTACH` speaks) does not auto-create warehouses — they only exist once created via Lakekeeper's separate management API. `publish_iceberg.py` checks for the `retail` warehouse via that API and creates it if missing, so `make lake-up` followed directly by `make lake-publish` works with no manual bootstrap step. The warehouse's storage-profile endpoint is intentionally the Compose service DNS name (`http://minio:9000`, overridable via `LAKEKEEPER_STORAGE_ENDPOINT`) rather than `LAKE_S3_ENDPOINT`, because Lakekeeper itself always runs as a container and needs a container-network-resolvable address for its own storage validation — independent of whether `publish_iceberg.py` is invoked from the host or from inside a container.

## Curated asset list

`lake/curated_assets.json` is the single source of truth for what gets published to Iceberg. It is a plain JSON data file (not a Python module), read by absolute path derived from each consumer's own `__file__` so every consumer works standalone regardless of `cwd` or `sys.path`. The same file is also read by `serving/export_marts_snapshot.py` (Rill export, Phase 3) and the OpenMetadata Iceberg ingestion YAML renderer (Phase 6), so the published, exported, and cataloged asset sets cannot drift from each other.

It currently lists all 11 `main_marts` business marts built by the dbt project:

- `mart_daily_revenue`
- `mart_top_products`
- `mart_customer_cohorts`
- `mart_fulfillment_performance`
- `mart_returns_analysis`
- `mart_promotion_effectiveness`
- `mart_channel_geography`
- `mart_inventory_health`
- `mart_web_funnel_conversion`
- `mart_supplier_purchasing`
- `mart_data_quality`

Core dimension/fact tables (`dim_customers`, `fct_orders`, etc.) are deliberately **not** included. The issue prefers a curated, business-facing mart set over raw core tables for the Iceberg/catalog demo, 11 marts already comfortably exceeds the ≥8 floor, and adding core tables would only add surface area without adding explainability for a demo audience. If a future need justifies exposing a core table (e.g. a specific OpenMetadata lineage story that a mart alone can't tell), add it to `curated_assets.json` with its `main_core` schema and document the reason here.

## Read-back verification

`read_back()` is strict: it counts rows for every asset in `curated_assets.json` and raises immediately (non-zero exit) if any asset is missing from the `lake.retail` namespace or has a row count of 0. Successful output looks like:

```text
Write->read-back smoke test:
  lake.retail.mart_daily_revenue: 365 rows
  lake.retail.mart_top_products: 492 rows
  ...
```

Use `--read-back-only` to run just the read-back check against already-published assets, without re-publishing (used by the Airflow `iceberg_read_back` task):

```bash
.venv/bin/python3 lake/publish_iceberg.py --read-back-only
```

Use `--skip-read-back` to publish without running the read-back check.

## Resource note

The `lake` profile is opt-in. On MacBook M1 Pro 16GB, run it separately from the `governance` profile.
