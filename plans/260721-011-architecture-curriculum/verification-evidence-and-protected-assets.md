# Verification, Evidence, and Protected Assets

## Verification Boundary

The v4 author correction runs plan/static/provenance checks only. It does not run product tests,
render a product candidate, create runtime evidence, or grant implementation authority. The exact
future commands, repository-level RED rules, render parity, raw/sanitized evidence, cleanup, and
independent-review separation are normative in the
[Stage A v4 amendment](./stage-a-release-amendment.md).

Fresh independent plan validation must bind the exact pushed head and repeat CK 4.5.2 strict
validation/status, links/anchors/placeholders, exact counts, lineage, fresh remote equality,
protected/released bytes, S3/private-path/secret scans, and staged diff scope. Fresh readiness is a
later separate role and SHA. Neither may reuse the author report as its verdict.

## Released Contract Identities

The descriptor `learning/contracts/learning-contract-set-v1.json` at integration `5644f01b…`
closes exactly these 21 read-only identities:

```text
contracts/openapi/learning-platform-openapi-profile-v1.schema.json
contracts/openapi/learning-platform-problem-details-v1.schema.json
contracts/openapi/learning-platform-v1.yaml
learning/contracts/command-owner-activation-i5-03-v1.json
learning/contracts/command-owner-activation-v1.schema.json
learning/contracts/completion-reconciliation-v1.json
learning/contracts/completion-reconciliation-v1.schema.json
learning/contracts/fitness-result-v2.schema.json
learning/contracts/lab-v1.schema.json
learning/contracts/learning-contract-set-v1.schema.json
learning/contracts/learning-contract-version-registry-v1.json
learning/contracts/learning-contract-version-registry-v1.schema.json
learning/contracts/learning-evidence-v1.schema.json
learning/contracts/lesson-v1.schema.json
learning/contracts/operation-matrix-v1.json
learning/contracts/operation-matrix-v1.schema.json
learning/contracts/progress-v1.schema.json
learning/contracts/promotion-trust-learning-manifest-v1.schema.json
learning/labs/promotion-trust/lab-v1.json
learning/lessons/promotion-trust/lesson-v1.json
learning/manifests/promotion-trust-v1.json
```

Verification reads every path/blob/content-SHA entry from that released descriptor and compares it
individually at cook input, every implementation gate, final candidate, rollback, and fresh
reviewer checkout. Count or aggregate-hash equality cannot replace per-path equality.

## Protected Identities

Exactly 33 Issue #6 identities are protected. The first 25 are six source-closure paths, six view
sources, six SVGs, six text alternatives, and one render manifest:

```text
architecture/likec4/specification.c4
architecture/likec4/model/people-and-systems.c4
architecture/likec4/model/learning-platform.c4
architecture/likec4/model/data-platform.c4
architecture/likec4/model/local-deployment.c4
architecture/likec4/view-manifest.yaml
architecture/likec4/views/C4-L0.c4
architecture/likec4/views/C4-L1.c4
architecture/likec4/views/C4-L2-LOCAL.c4
architecture/likec4/views/C4-L3-RUNNER.c4
architecture/likec4/views/DEP-LOCAL.c4
architecture/likec4/views/DYN-JOURNEY.c4
architecture/rendered/C4-L0.svg
architecture/rendered/C4-L1.svg
architecture/rendered/C4-L2-LOCAL.svg
architecture/rendered/C4-L3-RUNNER.svg
architecture/rendered/DEP-LOCAL.svg
architecture/rendered/DYN-JOURNEY.svg
architecture/rendered/C4-L0.txt
architecture/rendered/C4-L1.txt
architecture/rendered/C4-L2-LOCAL.txt
architecture/rendered/C4-L3-RUNNER.txt
architecture/rendered/DEP-LOCAL.txt
architecture/rendered/DYN-JOURNEY.txt
architecture/rendered/render-manifest.json
```

The eight protected tool/lock/Make identities are:

| Path | Integration Git blob | Content SHA-256 |
|---|---|---|
| `requirements/architecture/package.json` | `d0cad6ce6eac10fec8594db2777c9c3a4b1e5987` | `5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d` |
| `requirements/architecture/package-lock.json` | `a19867e61168e12328c4b15bcc43afc44bd4599a` | `7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c` |
| `scripts/golden/architecture-render.mjs` | `a57cc02f3b8dfab9ae4d12c3328b612fd3957ce4` | `1af83f8481ee2b9d883706ad4cce45fe7b0c935a31fd1ae95b1570acdfc377e3` |
| `scripts/golden/architecture_check.py` | `e841857e4a96f005ee201385db2d64d942ab05f5` | `0aef6edcb58e3237d685608e184f97a8710a2c94665aa427e59910964b094682` |
| `scripts/golden/architecture_finalize.py` | `63f55480d8532b5b55b22479d053ac8220d4d000` | `bcecad086fb22496de715a9fe88c7de48b6c5d4a8d6b8636074d1cfde20e38fb` |
| `scripts/golden/architecture_pipeline.py` | `49e8191dacc6a5d0ceaab4eebdc9ff1d9d84e3cd` | `10b57a1c263684ae5bb47c83f8cbf5f08a06218c998dc75c708611d98021ebb0` |
| `scripts/golden/architecture_render.py` | `ef66a1e7ffdbeafc3aed0e9dec1968ec73c7d057` | `8932520bb10f561002951d5595da4fb643c6c4695e28841b393f547edc550f5a` |
| `mk/issue-5/i5-01.mk` | `ba8646eda060f7b609b2e7a054a3f552e48e2ee5` | `d38dfb497161aa20761de7fcef7ae0fb09015adfdee885331ee1fba9403f9028` |

The checker derives the integration blob/content-hash inventory for all 33, requires exact count
and per-item equality, and only then checks the supporting sorted aggregate. It never rewrites a
protected source/render/tool to accommodate an expansion.

## Render and Governance Proof

The five expansion views use one locked LikeC4 export/DOT/Graphviz semantic chain. Two isolated
runs retain projection, DOT, raw SVG, normalized visible SVG, structured text, and evidence-only
fitted HTML. The verifier checks visible node/relation/boundary/label/order parity and mutation
sensitivity at 1440/1024; a hidden freshness/hash-only change is a failure.

The governance proof binds protected `learning.adapters -> retail` and
`local.developer_host.adapters_instance -> local.developer_host.retail_instance` to reciprocal
`DYN-PUBLISH`, `DEP-AWS`, and `BR-GOVERNANCE-01` identities. Dynamic-only, deployment-only, both-
wrong, and missing-reciprocal mutations traverse the real repository checker and public route.

## Evidence Classes

The closed private index must contain, at minimum:

1. owner and exact lineage/tree/source/fixture/tool records;
2. metadata-stripped real mutation bytes;
3. contemporaneous bounded raw stdout and stderr bytes and hashes;
4. separate sanitized logs with source hashes and redaction summaries;
5. exact callable plus CLI/Make result records for every valid control and all 82 mutations;
6. process/RSS/output/file/deadline/TERM/KILL/reap measurements;
7. both render runs and projection/DOT/raw-SVG/normalized-SVG/text/fitted-HTML records;
8. cook self-inspection truth, S3/privacy result, owner markers, index/count/size/mode/type/link
   closure, ignored-inclusive cleanup, rollback, and 33/21 identity results.

Raw bytes are not deleted and replaced by a hash claim. Passing raw evidence remains mode 0600
and privacy-clean; unsafe raw evidence makes the run fail and remains privately quarantined. Cook
self-inspection has `independent=false` and truthful synthesis metadata. Independent review is a
future separate exact-head bundle.

## Author Correction Checks

| Check | Required result |
|---|---|
| Branch/input | Required branch; initial local/upstream/fresh-live `287dc08546f7013ca8c187b318e0a2f7cf832e55` |
| Direct base | Integration `5644f01b…` is ancestor; post-integration diff is plan-only |
| Plan validation | CK 4.5.2 `plan validate --strict --json` and `plan status --json` pass |
| Links/anchors | Every relative link and explicit anchor resolves |
| Placeholders | No unresolved implementation SHA is presented as authority |
| Closed counts | 50 paths, 16 commands, 22 families, 82 codes, 12 templates, 20 modules, 11 flows, eight bridges, five views |
| Identity inventories | 33 protected and 21 released contract paths are exact and unchanged |
| Scope | Only this plan directory changes; historical reports unchanged |
| S3 | No secret, credential, token, private path, or action-bearing cloud command |
| Handoff | Local/upstream/fetched/live output equality; only fresh independent plan validation next |

No author check is independent validation, readiness, cook authority, merge approval, or product
verification.
