---
title: "Issue #3: Expand large-scale lineage, dashboards, OpenMetadata, and Airflow demo"
description: "Expand the AI-ready data platform sandbox with demo-large deterministic data, a source→staging→intermediate→core→mart dbt graph (≥8 marts), ≥8 Rill explores, a visible full-flow Airflow DAG, Iceberg publish/read-back of ≥8 curated assets, OpenMetadata Iceberg + dbt artifact ingestion, and resource-safe operation on a MacBook M1 Pro 16GB."
status: pending
priority: P2
branch: "plan/issue-3-expand-lineage-dashboards-governance"
tags: [data-platform, dbt, rill, airflow, iceberg, openmetadata, duckdb]
blockedBy: []
blocks: []
created: "2026-07-10T04:45:12.952Z"
createdBy: "ck:plan"
source: skill
---

# Issue #3: Expand large-scale lineage, dashboards, OpenMetadata, and Airflow demo

## Overview

Issue #3 grows the existing sandbox (issue #1 / PR #2) from a thin demo (12 raw tables, ~3 staging→mart hops, 3 Iceberg marts, 3 Rill explores) into a compelling, resource-safe customer demo: a large deterministic retail dataset, a real layered dbt lineage graph (source → staging → intermediate → dimensional/core → marts) with ≥8 business-facing marts, ≥8 Rill explores, a visible end-to-end Airflow DAG with task groups, Iceberg publication + read-back of ≥8 curated assets, and OpenMetadata catalog/lineage from **both** the physical Iceberg tables and the logical dbt models.

The hard constraint is unchanged: it must all run on a **MacBook M1 Pro 16GB** without uncontrolled all-services startup. Heavy profiles stay opt-in and staged; the one genuinely new resource conflict (OpenMetadata Iceberg ingestion needs `lake` **and** `governance` up at the same time) is resolved with an explicit, guarded, documented co-run window rather than by relaxing the safety guards globally.

**This is a plan-only deliverable.** No implementation files are modified in this stage.

## Dependency on issue #1 / PR #2 (read this first)

Issue #3 **expands the code from issue #1**, which is now **merged to `main`** (PR #2 merged at commit `45daa70`). The dependency is therefore satisfied, and the branch/merge story is simple:

- **Branch base:** the issue-3 work branch (`plan/issue-3-expand-lineage-dashboards-governance`) is cut **from `main`** (post-PR-#2), so the existing code is present to extend. This plan document is committed on that branch.
- **Plan stage scope:** the plan stage adds only the plan files under `plans/`. No implementation files are modified until this plan is audited. Because `.gitignore` ignores `plans/**/*`, the plan files are force-added on the branch so they ship with the plan branch (see the evidence-location note in Phase 7 / R8 for the same constraint applied to verification evidence).
- **Merge ordering:** none required — the issue-3 implementation PR targets current `main`. No coordination with PR #2 remains.
- **Determinism baseline:** adding new entities and reordering RNG draws will change the existing per-file checksums from issue #1. That is expected and in-scope. The determinism guarantee is re-established fresh (same seed/profile ⇒ byte-identical CSVs **within issue #3**), verified by generating twice and diffing, not by matching issue #1's old checksums.

## Current state (verified by reading the branch)

- Generator (`data-generator/generate.py`): 12 CSV tables + `manifest.json` (row counts, sha256, quality summary). Profiles `small`/`medium`/`large` (large ≈ 750k rows). All rows held in memory as lists.
- Ingestion (`ingestion/load_raw.py`): idempotent DuckDB loader, 12 landing tables in `raw.*`, single-writer discipline.
- dbt (`transform/dbt/`): 12 `stg_*` views + 3 marts. Two layers only (staging → marts). Warn-severity DQ tests. `make dbt` runs `dbt run` + `dbt test` (no `build`, no `docs generate`).
- Serving (`serving/`): `export_marts_snapshot.py` exports 3 marts to Parquet; Rill project has 3 models/metrics/explores.
- Lake (`lake/publish_iceberg.py`): publishes the same 3 marts to Iceberg via Lakekeeper/MinIO + read-back count.
- Orchestration (`orchestration/airflow/`): flat DAG `seed → load_raw → dbt_run → dbt_test (+ optional publish_iceberg)` on the pinned `apache/airflow:3.1.0-python3.12` image, currently built with `PythonOperator`/`airflow import DAG` over `callables/pipeline.py`. **Phase 5 modernizes this to the Airflow 3 TaskFlow API** (`airflow.sdk` `@dag`/`@task`/`@task_group`), keeping the callables as thin delegates — see the TaskFlow decision below and Phase 5.
- Governance (`governance/openmetadata/`): **manual dbt-artifact ingestion only**. No Iceberg ingestion. OpenMetadata starts empty.
- Resource guards: `docker-compose.yml` `mem_limit`s; Makefile refuses to start `lake` and `governance` together.
- Version matrix (`versions.md`): DuckDB 1.5.4, dbt-core 1.11.12, dbt-duckdb 1.10.1, Rill v0.87.8, Airflow 3.x, MinIO pinned, Lakekeeper v0.13.1, OpenMetadata 1.6.5.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Demo-large deterministic data generation](./phase-01-demo-large-deterministic-data-generation.md) | Pending |
| 2 | [dbt lineage source-staging-intermediate-core-marts](./phase-02-dbt-lineage-source-staging-intermediate-core-marts.md) | Pending |
| 3 | [Rill explores expansion](./phase-03-rill-explores-expansion.md) | Pending |
| 4 | [Iceberg publication and read-back](./phase-04-iceberg-publication-and-read-back.md) | Pending |
| 5 | [Airflow full-flow DAG](./phase-05-airflow-full-flow-dag.md) | Pending |
| 6 | [OpenMetadata Iceberg and dbt ingestion](./phase-06-openmetadata-iceberg-and-dbt-ingestion.md) | Pending |
| 7 | [Docs verification and rollback](./phase-07-docs-verification-and-rollback.md) | Pending |

## Phase dependencies

```text
P1 (data) ──► P2 (dbt graph) ──► P3 (Rill)
                    │
                    ├──► P4 (Iceberg publish/read-back) ──► P6 (OpenMetadata ingestion)
                    │                                        ▲
                    └──► P5 (Airflow full-flow DAG:          │
                          generate→load→transform→serve→     │ (P6 crawls the Iceberg
                          publish)                           │  tables from P4 and the
                    │                                        │  dbt artifacts from P2)
                    └────────────────────────────────────────┘
P2, P3, P4, P5, P6 ───────────────────────────────────────► P7 (docs, verification, rollback)
```

- P2 depends on P1 (new tables must exist as sources).
- P3, P4 depend on P2 (marts / curated assets must exist).
- P5 orchestrates the P1–P4 data-pipeline steps as a visible DAG **through the Iceberg publish group**. Governance ingestion is **not** an Airflow task (see R2/decision below) — it is a host-side `make catalog-ingest` staged step in P6.
- P6 depends on P4 (Iceberg tables to crawl) and P2 (dbt artifacts to ingest). It does **not** depend on P5: it runs in a guarded co-run window with Airflow stopped.
- P7 documents and verifies everything; run last.

## Acceptance criteria (traceability to phases)

| # | Issue acceptance criterion | Phase(s) |
|---|---|---|
| AC1 | `demo-large` ≥ 300,000 total rows, deterministic, ≤16GB in normal use | P1 |
| AC2 | dbt build succeeds, ≥8 documented business-facing marts | P2 |
| AC3 | Lineage graph contains source, staging, intermediate/core, mart layers with multiple branches/joins | P2 |
| AC4 | Rill starts, ≥8 useful explores/metric views with non-empty data | P3 |
| AC5 | Airflow DAG visible, executes the complete data-pipeline sequence with clear task boundaries (generate→load→transform→serve→publish). Governance ingestion is the immediate downstream step, run via `make catalog-ingest` (out-of-DAG, see decision note) | P5 (+ handoff to P6) |
| AC6 | ≥8 curated Iceberg assets published and read-back verified | P4 |
| AC7 | OpenMetadata Iceberg ingestion **and** dbt artifact ingestion both complete; catalog shows curated assets + logical dbt lineage. Delivered via the guarded `make catalog-ingest` co-run window, not via Airflow | P6 |
| AC8 | Verification captures row counts, dbt results, Iceberg read-back, OM ingestion summaries, Airflow run state, app URLs | P7 (evidence produced across P1–P6) |
| AC9 | No credentials or runtime artifacts committed | P1–P7 (cross-cutting), enforced in P7 |
| AC10 | README/runbook explains startup order, resource trade-offs, architecture, teardown | P7 |

## Cross-cutting constraints

- **Resource safety:** default `core` path starts no containers. Heavy profiles (`orchestration`, `lake`, `governance`) stay opt-in and are normally run one at a time. The single exception — the OpenMetadata Iceberg ingestion window that needs `lake` + `governance` together — is a guarded, explicit-opt-in `make catalog-ingest` step that **stops Airflow first**, so the peak never includes `orchestration` + `lake` + `governance` at once; it has a documented memory budget and teardown (P6).
- **Single-writer discipline:** only one process writes `warehouse/retail.duckdb` at a time. Pipeline steps stay sequenced; Rill reads exported Parquet, not the live file.
- **Secrets:** all credentials come from env / `.env` (gitignored). `.env.example` documents non-production local defaults. No tokens, keys, or JWTs committed. Verified by secret scan in P7.
- **Determinism:** same `--profile --seed` ⇒ byte-identical CSVs and stable per-file checksums; `manifest.json`'s `generated_at` is the only intentionally non-reproducible field.
- **Reuse over invention:** extend existing entrypoints (`generate.py`, `load_raw.py`, dbt project, `export_marts_snapshot.py`, `publish_iceberg.py`, `callables/pipeline.py`) and keep a single source of truth for the curated-asset list shared by publish, read-back, and OpenMetadata Iceberg ingestion.

## Global risks and mitigations

| Risk | Mitigation |
|---|---|
| R1: demo-large blows memory on 16GB (in-memory generation, web_events explosion) | Stream rows to CSV incrementally; bound event volume with configurable caps (`--max-web-events`); size demo-large to comfortably exceed 300k but stay well under memory limits; record measured peak RSS in P1/P7. |
| R2: OpenMetadata Iceberg ingestion needs `lake` + `governance` co-running, conflicting with the existing safety guard | Governance ingestion is **out of the Airflow DAG** and runs only via the explicit, opt-in guarded `make catalog-ingest` window (P6): stop Airflow + heavy generation first, start `lake` + `governance`, run both ingestions + `verify_catalog`, tear down `lake`. Because Airflow is stopped, the peak is `lake` + `governance` only (~9GB of container limits + overhead), not three heavy profiles. Documented memory math + teardown. Guard stays on by default; override requires a deliberate flag. |
| R3: OpenMetadata 1.6.5 Iceberg (RestCatalog) connector config/version drift with Lakekeeper v0.13.1 | **Gate this early:** P6 step 1 is a compatibility spike that proves the exact RestCatalog + MinIO fileIO config against pinned versions **before** the dependent ingestion/verification work. If the connector cannot reach Lakekeeper v0.13.1 cleanly, record it in `versions.md` and either pin-bump (if safe) or invoke the documented fallback (dbt-artifact-only logical lineage). The fallback would only partially satisfy AC7, so it is flagged to the auditor; the preferred and gated-for outcome is validated Iceberg ingestion. |
| R4: Heavier dbt graph (facts at demo-large, e.g. fct_web_events) increases build time/memory | Keep intermediate models as views/ephemeral, materialize only facts/marts as tables, marts are aggregates (small); measure `dbt build` wall time + memory on demo-large in P7; keep demo default profile at `medium` for interactive demos. |
| R5: Determinism regressions from reordered RNG draws / new tables | Re-establish determinism within issue #3; verify by generating twice and diffing manifest checksums (P1, P7). |
| R6: Merge/branch dependency on PR #2 | **Resolved** — PR #2 is merged to `main` (`45daa70`). Branch is cut from `main`; no merge ordering remains. |
| R7: Curated-asset list drift across publish / read-back / Rill export / OM ingestion | Single shared **data file** `lake/curated_assets.json` (not a Python module) resolved by absolute path from each script's `__file__`, so it is import-safe when scripts run standalone. `publish_iceberg.py`, `export_marts_snapshot.py`, and a required YAML renderer for OM Iceberg ingestion all read it; a verification check asserts the rendered `iceberg_ingestion.yaml` matches the list (P4, P6). |
| R8: Verification evidence written under `plans/` is gitignored (`plans/**/*`), so AC8 evidence could silently miss the implementation PR | P7 writes shippable verification evidence to a **tracked** path under `docs/` (e.g. `docs/verification/`), not `plans/reports/`. The plan files themselves are force-added on the plan branch. |
| R9: demo-large streaming must stay deterministic while not holding all fact rows | P1 specifies a concrete single-pass streaming design (bounded per-order summary index, inline duplicate/null injection with observed counters, running sha256 during write); determinism verified by generating twice and diffing (P1, P7). |

## Validation & handoff

- **Plan validation:** this plan was validated by **Codex via codex-plugin-cc** (`codex-companion.mjs task`, read-only, `--effort high`, default/latest GPT routing; Codex thread `019f4a64-4b5f-7df2-b38e-624263ae45ba`) — not the ck:plan red-team/self-review path. Codex read the plan **and the actual repo code** and returned an initial verdict of **NEEDS-REWORK** with 11 findings (2 critical, 4 high, 4 medium, 1 low). All findings were fixed in this revision before commit:
  - Critical: stale PR #2 "still open" claim (now merged → branch from `main`); Airflow-govern-group vs co-run-stop-Airflow conflict (governance ingestion moved out of the DAG to `make catalog-ingest`).
  - High: OM 1.6.5 Iceberg connector compatibility now gated by an early spike (P6 step 1); streaming-generation design made concrete (P1); purchasing lineage no longer a dead-end (P2 required `fct_purchase_orders`/`fct_purchase_order_items` + `mart_supplier_purchasing`); P5→P6 ordering fixed (P6 no longer depends on P5).
  - Medium: curated-asset source of truth changed from a Python module to an import-safe JSON data file (P4/P3); required YAML renderer + match-check for Iceberg ingestion (P6); verification evidence relocated to tracked `docs/` (P7); host-vs-container ingestion ambiguity removed (P5/P6).
  - Low: corrected the `serving/rill/.gitignore` note to the real `serving/export/` root-ignore + `make clean` (P3).
- **Plan audit (plan-to-cook stage):** re-audited by **Codex via codex-plugin-cc** (`codex-companion.mjs task`, read-only, `--effort high`, default/latest GPT routing; Codex thread `019f4a73-5bca-7763-a4fa-5dcca1c8f7e8`). Codex read the revised plan **and** the current repo and returned **NEEDS-REWORK** with 8 findings (3 high, 5 medium, 0 low). All 8 were verified against the real code and fixed in this revision:
  - High: streaming design's per-order summary tuple was insufficient for `payments`/`returns` (they need `payment_method`/`order_total`/returned-item `refund_amount` only in-loop) → payments/returns now stream **inline** in the order loop, index feeds only shipments + checkout linkage (P1). Curated-asset vs Rill-explore drift (`mart_web_funnel_conversion`/`mart_data_quality` missing from the JSON; `mart_supplier_purchasing` missing as an explore) → one canonical 11-mart set shared identically by publish/export/explores (P3/P4). Airflow `publish` group needs container-network endpoints (`lakekeeper:8181`, `minio:9000`), not `localhost` defaults, plus a shared Compose network (P5).
  - Medium: no read-back-only CLI for the split `iceberg_read_back` task → `--read-back-only` flag added (P4) and wired (P5); OpenMetadata JWT wrongly listed as an Airflow credential → removed, OM creds are P6-only (P5); dbt facts count mismatch (diagram `fct_* (7)` vs 9 required) → diagram corrected to 9 with facts named (P2); dbt `serviceName`/logical-vs-physical mapping underspecified → `retail_duckdb` (logical) vs `retail_iceberg` (physical) fixed, two distinct services, mapping documented (P6); verification did not exercise the lake-enabled Airflow publish group for AC5 → added (P7).
- **Plan audit (Airflow 3 TaskFlow modernization):** after the binding user decision to modernize the DAG to the Airflow 3 public TaskFlow API, Phase 5 (and its touch-points in `plan.md` and Phase 7) were rewritten from `PythonOperator` to `airflow.sdk` `@dag`/`@task`/`@task_group`, then re-audited by **Codex via codex-plugin-cc** (`codex-companion.mjs task`, read-only, `--effort high`, default/latest GPT routing; Codex thread `019f4ac9-fabd-7051-a2cd-34d1d55020e1`). Codex read the revised plan **and** the current repo, confirmed the core decision against the official Airflow Task SDK docs (`airflow.sdk` exposes `dag`/`task`/`task_group`; module-scope `@dag` factory instantiation and `>>` group chaining are valid), and returned **NEEDS-REWORK** with 5 findings (2 high, 2 medium, 1 low). All 5 were fixed in this revision:
  - High: verification used `LAKE_PROFILE_ENABLED=1` while the gate only matched `"true"` → adopted a shared `_TRUTHY` set (`{"1","true","yes","on"}`) binding for both the gate and every instruction (P5). High: the flag is read at parse time, so a re-trigger alone can't enable `publish` → verification now recreates the orchestration service with the flag set so the DAG reparses (P5 step 5, P7 step 7).
  - Medium: import-safety was mis-attributed to importing `pipeline` inside the `@dag` factory (which runs at parse time) → corrected to the real guarantee, `callables/pipeline.py` has no top-level optional imports and shells out to the lake script (P5). Medium: stale `PythonOperator` comments remained in `Dockerfile`/`requirements.txt`/`docker-compose.yml` and Phase 7's grep was ambiguous → P5 now scopes comment cleanup for all three files and P7's grep asserts zero matches across the whole Airflow surface.
  - Low: skeleton used bare `@task` against the plan's own `@task(task_id=...)` rule → skeleton now uses explicit `task_id`.
- **Post-plan label flow:** plan created → `ready for plan audit`; on audit completion with all findings resolved and pushed → remove `ready for plan audit`, add `ready to cook`.
- **Next stage:** `/ck:cook` on this plan — this plan-audit stage is complete.

## Decisions for audit review (pre-made, non-blocking)

1. **Governance ingestion is out of the Airflow DAG (deviation from a literal reading of issue scope 4).** Issue scope 4 lists "metadata ingestion/verification" as part of the DAG. Running OpenMetadata + Lakekeeper + MinIO **alongside** Airflow exceeds the 16GB budget and conflicts with the co-run guard. Decision: the DAG shows visible task groups through `publish` (Iceberg), and governance ingestion is the immediate downstream step run via a guarded `make catalog-ingest` window with Airflow stopped. This satisfies AC5 (visible pipeline DAG) and AC7 (both ingestions complete) without the resource conflict, and keeps a single source of truth for the ingestion entrypoint. Alternative if the auditor insists on in-DAG governance: bake the pinned `openmetadata/ingestion` invocation into a gated `govern` task group that still only runs inside the co-run window with Airflow's footprint added to the budget — heavier and riskier on 16GB, so not the recommended path.
2. **OpenMetadata Iceberg ingestion uses a guarded, explicit-opt-in `lake`+`governance` co-run window (R2), gated by an early compatibility spike (R3).** If the auditor prefers a stricter never-co-run posture, the fallback is dbt-artifact-only logical lineage plus a documented manual Iceberg crawl on a machine with more RAM — but that would not fully satisfy AC7 on the 16GB target, so the co-run window is the recommended path.
3. **Verification evidence ships under tracked `docs/`, not gitignored `plans/` (R8).**
4. **Airflow DAG is modernized to the Airflow 3 public TaskFlow API (binding user decision).** Per the issue #3 decision comment, the pinned `apache/airflow:3.1.0-python3.12` DAG is rewritten from `PythonOperator` construction to `from airflow.sdk import dag, task, task_group` using `@dag`/`@task`/`@task_group`, with decorated tasks as thin delegates to the reusable functions in `callables/pipeline.py`. Constraints: no explicit `PythonOperator`, no deprecated `airflow.decorators` import; preserve the visible groups and the `generate → load → transform → serve → optional publish` sequence, import-safe lake gating, and single-writer discipline. Verification must cover compile/import, `airflow dags list`, `airflow dags list-import-errors`, task IDs / group graph, and a real triggered DAG run (Phase 5, Phase 7). This is a user decision, not an audit-reversible trade-off.

## Open questions

- None blocking.
