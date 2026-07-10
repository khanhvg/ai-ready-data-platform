---
phase: 1
title: "Demo-large deterministic data generation"
status: pending
priority: P1
dependencies: []
effort: "M"
---

# Phase 1: Demo-large deterministic data generation

## Overview

Extend `data-generator/generate.py` with new business entities (suppliers/purchasing, shipments, web sessions/events) and a new `demo-large` scale profile that produces **≥ 300,000 total rows deterministically** while staying memory-safe on a MacBook M1 Pro 16GB. Preserve the deterministic-seed guarantee, `manifest.json` (row counts, checksums, quality summary), and controlled data-quality scenarios; add a few new scenarios for the new tables.

## Requirements

- **Functional**
  - Add a `demo-large` profile to `SCALE_PROFILES` sized so total rows across all tables ≥ 300,000 (target ~400k–800k so the ≥300k floor holds even after quality/dup adjustments).
  - Add configurable upper bounds via CLI so demo-large stays bounded: `--max-orders`, `--max-web-events` (and honor them across all profiles). Defaults keep current behavior for existing profiles.
  - Add new raw entities where they enrich the demo without breaking explainability:
    - `suppliers.csv` — supplier dimension (name, region_id, lead_time_days, reliability_score).
    - `purchase_orders.csv` — supplier → store replenishment activity (po_id, supplier_id, store_id, order_date, expected_date, status).
    - `purchase_order_items.csv` — PO lines (po_item_id, po_id, product_id, quantity, unit_cost).
    - `shipments.csv` — order fulfillment (shipment_id, order_id, carrier, ship_date, delivered_date, ship_status).
    - `web_sessions.csv` — one row per browsing session (session_id, customer_id nullable for anon, channel, device, started_at, ended_at, landing_page).
    - `web_events.csv` — events within a session (event_id, session_id, event_type, event_ts, product_id nullable, order_id nullable) with a bounded volume.
  - Keep referential scenarios explainable: shipments reference real orders; web_events optionally convert to orders; PO items reference real products; a small, controlled fraction are intentionally broken (see quality scenarios).
  - Preserve deterministic single-`random.Random(seed)` flow so same `--profile --seed` reproduces byte-identical CSVs and stable per-file `sha256`.
  - Extend `manifest.json`: include new tables' row counts/checksums and new `quality_summary.observed` counters; keep `generated_at` the only non-reproducible field.

- **Non-functional**
  - **Memory safety (R1):** convert generation of the high-volume tables (`orders`, `order_items`, `payments`, `shipments`, `web_events`) to **streamed row writing** (write to CSV as rows are produced) instead of accumulating full Python lists, so peak RSS stays bounded on demo-large. Small dimensions (regions, stores, categories, products, customers, suppliers, promotions) can stay in memory (needed for FK sampling).
  - demo-large generation completes in a reasonable interactive window (target < ~2 min) and peak RSS well under the 16GB budget (target ≤ ~1.5GB); record measured numbers.

## Architecture

Generation stays a single deterministic pass but restructured so streaming and checksums coexist. **The current generator (`generate.py`) returns full `orders`, `order_items`, `payments`, `returns`, and inventory lists, then mutates those lists for DQ injection and manifest counts.** The concrete streaming redesign that keeps determinism without holding all fact rows:

- **Dimensions in memory (unchanged):** build regions, stores, categories, products, customers, suppliers, promotions first — bounded by profile, safe to hold; they are needed for FK sampling.
- **Streaming writer contract:** `stream_csv(path, header, row_iter) -> (row_count, sha256_hex)` opens the file, writes the header, and for each row calls `writer.writerow(row)` **and** `hash.update(<canonical-serialized-row-bytes>)`, returning the count and digest. No full-list accumulation. The canonical serialization for the hash is the exact bytes written to the CSV (read the file back in fixed-size chunks after close, or hash the encoded line as it is written) so the manifest `sha256` equals the on-disk file hash — one definition, no second pass.
- **Per-order-derived tables stream inline (payments, returns, order_items).** Today `build_orders_and_items` already draws `payment_method`, accumulates `order_total`, and (for returned orders) picks a returned item and its `refund_amount` **inside** the per-order loop (`generate.py` ~lines 235–360). Those fields are not in the compact summary tuple, so `payments` and `returns` **must be streamed inline in the same order-loop iteration** (write `orders`, then `order_items`, then the order's `payments` row, then its `returns` row when `status == "returned"`) while the full order/item context is in scope — not reconstructed later from the index. Streaming them inline also preserves the existing RNG draw order for those tables, so determinism within issue #3 is straightforward.
- **Bounded per-order summary index (the key structure):** the only cross-table state kept in memory is a compact per-order summary needed by the tables produced *after* the order loop — `order_id → (customer_id, store_id, order_date, status)` — NOT the full order/item rows. `shipments` (only for `status in (completed, returned)`) and the `checkout`-event → `order_id` linkage are streamed by iterating this index, so they reference real orders without holding item rows. The index is O(orders) of small tuples, bounded and measured against the memory target.
- **web_events volume** is derived from `web_sessions` × avg events/session but **capped** by `--max-web-events`; this is the main memory/row-count lever and must be tunable and deterministic. Sessions are held in memory (bounded); events are streamed. A deterministic fraction of `checkout` events links to real `order_id`s drawn from the summary index.
- **Determinism ordering:** one `random.Random(seed)` instance, drawn in a fixed table/row order (dimensions → per-order loop emitting orders+items+payments+returns inline → shipments → sessions → events). Any new draw is appended at the end of its table's sequence so existing-within-issue-#3 sequences stay stable across runs.
- **Inline DQ injection + observed counts:** duplicate injection and optional-null injection move from post-hoc list mutation to a per-row decision during the streaming write using the seeded RNG. Duplicates are produced by re-emitting a chosen row immediately (write the row, then with probability `DUP_RATE` write it again) so no lookback buffer is needed; nulls are decided per field per row. Observed counters increment as each scenario fires, preserving the existing "count only what this run injected" discipline from `inject_optional_nulls`. Counters are written to `manifest.quality_summary.observed`.

### New controlled data-quality scenarios (new tables)

| Scenario | Where | Testable downstream |
|---|---|---|
| In-transit shipments (null `delivered_date`) | `shipments.csv` | fulfillment mart / dbt test asserts non-negative lead time only on delivered rows |
| Orphan web_events (`session_id` not in sessions) | `web_events.csv`, low rate | dbt `relationships` warn test stg_web_events → stg_web_sessions |
| PO items referencing inactive/dangling products | `purchase_order_items.csv`, low rate | dbt `relationships` warn test |

Reuse existing rate constants pattern; add new `*_RATE` constants and surface both target and observed counts in the manifest `quality_summary`.

## Related Code Files

- Modify: `data-generator/generate.py` — new profile, new entities, streaming writer, new quality scenarios, extended manifest.
- Modify: `data-generator/schema.md` — document new tables, grains, `demo-large` row math, new quality scenarios, updated profile table with measured runtime/RSS.
- Modify: `data-generator/requirements.txt` — only if a new dependency is genuinely needed (prefer stdlib; likely no change).
- Modify: `ingestion/load_raw.py` — add the 6 new tables to the `TABLES` map (landing 1:1). (Coordinated with Phase 2 sources but owned here since it's the raw-load contract.)
- Modify: `Makefile` — allow `SCALE=demo-large`; optionally pass `--max-orders`/`--max-web-events` via env; no behavior change for existing scales.
- Reference (read-only): `data/raw/manifest.json` shape, existing `SCALE_PROFILES`, `observed_quality_counts`.

## Implementation Steps

1. Add new dimension builders: `build_suppliers`, `build_purchase_orders_and_items`. Wire supplier→region and PO→store/product references from existing dimensions.
2. Add `build_web_sessions` and a streamed `write_web_events` that derives event count per session deterministically, capped by `--max-web-events`, and links a fraction of `checkout` events to real orders for funnel/conversion demos.
3. Add `build_shipments` (streamed) keyed off orders with `status in (completed, returned)`; carrier + lead-time distribution; in-transit null-delivery scenario.
4. Refactor `write_csv` into a streaming helper (`open file → write header → for row: writer.writerow + hash.update → return count, checksum`) and route high-volume tables through it. Keep the small-table path as-is.
5. Rework quality-scenario injection to work inline in the streaming path; keep observed-count accuracy.
6. Add `demo-large` to `SCALE_PROFILES` and add `--max-orders` / `--max-web-events` argparse args with profile-appropriate defaults; enforce caps.
7. Extend `manifest["tables"]` and `quality_summary.observed` for the new tables/scenarios.
8. Update `ingestion/load_raw.py` `TABLES` with the 6 new tables.
9. Update `data-generator/schema.md` and the Makefile scale handling.

## Success Criteria

- [ ] `make seed SCALE=demo-large SEED=42` writes all tables + manifest; total rows ≥ 300,000 (printed total).
- [ ] Running demo-large twice with the same seed yields identical per-file `sha256` values in `manifest.json` (diff shows only `generated_at`).
- [ ] Peak RSS during demo-large generation recorded and ≤ ~1.5GB (evidence captured for P7); wall time recorded.
- [ ] `make load` loads all 18 tables into `raw.*` with row counts matching the manifest.
- [ ] `manifest.json` `quality_summary.observed` includes counters for the new scenarios.
- [ ] `python -m py_compile data-generator/generate.py ingestion/load_raw.py` passes.
- [ ] No secrets or generated CSV/DuckDB artifacts committed (still gitignored).

## Risk Assessment

- **R1 (memory):** streaming writer + `--max-web-events` cap are the primary mitigations; if demo-large still peaks high, reduce web_events cap first (it is the largest table). Measure before finalizing profile sizes.
- **R5 (determinism):** any reordering of RNG draws changes checksums vs issue #1 — expected. Guard by verifying internal reproducibility (generate twice, diff) rather than matching old values. Keep a single RNG instance; do not introduce unseeded randomness (e.g., stray `Faker` calls without `seed_instance`).
- **Rollback:** revert `generate.py`/`load_raw.py`/`schema.md`; generated data is gitignored and removed by `make clean`.
