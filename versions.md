# Version Matrix

Proven by the P1 compatibility spike (2026-07-09) on macOS arm64 (M1 Pro), Python 3.12.3, in a
throwaway venv. This replaces the plan's *candidate* matrix with the actually-tested one.

| Component | Version | Notes |
|---|---|---|
| Python | 3.12.x | matches local toolchain |
| duckdb (Python package) | 1.5.4 | latest at spike time; supersedes the plan's DuckDB 1.4.x LTS candidate |
| dbt-core | 1.11.12 | pulled in transitively by dbt-duckdb |
| dbt-duckdb | 1.10.1 | adapter; `dbt run` verified against a live DuckDB 1.5.4 file |
| dbt-adapters | 1.24.4 | transitive |
| DuckDB `iceberg` extension | bundled w/ duckdb 1.5.4 | `INSTALL/LOAD iceberg` verified |
| DuckDB `httpfs` extension | bundled w/ duckdb 1.5.4 | required for S3/MinIO access; verified |
| Rill Developer | v0.87.8 | CLI binary verified (`rill version`); embeds its own DuckDB — see R2 below |
| Apache Airflow | 3.x (installed in `orchestration` extra, see `orchestration/airflow/requirements.txt`) | LocalExecutor/standalone, minimal providers; DAG uses the `airflow.sdk` TaskFlow API (`@dag`/`@task`/`@task_group`), not `PythonOperator` (Phase 5 rewrite) |
| MinIO | `RELEASE.2025-09-07T16-13-09Z` (`minio/minio`) | `lake` profile only; pinned instead of `latest` for reproducible pulls |
| Lakekeeper (Iceberg REST catalog) | `v0.13.1` (`quay.io/lakekeeper/catalog`) | `lake` profile only — required for DuckDB Iceberg **writes** (raw S3 path insufficient); pinned instead of `latest-main` |
| OpenMetadata | `1.6.5` (`docker.getcollate.io/openmetadata/server`) | `governance` profile only. `openmetadata-ingestion[iceberg,dbt]==1.6.5.0` ingests **both** the physical Iceberg tables (via its Iceberg RestCatalog connector, pyiceberg 0.5.1) and the logical dbt artifacts (`governance/openmetadata/`) — see the Phase 6 spike below. No native DuckDB connector, so the dbt-sourced `retail_duckdb` service is bootstrapped from dbt's own `catalog.json`, not a live crawl. |

## Issue #38 Phase 1–7 assessment package

The assessment uses its own `.assessment-venv` and hash-locked dependency files. Verified on
macOS arm64 with Python 3.12.3:

| Component | Version |
|---|---:|
| Package | `0.6.0` |
| Prototype framework/schema | `0.1.0-prototype` |
| Public contracts/archive format | `1.0.0` |
| pip | 25.1.1 |
| pip-tools lock compiler | 7.5.0 |
| Jinja2 | 3.1.6 |
| FastAPI / Starlette | 0.140.0 / 1.3.1 |
| Uvicorn | 0.51.0 |
| ItsDangerous | 2.2.0 |
| python-multipart | 0.0.32 |
| PyYAML | 6.0.2 |
| Pydantic | 2.11.7 |
| JSON Schema | jsonschema 4.24.0 |
| Evidence image canonicalization | Pillow 11.3.0 |
| pytest | 8.4.1 |
| Playwright | 1.61.0 |
| Chromium | Chrome for Testing 149.0.7827.55 |
| HTTP test client | httpx2 2.9.1 |
| Ruff | 0.12.4 |
| mypy | 1.16.1 |
| build | 1.2.2.post1 |
| setuptools / wheel | 80.9.0 / 0.45.1 |

Only dependency acquisition and deliberate lock compilation may use the package index. Schema,
contract, scenario, calibration, engine, report, local-store, migration, import/export,
portability, security, test, lint, typecheck, and build commands are process-local and use the
shared network-denying wrapper. Phase 4 browser installation is a separate bounded target.
Browser acceptance uses one pinned Chromium worker and a loopback-only sandbox that denies
external network requests.

Phase 6 also verified the fixed policy interface on Python 3.12.3 and DuckDB 1.5.4. Raw,
staging, classified-email, unknown role, and unknown asset cases fail nonzero; the one governed
product succeeds; attempted SQL and output-path arguments are rejected by the parser. PyYAML
6.0.3 and jsonschema 4.26.0 are explicitly pinned for the core policy/manifest verification
surface. The limitation is intentional: this is application authorization, not DuckDB IAM.

## Phase 6 compatibility spike: OpenMetadata 1.6.5 Iceberg connector vs Lakekeeper v0.13.1

**Outcome: PASS.** The pinned `openmetadata-ingestion[iceberg]==1.6.5.0` (pyiceberg 0.5.1,
`RestCatalog` + `PyArrowFileIO`) reaches Lakekeeper v0.13.1 + MinIO and lists/loads the
curated Iceberg tables published by `lake/publish_iceberg.py`, using the same
auth posture that script already proved out (no bearer token, no vended storage
credentials -- pyiceberg's REST client sends neither by default, matching
Lakekeeper's `AUTHORIZATION_TYPE 'none'` / `ACCESS_DELEGATION_MODE 'none'`).

Spiked directly against the connector's own classes
(`metadata.ingestion.source.database.iceberg.catalog.rest.IcebergRestCatalog`)
before building the full ingestion workflow, per the plan's compatibility-gate-first
ordering:

```
catalog = IcebergRestCatalog.get_catalog(IcebergCatalog(
    name="retail", warehouseLocation="retail",
    connection=RestCatalogConnection(
        uri="http://localhost:8181/catalog",
        fileSystem=IcebergFileSystem(type=AWSCredentials(
            awsAccessKeyId=..., awsSecretAccessKey=..., awsRegion="local",
            endPointURL="http://localhost:9000")),
    ),
))
list(catalog.list_namespaces())  # -> [('retail',)]
list(catalog.list_tables(('retail',)))  # -> all 11 curated marts
```

Two real, non-obvious findings from the spike and the full end-to-end run that follow
it (`governance/openmetadata/ingestion/iceberg_ingestion.yaml`):

- **Catalog-connection union is ambiguous without `ssl: null`.** OM's
  `IcebergCatalog.connection` is `Union[HiveCatalogConnection, RestCatalogConnection, ...]`
  with no discriminator field, and both Hive and Rest accept a bare `{uri, fileSystem}` --
  pydantic resolves the ambiguous case to `HiveCatalogConnection` (first in the union),
  which then fails at runtime with `Apache Hive support not installed`. Setting the
  Rest-only field `ssl: null` (a no-op) is what disambiguates to `RestCatalogConnection`.
- **Host, not container, endpoints.** `metadata ingest` was run from the host venv
  (matching the existing `dbt_ingestion.yaml` convention), so `iceberg_ingestion.yaml`
  uses `http://localhost:8181/catalog` / `http://localhost:9000`, not the container-network
  `lakekeeper`/`minio` hostnames Airflow's `publish` task group uses internally.

Real end-to-end result (`make catalog-ingest`, 2026-07-10): Iceberg ingestion listed all
11 curated marts under the `retail_iceberg` service (0 errors, 100% success). See
`governance/openmetadata/README.md` for the full workflow and the separate dbt-service
bootstrap finding (OM 1.6.5's dbt connector only enriches pre-existing Table entities;
it does not create them).

## Spike evidence

```
$ python3 -c "import duckdb; print(duckdb.__version__)"
1.5.4
$ dbt --version
Core: installed 1.11.12 - Up to date!
Plugins: duckdb 1.10.1 - Up to date!
$ dbt run   # trivial model against a real DuckDB file
Done. PASS=1 WARN=0 ERROR=0 SKIP=0 NO-OP=0 TOTAL=1
$ python3 -c "import duckdb; c=duckdb.connect(':memory:'); c.execute('INSTALL iceberg'); c.execute('LOAD iceberg')"
iceberg extension loaded OK
$ ./rill version
rill version v0.87.8
```

## Resolved risks from the plan

- **R1 (Iceberg write needs a catalog):** confirmed — DuckDB's `iceberg` extension attaches to a REST
  catalog for writes. `lake` profile ships MinIO + Lakekeeper. See `lake/README.md` for the exact
  `ATTACH` syntax and the write→read-back smoke test (P4).
- **R2 (Rill embeds its own DuckDB):** confirmed via CLI install — Rill's supported ingestion path is
  its own embedded DuckDB. Default Rill source in this repo is the **exported Parquet snapshot** of
  the marts (`serving/export_marts_snapshot.py`), not a direct attach to the shared pipeline
  `.duckdb` file. This makes the DuckDB-version mismatch (pipeline 1.5.4 vs Rill's bundled DuckDB)
  irrelevant, since Parquet is the interchange format.
- **R3 (M1 16GB budget):** `core` measured in P1 (see `docs/`); heavier profiles (`orchestration`,
  `lake`, `governance`) stay opt-in and are run one-at-a-time.

## Re-running the spike

```bash
python3 -m venv /tmp/ck-spike && source /tmp/ck-spike/bin/activate
unset PYTHONPATH   # required if a global PYTHONPATH leaks a different interpreter's site-packages
pip install duckdb dbt-duckdb
dbt --version
```
