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

Expand the flat DAG (`seed → load_raw → dbt_run → dbt_test`) into a **visible full-flow DAG with task groups** covering generate → load → dbt build/test → snapshot/export → Iceberg publish. The DAG is **modernized to the Airflow 3 public TaskFlow API** (`from airflow.sdk import dag, task, task_group`) on the pinned `apache/airflow:3.1.0-python3.12` image: `@dag`/`@task_group`/`@task` replace the current `PythonOperator` construction. Decorated tasks stay **thin delegates** that call the reusable functions in `callables/pipeline.py` (the single-source-of-truth entrypoints the `make` targets use), so no orchestration logic is duplicated. The heavy `publish` group is gated behind an explicit env flag so the default Airflow run stays light.

**Airflow 3 TaskFlow decision (binding user decision, issue #3 comment):** the modernized DAG uses **only** `@dag`, `@task`, and `@task_group` imported from `airflow.sdk`. It must contain **no explicit `PythonOperator`** and **no deprecated `airflow.decorators` import** (the `airflow.sdk` public API is authoritative on Airflow 3.1). This is a plan-only change here; the code rewrite lands in `/ck:cook`.

**Governance (OpenMetadata Iceberg + dbt) ingestion is deliberately out of this DAG.** Running OpenMetadata + Lakekeeper + MinIO alongside the Airflow stack exceeds the MacBook M1 Pro 16GB budget and conflicts with the safety guard. Instead, the DAG's `publish` group is the handoff point: once Iceberg tables exist, governance ingestion runs as the guarded host-side `make catalog-ingest` step (Phase 6) with Airflow stopped. This keeps AC5 (a visible pipeline DAG with clear task boundaries) and AC7 (both ingestions complete) satisfied without a three-heavy-profile co-run. See plan.md "Decisions for audit review" #1.

## Requirements

- **Functional**
  - Rewrite `retail_batch_pipeline.py` as a **TaskFlow `@dag` factory** whose body defines `@task_group`s with clear boundaries, each containing `@task`-decorated thin delegates:
    - `generate` → `seed`
    - `load` → `load_raw`, `health_check`
    - `transform` → `dbt_build` (or `dbt_run` + `dbt_test`), `dbt_docs_generate`
    - `serve` → `export_marts_snapshot`
    - `publish` (gated `LAKE_PROFILE_ENABLED`) → `publish_iceberg`, `iceberg_read_back`
  - **TaskFlow authoring rules (binding):** import `dag`, `task`, `task_group` from `airflow.sdk`; decorate the DAG factory with `@dag(...)` and instantiate it once at module scope; decorate groups with `@task_group(group_id=...)` and tasks with `@task(task_id=...)`. Each `@task` body is a one-line delegate to the matching `callables/pipeline.py` function (e.g. `pipeline.seed(...)`) — no subprocess/orchestration logic inline, no `PythonOperator`, no `airflow.operators.*` or `airflow.decorators` imports.
  - Add new callables in `callables/pipeline.py`: `health_check`, `dbt_build`, `dbt_docs_generate`, `iceberg_read_back`. Each shells out to the same script/CLI a `make` target uses (single source of truth), matching the existing thin-wrapper pattern. `publish_iceberg` reuses the existing `lake/publish_iceberg.py --skip-read-back`; `iceberg_read_back` invokes `lake/publish_iceberg.py --read-back-only` (the flag added in Phase 4) so the two Airflow tasks map to real CLI modes. **No OpenMetadata/ingestion callables are added here** — governance ingestion is a Phase-6 host-side step, so the Airflow image gains no `openmetadata-ingestion`/pyiceberg dependency.
  - **Container-network endpoints for the `publish` group (required):** `lake/publish_iceberg.py` defaults to host loopback (`LAKEKEEPER_CATALOG_URI=http://localhost:8181/catalog`, `LAKE_S3_ENDPOINT=http://localhost:9000`), which is unreachable **from inside the Airflow container**. The `publish` group must therefore run with the container-network equivalents injected as env: `LAKEKEEPER_CATALOG_URI=http://lakekeeper:8181/catalog` and `LAKE_S3_ENDPOINT=http://minio:9000`, plus `MINIO_ROOT_USER`/`MINIO_ROOT_PASSWORD`. This also requires the Airflow service and the `lake` services (`minio`, `lakekeeper`) to share a Docker Compose network so those service names resolve; confirm/declare that shared network when wiring the `publish` run.
  - Sequence to preserve single-writer discipline: chain the task-group return values `generate() >> load() >> transform() >> serve() >> publish()` so only one process writes DuckDB at a time. TaskFlow group ordering is expressed by `>>` on the group callables inside the `@dag` body (not by inter-group XCom), which keeps the linear single-writer chain explicit.
  - Default run (Airflow alone, no lake) executes `generate → load → transform → serve`; enabling `LAKE_PROFILE_ENABLED` extends into `publish`. Governance ingestion happens afterward, outside Airflow, via `make catalog-ingest` (Phase 6).

- **Non-functional**
  - **Safe credentials handling:** the Airflow service receives only the **lake publish** credentials/endpoints it actually needs (MinIO keys + Lakekeeper/MinIO container endpoints), from env/`.env`, surfaced via `docker-compose.yml` `environment:` referencing `${VARS}`; never hard-coded, never committed. **No `OPENMETADATA_JWT_TOKEN` is passed to the Airflow service** — OpenMetadata ingestion is not an Airflow task, so its JWT belongs solely to the Phase-6 host-side `make catalog-ingest` step. `.env.example` documents the lake vars here and the OM/governance vars in Phase 6.
  - DAG remains importable/parseable with the flag off (no import-time failures when optional deps/services absent). The **real** import-safety guarantee is that `callables/pipeline.py` has **no top-level optional imports** — it shells out to `lake/publish_iceberg.py` via `subprocess`, so pyiceberg/MinIO deps live only in the subprocess, never in the Airflow parse/worker process. (Note: the `@dag` factory body executes at parse time when the DAG is instantiated at module scope, so importing `pipeline` inside the factory is *not* execution-time isolation — it is safe only because `pipeline` itself imports nothing optional.) Read `LAKE_PROFILE_ENABLED` at module scope and conditionally add the `publish` group **inside** the factory body. Result: `airflow dags list-import-errors` stays clean whether or not the lake deps/services are present.
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
- `@task_group`s are the "clear task boundaries" AC5 requires and make the DAG graph readable in the UI.

TaskFlow structure (target skeleton, decorators only — cook fills bodies):

```python
from __future__ import annotations
import os
from datetime import datetime
from airflow.sdk import dag, task, task_group  # Airflow 3 public API; no PythonOperator

_TRUTHY = {"1", "true", "yes", "on"}
# Read at DAG parse time; changing it requires the Airflow container/scheduler to
# reparse the DAG (recreate the orchestration service), not just a re-trigger.
LAKE_PROFILE_ENABLED = os.environ.get("LAKE_PROFILE_ENABLED", "false").strip().lower() in _TRUTHY

@dag(dag_id="retail_batch_pipeline", schedule="@daily",
     start_date=datetime(2026, 1, 1), catchup=False, tags=["retail", "batch"])
def retail_batch_pipeline():
    from callables import pipeline  # pipeline.py has NO top-level optional (pyiceberg) imports

    @task_group(group_id="generate")
    def generate():
        @task(task_id="seed")
        def seed(): pipeline.seed(scale=os.environ.get("SCALE", "small"),
                                  seed=int(os.environ.get("SEED", "42")))
        seed()

    # load {load_raw -> health_check}, transform {dbt_build -> dbt_docs_generate},
    # serve {export_marts_snapshot} follow the same @task_group/@task(task_id=...) delegate pattern.

    chain = generate() >> load() >> transform() >> serve()
    if LAKE_PROFILE_ENABLED:
        chain >> publish()  # publish {publish_iceberg -> iceberg_read_back}

retail_batch_pipeline()
```

**Truthy gate (binding):** the same `_TRUTHY` set (`{"1","true","yes","on"}`) governs both the DAG gate and every doc/verification instruction, so `LAKE_PROFILE_ENABLED=1` **and** `=true` both enable `publish`. Do not reintroduce the old `== "true"`-only check, which would silently skip the group for `=1`.

## Related Code Files

- Modify: `orchestration/airflow/dags/retail_batch_pipeline.py` — rewrite as `@dag` TaskFlow factory using `@task_group`/`@task` from `airflow.sdk`; drop the `airflow.operators.python.PythonOperator` / `airflow import DAG` construction and the module-level `callables` import; keep `LAKE_PROFILE_ENABLED` gating and the linear group dependencies. Update the module docstring to state the TaskFlow style (remove the "Every task is a PythonOperator" wording).
- Modify: `orchestration/airflow/callables/pipeline.py` — new callables (reuse entrypoints); no OM/ingestion callables. The thin-delegate contract is unchanged by TaskFlow (decorated `@task`s call these functions), but drop the "PythonOperator" wording in its docstring — the functions are the shared reusable entrypoints invoked by TaskFlow tasks and by the host `make` path alike.
- Modify: `lake/publish_iceberg.py` — add the `--read-back-only` flag (owned in Phase 4) so the `iceberg_read_back` Airflow task maps to a real CLI mode. Listed here because Phase 5 is the consumer; the change itself lands with Phase 4.
- Modify (comment only): `orchestration/airflow/requirements.txt` — **no dependency change** for governance (OM ingestion is not run from Airflow, so no `openmetadata-ingestion`/pyiceberg is added; `publish`/`read_back` reuse the existing lake entrypoints). But its header comment currently says "the retail_batch_pipeline DAG's PythonOperator tasks" — update that stale wording to "TaskFlow tasks" so the Airflow surface has no lingering `PythonOperator` reference.
- Modify (comment only): `orchestration/airflow/Dockerfile` — line 2 comment says "PythonOperator tasks can call…"; reword to "TaskFlow tasks".
- Modify: `docker-compose.yml` (airflow service `environment:` **and** networks) — pass `LAKE_PROFILE_ENABLED` plus the container-network lake endpoints/creds `publish_iceberg` needs from `${VARS}`: `LAKEKEEPER_CATALOG_URI=http://lakekeeper:8181/catalog`, `LAKE_S3_ENDPOINT=http://minio:9000`, `MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`. Ensure the airflow service shares a Compose network with `minio`/`lakekeeper` so those hostnames resolve. Also reword the orchestration-profile section comment (`# --- orchestration profile: Apache Airflow (standalone, PythonOperator tasks) ---`) to drop `PythonOperator`. OpenMetadata JWT and Iceberg-connector creds belong to the Phase-6 ingestion step, **not** the Airflow service.
- Modify: `.env.example` — document `LAKE_PROFILE_ENABLED` and lake creds/endpoints (non-production local defaults or placeholders). Governance creds are documented in Phase 6.
- Modify: `docs/transform-orchestration.md` + `docs/demo-runbook.md` — full-flow DAG description, gating, staged run.
- Reference (read-only): existing DAG + callables, `docker-compose.yml` airflow service.

## Implementation Steps

1. Add new callables wrapping the canonical scripts/CLIs (health, dbt build, dbt docs, read-back).
2. Rewrite the DAG as an `@dag` TaskFlow factory: `from airflow.sdk import dag, task, task_group`; `@task_group` per boundary; `@task` thin delegates to `callables/pipeline.py`; import `callables.pipeline` inside the factory body; instantiate the DAG once at module scope. No `PythonOperator`, no `airflow.decorators`. Keep import safe when the flag is off.
3. Wire dependencies with `>>` on the group callables: `generate() >> load() >> transform() >> serve()`; append `>> publish()` only when `LAKE_PROFILE_ENABLED` is true.
4. Pass required lake env through the compose airflow service from `${VARS}` — the **container-network** endpoints (`lakekeeper:8181`, `minio:9000`) plus MinIO creds — and ensure the airflow service shares a network with the lake services; update `.env.example`.
5. Verify inside the pinned `apache/airflow:3.1.0-python3.12` container: `python -m py_compile` on the DAG + callables; `airflow dags list` shows `retail_batch_pipeline`; `airflow dags list-import-errors` is empty; `airflow tasks list retail_batch_pipeline` shows the expected group-prefixed task IDs and the task-group graph. Then `make airflow`, open :8080, and **trigger a real DAG run** (default groups green). To verify `publish`: because `LAKE_PROFILE_ENABLED` is read at **parse time**, a re-trigger alone will not enable the group — bring the `lake` profile up and **recreate the orchestration service with the flag set** so the DAG reparses (e.g. stop orchestration, then `LAKE_PROFILE_ENABLED=true docker compose --profile orchestration up -d --force-recreate`), re-run `dags list` / `list-import-errors` / `tasks list` to confirm `publish` now appears, then trigger and confirm the group completes. Capture run state (AC5/AC8). Governance ingestion is verified separately in Phase 6.

## Success Criteria

- [ ] DAG is authored with the Airflow 3 TaskFlow API only: `airflow.sdk` `@dag`/`@task_group`/`@task`; no `PythonOperator`, no `airflow.operators.*`, no `airflow.decorators` import (grep-checkable).
- [ ] DAG renders in the UI with named task groups (generate/load/transform/serve/publish) — visible boundaries (AC5).
- [ ] `airflow dags list` shows `retail_batch_pipeline`; `airflow dags list-import-errors` is empty; `airflow tasks list retail_batch_pipeline` shows the expected group-prefixed task IDs / group graph.
- [ ] Default run (no lake) triggers a real DAG run that completes generate→load→transform→serve green.
- [ ] With `LAKE_PROFILE_ENABLED=1` and the `lake` profile up, the `publish` group completes; full pipeline sequence green (AC5).
- [ ] DAG parses with the flag off (no import errors); `python -m py_compile` on DAG + callables passes.
- [ ] No credentials committed; env-driven (AC9).

## Risk Assessment

- **Import-time fragility:** optional deps (pyiceberg/MinIO) must not break DAG parsing when absent. The guarantee is that they are **never imported into the Airflow process at all** — `lake/publish_iceberg.py` is invoked via `subprocess` from `callables/pipeline.py`, and `pipeline.py` keeps no top-level optional imports. Note the `@dag` factory body runs at **parse time** (the DAG is instantiated at module scope), so importing `pipeline` inside the factory is *not* execution-time isolation and is not what keeps parsing safe; it is safe only because `pipeline` imports nothing optional. `airflow dags list-import-errors` therefore stays clean with or without the lake deps present.
- **TaskFlow API drift:** `airflow.sdk` is the Airflow 3.1 public import surface; confirm `dag`/`task`/`task_group` resolve from it in the pinned `3.1.0-python3.12` image during verification (they do on 3.1). If a symbol were unavailable, that is an import error caught by `airflow dags list-import-errors` before any run — do **not** fall back to `airflow.decorators` (deprecated) per the binding decision.
- **Resource:** never run Airflow + `lake` + `governance` at once. The `publish` group needs only `lake`; governance ingestion (P6) runs with Airflow stopped. Document the staged order.
- **Single-writer:** keep strict ordering via the linear `>>` group chain; never parallelize two DuckDB writers.
- **Rollback:** revert DAG/callables/compose-env changes; the flat pipeline still works.
