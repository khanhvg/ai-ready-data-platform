# Transform and Orchestration

## Goal

P3 transforms raw DuckDB landing tables into customer-demo marts with dbt-duckdb, then exposes the same steps through Airflow PythonOperators.

## Commands

```bash
make dbt
make bi
```

For orchestration UI:

```bash
make airflow
```

## dbt structure

- Staging views: `transform/dbt/models/staging/`
- Marts: `transform/dbt/models/marts/`
- Profile: `transform/dbt/profiles.yml`
- Tests: model YAML files in `transform/dbt/models/**`

The dbt target writes schemas into the same DuckDB file:

- `main_staging` for staging views
- `main_marts` for marts

## Data quality

Great Expectations is deferred. Quality signals are dbt tests only:

- strict tests for primary keys and core relationships
- warn-severity tests for deliberately injected demo data-quality scenarios, including invalid
  order statuses and dangling product references
- warn-severity `unique` tests directly on `raw.orders.order_id` / `raw.customers.customer_id`
  (see `_sources.yml`) surface the controlled duplicate-row scenario; staging dedupes those same
  tables before the corresponding staging-layer `unique` tests run, so only the raw-layer tests
  actually catch the duplicates

Warnings are expected and useful for customer demo storytelling; errors are not expected.

## Airflow

`orchestration/airflow/dags/retail_batch_pipeline.py` defines:

```text
seed -> load_raw -> dbt_run -> dbt_test -> optional publish_iceberg
```

Each task is a PythonOperator calling shared functions in `orchestration/airflow/callables/pipeline.py`.

## Rill snapshot

`make bi` runs `serving/export_marts_snapshot.py`, exporting marts as Parquet files under `serving/export/` for Rill Developer. Rill keeps its own embedded DuckDB, so the shared pipeline `.duckdb` file is not attached directly by default.
