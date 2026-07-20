# Repository Inventory for Issue #5 Discovery

## Summary

- Discovery input SHA: `9bcacd7a44a33d298388dca2a8d2b398c6bb22a8`.
- Git base: `origin/main` at `45daa70b20414c5dee76a18592ab905c11443d3b`.
- Branch: `plan/issue-5-enterprise-learning-sandbox`.
- The branch is exactly PR #4's current head and is five commits / 106 changed files ahead of
  `origin/main` (`+4,800/-333`). PR #4 is open and mergeable, not merged.
- Recommendation input: preserve the issue #3 golden data-platform assets, selectively refactor
  their execution/evidence seams, and add the learning portal and AWS track as new surfaces. A
  repository-wide rewrite has no evidence advantage and would discard verified behavior.

## Branch, Issue, and PR Dependencies

| Item | Exact state on 2026-07-21 | Discovery implication |
|---|---|---|
| Issue #5 | Open; labels `enhancement`, `triaged`, `risk:high`; one intake comment | Discovery may inform planning, but does not authorize implementation or a state transition. |
| Issue #3 | Open; implementation reported complete and awaiting review | Its acceptance evidence is relevant but not merged project history. |
| PR #4 | Open, mergeable, `CLEAN`; base `45daa70...`, head `9bcacd7...`; no CI checks | The golden baseline is a branch dependency. Freeze the exact head or merge/rebase it before issue #5 implementation branches fan out. |
| Current worktree | Clean before discovery; `docs/code-standards.md` absent | The issue body's warning about preserving that untracked file applies if it reappears in another worktree, but there is no such file here to inventory or commit. |
| Existing plan | `plans/260710-1145-GH-3-expand-lineage-dashboards-governance/` | Completed issue #3 plan with seven tracked phase files; do not rewrite it during issue #5 planning. |

The input/base relation is important: `origin/main` does not contain the 18-table generator,
four-layer dbt graph, expanded Rill content, current Airflow DAG, or full OpenMetadata/Iceberg
integration. A planner that scouts only `main` will design against the wrong repository.

## Valuable Assets and Preservation Candidates

| Surface | Actual asset at input SHA | Evidence/value | Preserve posture |
|---|---|---|---|
| Deterministic retail data | `data-generator/generate.py` (947 lines), `schema.md`, 18 table schemas, four scale profiles, seed/caps, controlled anomalies, per-file SHA-256 and row-count manifest | Historical double-run evidence: 620,340 `demo-large` rows, byte-identical CSVs, about 16.8 seconds and 78-92 MB on an M1 Pro | Preserve behavior and golden outputs. Refactor the large module only behind characterization tests. |
| Raw landing | `ingestion/load_raw.py` and DuckDB `raw.*` contract | Idempotent drop/recreate load; validates all manifest counts | Preserve local fast path. Add lab-safe wrappers rather than replacing it. |
| dbt graph | 18 staging SQL models, 6 intermediate, 16 core (7 dimensions + 9 facts), 11 marts, YAML tests/docs, one singular test | Historical `dbt build`: PASS=177, WARN=9, ERROR=0; 51-model graph | Preserve models, sources, warning semantics, names, and mart output contracts. Add contract/fitness checks. |
| Rill | 11 snapshot models, 11 metrics views, 11 explores, one DuckDB connector | Historical runtime API verified all explores non-empty | Preserve as the default local BI candidate unless a measured portal/Superset spike proves lower total learning cost. |
| Snapshot seam | `serving/export_marts_snapshot.py` and `lake/curated_assets.json` | Same 11-mart allow-list feeds Rill and Iceberg | Preserve as an explicit governed-data-product boundary; validate drift automatically. |
| Airflow | Airflow 3.1 TaskFlow DAG plus import-safe callables; five visible groups, optional publish | Historical real runs passed with and without publish | Preserve as an optional orchestration lab. Characterize task graph and reset behavior before changing. |
| Local lakehouse | MinIO, Lakekeeper 0.13.1/Postgres, DuckDB Iceberg publisher/read-back | Historical 11/11 publish and read-back | Preserve local profile; fix/teach non-atomic publish as a controlled failure rather than silently treating it as production-safe. |
| Governance | OpenMetadata 1.6.5 server, MySQL, Elasticsearch, Iceberg/dbt ingestion, bootstrap and verification scripts | Historical ingest: 11 physical tables, 45 logical tables, 130 lineage edges, no errors | Preserve concepts and adapters. Version-refresh compatibility is an early gate; current versions are not a 2026 target recommendation. |
| Resource guardrails | Compose profiles, memory limits, mutual-exclusion checks, guarded lake+governance window | Existing design avoids all heavy profiles concurrently | Preserve and convert to executable resource-budget assertions. |
| Documentation/evidence | README, architecture/storage/orchestration/runbook docs, `docs/verification/GH-3-full-flow-evidence.md`, `versions.md` | Rich exact-command evidence from 2026-07-10 | Preserve as historical golden evidence; do not present it as a current clean-checkout rerun. |

## Current Runnable Evidence

Discovery deliberately did not generate data, build images, start services, install project
dependencies, or mutate product/runtime state. The following read-only or in-memory checks ran at
the input SHA:

| Check | Result | Boundary |
|---|---|---|
| Worktree and branch inspection | Clean; expected branch; input SHA captured | Does not prove runtime behavior. |
| Python source compilation | 10/10 sources compiled in memory | Syntax only; no imports or service calls. |
| JSON parsing | `lake/curated_assets.json` and `release-manifest.json` valid | Does not validate semantic drift. |
| Docker Compose render | All profiles render; 9 services and 5 named volumes; exit 0 | No image pull, health, persistence, or architecture test. |
| Markdown/Git whitespace baseline | `git diff --check` passed before discovery edits | Formatting only. |
| Tool availability | Python 3.12.3, Docker 29.4.0, Terraform 1.12.2, Node 22.22.3, npm 10.9.8, ClaudeKit 4.5.2, `gh` 2.86.0 | Rill, dbt, and `.venv` are absent. |
| PR checks | `gh pr checks 4` reports no checks | Historical manual evidence is not CI enforcement. |

Historical evidence at `docs/verification/GH-3-full-flow-evidence.md` records real execution on
2026-07-10. It also records a stale `.venv` dependency failure that required rebuilding the local
environment. That incident is evidence for dependency-lock and clean-checkout gates, not a reason
to dismiss the successful run.

## Compose State and Resource Inventory

| Profile | Services | Declared memory limits | Durable local state |
|---|---|---:|---|
| `core` | No containers; generator, DuckDB, dbt, snapshot exporter | Not constrained by Compose | Host CSV, manifest, DuckDB, Parquet and dbt/Rill artifacts; all ignored |
| `orchestration` | Airflow standalone | 4 GiB | `airflow-home`; project root is mounted read-write into the task container |
| `lake` | MinIO, init job, Lakekeeper, migration job, Postgres | 3.25 GiB declared across services | `minio-data`, `lakekeeper-db-data` |
| `governance` | OpenMetadata, MySQL, Elasticsearch | 4 GiB | `openmetadata-db-data`, `openmetadata-es-data` |
| Guarded co-run | Lake + governance after Airflow stops | 7.25 GiB declared | Both state sets retained across `down` |

Declared limits are ceilings, not measured peak RSS or proof that Docker Desktop plus the portal
fits a 16 GiB laptop. The first vertical slice needs a machine-readable budget, profile matrix,
and measured cold/warm peaks.

## Generated and Ignored Artifacts

`git check-ignore -v` maps the requested issue #5 discovery path to `.gitignore:62`:
`plans/**/*`. Only the exact issue directory may be force-added.

Important generated/ignored surfaces include:

- `.hermes/` logs and prompts;
- `.venv/`;
- `data/raw/*.csv` and `data/raw/manifest.json`;
- `warehouse/*.duckdb` and WAL files;
- `serving/export/*.parquet`, Rill `.rill/` and `tmp/`;
- dbt `target/`, `logs/`, packages, and `.user.yml`;
- Airflow logs/database;
- local lake/OpenMetadata data directories;
- all `plans/**/*` except the repository's explicitly force-added plan artifacts.

The root `release-manifest.json` is not the retail generator manifest. It is a 1,558-entry
ClaudeKit release manifest (`version: 2.20.0`, generated 2026-06-18) containing paths unrelated to
the 138 files tracked in this repository. Treat it as legacy/tooling provenance until ownership
is clarified; do not use it as a product golden baseline.

## Baseline Gaps

| Gap | Severity | Why it matters before planning/implementation |
|---|---|---|
| PR #4 is unmerged and has no CI | Critical | The proposed issue #5 foundation can move or disappear. Pin/merge it and run clean-checkout gates. |
| No executable golden-baseline command | Critical | Historical evidence cannot be regenerated by one credential-free command with machine-readable output. |
| Generated fixtures are ignored and absent | High | Clean-checkout tests must generate bounded fixtures and never depend on a developer's prior state. |
| `.venv` target is not keyed to requirement hashes | High | Dependency changes can leave an apparently valid but incompatible environment. |
| No application/API/web source exists | High | The first vertical slice is a true new subsystem, including identity, progress, lab runner, reset, verification and evidence contracts. |
| No Terraform/AWS assets exist | High | Networking, IAM, ECS capacity, persistence, backup, cost and teardown are greenfield; local Compose is not an AWS design. |
| Stateful AWS ownership is undecided | Critical | ClickHouse, Superset metadata, OpenMetadata metadata/search and the Iceberg catalog cannot be placed safely on scale-to-zero compute by implication. |
| Local Iceberg publish is non-atomic | High | `DROP TABLE` then `CREATE TABLE` can expose absence after failure; acceptable demo trade-off must become an explicit lab/rollback invariant. |
| OpenMetadata repeat ingest does not reconcile removed/renamed dbt models | High | Long-lived learner state can accumulate stale catalog objects and misleading lineage. |
| Default local ports and placeholder credentials are development-only | High | The portal must not expose these services beyond localhost or reuse placeholder auth in AWS. |
| Airflow mounts repository root read-write | High | A learner task or compromised DAG can alter the worktree; lab execution needs scoped workspaces and reset boundaries. |
| No architecture/API/data contract validators or frontend tests | High | Issue #5 acceptance requires C4, OpenAPI/AsyncAPI, accessibility, browser, lab and Terraform gates that do not exist. |
| Current versions are historical pins | High | OpenMetadata 1.6.5, Elasticsearch 8.11.4 and Lakekeeper 0.13.1 require a compatibility/security refresh before target selection. |
| No cost envelope or AWS residual-cost inventory | Critical | Office-hours compute shutdown does not eliminate managed database, search, load balancer, NAT, storage, logs, secrets, state or AgentCore charges. |

## Inventory Decision

Use `9bcacd7...` as the provisional immutable input until the maintainer decides how PR #4 lands.
Do not rebuild the repository. Preserve the deterministic data/model/governance spine, build a
clean-checkout golden command around it, and introduce the portal/AWS track behind explicit
contracts. If PR #4 changes, rerun discovery deltas and the golden baseline before the planner
freezes file ownership.

## Unresolved Questions

- Will PR #4 merge unchanged, be rebased, or remain a pinned branch dependency?
- What maximum cold-start time and measured local RSS are acceptable for a lesson profile?
- Is ClickHouse an authoritative durable warehouse or a disposable serving projection rebuilt
  from S3/Iceberg?
- What monthly AWS residual-cost ceiling and recovery objective may the planner design for?
