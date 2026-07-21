# Issue #7 fixture and merge handoff

## Exact authority

The binding [issue #6 owner clarification](https://github.com/khanhvg/ai-ready-data-platform/issues/6#issuecomment-5027528463) authorizes only:

```text
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
tests/fixtures/learning/promotion-trust/invalid/**
```

All other `tests/fixtures/**` paths are forbidden. Issue #7 consumes the authorized files read-only only after issue #6 merges. This authority resolves discovery gate F-05; it does not authorize raw rows, framework score/ADR, campaign attribution, portal code or any issue #7 write.

## Fixture identity and producer

The sole producer command is exactly:

```text
make golden-clean PROFILE=small SEED=42
```

It produces a private raw bundle and deterministic projection first. Only the explicit attestation workflow may copy the safe projection into tracked `evidence-v1.json`. A dirty tree, wrong input/lock/tool hash, failed assertion, single run, reused venv/cache/data, unauthorized field or projection mismatch blocks fixture publication.

`evidence-v1.json` top-level contract:

| Field | Exact rule |
|---|---|
| `schemaVersion` | `promotion-trust-evidence-v1` |
| `contractId` | `promotion-trust-v1` |
| `fixtureId` | `promotion-trust-small-42-v1` |
| `fixtureKind` | `tracked-real` |
| `dataClassification` | `sanitized-synthetic-aggregate` |
| `profile`, `seed` | `small`, `42` |
| `inputWindow` | generated input domain `2025-07-01` through `2026-06-30`, explicitly not a mart predicate |
| `sources` | exactly four unique entries in the order below |
| `assertions`, `decision`, `limitations`, `integrity` | required, closed schemas |

The file contains **all 89 aggregate rows**, never a raw event/customer/order row:

| Source | Independent grain and order | Rows | Source-mart SHA-256 anchor |
|---|---|---:|---|
| `mart_promotion_effectiveness` | `(promo_name, channel)` | 7 | `5b6bc790aaeed2891608b8c1fceba0d4904fd49b9865c160658d6f5249e0bfc0` |
| `mart_fulfillment_performance` | `(carrier, region_name)` | 25 | `8c0114d1ab48b4fb42009aba3df192988bf917004461d0c0dd0155d0283dce60` |
| `mart_returns_analysis` | `(reason, category_name, region_name)` | 47 | `2aa068d1c676cc9234f9a6703f0d2490a10b007ae673b758fa45f614963e7db4` |
| `mart_data_quality` | `(scenario)` | 10 | `cd3bb0424396aad0d902e9dc594072a5506c3b6484be3f3f2209b7cbbcdae5fa` |

Each source entry declares grain, stable ordering and null placement, full-input/time scope, filter, numerator, denominator, aggregation/weighting rule, limitation, row count, source-mart content hash and normalized-records hash. Rows use these allow-lists:

- Promotion: `promo_name`, `channel`, `order_count`, `gross_revenue`, `total_discount_amount`, `net_revenue`, `avg_order_value`, `discount_pct_of_gross`.
- Fulfillment: `carrier`, `region_name`, `shipment_count`, `on_time_count`, `on_time_pct`, `avg_lead_time_days`, `in_transit_count`.
- Returns: `reason`, `category_name`, `region_name`, `return_count`, `total_refund_amount`, `avg_refund_amount`.
- Data quality: `scenario`, `row_count`.

Counts are JSON integers. Currency/AOV/refund values are fixed-scale two-decimal strings; percentages and lead time are fixed-scale one-decimal strings. `-0.00`/`-0.0` is invalid. `null` is permitted only for a source field whose declared denominator is absent. Names here are synthetic aggregate labels but still pass the credential/path/private-URL scanner.

The ten data-quality rows are the exact `mart_data_quality` aggregate, not the generator anomaly projection: duplicate customers 1, duplicate orders 1, null email 7, null promotion ID 879, invalid status 9, late orders 20, orphan order-item product 6, in-transit shipments 70, orphan web event/session 1, and dangling PO-item product 0. Generator-observed injected anomalies remain separately recorded as null promotion ID 1 and invalid status 10; substituting those values into the mart source is `PROMOTION_SOURCE_VALUE_MISMATCH`.

## Promotion trust contract and expected result

`contracts/data/promotion-trust-v1.yaml` declares four independent grains. There is no shared join key and no legal cross-source attribution. Stable assertions include:

```text
PTV1-GRAIN-PROMOTION
PTV1-GRAIN-FULFILLMENT
PTV1-GRAIN-RETURNS
PTV1-GRAIN-DATA-QUALITY
PTV1-HEADLINE-SUFFICIENT
PTV1-NO-CROSS-GRAIN-JOIN
PTV1-NO-ATTRIBUTION
PTV1-DECISION-INSUFFICIENT-EVIDENCE
```

`PTV1-HEADLINE-SUFFICIENT` is an expected controlled failure with code `PROMOTION_HEADLINE_INSUFFICIENT`. The fixture decision is exactly `insufficient-evidence`, reason `no-common-grain`. “Promotion caused fulfillment/returns/data-quality outcome,” campaign ranking, inferred matching, or any equivalent attribution language fails schema/semantic checks.

Mutation tests independently introduce a cross-grain reference/join, campaign/carrier/return/DQ attribution, altered grain/order, missing/extra source, duplicate aggregate row, changed value/hash/count, decision other than `insufficient-evidence`, raw row/identifier, score/ADR field and forbidden provenance identity. Each fails with a stable code and no tracked output.

## Tracked fixture manifest

`manifest.json` uses `promotion-trust-fixture-manifest-v1` and contains:

- fixture/schema/contract IDs and producer command;
- `testedTreeSha` for the clean producer/contracts/readers commit;
- profile/seed and generated input window;
- Python lock SHA-256 and architecture/tool IDs where relevant;
- two-clean-run comparison status and evidence-relative locators;
- byte length and SHA-256 of `evidence-v1.json`, `contracts/data/retail-golden-v1.json`, `contracts/data/promotion-trust-v1.yaml`, and applicable learning schemas/registry entries;
- canonicalization `rfc8785-jcs-v1`, digest algorithm `sha-256`;
- only repository-relative retention locators;
- `redactionClass: sanitized-synthetic-aggregate`;
- explicit statements that publisher authenticity and merged identity are externally attested.

The canonical fixture payload excludes its own digest. `manifest.json` must not list its own byte digest or containing commit. Neither tracked file contains `attestationCommitSha` or `mergeOrTagSha`; those are necessarily external.

## Authorized negative fixtures

Track only raw-parser/canonicalization cases that cannot reliably be reconstructed after ordinary JSON parsing:

```text
tests/fixtures/learning/promotion-trust/invalid/canonicalization/duplicate-name.json
tests/fixtures/learning/promotion-trust/invalid/canonicalization/nan.json
tests/fixtures/learning/promotion-trust/invalid/canonicalization/positive-infinity.json
tests/fixtures/learning/promotion-trust/invalid/canonicalization/negative-infinity.json
tests/fixtures/learning/promotion-trust/invalid/canonicalization/lone-surrogate.json
tests/fixtures/learning/promotion-trust/invalid/canonicalization/negative-zero-decimal.json
```

All semantic, security, path, score/ADR and attribution mutations are generated inside a private run root. No negative tracked file may contain raw PII-like rows, credentials, private URLs, absolute paths or causal claims that could be mistaken for evidence.

## C1 / C2 / M non-recursive attestation

1. **C1 (`testedTreeSha`)**: commit producer, locks, contracts, readers and tests; require clean tree; run two independent golden archives and compare projections.
2. Generate the authorized tracked fixture only from C1’s validated projection. Verify all listed hashes and protected paths.
3. **C2 (`attestationCommitSha`)**: child commit adds only the authorized fixture/attestation bytes. Record C2 and exact path digests externally in issue #6/PR metadata, never inside tracked files.
4. **M (`mergeOrTagSha`)**: issue #7 waits for the remotely observed merge/tag identity, reads the exact four paths from M, verifies their blob/digest identity against the external issue #6 attestation, then records M in its own external score evidence.

The four issue #7 handoff digests are:

```text
contracts/data/retail-golden-v1.json
contracts/data/promotion-trust-v1.yaml
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
```

For a squash merge, accept the GitHub PR merge record plus exact merged-path blob equality; do not falsely require C2 to be an ancestor when the merge strategy discarded commit identity. The tested-tree relationship and all artifact hashes must still verify.

## Issue #7 merge gate and invalidation

Issue #7 may move from synthetic preview to scoreable execution only after:

- M is remotely observed and the four path digests match the external attestation;
- fixture/manifest schemas, JCS payload hashes and tested-tree record pass;
- every candidate is rerun from clean state against the identical merged bytes;
- synthetic preview state is cleared rather than relabelled as real evidence.

Any fixture, contract, schema, version-registry entry, tested tree, attestation commit, merge identity or one of the four path digests changing invalidates all prior candidate samples, scores and ADR input. Issue #7 must clear fixture-bound browser state and rerun all surviving candidates. Issue #6 never publishes or endorses a framework score, winner or ADR.

## Forbidden tracked content

Raw customer/order rows or identifiers, credentials/tokens/keys, private URLs, usernames, absolute host/workspace paths, Docker/volume/runtime IDs, framework scores, ADR decisions, causal campaign attribution, recursive manifest hashes and self-containing commit claims are all hard failures.
