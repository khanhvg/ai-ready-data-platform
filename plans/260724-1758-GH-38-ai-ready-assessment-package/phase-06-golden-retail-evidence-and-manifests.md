# Phase 6: Golden retail evidence gaps and manifests

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phase 5](./phase-05-capability-architecture-and-demo-catalog.md)
- Decisions: [PD-03, PD-15–PD-16, PD-18](./architecture-decisions.md)
- Traceability: [AC-04, AC-10; SM-11–SM-16](./requirements-traceability.md)
- Existing runbook/proof: repository `docs/demo-runbook.md`, `docs/verification/GH-3-full-flow-evidence.md`
- Reconciled baseline: [scout-01](./scout/scout-01-reconciled-contracts-and-decisions.md)

## Overview

- Date: 2026-07-24
- Description: Reuse the existing golden retail pipeline and add only missing quarantine, PII classification/masking/access-policy proof, AI-ready manifest, Demo Guide, and stage evidence manifests.
- Priority: P2
- Implementation status: Completed
- Review status: Completed through merged Phase 6 verification evidence.

## Key Insights

- Existing ingestion, transformation, serving, Iceberg, Airflow, and OpenMetadata proof remains authoritative; duplicating it would introduce drift.
- Current controlled dbt warnings/deduplication are not an explicit quarantine dataset.
- Synthetic email is PII-like, but classification plus masking/access-control is not currently proved.
- Web display and customer maturity are consumers of neither command execution nor pipeline state; demo evidence is a separate namespace.

## Requirements

- Preserve exact current pipeline and public commands; no replacement stack or industry pipeline.
- Demonstrate ingestion, quality, quarantine, transformation, metadata/lineage, governance, policy-based access, serving, and AI-ready publication.
- At least one deliberately failing record/rule is detected, recorded in quarantine, excluded from an explicit accepted/curated partition, and absent from the governed AI-ready product without changing the legacy canonical 11 marts.
- At least one PII field is classified and masked; a bounded application-level local policy control denies raw/staging PII asset IDs and allows only the safe projection.
- Versioned AI-ready dataset manifest includes owner, contract/schema, quality/freshness SLA, access classification, lineage, reproduction instructions, and checksums.
- Versioned stage manifests point by relative path to actual artifacts and commands; ≥95% eligible guide steps automated.
- Heavy services staged within current memory guards; corrected OpenMetadata search/server limits are 1g/2g.

## Architecture

The canonical chain remains:

```text
generate.py -> load_raw.py -> dbt source/staging/intermediate/core/marts
             -> Parquet/Rill and Iceberg/Lakekeeper
             -> OpenMetadata logical dbt + physical Iceberg views
```

Use the existing deterministic invalid-order-status injection as the exact quality rule. Add complementary dbt models over deduplicated `stg_orders`: `quarantine_orders` selects status outside `completed|cancelled|returned|pending` and emits rule ID/reason/order key; `accepted_orders` selects only the allowed statuses. Tests prove the two sets are disjoint, their union equals `stg_orders`, quarantine is non-empty for the pinned small/seed-42 fixture, and no quarantined key appears in `accepted_orders` or the governed AI-ready product. Existing canonical 11 marts remain unchanged and are labeled legacy business marts rather than falsely claimed as the new quality-gated accepted boundary.

The governed AI-ready customer product consumes `accepted_orders`, joins customer attributes, and deterministically masks/pseudonymizes email. A policy entrypoint reads a checked YAML policy, accepts only a fixed role ID/asset ID/output root, opens DuckDB itself, denies raw/staging/customer-PII assets before query construction, and exposes only the safe product for the demo role. Tests invoke the real CLI and prove raw-deny/safe-allow, unknown-role/asset denial, safe output columns, and no arbitrary SQL/path input. This is an application authorization demonstration; the machine owner can still open DuckDB directly, so it is not database IAM.

`demo/manifests/stages/*.yaml` references output artifacts, verification commands, expected contract, limitations, and cleanup. `demo/manifests/ai-ready-customer-product.v1.yaml` is the versioned publication contract. Assessment web/catalog validates and displays these files; no engine dependency points from them into customer score inputs.

## Related code files

- Existing/reuse: `data-generator/generate.py`, `data/raw/manifest.json`, `ingestion/load_raw.py`
- Existing/reuse: `transform/dbt/dbt_project.yml`, `transform/dbt/models/**`, `transform/dbt/target/{manifest.json,catalog.json}`
- Existing/reuse: `serving/export_marts_snapshot.py`, `serving/rill/**`
- Existing/reuse: `lake/curated_assets.json`, `lake/publish_iceberg.py`
- Existing/reuse: `orchestration/airflow/dags/retail_batch_pipeline.py`
- Existing/reuse: `governance/openmetadata/ingestion/**`, `governance/openmetadata/verify_catalog.py`
- Create: `transform/dbt/models/quarantine/{quarantine_orders.sql,_quarantine__models.yml}`
- Create: `transform/dbt/models/curated/{accepted_orders.sql,_curated__models.yml}`
- Create: `transform/dbt/models/products/{ai_ready_customer_product.sql,_products__models.yml}`; keep it outside the canonical 11 business-mart publication list
- Create: `governance/policy/{access-policy.yaml,export_authorized_dataset.py,verify_access_policy.py}`
- Reuse: `demo/contracts/{demo-stage-manifest,ai-ready-dataset-manifest}-v1.schema.json` defined in Phase 2
- Create: `demo/manifests/stages/{ingestion,quality,quarantine,transformation,lineage,governance,access-control,serving,ai-ready-publication}.yaml`
- Create: `demo/manifests/ai-ready-customer-product.v1.yaml`, `demo/verify_manifests.py`
- Create/modify: `docs/demo-guide.md`, `docs/system-architecture.md`, `docs/demo-runbook.md`
- Create: focused dbt/policy/manifest tests under `assessment/tests/demo/`
- Modify: `Makefile` for `demo-contract`, `demo-verify`, and `demo-airflow-verify`

## Implementation Steps

1. Run an early compatibility spike for the exact PD-16 application authorization boundary on Python 3.12/DuckDB 1.5.4: invoke the real CLI and prove raw/staging classified-email asset denial, safe-product allowance, unknown-role/asset denial, no SQL/path input, and output schema constraints; record exact versions/limitations. If any required deny/allow property cannot be enforced, stop for BQ-02 rather than downgrade proof silently.
2. Add complementary `quarantine_orders`/`accepted_orders` models for the existing invalid-status scenario; emit rule/reason/source identifiers and prove non-empty quarantine, disjointness, full partition coverage, and exclusion from accepted/governed outputs, without changing the canonical 11 marts.
3. Classify `customers.email` in versioned policy/manifest content and add a deterministic masked/pseudonymous AI-ready product with tests proving raw email is absent and stable masked value is present.
4. Implement the bounded policy-controlled export and verifier; prove unauthorized raw/staging/unknown requests fail nonzero and authorized safe export succeeds with only the declared columns, with no claim of database IAM or protection from a local user opening DuckDB.
5. Define AI-ready dataset manifest schema/instance including ownership, contract/schema version, quality/freshness SLA, classification/access policy, dbt/OpenMetadata lineage references, reproduction commands, artifact checksums, and limitations.
6. Define all nine stage manifest schemas/instances and validator; each uses repository-relative paths and labels artifact origin, command, automation status, expected proof, cleanup, and non-scoring status.
7. Update the Demo Guide/runbook/architecture for the additive evidence path. Every executable setup/run/verify/cleanup step is a manifest row with `eligible_for_automation` and rationale; the ≥95% numerator/denominator are emitted explicitly. Presenter talk-track and optional visual browsing are non-executable and listed separately, not removed from the denominator after a failed automation attempt.
8. Add exact targets: `make demo-contract` validates both manifest schemas and semantic references without generated artifacts; after the existing core commands, `make demo-verify` validates the quarantine/accepted partition, PII/masking/policy behavior, manifests/checksums, stage coverage, automation ratio, and assessment-score separation. Assessment tests never start heavy profiles.
9. Verify core proof first: `make seed SCALE=small SEED=42`, `make load`, `make health`, `make dbt`, `make dbt-docs`, `make bi`, `make demo-contract`, then `make demo-verify`.
10. Stage optional proof one profile/window at a time. `make demo-airflow-verify` starts Airflow alone, waits healthy, checks import errors, triggers the default generate→load→transform→serve DAG, captures its exact run ID, polls all tasks to terminal success, and always tears Airflow down; merely starting the UI is not proof. Then run `make lake-up && make lake-publish && make down`; only after Airflow is stopped run guarded `make catalog-ingest`, verify, then `make down`. Reuse the tracked GH-3 full-flow publish/Rill evidence where explicitly referenced, but mark it historical rather than a current run. Capture current Compose limits including OpenMetadata search 1g/server 2g.
11. Mutation-test the separation: alter/remove demo stage artifacts and prove customer scenario maturity, confidence, gate, and finding priority JSON is byte-identical; only evidence-appendix availability may change.

## Todo list

- [x] Pass bounded access-policy compatibility spike or raise BQ-02.
- [x] Add explicit quarantine/accepted partition and curated-exclusion proof.
- [x] Add PII classification and masked safe product.
- [x] Prove raw-deny/safe-allow policy behavior.
- [x] Add versioned AI-ready dataset manifest.
- [x] Add and validate all nine stage manifests.
- [x] Update Demo Guide/runbook/architecture and automation ratio.
- [x] Run exact core, Airflow-DAG, then staged heavy evidence with current guards.
- [x] Prove demo evidence cannot alter customer maturity.

## Success Criteria

- Existing core regression remains green and canonical 11 marts remain consistent through `lake/curated_assets.json`.
- Invalid-status orders form a non-empty quarantine; accepted/quarantine are disjoint and complete; quarantined keys cannot appear in the explicit accepted boundary or governed AI-ready product; the canonical 11 marts retain their established contract and are not relabeled as quality-gated.
- `customers.email` is classified; safe output masks it; the real policy CLI denies raw/staging/unknown assets and allows only the safe export, with its application-level limitation stated.
- AI-ready manifest validates and contains every required ownership/contract/SLA/access/lineage/reproduction field.
- All nine stage manifests validate, point to real generated/tracked artifacts, and meet ≥95% eligible-step automation.
- Current Airflow proof executes and polls the default DAG rather than only starting containers; lake and governance proof runs in staged order, with only the guarded lake+governance co-run.
- Web can display every stage manifest/artifact read-only and cannot run the pipeline.
- Demo mutation leaves all customer assessment results unchanged.

## Risk Assessment

- Adding a twelfth publishable mart could break the canonical 11-asset contract; keep the safe mart outside that list unless all downstream contracts are intentionally updated and regressed.
- Existing warning rows may not map cleanly to one quarantine rule; choose one deterministic source rule and assert exact exclusion.
- Local policy enforcement may be mistaken for production IAM; label scope/limitations in manifests, guide, report, and UI.
- Heavy verification can exhaust 16GB; preserve one-profile sequencing and use the existing guarded exception only.
- Rollback: `make down`, revert the additive quarantine/safe-mart/policy/demo-manifest changes, and run existing `make clean` before regenerating the baseline core path. Preserve engagement folders/evidence and never remove named volumes unless separately authorized.

## Security Considerations

All demo data remains deterministic synthetic retail data. Never use customer data, credentials, OpenMetadata tokens in tracked evidence, or AWS/Terraform. The policy export fails closed, validates asset IDs, uses fixed output roots, and never accepts arbitrary SQL. Manifests redact environment values and contain relative paths/checksums only.

## Next steps

Review P6 evidence and its non-scoring boundary before Phase 7 joins assessment findings to catalog/demo references and adds initial deep dives plus an inert recipe extension.
