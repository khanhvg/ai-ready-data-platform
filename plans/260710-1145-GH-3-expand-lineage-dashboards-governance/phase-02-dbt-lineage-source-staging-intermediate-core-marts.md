---
phase: 2
title: "dbt lineage source-staging-intermediate-core-marts"
status: pending
priority: P1
dependencies: [1]
effort: "L"
---

# Phase 2: dbt lineage source → staging → intermediate → core → marts

## Overview

Grow the dbt project from two layers (staging → marts) into a real, multi-branch lineage graph: **source → staging → intermediate → dimensional/core → marts**, with reusable dims/facts and **≥ 8 documented business-facing marts**. Add descriptions, tests, owners/tags, and enable persisted docs so lineage/descriptions flow to OpenMetadata (Phase 6). Switch the canonical transform step to `dbt build` and add `dbt docs generate`.

## Requirements

- **Functional**
  - **Sources:** add the 6 new raw tables from Phase 1 to `_sources.yml`.
  - **Staging (`models/staging/`):** add `stg_suppliers`, `stg_purchase_orders`, `stg_purchase_order_items`, `stg_shipments`, `stg_web_sessions`, `stg_web_events`. Keep the existing 12. Staging stays type/clean/dedupe views; DQ scenarios surfaced (not silently cleaned), matching the existing pattern.
  - **Intermediate (`models/intermediate/`, ephemeral or view):** reusable joined/enriched building blocks, e.g.:
    - `int_order_items_priced` — items × products × categories with revenue/discount math.
    - `int_orders_enriched` — orders × customers × stores × regions × promotions.
    - `int_fulfillment` — orders × shipments (+ returns) with lead-time/on-time flags.
    - `int_web_funnel` — sessions × events rolled to funnel steps, attributed to orders.
    - `int_inventory_position` — inventory movements → running stock position per product/store.
    - `int_purchasing` — purchase orders × items × suppliers with spend/cycle-time.
  - **Core / dimensional (`models/core/`, table):**
    - Dimensions: `dim_customers`, `dim_products`, `dim_stores`, `dim_regions`, `dim_promotions`, `dim_suppliers`, `dim_date`.
    - Facts: `fct_orders`, `fct_order_items`, `fct_payments`, `fct_shipments`, `fct_returns`, `fct_inventory_movements`, `fct_web_events`, `fct_purchase_orders`, `fct_purchase_order_items`. The two purchasing facts are **required** (not optional) so the suppliers / purchase-orders / PO-items sources added in P1 flow all the way through source→staging→intermediate (`int_purchasing`)→core→mart and are not dead-end lineage.
  - **Marts (`models/marts/`, table) — ≥ 8 business-facing:**
    1. `mart_daily_revenue` (rebuild on core)
    2. `mart_top_products` (rebuild on core)
    3. `mart_customer_cohorts` (rebuild on core)
    4. `mart_fulfillment_performance` — on-time %, avg lead time by carrier/region.
    5. `mart_returns_analysis` — return rate/refund by reason/category/region.
    6. `mart_promotion_effectiveness` — discounted vs baseline revenue, uplift by campaign/channel.
    7. `mart_channel_geography` — revenue by channel/region/city.
    8. `mart_inventory_health` — stock position, restock vs sale, low/negative balances.
    9. `mart_web_funnel_conversion` — session→event→order conversion by device/channel.
    10. `mart_supplier_purchasing` — supplier spend, lead time, on-time PO %, cycle time (consumes `fct_purchase_orders` + `fct_purchase_order_items` + `dim_suppliers`). **Required** so purchasing has a business-facing terminus.
    11. `mart_data_quality` — counts of the controlled DQ scenarios for demo storytelling.
    - Implement 10–11; **≥ 8 must build clean** and `mart_supplier_purchasing` is among the required set. (`mart_customer_ltv_segments` is optional stretch, only if it stays explainable and cheap.)
  - **Metadata:** every core/mart model gets a `description`; key models get `meta: {owner: ...}` and `tags` (e.g. `["marts","revenue"]`). Enable `+persist_docs: {relation: true, columns: true}` so descriptions persist into DuckDB and are picked up by OpenMetadata.
  - **Tests:** PK `not_null`/`unique` on dims/facts grain; `relationships` tests across the new joins (warn severity where a controlled DQ scenario intentionally breaks them); keep existing warn-severity DQ tests.
  - **Build command:** `make dbt` runs `dbt build` (models + tests in DAG order). Add a `make dbt-docs` target running `dbt docs generate` (produces `target/manifest.json` + `catalog.json` for Phase 6).

- **Non-functional**
  - Intermediate models materialized as `ephemeral` or `view` to bound memory; core facts + marts as `table`. Marts stay aggregates (small).
  - `dbt build` succeeds with **0 errors**; existing controlled warnings remain acceptable and documented.

## Architecture

```text
raw.* (18 sources)
   └─ stg_* (18 staging views: clean/dedupe/type, DQ surfaced)
        └─ int_* (6 intermediate: joins/enrichment, ephemeral/view)
             └─ core: dim_* (7) + fct_* (7)  [tables, persist_docs on]
                  └─ mart_* (≥8 tables: business aggregates)
```

Multiple branches/joins required by AC3 come from marts fanning in from several facts+dims (e.g. `mart_fulfillment_performance` ← `fct_shipments` + `fct_orders` + `dim_stores`/`dim_regions`; `mart_web_funnel_conversion` ← `fct_web_events` + `fct_orders` + `dim_customers`).

### dbt_project.yml layer config (sketch)

```yaml
models:
  retail_pipeline:
    +persist_docs: {relation: true, columns: true}
    staging:      {+materialized: view,       +schema: staging}
    intermediate: {+materialized: ephemeral,  +schema: intermediate}
    core:         {+materialized: table,       +schema: core, +tags: ["core"]}
    marts:        {+materialized: table,       +schema: marts, +tags: ["marts"]}
```

## Related Code Files

- Modify: `transform/dbt/dbt_project.yml` — add intermediate/core layers, persist_docs, tags.
- Modify: `transform/dbt/models/staging/_sources.yml` — add 6 new sources (+ any warn tests for new duplicate/orphan scenarios).
- Create: `transform/dbt/models/staging/stg_{suppliers,purchase_orders,purchase_order_items,shipments,web_sessions,web_events}.sql` + `_staging__models.yml` entries.
- Create: `transform/dbt/models/intermediate/int_*.sql` + `_intermediate__models.yml`.
- Create: `transform/dbt/models/core/{dim_*,fct_*}.sql` + `_core__models.yml`.
- Create/Modify: `transform/dbt/models/marts/*.sql` (rebuild the 3 existing on core; add ≥5 new) + `_marts__models.yml`.
- Modify: `Makefile` — `make dbt` → `dbt build`; add `make dbt-docs` → `dbt docs generate`.
- Modify: `docs/transform-orchestration.md` — new layer structure, build command, schemas (`main_intermediate`, `main_core`, `main_marts`).
- Reference (read-only): existing `stg_orders.sql`, `mart_daily_revenue.sql`, `_marts__models.yml` patterns.

## Implementation Steps

1. Add 6 sources to `_sources.yml`; add warn tests for new controlled scenarios (orphan web_events, dangling PO items).
2. Write the 6 new staging models following the existing dedupe/clean pattern; document them in `_staging__models.yml`.
3. Add `intermediate` + `core` layer config to `dbt_project.yml` with persist_docs and tags.
4. Build intermediate models (ephemeral/view); keep join logic here to avoid duplication in marts (DRY).
5. Build core dims + facts (tables); add PK/relationship tests and descriptions/owners/tags in `_core__models.yml`.
6. Rebuild the 3 existing marts on top of core; add ≥5 new marts; document all in `_marts__models.yml` with descriptions + tags + owners.
7. Switch `make dbt` to `dbt build`; add `make dbt-docs`.
8. Run `dbt build` on `small` then `medium`; confirm 0 errors and expected warnings; run `dbt docs generate` and confirm artifacts.

## Success Criteria

- [ ] `make dbt` (`dbt build`) succeeds with 0 errors on `small` and `medium`; controlled warnings only.
- [ ] `dbt ls` / lineage shows 4 distinct layers (staging, intermediate, core, marts) with multiple branches (AC3).
- [ ] ≥ 8 marts build and each has a `description` in `_marts__models.yml` (AC2).
- [ ] Core dims/facts carry descriptions + owner/tag meta; `persist_docs` writes comments into DuckDB (spot-checked via `information_schema`).
- [ ] `make dbt-docs` produces `transform/dbt/target/manifest.json` + `catalog.json`.
- [ ] `dbt build` on `demo-large` completes; wall time + memory recorded for P7 (AC8 input).

## Risk Assessment

- **R4 (build cost at scale):** ephemeral intermediates + table facts; measure demo-large build; if `fct_web_events` is heavy, consider `view` or a documented `--exclude` for interactive demos (keep default demo profile at `medium`). Do not add incremental models now (YAGNI) unless measurement forces it.
- **Persist_docs / OpenMetadata coupling:** descriptions must exist in YAML for both DuckDB comments and dbt-artifact ingestion (Phase 6); keep them the single source.
- **Rollback:** revert dbt model/config/yaml additions and the Makefile `dbt` target; no data loss (models are rebuilt from raw).
