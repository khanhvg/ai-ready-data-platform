PROFILE ?= core
SCALE ?= small
SEED ?= 42
VENV := .venv
PY := $(VENV)/bin/python3
PIP := $(VENV)/bin/pip
DBT := $(VENV)/bin/dbt
PYENV := env -u PYTHONPATH
DBT_PROJECT_DIR := transform/dbt
DBT_PROFILES_DIR := transform/dbt
RUNNING_LAKE := docker ps --filter name=retail-minio --filter name=retail-lakekeeper --format '{{.Names}}'
RUNNING_GOVERNANCE := docker ps --filter name=retail-openmetadata --format '{{.Names}}'

.PHONY: venv up down seed load health dbt airflow bi catalog lake-up lake-publish clean

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
	$(PYENV) $(PY) data-generator/generate.py --profile $(SCALE) --seed $(SEED)

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
	cd $(DBT_PROJECT_DIR) && $(PYENV) DBT_PROFILES_DIR=$(CURDIR)/$(DBT_PROFILES_DIR) $(CURDIR)/$(DBT) run
	cd $(DBT_PROJECT_DIR) && $(PYENV) DBT_PROFILES_DIR=$(CURDIR)/$(DBT_PROFILES_DIR) $(CURDIR)/$(DBT) test

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

clean:
	python3 -c "import pathlib, shutil; [shutil.rmtree(p, ignore_errors=True) for p in [pathlib.Path('$(VENV)')]]; [p.unlink(missing_ok=True) for pattern in ['data/raw/*.csv','serving/export/*.parquet','warehouse/*.duckdb','warehouse/*.duckdb.wal'] for p in pathlib.Path('.').glob(pattern)]; pathlib.Path('data/raw/manifest.json').unlink(missing_ok=True)"
	find . -name .DS_Store -type f -delete
