---
phase: 8
title: "Two-run evidence, rollback and merge handoff"
status: pending
effort: "1.5-2.0 implementation days plus review wait"
dependsOn: [1, 2, 3, 4, 5, 6, 7]
---

<!-- Updated: Initial validation restored pre-implementation validation/readiness ordering. -->

# Phase 8: Two-run evidence, rollback and merge handoff

## Overview

From committed clean tree C1 in the sole implementation worktree, execute two sequential,
completely state-independent bounded golden runs, prove exact equality, rehearse migrations/
rollback, publish only the authorized aggregate fixture in child C2, and record the non-recursive
external issue #7 handoff. This phase does not merge.

## Requirements

- Run A/B have no prior/shared venv, data, home, cache, target, warehouse, export, workspace or evidence state.
- Each monotonic deadline 300 seconds; combined 600 seconds; exact per-step/output/termination policy from handoff.
- All registered commands pass with schema-valid evidence; exact projections/hashes match.
- Changed-path, protected-hash, credential/private-path, symlink/foreign path and command-registry checks pass.
- Rollback restores prior lock/registry/schema/Make/architecture/pointer model and reads retained v1.
- C1 tested tree, C2 external attestation and future remote M remain distinct.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create before behavior | `tests/golden/test_two_run_release.py`, `tests/contracts/test_issue7_handoff.py` | shared-state/time/failure/rollback and C1/C2/M mutation RED cases |
| Generate visible/untracked private state | `.artifacts/evidence/**`, `.artifacts/workspaces/**` | raw/projection/envelope and failure diagnostics; `.artifacts` is not ignored and is never staged |
| Create at C2 only | exact authorized promotion evidence/manifest/invalid files | read-only issue #7 fixture |
| External write | issue #6 comment/PR metadata when later authorized | C1/C2/four digests; no tracked recursion |
| Preserve | every protected/unrelated/other fixture path | pre/post hash/absence/sentinel proof |

## Dependency map

- Requires every prior phase and clean committed C1.
- Produces issue #7’s merge-blocked handoff; issue #7 waits for remote M.
- Independent initial validation and the fresh readiness audit precede implementation and publish the exact implementation input. After implementation, independent implementation validation/readiness evidence and human pre-merge review still precede any merge. This plan never bypasses either gate.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| A/B exact semantic data, volatile run metadata differs | projection equal; only five raw pointers drift |
| semantic/hash/tool/lock/tree difference | determinism failure; no fixture publication |
| 300/600-second timeout or child leak/output overflow | typed failure, bounded evidence, C1 retained |
| rollback at each atomic/migration boundary | old complete/readable state restored |
| C2 manifest contains C2/M/self digest | non-recursion failure |
| squash merge future | remote merge record plus blob equality accepted, false ancestry requirement rejected |
| one of four handoff digests changes | all issue #7 samples/scores invalidated |
| other fixture/protected/ignored path changes | publication blocked |

## Interface checklist

- [ ] A/B evidence roots and all caches/homes are distinct.
- [ ] Comparison reports exact expected projection/hash values and five allowed raw pointers only.
- [ ] Fixture derives from C1 projection and manifest records `testedTreeSha=C1`.
- [ ] External record—not tracked bytes—records C2 and later M.
- [ ] Score invalidation and unscored-preview clearing are explicit.

## Tests Before

1. Add two-run orchestrator tests with deliberate shared-cache/path/tree/tool/semantic drift.
2. Add overall/step timeout, output overflow and failure preservation cases.
3. Add rollback rehearsals for lock, registry/readers, curated pointer model, Make seam and architecture set.
4. Add exact changed/protected/credential/private-path scans and fixture recursion tests.
5. Add C1/C2/M and squash-merge blob-identity handoff tests.

## Implementation

1. Commit implementation/contracts/readers/tests as C1.
2. Keep the C1 worktree source read-only and run `make golden-clean PROFILE=small SEED=42` twice
   sequentially with distinct generated run IDs, homes, venvs, caches, data, warehouses, dbt
   targets/logs, exports, workspaces and evidence roots under the 300/600-second guard. Verify C1
   and the tracked source tree before and after each run. Do not create another worktree or execute
   from a Git-less archive.
3. Run `make data-contracts-check`, `make evidence-contracts-check`, `make migration-contracts-check`, `make architecture-check`, `make architecture-render`, and `make help` through clean/check modes as applicable; retain all result links.
4. Compare exact golden matrix, lock/environment, architecture and projection hashes; run protected/secret/path scans and rollback rehearsals.
5. Derive the 89-row aggregate fixture from the stable projection, validate/scan it, and add only authorized fixture files in child C2.
6. Record C1, C2 and the four required path digests externally. Do not insert C2/M/self digest in tracked bytes; do not merge.

## Refactor

No behavior refactor after C1 evidence without invalidating C1 and restarting both runs. Evidence formatting-only change that changes a schema/hash also requires a new C1 and full rerun.

## Tests After

- Reverify both retained evidence bundles and the tracked fixture from a third reader with a clean
  tracked/index source state and fresh private runtime environment, without regenerating producer
  output; only allow-listed untracked `.artifacts` evidence roots may remain.
- Repeat protected/credential/path/registry scans on the exact C2 tree.
- Require `git ls-files '.artifacts/**'` and the staged-path inventory to be empty for transient
  state, then remove only marker-verified cook-created mutable roots after sanitized evidence is
  retained.
- Rehearse fixture invalidation on each of the four digest identities.
- Verify issue #7 remains unscored/blocked until remote M.

## Regression Gate

- A/B exact equality and runtime/process bounds pass.
- All seven command results pass; no missing required tool/evidence is skipped.
- C2 diff is fixture-authority exact; protected state unchanged.
- Rollback and retained-v1 reader pass.
- F-09/F-11 and SC-01/SC-04/SC-06/SC-11/SC-14/SC-15 pass.

## Failure Evidence, Rollback and STOP

Retain both bounded raw/projection/envelope bundles and any sanitized typed failure before
marker-scoped cleanup. Rehearse lock/registry/schema/pointer/Make/architecture/workspace rollback
before fixture publication; a behavior or schema change after C1 invalidates C1 and both runs.
STOP without C2/publication on any >300-second run or >600-second pair, shared/prior state,
projection mismatch, required skip, protected/credential/private-path/PII-like scan failure,
unsafe cleanup, rollback failure, extra fixture byte, tracked/staged `.artifacts`, or request to
score, PR, merge, tag or bypass human approval.

## Success criteria

- [ ] Two no-prior-state runs reproduce every exact anchor within local bounds.
- [ ] Failure evidence and rollback are safe and verified.
- [ ] Authorized fixture/manifest are aggregate-only, canonical and externally attestable.
- [ ] Issue #7 handoff is merge-gated and score-invalidating on any identity change.
- [ ] No PR, merge, cloud action, destructive migration or human-gate bypass occurred.
