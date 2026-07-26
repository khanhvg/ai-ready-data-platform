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

For the large-scale customer demo (issue #3: 18 tables, ≥300,000 rows, measured 620,340), use
`demo-large`, optionally capped for a slower machine with `MAX_ORDERS`/`MAX_WEB_EVENTS`:

```bash
make seed SCALE=demo-large SEED=42
# or, capped:
make seed SCALE=demo-large SEED=42 MAX_ORDERS=20000 MAX_WEB_EVENTS=50000
```

`demo-large` streams its high-volume tables straight to disk instead of holding them in memory,
so generation stays fast (~17s measured) and memory-light (~78-92MB peak RSS measured on an M1
Pro) regardless of scale.

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

Talk track: staging views clean/dedupe raw inputs; marts power dashboard metrics. dbt warnings
are deliberate quality scenarios, not failures. Phase 6 adds a complementary boundary over
deduplicated `stg_orders`: `accepted_orders` retains the four allowed statuses while
`quarantine_orders` retains every invalid/null status with a rule ID and reason. The canonical
eleven business marts remain the established legacy publication contract.

Generate lineage metadata and verify the complete additive evidence contract:

```bash
make dbt-docs
make demo-contract
make demo-verify
```

The pinned small/seed-42 fixture proves 990 accepted and 10 quarantined orders, complete and
disjoint coverage, no quarantined key in the governed product, and no raw email in the fixed
policy export. See `docs/demo-guide.md` and the nine manifests under `demo/manifests/stages/`.

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

For current proof, use the bounded verifier rather than merely opening the UI:

```bash
make demo-airflow-verify
```

It starts Airflow alone, waits healthy, checks import errors, triggers an exact run ID, polls all
six default tasks to success, records ignored local evidence, and always tears the profile down.
Starting the UI alone is not current execution evidence.

For presenter-only browsing after a separate verified run, `make airflow` remains available.

Open http://localhost:8080 and show `retail_batch_pipeline`, authored with the
Airflow 3 TaskFlow API (`@dag`/`@task`/`@task_group`, no `PythonOperator`) as five
visible task groups: `generate` (seed) -> `load` (load_raw, health_check) ->
`transform` (dbt_build, dbt_docs_generate) -> `serve` (export_marts_snapshot) ->
optional `publish` (publish_iceberg, iceberg_read_back).

The bounded Phase 6 proof uses the default
`generate -> load -> transform -> serve` flow with
`LAKE_PROFILE_ENABLED=false`; no lake profile is needed. The preserved DAG
contains an optional `publish` group, but this slice does not exercise it
because Airflow and lake must not overlap. Let `make demo-airflow-verify` stop
Airflow before starting the separate lake proof below.

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
containers -- it ingests nothing by itself. The Makefile guards this by refusing `make lake-up`
while governance containers are running and refusing `make catalog` while lake containers are
running, so the two heavy profiles are never started together by accident.

To actually populate OpenMetadata with **both** the physical Iceberg tables and the logical dbt
model graph, use the one deliberate, guarded exception to that rule:

```bash
make catalog-ingest
```

This stops `orchestration` first (so the peak is never all three heavy profiles at once), starts
`lake` + `governance` together for the ingestion window only, runs the Iceberg ingestion + the dbt
artifact ingestion + `verify_catalog.py`, then tears `lake` back down (leaving `governance` up so
you can browse http://localhost:8585). It requires an `OPENMETADATA_JWT_TOKEN` exported first --
see `governance/openmetadata/README.md` for how to mint the ingestion-bot token and the full
workflow/measured-memory details.

When the token is unavailable, leave this current stage unexecuted. The tracked GH-3 evidence is
historical context and must not be presented as a current run. OpenMetadata search and server
limits are 1g and 2g.

## 8. Teardown and recovery

Stop every heavy profile's containers when you're done:

```bash
make down
```

This runs `docker compose --profile orchestration --profile lake --profile governance down`, so
it's safe to run even if only one (or none) of those profiles is currently up. Docker named
volumes (MinIO's bucket, Lakekeeper's Postgres, OpenMetadata's MySQL/Elasticsearch, Airflow's
home directory) persist across `make down` by design, so restarting a profile picks up where it
left off (e.g. previously published Iceberg tables, previously ingested catalog entries).
Named-volume removal is outside the bounded Phase 6 workflow. `make down` deliberately preserves
those volumes.

To remove generated local files (CSVs, `manifest.json`, the DuckDB warehouse, Rill's Parquet
exports, dbt's `target/`/`logs/`, Rill's local runtime state, the Python venv):

```bash
make clean
```

**Recovery from a stuck/partial demo run:** if a run is interrupted mid-way (e.g. `make dbt`
fails partway or a container never reports healthy), `make down` + `make clean` returns the repo
to a clean starting state; re-run from `make seed` onward. Because every profile's containers are
stateless relative to the generated data (the DuckDB file and CSVs live on the host, not in a
container), there is no multi-step "rollback" beyond stopping containers and regenerating data --
determinism (`SCALE`/`SEED`) means re-running always reproduces the same dataset.
