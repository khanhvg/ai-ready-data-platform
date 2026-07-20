# Governance profile: OpenMetadata catalog/lineage

The `governance` profile (`make catalog`) only starts OpenMetadata's own containers
(MySQL, Elasticsearch, server). It does not, by itself, ingest any metadata from this
project -- OpenMetadata starts empty. This directory holds the ingestion workflows that
populate it: one for the **physical** Iceberg tables published by Phase 4/5, one for the
**logical** dbt model graph from Phase 2.

## Two services, two views of the same marts

- **`retail_iceberg`** -- physical. Crawled live via OpenMetadata's Iceberg connector
  (RestCatalog against Lakekeeper + S3 fileIO against MinIO). Shows the ≥8 curated
  Iceberg tables published by `lake/publish_iceberg.py`, under namespace `retail`.
- **`retail_duckdb`** -- logical. Not a live crawl (OpenMetadata has no native DuckDB
  connector). Shows the full `stg_*` / `int_*` / `fct_*` / `dim_*` / `mart_*` dbt graph
  with lineage, descriptions, and tests sourced from dbt's own `manifest.json` +
  `catalog.json` (Phase 2).

A curated mart (e.g. `mart_daily_revenue`) therefore shows up in **both** views:
`retail_iceberg.default.retail.mart_daily_revenue` (the published Iceberg table) and
`retail_duckdb.retail.main_marts.mart_daily_revenue` (the dbt model, with its full
upstream lineage). OpenMetadata does not auto-link the two -- no cross-service lineage
edge is fabricated between them; they are deliberately separate catalog entries
representing the physical asset and the transformation that produced it.

## Why Iceberg ingestion needs `lake` + `governance` together (R2)

The Iceberg connector must reach both Lakekeeper (the REST catalog) and MinIO (the
table data) live, so `governance` has to be up *at the same time* as `lake` -- the one
new resource conflict on a 16GB machine. This is resolved with a guarded, explicit
opt-in co-run window, not by relaxing the default guards:

```
make catalog-ingest
```

This target (see `Makefile`):

1. Stops `orchestration` (Airflow) first, so the peak is never all three heavy profiles
   at once.
2. Starts `lake` + `governance` together (bypassing the default mutual-exclusion guard
   -- only this target does).
3. Waits for `lakekeeper` and `openmetadata-server` to report healthy.
4. Installs `openmetadata-ingestion[iceberg,dbt]` in the venv (first run only).
5. Runs `render_iceberg_ingestion.py --check` -- fails loudly if the committed
   `iceberg_ingestion.yaml` table filter has drifted from `lake/curated_assets.json`.
6. Publishes the curated Iceberg assets (`lake/publish_iceberg.py --skip-read-back`; the
   DuckDB warehouse from `make dbt` must already exist).
7. Runs the Iceberg ingestion workflow.
8. Bootstraps the `retail_duckdb` service (see below) and runs the dbt ingestion
   workflow.
9. Runs `verify_catalog.py` and prints the summary.
10. Tears down `lake`, leaving `governance` up so you can browse the result at
    http://localhost:8585. Run `make down` afterwards to stop `governance` too.

**Prerequisite:** export a real ingestion-bot JWT first (`make catalog-ingest` fails
loudly otherwise):

```bash
make catalog                       # start governance alone first, just to mint the token
# UI: http://localhost:8585 (admin/admin) -> Settings -> Bots -> ingestion-bot -> generate token
# or via API:
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8585/api/v1/users/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@open-metadata.org","password":"YWRtaW4="}' | python3 -c \
  'import sys,json;print(json.load(sys.stdin)["accessToken"])')
BOT_ID=$(curl -s http://localhost:8585/api/v1/bots/name/ingestion-bot \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -c \
  'import sys,json;print(json.load(sys.stdin)["botUser"]["id"])')
export OPENMETADATA_JWT_TOKEN=$(curl -s "http://localhost:8585/api/v1/users/token/$BOT_ID" \
  -H "Authorization: Bearer $ADMIN_TOKEN" | python3 -c \
  'import sys,json;print(json.load(sys.stdin)["JWTToken"])')
make down                          # stop the solo governance instance...
make catalog-ingest                # ...catalog-ingest starts lake+governance together
```

Never commit this token -- it is read from the environment only (`OPENMETADATA_JWT_TOKEN`
is a placeholder in `.env.example`).

### Measured memory (2026-07-10, M1 Pro 16GB, Airflow stopped)

Actual container RSS during the co-run window (well under the `mem_limit` ceilings,
which sum to ~7.5g of headroom -- these are the real numbers, not the ceiling):

| Container | Measured | Limit |
|---|---|---|
| openmetadata-server | ~1.1g | 2g |
| openmetadata-search (ES) | ~0.9g | 1g |
| openmetadata-db (MySQL) | ~0.4g | 1g |
| lakekeeper | ~0.03g | 1g |
| minio | ~0.1g | 1g |
| lakekeeper-db | ~0.04g | 0.5g |

Total ≈ **2.6g** actual RSS for the co-run window, plus Docker Desktop/macOS overhead.
This is comfortably inside 16GB with Airflow stopped -- the `~11g` figure in the plan
was the container `mem_limit` ceiling sum, not a measured peak.

## Why dbt ingestion needs a bootstrap step first

OM 1.6.5's dbt connector **enriches** Table entities that already exist in the catalog
(it looks each dbt model up via `es_search_from_fqn`); it does not create them. Since
there is no native DuckDB connector to crawl `retail_duckdb` live, `metadata ingest -c
dbt_ingestion.yaml` against an empty/missing service completes with 0 errors but attaches
nothing (confirmed empirically). `governance/openmetadata/ingestion/bootstrap_dbt_service.py`
is the required prerequisite: it creates the `retail_duckdb` Custom Database service (if
absent) and one Table entity per materialized dbt model, with real columns read from
dbt's own `catalog.json` (itself produced from a live `information_schema` query against
the DuckDB warehouse) -- no fabricated schema. `make catalog-ingest` runs this
automatically before the dbt ingestion step.

Six `int_*` intermediate models are dbt `ephemeral` (inlined CTEs, never materialized),
so they have no `catalog.json` entry and are skipped by the bootstrap script. OM's dbt
connector still logs a benign `Unable to find the node or columns in the catalog file`
warning for each when it walks their `ref()` edges -- expected, not an error; lineage
still connects correctly through them to the physical parent/child models.

## Running the ingestion workflows manually (iteration / debugging)

With `lake` + `governance` already up and `OPENMETADATA_JWT_TOKEN` exported:

```bash
# Table filter must match lake/curated_assets.json (Phase 4's source of truth)
.venv/bin/python3 governance/openmetadata/ingestion/render_iceberg_ingestion.py --check

MINIO_ROOT_USER=minioadmin MINIO_ROOT_PASSWORD=minioadmin_local_only \
  .venv/bin/metadata ingest -c governance/openmetadata/ingestion/iceberg_ingestion.yaml

REPO_ROOT=$(pwd) .venv/bin/python3 governance/openmetadata/ingestion/bootstrap_dbt_service.py
REPO_ROOT=$(pwd) .venv/bin/metadata ingest -c governance/openmetadata/ingestion/dbt_ingestion.yaml

.venv/bin/python3 governance/openmetadata/verify_catalog.py
```

`render_iceberg_ingestion.py` (no flags) regenerates `iceberg_ingestion.yaml`'s table
filter from `lake/curated_assets.json` in place if you add/remove a curated asset.

## Real, measured evidence (2026-07-10 run)

```
$ .venv/bin/metadata ingest -c governance/openmetadata/ingestion/iceberg_ingestion.yaml
Workflow Iceberg Summary: Processed records: 14  Errors: 0  Success %: 100.0

$ .venv/bin/metadata ingest -c governance/openmetadata/ingestion/dbt_ingestion.yaml
Workflow dbt Summary: Processed records: 252  Errors: 0  Success %: 100.0

$ .venv/bin/python3 governance/openmetadata/verify_catalog.py
OpenMetadata catalog summary:
  retail_iceberg (physical Iceberg tables): 11 table(s)
  retail_duckdb (logical dbt models):         45 table(s)
  retail_duckdb lineage edges:                 130
```

## What this does NOT give you (by design, kept lightweight)

- No live DuckDB table stats, sampling, or profiling for `retail_duckdb` -- there's no
  DuckDB connector; column types come from dbt's `catalog.json` at bootstrap time, not a
  live query.
- No cross-service lineage edge between `retail_iceberg` and `retail_duckdb` -- see
  "Two services, two views" above.
