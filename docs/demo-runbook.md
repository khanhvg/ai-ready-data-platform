# Customer Demo Runbook

This demo is designed for a MacBook M1 Pro 16GB. Keep the default `core` path lightweight; start heavier profiles one at a time.

## 1. Generate diverse retail data

```bash
make seed SCALE=small SEED=42
```

Show `data/raw/manifest.json` to explain reproducibility, row counts, checksums, and controlled quality scenarios.

For a richer demo, use:

```bash
make seed SCALE=medium SEED=42
```

## 2. Load DuckDB raw landing tables

```bash
make load
make health
```

Talk track: raw CSV lands into DuckDB `raw.*` tables; this is idempotent and local-first.

## 3. Transform and test with dbt

```bash
make dbt
```

Talk track: staging views clean/dedupe raw inputs; marts power dashboard metrics. dbt warnings are deliberate quality scenarios, not failures.

## 4. Export marts for Rill

```bash
make bi
```

Then run Rill if installed:

```bash
rill start serving/rill
```

Open the Rill URL shown by the CLI and walk through daily revenue, top products, and customer cohorts.

## 5. Optional: Airflow orchestration

```bash
make airflow
```

Open http://localhost:8080 and show `retail_batch_pipeline` using PythonOperators.

## 6. Optional: Iceberg lake smoke test

```bash
make lake-up
make lake-publish
```

This starts MinIO + Lakekeeper and publishes curated marts to Iceberg. Use this after the core demo, not during a low-resource run.

## 7. Optional: Catalog/lineage

```bash
make catalog
```

OpenMetadata is opt-in and the heaviest profile. `make catalog` only starts the OpenMetadata
containers -- it ingests nothing by itself. Follow `governance/openmetadata/README.md` for the
manual one-time steps (register a database service, `dbt docs generate`, run the dbt ingestion
workflow) to pull dbt lineage/descriptions into it. Do not run `lake` and `governance`
simultaneously on 16GB RAM unless you intentionally accept the overhead.
The Makefile guards this by refusing `make lake-up` while governance containers are running and refusing `make catalog` while lake containers are running.
