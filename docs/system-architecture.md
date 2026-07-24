# System Architecture

End-to-end flow of the sandbox and the one distinction that matters most when reasoning about
it: the pipeline has a **logical** (DuckDB/dbt) side and a **physical** (Iceberg) side, and they
are deliberately kept as two separate, explainable views of the same curated marts rather than
merged into one.

## End-to-end flow

```text
data-generator/generate.py          (18 CSVs + manifest.json, deterministic per SCALE/SEED)
        |
        v
ingestion/load_raw.py               (raw.* landing tables in warehouse/retail.duckdb)
        |
        v
dbt (transform/dbt/)                staging (18 views) -> intermediate (6 ephemeral)
        |                              -> core: dim (7) + fct (9) -> marts (11 tables)
        v
        +-----------------------------------------+
        |                                         |
        v                                         v
serving/export_marts_snapshot.py         lake/publish_iceberg.py
  (marts -> Parquet, serving/export/)      (marts -> Iceberg tables, lake.retail.*)
        |                                         |
        v                                         v
   Rill Developer                          MinIO + Lakekeeper
   (serving/rill/, 11 explores)            (S3 storage + Iceberg REST catalog)
                                                   |
                                                   v
                                     OpenMetadata Iceberg ingestion
                                     (governance/openmetadata/ingestion/iceberg_ingestion.yaml)
                                     -> retail_iceberg service (11 physical tables)

   dbt artifacts (target/manifest.json, target/catalog.json)
        |
        v
   bootstrap_dbt_service.py + dbt ingestion workflow
   (governance/openmetadata/ingestion/dbt_ingestion.yaml)
        |
        v
   retail_duckdb service (45 logical tables, 130 lineage edges)

Airflow (orchestration/airflow/dags/retail_batch_pipeline.py) orchestrates the top of this chain
as one TaskFlow DAG: generate -> load -> transform -> serve -> [optional] publish. Everything
below "publish" (governance ingestion) runs out-of-DAG via the guarded `make catalog-ingest`
step, never co-running with Airflow -- see the Airflow section below and
`governance/openmetadata/README.md`.
```

## Independent assessment prototype

The Issue #38 Phase 1 assessment is a separate offline path, not another stage in the retail
pipeline:

```text
versioned rubric + synthetic architect fixtures
        |
        v
assessment/prototype/run.py
        |
        +--> deterministic scoring, confidence, seven gate traces, findings
        +--> ignored standalone report.json + report.html artifacts
```

It runs in `.assessment-venv`, starts no services, and never uses the demo repository or its
artifacts as customer maturity evidence. Engagement persistence, web workflow, knowledge
catalog, diagrams, and golden-demo integration remain later Issue #38 phases.

## The logical/physical distinction

Two independent views of the same 11 curated marts exist by design, and OpenMetadata does not
fabricate a lineage edge between them:

| | **Logical** (`retail_duckdb`) | **Physical** (`retail_iceberg`) |
|---|---|---|
| Storage | A single-file DuckDB warehouse (`warehouse/retail.duckdb`), single-writer | Apache Iceberg tables in MinIO (S3-compatible), cataloged via Lakekeeper's REST API |
| What it represents | The dbt **transformation graph** -- every model from `stg_*` through `int_*`/`dim_*`/`fct_*` to `mart_*`, with column-level lineage | The **published output** -- only the 11 business-facing marts, as durable, queryable table format artifacts |
| How OpenMetadata sees it | Bootstrapped from dbt's own `manifest.json`/`catalog.json` (no live DuckDB connector exists) | Crawled *live* via OpenMetadata's Iceberg connector (RestCatalog against Lakekeeper + S3 fileIO against MinIO) |
| Why it exists | Explains *how* a number was computed -- the joins, filters, and business logic between raw and mart | Explains *what* is durable and shareable outside this pipeline's own DuckDB file -- what a downstream consumer (a BI tool, another team) would actually read |

A curated mart therefore shows up twice in the catalog on purpose:
`retail_duckdb.retail.main_marts.mart_daily_revenue` (the dbt model, with full upstream lineage)
and `retail_iceberg.default.retail.mart_daily_revenue` (the Iceberg table Lakekeeper served to
OpenMetadata's crawler). Keeping them separate — rather than merging into one entity with a
fabricated cross-service edge — keeps each view honest about what it actually observed: dbt's
static artifacts describe the transformation; the live crawl describes the physical asset.
Rill and the Airflow `serve`/`publish` task groups read from the **same source of truth** for
"which marts are curated" (`lake/curated_assets.json`), so the exported Parquet, the published
Iceberg tables, and the Rill explores never drift from each other.

## Orchestration surface

`orchestration/airflow/dags/retail_batch_pipeline.py` is the only component that runs the
pipeline as a visible, schedulable DAG. It is authored exclusively with the Airflow 3 public
TaskFlow API (`airflow.sdk` `@dag`/`@task`/`@task_group` — no `PythonOperator`, no
`airflow.operators.*`), with every task a one-line delegate into
`orchestration/airflow/callables/pipeline.py`, the same functions the `make` targets call
directly on the host. This keeps a single source of truth for "what the pipeline does" whether
it's driven by Airflow or run step-by-step from a terminal. See
`docs/transform-orchestration.md` for the task-group structure and `docs/demo-runbook.md` for
how to exercise the optional `publish` group.

## Resource-safety model

Only the `core` path (generator, loader, dbt, Rill) runs with no containers at all. Every heavier
profile — `orchestration` (Airflow), `lake` (MinIO+Lakekeeper), `governance` (OpenMetadata) — is
opt-in and, by default, mutually exclusive with the others (enforced by Makefile guards). The one
deliberate exception is `make catalog-ingest`, which needs `lake` + `governance` live at the same
time for the Iceberg crawl; it stops `orchestration` first and tears `lake` back down afterward,
so the three heavy profiles are never all up simultaneously. See the "Startup order and resource
trade-offs" section of `README.md` and the measured memory table in
`governance/openmetadata/README.md`.
