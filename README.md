# AI Ready Data Platform Sandbox

Local-first sandbox for practicing and demonstrating an AI-ready retail data platform on a MacBook M1 Pro 16GB without overloading the machine.

## Core stack

- Synthetic retail CSV generator with deterministic seeds and scale profiles.
- DuckDB embedded warehouse for local analytics.
- dbt-duckdb for staging, marts, and dbt tests.
- Airflow PythonOperators for the same pipeline steps as the Makefile.
- Rill Developer for lightweight dashboarding over exported Parquet marts.
- Optional `lake` profile: MinIO + Lakekeeper for Iceberg publish smoke tests.
- Optional `governance` profile: OpenMetadata/catalog/lineage experiments.

## Quick start: core profile

```bash
make seed SCALE=small SEED=42
make load
make health
make dbt
make bi
```

The core profile uses local Python tools and DuckDB only; it starts no containers.
Generated data and warehouses are intentionally gitignored.

## Scale profiles

| Profile | Purpose | Approximate order volume |
|---|---|---:|
| `small` | smoke test / quick demo | 1,000 orders |
| `medium` | normal demo/dev dataset | 15,000 orders |
| `large` | richer demo dataset, still intended for 16GB RAM | 150,000 orders |

All profiles are deterministic for a given `SEED` and emit a `data/raw/manifest.json` with row counts, checksums, quality summary, and generation metadata.

## Optional profiles

Run heavier profiles one at a time on 16GB RAM:

```bash
make airflow        # Airflow UI on :8080
make lake-up        # MinIO + Lakekeeper
make lake-publish   # publish marts to Iceberg after make dbt
make catalog        # OpenMetadata, heaviest profile
```

`make lake-up` and `make catalog` include a safety guard so the lake and governance profiles are not started together by accident on a 16GB laptop.

See `docs/demo-runbook.md` for demo flow and `versions.md` for the tested component matrix.
