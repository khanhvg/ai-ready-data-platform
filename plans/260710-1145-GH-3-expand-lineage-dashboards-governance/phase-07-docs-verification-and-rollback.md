---
phase: 7
title: Docs verification and rollback
status: completed
priority: P2
dependencies:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
effort: M
---

# Phase 7: Docs, verification, and rollback

## Overview

Land the documentation, run the full real verification suite, and codify teardown/rollback. This phase produces the evidence for AC8 (row counts, dbt results, Iceberg read-back, OM ingestion summaries, Airflow run state, app URLs) and satisfies AC9 (no secrets/artifacts committed) and AC10 (README/runbook explains startup order, resource trade-offs, architecture, teardown).

## Requirements

- **Functional (docs)**
  - Update `README.md`: new stack surface (18 tables, layered dbt graph, ≥8 marts, ≥8 explores, full-flow DAG, Iceberg ≥8 assets, OM Iceberg + dbt ingestion), `demo-large` profile, startup order, resource trade-offs.
  - Update `docs/demo-runbook.md`: staged one-command-or-clearly-staged demo procedure for M1 Pro 16GB, including the guarded OpenMetadata Iceberg co-run window and teardown/recovery.
  - Update `docs/storage-ingestion.md`, `docs/transform-orchestration.md`: new tables, layers, schemas, build/docs commands, DAG task groups.
  - Update `data-generator/schema.md`: new tables/grains, `demo-large` row math, new DQ scenarios, measured runtime/RSS.
  - Update `versions.md`: any new pins/validations (OpenMetadata Iceberg connector, pyiceberg/ingestion extras), measured demo-large numbers, resolved/again-open risks.
  - Add an architecture overview (in `README.md` or `docs/system-architecture.md`) showing the DuckDB-logical vs Iceberg-physical distinction and the end-to-end flow.
  - Update `governance/openmetadata/README.md` and `lake/README.md` (owned in P4/P6, cross-checked here for consistency).

- **Functional (resource controls & rollback)**
  - Extend `make clean` to remove new generated artifacts (new export Parquet, dbt `target/`, any local ingestion output).
  - Document teardown: `make down` (all heavy profiles), MinIO bucket/namespace cleanup, Docker volume removal, venv removal.
  - Document rollback: revert the issue-3 feature branch/PR; generated data + Docker volumes remain gitignored and removable. (No PR #2 merge-order dependency remains — PR #2 is merged to `main`.)

- **Functional (verification suite — real, not mocked)** — run and capture:
  1. Determinism: `make seed SCALE=demo-large SEED=42` twice; diff `manifest.json` checksums (only `generated_at` differs). Record total rows ≥ 300,000.
  2. Load + health: `make load` (18 tables, counts match manifest); `make health`.
  3. dbt: `make dbt` (`dbt build`) on `medium` and `demo-large`; record PASS/WARN/ERROR + wall time; `make dbt-docs`.
  4. Rill: `make bi`; `rill start serving/rill`; confirm ≥8 explores non-empty; record URL.
  5. Iceberg: `make lake-up`, `make lake-publish`; record ≥8 published + read-back counts; `make down`.
  6. Governance: guarded co-run window; run Iceberg + dbt ingestion + `verify_catalog`; record summaries + URL; teardown.
  7. Airflow: `make airflow`. First confirm the modernized TaskFlow DAG (Airflow 3 `airflow.sdk` `@dag`/`@task`/`@task_group`) loads clean: record `airflow dags list` (shows `retail_batch_pipeline`), `airflow dags list-import-errors` (empty), and `airflow tasks list retail_batch_pipeline` (group-prefixed task IDs / group graph), plus a grep over the whole Airflow surface (`orchestration/airflow/` + the compose `airflow` service block) confirming **zero** `PythonOperator` / `airflow.operators` / `airflow.decorators` matches — Phase 5 removes the stale comments in `Dockerfile`, `requirements.txt`, and `docker-compose.yml`, so this grep is expected to be empty, not merely DAG-scoped. Then trigger a real DAG run and record the default run (`generate→load→transform→serve`) task-group state + URL. Then, for AC5's full-flow requirement, bring the `lake` profile up and **recreate the orchestration service with `LAKE_PROFILE_ENABLED=true`** (the flag is read at parse time, so recreate — not just re-trigger — to reparse the DAG; e.g. `LAKE_PROFILE_ENABLED=true docker compose --profile orchestration up -d --force-recreate`). Confirm `dags list-import-errors` still empty and `tasks list` now shows the `publish` group, then trigger and capture the **`publish` task group** (`publish_iceberg` + `iceberg_read_back`) completing green through the container-network endpoints (Phase 5). **Stop Airflow** (`make down` of orchestration) before the Phase-6 governance co-run window so the three heavy profiles never overlap.
  8. Hygiene: `docker compose config --quiet`; `python -m py_compile` on all touched scripts; secret scan (`/ck:security-scan` or `security-scan` skill); `git status` clean of generated artifacts.
  - Save the captured evidence to a **tracked** path `docs/verification/GH-3-full-flow-evidence.md`. Do **not** use `plans/reports/`: `.gitignore` ignores `plans/**/*`, so evidence stored there would be silently excluded from the implementation PR and AC8 would appear unmet on review. (`docs/` is tracked.)

- **Non-functional**
  - Record measured resource numbers (demo-large gen RSS/time, dbt build time/memory, co-run window peak) so the resource claims in docs are evidence-backed.

## Related Code Files

- Modify: `README.md`, `docs/demo-runbook.md`, `docs/storage-ingestion.md`, `docs/transform-orchestration.md`, `data-generator/schema.md`, `versions.md`.
- Create (optional): `docs/system-architecture.md` — end-to-end + logical/physical distinction.
- Modify: `Makefile` — `make clean` covers new artifacts.
- Create: `docs/verification/GH-3-full-flow-evidence.md` — captured run evidence (AC8), tracked so it ships in the PR.
- Reference (read-only): all phases' outputs.

## Implementation Steps

1. Update all docs to match the implemented behavior (do not document unbuilt features).
2. Extend `make clean`; document teardown/rollback.
3. Execute the full verification suite on M1 Pro 16GB in the documented staged order; capture evidence to `docs/verification/GH-3-full-flow-evidence.md` (tracked).
4. Run secret scan + `git status`; confirm no credentials/runtime artifacts staged.
5. Cross-check `lake/README.md` + `governance/openmetadata/README.md` for consistency with final behavior.
6. Reconcile any doc/plan drift (whole-plan consistency).

## Success Criteria

- [x] All ACs demonstrably met with captured evidence in `docs/verification/GH-3-full-flow-evidence.md` (tracked) (AC8).
- [x] Determinism verified on demo-large (checksums stable; total ≥ 300,000 rows) (AC1).
- [x] `dbt build` green with ≥8 documented marts; 4-layer lineage shown (AC2/AC3).
- [x] ≥8 Rill explores non-empty (AC4); ≥8 Iceberg assets read-back (AC6); Airflow full-flow visible + green (AC5).
- [x] OM Iceberg + dbt ingestion both complete with summaries captured (AC7).
- [x] Secret scan clean; `git status` free of credentials/runtime artifacts (AC9).
- [x] README/runbook explain startup order, resource trade-offs, architecture, teardown (AC10).
- [x] `make clean` removes all new generated artifacts; teardown/rollback documented.

## Risk Assessment

- **Evidence gaps:** if any heavy step can't be fully run on the target machine in one pass, run steps in the staged order and capture each independently; never fabricate results — record actual outcomes, including any partial/failed step with its output (per project rules).
- **Doc drift:** docs must describe only shipped behavior; run the whole-plan consistency sweep before declaring done.
- **Rollback:** this phase is docs/verification; rollback is reverting doc edits + Makefile clean changes. Feature rollback = revert the branch/PR (targets current `main`; no PR #2 dependency remains).
