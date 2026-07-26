# Golden Retail Evidence Demo Guide

This presenter guide follows the existing retail pipeline and the nine versioned
stage manifests under `demo/manifests/stages/`. It is a local, deterministic
illustration only. Nothing in this guide is customer assessment evidence, and
artifact availability cannot change maturity, confidence, findings, priorities,
gates, or readiness.

## Fixed operating boundary

- Use only deterministic synthetic data generated with `SCALE=small SEED=42`.
- Run the core proof before any optional profile.
- Run Airflow, lake, and governance in the documented staged order. Never overlap
  Airflow with lake or governance. The existing guarded catalog-ingestion window
  is the only lake-plus-governance exception.
- Use `make down` after each optional profile. Do not remove named volumes.
- The assessment web page is read-only. It displays repository-relative evidence
  but exposes no command, SQL, pipeline, container, credential, cloud, upload, or
  deployment control.
- The policy export is an application-level local demonstration. It is not
  DuckDB IAM, and a local machine owner can open the database directly.

## Core evidence

Run the exact lightweight sequence:

```bash
make seed SCALE=small SEED=42
make load
make health
make dbt
make dbt-docs
make bi
make demo-contract
make demo-verify
```

The current pinned fixture produces 1,000 deduplicated staging orders: 990
accepted rows and 10 quarantined invalid-status rows. The two partitions are
disjoint and complete. Quarantined keys are absent from both `accepted_orders`
and `ai_ready_customer_product`.

The governed product is outside `lake/curated_assets.json`, so the established
eleven legacy business marts remain the sole Parquet, Rill, and Iceberg
publication inventory. The product exposes deterministic pseudonymous order,
customer, and email-derived keys and never publishes raw email, names, customer
IDs, or order IDs.

`make demo-verify` invokes the real fixed-interface policy CLI. It proves raw,
staging, classified-email, unknown-role, unknown-asset, SQL-input, and
output-path attempts fail nonzero; only the safe product is allowed.

## Optional runtime evidence

Run one profile/window at a time:

```bash
make demo-airflow-verify
make lake-up
make lake-publish
make down
```

`make demo-airflow-verify` starts Airflow alone, waits for health, checks DAG
imports, triggers one exact run ID, polls all six default tasks to terminal
success, records ignored local evidence, and always calls `make down`.

The current OpenMetadata stage requires a local ingestion-bot token:

```bash
make catalog-ingest
make down
```

If the token is unavailable, do not run or claim a current catalog ingestion.
The metadata stage manifest remains `historical` with
`current_execution: unexecuted`; the tracked GH-3 record is historical context
only. Current Compose limits remain 1g for OpenMetadata search and 2g for the
server.

## Stage manifest index

| Presenter stage | Versioned manifest | Current truth |
|---|---|---|
| Ingestion | `demo/manifests/stages/ingestion.yaml` | Current core proof |
| Quality and quarantine | `demo/manifests/stages/quality-quarantine.yaml` | Current core proof |
| Transformation | `demo/manifests/stages/transformation.yaml` | Core plus exact Airflow proof |
| Metadata | `demo/manifests/stages/metadata.yaml` | Historical; current ingestion unexecuted without token |
| Lineage | `demo/manifests/stages/lineage.yaml` | Current dbt lineage; catalog history labeled separately |
| Governance | `demo/manifests/stages/governance.yaml` | Current classification and product contract |
| Policy access | `demo/manifests/stages/access-control.yaml` | Current application-level allow/deny proof |
| Serving | `demo/manifests/stages/serving.yaml` | Current local serving; lake proof staged separately |
| AI-ready publication | `demo/manifests/stages/ai-ready-publication.yaml` | Current manifest and deterministic output |

The nine manifests declare 30 eligible run and cleanup rows and 30 automated steps:
`30/30 = 100%`, above the 95% requirement. Presenter talk-track and optional
visual browsing are non-executable activities and are listed separately from the
automation denominator.

## Cleanup and rollback

Use `make down` to stop optional profiles and `make clean` to remove generated
CSV, DuckDB, dbt, and serving artifacts. Neither command removes assessment
engagement folders. Rollback is additive: revert the quarantine, accepted,
product, policy, manifest, and read-only presentation changes, then regenerate
the baseline core path. No cloud resource exists to destroy.
