#!/usr/bin/env python3
"""Print evidence that both OpenMetadata ingestion workflows populated the catalog.

Host-side check (not an Airflow callable, per plan decision 1): queries the
OpenMetadata REST API for the physical Iceberg service (`retail_iceberg`) and the
logical dbt service (`retail_duckdb`), and sums lineage edges across the dbt-sourced
tables. Exits non-zero if either service has zero tables, since that would mean
`make catalog-ingest` silently produced an empty catalog.
"""
from __future__ import annotations

import os
import sys

from metadata.generated.schema.entity.data.table import Table
from metadata.generated.schema.entity.services.connections.metadata.openMetadataConnection import (
    AuthProvider,
    OpenMetadataConnection,
)
from metadata.generated.schema.security.client.openMetadataJWTClientConfig import (
    OpenMetadataJWTClientConfig,
)
from metadata.ingestion.ometa.ometa_api import OpenMetadata

ICEBERG_SERVICE = "retail_iceberg"
DBT_SERVICE = "retail_duckdb"
DEFAULT_HOST_PORT = "http://localhost:8585/api"


def _client() -> OpenMetadata:
    jwt_token = os.environ.get("OPENMETADATA_JWT_TOKEN")
    if not jwt_token:
        raise SystemExit(
            "OPENMETADATA_JWT_TOKEN is not set. Export an ingestion-bot JWT "
            "(Settings -> Bots -> ingestion-bot in the OpenMetadata UI) first."
        )
    connection = OpenMetadataConnection(
        hostPort=os.environ.get("OPENMETADATA_HOST_PORT", DEFAULT_HOST_PORT),
        authProvider=AuthProvider.openmetadata,
        securityConfig=OpenMetadataJWTClientConfig(jwtToken=jwt_token),
    )
    return OpenMetadata(connection)


def _tables_for_service(metadata: OpenMetadata, service_name: str) -> list[Table]:
    """`/v1/tables` has no working per-service filter in 1.6.5 (confirmed empirically:
    `service=<name>` is silently ignored server-side), so filter client-side instead."""
    return [
        table
        for table in metadata.list_all_entities(entity=Table, fields=["service"])
        if table.service.name == service_name
    ]


def count_lineage_edges(metadata: OpenMetadata, tables: list[Table]) -> int:
    """Sum upstream+downstream lineage edges across the given tables."""
    edges = 0
    for table in tables:
        lineage = metadata.get_lineage_by_name(
            entity=Table, fqn=table.fullyQualifiedName.root, up_depth=1, down_depth=1
        )
        if lineage:
            edges += len(lineage.get("upstreamEdges", [])) + len(lineage.get("downstreamEdges", []))
    return edges


def main() -> None:
    metadata = _client()

    iceberg_tables = _tables_for_service(metadata, ICEBERG_SERVICE)
    dbt_tables = _tables_for_service(metadata, DBT_SERVICE)
    dbt_lineage_edges = count_lineage_edges(metadata, dbt_tables)

    print("OpenMetadata catalog summary:")
    print(f"  {ICEBERG_SERVICE} (physical Iceberg tables): {len(iceberg_tables)} table(s)")
    print(f"  {DBT_SERVICE} (logical dbt models):         {len(dbt_tables)} table(s)")
    print(f"  {DBT_SERVICE} lineage edges:                 {dbt_lineage_edges}")

    failures = []
    if not iceberg_tables:
        failures.append(f"{ICEBERG_SERVICE} has 0 tables -- Iceberg ingestion did not populate the catalog.")
    if not dbt_tables:
        failures.append(f"{DBT_SERVICE} has 0 tables -- dbt ingestion did not populate the catalog.")

    if failures:
        print("\nFAILED:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
