---
phase: 3
title: "Rill explores expansion"
status: pending
priority: P2
dependencies: [2]
effort: "M"
---

# Phase 3: Rill explores expansion

## Overview

Grow the Rill Developer project from 3 to **≥ 8 explores / metric views**, each backed by an exported Parquet snapshot of a Phase-2 mart, so the dashboard renders non-empty data. Keep the existing serving contract: Rill reads exported Parquet (not the live DuckDB file), preserving single-writer discipline (issue #1 risk R2).

## Requirements

- **Functional**
  - Extend `serving/export_marts_snapshot.py` to export **all** marts in the shared canonical set `lake/curated_assets.json` (see Phase 4) resolved by absolute path from the script's `__file__`, so the export set, the Rill explore set, and the Iceberg set are the **same list** and cannot drift. There is **one explore per curated asset** — the explore list below equals `curated_assets.json` (11 marts), so every explore has an exported Parquet and every published Iceberg asset has an explore.
  - Add one Rill explore per canonical mart (11 total; ≥8 required) with a model + metrics + explore YAML each:
    1. `daily_revenue` (exists)
    2. `top_products` (exists)
    3. `customer_cohorts` (exists)
    4. `fulfillment_performance`
    5. `returns_analysis`
    6. `promotion_effectiveness`
    7. `channel_geography`
    8. `inventory_health`
    9. `web_funnel_conversion`
    10. `supplier_purchasing`
    11. `data_quality`
  - Each explore exposes meaningful dimensions + measures (time grain where relevant) so the demo can slice revenue, products, cohorts, fulfillment, returns, promotions, channels, geography, inventory, funnel, and data quality.
  - Rill models read from `serving/export/*.parquet` (same pattern as existing `serving/rill/models/*.sql`).

- **Non-functional**
  - Explores must render non-empty data on at least the `medium` profile (AC4).
  - No new heavy services; Rill stays a local CLI over Parquet.

## Architecture

```text
main_marts.mart_*  ──(export_marts_snapshot.py)──►  serving/export/*.parquet
                                                       └─ serving/rill/models/*.sql (read_parquet)
                                                            └─ metrics/*.yaml ──► explore/*.yaml
```

Reuse the existing three-file pattern per explore (`models/<name>.sql`, `metrics/<name>_metrics.yaml`, `explore/<name>_explore.yaml`). Keep naming consistent with the mart it visualizes.

## Related Code Files

- Modify: `serving/export_marts_snapshot.py` — export all marts feeding explores by reading `lake/curated_assets.json` via an absolute path resolved from `__file__` (no cross-package Python import; see Phase 4).
- Create: `serving/rill/models/mart_*.sql` (8 new — one per canonical mart beyond the 3 existing).
- Create: `serving/rill/metrics/*_metrics.yaml` (8 new).
- Create: `serving/rill/explore/*_explore.yaml` (8 new).
- Reference (read-only): existing `serving/rill/models/mart_daily_revenue.sql`, `metrics/daily_revenue_metrics.yaml`, `explore/daily_revenue_explore.yaml`, `serving/rill/rill.yaml`, `connectors/duckdb.yaml`.
- Verify (no edit expected): exported Parquet lives at `serving/export/*.parquet` and is already ignored by the **root** `.gitignore`; confirm that and that `make clean` removes it. (There is no per-mart `serving/rill/.gitignore` step — exports are not under `serving/rill/`.)

## Implementation Steps

1. Decide the exact ≥8 marts to visualize (align with Phase 2 mart list).
2. Extend `export_marts_snapshot.py` to export those marts; print row counts (evidence for AC8).
3. For each new explore, add model SQL (read the parquet), metrics YAML (measures/dimensions/time), explore YAML.
4. Run `make bi` then `rill start serving/rill`; confirm each explore loads with non-empty data on `medium`.
5. Capture the Rill URL and a per-explore row/measure sanity note for P7 evidence.

## Success Criteria

- [ ] `make bi` exports ≥ 8 mart Parquet files with non-zero row counts (printed).
- [ ] `rill start serving/rill` launches and lists ≥ 8 explores.
- [ ] Each explore renders non-empty data on the `medium` profile (AC4).
- [ ] Export list shares a single source of truth with Phase 4 curated assets (no drift).
- [ ] No committed Parquet/runtime artifacts (still gitignored).

## Risk Assessment

- **Empty explores:** some marts (e.g. `data_quality`) are small; verify non-empty on `medium`, not just `small`. If a mart is empty on `small`, document the minimum profile for a full demo.
- **Drift with Phase 4:** the exported-mart list and the Iceberg curated-asset list overlap; keep them from diverging by reading the same `lake/curated_assets.json` data file (owned in Phase 4, read-by-path here).
- **Rollback:** revert serving/rill additions and the export script change; Rill artifacts are gitignored.
