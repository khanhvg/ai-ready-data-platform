# AI Ready Data Platform Sandbox

Local-first sandbox for practicing and demonstrating an AI-ready retail data platform on a MacBook M1 Pro 16GB without overloading the machine.

## Core stack

- Synthetic retail CSV generator: 18 tables, deterministic seeds, scale profiles up to
  `demo-large` (≥300,000 rows, streamed generation so peak memory stays flat as scale grows).
- DuckDB embedded warehouse for local analytics.
- dbt-duckdb layered lineage graph -- source -> staging (18 views) -> intermediate (6 ephemeral
  models) -> core dimensional (7 `dim_*` + 9 `fct_*`) -> 11 documented business-facing marts --
  built with `dbt build` (models + tests together) and `dbt docs generate`.
- Rill Developer: 11 explores/metrics views over the exported Parquet marts.
- Airflow 3 TaskFlow DAG (`airflow.sdk` `@dag`/`@task`/`@task_group`, no `PythonOperator`) running
  the full `generate -> load -> transform -> serve` sequence, with an optional `publish` task
  group for the Iceberg step.
- Optional `lake` profile: MinIO + Lakekeeper Iceberg REST catalog; publishes and read-back
  verifies all 11 curated marts.
- Optional `governance` profile: OpenMetadata server, with `make catalog-ingest` ingesting both
  the physical Iceberg tables (11) and the logical dbt model graph (45 tables, 130 lineage
  edges) -- see `governance/openmetadata/README.md`.

See `docs/system-architecture.md` for the end-to-end flow and the DuckDB-logical vs
Iceberg-physical distinction.

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

## AI-ready assessment package

Issue #38 Phases 1–3 add a separate, local-only Python 3.12 package under `assessment/`. It
validates the 10-domain rubric and 30 anchored questions, recomputes four two-rater scenarios,
checks the 117/119 calibration result, defines the v1 portable engagement contracts and local
folder authority, and evaluates those folders with a deterministic maturity, confidence,
seven-gate, finding, recommendation, and report engine:

```bash
make assessment-install
make assessment-schema assessment-contract assessment-scenarios assessment-calibration
make assessment-store assessment-migration assessment-import-export
make assessment-portability assessment-security-scan
make assessment-engine assessment-report assessment-test
make assessment-lint assessment-typecheck assessment-build
```

The assessment uses `.assessment-venv`, starts no containers, and does not read from or score
the retail demo. Prototype generated reports are ignored under `assessment/.generated/`; see
`assessment/README.md` for the final explicit-root CLI and exact implemented boundary.
Engagement and output roots are selected explicitly by the user and are never broadly ignored
or removed by assessment cleanup. Phase 3 verification is recorded in
`docs/verification/GH-38-phase-3-evidence.md`.

## Scale profiles

| Profile | Purpose | Approximate order volume | Total rows (18 tables) |
|---|---|---:|---:|
| `small` | smoke test / quick demo | 1,000 orders | ~6,800 |
| `medium` | normal demo/dev dataset | 15,000 orders | ~91,000 |
| `large` | richer demo dataset, still intended for 16GB RAM | 150,000 orders | ~945,000 |
| `demo-large` | large-scale customer demo (issue #3): the full 18-table graph, ≥300,000-row floor with margin | 90,000 orders | ~620,000 (measured 620,340) |

All profiles are deterministic for a given `SEED` and emit a `data/raw/manifest.json` with row
counts, checksums, quality summary, and generation metadata. `demo-large` streams its high-volume
tables straight to disk (peak RSS measured ~78-92 MB on M1 Pro, well under the 16GB budget); use
`--max-orders`/`--max-web-events` (or `MAX_ORDERS`/`MAX_WEB_EVENTS` with `make seed`) to bound any
profile further on a slower machine. See `data-generator/schema.md` for the row math and
`docs/storage-ingestion.md` for the full table list.

## Optional profiles

Run heavier profiles one at a time on 16GB RAM:

```bash
make airflow          # Airflow UI on :8080 -- TaskFlow DAG, full generate->load->transform->serve(+publish)
make lake-up           # MinIO + Lakekeeper
make lake-publish      # publish marts to Iceberg after make dbt
make catalog           # OpenMetadata, heaviest profile alone
make catalog-ingest    # guarded lake+governance co-run window: Iceberg + dbt ingestion into OpenMetadata
```

`make lake-up` and `make catalog` include a safety guard so the `lake` and `governance` profiles
are not started together by accident on a 16GB laptop. `make catalog-ingest` is the one deliberate,
guarded exception (documented in `governance/openmetadata/README.md`): it stops `orchestration`
first, brings `lake` + `governance` up together only for the ingestion window (measured ≈2.6GB
actual RSS, well under the ~7.5GB of `mem_limit` headroom), then tears `lake` back down.

### Startup order and resource trade-offs

1. **Core** (no containers): `make seed` -> `make load` -> `make health` -> `make dbt` -> `make bi`.
   Safe to run repeatedly; this is the default path for iteration and CI-style smoke checks.
2. **Rill** (local CLI, no containers): `rill start serving/rill` after `make bi`.
3. **One heavy profile at a time** for `orchestration` (Airflow), `lake` (MinIO+Lakekeeper), or
   `governance` (OpenMetadata) alone -- each is opt-in and torn down (`make down`) before starting
   the next, so no two heavy profiles compete for RAM by accident.
4. **The one documented co-run exception**: `make catalog-ingest` needs `lake` + `governance`
   together (the Iceberg connector must reach both live) and stops `orchestration` first so the
   peak is never all three heavy profiles at once.
5. **Teardown**: `make down` stops every heavy profile's containers; `make clean` removes
   generated data/artifacts (CSVs, manifest, DuckDB file, Parquet exports, dbt `target/`/`logs/`,
   Rill's local runtime state, the venv). Docker named volumes (MinIO, Lakekeeper's Postgres,
   OpenMetadata's MySQL/Elasticsearch, Airflow's home) persist across `make down` -- remove them
   with `docker compose down -v` (or `docker volume rm`) for a fully clean slate.

See `docs/demo-runbook.md` for the full staged demo flow, `docs/verification/GH-3-full-flow-evidence.md`
for a real end-to-end verification run, and `versions.md` for the tested component matrix.
