# Dependency and Release Gates

## Purpose

Define the only legal path from this planner-only output to Stage A and Stage B cook authority.
Planning may run in parallel; implementation may not consume a plan, feature branch, readiness
input, ignored artifact, or predicted SHA as though it were a released dependency.

## Immutable Planner Provenance

| Input | Exact value | Authority |
|---|---|---|
| Planner input / integration head | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Required clean Issue #11 base |
| Golden main | `3cd3d41f71582774e8d9656a51d1044035f4503c` | Accepted master provenance |
| Reviewed golden tree | `d0273731a5077cc17c2f4398057623b83a50bb65` | Preserved data-platform truth |
| Master discovery | `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430` | Accepted findings/source register |
| Master planning sync | `b04ff80486de8a9c008c6320669212f27df80182` | Accepted planning input |
| Master planner | `8ec96f92245c679d019ac3648c5c2d77a49f0429` | Accepted master plan |
| Master validation | `5962316b8113ece592a26fe6211a97ae77eb70fb` | Accepted initial validation |
| Red-team/readiness input | `bf740edb87452fe766591d0eeefd0bd5151220fa` | Accepted risk input |
| Master readiness report | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Fan-out authority only |
| Audited mapping/integration handoff | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Ownership/dependency graph |
| Owner parallelization decision | [Issue #5 comment 5036142770](https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5036142770) | Plan now; do not bypass dependencies |
| Live Issue #11 | [Issue #11](https://github.com/khanhvg/ai-ready-data-platform/issues/11) | OPEN, initial label `triaged`, risk high/TDD/S3/architecture/curriculum |

Primary repository inputs:

- [Master plan](../260721-005-enterprise-learning-sandbox/plan.md)
- [Phase 6](../260721-005-enterprise-learning-sandbox/phase-06-architecture-curriculum-templates-and-fitness-functions.md)
- [Curriculum map](../260721-005-enterprise-learning-sandbox/curriculum-and-competency-map.md)
- [Lesson/lab contract](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md)
- [Architecture views](../260721-005-enterprise-learning-sandbox/architecture-view-plan.md)
- [Architecture decisions](../260721-005-enterprise-learning-sandbox/architecture-decisions.md)
- [Execution authority](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md)
- [Requirements traceability](../260721-005-enterprise-learning-sandbox/requirements-traceability.md)
- [Implementation graph](../260721-005-enterprise-learning-sandbox/implementation-issue-graph.md)
- [Master readiness](../260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md)
- [Issue #6 architecture toolchain](../260721-006-freeze-golden-baseline/architecture-toolchain-decision.md)
- [Issue #6 implementation handoff](../260721-006-freeze-golden-baseline/implementation-handoff.md)

## Fresh Dependency Snapshot

Observed after `git fetch --prune origin` and fresh GitHub reads on 2026-07-22:

| Dependency | Fresh state | Why it is not consumable now |
|---|---|---|
| Issue #8 learning contracts | OPEN; label `ready to cook`; repair candidate `393b66e93461433fcded4ce4e6defa64f937fcfa` is on `feature/issue-5-03-learning-contracts-v3` and awaits one fresh exact-head review; no matching PR, passing review, human exact-head approval, merge, tag, or release | Candidate/test evidence is not released downstream contract authority; the prior readiness input and every failed/superseded feature head are also forbidden as dependencies |
| Issue #10 real journey/renderer | OPEN; label `ready for plan audit`; blocked readiness-audit head `4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7` has `COOK_SCOPE=none`; no matching implementation PR, passing merged journey, released renderer, tag, or release | A blocked plan audit is not implementation, passing journey, merge, renderer release, or downstream authority |

These SHAs are status evidence only. They are forbidden as future dependency placeholders.
The live #8 review may later produce new evidence, but an in-flight or published review comment
still cannot substitute for the complete owner-authored release handoff in Gate A.

## Gate A — Released Issue #8 Contracts

Stage A remains blocked until one owner-authored release handoff supplies all of the following:

1. Exact released Issue #8 commit SHA reachable from the authorized merged integration lineage,
   not merely a plan/readiness/feature-branch SHA.
2. Release identity and merge/attestation URL; Issue #8 contract version registry and every
   consumed lesson/lab/progress/prerequisite/hint/evidence/operation-matrix path.
3. SHA-256 for every consumed schema, validator, registry, fixture, example, and canonicalization
   rule; exact compatibility/rollback versions.
4. Exact evidence/fitness result bindings and compatibility. The current
   `fitness-result-v1` schema/registry is Issue #6 command-result truth; the Issue #8 validated
   plan currently proposes a distinct Issue #8 evidence version, but that proposal is not a
   release. The later amendment must pin the actual released #8 evidence schema and an exact
   owner-authorized mapping to the Issue #11 command-result requirement. It may not bind the two
   by name, copy the Issue #6 schema, consume the proposed version, or invent a compatibility
   object. If the release supplies no authorized mapping, STOP for a plan/owner decision.
5. Exact successful release commands, evidence locator/hash, tested tree SHA, implementation
   review, and human exact-head pre-merge approval.
6. Confirmation that Issue #11 consumes these files read-only and creates no duplicate lesson,
   lab, progress, completion, evidence, OpenAPI, or operation-matrix truth.

After all six exist, a fresh amendment must pin the values, derive a closed Stage A file and
command allow-list, update protected hashes, and run independent validation plus fresh readiness.
Only that readiness output may authorize a Stage A cook.

## Gate B — Passing Merged Issue #10 Journey and Renderer

Stage B remains blocked until one owner-authored release handoff supplies all of the following:

1. Exact Issue #10 merged commit SHA reachable from the authorized integration lineage.
2. Passing real promotion-trust journey evidence at that exact tree, including tested commands,
   dependency SHAs, evidence hash, reset/verify/completion result, and cleanup result.
3. Exact released portal renderer/registry/content-discovery paths, versions, build/test commands,
   input contract hashes, publication mechanism, and read-only consumer rules.
4. Exact client/renderer error, unavailable, no-JavaScript/static, accessibility, and evidence
   presentation semantics needed by the architecture lab. No route, module, viewport, or fallback
   may be guessed from the Issue #10 plan.
5. Proof that Issue #11 can publish content/lab assets through the released seam without editing
   portal source. If no such seam exists, STOP for a serialized portal integration lease and new
   scope authorization; do not patch the portal opportunistically.
6. Passing Stage A release SHA and exact #8 contract release still current and compatible.

After all six exist, a second fresh amendment must pin the values, derive a closed Stage B file
and command allow-list, update threat/rollback/evidence mappings, and run independent
revalidation plus fresh readiness. Only that readiness output may authorize Stage B.

## Architecture View Lease Gate

Issue #6 selected LikeC4 `1.59.1` plus WASM Graphviz and explicitly records the master
`architecture/structurizr/**` layout as a placeholder, with no silent Structurizr/browser/native
Graphviz fallback. The Issue #11 body and master graph retain “Structurizr expansion” as an
ownership label. The later amendment must reconcile that label against the released Issue #6
toolchain:

- default legal interpretation: additions-only expansion using the exact released LikeC4
  toolchain and a lease-provided extension seam;
- forbidden: alter the six local source files/rows/renders, tool lock, renderer/normalizer, or
  hard-coded six-view fitness logic without explicit shared-core authority;
- if no additions-only seam exists, STOP and obtain a separately validated shared-core/toolchain
  migration or extension lease; do not invent a second renderer or call Structurizr equivalent.

The amendment must name the exact lease start SHA, owner, paths, duration, conflict check, old/new
manifest semantics, render commands, and rollback. Until then, architecture expansion paths and
commands remain empty.

## Current and Future Authority Matrix

| Boundary | Current planner output | Value required in later amendment |
|---|---|---|
| Implementation input SHA | None | Exact readiness output commit for the authorized stage |
| Dependency release SHAs | `[]` | Exact accepted #8, and #10 for Stage B |
| File allow-list | `[]` | Enumerated exact paths, no wildcard outside immutable ownership ceiling |
| Command allow-list | `[]` | Exact commands, arguments, tools, versions, time/resource bounds |
| Contract bindings | `[]` | Exact paths, versions, SHA-256, reader/rollback rules |
| Portal renderer bindings | `[]` | Stage B exact released modules/registries/build-test commands |
| Fitness/evidence schema bindings | `[]` | Exact released #8 evidence path/version/SHA-256 plus an owner-authorized command-result compatibility mapping; never the current #6 copy as fallback |
| View lease | None | Exact additions-only sources/rows/renders and protected baseline |
| Cloud/AWS/Terraform authority | None | Remains none for both stages |

## Dependency Preflight Algorithm

At each amendment/readiness and again before the first write:

1. Fetch origin and GitHub issue/PR/release state fresh.
2. Require clean worktree and required branch; local HEAD = tracking = fresh-live exact authorized
   input.
3. Verify every release SHA exists, is reachable from the named merged lineage, and contains the
   exact released blobs/hashes.
4. Verify prior dependency commands/evidence against the release attestation; reject stale or
   mutable locators.
5. Verify no active shared-contract, architecture-view, portal, generated-render, or Make lease
   overlaps.
6. Recompute the Issue #6 protected baseline and fail on any byte/blob drift.
7. Compare the staged diff to the amendment’s exact file allow-list before and after each phase.
8. Stop on mismatch. Never rebase, merge, reset, force-push, delete a competing worktree, or
   substitute another dependency to make the gate pass.

## Hard STOP Conditions

- Either dependency is unmerged, unreleased, stale, unreachable, or hash-inconsistent.
- A plan/readiness/feature SHA is offered as a release.
- Any future SHA, route, renderer, contract, schema, fixture, tool, or command is inferred.
- Exact allow-lists remain empty or fresh validation/readiness is missing.
- Protected Issue #6 bytes drift or a view/tool/shared-contract lease overlaps.
- Portal integration would require an unowned portal edit.
- AWS credentials, cloud calls, Terraform plan/apply/destroy, or resource creation become required.
- Human exact-head pre-merge approval or independent implementation review is absent.

## Unresolved Questions

None. The missing release values are dependency outputs, not choices for this planner.
