---
phase: 5
title: "Curated release and promotion-trust handoff"
status: pending
effort: "2.0-2.5 implementation days"
dependsOn: [1, 2, 3, 4]
---

# Phase 5: Curated release and promotion-trust handoff

## Overview

Implement the three named data contracts, exact 11-asset release/current-pointer schema semantics, four-grain promotion-trust contract and authorized fixture schemas. Do not implement the publisher or publish the tracked fixture until phase 8.

## Requirements

- `retail-golden-v1` exactly implements the golden matrix.
- `CuratedReleaseManifest` represents one immutable release of exactly 11 required actual asset IDs sharing one generation identity; one separate pointer selects exactly one complete release.
- Reject missing/duplicate/extra/mixed-generation assets. JSON Schema `uniqueItems` is insufficient for duplicate IDs, so semantic validation is mandatory.
- Promotion/fulfillment/returns/DQ retain four independent grains and expected `insufficient-evidence`; no cross-grain attribution.
- Exact safe 89-row aggregate fixture shape, JCS/digests, C1/C2/M separation and owner-approved paths.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | three exact `contracts/data/*` issue files | retail, promotion, curated release contracts |
| Create | promotion evidence/manifest schemas under `learning/contracts/**` | tracked handoff validation |
| Create | `tests/contracts/test_retail_golden_contract.py` | exact anchor/mutations |
| Create | `tests/contracts/test_curated_release_manifest.py` | 11-set/generation/pointer/rollback mutations |
| Create | `tests/contracts/test_promotion_trust.py` | grains/decision/attribution negatives |
| Reserve, do not yet publish | exact authorized promotion fixture paths | phase 8 only |

## Curated release interface

`curated-release-manifest.schema.json` exposes closed `$defs` for:

- `CuratedReleaseManifestV1`: schema/contract version, immutable `releaseId`, `dataRunId`, `testedTreeSha`, input/profile/seed, lock/contract-set/engine snapshot IDs and exactly 11 asset entries.
- Each asset: one allow-listed `assetId`, logical dbt FQN, physical Iceberg FQN, schema hash, logical content hash, exact row count, immutable staged locator/version/snapshot and common generation fields.
- `CuratedReleaseCurrentPointerV1`: exactly one `currentReleaseId`, exact manifest SHA-256 and optional `previousReleaseId`; no embedded mutable asset list.

The semantic validator checks exact ID set/order, unique IDs, common release/data-run/input/lock/contract/engine identity and locator immutability. Pointer transition model: validate complete new manifest, atomically change one pointer, readers see old or new complete generation, prior generation retained, rollback points to a previously validated complete manifest. I5-01 tests this model with private documents only; I5-07 owns staging/switch/read-back/reconciliation and any current publisher change.

## Dependency map

- Depends on phase 4 schemas/canonicalization and phase 1 current anchors.
- Blocks issue #7’s real-fixture gate and phase 8 attestation.
- I5-07 consumes release schema; I5-02/#7 consumes promotion fixture read-only.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| 10/12 assets, duplicate ID, unknown ID | reject exact release set |
| one asset from another run/lock/contract/engine snapshot | reject mixed generation |
| pointer references absent/invalid/partial manifest | reject switch |
| rollback target absent or not previously complete | reject rollback |
| cross-grain join/reference or attribution phrase | promotion contract failure |
| decision changed from `insufficient-evidence` | `PROMOTION_HEADLINE_INSUFFICIENT`/decision failure |
| raw row, score/ADR, path/credential or recursive SHA field | fixture schema/publication failure |

## Interface checklist

- [ ] Exact curated ID list uses actual mart names and physical/logical FQNs.
- [ ] Manifest schema and current-pointer schema are distinct definitions.
- [ ] Publisher behavior is not implemented or invoked.
- [ ] Four promotion source entries carry grain/order/filter/numerator/denominator/weight/limitation.
- [ ] Fixture manifest excludes own digest, C2 and M; `testedTreeSha` is allowed.

## Tests Before

1. Add valid private documents and all release set/generation/pointer/rollback mutations.
2. Add four-grain records and cross-grain/causal/score/ADR/raw-row mutations.
3. Add exact aggregate field/scale/order/hash tests and authorized-path tests.
4. Require current golden matrix to validate; fail because the three contracts/readers are absent.

## Implementation

Create closed schemas/contracts and pure semantic validators. Map current anchors without changing source data/models. Generate fixture candidate only inside private evidence state; do not write tracked fixture paths in this phase.

## Refactor

Share stable ID/set/hash validators through the evidence core, but keep release state semantics and promotion grain semantics separate. Do not introduce a generic publisher abstraction.

## Tests After

- Run every missing/duplicate/extra/mixed/rollback and promotion mutation.
- Validate exact 11 asset identities and all 89 safe aggregate records from both clean projections.
- Scan candidate for forbidden fields/values and prove no other fixture path is touched.

## Regression Gate

- I5-01 has schema/current-pointer contract only.
- Expected promotion conclusion remains insufficient evidence.
- F-03/F-04/F-05 and SC-05/SC-12/SC-13 pass.
- Phase 8 publication remains blocked until clean C1 two-run evidence.

## Failure Evidence, Rollback and STOP

Retain the exact release/pointer/grain/fixture mutation and private candidate scan; do not publish
the candidate. Rollback discards only the private candidate and atomically restores the prior
coherent contract/reader set or conceptual previous complete pointer. STOP on a set other than
the exact 11 assets/current pointer, mixed generation, any result other than 89 safe aggregate
rows and `insufficient-evidence`, cross-grain/causal/raw-ID/secret/private-URL/score/ADR content,
publisher behavior or an unauthorized fixture path.

## Success criteria

- [ ] All three named contracts are exact and mutation-complete.
- [ ] 11-asset atomicity/rollback semantics are machine-verifiable.
- [ ] Promotion fixture candidate is safe, aggregate-only and grain-honest.
- [ ] No publisher, score, ADR, attribution or unauthorized fixture is created.
