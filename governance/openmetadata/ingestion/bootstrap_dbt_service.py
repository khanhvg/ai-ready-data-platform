#!/usr/bin/env python3
"""Pre-register the `retail_duckdb` logical service and its dbt-model tables.

OM 1.6.5's dbt connector only *enriches* Table entities that already exist in
the catalog (it looks them up via `es_search_from_fqn`; it never creates one) --
confirmed empirically: `metadata ingest -c dbt_ingestion.yaml` completes with
0 errors but attaches nothing when no Table entities pre-exist. There is no
native DuckDB connector to crawl these tables live (versions.md), so this
script is the required bootstrap step run once per fresh `retail_duckdb`
service, before `metadata ingest -c dbt_ingestion.yaml`, inside the guarded
`make catalog-ingest` window. It only ever seeds real schema (dbt's own
catalog.json, itself produced from a live `information_schema` query against
the DuckDB warehouse) -- no fabricated columns or row data.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from metadata.generated.schema.api.data.createDatabase import CreateDatabaseRequest
from metadata.generated.schema.api.data.createDatabaseSchema import (
    CreateDatabaseSchemaRequest,
)
from metadata.generated.schema.api.data.createTable import CreateTableRequest
from metadata.generated.schema.api.services.createDatabaseService import (
    CreateDatabaseServiceRequest,
)
from metadata.generated.schema.entity.data.table import Column, DataType
from metadata.generated.schema.entity.services.connections.database.customDatabaseConnection import (
    CustomDatabaseConnection,
    CustomDatabaseType,
)
from metadata.generated.schema.entity.services.databaseService import (
    DatabaseConnection,
    DatabaseServiceType,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    AuthProvider,
    OpenMetadataConnection,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

REPO_ROOT = Path(__file__).resolve().parents[3]
MANIFEST_PATH = REPO_ROOT / "transform" / "dbt" / "target" / "manifest.json"
CATALOG_PATH = REPO_ROOT / "transform" / "dbt" / "target" / "catalog.json"
SERVICE_NAME = "retail_duckdb"

# DuckDB's `information_schema` type names (as dbt's catalog.json records them)
# mapped onto OpenMetadata's DataType enum; anything unlisted falls back to STRING.
_DUCKDB_TYPE_MAP = {
    "BIGINT": DataType.BIGINT,
    "INTEGER": DataType.INT,
    "SMALLINT": DataType.SMALLINT,
    "TINYINT": DataType.TINYINT,
    "DOUBLE": DataType.DOUBLE,
    "FLOAT": DataType.FLOAT,
    "DECIMAL": DataType.DECIMAL,
    "BOOLEAN": DataType.BOOLEAN,
    "VARCHAR": DataType.VARCHAR,
    "DATE": DataType.DATE,
    "TIMESTAMP": DataType.TIMESTAMP,
    "TIMESTAMP WITH TIME ZONE": DataType.TIMESTAMPZ,
    "TIME": DataType.TIME,
    "BLOB": DataType.BLOB,
    "UUID": DataType.UUID,
}


_LENGTHED_TYPES = {DataType.VARCHAR, DataType.CHAR, DataType.BINARY, DataType.VARBINARY}
# DuckDB VARCHAR/BLOB are unbounded (no declared length in catalog.json); OM
# requires a non-null dataLength for these types regardless, so this is a
# fixed placeholder, not a real observed constraint.
_UNBOUNDED_LENGTH_PLACEHOLDER = 65535


def _map_data_type(duckdb_type: str) -> DataType:
    base = duckdb_type.split("(")[0].strip().upper()
    return _DUCKDB_TYPE_MAP.get(base, DataType.STRING)


def _column_kwargs(duckdb_type: str) -> dict:
    data_type = _map_data_type(duckdb_type)
    kwargs = {"dataType": data_type, "dataTypeDisplay": duckdb_type}
    if data_type in _LENGTHED_TYPES:
        kwargs["dataLength"] = _UNBOUNDED_LENGTH_PLACEHOLDER
    return kwargs


def _client() -> OpenMetadata:
    jwt_token = os.environ.get("OPENMETADATA_JWT_TOKEN")
    if not jwt_token:
        raise SystemExit("OPENMETADATA_JWT_TOKEN is not set.")
    connection = OpenMetadataConnection(
        hostPort=os.environ.get("OPENMETADATA_HOST_PORT", "http://localhost:8585/api"),
        authProvider=AuthProvider.openmetadata,
        securityConfig=OpenMetadataJWTClientConfig(jwtToken=jwt_token),
    )
    return OpenMetadata(connection)


def _ensure_service(metadata: OpenMetadata) -> None:
    metadata.create_or_update(
        CreateDatabaseServiceRequest(
            name=SERVICE_NAME,
            serviceType=DatabaseServiceType.CustomDatabase,
            description=(
                "Logical DuckDB warehouse (schemas main_staging/main_intermediate/"
                "main_core/main_marts). Table schemas seeded from dbt's catalog.json; "
                "lineage/descriptions/tests enriched by dbt_ingestion.yaml. Not a live "
                "crawl -- no native DuckDB connector (versions.md)."
            ),
            connection=DatabaseConnection(
                config=CustomDatabaseConnection(type=CustomDatabaseType.CustomDatabase)
            ),
        )
    )


def _materialized_models(manifest: dict) -> dict:
    return {
        key: node
        for key, node in manifest["nodes"].items()
        if node.get("resource_type") == "model"
        and node.get("config", {}).get("materialized") != "ephemeral"
    }


def bootstrap() -> int:
    with MANIFEST_PATH.open() as f:
        manifest = json.load(f)
    with CATALOG_PATH.open() as f:
        catalog = json.load(f)

    models = _materialized_models(manifest)
    catalog_nodes = catalog.get("nodes", {})

    metadata = _client()
    _ensure_service(metadata)

    seen_databases: set[str] = set()
    seen_schemas: set[tuple[str, str]] = set()
    tables_created = 0

    for key, node in models.items():
        database_name = node["database"]
        schema_name = node["schema"]
        table_name = node["name"]

        if database_name not in seen_databases:
            metadata.create_or_update(
                CreateDatabaseRequest(name=database_name, service=SERVICE_NAME)
            )
            seen_databases.add(database_name)

        if (database_name, schema_name) not in seen_schemas:
            metadata.create_or_update(
                CreateDatabaseSchemaRequest(
                    name=schema_name,
                    database=f"{SERVICE_NAME}.{database_name}",
                )
            )
            seen_schemas.add((database_name, schema_name))

        catalog_columns = catalog_nodes.get(key, {}).get("columns", {})
        columns = [
            Column(name=col["name"], **_column_kwargs(col["type"]))
            for col in sorted(catalog_columns.values(), key=lambda c: c["index"])
        ] or [Column(name="_placeholder", dataType=DataType.STRING)]

        metadata.create_or_update(
            CreateTableRequest(
                name=table_name,
                databaseSchema=f"{SERVICE_NAME}.{database_name}.{schema_name}",
                columns=columns,
                description=node.get("description") or None,
            )
        )
        tables_created += 1

    print(
        f"Bootstrapped {SERVICE_NAME}: {len(seen_databases)} database(s), "
        f"{len(seen_schemas)} schema(s), {tables_created} table(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(bootstrap())
