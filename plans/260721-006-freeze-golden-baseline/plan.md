---
title: "I5-01 — Freeze golden baseline and shared architecture contracts"
description: "Deep/TDD implementation plan for the reproducible small/42 baseline, versioned data/evidence/release contracts, secure private run envelope, six deterministic local architecture views, and the read-only I5-02 fixture handoff."
status: pending
priority: P1
issue: 6
branch: "plan/issue-6-freeze-golden-baseline-contracts"
tags: ["issue-5", "i5-01", "golden-baseline", "contracts", "architecture", "tdd", "security-s3"]
blockedBy: []
blocks: []
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
planningMode: "deep-tdd"
inputSha: "7a65da010abf0e3730731b6d744b532156c48fdc"
integrationSha: "f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c"
masterReadinessSha: "e440c5855732d5d8f5d634e3cc1359c010cc5ed3"
---

# I5-01 — Freeze golden baseline and shared architecture contracts

## Outcome

Implementers will freeze the existing `small`/`42` retail pipeline as a reproducible, hashed baseline; publish versioned data, evidence, promotion-trust, and curated-release schema contracts; create the six minimum local architecture views from validated source; and produce the only issue-owned tracked fixture that issue #7 may consume after merge. The implementation must preserve current business behavior and protected files.

This directory is a planning artifact only. Every command and path described as future work is explicitly **planned and absent at the immutable input unless the current repository already contains it**. This plan does not validate itself and does not authorize implementation, `$ck:cook`, an independent validation/red-team/readiness audit, dependency-lock publication, fixture generation, cloud activity, a PR, or a merge.

## Binding decisions

1. **Dependency baseline:** CPython `3.12.x` only on the required darwin-arm64 lane (planning proof patch `3.12.3`), with `pip==26.1.1`, `dbt-core==1.11.12`, `dbt-adapters==1.24.4`, `dbt-duckdb==1.10.1`, `duckdb==1.5.4`, and `faker==40.28.1`. The wheel-only fully hashed lock is compiled by `pip-tools==7.6.0`; the exact proposed-path candidate has 55 distributions and SHA-256 `6552bc4c96df53656a83f5c4d7e01317bc29a094fa7e3ac948d35f8d1b997d6a`. Two independent clean full installs/runs produced the same normalized environment SHA-256 `e0b9ba79a6889cc0ab8f5d3b2d30ea3c9b37900f830094cd17affa389a9354bd` and the required data/dbt outputs. `dbt-core` 1.12.0 is intentionally not selected because it adds a new parser/MetricFlow dependency surface and would silently redefine the golden baseline.
2. **Architecture chain:** pin Java-free LikeC4 `1.59.1` for `.c4` semantic validation/computed model output and `@hpcc-js/wasm-graphviz` `1.22.2` (embedded Graphviz `15.0.0`) for SVG, behind a project fitness/text/normalization wrapper. The renderer must fail on missing tools, malformed references, stale output, or non-deterministic bytes; it must not claim a Structurizr CLI export.
3. **Fixture handoff:** the owner clarification authorizes only `tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}` and issue-owned negative cases under `tests/fixtures/learning/promotion-trust/invalid/**`. The fixture contains four separately grained, sanitized aggregate projections and the expected decision `insufficient-evidence`; all other fixtures and every score/ADR/attribution are forbidden.

Details and probe evidence are normative in [dependency-lock-decision.md](./dependency-lock-decision.md), [architecture-toolchain-decision.md](./architecture-toolchain-decision.md), and [issue-7-fixture-and-merge-handoff.md](./issue-7-fixture-and-merge-handoff.md).

## Authority and invariants

- Exact implementation input: `7a65da010abf0e3730731b6d744b532156c48fdc`; its ancestry contains integration `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` and master readiness/audit `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`.
- Writable product scope is limited to `scripts/golden/**`; the three named `contracts/data/**` files; base `learning/contracts/**`; evidence core; six architecture source/render/text/manifest paths; dependency locks; root Make include/help plus `mk/issue-5/i5-01.mk`; the exact fixture paths above; and only a proven Airflow workspace-path forwarding seam.
- Root `release-manifest.json`, `docs/code-standards.md` (currently absent), discovery history, unrelated tracked/ignored/generated paths, later issue fragments, portal/runner/Terraform/cloud paths, and every other fixture are protected.
- I5-01 defines the `CuratedReleaseManifest` schema and current-pointer contract. I5-07 implements staging, switch, read-back, reconciliation, and the publisher. I5-14 owns trusted signing. I5-02 owns framework score/ADR. I5-04 owns generalized privileged-runner containment. I5-06 receives only a serialized additions-only architecture lease.
- The implementation begins only from a clean tree at the approved SHA. Any unauthorized path need, unresolved tool/license incompatibility, baseline drift, inability to obtain complete hashes, or protected-path mutation is a STOP, not an invitation to broaden scope.

## Phases

| Phase | Name | Status | Primary gate |
|---:|---|---|---|
| 1 | [Immutable anchors and tests-first harness](./phase-01-immutable-anchors-and-tests-first-harness.md) | Pending | Characterization tests fail before production code |
| 2 | [Dependency baseline and hashed lock](./phase-02-dependency-baseline-and-hashed-lock.md) | Pending | Two empty-cache installs resolve exact pins/hashes |
| 3 | [Private workspace and provenance envelope](./phase-03-private-workspace-and-provenance-envelope.md) | Pending | Path/TOCTOU/process/redaction negatives pass |
| 4 | [Data and evidence contract schemas](./phase-04-data-and-evidence-contract-schemas.md) | Pending | Schemas, JCS vectors, mutation readers pass |
| 5 | [Curated release and promotion-trust handoff](./phase-05-curated-release-and-promotion-trust-handoff.md) | Pending | 11-asset and four-grain mutation barriers pass |
| 6 | [Architecture source validation and deterministic render](./phase-06-architecture-source-validation-and-deterministic-render.md) | Pending | Six sources/render/text alternatives are fresh and reproducible |
| 7 | [Make registry and Airflow seam](./phase-07-make-registry-and-airflow-seam.md) | Pending | Current 15 targets preserved; 54-target ownership registry exact |
| 8 | [Two-run evidence, rollback and merge handoff](./phase-08-two-run-evidence-rollback-and-merge-handoff.md) | Pending | Two clean 300-second-bounded runs agree; C1/C2/M handoff is externalized |

## Phase dependency graph

`1 → 2 → 3 → 4 → 5`; phases 5 and 6 may proceed in parallel only after phases 1–4 establish the shared evidence rules; `5 + 6 → 7 → 8`. Phase 8 is the only fixture publication phase. No tracked fixture may be generated from an uncommitted or dirty tree.

External dependency: issue #7 remains read-only and unscored until issue #6 is remotely merged and the four required path digests are externally attested. This is not a plan-directory dependency because no local issue #7 implementation artifact is modified here.

## Planned public command contract

The only issue-owned future targets are:

```text
make help
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make migration-contracts-check
make architecture-check
make architecture-render
```

Each will be registered in the machine-readable 54-command owner registry, non-interactive, and fail non-zero with a typed code, bounded remediation, and schema-valid `FitnessResult` under `.artifacts/evidence/<fitness-id>/<run-id>/`. Missing required tools or evidence are failures, never skips. Lock/bootstrap, two-run comparison, fixture verification, registry verification, protected-path scanning, and rollback rehearsal are owned steps inside these seven targets—not new unregistered root targets.

The exact user-mandated paths are exercised by `make golden-clean PROFILE=small SEED=42`, `make data-contracts-check`, `make evidence-contracts-check`, `make architecture-check`, and the lock/bootstrap checks embedded in `golden-clean`. `architecture-render` creates deterministic derived bytes; `migration-contracts-check` proves version-reader/rollback compatibility. See [implementation-handoff.md](./implementation-handoff.md) for command-to-evidence mapping and budgets.

## Acceptance criteria

- All F-01…F-12 and SC-01…SC-15 rows have an owner, path, test, evidence, rollback, dependency, and explicit STOP condition in [requirements-and-risk-traceability.md](./requirements-and-risk-traceability.md).
- Tests are written first for every current anchor, schema mutation, workspace attack, Make/ownership invariant, view freshness rule, and merge handoff.
- Raw run bundle, deterministic semantic projection, and provenance/integrity envelope remain separate; only the five declared volatile pointers may drift.
- Two independent runs start with no prior venv/data/cache, complete within 300 seconds each and 600 seconds together on the discovery host, terminate descendants on timeout, retain bounded failure evidence, and produce exact projection/content hashes.
- The 18 CSV/6,812-row generator result, 18 sources, 51 dbt models, 141 generic plus one singular test, 179 pass/7 observed warn/0 error/186 total result, 11 marts, Rill semantics, six-plus-two Airflow graph, 11 curated assets, and data/catalog identities are all characterized without recasting historical context as a current claim.
- Curated release schemas reject incomplete, duplicate, extra, and mixed-generation assets and define one immutable 11-asset release plus one atomic current pointer and rollback semantics without changing the publisher.
- Promotion trust keeps four independent grains and rejects cross-grain joins or attribution language; the only supported conclusion is `insufficient-evidence`.
- Six view IDs only—`C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, `DYN-JOURNEY`—validate, render deterministically, expose semantic text alternatives, and pass audience/concern/legend/freshness checks.
- Changed-path, protected-hash, credential/private-path, symlink/TOCTOU, registry, rollback, and issue #7 merged-SHA gates pass before completion.

## Planner handoff

Read in this order:

1. [requirements-and-risk-traceability.md](./requirements-and-risk-traceability.md)
2. [golden-contract-matrix.md](./golden-contract-matrix.md)
3. the three gate decisions linked above
4. [evidence-canonicalization-and-provenance-contract.md](./evidence-canonicalization-and-provenance-contract.md)
5. [workspace-security-s3-disposition.md](./workspace-security-s3-disposition.md)
6. all eight phase files
7. [implementation-handoff.md](./implementation-handoff.md)

After this planner commit, the next authorized state is **independent plan validation**, not implementation. Validation and a fresh readiness audit must be separate sessions and may amend the plan before any cook phase.
