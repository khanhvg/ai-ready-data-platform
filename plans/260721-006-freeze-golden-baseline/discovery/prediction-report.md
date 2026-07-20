# Prediction Report

## Proposal analyzed

I5-01 will freeze deterministic local data/evidence/architecture contracts at immutable input `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`, publish a sanitized real promotion-trust fixture for issue #7, and add only the master-authorized root Make include/help seam plus I5-01's fragment. It will not implement later product, runner, atomic lake publisher, hosted-signing, Terraform, or cloud concerns.

Method: `$ck:predict` five-persona pre-mortem after repository and issue/master review. All severity-bearing findings map to the complete owner/evidence/mitigation/dependency/STOP records F-01 through F-12 in `repository-and-contract-inventory.md`.

## Persona 1 — System Architect

1. The architecture source/manifest skeleton is viable, but the required renderer is not: the described Structurizr CLI boundary does not directly produce SVG, and the clean host lacks Java/Structurizr. Without D-09, architecture freshness becomes ceremonial rather than executable (F-07).
2. The six pre-P5 view IDs are appropriately bounded. The greatest ownership risk is I5-01 accidentally adding `DYN-PUBLISH` or letting I5-06 later rewrite the original six instead of taking a serialized additions-only lease (F-08).
3. `CuratedReleaseManifest` must be a generation-coherence contract, not merely a JSON list. Exactly 11 immutable staged assets and one atomic current pointer are the minimum architectural invariant (F-03).
4. The root include-fragment design scales to 54 commands only if target ownership is machine-checked and current recipes remain untouched. Hand-maintained help text alone will drift (F-08).
5. The fixture-path omission is an authority defect, not permission to infer a convenient write lease. Planning can continue, but cook cannot (F-05).

Recommendation: resolve tool/output formats and path authority in the plan's first gate; make manifest/registry fitness executable and mutation-tested.

## Persona 2 — Security Engineer

1. The highest immediate risk is workspace escape through absolute paths, `..`, symlinks, concurrent swaps, or broad cleanup. A golden harness that hashes after a check-then-use race can certify attacker-controlled bytes (F-02).
2. Dynamic installers, ambient environment inheritance, and a read-write project-root Airflow mount can inject tools, paths, credentials, or modules into evidence. Issue #6 should harden only its clean harness/narrow path-forwarding seam and hand generalized containment to I5-04 (F-12).
3. SHA-256 offers local corruption/tamper detection, not publisher identity. Any “signed” or “authentic” wording before I5-14 is a security overclaim (F-09).
4. Evidence and tracked fixtures can leak credentials, absolute home paths, raw IDs, container/volume names, or private URLs. A schema plus high-confidence credential/PII-like field scan must block publication (F-04, F-11, F-12).
5. Atomic write must cover both bytes and authority: private temp creation, no-follow resolution, fsync/rename policy where supported, and refusal to overwrite a foreign/pre-existing destination. Pointer rollback must never delete the prior generation (F-02, F-03).

Recommendation: treat the golden workspace as an untrusted-input boundary and make adversarial path/tamper/corruption cases first-class acceptance evidence.

## Persona 3 — Product Owner

1. The promotion-trust lesson cannot honestly claim campaign influence on fulfillment, returns, or data quality from the existing marts. Such a claim would teach a false causal model (F-04).
2. A real fixture is valuable only when its provenance is understandable: exact tested tree, exact contract/artifact hashes, and a later externally observed merge identity. A provisional fixture score creates false confidence (F-11).
3. The 18-table/51-model/11-mart envelope is sufficient for a useful baseline, but `small/42` and historical `demo-large` observations must be presented as different contexts, not as conflicting product results (F-10).
4. “Golden” must mean reproducible contract behavior, not frozen incidental timings, temp paths, or Parquet container metadata. Conversely, dropping too many fields hides real semantic regression (F-01).
5. Issue #6 should not solve future lake publication, portal scoring, or campaign attribution now. Those are deliberate later milestones with different owners.

Recommendation: define grain-honest learner-facing assertions and keep issue #7 unscored until the authorized fixture is merged and independently identified.

## Persona 4 — Site Reliability / Operations Engineer

1. Two empty-cache runs took 155 seconds each, but network bootstrap dominates and no command currently has a hard timeout. Without per-step budgets and child termination, “bounded” is aspirational (F-06, F-12).
2. A `.venv/bin/python3` sentinel does not prove lock conformance. A stale environment or fresh transitive resolution can yield a different dbt core/adapter set while Make reports success (F-06).
3. Raw `run_results.json` is lifecycle-sensitive because dbt docs can replace it. Capture ordering and immutable evidence destinations are necessary for incident diagnosis and deterministic comparison (F-01).
4. Current Iceberg publication drops and recreates sequentially. The schema must prepare I5-07 for stage/validate/switch/rollback rather than normalize partial availability (F-03).
5. Portable local execution cannot assume GNU `flock`, GNU checksum tools, Java, Structurizr, dbt, Rill, Docker volumes, or credentials. Missing required tools must fail with a useful message; optional profile absence must be explicit (F-07, F-12).

Recommendation: establish lock fingerprint, step budgets, raw/projection retention, atomic pointer semantics, and portable primitives before cook.

## Persona 5 — Implementing Developer

1. The repository already has output seams for the generator, loader/export path, and Airflow callables, so focused implementation is possible. The plan must name exactly which existing seams are read-only and which narrow callables may change.
2. A single evidence library can centralize schema validation, canonicalization, hashing, atomic file creation, and registry lookup, but it must not become an unbounded framework or absorb I5-04 runner responsibilities (F-01, F-02, F-12).
3. A machine-readable command/view/schema registry is preferable to duplicating IDs in Make, tests, and docs. Tests should fail stale/duplicate/orphan records (F-08).
4. The dbt oracle needs two inventories: nine tests configured as warnings and the `small/42` observed result of seven warnings/two passes. Encoding only one count will produce brittle tests (F-10).
5. The fixture can be generated safely from canonical aggregate queries, but only after exact path authority exists. The implementation must never fabricate a merge SHA or score (F-05, F-11).

Recommendation: keep modules small and contract-driven, capture build artifacts before docs, and put every owner/authority boundary into executable negative tests.

## Consensus analysis

### Agreements

- All personas agree that the work is technically feasible and belongs in planning, but it is not cook-ready.
- F-05 fixture-path authority, F-06 dependency locking, and F-07 architecture renderer are unanimous pre-cook gates.
- Raw evidence and deterministic projection must be separate (F-01).
- Atomic release/schema semantics and grain-honest promotion assertions are core correctness, not optional polish (F-03, F-04).
- Local checksum integrity must not be presented as hosted signing/authorship (F-09).
- Root Make integration and the six-view lease must remain disjoint from later issue ownership (F-08).

### Tensions resolved for the planner

| Tension | Resolution input |
|---|---|
| Freeze historical dbt versions or accept today's resolver output | Prefer historical known-good 1.11.12-compatible lock unless an explicit compatibility experiment accepts 1.12.0; never let the resolver decide implicitly. |
| Hash everything or remove volatility broadly | Retain everything raw; hash a narrow, versioned semantic projection with explicit allowed-drift pointers and mutation tests. |
| Produce SVG as written or use the available CLI | Do not fake SVG. Pin a supported two-stage renderer or explicitly revise the artifact format contract before cook. |
| Harden Airflow completely in I5-01 or ignore environment threats | I5-01 owns only its clean harness and narrow workspace forwarding; record and test the handoff to I5-04 for generalized runner security. |
| Publish issue #7 fixture now or avoid it entirely | Obtain explicit exact-path authority, publish sanitized aggregate fixture, then let #7 score only after an external merged-SHA handoff. |

## Risk matrix

| Probability / impact | Low impact | Medium impact | High impact |
|---|---|---|---|
| High probability | — | Historical/current evidence confusion (F-10) | Dependency drift (F-06); raw/projection oracle error (F-01) |
| Medium probability | — | Make/help registry drift (F-08) | Path/TOCTOU tampering (F-02); partial release schema (F-03); attribution overclaim (F-04); renderer mismatch (F-07) |
| Low probability | — | — | Credential/private-path leak (F-12); hostile replacement presented as authentic (F-09) |

## Recommended pre-plan gates

1. Amend/cite explicit I5-01 authority for `tests/fixtures/learning/promotion-trust/**`, or retain an explicit cook STOP and issue #7 scoring block.
2. Select the exact Python/dbt baseline and complete hashed lock strategy.
3. Select a real deterministic architecture validation/render chain and artifact formats.
4. Define evidence schema/canonicalization/version/provenance layers before listing implementation files.
5. Model workspace/path/atomic-write/runtime/redaction negative tests as requirements, not follow-up hardening.
6. Freeze exact data/dbt/Rill/Airflow/curated/metadata projections and contextual historical parsing.
7. Preserve issue boundaries: schema in I5-01, atomic publisher/reconciliation in I5-07, generalized runner security in I5-04, scoring/ADR in I5-02, hosted signing in I5-14.

## Prediction verdict

**CAUTION — proceed to planning only.** The proposal is viable within I5-01, and no fundamental architecture defect requires abandoning it. Local cook remains stopped until authority, lock, and rendering gates are resolved and all F-01 through F-12 acceptance/rollback conditions are represented in the plan.
