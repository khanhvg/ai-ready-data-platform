---
phase: 1
title: "Immutable anchors and tests-first harness"
status: pending
effort: "1.5-2.0 implementation days"
dependsOn: []
---

<!-- Updated: Initial validation made mart content and summary canonicalization executable. -->

# Phase 1: Immutable anchors and tests-first harness

## Overview

Write read-only characterization and negative tests before any golden producer or contract exists. Freeze exact current semantics, not implementation accidents or historical-context claims. This phase changes test/evidence-core files only.

## Context

- [Golden contract matrix](./golden-contract-matrix.md)
- [Traceability F-01/F-10 and SC-07/SC-09](./requirements-and-risk-traceability.md)
- Discovery inventory at `discovery/repository-and-contract-inventory.md`
- Immutable source objects recorded in the discovery inventory

## Requirements

- Characterize all 18 exact CSV bytes/6,812 rows/checksum-list/manifest projection and observed anomalies separately from configured rates.
- Characterize 18 sources, 51 models by layer/materialization, 141 generic tests plus `assert_non_negative_shipment_lead_time.sql`, graph hash, all nine warning-configured IDs and 7-warn/2-pass distinction, and 179/7/0/186 result.
- Characterize 11 actual mart IDs/rows/content hashes, exact CSV value/dialect rules, normative JCS summary SHA `4b8a16…`, contextual legacy summary SHA `8ffb3e…`, and every Rill model/dimension/expression/weighting rule.
- Characterize six default plus two optional Airflow IDs/edges, ordered 11 curated assets, Iceberg/OpenMetadata identifiers, and historical issue #3 parsing with context retained.
- Every coarse-total-preserving semantic mutation fails a named assertion.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | `tests/golden/test-generator-characterization.py` | CSV, manifest and anomaly anchors |
| Create | `tests/golden/test-dbt-characterization.py` | graph/test/warning/build-capture anchors |
| Create | `tests/golden/test-mart-rill-characterization.py` | 11 marts and exact expressions |
| Create | `tests/golden/test-airflow-curated-characterization.py` | DAG, asset and identity inventory |
| Create | `tests/golden/test-historical-evidence-reader.py` | contextual evidence parser contract |
| Create | `tests/contracts/test-semantic-mutations.py` | itemized drift mutations |
| Preserve/read | current generator/dbt/Rill/Airflow/lake/governance/docs inputs | no product edits in this phase |

## Dependency map

- Input: immutable repository and discovery anchors.
- Blocks phases 2–8; every later schema/producer must satisfy these tests.
- The Airflow file remains read-only; this phase only determines whether its existing callable path seam is insufficient.

## Test scenario matrix

| Priority | Scenario | Oracle |
|---|---|---|
| Critical | Exact unmodified small/42 archive | every table/model/test/mart/expression/edge/identity anchor matches |
| Critical | Change one CSV byte while preserving row count | `GOLDEN_INPUT_MISMATCH` names file/hash |
| Critical | Let docs replace the only build result | `DBT_RAW_CAPTURE_MUTATED` |
| Critical | Change one Rill denominator or one DAG edge | named semantic mismatch despite unchanged totals |
| High | Treat PO orphan zero as missing warning config | fail configured-nine/observed-seven distinction |
| High | Rename actual mart to discovery shorthand | fail current model-ID inventory |
| High | Parse issue #3 177/9 as current small/42 | `HISTORICAL_EVIDENCE_MISCLASSIFIED` |

## Interface checklist

- [ ] Characterizer returns typed records, never writes current inputs.
- [ ] Every set has exact key/order plus duplicate detection.
- [ ] Raw byte hashing and typed semantic canonicalization are separate.
- [ ] Historical parser always returns evidence kind/date/profile/platform/source identity.
- [ ] Mutation reports identify the changed semantic field, expected and actual.

## Tests Before

1. Add table-driven expectations copied exactly from the golden matrix.
2. Run characterizers against an immutable archive: current anchors pass read-only.
3. Add tests expecting future `retail-golden-v1`, raw capture/projection and typed failure envelopes; they fail because those artifacts/readers do not exist.
4. Add private-copy mutations for every matrix row; verify coarse current checks would miss at least one mutation while the new assertion fails.
5. Record failing assertion IDs and immutable input SHA in phase evidence; do not edit expected values to match a changed run.

## Implementation

No product behavior. Implement only reusable read-only test helpers in evidence-core paths: deterministic inventory walkers, exact byte hashes, SQL/YAML semantic readers and historical-context parser fixtures constructed in private temp roots. Helpers reject duplicate identities and absolute paths.

## Refactor

Deduplicate test-only normalization helpers only after all anchor tests are green. Do not share a helper with the future producer until phase 4 reader contract prevents correlated producer/verifier bugs.

## Tests After

- Re-run all current anchors twice against separate `git archive` extracts.
- Run every semantic mutation and require the expected typed assertion.
- Verify working tree product/protected paths are unchanged.

## Regression Gate

- Exact golden matrix is fully exercised.
- No test relies only on total rows/models or nonzero reads.
- Source hash, test inventory and historical-context claims remain distinguishable.
- F-01, F-10, SC-07 and SC-09 have failing-before/pass-after evidence.

## Success criteria

- [ ] Current semantics are characterized with exact itemized diagnostics.
- [ ] Future contract/producer tests fail for expected missing behavior.
- [ ] Mutation suite detects drift hidden by aggregate totals.
- [ ] No product/config/data/protected file changed.
