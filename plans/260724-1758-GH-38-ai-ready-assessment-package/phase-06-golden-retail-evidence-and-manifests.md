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
- Implementation status: Pending
- Review status: Pending catalog/Demo Guide contract review.

## Key Insights

- Existing ingestion, transformation, serving, Iceberg, Airflow, and OpenMetadata proof remains authoritative; duplicating it would introduce drift.
- Current controlled dbt warnings/deduplication are not an explicit quarantine dataset.
- Synthetic email is PII-like, but classification plus masking/access-control is not currently proved.
- Web display and customer maturity are consumers of neither command execution nor pipeline state; demo evidence is a separate namespace.

## Requirements

- Preserve exact current pipeline and public commands; no replacement stack or industry pipeline.
- Demonstrate ingestion, quality, quarantine, transformation, metadata/lineage, governance, policy-based access, serving, and AI-ready publication.
- At least one deliberately failing record/rule is detected, recorded in quarantine, and excluded from curated outputs.
- At least one PII field is classified and masked; a bounded local policy control denies raw and allows the safe projection.
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

Add an explicit dbt quarantine model selecting a known invalid input rule with rule ID/reason/source key. Preserve the canonical 11 marts, and add a separate governed AI-ready customer product that anti-joins quarantined keys and deterministically masks/pseudonymizes email. A small policy entrypoint reads a checked YAML policy and exposes only that safe product for the demo role; tests must prove raw PII denial and safe-product allowance. This is a bounded local demonstration control, not production IAM.

`demo/manifests/stages/*.yaml` references output artifacts, verification commands, expected contract, limitations, and cleanup. `demo/manifests/ai-ready-customer-product.v1.yaml` is the versioned publication contract. Assessment web/catalog validates and displays these files; no engine dependency points from them into customer score inputs.

## Related code files

- Existing/reuse: `data-generator/generate.py`, `data/raw/manifest.json`, `ingestion/load_raw.py`
- Existing/reuse: `transform/dbt/dbt_project.yml`, `transform/dbt/models/**`, `transform/dbt/target/{manifest.json,catalog.json}`
- Existing/reuse: `serving/export_marts_snapshot.py`, `serving/rill/**`
- Existing/reuse: `lake/curated_assets.json`, `lake/publish_iceberg.py`
- Existing/reuse: `orchestration/airflow/dags/retail_batch_pipeline.py`
- Existing/reuse: `governance/openmetadata/ingestion/**`, `governance/openmetadata/verify_catalog.py`
- Create: `transform/dbt/models/quarantine/{quarantine_orders.sql,_quarantine__models.yml}`
- Create: `transform/dbt/models/products/{ai_ready_customer_product.sql,_products__models.yml}`; keep it outside the canonical 11 business-mart publication list
- Create: `governance/policy/{access-policy.yaml,export_authorized_dataset.py,verify_access_policy.py}`
- Reuse: `demo/contracts/{demo-stage-manifest,ai-ready-dataset-manifest}-v1.schema.json` defined in Phase 2
- Create: `demo/manifests/stages/{ingestion,quality,quarantine,transformation,lineage,governance,access-control,serving,ai-ready-publication}.yaml`
- Create: `demo/manifests/ai-ready-customer-product.v1.yaml`, `demo/verify_manifests.py`
- Create/modify: `docs/demo-guide.md`, `docs/system-architecture.md`, `docs/demo-runbook.md`
- Create: focused dbt/policy/manifest tests under `assessment/tests/demo/`

## Implementation Steps

1. Run an early compatibility spike for the bounded policy control on Python 3.12/DuckDB 1.5.4: prove the safe-export entrypoint can deny raw classified email and allow only `ai_ready_customer_product`; record exact versions/limitations. If it cannot enforce allow/deny, stop for BQ-02 rather than downgrade proof silently.
2. Add explicit quarantine model/schema tests using an existing deterministic invalid scenario; emit rule/reason/source identifiers and prove at least one row is quarantined while absent from the governed AI-ready product, without changing the canonical 11 marts.
3. Classify `customers.email` in versioned policy/manifest content and add a deterministic masked/pseudonymous AI-ready product with tests proving raw email is absent and stable masked value is present.
4. Implement the bounded policy-controlled export and verifier; prove unauthorized raw access request fails nonzero and authorized safe export succeeds, with no claim of general database IAM.
5. Define AI-ready dataset manifest schema/instance including ownership, contract/schema version, quality/freshness SLA, classification/access policy, dbt/OpenMetadata lineage references, reproduction commands, artifact checksums, and limitations.
6. Define all nine stage manifest schemas/instances and validator; each uses repository-relative paths and labels artifact origin, command, automation status, expected proof, cleanup, and non-scoring status.
7. Update the Demo Guide/runbook/architecture for the additive evidence path. Calculate eligible automated steps/total and require ≥95%; manual UI browse/talk-track steps are labeled non-automatable and excluded transparently.
8. Verify core proof first: `make seed SCALE=small SEED=42`, `make load`, `make health`, `make dbt`, `make dbt-docs`, `make bi`, then manifest/policy checks. Assessment tests never start heavy profiles.
9. Stage optional proof one profile/window at a time: `make airflow && make down`; `make lake-up && make lake-publish && make down`; only after Airflow is stopped run guarded `make catalog-ingest`, verify, then `make down`. Capture current Compose limits including OpenMetadata search 1g/server 2g.
10. Mutation-test the separation: alter/remove demo stage artifacts and prove customer scenario maturity, confidence, gate, and finding priority JSON is byte-identical; only evidence-appendix availability may change.

## Todo list

- [ ] Pass bounded access-policy compatibility spike or raise BQ-02.
- [ ] Add explicit quarantine and curated-exclusion proof.
- [ ] Add PII classification and masked safe product.
- [ ] Prove raw-deny/safe-allow policy behavior.
- [ ] Add versioned AI-ready dataset manifest.
- [ ] Add and validate all nine stage manifests.
- [ ] Update Demo Guide/runbook/architecture and automation ratio.
- [ ] Run core then staged heavy evidence with current guards.
- [ ] Prove demo evidence cannot alter customer maturity.

## Success Criteria

- Existing core regression remains green and canonical 11 marts remain consistent through `lake/curated_assets.json`.
- A deterministic failing row/rule appears in quarantine and cannot appear in the governed AI-ready product; the canonical 11 marts retain their established contract.
- `customers.email` is classified; safe output masks it; policy verifier denies raw and allows safe export.
- AI-ready manifest validates and contains every required ownership/contract/SLA/access/lineage/reproduction field.
- All nine stage manifests validate, point to real generated/tracked artifacts, and meet ≥95% eligible-step automation.
- Existing Airflow/lake/governance proof runs only in staged order; only guarded lake+governance co-run occurs.
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
