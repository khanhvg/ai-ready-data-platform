# Planner Handoff

## Handoff status

`GO_TO_PLANNER`, with no cook authority.

The repository supports a bounded I5-01 plan. Three matters must be resolved before local cook:

1. explicit issue/master write authority for `tests/fixtures/learning/promotion-trust/**` (F-05);
2. an accepted complete hashed Python/dbt lock baseline (F-06); and
3. a real pinned architecture validation/render chain whose formats match the committed artifact contract (F-07).

All remaining Critical/High STOP conditions are fully recorded in `repository-and-contract-inventory.md` and `scenario-report.md` and must appear in plan acceptance/rollback evidence.

## Immutable inputs

| Input | Verified identity |
|---|---|
| Local/tracking/direct remote integration input | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` |
| Branch | `plan/issue-6-freeze-golden-baseline-contracts` |
| Master audit commit | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` (ancestor of input) |
| Master audit report blob at input | `d0d5f0bad31fe7a3ad701bbbe157e85c00a2c0d8` |
| Root release manifest blob / SHA-256 | `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` / `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| Issue state required through planning | `triaged`, retaining `risk:high`; no plan-state promotion |

Before planning, re-read issue #6 body/comments, issue #5 authority, issue #7 handoff, and the input versions of:

- `plans/260721-005-enterprise-learning-sandbox/phase-01-immutable-golden-baseline-and-architecture-contract.md:31-182`
- `plans/260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md:25-212`
- `plans/260721-005-enterprise-learning-sandbox/implementation-issue-graph.md:3-204`
- `plans/260721-005-enterprise-learning-sandbox/architecture-view-plan.md:9-160`
- `plans/260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md:3-184`

The master audit's `READY_WITH_GATES` verdict is binding; it is not permission to implement.

## Discovery artifacts

| Artifact | Planner use |
|---|---|
| `repository-and-contract-inventory.md` | Exact repository/source/protection inventory, deterministic characterization envelope, and F-01–F-12 owner/acceptance/rollback/STOP registry |
| `prediction-report.md` | Five-persona pre-mortem and cross-role conflicts/resolutions |
| `scenario-report.md` | Fifteen-iteration scenario analysis and SC-01–SC-15 execution gates |
| `scenario-results.tsv` | Machine-readable scenario log |
| `golden-evidence-decision-inputs.md` | D-01–D-13 decisions the plan must make explicitly |
| `planner-handoff.md` | Scope/authority/acceptance and issue #7 publication boundary |

## Verified characterization anchors

The planner may reuse these empirical facts, but should reference the full inventory rather than duplicate values inconsistently:

- `small/42`: 18 exact CSV files, 6,812 rows, ordered checksum-list SHA-256 `60ce82ce297acec1e3c047466f4b068baed5dc1875964832cb6cda3d4f91e9d6`, deterministic manifest SHA-256 `74ef96503fae5b0805c3261a5930f50420e8d168f2329f15408827ac29672f25`.
- dbt: 18 sources, 51 SQL models, six ephemeral/45 materialized, 11 marts, 141 tests plus one singular file, canonical graph SHA-256 `9cc9079097c4891e2939085729f23d0649af4ded52518966a6c0988991d533df`.
- `small/42` build: `PASS=179 WARN=7 ERROR=0 TOTAL=186`; nine tests are warning-configured, with the two purchase-order relationship tests passing because the observed PO orphan count is zero.
- Ordered 11-mart canonical summary SHA-256 `8ffb3ef70bdb460eebe28ec5fb1986ec728fcd711e658523efb93671df8418ea`.
- Rill: freeze exact source/dimension/measure expression text; label only actual ratio-of-sums/count-weighted expressions as weighted.
- Airflow: six-task default graph and optional two-task Iceberg append; narrow explicit workspace path forwarding only.
- Curated/OpenMetadata: exact 11-asset registry, physical prefix `retail_iceberg.default.retail`, logical prefix `retail_duckdb.retail.main_marts`, historical 11/45/130 only in its dated/profile/tool context.
- Clean no-cache run: 155 seconds per run on the discovery host; two runs matched deterministic projections. Current resolver drifted to dbt-core 1.12.0/dbt-adapters 1.24.5 from historical 1.11.12/1.24.4 context.
- Make: exactly 54 master future targets, 15 input targets, and seven I5-01-owned future targets.
- Architecture: exactly six pre-P5 view IDs — `C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, and `DYN-JOURNEY`; clean host has no usable Java/Structurizr; the specified CLI/SVG boundary requires correction.

## Required ownership map

| Surface | I5-01 authority | Explicit non-owner / later owner |
|---|---|---|
| Generator/dbt/Rill/Airflow/curated/metadata baseline | Characterize and assert; only narrow Airflow workspace path forwarding where phase authority permits | No behavior “fixes” or new analytics |
| Root Makefile | One include/help integration seam | Later recipes remain in their own fragments; root changes after I5-01 require serialized shared-core lease |
| `mk/issue-5/i5-01.mk` | Seven I5-01 targets only | I5-02+ fragments forbidden |
| Evidence/data/learning base contracts | I5-01 base schemas, canonicalization, registry, local integrity/provenance | I5-03 learning API/product contracts; I5-14 hosted signing/authenticity |
| Golden workspace and local harness | Scoped clean-run determinism and path/output safety | I5-04 generalized privileged runner containment/race/security |
| Curated release | `CuratedReleaseManifest` schema and atomic-pointer contract only | I5-07 publisher staging/switch/read-back/reconciliation implementation |
| Promotion trust | Grain-honest query/assertion contract and, after authority, sanitized tracked aggregate fixture | I5-02 scorecard/ADR; I5-07 any later additive attribution product |
| Architecture | Workspace/manifest skeleton and the six sources/renders/text alternatives/fitness checks | I5-06 additions-only serialized lease; `DYN-PUBLISH` is later |
| Terraform/cloud/product configuration | None | Later milestones only |

The planner must not infer fixture write authority from a desired handoff. It must obtain/cite an explicit amendment for `tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}` or plan the fixture as blocked and preserve issue #7's no-score state.

## Mandatory plan decisions

The plan must make D-01 through D-13 explicit. At minimum, acceptance criteria must name:

1. exact interpreter/dbt version set, transitive lock/hashes, install command, empty-cache behavior, and lock fingerprint;
2. raw evidence lifecycle and deterministic projection fields/allowed-drift pointers;
3. JSON Schema 2020-12 and RFC 8785/I-JSON canonicalization vectors, including duplicate-name and negative-zero handling;
4. schema/canonicalization/version registry and v1 backward-read/migration/rollback tests;
5. distinct `testedTreeSha`, external/child `attestationCommitSha`, and later external `mergeOrTagSha` without recursive self-hashing;
6. private run-root, path/symlink/TOCTOU/concurrency/atomic-write, bounded output/time, and scoped cleanup behavior;
7. exact generator/anomaly/dbt/warning/lineage/mart/Rill/Airflow/curated/Iceberg/OpenMetadata/historical projections and mutation cases;
8. exactly-11, common-generation `CuratedReleaseManifest` schema and one-pointer rollback semantics without implementing I5-07;
9. grain declarations and prohibited attribution for `promotion-trust-v1`;
10. actual architecture tool/digest/bootstrap/render/text/freshness contract for all six views;
11. 54-command owner registry uniqueness, seven-target I5-01 fragment, current 15-target non-regression, and root include/help rollback;
12. protected/unrelated path preservation and publication scans;
13. issue #7 unscored pre-merge versus scored post-merge gates.

## Local-cook STOP ledger

Planning may proceed while these are modeled, but cook must not start if any applies:

- input SHA, branch, tracking ref, issue authority, or master-audit ancestry drifts;
- fixture path authority remains absent/ambiguous;
- dependency baseline or complete hashed lock is unresolved;
- architecture renderer/output contract is unsupported, unpinned, or can skip;
- any F-01–F-12 or SC-01–SC-15 owner/acceptance/rollback/dependency is missing from the plan;
- evidence canonicalization drops unspecified fields or cannot detect semantic mutations;
- cleanup/path logic can reach outside one owned run root or follow symlinks;
- local checksums are represented as signatures/authenticity;
- `CuratedReleaseManifest` permits partial/mixed/extra generations or I5-01 starts implementing the publisher;
- promotion assertions imply campaign causality/attribution;
- issue #6 defines another owner's Make target, architecture row, runner behavior, score, ADR, publisher, hosted signing, Terraform, or cloud action;
- root `release-manifest.json`, absent `docs/code-standards.md`, tracked placeholders, ignored fixtures, or unrelated files change.

## Issue #7 real-fixture handoff contract

### Safe to publish after path authority

- sanitized aggregate query/assertion results at each declared grain;
- contract/schema/canonicalization/version IDs and hashes;
- exact tested tree SHA, tool/lock identity, producer command, artifact hashes, and redaction statement;
- no secrets, PII-like raw rows, home/temp paths, private URLs, runtime/volume identifiers, score, ADR, or attribution claim.

### Must wait for merge

- the externally observed merge/tag SHA;
- framework scorecard execution and any “real fixture” pass claim tied to merged provenance;
- ADR-005 decision/publication;
- any comparison that treats a provisional/attestation commit as the merged producer identity.

Issue #7 may build unscored preview/common assertions before merge. If fixture authority is not granted, the safe outcome is no tracked fixture and a continuing score block—not publication in an invented path.

## Preservation baseline for later validation

Before and after implementation, validation must prove:

- `release-manifest.json` retains blob `b27d231c5ee6d48fd7932b06807ef6a9a2220e21` unless separately and explicitly authorized;
- `docs/code-standards.md` remains absent and is never created/deleted/overwritten;
- `data/raw/.gitkeep` and other tracked placeholders remain;
- no user-owned ignored fixture, cache, volume, generated directory, or unrelated file is staged or deleted;
- no tracked symlink is introduced in evidence/workspace/publication paths;
- changed paths match the final I5-01 authority allow-list exactly.

## Planner entry condition

The planner may start from this handoff because the immutable input is verified, the repository envelope is empirical, the 15 scenario iterations are saturated, and all Critical/High concerns have owners and STOP evidence. It must run a fresh `$ck:plan` phase and subsequent validation/red-team/audit under the issue's workflow; this discovery has intentionally run none of those phases.
