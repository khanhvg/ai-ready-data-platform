---
phase: 13
title: "Verification Release Recovery and Rollback"
status: pending
priority: P1
dependencies: [5, 6, 7, 8]
effort: "L"
---

# Phase 13: Verification Release Recovery and Rollback

## Overview

Run the release contract from a clean checkout, retain exact-SHA machine-readable evidence, review
real browser/accessibility/resource/security/recovery/rollback behavior and publish only the
surfaces whose gates pass. AWS remains non-applying and AI optional/not-run unless separately
admitted.

## Context Links

- [Fitness catalogue](./requirements-traceability.md#fitness-function-catalogue)
- [Implementation issue graph I5-13](./implementation-issue-graph.md)
- Historical issue #3 evidence (reused as historical, not rerun substitute)
- Every phase acceptance and discovery finding matrix

## Requirements

- `make release-evidence` runs from a detached clean checkout/worktree with no prior venv,
  generated fixtures, caches or volumes required.
- It calls the tracked golden command, architecture/contracts, portal/runner, data, Compose,
  resource, recovery, security and migration gates. Non-applying Terraform/AWS gates run when
  their artifacts are present; otherwise they remain `not-run-optional` for the local release.
- Real browser E2E/visual review and manual keyboard/screen-reader/200%/reduced-motion review are
  recorded with environment/tool/SHA.
- Run race/fault/crash/replay/reset/publish/evidence tamper and rollback rehearsal.
- Verify tracked repository unchanged by lab runs; runtime artifacts ignored/deletable.
- Evidence manifest distinguishes `pass`, `fail`, `not-run-optional` and
  `blocked-by-TBC`; never convert a blocked AWS/AI gate into pass.
- Reuse exact merge/tree/discovery evidence and record final implementation/release SHA.
- Update user/maintainer docs only for actual shipped behavior/commands/architecture.
- Release rollback keeps golden spine and user-owned files; no destructive migration.

## Architecture

The release driver executes named fitness functions and gathers their result manifests, not raw
unbounded logs. Each evidence item has command, tool version, timestamps, input/output SHAs,
artifact hashes and retention class. A top-level release manifest validates cross-links and
finding coverage.

```text
clean detached checkout
 -> golden/contracts/architecture
 -> runner/portal real journey + a11y/visual
 -> data/profile/resource/recovery/security
 -> Terraform static/mock/non-applying
 -> optional AWS/AI status
 -> migration/rollback rehearsal
 -> release-evidence.json + artifact index + clean tree
```

## File Inventory

| Action | Likely path | Rough size | Test impact |
|---|---|---:|---|
| Create | `scripts/release/run-release-evidence.py` | 400-650 LOC | Aggregate driver |
| Create | `contracts/evidence/release-evidence.schema.json` | 180-280 lines | Result/status schema |
| Create | `tests/release/**` | 700-1,000 LOC | Missing/stale/forged/blocked fixtures |
| Create | `scripts/release/rollback-rehearsal.sh` or safe wrapper | 150-250 LOC | Additive rollback |
| Create | `docs/verification/GH-5-<sha>-release-evidence.md` | generated summary | Tracked human index |
| Modify | `Makefile`, CI workflow if repo adopts CI | 50-100 lines | Release target/artifact retention |
| Modify | README/runbook/system architecture/versions | evidence-based only | Shipped behavior |
| Preserve | Historical evidence, discovery, user files | 0 | Hash/clean checks |

## Interface Checklist

- [ ] `FitnessResult(id, command, status, evidence, blocker, duration, toolVersions)`
- [ ] release manifest required/optional gate registry
- [ ] exact SHA/tree/discovery/plan/validation/audit/implementation provenance
- [ ] clean-checkout/worktree lifecycle with explicit safe target
- [ ] rollback manifest and contract compatibility result
- [ ] docs claim-to-evidence link checker

## Dependency Map

- Local release requires Phases 1-8. Phase 13 consumes Phase 10/11 non-applying evidence only when
  those artifacts have already merged; they are not dependencies of the local release.
- Phase 12 is optional and excluded unless admitted.
- Final release/merge remains human-approved.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Clean run relies on stale cache/fixture/volume | Fail; identify dependency |
| Critical | Evidence forged/stale/wrong SHA/verifier | Reject release |
| Critical | Rollback changes/deletes golden/user file | Fail and stop |
| Critical | Race/fault leaves mixed state or dirty repo | Fail; recover and preserve artifacts |
| High | Manual a11y/visual missing | Local release blocked |
| High | Resource threshold exceeded | Profile/release blocked with raw metrics |
| High | Terraform apply/TBC treated as pass | Release schema/policy fails |
| High | Docs claim unsupported AWS cost/readiness | Claim link check fails |
| High | Second clean run differs | Determinism/release fails |

## Tests Before

Build release-manifest fixtures with missing, stale, forged, optional, blocked and failed results.
Write rollback tests against a disposable clone/worktree and sentinel user file.

## Refactor

Only aggregate existing commands/evidence. Do not weaken a phase test to make the aggregate green.
Fix at the owning phase/contract.

## Tests After

Run complete release twice from clean checkouts, compare deterministic contracts, execute manual
reviews, inspect retained artifacts and run rollback rehearsal. Confirm final tree clean and no
containers/processes remain.

## Regression Gate

```bash
make release-evidence
git diff --check
git status --short
```

The release driver expands to:

```bash
make golden-clean PROFILE=small SEED=42
make learning-contracts-check api-contracts-check evidence-contracts-check
make architecture-check architecture-render traceability-check
make runner-test runner-security-test runner-race-test
make portal-test portal-a11y lesson-e2e local-journey-e2e portal-visual-review
make data-contracts-check data-labs-e2e lake-fault-test metadata-reconcile-test
make compose-check compose-security-check profile-budget-check recovery-test
make terraform-check terraform-plan-offline
```

## Implementation Steps

1. Write release/blocked/rollback fixtures and schema.
2. Implement safe clean-worktree aggregate driver and artifact index.
3. Run all local automated gates twice and compare.
4. Perform real browser visual plus manual accessibility review.
5. Run resource, race/fault/crash, tamper, migration and rollback rehearsals.
6. Run Terraform static/mock/non-applying gates; record apply TBCs as blocked.
7. Update docs from evidence and generate tracked human-readable index.
8. Obtain mandatory human pre-merge approval; commit/push/merge only in authorized workflow.

## Success Criteria

- [ ] Clean checkout regenerates all required ignored fixtures and machine evidence.
- [ ] First local journey and every required fitness function pass with exact SHAs.
- [ ] Critical/High discovery finding coverage is complete and no gate disappeared.
- [ ] Accessibility, browser visual, resource, security, race and rollback evidence is retained.
- [ ] AWS apply/AI optional states are honest and do not block credential-free local release.
- [ ] Rollback preserves golden spine, historical/discovery evidence and unrelated user files.
- [ ] No cloud apply/resource creation or destructive migration occurs.

## Risk, Security, and Rollback

Release automation can accidentally become destructive. It operates only in an explicitly
created/validated temporary worktree and removes generated state, never arbitrary directories.
Secret scans run before artifact retention. Rollback is additive/feature-flag/adapter based and
uses exact SHAs; any destructive data step requires a separate approved migration.

## Next Steps

After independent validation/readiness audit and implementation completion, the human owner
decides merge/release. AWS apply and optional AI remain separate authorized issues.
