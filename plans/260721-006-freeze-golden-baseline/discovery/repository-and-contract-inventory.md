# Repository and Contract Inventory

## Discovery identity and authority

- Phase: pre-plan discovery for GitHub issue #6, I5-01 — Freeze golden baseline and shared architecture contracts.
- Runtime identity requested by the issue: Codex `gpt-5.6-sol`, `model_reasoning_effort="xhigh"`.
- Branch: `plan/issue-6-freeze-golden-baseline-contracts`.
- Immutable tested input: `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`.
- Verified local `HEAD`, local tracking ref `origin/integration/issue-5-local-learning`, and the direct remote tracking ref all equal the immutable input before discovery writes.
- Master audit commit: `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`; it is an ancestor of the immutable input. The binding audit report is `plans/260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md` (blob `d0d5f0bad31fe7a3ad701bbbe157e85c00a2c0d8` at the immutable input).
- Authority sources: issue #6 body/comments; issue #5 body/comments; issue #7 handoff requirements; master phase 1 at `plans/260721-005-enterprise-learning-sandbox/phase-01-immutable-golden-baseline-and-architecture-contract.md:31-182`; execution authority at `plans/260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md:25-212`; implementation graph at `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md:3-204`; architecture view plan at `plans/260721-005-enterprise-learning-sandbox/architecture-view-plan.md:9-160`; and the master readiness audit at the master audit SHA.

The master result is `READY_WITH_GATES`, not implementation authority. This discovery does not promote plan state and does not authorize a local cook.

## Repository preservation and ownership inventory

| Item | Verified state at input | Discovery consequence |
|---|---|---|
| Worktree | Clean before discovery; zero tracked symlinks | Any final changed path outside the exact issue #6 discovery directory is a STOP. |
| Ignore rule | `.gitignore:62` is `plans/**/*` | Publication must use `git add -f -- plans/260721-006-freeze-golden-baseline/discovery` and no broader force-add. |
| Root `release-manifest.json` | Blob `b27d231c5ee6d48fd7932b06807ef6a9a2220e21`; SHA-256 `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539`; top-level keys `files`, `generatedAt`, `version` | This is existing repository/release provenance, not the retail curated-release contract. It must remain byte-identical. |
| `docs/code-standards.md` | Absent as both file and symlink | It is user-owned and protected. Never create, overwrite, or delete it. |
| `data/raw/.gitkeep` | Tracked; no generated raw files present | Preserve the tracked placeholder. Golden cleanup must remove only owned generated children, never the directory contract indiscriminately. |
| Existing ignored/generated areas | No `.venv`, dbt `target`, Docker volumes, `node_modules`, warehouse DB, or serving export was present in the clean-checkout probes | Reproducibility cannot depend on any of them. Unrelated ignored fixtures remain user-owned. |
| Issue #6 declared write scope | `scripts/golden/**`, specified `contracts/data/**`, base `learning/contracts/**`, evidence core, dependency locks, six local architecture sources/renders/manifest rows, root Make include/help, `mk/issue-5/i5-01.mk` | Do not edit I5-02+ fragments, product UI, runner internals beyond the explicitly narrow Airflow path-forwarding seam, current lake publisher, OpenMetadata product code, Terraform, or cloud assets. |
| Fixture handoff path | The binding phase requires `tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}`, but issue #6's explicit “May write” list and the master file-ownership table omit this path | This is finding F-05. The planner may model the resolution, but local cook must STOP until issue/master authority explicitly assigns that exact path to I5-01. |

## Source snapshot

All object IDs below are Git blob/tree IDs at `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`.

| Source | Object ID | Contract surface |
|---|---|---|
| `Makefile` | `41b385c2119520e8925fb1a48ef291e9e64154cb` | Current lifecycle, virtualenv bootstrap, 15 targets, cleanup, root integration seam |
| `data-generator/generate.py` | `b6b7816316e01208d4af7e1571c06103ac14e6ca` | Seeded CSV bytes, anomaly injection, manifest |
| `transform/dbt/` | tree `28932692fc20e079eecbe7ab1c9f93b2a94a8bbf` | 18 sources, 51 SQL models, tests, lineage, 11 marts |
| `serving/rill/` | tree `27bda8a14222cae083d480275453659adb85b3ff` | 11 models, metrics views, dashboards |
| `orchestration/airflow/dags/retail_batch_pipeline.py` | `77b1fd204c1340ff62fd376651da0b67d1a9b423` | Six-task default graph and two optional publish tasks |
| `lake/curated_assets.json` | `fc4b04aca3d4941d06658f27c58d078299301200` | Ordered 11-asset allow-list |
| `lake/publish_iceberg.py` | `f929090963f94e0847231558271d176f3c8b714c` | Current destructive/non-atomic publisher and identifiers |
| `governance/openmetadata/ingestion/bootstrap_dbt_service.py` | `86e05fb308f6e98d80bd51080ad5f659ebf0cf93` | Logical model and lineage bootstrap |
| `governance/openmetadata/ingestion/iceberg_ingestion.yaml` | `3e91ac8419be56f66d39bed70e1806a24329954c` | Physical 11-table filter and service identity |
| `docs/verification/GH-3-full-flow-evidence.md` | `f0823bf8adcc81918beea3942a3b548cdd0f8526` | Historical, environment-qualified evidence only |

## Exact golden characterization envelope

### Generator bytes, checksums, and anomalies

`data-generator/generate.py:34-51` defines four scale profiles and anomaly rates; `:134-166` hashes the exact emitted CSV byte stream; `:728-747` exposes the output-directory seam; `:754-755` fixes the event range to 2025-07-01 through 2026-06-30; `:900-938` writes a manifest whose `generated_at` is intentionally volatile.

Two independent no-cache archives of the immutable input ran `make seed SCALE=small SEED=42`. Every CSV byte matched. Removing only `generated_at` made both manifests equal. The deterministic table envelope is:

| Table | Rows | SHA-256 of exact CSV bytes |
|---|---:|---|
| `regions.csv` | 5 | `aa53262dffa42af91d54bb08b210950b9006f1d5fa05539db65c7fdc56066446` |
| `stores.csv` | 20 | `9500b325ab38d24436f0e7527e5d196ede91a6c41900392a8cb926a38e6a4ccf` |
| `product_categories.csv` | 8 | `b2f3b1157635ad1204550adcf202db74925c25b5111b610ed6e20e293e826bf5` |
| `products.csv` | 150 | `69f6670f4fc776137b6eb66b4b811ee7bff56f60f258245712ca211107534c65` |
| `customers.csv` | 201 | `6bb1bd567be4cd43abca76ea7e35ce2be08f8307c583ad6de2b9a123d7aa2e45` |
| `promotions.csv` | 6 | `94beef9b03a4d6eaccc104a0240a52777e0422c1ef636b16f8206509fb8c6de3` |
| `suppliers.csv` | 10 | `7c7d478912cffa95e86f95d9af8d95cbc0dbdd8f9cf1d23df9f5f1b779658e6f` |
| `purchase_orders.csv` | 69 | `c0b710c062f6f8ba86b7ae4722213fcff260b13ba3d27aa6d31e4f67c7048f06` |
| `purchase_order_items.csv` | 188 | `92c606b32704ef407f6f25dc977c6365b02172c7bc7beea4f2d15a71bff8b209` |
| `orders.csv` | 1,001 | `1fa72d45cbb8680903ae149d3fa99d2ffad6787a24acdd99b0d1783a66969cd1` |
| `order_items.csv` | 2,136 | `17a56e72564952e3b0c81b021d7a31a00ca42810eb4601a06cc507728ef534c2` |
| `payments.csv` | 1,000 | `c67719cfec3be7c8448f4a1906044a8a9db148c92bb03a21c40a8ff651aec069` |
| `returns_refunds.csv` | 56 | `bf1e736d5e2e5b67ca2cd24dee65df5c020b345e48afabc01ed5974dc8007b44` |
| `inventory_movements.csv` | 295 | `c0d8cc6ef721fea76fed7e8b81a3a981807615c85fa746a597e0b04c4118f2c4` |
| `reviews.csv` | 125 | `b07705ff914640663dbee87cf49f469d066fb0d6ebf66804cd58c0874f796ce6` |
| `shipments.csv` | 870 | `d73d88f0b0efac24e0f1fb40179de6718320bf2d16abcc7aa427f475fe191611` |
| `web_sessions.csv` | 200 | `4a642f3f93e6c05cdc10c32e186d170f242af627b828666f21b76be385be25e4` |
| `web_events.csv` | 472 | `7942455445d7915e644a64f8c27c5438a0824e3e8e9a83d7d5f103d5903fd693` |

Aggregate comparison anchors:

- 18 tables, 6,812 total data rows.
- SHA-256 of the ordered table/checksum list: `60ce82ce297acec1e3c047466f4b068baed5dc1875964832cb6cda3d4f91e9d6`.
- SHA-256 of the deterministic manifest projection: `74ef96503fae5b0805c3261a5930f50420e8d168f2329f15408827ac29672f25`.
- Observed anomalies: duplicate customer rows 1; duplicate order rows 1; null emails 7; null promotion IDs 1; null review text 3; invalid order statuses 10; late-arriving orders 20; orphan order-item product FKs 6; in-transit shipments 70; orphan web-event sessions 1; orphan purchase-order-item products 0.

The zero purchase-order orphan is intentional for `small/42`: the configured 2% rate does not guarantee at least one event at this scale. The contract must distinguish configured anomaly classes/rates from observed seed/profile counts.

### dbt warning, graph, and mart envelope

Static inventory at the input:

- 51 SQL models: 18 staging, 6 ephemeral intermediate, 16 core, and 11 marts.
- 45 materialized models, 18 sources, 141 generic/singular tests, and one singular test file.
- Nine relationship/accepted-value/uniqueness tests are configured as warnings.
- Canonical graph projection SHA-256: `9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df`.

The clean `small/42` build reported `PASS=179 WARN=7 ERROR=0 TOTAL=186`: 134 passing tests, 45 successful materializations, and seven warnings. The configured warning contracts cover duplicate source customers, duplicate source orders, invalid order status in staging and fact, orphan product in staging and fact order items, orphan web session, and orphan product in staging and fact purchase-order items. The last two pass for `small/42` because its observed purchase-order orphan count is zero. Therefore the golden result must record both all nine warning-configured test IDs and the profile-specific seven-warning/two-pass oracle.

`dbt docs generate` can replace `target/run_results.json`; raw dbt artifacts also contain elapsed time, invocation IDs, generated timestamps, and absolute paths. The harness must capture build results before docs and compare a defined deterministic projection, not raw JSON bytes.

The canonical mart projection used `SELECT * FROM main_marts.<name> ORDER BY ALL`, serialized with a fixed representation. It characterizes logical results, not Parquet container bytes:

| Mart | Rows | Canonical content SHA-256 |
|---|---:|---|
| `mart_daily_revenue` | 319 | `59bf560c8a504481f60c2e3c593f840f17afc0f38a835db0cc1ed7b6e99f7fc8` |
| `mart_top_products` | 149 | `5ea0c4bb2504002fa601c39635b4c71a61c444a2cb0df0a41767128ff9992167` |
| `mart_customer_cohorts` | 97 | `84e10b8277ecfbc30187fb45c8760b5b115cfcbf706cdb60374919cb1f8d77db` |
| `mart_fulfillment_performance` | 25 | `8c0114d1ab48b4fb42009aba3df192988bf917004461d0c0dd0155d0283dce60` |
| `mart_returns_analysis` | 47 | `2aa068d1c676cc9234f9a6703f0d2490a10b007ae673b758fa45f614963e7db4` |
| `mart_promotion_effectiveness` | 7 | `5b6bc790aaeed2891608b8c1fceba0d4904fd49b9865c160658d6f5249e0bfc0` |
| `mart_channel_performance` | 14 | `ca42f1e1d54fa8695e55689cd7d6abaf33b63f431154f01da917d7d4f5d697fb` |
| `mart_inventory_health` | 149 | `33cf57ccc6ce152e90ce1a19665f888e7a204150e95c3da75a053770543e9f52` |
| `mart_web_funnel` | 15 | `63e8aabf6b333328f7f875df5aba696cebefbd2a5c12b6112c50f14fb4e1d189` |
| `mart_supplier_performance` | 10 | `2b6c9c9fe4f0e1b8ea756d8765d25b4ed52dadb89d4e8ed1631f265b3985b95b` |
| `mart_data_quality` | 10 | `cd3bb0424396aad0d902e9dc594072a5506c3b6484be3f3f2209b7cbbcdae5fa` |

Ordered 11-mart summary SHA-256: `8ffb3ef70bdb460eebe28ec5fb1986ec728fcd711e658523efb93671df8418ea`.

### Rill semantic expressions

The exact expression text and referenced model/column form the semantic contract. “Weighted” must be asserted only where the current expression actually weights:

| View | Ratio/average behavior to freeze |
|---|---|
| Channel | Average order value is `SUM(revenue) / SUM(completed orders)` (ratio of sums). |
| Daily revenue | Average order value is `AVG(avg_order_value)` across source rows; it is not reweighted. |
| Customer cohorts | Revenue per customer is `AVG(revenue_per_customer)`; it is not reweighted. |
| Fulfillment | On-time rate is a ratio of summed counts; average lead time weights by completed shipment count (`shipment_count - in_transit_count`). |
| Promotion | Average order value and discount rate are ratios of sums. |
| Returns | Average refund is a ratio of sums. |
| Supplier | On-time and cycle time weight by `total_pos`; reliability is `AVG`. |
| Web funnel | Conversion is a ratio of summed counts. |

The remaining Rill measures must still be frozen by exact expression/model/dimension inventory. Mutation tests should change an expression, numerator/denominator, source model, or weighting term and require a contract failure.

### Airflow graph and path boundary

The static default graph has six task IDs:

`generate.seed -> load.load_raw -> load.health_check -> transform.dbt_build -> transform.dbt_docs_generate -> serve.export_marts_snapshot`

The optional full profile appends `publish.publish_iceberg -> publish.iceberg_read_back`, producing eight tasks. DAG ID is `retail_batch_pipeline`.

Current task subprocesses inherit ambient `os.environ`, capture unbounded output, lack per-command timeouts, and the DAG inserts `/opt/airflow` on `sys.path`. The compose mount exposes the project root read-write at `/opt/airflow/project`. I5-01 may forward only the explicit raw/warehouse/export workspace paths required by the golden harness. General runner isolation, output caps, and cross-entrypoint security belong to I5-04 and must not be pulled into issue #6.

### Curated assets, Iceberg, OpenMetadata, and historical evidence

`lake/curated_assets.json` orders these 11 assets: daily revenue, top products, customer cohorts, fulfillment performance, returns analysis, promotion effectiveness, channel performance, inventory health, web funnel, supplier performance, and data quality. The current publisher defaults to catalog `retail`, namespace `lake.retail`, then executes `DROP TABLE IF EXISTS` followed by `CREATE TABLE` sequentially. Its read-back checks presence/nonzero rows, not exact schemas, row counts, checksums, or generation atomicity. I5-01 owns the release-manifest schema; I5-07 owns the later staged publisher/current-pointer implementation and reconciliation. Issue #6 must not edit `lake/publish_iceberg.py`.

OpenMetadata identities to characterize are:

- Physical service `retail_iceberg`, FQN prefix `retail_iceberg.default.retail.<mart>` for exactly the curated 11.
- Logical service `retail_duckdb`, FQN prefix `retail_duckdb.retail.main_marts.<mart>` for the materialized dbt models.
- Historical successful evidence reports 11 physical entities, 45 logical model entities, and 130 lineage edges.

`docs/verification/GH-3-full-flow-evidence.md` is historical evidence captured 2026-07-10 for `demo-large` (620,340 rows), dbt-core 1.11.12, `177/9`, 11 marts, 11/45/130 OpenMetadata counts, and the six/eight-task Airflow graph. A parser must retain capture date, input commit if present, platform/profile, tool versions, command, and observed counts. It must never relabel those claims as a current clean-checkout run.

## Clean-checkout reproducibility probe

Two independent `git archive` extractions of the immutable input were run without pre-existing `.venv`, generated data, Docker volumes, `node_modules`, credentials, or shared caches. Each ran `make seed SCALE=small SEED=42`, `make load`, `make dbt`, `make dbt-docs`, and `make bi` in 155 seconds on the discovery host. CSV bytes, deterministic manifest projection, dbt graph projection, and canonical mart results matched across runs.

The bootstrap resolved dbt-core 1.12.0 and dbt-adapters 1.24.5 even though historical evidence names dbt-core 1.11.12 and the master source notes dbt-adapters 1.24.4. The direct requirements pin only Faker 40.28.1, DuckDB 1.5.4, and dbt-duckdb 1.10.1. There are no complete transitive locks or hashes. The observed `pip freeze` SHA-256 was `2db8f901e9f957cbe466bf253028a97bbf9a0c595595b403324635bf4bc0e1fe`, but that is evidence of one resolution, not a lock contract.

The root virtualenv sentinel is only `.venv/bin/python3`; pip is upgraded without a version/hash, and only `PYTHONPATH` is explicitly unset. The `bi` guidance includes a curl-to-shell installer and catalog ingestion can dynamically install packages. A golden command must use a fully resolved, hash-checked lock and bounded install policy. pip's documented secure-install mode requires all dependencies to be pinned and hashed when `--require-hashes` is used; `--only-binary :all:` is an additional supply-chain hardening option ([pip secure installs](https://pip.pypa.io/en/stable/topics/secure-installs/)).

Discovery-host portability facts: Python 3.12.3, GNU Make 3.81, Docker present, `uv` present but not safe to assume, `flock` absent, and no usable Java runtime, Structurizr CLI, dbt, or Rill binary on the clean host. Python `hashlib` is the portable checksum primitive; do not require GNU-only `sha256sum` or `flock`.

## Make integration and architecture workspace

The master registry at `execution-authority-and-release-contract.md:160-187` contains exactly 54 future targets. I5-01 owns only seven: `help`, `golden-clean`, `data-contracts-check`, `evidence-contracts-check`, `migration-contracts-check`, `architecture-check`, and `architecture-render`. The input Makefile has 15 existing targets. Root integration must be a disjoint include such as `-include mk/issue-5/*.mk`, preserve existing target behavior, and derive help/registry checks without defining later owners' targets. Any target collision, duplicated recipe, or edit to another `i5-<nn>.mk` is a STOP.

The architecture skeleton must register exactly six pre-P5 local views:

1. `C4-L0`
2. `C4-L1`
3. `C4-L2-LOCAL`
4. `C4-L3-RUNNER`
5. `DEP-LOCAL`
6. `DYN-JOURNEY`

The required manifest fields and fitness behavior are defined at `architecture-view-plan.md:102-160`: stable ID, source, rendered artifact paths, concerns, owners, elements/relationships, release status, and freshness hashes; reject missing concerns, orphan elements, undeclared references, missing text alternatives, and stale output. I5-06 receives only a serialized, time-bounded lease after I5-05 to add expansion rows/includes/renders; it cannot rewrite these six. `DYN-PUBLISH` belongs to I5-06, not I5-01.

The master text expects deterministic SVG export, but current Structurizr CLI export formats do not directly include PNG/SVG; image export is described through browser/Puppeteer workflows ([CLI export](https://docs.structurizr.com/cli/export), [diagram export](https://docs.structurizr.com/ui/diagrams/export)). The clean host also lacks Java/Structurizr. The planner must select and pin a real render chain (including digest/hash and deterministic normalization) or revise the committed render contract to a format the pinned tool actually produces. A missing required tool is failure, never skip.

## Critical and High finding registry

Every local-cook STOP below is mandatory. “Owner” identifies who resolves the finding without widening I5-01 ownership.

| ID | Severity | Finding | Owner | Acceptance evidence | Mitigation and rollback | Dependency | Local-cook STOP condition |
|---|---|---|---|---|---|---|---|
| F-01 | Critical | A false deterministic oracle is possible if volatile fields or raw dbt artifacts are hashed, if `run_results.json` is captured after docs overwrites it, or if canonicalization silently drops semantic fields. | I5-01 | Two isolated runs; raw artifacts retained; schema-valid deterministic projections equal; explicit allowed-drift pointers; mutation of a semantic field fails. | Separate raw evidence from projection; use a registered canonical payload; preserve both runs. Roll back by disabling promotion and reading the last supported evidence version. | Evidence schema, lock, dbt capture order | STOP if canonical field inventory, allowed-drift list, capture order, and mutation tests are not explicit. |
| F-02 | Critical | Generated path, symlink, TOCTOU, or cleanup mistakes can escape the owned workspace, tamper with evidence, or delete user files. | I5-01 for golden workspace; I5-04 for generalized runner containment | Adversarial tests for absolute paths, `..`, symlink swap, pre-existing destination, concurrent run, and interrupted write; protected paths stay byte-identical. | Resolve/validate beneath an owned root, reject symlink components, create private temp dirs, write with exclusive creation and atomic rename, never call broad root `clean`. Roll back by retaining failed workspaces and restoring only the prior scoped pointer. | Workspace ID/lease contract; filesystem portability | STOP on any unbounded delete, unresolved path, writable shared evidence destination, or check-then-use gap without an atomic primitive. |
| F-03 | Critical | An underspecified `CuratedReleaseManifest` can bless a partial or mixed-generation 11-asset release. | I5-01 schema; I5-07 publisher/pointer implementation | Schema requires all 11 exact asset IDs, schema/content hashes, row counts, staged locators, engine snapshot/version IDs, common release/data run/input SHA; negative fixtures reject missing, duplicate, mixed, or extra assets. | Stage immutable generation, validate completely, then atomically replace one current pointer. Roll back the pointer to the prior complete release; never mutate a published generation. | I5-07 implementation lease | STOP if issue #6 starts implementing the publisher or if the schema permits partial/mixed releases. |
| F-04 | Critical | `promotion-trust-v1` can invent campaign attribution by joining marts at incompatible grains. | I5-01 contract/fixture; I5-07 owns any later additive order/promotion data product | Contract states each source grain and allowed assertions; negative tests reject causal/campaign, carrier, return, or data-quality attribution not present in current data. Fixture contains only grain-honest aggregates. | Keep promotion, fulfillment, returns, and data-quality assertions separate; add a later governed data product if attribution is required. Roll back by invalidating the overclaimed fixture/contract version. | Current four marts; issue #7 consumer | STOP if any assertion implies a causal/campaign join or introduces new attribution fields. |
| F-05 | High | Required tracked promotion fixture path lacks explicit issue #6/file-matrix write authority. | Issue #6 owner and master-plan maintainer | Issue body or binding authority artifact explicitly assigns `tests/fixtures/learning/promotion-trust/**` to I5-01 and excludes overlapping owners; planner cites it. | Amend authority before cook; if not granted, leave fixture unpublished and keep issue #7 scoring blocked. Roll back any premature fixture commit. | Issue #7 real-fixture gate | STOP while exact path authority remains absent or ambiguous. |
| F-06 | High | Direct pins without a complete hashed transitive lock already resolve different dbt core/adapter versions from historical evidence. | I5-01 | Checked-in platform-appropriate lock with all transitive versions/hashes, interpreter policy, offline/cache behavior, and two clean installs yielding the same lock fingerprint. | Choose and test a known-good dbt baseline; use `--require-hashes`; retain prior lock and evidence reader for rollback. | Planner decision D-01 | STOP until the 1.11.12-versus-1.12.0 baseline decision is explicit and reproducible. |
| F-07 | High | The required SVG render path is not implemented by the described CLI boundary, and the clean host has no Java/Structurizr. | I5-01 architecture contract | Pinned renderer/tool digest, bootstrap policy, deterministic sample output, text alternative, freshness hash, and negative missing-tool test. | Select a supported CLI text/export plus pinned deterministic renderer, or explicitly revise the render artifact contract. Retain sources and previous renders for rollback. | Architecture toolchain decision | STOP if `architecture-render` can skip, use an unpinned browser, or claim an unsupported output format. |
| F-08 | High | Root Make integration can collide with the existing 15 targets or predeclare later owners' entries in the 54-command registry; broad cleanup can touch protected/unrelated files. | I5-01 | Registry parser proves 54 unique owner assignments; issue #6 fragment defines only seven; current target behavior tests pass; protected-path hashes and ignored fixtures remain unchanged. | Use one root include/help seam and disjoint fragments; use scoped golden cleanup only. Revert root include and I5-01 fragment as a unit. | Master command registry | STOP on duplicate targets, another issue's fragment/recipe, changed existing semantics, or protected path drift. |
| F-09 | High | A local unkeyed checksum detects corruption but not hostile replacement; self-containing exact-SHA claims can become recursively unhashable. | I5-01 local evidence; I5-14 hosted signing/authenticity | Evidence labels integrity/authenticity separately; canonical payload excludes its own digest; tested tree SHA, attestation commit SHA, and later merge/tag SHA occupy distinct fields/records; tampering fails. | Do not claim signing. Record attestation and merge SHAs externally or in a child index. Keep local SHA verification and defer hosted signing to I5-14. | Version registry; publication workflow | STOP if local checksums are described as signatures, or one artifact must contain the SHA of the commit/artifact containing itself. |
| F-10 | High | Historical demo evidence, current small-profile evidence, Iceberg FQNs, and OpenMetadata counts can be conflated and produce a misleading baseline. | I5-01 | Parser preserves evidence kind/date/profile/platform/tool/input identity; contracts separately enumerate 11 physical FQNs, 45 logical materializations, expected lineage set/count, and current versus historical observations. | Treat Markdown as historical input, never current attestation; fail ambiguous or context-free records. Roll back to raw historical evidence plus parser version. | Evidence registry and I5-07 exact reconciliation | STOP if `177/9` is asserted for `small/42`, or historical counts are promoted without their context. |
| F-11 | High | Issue #7 can publish a score or ADR against a provisional/unmerged fixture or a self-referential producer SHA. | I5-01 producer, I5-02/#7 consumer | Sanitized aggregate fixture and manifest are tracked at an authorized path; exact tested-tree SHA and artifact hashes verify; issue #7 records the externally observed merge SHA before scoring. | Allow only unscored preview/common tests before merge; invalidate scores whose fixture/merge identity differs. | F-05, issue #6 merge | STOP if issue #6 emits a framework score/ADR or #7 scoring is represented as ready before merged identity exists. |
| F-12 | High | Ambient environment/PYTHONPATH, dynamic installers, unbounded Airflow subprocess output, and a read-write root mount threaten portability and evidence integrity. | I5-01 narrow clean harness/path forwarding; I5-04 generalized runner security | Golden commands use an allow-listed environment, no credentials, bounded time/output, locked dependencies, isolated workspace paths; broad runner threats are explicitly handed to I5-04. | Avoid curl-to-shell/dynamic install in golden path, sanitize environment, add timeouts, and retain failure logs with secrets redacted. Revert only the narrow forwarding seam if it breaks the existing DAG. | Lock strategy and I5-04 | STOP if the golden path consumes ambient credentials/PYTHONPATH, runs an unpinned installer, or silently expands into generalized runner redesign. |

## Discovery conclusion

The repository is characterizable and I5-01 remains plan-able, but it is not cook-ready. The planner must close F-05, F-06, and F-07 as explicit authority/tooling decisions and encode every other STOP as acceptance/rollback evidence. No issue #6 ownership should be widened silently.
