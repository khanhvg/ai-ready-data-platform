# Repository current-state evidence for GitHub Issue #38

## Baseline and sources

- Repository root: `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-38-assessment-plan`.
- Inspected commit: `58a9b7f45f5b2d473a39bc2f9eb9258fe92d0b2a` (`Merge pull request #37 from khanhvg/cleanup/remove-learning-sandbox`); worktree was clean.
- Read in full: `README.md`, `.gitignore`, `Makefile`, `docker-compose.yml`, `.env.example`, `versions.md`, `docs/*.md`, and all eight Markdown files under `plans/260710-1145-GH-3-expand-lineage-dashboards-governance/`.
- Also inspected current Python entrypoints/configuration, dbt/Rill model surfaces, requirements, tracked test files, recent history, and cleanup commit `656322d`.

## Exact current implementation inventory

- Data generation: `data-generator/generate.py`, `data-generator/schema.md`, `data-generator/requirements.txt`; 18 deterministic retail CSV tables plus `data/raw/manifest.json`.
- Landing: `ingestion/load_raw.py`, `ingestion/requirements.txt`; creates 18 `raw.*` DuckDB tables in `warehouse/retail.duckdb`.
- Transformation: `transform/dbt/dbt_project.yml`, `profiles.yml`, `requirements.txt`; 18 `models/staging/stg_*.sql`, 6 `models/intermediate/int_*.sql`, 7 `models/core/dim_*.sql`, 9 `models/core/fct_*.sql`, and 11 `models/marts/mart_*.sql`.
- dbt contracts are in `_sources.yml`, `_staging__models.yml`, `_intermediate__models.yml`, `_core__models.yml`, and `_marts__models.yml`; they hold descriptions and generic tests. The sole singular test is `transform/dbt/tests/assert_non_negative_shipment_lead_time.sql`.
- Serving: `serving/export_marts_snapshot.py`; Rill has exactly 11 model SQL files, 11 metric YAML files, and 11 explore YAML files under `serving/rill/`, plus `rill.yaml` and `connectors/duckdb.yaml`.
- Curated lake: `lake/curated_assets.json` is the canonical 11-mart inventory; `lake/publish_iceberg.py` publishes and read-back checks them; `lake/README.md` documents the local REST-catalog path.
- Orchestration: `orchestration/airflow/dags/retail_batch_pipeline.py` is an Airflow 3 TaskFlow DAG; `orchestration/airflow/callables/pipeline.py` delegates to existing scripts; `Dockerfile` and `requirements.txt` define its image.
- Governance: `governance/openmetadata/ingestion/{iceberg_ingestion.yaml,dbt_ingestion.yaml,render_iceberg_ingestion.py,bootstrap_dbt_service.py}`, `verify_catalog.py`, and `README.md`.
- Root control/configuration is limited to `Makefile`, `docker-compose.yml`, `.env.example`, `.gitignore`, `release-manifest.json`, `versions.md`, and the user/architecture/runbook docs. There is no root `pyproject.toml`, package manifest, application package, or general-purpose test runner at this baseline.

## Commands and toolchain contracts

- Core workflow: `make seed SCALE=<small|medium|large|demo-large> SEED=<n>`, `make load`, `make health`, `make dbt`, `make dbt-docs`, `make bi`; `PROFILE=core` starts no containers (`Makefile`).
- Heavy workflow: `make airflow`, `make lake-up`, `make lake-publish`, `make catalog`, guarded `make catalog-ingest`, `make down`; cleanup is `make clean`.
- `make venv` builds `.venv` and installs only the three existing requirements files; an assessment package therefore needs an explicit dependency/test-install decision rather than assuming a root Python project.
- Pinned/tested matrix in `versions.md` and configs: Python 3.12, DuckDB 1.5.4, dbt-core 1.11.12, dbt-duckdb 1.10.1, Rill v0.87.8, `apache/airflow:3.1.0-python3.12`, Lakekeeper v0.13.1, MinIO `RELEASE.2025-09-07T16-13-09Z`, OpenMetadata 1.6.5 / ingestion 1.6.5.0, MySQL 8.3, Elasticsearch 8.11.4.
- Airflow public contract is `airflow.sdk` decorators with no `PythonOperator`; its visible order is generate → load → transform → serve, with optional publish (`README.md`, `docs/transform-orchestration.md`).
- The shared DuckDB file has a single-writer contract. Rill reads exported Parquet instead of attaching the live database (`docs/system-architecture.md`).
- Secrets remain environment-provided. `.env*` is ignored except `.env.example`; `make catalog-ingest` requires `OPENMETADATA_JWT_TOKEN`. Local Compose defaults are explicitly non-production.

## Tests and proof already present

- There is no pytest/unit/integration suite in the surviving repository. `rg` finds only the dbt singular SQL test above; dbt YAML generic tests run through `dbt build`.
- `make health` proves the DuckDB file opens read-only and that `raw` contains tables.
- `make dbt` runs models and tests together; `make dbt-docs` emits `manifest.json`/`catalog.json`.
- Lake publication performs table read-back; `governance/openmetadata/verify_catalog.py` verifies physical Iceberg and logical dbt catalog/lineage expectations.
- `docs/verification/GH-3-full-flow-evidence.md` is the tracked empirical record: demo-large 620,340 rows, low generator RSS, 45 dbt models, 11 marts/Rill explores/Iceberg assets, and OpenMetadata logical/physical lineage. These are existing platform facts, not Issue #38 assessment tests.

## Generated/runtime-data boundary

- Ignored local artifacts: `.venv/`, `data/raw/*.csv`, `data/raw/manifest.json`, `warehouse/*.duckdb{,.wal}`, `serving/export/*.parquet`, Rill `.rill/`/`tmp/`, dbt `target/`/`logs/`/`dbt_packages/`/`.user.yml`, Airflow logs/database, local lake/governance data, and `.env*` (`.gitignore`).
- Docker named volumes (`airflow-home`, `minio-data`, `lakekeeper-db-data`, `openmetadata-db-data`, `openmetadata-es-data`) survive `make down`; full reset requires Compose volume deletion (`README.md`).
- Plans are ignored by `plans/**/*` unless force-added. Shippable Issue #38 evidence should follow the established `docs/verification/` pattern, not rely on an untracked plan report.
- Implementation and verification inputs must be synthetic/sanitized. The product records architect-led engagement answers; it does not assess repository readiness or scan customer systems. Offline assessment tests need no cloud apply, credentials, customer data, or live services.

## Data-platform capabilities already proven

- Deterministic, bounded, streaming synthetic generation for four profiles; manifest row counts, SHA-256 checksums, quality observations, and seed/profile metadata.
- Idempotent raw DuckDB landing; layered source → staging → intermediate → core → mart lineage; schema/data-quality tests and dbt documentation artifacts.
- Eleven business marts delivered consistently to Parquet/Rill and Iceberg via one canonical asset list.
- Airflow TaskFlow orchestration, optional-profile gating, lake read-back, and dual OpenMetadata representation: 45 logical dbt tables/130 lineage edges versus 11 physical Iceberg assets.
- A documented MacBook M1 Pro 16GB operating model and reproducible evidence/runbook already exist.

## Resource constraints Issue #38 must preserve

- `docker-compose.yml` caps Airflow at 4g; MinIO 1g; MinIO init 256m; Lakekeeper DB/migration 512m each; Lakekeeper 1g; OpenMetadata DB 1g; search 1g; server 2g.
- Normal operation permits only one heavy profile. `make catalog-ingest` is the sole guarded lake+governance co-run: it stops Airflow, health-polls services, ingests, verifies, then stops lake.
- `demo-large` is already streamed (~78–92 MB measured RSS). Assessment commands should default to static checks/small fixtures and must not auto-start Airflow, lake, or governance.

## Cleanup boundary and consequences for Issue #38

- Commit `656322d` (`chore: remove learning sandbox and interactive labs`) removed `apps/lab-runner/`, `apps/learning-portal/`, all `learning/`, architecture/rendered curricula, learning OpenAPI/data contracts, `mk/issue-5/`, and the enterprise-learning plan. It also removed their extensive Python/Node/security/race/e2e tests and trimmed the root Makefile.
- Therefore Issue #38 starts from a deliberate data-platform-only repository. It must not restore a browser portal, privileged container runner, interactive labs, learner progress/evidence APIs, or the deleted broad curriculum contract system unless separately authorized.
- The surviving repo has no assessment schema, rubric, question bank, evaluator, scoring/report contract, CLI, Make target, or native automated test harness. Those are the concrete gaps Issue #38 must add.

## Evidence-based likely module and command boundaries

- Prefer a self-contained `assessment/` boundary: versioned static contracts/content, deterministic customer-assessment domain services under `assessment/src/`, fixtures under `assessment/tests/fixtures/`, and tests under `assessment/tests/`.
- Keep platform truth referenced from existing sources (`lake/curated_assets.json`, dbt YAML, `release-manifest.json`, `versions.md`) rather than copying counts into a second mutable inventory.
- Provide one non-interactive local entrypoint such as `python -m assessment ...` (or a thin script if avoiding a root package), with stable machine-readable output and an optional human-readable report. Do not bind it to Airflow/OpenMetadata startup.
- Add narrow Make targets consistent with current naming, likely `assessment`, `assessment-test`, and optionally `assessment-verify`; keep them out of `make up` and heavy profiles.
- Acceptance tests should cover deterministic scoring, schema validation, missing/malformed evidence, stale claimed counts, no-secret/customer-data fixtures, offline execution, and a memory-light default. Generated assessment reports need an explicit tracked-vs-ignored policy; durable release evidence belongs under `docs/verification/`.

## Planning implications

- Treat the assessment package as a new bounded capability over proven repository evidence, not a redesign of the data platform and not a resurrection of the deleted learning product.
- Separate architect-entered customer assessment from optional demo-artifact verification. The web must not invoke existing commands; staged implementation verification that invokes them must preserve profiles, single-writer discipline, teardown, and credential boundaries.
- Document whether report content comes from customer answers/evidence, architect judgment, catalog guidance, or demo illustration; never present absent demo services as a failed customer capability.
