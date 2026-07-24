PROFILE ?= core
SCALE ?= small
SEED ?= 42
VENV := .venv
PY := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
DBT := $(VENV)/bin/dbt
METADATA := $(VENV)/bin/metadata
PYENV := env -u PYTHONPATH
DBT_PROJECT_DIR := transform/dbt
DBT_PROFILES_DIR := transform/dbt
RUNNING_LAKE := docker ps --filter name=retail-minio --filter name=retail-lakekeeper --format '{{.Names}}'
RUNNING_GOVERNANCE := docker ps --filter name=retail-openmetadata --format '{{.Names}}'
# Only openmetadata-server has no own-health depender in docker-compose.yml, so
# `docker compose up -d` returns before it (or lakekeeper) finishes booting;
# catalog-ingest polls both explicitly instead of racing the ingestion calls
# against a container that's still starting.
CATALOG_INGEST_HEALTH_RETRIES := 30
ASSESSMENT_VENV := .assessment-venv
ASSESSMENT_PY := $(ASSESSMENT_VENV)/bin/python
ASSESSMENT_PIP := $(ASSESSMENT_VENV)/bin/pip
ASSESSMENT_CLI := $(ASSESSMENT_VENV)/bin/assessment-prototype
ASSESSMENT_FIXTURES := assessment/tests/fixtures/scenarios/0.1.0
ASSESSMENT_OFFLINE := assessment/tools/run-offline.sh

.PHONY: venv up down seed load health dbt dbt-docs airflow bi catalog lake-up lake-publish catalog-ingest clean \
	assessment-install assessment-schema assessment-contract assessment-scenarios assessment-calibration \
	assessment-report assessment-test assessment-lint assessment-typecheck assessment-build assessment-clean

venv: $(VENV)/bin/python3

$(VENV)/bin/python3:
	python3 -m venv $(VENV)
	$(PYENV) $(PIP) install --quiet --upgrade pip
	$(PYENV) $(PIP) install --quiet \
		-r data-generator/requirements.txt \
		-r ingestion/requirements.txt \
		-r transform/dbt/requirements.txt

up: venv
ifeq ($(PROFILE),core)
	@echo "core profile is local-only (DuckDB embedded + CLI tools) -- no containers to start."
	@echo "Run 'make seed', 'make load', 'make dbt', 'make bi' directly."
else
	docker compose --profile $(PROFILE) up -d
endif

down:
	docker compose --profile orchestration --profile lake --profile governance down

seed: venv
	$(PYENV) $(PY) data-generator/generate.py --profile $(SCALE) --seed $(SEED) \
		$(if $(MAX_ORDERS),--max-orders $(MAX_ORDERS)) \
		$(if $(MAX_WEB_EVENTS),--max-web-events $(MAX_WEB_EVENTS))

load: venv
	$(PYENV) $(PY) ingestion/load_raw.py

health:
	$(PYENV) $(PY) -c "import duckdb, pathlib; \
		p = pathlib.Path('$${DUCKDB_PATH:-warehouse/retail.duckdb}'); \
		assert p.exists(), f'DuckDB file missing: {p}'; \
		con = duckdb.connect(str(p), read_only=True); \
		tables = con.sql(\"select table_schema, table_name from information_schema.tables where table_schema='raw'\").fetchall(); \
		assert tables, 'raw schema has no tables -- run make load first'; \
		print(f'OK: {p} opens read-only, raw schema has {len(tables)} tables')"

dbt: venv
	cd $(DBT_PROJECT_DIR) && $(PYENV) DBT_PROFILES_DIR=$(CURDIR)/$(DBT_PROFILES_DIR) $(CURDIR)/$(DBT) build

dbt-docs: venv
	cd $(DBT_PROJECT_DIR) && $(PYENV) DBT_PROFILES_DIR=$(CURDIR)/$(DBT_PROFILES_DIR) $(CURDIR)/$(DBT) docs generate

airflow:
	docker compose --profile orchestration up -d

bi: venv
	$(PYENV) $(PY) serving/export_marts_snapshot.py
	@echo "Run 'rill start serving/rill' (see docs/demo-runbook.md) to open the dashboard."
	@echo "First time only: install the Rill CLI -- curl https://cdn.rilldata.com/install.sh | sh"

catalog:
	@test -z "$$($(RUNNING_LAKE))" || (echo "Refusing to start governance while lake containers are running on a 16GB laptop. Run 'make down' first." && exit 1)
	docker compose --profile governance up -d

lake-up:
	@test -z "$$($(RUNNING_GOVERNANCE))" || (echo "Refusing to start lake while governance containers are running on a 16GB laptop. Run 'make down' first." && exit 1)
	docker compose --profile lake up -d

lake-publish: venv
	$(PYENV) $(PY) lake/publish_iceberg.py

# Guarded, explicit opt-in co-run window: the only place `lake` and
# `governance` run together, and only after `orchestration` is stopped, so the
# peak is never all three heavy profiles at once. Bypasses the RUNNING_LAKE/
# RUNNING_GOVERNANCE mutual-exclusion guard on purpose -- catalog/lake-up keep
# refusing accidental co-run for every other workflow.
catalog-ingest: venv
	@test -n "$$OPENMETADATA_JWT_TOKEN" || (echo "OPENMETADATA_JWT_TOKEN is not set -- export an ingestion-bot JWT first (Settings -> Bots -> ingestion-bot in the OpenMetadata UI; see governance/openmetadata/README.md)." && exit 1)
	@echo "Stopping orchestration (Airflow) so the co-run window is lake+governance only..."
	docker compose --profile orchestration down
	@echo "Starting lake + governance together for the ingestion window..."
	docker compose --profile lake --profile governance up -d
	@echo "Waiting for lakekeeper and openmetadata-server health (up to $(CATALOG_INGEST_HEALTH_RETRIES)x5s each)..."
	@for svc in retail-lakekeeper retail-openmetadata-server; do \
		ok=0; \
		for i in $$(seq 1 $(CATALOG_INGEST_HEALTH_RETRIES)); do \
			status=$$(docker inspect $$svc --format '{{.State.Health.Status}}' 2>/dev/null); \
			if [ "$$status" = "healthy" ]; then ok=1; break; fi; \
			sleep 5; \
		done; \
		if [ "$$ok" != "1" ]; then echo "$$svc did not become healthy in time." >&2; exit 1; fi; \
	done
	$(PYENV) $(PIP) install --quiet "openmetadata-ingestion[iceberg,dbt]==1.6.5.0"
	$(PYENV) $(PY) governance/openmetadata/ingestion/render_iceberg_ingestion.py --check
	MINIO_ROOT_USER=$${MINIO_ROOT_USER:-minioadmin} MINIO_ROOT_PASSWORD=$${MINIO_ROOT_PASSWORD:-minioadmin_local_only} $(PYENV) $(PY) lake/publish_iceberg.py --skip-read-back
	MINIO_ROOT_USER=$${MINIO_ROOT_USER:-minioadmin} MINIO_ROOT_PASSWORD=$${MINIO_ROOT_PASSWORD:-minioadmin_local_only} $(PYENV) $(METADATA) ingest -c governance/openmetadata/ingestion/iceberg_ingestion.yaml
	$(MAKE) dbt-docs
	REPO_ROOT=$(CURDIR) $(PYENV) $(PY) governance/openmetadata/ingestion/bootstrap_dbt_service.py
	REPO_ROOT=$(CURDIR) $(PYENV) $(METADATA) ingest -c governance/openmetadata/ingestion/dbt_ingestion.yaml
	$(PYENV) $(PY) governance/openmetadata/verify_catalog.py
	@echo "Tearing down lake (governance stays up for browsing -- 'make down' to stop it too)."
	docker compose --profile lake down

assessment-install:
	python3.12 -m venv --clear $(ASSESSMENT_VENV)
	$(PYENV) $(ASSESSMENT_PIP) install --quiet --upgrade "pip==25.1.1"
	$(PYENV) $(ASSESSMENT_PIP) install --quiet --require-hashes -r assessment/requirements.lock
	$(PYENV) $(ASSESSMENT_PIP) install --quiet --require-hashes -r assessment/requirements-dev.lock
	$(PYENV) $(ASSESSMENT_PIP) install --quiet --no-deps assessment/

assessment-schema:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) schema

assessment-contract:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) contract --fixture-root $(ASSESSMENT_FIXTURES)

assessment-scenarios:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) scenarios --fixture-root $(ASSESSMENT_FIXTURES)

assessment-calibration:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) calibration --fixture-root $(ASSESSMENT_FIXTURES)

assessment-report:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) report --verify-stability --fixture-root $(ASSESSMENT_FIXTURES)

assessment-test:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_PY) -m pytest -q assessment/tests

assessment-lint:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_VENV)/bin/ruff check assessment

assessment-typecheck:
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_VENV)/bin/mypy assessment/prototype

assessment-build:
	cd assessment && $(CURDIR)/$(ASSESSMENT_OFFLINE) $(CURDIR)/$(ASSESSMENT_PY) -m build --no-isolation
	$(PYENV) $(ASSESSMENT_OFFLINE) $(ASSESSMENT_CLI) build-check assessment/dist

assessment-clean:
	python3 -c "import pathlib, shutil; [shutil.rmtree(pathlib.Path(p), ignore_errors=True) for p in ['assessment/.generated','assessment/.pytest_cache','assessment/.mypy_cache','assessment/.ruff_cache','assessment/build','assessment/dist','assessment/ai_ready_assessment_prototype.egg-info']]"

clean:
	python3 -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('$(VENV)'), pathlib.Path('transform/dbt/target'), pathlib.Path('transform/dbt/logs'), pathlib.Path('transform/dbt/dbt_packages'), pathlib.Path('serving/rill/.rill'), pathlib.Path('serving/rill/tmp')]]; [p.unlink(missing_ok=True) for pattern in ['data/raw/*.csv','serving/export/*.parquet','warehouse/*.duckdb','warehouse/*.duckdb.wal'] for p in pathlib.Path('.').glob(pattern)]; pathlib.Path('data/raw/manifest.json').unlink(missing_ok=True); pathlib.Path('transform/dbt/.user.yml').unlink(missing_ok=True)"
	find . -name .DS_Store -type f -delete
