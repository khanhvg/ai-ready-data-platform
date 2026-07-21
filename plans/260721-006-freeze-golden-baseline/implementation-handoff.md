# Implementation handoff

## Entry gate

Do not implement from the discovery SHA or original planner commit. Independent plan validation is followed by a fresh readiness audit. Cook begins only if both publish explicit acceptance, issue #6 authority remains unchanged, the worktree is clean at the exact remotely observed `IMPLEMENTATION_INPUT_SHA` emitted by readiness, and a human has authorized that later phase.

At implementation start, prove local HEAD, tracking ref and remote branch identity all equal that externally recorded `IMPLEMENTATION_INPUT_SHA`; prove ancestry contains planner artifact `cec9f6b02cb3bf9f2aa7e2cf26af32692008aacd`, discovery `7a65da010abf0e3730731b6d744b532156c48fdc`, integration `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` and master readiness `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`. A mismatch, active shared lease or dirty tree is `BASE_AUTHORITY_MISMATCH` and STOP.

The only future implementation branch is `feature/issue-6-golden-baseline-contracts`; the only
future product worktree is
`{workspace-parent}/ai-ready-data-platform-issue-6-implementation`, where
`{workspace-parent}` is resolved as the parent directory of the primary repository. The exact
implementation input is the containing readiness-audit commit attested in issue #6 after
publication. Before creation, fetch and prove both the local/remote branch and exact worktree path
are absent. Create them once from that full SHA, push the unchanged branch with upstream tracking,
fetch, and require local HEAD = upstream = live remote = input before the first write. A
pre-existing branch/path, divergence or active writer is a STOP; never reuse, delete, reset,
rebase, merge, force-push or destructively clean around it.

One implementation actor executes all eight phases sequentially. No parallel implementation
writer, second product worktree, phase-5/6 fan-out or shared-contract lease overlap is allowed.
If integration or authority changes, stop for a new validated/readiness input rather than merging
or rebasing during this lease. [audit/cook-scope.md](./audit/cook-scope.md) is the executable task
and RED/evidence contract.

## Exact owned paths

The implementation allow-list is:

```text
scripts/golden/**
contracts/data/retail-golden-v1.json
contracts/data/promotion-trust-v1.yaml
contracts/data/curated-release-manifest.schema.json
learning/contracts/**
tests/golden/**
tests/contracts/**
tests/fixtures/learning/promotion-trust/evidence-v1.json
tests/fixtures/learning/promotion-trust/manifest.json
tests/fixtures/learning/promotion-trust/invalid/**
requirements/golden-py312-macos-arm64.in
requirements/golden-py312-macos-arm64.lock
requirements/golden-py312-macos-arm64.metadata.json
requirements/golden-lock-tools.in
requirements/golden-lock-tools.lock
requirements/architecture/package.json
requirements/architecture/package-lock.json
architecture/likec4/specification.c4
architecture/likec4/model/people-and-systems.c4
architecture/likec4/model/learning-platform.c4
architecture/likec4/model/data-platform.c4
architecture/likec4/model/local-deployment.c4
architecture/likec4/views/C4-L0.c4
architecture/likec4/views/C4-L1.c4
architecture/likec4/views/C4-L2-LOCAL.c4
architecture/likec4/views/C4-L3-RUNNER.c4
architecture/likec4/views/DEP-LOCAL.c4
architecture/likec4/views/DYN-JOURNEY.c4
architecture/likec4/view-manifest.yaml
architecture/rendered/C4-L0.{svg,txt}
architecture/rendered/C4-L1.{svg,txt}
architecture/rendered/C4-L2-LOCAL.{svg,txt}
architecture/rendered/C4-L3-RUNNER.{svg,txt}
architecture/rendered/DEP-LOCAL.{svg,txt}
architecture/rendered/DYN-JOURNEY.{svg,txt}
architecture/rendered/render-manifest.json
Makefile                 # one include/help seam only
mk/issue-5/i5-01.mk      # only issue #6's seven recipes
orchestration/airflow/callables/pipeline.py  # only if tests prove raw/warehouse/export path forwarding absent
```

The master phase explicitly identifies `tests/golden/**` and `tests/contracts/**` as the issue’s evidence-core test surface. No other test/fixture directory is implied. If independent validation determines “evidence core” maps differently, it must amend authority before cook; the implementer may not guess.

## Protected paths and behavior

Hard deny-list:

```text
release-manifest.json
docs/code-standards.md
plans/260721-006-freeze-golden-baseline/discovery/**
all other plans/discovery/audit history
all tests/fixtures/** except the exact promotion-trust paths above
.gitignore
data-generator/**
ingestion/**
transform/dbt/**
serving/rill/**
orchestration/airflow/dags/**
lake/**
governance/**
portal/**
runner/**
terraform/** and all cloud/AWS paths
mk/issue-5/i5-02.mk through i5-14.mk
unrelated tracked, ignored and generated files
```

Read-only characterization of these paths is required. At the planner input, root `release-manifest.json` SHA-256 is `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539`; `docs/code-standards.md` is absent and must remain absent. Before/after manifests also hash all protected tracked files and create unrelated ignored sentinel files outside issue roots. The narrow Airflow file is deny-by-default: only a failing tests-before proof may activate its exact-path exception, and its diff may only forward explicit raw/warehouse/export workspace parameters while preserving the six/eight graph and current callers.

The repository-wide ignore rule currently matches `package-lock.json`; `.gitignore` is protected. After generating and verifying the exact 119-record architecture lock, stage only `requirements/architecture/package-lock.json` with an exact-path force-add. Never force-add a directory or change ignore rules. The Python `requirements/*.lock` paths are not ignored and use normal staging.

The already-discovered narrow seam is concrete: preserve every existing default while allowing `seed` to append `--out <raw-dir>`; `load_raw` to append `--raw-dir <raw-dir> --duckdb-path <warehouse-file>`; `health_check` to receive the same warehouse file; dbt build/docs to honor a caller-supplied private `DBT_PROFILES_DIR` (whose generated profile points at that warehouse and whose target/log paths are private) instead of always overwriting it with the product project directory; and export to append `--duckdb-path <warehouse-file> --export-dir <export-dir>`. No DAG file, task ID/edge, `_run` containment, publisher callable or default behavior changes. Bounded golden process execution wraps this seam outside Airflow; generalized Airflow subprocess containment remains I5-04.

I5-01 must not change `lake/publish_iceberg.py`; implement runner containment; create a portal; generate scores/ADR; add campaign attribution; create AWS/Compose/Terraform resources; or modify the root release manifest.

## TDD execution order

1. Implement all phase-01 characterization and mutation tests. Run them against immutable input, record expected failing IDs for not-yet-created contracts/commands, and prove current business anchors pass read-only characterizers.
2. Implement phase 2 lock/bootstrap tests and exact locks. Repeat both empty-cache full-run proofs; never rewrite a lock during `golden-clean`.
3. Implement phase 3 workspace/process/evidence safety tests; then the smallest allocation/execution/envelope primitives that make them pass.
4. Implement phase 4 schemas, registry, readers and canonicalization only after parser/JCS/mutation tests fail for the expected reason.
5. Implement phase 5 data/promotion/curated-release schemas and readers; generate semantic mutations privately. Do not publish the tracked fixture yet.
6. Implement phase 6 LikeC4 source/manifest/tool lock and render wrapper; render/normalize/compare all six atomically.
7. Implement phase 7 machine registry, issue fragment and reversible root include/help; activate the narrow Airflow seam only if its characterization test is still failing.
8. Phase 8: commit C1; from the single read-only C1 implementation worktree run the sequential
   two-run 600-second oracle in disjoint, fresh private state roots; rehearse rollback;
   generate/scan the authorized fixture; commit C2; publish external attestation. Do not merge.

Within every phase the order is: **Tests Before → smallest implementation → Refactor with tests green → Tests After → Regression Gate → evidence finalization**. Never weaken an anchor or mutation to make a result pass.

## Public commands and canonical evidence

These seven future public targets are the entire I5-01 command surface. They are planned here; they do not exist at the planner input.

| Registered command | Fitness ID / evidence root | Required internal checks and typed failure boundary |
|---|---|---|
| `make help` | `.artifacts/evidence/command-registry/<run-id>/` | parse machine registry, 54 unique owner assignments, current 15 preserved, issue seven only; duplicate/missing/owner mismatch fails |
| `make golden-clean PROFILE=small SEED=42` | `.artifacts/evidence/golden/<run-id>/` | base/lock/platform/protected preflight; new workspace/cache/venv; exact pipeline; raw capture; projection/envelope; fixture candidate; cleanup; all required drift fails |
| `make data-contracts-check` | `.artifacts/evidence/data-contracts/<run-id>/` | retail, promotion and curated manifest schemas/readers; exact matrices and mutation suite |
| `make evidence-contracts-check` | `.artifacts/evidence/evidence-contracts/<run-id>/` | JSON/JCS vectors, raw/projection/envelope, registry, fixture digest/redaction/non-recursion and tamper tests |
| `make migration-contracts-check` | `.artifacts/evidence/migration-contracts/<run-id>/` | current/backward dispatch, private migration vector, N-1 preservation, rollback rehearsal |
| `make architecture-check` | `.artifacts/evidence/architecture-check/<run-id>/` | exact tool lock, six sources/model/fitness/text/render hashes/freshness; private regeneration; no writes to committed renders |
| `make architecture-render` | `.artifacts/evidence/architecture-render/<run-id>/` | two staged deterministic renders then atomic six-view replacement; failure leaves previous complete set |

`learning/contracts/command-owner-registry-v1.json` contains all 54 master target entries and owners; I5-01’s entries alone have `implementationPath: mk/issue-5/i5-01.mk`. Later entries are declarations with their later owner/fragment and `availability: future-owner`, not recipes. `make help` derives discoverability from this file without fabricating later targets.

Lock/bootstrap assertion, two-run comparison, fixture verification, protected-path scan and rollback rehearsal are named internal fitness steps inside the seven commands. They are not extra public shell commands and therefore cannot escape the owner registry. Tests invoke the registered targets rather than undocumented direct scripts.

Every target is non-interactive, closes stdin, uses only pinned tools/private paths, emits `fitness-result-v1` on pass or safe failure, and exits non-zero for required missing tool/evidence. Remediation is typed and bounded; it never instructs the caller to disable hashes, broaden permissions, skip a gate or run a curl-to-shell installer.

For the new `golden-clean` target only, `PROFILE=small` is the golden data-profile argument and is forwarded as generator `--profile small`; it does not invoke the existing `seed` target or reinterpret the existing `PROFILE` variable for `up`/Compose. `SEED=42` is forwarded exactly. Any other golden profile/seed is outside v1 and fails without changing existing target behavior.

## Runtime plan

The discovery host completed the unlocked current flow in about 155 seconds. The initial reproducibility guard is host-local, not a product/global SLO:

| `golden-clean` step | Deadline |
|---|---:|
| repository/platform/protected snapshot and private allocation | 10 s |
| hash-only empty-cache Python bootstrap | 120 s |
| generate 18 CSVs and immutable manifest projection | 20 s |
| load DuckDB and health check | 20 s |
| dbt build | 45 s |
| immutable build capture then dbt docs | 25 s |
| export 11 marts and semantic contract projection | 25 s |
| evidence validation/atomic finalization/scoped cleanup | 25 s |
| termination/reap reserve | 10 s |
| **one monotonic run deadline** | **300 s** |

Unused step time does not extend the 300-second monotonic deadline. Two runs are sequential with completely independent venv/data/cache/home/workspaces and one combined 600-second deadline. Each timeout terminates the process group (TERM 5 seconds, KILL/reap 5 seconds) and preserves bounded failure evidence. Per-step stdout and stderr are each 2 MiB; combined retained output is 16 MiB/run.

Separate command initial bounds: `help` 10 seconds; each data/evidence/migration contract check 60 seconds; architecture check/render 120 seconds each. These are local regression guards and must be recalibrated only with retained measurements and an explicit contract revision, never silently treated as global availability/performance promises.

## Curated release migration/rollback handoff

The schema defines one immutable release containing exactly the ordered 11 asset IDs. All entries share `releaseId`, `dataRunId`, `testedTreeSha`, input identity, lock/contract set and engine snapshot; each has logical/physical identity, schema/content hash, row count and immutable staged locator. One separate current-pointer document contains exactly one `currentReleaseId` and manifest hash plus optional previous release ID. JSON Schema plus semantic validation reject duplicate IDs (JSON Schema `uniqueItems` alone is insufficient), missing/extra IDs and mixed generations.

Rollback semantics are contractual only: a future publisher validates a complete prior immutable manifest, atomically changes one current pointer, then reads back/reconciles. Issue #6 tests the state-machine fixtures but does not stage, switch, drop/create, read back or reconcile real assets. I5-07 owns those actions.

Evidence/version migration is additive-first: retain v1 schemas/readers and prior lock; update registry only with proven migration and rollback; never mutate retained evidence. Architecture rollback restores source/manifest/tool lock/render text as one set. Make rollback restores the root include/help and `i5-01.mk` together. Workspace rollback deletes only a marker-verified issue-owned mutable root and preserves failure evidence.

## Completion and external handoff

Before calling implementation complete, require:

- exact changed-path allow-list and protected hashes;
- two complete C1 runs with equal lock/environment/projection hashes and exact golden anchors;
- all seven target results pass and link under `.artifacts/evidence/**`;
- architecture six-set freshness and deterministic render pass;
- rollback rehearsals pass without altering protected/current user state;
- tracked fixture fields/path scan and four external handoff digests pass;
- C2 contains only authorized fixture/attestation changes relative to C1;
- human pre-merge approval remains outstanding and no PR/merge/cloud/destructive action occurred unless separately authorized.

The external issue #6 comment records C1, C2, all four handoff digests, evidence locators, tool/lock identities and explicit integrity-not-authenticity language. Issue #7 waits for remote M and verifies exact blobs as specified in [issue-7-fixture-and-merge-handoff.md](./issue-7-fixture-and-merge-handoff.md).
