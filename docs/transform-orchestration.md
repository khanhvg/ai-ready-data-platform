# Transform and Orchestration

## Goal

The dbt project transforms raw DuckDB landing tables into a layered lineage graph --
source -> staging -> intermediate -> core (dimensional) -> marts -- producing 11
documented business-facing marts with dbt-duckdb, then exposes the same steps through
an Airflow TaskFlow DAG.

## Commands

```bash
make dbt
make dbt-docs
make bi
```

For orchestration UI:

```bash
make airflow
```

## dbt structure

- Staging views (`models/staging/`): 18 `stg_*` views, one per raw source table. Clean/dedupe/type
  only; controlled data-quality scenarios are surfaced, not silently fixed.
- Intermediate models (`models/intermediate/`): 6 `int_*` ephemeral models holding reusable join
  and business-math logic (pricing, order enrichment, fulfillment, web funnel, inventory position,
  purchasing) so marts don't duplicate joins.
- Core dimensional models (`models/core/`): 7 `dim_*` + 9 `fct_*` tables -- the stable interface
  marts join against. `fct_purchase_orders` / `fct_purchase_order_items` are required so the
  suppliers/purchase-orders lineage added in the demo-large expansion has a business-facing
  terminus (not a dead end).
- Marts (`models/marts/`): 11 `mart_*` tables, each with a `description`, `tags`, and
  `meta.owner` in its YAML (`mart_supplier_purchasing` is required; see `_marts__models.yml`).
- Profile: `transform/dbt/profiles.yml`
- Tests: model YAML files in `transform/dbt/models/**`, plus one singular test in
  `transform/dbt/tests/` (non-negative shipment lead time).

The dbt target writes schemas into the same DuckDB file (intermediate models are `ephemeral` and
have no physical schema):

- `main_staging` for staging views
- `main_core` for dimension/fact tables
- `main_marts` for marts

`+persist_docs: {relation: true, columns: true}` is enabled project-wide, so every model
`description` is written as a DuckDB table/column comment (spot-checked via
`duckdb_tables()`/`duckdb_columns()`) in addition to landing in `target/manifest.json` for the
OpenMetadata dbt-artifact ingestion step.

## Data quality

Great Expectations is deferred. Quality signals are dbt tests only:

- strict tests for primary keys and core relationships
- warn-severity tests for deliberately injected demo data-quality scenarios: invalid order
  statuses, dangling `order_items`/`purchase_order_items` product references, and orphaned
  `web_events` session references
- warn-severity `unique` tests directly on `raw.orders.order_id` / `raw.customers.customer_id`
  (see `_sources.yml`) surface the controlled duplicate-row scenario; staging dedupes those same
  tables before the corresponding staging-layer `unique` tests run, so only the raw-layer tests
  actually catch the duplicates
- `mart_data_quality` aggregates counts for every controlled scenario in one table, for demo
  storytelling

Warnings are expected and useful for customer demo storytelling; errors are not expected.
`make dbt` now runs `dbt build` (models + tests together, in DAG order) instead of separate
`run`/`test` steps.

## Airflow

`orchestration/airflow/dags/retail_batch_pipeline.py` is authored with the Airflow 3
public TaskFlow API (`airflow.sdk` `dag`/`task`/`task_group` -- no `PythonOperator`,
no `airflow.operators.*`, no deprecated `airflow.decorators`) as five task groups,
chained with `>>` so only one process writes the DuckDB file at a time:

```text
generate {seed} -> load {load_raw, health_check} -> transform {dbt_build, dbt_docs_generate}
  -> serve {export_marts_snapshot} -> [optional] publish {publish_iceberg, iceberg_read_back}
```

Every `@task` is a one-line delegate into shared functions in
`orchestration/airflow/callables/pipeline.py` (the same entrypoints `make` targets
call), so no orchestration logic is duplicated between Airflow and the host path.

The `publish` group only exists when `LAKE_PROFILE_ENABLED` is truthy
(`{"1","true","yes","on"}`), read at DAG **parse** time -- see `docs/demo-runbook.md`
for the staged run order and why enabling it requires recreating the Airflow
container rather than just re-triggering a run.

## Rill snapshot

`make bi` runs `serving/export_marts_snapshot.py`, exporting marts as Parquet files under `serving/export/` for Rill Developer. Rill keeps its own embedded DuckDB, so the shared pipeline `.duckdb` file is not attached directly by default.
