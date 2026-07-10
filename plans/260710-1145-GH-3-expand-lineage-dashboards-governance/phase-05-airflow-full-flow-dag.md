---
phase: 5
title: "Airflow full-flow DAG"
status: pending
priority: P2
dependencies: [1, 2, 3, 4]
effort: "M"
note: "Governance ingestion is intentionally NOT an Airflow task — it runs as the out-of-DAG make catalog-ingest step (P6) because co-running OpenMetadata+Lakekeeper+MinIO with Airflow exceeds the 16GB budget. See plan.md decision 1."
---

# Phase 5: Airflow full-flow DAG

## Overview

Expand the flat DAG (`seed → load_raw → dbt_run → dbt_test`) into a **visible full-flow DAG with task groups** covering generate → load → dbt build/test → snapshot/export → Iceberg publish. Tasks stay PythonOperator/subprocess and reuse the canonical project entrypoints via `callables/pipeline.py`. The heavy `publish` group is gated behind an explicit env flag so the default Airflow run stays light.

**Governance (OpenMetadata Iceberg + dbt) ingestion is deliberately out of this DAG.** Running OpenMetadata + Lakekeeper + MinIO alongside the Airflow stack exceeds the MacBook M1 Pro 16GB budget and conflicts with the safety guard. Instead, the DAG's `publish` group is the handoff point: once Iceberg tables exist, governance ingestion runs as the guarded host-side `make catalog-ingest` step (Phase 6) with Airflow stopped. This keeps AC5 (a visible pipeline DAG with clear task boundaries) and AC7 (both ingestions complete) satisfied without a three-heavy-profile co-run. See plan.md "Decisions for audit review" #1.

## Requirements

- **Functional**
  - Restructure `retail_batch_pipeline.py` into TaskGroups with clear boundaries:
    - `generate` → `seed`
    - `load` → `load_raw`, `health_check`
    - `transform` → `dbt_build` (or `dbt_run` + `dbt_test`), `dbt_docs_generate`
    - `serve` → `export_marts_snapshot`
    - `publish` (gated `LAKE_PROFILE_ENABLED`) → `publish_iceberg`, `iceberg_read_back`
  - Add new callables in `callables/pipeline.py`: `health_check`, `dbt_build`, `dbt_docs_generate`, `iceberg_read_back`. Each shells out to the same script/CLI a `make` target uses (single source of truth), matching the existing thin-wrapper pattern. `publish_iceberg` reuses the existing `lake/publish_iceberg.py --skip-read-back`; `iceberg_read_back` invokes `lake/publish_iceberg.py --read-back-only` (the flag added in Phase 4) so the two Airflow tasks map to real CLI modes. **No OpenMetadata/ingestion callables are added here** — governance ingestion is a Phase-6 host-side step, so the Airflow image gains no `openmetadata-ingestion`/pyiceberg dependency.
  - **Container-network endpoints for the `publish` group (required):** `lake/publish_iceberg.py` defaults to host loopback (`LAKEKEEPER_CATALOG_URI=http://localhost:8181/catalog`, `LAKE_S3_ENDPOINT=http://localhost:9000`), which is unreachable **from inside the Airflow container**. The `publish` group must therefore run with the container-network equivalents injected as env: `LAKEKEEPER_CATALOG_URI=http://lakekeeper:8181/catalog` and `LAKE_S3_ENDPOINT=http://minio:9000`, plus `MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD`. This also requires the Airflow service and the `lake` services (`minio`, `lakekeeper`) to share a Docker Compose network so those service names resolve; confirm/declare that shared network when wiring the `publish` run.
  - Sequence to preserve single-writer discipline: `generate → load → transform → serve → publish` (only one writer of DuckDB at a time).
  - Default run (Airflow alone, no lake) executes `generate → load → transform → serve`; enabling `LAKE_PROFILE_ENABLED` extends into `publish`. Governance ingestion happens afterward, outside Airflow, via `make catalog-ingest` (Phase 6).

- **Non-functional**
  - **Safe credentials handling:** the Airflow service receives only the **lake publish** credentials/endpoints it actually needs (MinIO keys + Lakekeeper/MinIO container endpoints), from env/`.env`, surfaced via `docker-compose.yml` `environment:` referencing `${VARS}`; never hard-coded, never committed. **No `OPENMETADATA_JWT_TOKEN` is passed to the Airflow service** — OpenMetadata ingestion is not an Airflow task, so its JWT belongs solely to the Phase-6 host-side `make catalog-ingest` step. `.env.example` documents the lake vars here and the OM/governance vars in Phase 6.
  - DAG remains importable/parseable with the flag off (no import-time failures when optional deps/services absent).
  - Airflow container stays within its 4g `mem_limit`. Airflow is **stopped** before the Phase-6 `make catalog-ingest` window, so its footprint never overlaps the `lake` + `governance` peak (see P6 memory math).

## Architecture

```text
[generate] → [load] → [transform] → [serve] ──►(LAKE_PROFILE_ENABLED) [publish]
                                                                          │
                                                                          ▼
                                              (out-of-DAG, Airflow stopped)
                                                 make catalog-ingest  → OpenMetadata Iceberg + dbt ingestion (P6)
```

- Gating uses the existing env-flag pattern (issue #1 already reads `LAKE_PROFILE_ENABLED`). No `GOVERNANCE_PROFILE_ENABLED` DAG flag is added.
- Governance ingestion consumes `publish` output (Iceberg tables) and `transform` output (dbt artifacts), but runs as the P6 host-side step, not an Airflow task.
- Task groups are the "clear task boundaries" AC5 requires and make the DAG graph readable in the UI.

## Related Code Files

- Modify: `orchestration/airflow/dags/retail_batch_pipeline.py` — TaskGroups, `LAKE_PROFILE_ENABLED` gating, dependencies.
- Modify: `orchestration/airflow/callables/pipeline.py` — new callables (reuse entrypoints); no OM/ingestion callables.
- Modify: `lake/publish_iceberg.py` — add the `--read-back-only` flag (owned in Phase 4) so the `iceberg_read_back` Airflow task maps to a real CLI mode. Listed here because Phase 5 is the consumer; the change itself lands with Phase 4.
- `orchestration/airflow/requirements.txt` — **no change** for governance: OM ingestion is not run from Airflow, so no `openmetadata-ingestion`/pyiceberg is added to the Airflow image (decision, not deferred). `publish`/`read_back` reuse the existing lake entrypoints already present.
- Modify: `docker-compose.yml` (airflow service `environment:` **and** networks) — pass `LAKE_PROFILE_ENABLED` plus the container-network lake endpoints/creds `publish_iceberg` needs from `${VARS}`: `LAKEKEEPER_CATALOG_URI=http://lakekeeper:8181/catalog`, `LAKE_S3_ENDPOINT=http://minio:9000`, `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`. Ensure the airflow service shares a Compose network with `minio`/`lakekeeper` so those hostnames resolve. OpenMetadata JWT and Iceberg-connector creds belong to the Phase-6 ingestion step, **not** the Airflow service.
- Modify: `.env.example` — document `LAKE_PROFILE_ENABLED` and lake creds/endpoints (non-production local defaults or placeholders). Governance creds are documented in Phase 6.
- Modify: `docs/transform-orchestration.md` + `docs/demo-runbook.md` — full-flow DAG description, gating, staged run.
- Reference (read-only): existing DAG + callables, `docker-compose.yml` airflow service.

## Implementation Steps

1. Add new callables wrapping the canonical scripts/CLIs (health, dbt build, dbt docs, read-back).
2. Rebuild the DAG with TaskGroups and `LAKE_PROFILE_ENABLED` gating; keep import safe when the flag is off.
3. Wire dependencies: `generate→load→transform→serve→publish`; the `publish` group is present only when `LAKE_PROFILE_ENABLED` is true.
4. Pass required lake env through the compose airflow service from `${VARS}` — the **container-network** endpoints (`lakekeeper:8181`, `minio:9000`) plus MinIO creds — and ensure the airflow service shares a network with the lake services; update `.env.example`.
5. `make airflow`, open :8080, trigger `retail_batch_pipeline`; verify default groups succeed; then verify the `publish` group with `LAKE_PROFILE_ENABLED=1` and the `lake` profile up. Capture run state (AC5/AC8). Governance ingestion is verified separately in Phase 6.

## Success Criteria

- [ ] DAG renders in the UI with named TaskGroups (generate/load/transform/serve/publish) — visible boundaries (AC5).
- [ ] Default run (no lake) completes generate→load→transform→serve green.
- [ ] With `LAKE_PROFILE_ENABLED=1` and the `lake` profile up, the `publish` group completes; full pipeline sequence green (AC5).
- [ ] DAG parses with the flag off (no import errors); `python -m py_compile` on DAG + callables passes.
- [ ] No credentials committed; env-driven (AC9).

## Risk Assessment

- **Import-time fragility:** optional imports (pyiceberg) used by the `publish` callables must not break DAG parsing when absent — import inside callables, not at module top.
- **Resource:** never run Airflow + `lake` + `governance` at once. The `publish` group needs only `lake`; governance ingestion (P6) runs with Airflow stopped. Document the staged order.
- **Single-writer:** keep strict ordering; never parallelize two DuckDB writers.
- **Rollback:** revert DAG/callables/compose-env changes; the flat pipeline still works.
