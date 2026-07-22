# Dependency and Release Gates

## Purpose

Define the only legal path to Stage A and Stage B cook authority. Released dependency Gate A is
closed, but the [post-review scaffold-first amendment](./stage-a-release-amendment.md) reopens the
Issue #11 plan-validation/readiness gate. Current implementation authority is `none`. Stage B
remains blocked and empty. A plan, failed feature branch, prior readiness result, ignored artifact,
or predicted SHA is never released implementation authority.

## Immutable Planner Provenance

| Input | Exact value | Authority |
|---|---|---|
| Original planner input / integration head | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Historical initial planning provenance; not the current correction or v3 base |
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
| Live Issue #11 | [Issue #11](https://github.com/khanhvg/ai-ready-data-platform/issues/11) | OPEN; post-correction label must be `ready for plan validation`; risk high/TDD/S3/architecture/curriculum |
| Stage A amendment start | `ab653f6edec73e5ef875723945d2e3cd7814b4e6` | Historical exact-release amendment input |
| Post-review correction start | `1c62b68159ffc48cc2f063c137cb9072d8ed741f` | Exact clean local/upstream/fresh-live author input |
| Fresh v3 clean base | `c07c9a080be7be88447aac497bdf0a2b5fddd020` | Descends from `fecf6bb8…`; all 50 paths absent; failed v1/v2 not ancestors |
| Released integration / Issue #8 Stage A | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | Current read-only dependency and required ancestor of the v3 base |
| Released tree | `27fc3667ef37892dad5c3fbfd76769f65a0760be` | Independently recomputed commit tree |

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

## Historical Dependency Snapshot

This table records the original blocked audit on 2026-07-22. It is retained as history and does
not describe current Stage A authority:

| Dependency | Fresh state | Why it is not consumable now |
|---|---|---|
| Issue #8 learning contracts | OPEN; label `ready to cook`; candidate `393b66e93461433fcded4ce4e6defa64f937fcfa` on `feature/issue-5-03-learning-contracts-v3` failed fresh exact-head review with two High and one Medium findings; owner comment `5040086369` authorizes one narrow follow-up repair; no matching PR, passing review, human exact-head approval, merge, tag, or release | Failed review and repair authority are not released downstream contract authority; the prior readiness input and every failed/superseded feature head are also forbidden as dependencies |
| Issue #10 real journey/renderer | OPEN; label `ready for plan audit`; blocked readiness-audit head `4a36bab4f8a8c9f393060cf7337b2e5ca45cd9b7` has `COOK_SCOPE=none`; no matching implementation PR, passing merged journey, released renderer, tag, or release | A blocked plan audit is not implementation, passing journey, merge, renderer release, or downstream authority |

Those former candidate SHAs remain status evidence only and are forbidden as dependency
placeholders. The current release binding is the exact merge object below.

## Gate A1 — Released Issue #8 Contracts — PASS

Fresh Git and GitHub proof closes the Stage A dependency gate:

1. `refs/heads/integration/issue-5-local-learning` resolves exactly to
   `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; its ordered parents are the PR #23 merge
   `5c2244c2c860234d0df49cf0a42ad950c6495717` and composition head
   `734cf637a20ae186597e23d96a194ed4e30220ea`.
2. [Release evidence](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549)
   records `STAGE_A_MERGED_VERIFIED_RELEASED` and exact 56/56, invalid 65/65, API 16, final 4/4,
   inherited 19/19 + 1/1 + 13/13 results without inventing a CI-success claim.
3. The release contains a 21-path contract-set descriptor with SHA-256
   `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`; the amendment pins
   every consumed read-only path plus canonicalization, version registry, command registry,
   Python lock, and public validator command identities.
4. I5-06 activates only `fitness-result-v1` command evidence. Released `fitness-result-v2` has
   `emissionFallback: null`, so it and all progress/completion/learner-evidence outputs are
   explicit non-authorities, not guessed compatibility targets.
5. Issue #11 creates no shared contract, lesson, lab, progress, completion, evidence, OpenAPI,
   Vite, or operation-matrix truth.
6. The released dependency is consumable read-only. This does not pass Issue #11 plan readiness.

## Gate A2 — Corrected Issue #11 Plan Validation and Readiness — BLOCKED

The author correction proposes the exact 50-path/16-command scope and 7/5/38 scaffold-first
chronology. Before implementation, a fresh xhigh context independent of this author must validate
the exact pushed correction head and map all seven findings. A later fresh readiness auditor must
bind the validator output, exact released dependencies, proposed view lease, paths/commands,
resource/visual/evidence/cleanup rules and v3 base. Until both pass:

```yaml
validatedAmendmentSha: null
auditedAmendmentSha: null
stageAImplementationInputSha: null
implementationAuthority: none
```

A future v3 input is derived by applying only the exact passed plan-artifact diff to clean
`c07c9a080be7be88447aac497bdf0a2b5fddd020`. No product/test/render/evidence commit from failed v1
or v2 may be cherry-picked or copied. The derived SHA is recorded and preflighted, never predicted.

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
ownership label. The current amendment reconciles that label against the released Issue #6
toolchain:

- proposed legal interpretation, pending Gate A2: additions-only expansion using the exact
  released LikeC4 toolchain and an I5-06-owned extension seam beneath
  `architecture/expansions/i5-06/**`;
- forbidden: alter the six local source files/rows/renders, tool lock, renderer/normalizer, or
  hard-coded six-view fitness logic without explicit shared-core authority;
- if no additions-only seam exists, STOP and obtain a separately validated shared-core/toolchain
  migration or extension lease; do not invent a second renderer or call Structurizr equivalent.

The amendment names the proposed lease start SHA, owner, exact 19 expansion paths, duration,
conflict rule, separate base/extension manifest semantics, render commands, and rollback. The
existing exact-six roots remain separate and byte-identical. The technical seam is valid, but the
lease becomes implementation authority only after Gate A2 passes.

## Current Authority Matrix

| Boundary | Stage A | Stage B |
|---|---|---|
| Cook base | Clean `c07c9a0…` plus exact future passed plan-only diff; derived SHA currently `null` | None; blocked on Issue #10 |
| Dependency release | Released Issue #8 Stage A, read-only | `[]` |
| File allow-list | Proposed exact 50 final create-only paths; implementation authority `none` | `[]` |
| Command allow-list | Proposed exact 16 shapes; implementation authority `none` | `[]` |
| Contract bindings | Exact released paths/blobs/hashes; read-only | `[]` |
| Portal renderer bindings | `[]`; not needed | `[]` |
| Evidence binding | Existing `fitness-result-v1` command envelope only; no learner evidence | `[]` |
| View lease | Proposed `i5-06-stage-a-architecture-expansion-v1`; exact additions only; pending Gate A2 | None |
| Cloud/AWS/Terraform authority | None | None |

## Dependency Preflight Algorithm

At each amendment/readiness and again before the first write:

1. Fetch origin and GitHub issue/PR/release state fresh.
2. Require clean worktree and required branch; local HEAD = tracking = fresh-live exact authorized
   input. For v3, require exact derived input from clean `c07c9a0…` plus the passed plan-only diff.
3. Verify every release SHA exists, is reachable from the named merged lineage, and contains the
   exact released blobs/hashes.
4. Verify prior dependency commands/evidence against the release attestation; reject stale or
   mutable locators.
5. Verify no active shared-contract, architecture-view, portal, generated-render, or Make lease
   overlaps.
6. Recompute the Issue #6 protected baseline and fail on any byte/blob drift.
7. Compare commit chronology and diff to the exact 7 scaffold / 5 complete tests / 38 semantic
   complement partition and final 50-path allow-list before and after each phase.
8. Stop on mismatch. Never rebase, merge, reset, force-push, delete a competing worktree, or
   substitute another dependency to make the gate pass.

## Hard STOP Conditions

- A dependency required by the active stage is unmerged, unreleased, stale, unreachable, or
  hash-inconsistent.
- A plan/readiness/feature SHA is offered as a release.
- Any future SHA, route, renderer, contract, schema, fixture, tool, or command is inferred.
- Gate A2 is not PASS, exact derived v3 input is null/mismatched, or fresh validation/readiness is
  missing.
- Protected Issue #6 bytes drift or a view/tool/shared-contract lease overlaps.
- Portal integration would require an unowned portal edit.
- AWS credentials, cloud calls, Terraform plan/apply/destroy, or resource creation become required.
- Human exact-head pre-merge approval or independent implementation review is absent.

## Unresolved Questions

None for Stage A. Issue #10 release values are dependency outputs that keep Stage B blocked; they
are not guessed choices for this plan.
