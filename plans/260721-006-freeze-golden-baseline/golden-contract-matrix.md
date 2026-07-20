# Golden contract matrix

## Projection identity

`contracts/data/retail-golden-v1.json` freezes the semantic projection of immutable input `7a65da010abf0e3730731b6d744b532156c48fdc`, profile `small`, seed `42`. The producer command is `make golden-clean PROFILE=small SEED=42`. Raw bytes remain in the private evidence bundle; the contract stores exact stable fields/hashes and explicitly typed contextual history.

Top-level projection fields are closed and ordered by schema semantics:

```text
contractId, schemaVersion, inputIdentity, generator, anomalies,
dbt, marts, rill, airflow, curatedAssets, metadataIdentities,
historicalContext, assertions, integrity
```

`inputIdentity` includes `testedTreeSha`, lock fingerprint, tool versions, profile and seed. It contains no run/timestamp/path fields. Every inventory is an array with an explicit stable key/order plus duplicate-key validation.

## Generator: exact 18 CSVs

| Ordinal | File | Rows | SHA-256 of exact CSV bytes |
|---:|---|---:|---|
| 1 | `regions.csv` | 5 | `aa53262dffa42af91d54bb08b210950b9006f1d5fa05539db65c7fdc56066446` |
| 2 | `stores.csv` | 20 | `9500b325ab38d24436f0e7527e5d196ede91a6c41900392a8cb926a38e6a4ccf` |
| 3 | `product_categories.csv` | 8 | `b2f3b1157635ad1204550adcf202db74925c25b5111b610ed6e20e293e826bf5` |
| 4 | `products.csv` | 150 | `69f6670f4fc776137b6eb66b4b811ee7bff56f60f258245712ca211107534c65` |
| 5 | `customers.csv` | 201 | `6bb1bd567be4cd43abca76ea7e35ce2be08f8307c583ad6de2b9a123d7aa2e45` |
| 6 | `promotions.csv` | 6 | `94beef9b03a4d6eaccc104a0240a52777e0422c1ef636b16f8206509fb8c6de3` |
| 7 | `suppliers.csv` | 10 | `7c7d478912cffa95e86f95d9af8d95cbc0dbdd8f9cf1d23df9f5f1b779658e6f` |
| 8 | `purchase_orders.csv` | 69 | `c0b710c062f6f8ba86b7ae4722213fcff260b13ba3d27aa6d31e4f67c7048f06` |
| 9 | `purchase_order_items.csv` | 188 | `92c606b32704ef407f6f25dc977c6365b02172c7bc7beea4f2d15a71bff8b209` |
| 10 | `orders.csv` | 1,001 | `1fa72d45cbb8680903ae149d3fa99d2ffad6787a24acdd99b0d1783a66969cd1` |
| 11 | `order_items.csv` | 2,136 | `17a56e72564952e3b0c81b021d7a31a00ca42810eb4601a06cc507728ef534c2` |
| 12 | `payments.csv` | 1,000 | `c67719cfec3be7c8448f4a1906044a8a9db148c92bb03a21c40a8ff651aec069` |
| 13 | `returns_refunds.csv` | 56 | `bf1e736d5e2e5b67ca2cd24dee65df5c020b345e48afabc01ed5974dc8007b44` |
| 14 | `inventory_movements.csv` | 295 | `c0d8cc6ef721fea76fed7e8b81a3a981807615c85fa746a597e0b04c4118f2c4` |
| 15 | `reviews.csv` | 125 | `b07705ff914640663dbee87cf49f469d066fb0d6ebf66804cd58c0874f796ce6` |
| 16 | `shipments.csv` | 870 | `d73d88f0b0efac24e0f1fb40179de6718320bf2d16abcc7aa427f475fe191611` |
| 17 | `web_sessions.csv` | 200 | `4a642f3f93e6c05cdc10c32e186d170f242af627b828666f21b76be385be25e4` |
| 18 | `web_events.csv` | 472 | `7942455445d7915e644a64f8c27c5438a0824e3e8e9a83d7d5f103d5903fd693` |

Exact aggregate anchors:

- file count `18`; total data rows `6,812`;
- SHA-256 of ordered `(file,rowCount,csvSha256)` list: `60ce82ce297acec1e3c047466f4b068baed5dc1875964832cb6cda3d4f91e9d6`;
- SHA-256 of generator manifest after removing only its volatile generation timestamp and applying the contract canonicalizer: `74ef96503fae5b0805c3261a5930f50420e8d168f2329f15408827ac29672f25`;
- generated input domain: `2025-07-01` through `2026-06-30`.

### Observed versus configured anomaly contract

| Stable assertion | Observed small/42 count |
|---|---:|
| duplicate customer rows | 1 |
| duplicate order rows | 1 |
| null emails | 7 |
| null promotion IDs | 1 |
| null review text | 3 |
| invalid order statuses | 10 |
| late-arriving orders | 20 |
| orphan order-item product FKs | 6 |
| in-transit shipments | 70 |
| orphan web-event sessions | 1 |
| orphan purchase-order-item products | 0 |

Configured anomaly class/rate and observed count are separate fields. The configured purchase-order-item orphan rate does not guarantee an observation at this scale; zero is the exact seed/profile result and cannot be reclassified as a missing test.

## dbt graph and result matrix

| Field | Exact current anchor |
|---|---|
| source count | 18 |
| SQL model count | 51 |
| model layers | 18 staging, 6 ephemeral intermediate, 16 core, 11 marts |
| materialized models | 45 |
| generic tests | 141 |
| singular test files | 1: `tests/assert_non_negative_shipment_lead_time.sql` |
| canonical graph projection SHA-256 | `9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df` |
| clean build | PASS 179, WARN 7, ERROR 0, TOTAL 186 |
| result composition | 134 passing tests + 45 successful materializations + 7 observed warnings |

The contract records all nine warning-configured test names and their small/42 observed status:

| dbt test name | Expected small/42 |
|---|---|
| `source_unique_raw_customers_customer_id` | warn |
| `source_unique_raw_orders_order_id` | warn |
| `accepted_values_stg_orders_status__completed__cancelled__returned__pending` | warn |
| `accepted_values_fct_orders_status__completed__cancelled__returned__pending` | warn |
| `relationships_stg_order_items_product_id__product_id__ref_stg_products_` | warn |
| `relationships_fct_order_items_product_id__product_id__ref_dim_products_` | warn |
| `relationships_stg_web_events_session_id__session_id__ref_stg_web_sessions_` | warn |
| `relationships_stg_purchase_order_items_product_id__product_id__ref_stg_products_` | pass |
| `relationships_fct_purchase_order_items_product_id__product_id__ref_dim_products_` | pass |

Thus “nine configured warning tests” and “seven observed warnings” are independent assertions. Tests fail a change in severity, identity, observed status or the two-pass distinction. The runner captures build artifacts before docs generation; docs metadata (`51 models`, `141 tests`, `18 sources`, locked dbt 1.11.12’s `485 macros`) is a separate projection and does not overwrite build evidence.

## Canonical 11-mart summary

The query contract is `SELECT * FROM main_marts.<actual-model-id> ORDER BY ALL`, followed by typed, fixed canonical row serialization. It hashes logical content, never Parquet container bytes.

| Ordinal | Actual current mart ID | Rows | Canonical content SHA-256 |
|---:|---|---:|---|
| 1 | `mart_daily_revenue` | 319 | `59bf560c8a504481f60c2e3c593f840f17afc0f38a835db0cc1ed7b6e99f7fc8` |
| 2 | `mart_top_products` | 149 | `5ea0c4bb2504002fa601c39635b4c71a61c444a2cb0df0a41767128ff9992167` |
| 3 | `mart_customer_cohorts` | 97 | `84e10b8277ecfbc30187fb45c8760b5b115cfcbf706cdb60374919cb1f8d77db` |
| 4 | `mart_fulfillment_performance` | 25 | `8c0114d1ab48b4fb42009aba3df192988bf917004461d0c0dd0155d0283dce60` |
| 5 | `mart_returns_analysis` | 47 | `2aa068d1c676cc9234f9a6703f0d2490a10b007ae673b758fa45f614963e7db4` |
| 6 | `mart_promotion_effectiveness` | 7 | `5b6bc790aaeed2891608b8c1fceba0d4904fd49b9865c160658d6f5249e0bfc0` |
| 7 | `mart_channel_geography` | 14 | `ca42f1e1d54fa8695e55689cd7d6abaf33b63f431154f01da917d7d4f5d697fb` |
| 8 | `mart_inventory_health` | 149 | `33cf57ccc6ce152e90ce1a19665f888e7a204150e95c3da75a053770543e9f52` |
| 9 | `mart_web_funnel_conversion` | 15 | `63e8aabf6b333328f7f875df5aba696cebefbd2a5c12b6112c50f14fb4e1d189` |
| 10 | `mart_supplier_purchasing` | 10 | `2b6c9c9fe4f0e1b8ea756d8765d25b4ed52dadb89d4e8ed1631f265b3985b95b` |
| 11 | `mart_data_quality` | 10 | `cd3bb0424396aad0d902e9dc594072a5506c3b6484be3f3f2209b7cbbcdae5fa` |

Ordered 11-mart summary SHA-256: `8ffb3ef70bdb460eebe28ec5fb1986ec728fcd711e658523efb93671df8418ea`.

The three actual IDs above correct discovery’s human shorthand “channel performance,” “web funnel,” and “supplier performance”; changing the current model IDs to match shorthand would be an unauthorized product change.

## Exact Rill semantic inventory

Expression text, source model, dimensions and weighting are semantic. Whitespace-only YAML normalization may drift only through the registered YAML parser projection; parsed expression strings may not.

| View/model | Dimensions/timeseries | Exact measures |
|---|---|---|
| channel geography | `channel`, `region_name`, `city` | `SUM(completed_order_count)`; `SUM(revenue)`; `SUM(revenue) / NULLIF(SUM(completed_order_count), 0)` |
| customer cohorts | `loyalty_tier`; `cohort_month` | `SUM(customer_count)`; `SUM(total_orders)`; `SUM(total_revenue)`; `AVG(revenue_per_customer)` |
| daily revenue | `order_date` | `SUM(revenue)`; `SUM(completed_order_count)`; `AVG(avg_order_value)` |
| data quality | `scenario` | `SUM(row_count)` |
| fulfillment | `carrier`, `region_name` | `SUM(shipment_count)`; `SUM(on_time_count)`; `100.0 * SUM(on_time_count) / NULLIF(SUM(shipment_count), 0)`; `SUM(avg_lead_time_days * (shipment_count - in_transit_count)) / NULLIF(SUM(shipment_count - in_transit_count), 0)`; `SUM(in_transit_count)` |
| inventory | `product_name`, `category_name`, `store_name`, `region_name`, `is_negative_balance` | `SUM(current_stock_position)`; `SUM(restock_qty)`; `SUM(sale_qty)`; `SUM(return_qty)`; `SUM(adjustment_qty)` |
| promotion | `promo_name`, `channel` | `SUM(order_count)`; `SUM(gross_revenue)`; `SUM(total_discount_amount)`; `SUM(net_revenue)`; `SUM(net_revenue) / NULLIF(SUM(order_count), 0)`; `100.0 * SUM(total_discount_amount) / NULLIF(SUM(gross_revenue), 0)` |
| returns | `reason`, `category_name`, `region_name` | `SUM(return_count)`; `SUM(total_refund_amount)`; `SUM(total_refund_amount) / NULLIF(SUM(return_count), 0)` |
| supplier purchasing | `supplier_name`, `region_name` | `SUM(total_pos)`; `SUM(received_pos)`; `SUM(on_time_pct * total_pos) / NULLIF(SUM(total_pos), 0)`; `SUM(avg_cycle_days * total_pos) / NULLIF(SUM(total_pos), 0)`; `SUM(total_spend)`; `SUM(total_units_ordered)`; `AVG(reliability_score)` |
| top products | `product_name`, `sku`, `category_name` | `SUM(units_sold)`; `SUM(revenue)` |
| web funnel | `channel`, `device` | `SUM(session_count)`; `SUM(checkout_session_count)`; `SUM(converted_session_count)`; `100.0 * SUM(converted_session_count) / NULLIF(SUM(session_count), 0)`; `SUM(attributed_revenue)` |

The contract explicitly distinguishes ratio-of-sums from unweighted `AVG`: daily AOV and cohort revenue/customer are not reweighted; fulfillment lead time is weighted by non-in-transit shipments; supplier on-time/cycle are weighted by total POs while reliability is not. Mutation of numerator, denominator, multiplier, weighting term, source model, dimension or measure set fails.

## Airflow graph and the only path seam

DAG ID `retail_batch_pipeline` has this required default order:

```text
generate.seed
  -> load.load_raw
  -> load.health_check
  -> transform.dbt_build
  -> transform.dbt_docs_generate
  -> serve.export_marts_snapshot
```

The optional full profile appends:

```text
publish.publish_iceberg -> publish.iceberg_read_back
```

The semantic projection stores six default IDs/edges and exactly two optional IDs/edges. I5-01 may change `orchestration/airflow/callables/pipeline.py` only if a tests-before probe proves the current callables cannot forward explicit raw, warehouse and export workspace paths. It may not redesign process containment, DAG logic, Compose mounts, publisher behavior or Airflow security.

## Curated asset and catalog identities

The ordered asset allow-list is exactly the 11 actual mart IDs in the mart table above. `CuratedReleaseManifest` entries map each asset to its logical and physical identities:

- physical service/prefix: `retail_iceberg.default.retail.<mart>` for exactly the curated 11;
- logical dbt service/prefix: `retail_duckdb.retail.main_marts.<mart>` within the current 45 materialized logical models.

The current publisher’s sequential drop/create behavior and shallow read-back are characterized as a gap, not modified by I5-01. Historical issue #3 claims of 11 physical entities, 45 logical entities and 130 lineage edges are contextual only.

## Contextual historical evidence parser

`docs/verification/GH-3-full-flow-evidence.md` is parsed into a separately labelled context object: capture date `2026-07-10`, `demo-large`, 620,340 rows, macOS arm64, dbt-core 1.11.12/dbt-adapters 1.24.4, build 177 pass/9 warn, 11 marts, 11/45/130 OpenMetadata counts and six/eight Airflow tasks. The reader retains source path/blob/SHA, capture time, input commit when present, platform/profile/tools/commands/counts and `authority: historical-context`.

Mutation tests remove capture date/platform/profile/SHA, relabel the context as current, or feed prose with ambiguous counts; all must reject or retain an explicit “unparsed contextual note.” Historical evidence never supplies a current pass.

## Drift and mutation matrix

The only raw normalized record pointers allowed to drift are:

```text
/run/runId
/run/startedAt
/run/finishedAt
/run/durationMs
/run/workspaceLocator
```

The semantic projection has no allowed drift. Required mutations include:

| Mutation | Expected failure |
|---|---|
| 17/19 CSVs, row/hash change, reordered checksum list, manifest semantic change | `GOLDEN_INPUT_MISMATCH` |
| generator timestamp changed only | projection equal; raw pointer handled without hiding other drift |
| configured anomaly removed/rate changed or observed count changed | `GOLDEN_ANOMALY_MISMATCH` |
| 17/19 sources, 50/52 models, layer/materialization change, graph hash change | `DBT_GRAPH_MISMATCH` |
| generic/singular test count or singular file changes | `DBT_TEST_INVENTORY_MISMATCH` |
| configured-nine identity/severity or observed 7-warn/2-pass distinction changes | `DBT_WARNING_CONTRACT_MISMATCH` |
| dbt docs overwrites captured build artifact | `DBT_RAW_CAPTURE_MUTATED` |
| mart missing/extra/duplicate/renamed, row or content hash changes | `MART_PROJECTION_MISMATCH` |
| Rill expression/dimension/source/weight changes | `RILL_SEMANTIC_MISMATCH` |
| Airflow edge/ID/order/profile changes | `AIRFLOW_GRAPH_MISMATCH` |
| curated list/FQN/service identity changes | `CURATED_IDENTITY_MISMATCH` |
| historical prose presented as current evidence | `HISTORICAL_EVIDENCE_MISCLASSIFIED` |
| any undeclared JSON field, duplicate key, NaN/Infinity, Unicode normalization, negative-zero decimal | schema/canonicalization typed failure |
| a semantic value is added to allowed drift | `DRIFT_POLICY_VIOLATION` |

Every mutation is made in a private copy and verifies both non-zero exit and schema-valid failure evidence; tests never edit the protected input files in place.
