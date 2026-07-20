# Storage and Ingestion

## Goal

P2 loads deterministic retail CSV files from `data/raw/` into a single local DuckDB warehouse at `warehouse/retail.duckdb`.

## Commands

```bash
make seed SCALE=small SEED=42
make load
make health
```

For the large-scale demo profile (issue #3), with optional caps:

```bash
make seed SCALE=demo-large SEED=42 MAX_ORDERS=20000 MAX_WEB_EVENTS=50000
make load
make health
```

`MAX_ORDERS`/`MAX_WEB_EVENTS` (passed through as `--max-orders`/`--max-web-events` to
`data-generator/generate.py`) are optional and default to no cap beyond the profile's own sizing --
use them to bound `demo-large` (or any profile) further on a slower machine. See
`data-generator/schema.md` for the full row-count math.

## Inputs

The generator writes one CSV per raw domain (18 tables):

- `regions.csv`
- `stores.csv`
- `product_categories.csv`
- `products.csv`
- `customers.csv`
- `promotions.csv`
- `suppliers.csv`
- `purchase_orders.csv`
- `purchase_order_items.csv`
- `orders.csv`
- `order_items.csv`
- `payments.csv`
- `inventory_movements.csv`
- `returns_refunds.csv`
- `reviews.csv`
- `shipments.csv`
- `web_sessions.csv`
- `web_events.csv`

`data/raw/manifest.json` records the profile, seed, generation timestamp, table row counts,
checksums, and a `quality_summary` with both the target injection rates and the observed counts
for this specific run. The CSVs (and their checksums) are byte-identical for a given
profile/seed; the manifest file itself is not, since `generated_at` changes every run.
`demo-large` comfortably clears the ≥300,000-row floor (measured total: 620,340 rows across the
18 tables) while streaming its high-volume tables straight to disk to keep peak memory flat.

## Loader behavior

`ingestion/load_raw.py` is idempotent. Each run drops and recreates `raw.<table>` from the matching CSV, then compares loaded row counts against `manifest.json`.

The loader closes its DuckDB connection before exiting. Downstream dbt/Rill steps only read after the write step completes, preserving DuckDB single-writer discipline.

## Health check

`make health` opens the DuckDB file read-only and verifies that the `raw` schema contains all 18 landing tables.

## Demo evidence

For a successful run, the loader prints each of the 18 `raw.*` tables and an `[OK]` row-count
marker against `manifest.json`. See `docs/verification/GH-3-full-flow-evidence.md` for a real
`demo-large` load run. Raw/landing validation happens here; business aggregates are produced in
the dbt marts (`docs/transform-orchestration.md`).
