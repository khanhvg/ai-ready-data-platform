---
phase: 7
title: "Make registry and Airflow seam"
status: pending
effort: "1.0-1.5 implementation days"
dependsOn: [1, 2, 3, 4, 5, 6]
---

# Phase 7: Make registry and Airflow seam

## Overview

Add one reversible root include/help integration, one I5-01 fragment, and a machine-readable exact 54-command ownership registry. Preserve every current target. Change only the narrow Airflow path forwarding seam if phase-1 tests prove it is necessary.

## Exact command registry

| Owner | Exact future target set | Count |
|---|---|---:|
| I5-01 | `help`, `golden-clean`, `data-contracts-check`, `evidence-contracts-check`, `migration-contracts-check`, `architecture-check`, `architecture-render` | 7 |
| I5-02 | `learn-preview`, `web-spike-scorecard-check` | 2 |
| I5-03 | `learning-contracts-check`, `lesson-check`, `api-contracts-check`, `evidence-verify` | 4 |
| I5-04 | `runner-test`, `runner-security-test`, `runner-race-test` | 3 |
| I5-05 | `learn`, `learn-status`, `learn-down`, `portal-test`, `portal-a11y`, `portal-e2e`, `lesson-e2e`, `local-journey-e2e`, `portal-visual-review` | 9 |
| I5-06 | `curriculum-check`, `traceability-check`, `architecture-visual-review`, `architecture-lab-e2e` | 4 |
| I5-07 | `data-labs-e2e`, `lake-contracts-check`, `lake-fault-test`, `metadata-contracts-check`, `metadata-reconcile-test` | 5 |
| I5-08 | `compose-check`, `compose-security-check`, `profile-budget-check`, `recovery-test` | 4 |
| I5-09 | `state-matrix-check`, `cost-model-check`, `aws-decision-check` | 3 |
| I5-10 | `terraform-check`, `terraform-validate-offline`, `terraform-test-mocked`, `terraform-plan-aws` | 4 |
| I5-11 | `aws-adapters-contract`, `engine-equivalence`, `aws-composition-check`, `aws-restore-drill` | 4 |
| I5-12 | `ai-admission-check`, `ai-evals` | 2 |
| I5-13 | `release-evidence` | 1 |
| I5-14 | `hosted-authz-test`, `hosted-isolation-test` | 2 |
| **Total** | exact unique owner-target pairs | **54** |

Current 15 targets to preserve exactly: `venv`, `up`, `down`, `seed`, `load`, `health`, `dbt`, `dbt-docs`, `airflow`, `bi`, `catalog`, `lake-up`, `lake-publish`, `catalog-ingest`, `clean`.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | `learning/contracts/command-owner-registry-v1.json` | exact 54 target/owner/security/evidence/availability rows |
| Create | `mk/issue-5/i5-01.mk` | all and only seven I5-01 target recipes |
| Modify | root `Makefile` | minimal sorted include/help discovery seam; no other recipe absorption |
| Create | `tests/contracts/test_command_registry.py` | uniqueness/ownership/availability/collision |
| Create | `tests/golden/test_make_compatibility.py` | current 15 behavior and scoped clean |
| Conditional modify | `orchestration/airflow/callables/pipeline.py` | raw/warehouse/export paths only after failing proof |

## Requirements

- Registry has exactly 54 unique commands/owners; later entries are `future-owner` declarations and do not create recipes.
- `i5-01.mk` owns exactly seven recipes. Root seam includes fragments/discovers help but does not absorb recipes from later issues.
- The complete root diff is the ordered fragment declaration and optional include
  `ISSUE_5_MAKE_FRAGMENTS := $(sort $(wildcard mk/issue-5/*.mk))` followed by
  `-include $(ISSUE_5_MAKE_FRAGMENTS)` at the end of the root file. `help` is implemented in
  `i5-01.mk` from the registry; no other root variable, prerequisite or recipe changes.
- `make help` is non-interactive, reports current/future availability honestly and emits registry evidence.
- Existing 15 target semantics/variables remain compatible; `clean` is never invoked by golden targets.
- Airflow default/optional graph and all callers remain stable. The only allowed seam is optional default-preserving forwarding of generator `--out`, loader `--raw-dir/--duckdb-path`, health warehouse path, caller-supplied private `DBT_PROFILES_DIR`, and export `--duckdb-path/--export-dir`; no DAG or `_run` containment redesign.

## Dependency map

- Exposes implementations from phases 2–6.
- Blocks phase 8 acceptance commands.
- Root/shared core requires serialization; later issue fragments are read-only/absent.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| duplicate command, owner or recipe | registry/root collision failure |
| registry count 53/55 or issue6 count 6/8 | exact-count failure |
| later declaration becomes runnable recipe | ownership failure |
| current target prerequisites/recipe/variables change | compatibility failure |
| `golden-clean` invokes `clean` or follows broad path | security failure |
| Airflow path seam unnecessary | file remains byte-identical |
| path seam used | three explicit paths forwarded; six/eight graph/callers pass |

## Interface checklist

- [ ] Registry row includes command, owner, fragment, tier/security, evidence schema/root, availability and failure rule.
- [ ] Root Make diff is reversible and contains no later recipe.
- [ ] Help distinguishes existing, I5-01 implemented and later future commands.
- [ ] All seven targets are non-interactive and schema-evidenced.
- [ ] Airflow exception is tests-before and line-scoped.

## Tests Before

1. Parse the master list into expected exact owner-command pairs and add count/duplicate/collision mutations.
2. Snapshot current 15 Make recipes/prerequisites/help behavior and test ignored sentinel preservation.
3. Test I5-01 target evidence/non-zero missing-tool behavior; fail because registry/fragment are absent.
4. Run explicit-path Airflow callable characterization for raw directory, warehouse file,
   generated private dbt profile, dbt target/log and export directory. Include import-without-
   optional-dependencies, AST/DAG parse, default-call behavior, explicit-call behavior and exact
   six/eight task-ID/edge regression. The immutable input is expected to fail only the explicit
   path isolation because the callables omit/override those paths; retain that exact failure as
   the proof for the line-scoped exception.

## Implementation

Create registry and I5-01 fragment. Add the smallest sorted include/help seam to root Make. Wire all seven targets to phase implementations with unique run evidence. Apply only the proven optional parameters/environment forwarding enumerated above to `pipeline.py`, retaining all defaults/callers and the DAG byte-for-byte. The golden runner, not Airflow `_run`, owns bounds and environment sanitation.

## Refactor

Keep registry parsing/help formatting out of root Make recipes where possible; root remains a dispatcher. Do not create fragments for later owners or generic runner/process abstractions.

## Tests After

- Run help/registry and all target missing-tool/failure evidence tests.
- Compare current 15 target database/prerequisites/recipes/variables and exercise safe read-only
  representatives; do not start Docker or invoke the existing broad `clean`.
- Import and parse the Airflow seam, exercise every existing default caller, then exercise the
  explicit private raw/warehouse/profile/target/log/export parameters. The DAG source and its
  six/eight graph remain byte-identical.
- Inject duplicate target/fragment/owner mutations privately.
- Verify root Make plus `i5-01.mk` rollback restores exact input behavior.

## Regression Gate

- Machine registry count/ownership is 54/14 owners; I5-01 is exactly seven.
- Current 15 targets preserved; no broad clean or later recipe.
- Airflow remains unchanged or the exact seam is proven and caller-compatible.
- F-08/F-12 and SC-10 pass.

## Failure Evidence, Rollback and STOP

Retain the Make database/help/recipe comparison, registry mutation, exact root diff and Airflow
import/parse/default/explicit-path/graph result. Rollback removes the issue fragment and reverses
the exact two-line root seam plus only the proven forwarding diff as one reviewed inverse. STOP
if any current 15 target changes, the 54/14 registry or exact seven differs, a later fragment gains
a recipe, missing fragments break help, root clean broadens, the DAG changes, or Airflow defaults/
callers/path isolation regress.

## Success criteria

- [ ] Seven issue targets are registered, discoverable and evidenced.
- [ ] Later 47 targets remain non-runnable declarations owned by later issues.
- [ ] Root integration is one reversible seam.
- [ ] Existing Make/Airflow contracts remain stable.
