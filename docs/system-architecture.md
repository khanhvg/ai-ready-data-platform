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

## Independent assessment package

The Issue #38 assessment is a separate offline path, not another stage in the retail pipeline:

```text
explicit engagement root + pinned v1 framework assets
        |
        v
deterministic engine
        |
        +--> maturity + coverage
        +--> confidence summary
        +--> all seven readiness-gate traces
        +--> findings + recommendations + separate architect review state
        |
        v
canonical source-state digest + 12-section report.json
        |
        v
standalone report.html (embedded CSS, no script or remote resources)
        ^
        |
loopback FastAPI/Jinja2 workflow
  create/resume -> quick assessment -> review -> deep-dive planning
  -> deterministic report -> archive export/preflight/import/reopen
```

The `evaluate` and `report` CLI commands require both an explicit engagement root and an
explicit output root. They run in `.assessment-venv`, start no services, and never use the demo
repository or its artifacts as customer maturity evidence. Demo references are presentation-only
illustrations and cannot affect maturity, confidence, priority, gates, or readiness.

Phase 2 adds public v1 JSON Schemas and typed consumers plus an authoritative engagement-folder
boundary under a user-selected root. `LocalEngagementStore` uses relative POSIX keys, canonical
JSON, checksums, one writer lock per engagement, and atomic same-directory replacement. A pure
registry migrates frozen prototype fixtures to v1 without editing their source.

Phase 3 adds package-versioned framework assets and pure maturity, confidence, gate, finding,
recommendation, and reporting services. The engine evaluates every rule in the pinned seven-gate
bundle without short-circuiting, retains operand provenance for triggered and untriggered rules,
and selects the most restrictive cap deterministically. Canonical JSON and HTML bytes derive
from the pinned framework plus a coherent engagement snapshot; generated output files are
excluded from the source-state digest.

Phase 4 adds a dependency-injected FastAPI/Jinja2 orchestration layer over those services.
Routes do not contain scoring, gate, question, or catalog rules. The server defaults to literal
loopback, rejects other hosts unless an explicit unsupported development override is provided,
and runs with one worker. Signed local sessions and CSRF tokens, host/origin enforcement,
revision checks held under the engagement writer lock, bounded uploads, escaped templates,
attachment-only evidence, CSP, and local static assets define the web boundary. Forms complete
through POST/Redirect/GET without JavaScript; JavaScript only enhances autosave and status.

The Phase 4 runtime acceptance starts two real loopback servers under different roots and one
pinned Chromium journey inside a non-loopback-network-denying sandbox. It creates and completes
an engagement, reviews all deterministic results, records a content-pending deep-dive selection,
generates and downloads the report, exports/imports the archive, reopens it, and compares source
and imported state plus report bytes. Catalog/demo views are read-only and unavailable content
is explicit. No route can run the retail pipeline or a command.

Portable export/import is separate from the retail pipeline: deterministic `ZIP_STORED` archives
contain normalized files and a canonical digest manifest. Import fully preflights archive names,
features, limits, checksums, versions, secrets, credentialed URIs, and machine paths, then writes
only to a sibling staging directory before atomic destination promotion. No assessment command
starts Docker, DuckDB, dbt, Rill, Airflow, Lakekeeper, OpenMetadata, AWS, or Terraform.

Knowledge-catalog content, architecture diagrams, AWS mappings, golden-demo integration,
deep-dive execution content, cloud/object-store implementation, and deployment remain Phase
5–8 work or explicitly deferred.

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
