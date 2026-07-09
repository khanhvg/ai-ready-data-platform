# Storage and Ingestion

## Goal

P2 loads deterministic retail CSV files from `data/raw/` into a single local DuckDB warehouse at `warehouse/retail.duckdb`.

## Commands

```bash
make seed SCALE=small SEED=42
make load
make health
```

## Inputs

The generator writes one CSV per raw domain:

- `regions.csv`
- `stores.csv`
- `product_categories.csv`
- `products.csv`
- `customers.csv`
- `promotions.csv`
- `orders.csv`
- `order_items.csv`
- `payments.csv`
- `inventory_movements.csv`
- `returns_refunds.csv`
- `reviews.csv`

`data/raw/manifest.json` records the profile, seed, generation timestamp, table row counts, checksums, and quality-summary counts.

## Loader behavior

`ingestion/load_raw.py` is idempotent. Each run drops and recreates `raw.<table>` from the matching CSV, then compares loaded row counts against `manifest.json`.

The loader closes its DuckDB connection before exiting. Downstream dbt/Rill steps only read after the write step completes, preserving DuckDB single-writer discipline.

## Health check

`make health` opens the DuckDB file read-only and verifies that the `raw` schema contains landing tables.

## Demo evidence

For a successful small-profile run, the loader prints each `raw.*` table and an `[OK]` row-count marker. P2 demo evidence is raw/landing validation only; business aggregates are produced in P3 marts.
