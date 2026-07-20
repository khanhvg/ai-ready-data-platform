---
title: "Issue #5: Enterprise Architecture Learning Sandbox"
description: "Preserve the shipped retail data spine and deliver a credential-free, interactive architecture-learning vertical slice before gated AWS and optional AI waves."
status: pending
priority: P1
issue: 5
branch: "plan/issue-5-enterprise-learning-sandbox"
tags: [feature, frontend, backend, data-platform, architecture, infra, critical]
blockedBy: []
blocks: []
created: "2026-07-20T18:31:21.534Z"
createdBy: "ck:plan"
source: skill
mode: deep-tdd
inputMainSha: "3cd3d41f71582774e8d9656a51d1044035f4503c"
reviewedTreeHead: "d0273731a5077cc17c2f4398057623b83a50bb65"
discoverySha: "d3ce0c5832cca4f1b68299cbba111e7cc6c7a430"
planningSyncSha: "b04ff80486de8a9c008c6320669212f27df80182"
---

# Issue #5: Enterprise Architecture Learning Sandbox

## Overview

Build a hands-on-first Enterprise Architecture learning sandbox around the shipped issue #3
retail platform. Preserve generator anomalies, dbt/mart/lineage/metric contracts, Rill, local
DuckDB, MinIO/Lakekeeper Iceberg, OpenMetadata, and unrelated user files. Add a content-driven
portal as a modular monolith and isolate privileged lab execution behind a typed, deny-by-default
runner. The first release is single-user, localhost-only, credential-free, and completes one real
failure-reset-verify-evidence journey on a 16 GiB laptop.

The first journey asks: **Can Retail Operations trust a promotion decision when fulfillment
delays, returns/refunds, and controlled data-quality failures distort the headline?** It uses the
existing `mart_promotion_effectiveness`, `mart_fulfillment_performance`,
`mart_returns_analysis`, and `mart_data_quality` products.

AWS is a later, non-applying track: configurable `ap-southeast-1`, weekdays 08:00-18:00
`Asia/Ho_Chi_Minh`, ECS on EC2, ClickHouse, Superset, OpenMetadata, and S3/Iceberg. Budget,
retention, cold-start SLO, and production RTO/RPO remain TBC and block every AWS apply. AI,
LangGraph, Restate, and AgentCore are admission-gated after the local and governed-data waves.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Immutable Golden Baseline and Architecture Contract](./phase-01-immutable-golden-baseline-and-architecture-contract.md) | Pending |
| 2 | [Representative Lesson and Web Stack Spike](./phase-02-representative-lesson-and-web-stack-spike.md) | Pending |
| 3 | [Shared Lesson Lab and Evidence Contract](./phase-03-shared-lesson-lab-and-evidence-contract.md) | Pending |
| 4 | [Privileged Local Lab Runner and Security Boundary](./phase-04-privileged-local-lab-runner-and-security-boundary.md) | Pending |
| 5 | [Runnable Portal Vertical Slice](./phase-05-runnable-portal-vertical-slice.md) | Pending |
| 6 | [Architecture Curriculum Templates and Fitness Functions](./phase-06-architecture-curriculum-templates-and-fitness-functions.md) | Pending |
| 7 | [Data Pipeline Guided Labs](./phase-07-data-pipeline-guided-labs.md) | Pending |
| 8 | [Local Compose Profiles and Resource Measurement](./phase-08-local-compose-profiles-and-resource-measurement.md) | Pending |
| 9 | [AWS State Cost and Persistence Decisions](./phase-09-aws-state-cost-and-persistence-decisions.md) | Pending |
| 10 | [Terraform Networking IAM State and ECS Scheduling](./phase-10-terraform-networking-iam-state-and-ecs-scheduling.md) | Pending |
| 11 | [AWS Analytics BI Governance and Iceberg Adapters](./phase-11-aws-analytics-bi-governance-and-iceberg-adapters.md) | Pending |
| 12 | [Optional AI Admission and Add-on](./phase-12-optional-ai-admission-and-add-on.md) | Pending |
| 13 | [Verification Release Recovery and Rollback](./phase-13-verification-release-recovery-and-rollback.md) | Pending |

## Dependencies

- No active cross-plan blocker. Issue #3 is shipped; PR #4 merged at
  `3cd3d41f71582774e8d9656a51d1044035f4503c`.
- The merge commit tree equals reviewed head
  `d0273731a5077cc17c2f4398057623b83a50bb65`.
- Discovery input is immutable at
  `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430`; its STOP verdict still blocks
  implementation, destructive migration, and cloud actions until the relevant gates clear.
- The older issue #3 plan has stale phase metadata but is historical evidence, not an unfinished
  dependency; do not edit it in issue #5.

## Leading Decisions and TBC Gates

| Scope | Leading decision | Gate |
|---|---|---|
| Repository | Preserve + selective refactor + new portal/AWS bounded contexts | Rebuild only after characterization evidence disproves refactor |
| Physical services | Portal modular monolith + isolated privileged runner | Extract more services only for measured security/scale/release NFR |
| Local data/BI | DuckDB + Rill; MinIO/Lakekeeper; OpenMetadata | Replacement requires measured learning/resource win |
| Web stack | Time-box Astro, Next.js, and React/Vite with one real lesson contract | Winner ADR required before Phase 5 |
| Local identity | Single-user localhost; hosted multi-user is an explicit evolution | Same-user race/security tests still mandatory |
| AWS ClickHouse | Disposable serving projection rebuilt from S3/Iceberg | Rebuild/readiness/equivalence evidence and owner approval |
| AWS catalog | Glue Iceberg REST is the leading candidate | Client/auth/lifecycle/cost compatibility evidence |
| AWS apply | Not authorized | Budget + retention + cold-start + RTO/RPO + state/trust approvals |
| AI | Deferred optional add-on | All admission checks in Phase 12 |

## Implementation Waves

1. **Runnable local journey:** Phases 1-5. Shared-core owner freezes golden/evidence contracts;
   the web spike selects a stack; runner and portal deliver the complete local journey.
2. **Architecture and data curriculum:** Phases 6-8. Add only lessons with controlled failures,
   quality attributes, and executable evidence; measure mutually exclusive profiles.
3. **AWS non-applying design/build:** Phases 9-11. Decision records first, then Terraform and
   adapters; no apply.
4. **Optional AI:** Phase 12 only after admission.
5. **Release evidence:** Phase 13 runs clean-checkout, browser, recovery, policy, and rollback
   gates.

## Master Acceptance

- One clean-checkout command regenerates ignored fixtures and emits schema-valid,
  machine-readable exact-SHA evidence.
- One accessible local journey reaches a verified data product through a controlled failure,
  reset, architecture decision, and evidence record without cloud credentials.
- All Critical/High discovery findings retain an owner, gate, verification, mitigation/rollback,
  and dependency in `requirements-traceability.md`.
- Local and AWS C4/deployment/dynamic sources render and validate; views exist only for a stated
  stakeholder concern.
- API taxonomy remains logical; physical deployment begins with two processes, not five API
  services.
- Resource, cost, security, accessibility, recovery, Terraform, data, browser, and optional AI
  fitness functions have named commands and retained evidence.
- No destructive rewrite, Terraform apply, cloud resource creation, validation, audit, or
  implementation occurs in this planning phase.

## Companion Artifacts

- [Implementation issue graph](./implementation-issue-graph.md)
- [Requirements traceability](./requirements-traceability.md)
- [Curriculum and competency map](./curriculum-and-competency-map.md)
- [Lesson/lab contract](./lesson-lab-contract.md)
- [Architecture decisions](./architecture-decisions.md)
- [Architecture view source plan](./architecture-view-plan.md)
