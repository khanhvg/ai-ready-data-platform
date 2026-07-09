# Version Matrix

Proven by the P1 compatibility spike (2026-07-09) on macOS arm64 (M1 Pro), Python 3.12.3, in a
throwaway venv. This replaces the plan's *candidate* matrix with the actually-tested one.

| Component | Version | Notes |
|---|---|---|
| Python | 3.12.x | matches local toolchain |
| duckdb (Python package) | 1.5.4 | latest at spike time; supersedes the plan's DuckDB 1.4.x LTS candidate |
| dbt-core | 1.11.12 | pulled in transitively by dbt-duckdb |
| dbt-duckdb | 1.10.1 | adapter; `dbt run` verified against a live DuckDB 1.5.4 file |
| dbt-adapters | 1.24.4 | transitive |
| DuckDB `iceberg` extension | bundled w/ duckdb 1.5.4 | `INSTALL/LOAD iceberg` verified |
| DuckDB `httpfs` extension | bundled w/ duckdb 1.5.4 | required for S3/MinIO access; verified |
| Rill Developer | v0.87.8 | CLI binary verified (`rill version`); embeds its own DuckDB — see R2 below |
| Apache Airflow | 3.x (installed in `orchestration` extra, see `orchestration/airflow/requirements.txt`) | LocalExecutor/standalone, minimal providers, PythonOperator only |
| MinIO | latest stable image (`minio/minio`) | `lake` profile only |
| Lakekeeper (Iceberg REST catalog) | latest stable image (`quay.io/lakekeeper/catalog`) | `lake` profile only — required for DuckDB Iceberg **writes** (raw S3 path insufficient) |
| OpenMetadata | latest stable (`docker-compose` from upstream) | `governance` profile only — no native DuckDB connector; ingests dbt artifacts + OpenLineage/Airflow + S3/Iceberg metadata |

## Spike evidence

```
$ python3 -c "import duckdb; print(duckdb.__version__)"
1.5.4
$ dbt --version
Core: installed 1.11.12 - Up to date!
Plugins: duckdb 1.10.1 - Up to date!
$ dbt run   # trivial model against a real DuckDB file
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=1
$ python3 -c "import duckdb; c=duckdb.connect(':memory:'); c.execute('INSTALL iceberg'); c.execute('LOAD iceberg')"
iceberg extension loaded OK
$ ./rill version
rill version v0.87.8
```

## Resolved risks from the plan

- **R1 (Iceberg write needs a catalog):** confirmed — DuckDB's `iceberg` extension attaches to a REST
  catalog for writes. `lake` profile ships MinIO + Lakekeeper. See `lake/README.md` for the exact
  `ATTACH` syntax and the write→read-back smoke test (P4).
- **R2 (Rill embeds its own DuckDB):** confirmed via CLI install — Rill's supported ingestion path is
  its own embedded DuckDB. Default Rill source in this repo is the **exported Parquet snapshot** of
  the marts (`serving/export_marts_snapshot.py`), not a direct attach to the shared pipeline
  `.duckdb` file. This makes the DuckDB-version mismatch (pipeline 1.5.4 vs Rill's bundled DuckDB)
  irrelevant, since Parquet is the interchange format.
- **R3 (M1 16GB budget):** `core` measured in P1 (see `docs/`); heavier profiles (`orchestration`,
  `lake`, `governance`) stay opt-in and are run one-at-a-time.

## Re-running the spike

```bash
python3 -m venv /tmp/ck-spike && source /tmp/ck-spike/bin/activate
unset PYTHONPATH   # required if a global PYTHONPATH leaks a different interpreter's site-packages
pip install duckdb dbt-duckdb
dbt --version
```
