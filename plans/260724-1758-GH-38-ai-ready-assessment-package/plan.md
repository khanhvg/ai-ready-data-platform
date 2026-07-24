---
title: "Issue #38: AI-ready data platform assessment package"
description: "Build a portable, architect-led assessment workflow with deterministic scoring, reports, catalogs, and separate golden-demo evidence."
status: in-progress
priority: P2
effort: 36d
branch: feature/issue-38-phase-2-contracts-portability
tags: [assessment, architecture, evidence, local-first, data-platform]
created: 2026-07-24
---

# Issue #38: AI-ready data platform assessment package

## Outcome

Deliver a Python 3.12 local-first package for Solution/Enterprise Architects to create a customer engagement, conduct a quick assessment and selected deep dives, review explainable findings/gates, generate a deterministic standalone report, and export/import the engagement. Keep framework, knowledge catalog, and golden-demo evidence independent; demo facts never score customer maturity.

## Baseline and boundaries

- Immutable planning input: `58a9b7f45f5b2d473a39bc2f9eb9258fe92d0b2a`.
- Proven today: deterministic 18-table retail data; DuckDB/dbt 51-model lineage; 11 Rill/Iceberg assets; Airflow TaskFlow; OpenMetadata 45 logical tables/130 edges plus 11 physical assets; resource-safe staged commands.
- Issue gaps: no assessment content/contracts/store/engine/report/web/catalog; no explicit quarantine, classified-and-masked PII path, AI-ready dataset manifest, or demo-stage manifest.
- Customer answers/evidence are architect-entered. The package does not scan customer systems, infer maturity from this repository, run the demo pipeline, or restore learning/lab surfaces.
- Excluded: AWS/Terraform apply/destroy, credentials/customer data, hosted deployment, SaaS/multi-tenancy, customer scanning, pipeline control, vendor scoring, complex model training, learning portal/labs.

## Delivery phases

| Phase | Deliverable | Effort | Status | Progress |
|---|---|---:|---|---:|
| 1 | [Rubric/report prototype and synthetic calibration](./phase-01-rubric-report-prototype-and-calibration.md) | 4d | Completed | 100% |
| 2 | [Versioned schemas, local store, migration, import/export](./phase-02-versioned-contracts-local-store-and-portability.md) | 5d | Completed | 100% |
| 3 | [Deterministic assessment engine and report generation](./phase-03-deterministic-engine-and-report-generation.md) | 5d | Pending | 0% |
| 4 | [Loopback server-rendered assessment workflow](./phase-04-loopback-web-assessment-workflow.md) | 4d | Pending | 0% |
| 5 | [Capability, architecture, mapping, and Demo Guide catalog](./phase-05-capability-architecture-and-demo-catalog.md) | 4d | Pending | 0% |
| 6 | [Golden retail pipeline evidence gaps and manifests](./phase-06-golden-retail-evidence-and-manifests.md) | 5d | Pending | 0% |
| 7 | [End-to-end mappings, deep dives, and recipe extension](./phase-07-mappings-deep-dives-and-recipe-extension.md) | 4d | Pending | 0% |
| 8 | [Portability, security, resource, regression, docs, release](./phase-08-verification-regression-docs-and-release.md) | 5d | Pending | 0% |

Binding sequence: `P1 → P2 → P3 → P4 → P5 → P6 → P7 → P8`. The first reviewable vertical slice is **Phase 1 only**; it proves the rubric/report/scenarios before framework infrastructure, web, or golden-pipeline work. Recommended later reviews follow P2–P3, P4–P5, P6–P7, and P8; do not create GitHub issues from this plan.

## Plan controls

- [Architecture decisions](./architecture-decisions.md) records reversible defaults `PD-01…` and deferred alternatives.
- [Requirements traceability](./requirements-traceability.md) maps all `AC-01…AC-12` and `SM-01…SM-17` to steps and commands. These IDs are plan-only; implementation names describe behavior.
- [Independent combined plan-readiness audit](./reports/combined-plan-readiness-audit.md) records the immutable input, evidence-backed findings, corrections, residual execution conditions, and verdict.
- Every phase has rollback, cleanup, security, and verification. Assessment test targets start no containers; heavy services remain staged, with only the existing guarded lake+governance window.
- Implementation remains gated on the owner-required independent combined plan-readiness audit and corresponding GitHub authorization. This planner self-check is not that audit.

## Acceptance

Complete only when all traceability rows pass, `report.json` and standalone `report.html` regenerate without edits, a copied engagement round-trips without data loss or path/secret leakage, the golden stage chain is evidenced without influencing maturity, and the clean-checkout assessment plus existing core regression pass within the documented resource model.
