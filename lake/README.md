# Lake profile: MinIO + Lakekeeper + Iceberg

DuckDB Iceberg writes require an Iceberg REST catalog; writing directly to a raw MinIO path is not enough. This repo uses Lakekeeper as the REST catalog for the optional `lake` profile.

## Start services

```bash
make lake-up
```

Services:

- MinIO API: http://localhost:9000
- MinIO console: http://localhost:9001
- Lakekeeper catalog: http://localhost:8181

## Publish marts

Run the core pipeline first:

```bash
make seed SCALE=small SEED=42
make load
make dbt
```

Then publish marts to Iceberg:

```bash
make lake-publish
```

`lake/publish_iceberg.py` loads DuckDB `iceberg` and `httpfs` extensions, attaches the Lakekeeper REST catalog, writes each `main_marts.*` table to `lake.retail.*`, then performs a read-back count smoke test.

## Resource note

The `lake` profile is opt-in. On MacBook M1 Pro 16GB, run it separately from the `governance` profile.
