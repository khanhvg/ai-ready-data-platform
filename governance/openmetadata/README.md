# Governance profile: OpenMetadata catalog/lineage

The `governance` profile (`make catalog`) only starts OpenMetadata's own containers
(MySQL, Elasticsearch, server). It does not, by itself, ingest any metadata from this
project -- OpenMetadata starts empty. This directory holds the minimal, manual ingestion
step that pulls dbt-generated lineage into it.

There is no native DuckDB connector in OpenMetadata (see `versions.md`), so this sandbox
does not do a live warehouse crawl. Instead it ingests the dbt artifacts
(`transform/dbt/target/manifest.json` + `catalog.json`), which is the supported path for
getting model/column descriptions and lineage out of a dbt project into OpenMetadata.

## What this gives you

- Model and column-level lineage between `stg_*` staging models and `mart_*` marts,
  derived from dbt's own dependency graph.
- Descriptions/tests already written in the dbt YAML files (`_staging__models.yml`,
  `_marts__models.yml`) surfaced as OpenMetadata table/column descriptions.

## What this does NOT give you (by design, kept lightweight)

- No live DuckDB table stats, sampling, or profiling -- there's no DuckDB connector.
- No automatic linkage to the underlying `raw.*`/`main_staging.*`/`main_marts.*` DuckDB
  tables unless you first register a **Database Service** for them in the OpenMetadata UI
  (e.g. a "Custom Database" service named to match `serviceName` below). Without that
  service existing, the dbt ingestion still runs and creates lineage/description
  metadata, but it will not resolve against a previously-crawled table.

## Steps (manual, one-time setup)

1. Start the profile: `make catalog` (do not run this alongside `make lake-up`; see
   `docs/demo-runbook.md`). Open http://localhost:8585 (default `admin` / `admin`).
2. In the OpenMetadata UI, create a Database Service so dbt lineage has something to
   attach to (Settings -> Services -> Databases -> Add -> "Custom Database"). Name it
   to match `serviceName` in `ingestion/dbt_ingestion.yaml` (default: `retail_duckdb`).
3. Generate dbt's catalog artifact (the Makefile's `make dbt` only runs `run`/`test`,
   not `docs generate`):

   ```bash
   cd transform/dbt && ../../.venv/bin/dbt docs generate --profiles-dir .
   ```

4. Get an ingestion-bot JWT token from Settings -> Bots -> ingestion-bot, and export it:

   ```bash
   export OPENMETADATA_JWT_TOKEN=<token>
   ```

5. Run the ingestion workflow from the venv (installs the OpenMetadata ingestion
   framework's dbt extra on first use):

   ```bash
   .venv/bin/pip install --quiet "openmetadata-ingestion[dbt]"
   .venv/bin/metadata ingest -c governance/openmetadata/ingestion/dbt_ingestion.yaml
   ```

6. In the UI, open the Database Service and confirm dbt-sourced lineage/descriptions
   appear on the `stg_*`/`mart_*` entities.

This is a manual, opt-in step for exploring OpenMetadata's dbt ingestion path -- it is
not wired into `make dbt`/`make bi` and does not run automatically.
