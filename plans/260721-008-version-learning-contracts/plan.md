---
title: "Issue #8: Version lesson, lab, progress, and evidence contracts"
description: "Released Stage A contract core plus the completed post-release decision that a bounded Stage B consumer-binding release is required."
status: completed
priority: P1
issue: 8
branch: "plan/issue-8-stage-b-amendment"
tags: [feature, api, shared-core, contracts, tdd, security-s3, migration]
blockedBy: []
blocks: [9, 10]
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
planningMode: "post-stage-a-release-audit"
inputSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
releaseIntegrationSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
stageARelease: "pass"
stageBReadiness: "required-planned-separately"
sharedContractLease: "active"
stageBPlan: "../260722-008-stage-b-release/plan.md"
stageBRequirementAudit: "../260722-008-stage-b-release/audit/post-stage-a-requirement-audit.md"
---

# Issue #8: Version Lesson, Lab, Progress, and Evidence Contracts

## Outcome

Stage A is a valid released core at integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`. It delivered the I5-03-owned framework-neutral
schemas, version/readers, 16-operation OpenAPI matrix, completion/evidence rules, promotion-trust
lesson/lab/manifest, public checks, compatibility behavior, and 21-entry contract set. The public
release evidence remains passing and the released Stage A bytes remain immutable.

The post-release dependency audit found one bounded consumer incompatibility that Stage A did not
test: its promotion-trust manifest calls two analytical keys `region` and `category`, while the
hash-pinned Issue #6 evidence and released Issue #7 Vite contract use `region_name` and
`category_name`. The grain ID `dq` is also presented as `data-quality` by the Vite contract. There
is no released alias/binding document. Issue #10 may consume shared contracts read-only and cannot
invent that mapping inside the portal.

Stage B is therefore required, but only as the additive, hash-bound, presentation-identifier
binding defined by the fresh [Stage B release plan](../260722-008-stage-b-release/plan.md). It does
not reopen Stage A, add portal/runner behavior, or create a second completion/validation authority.

## Stage Decision

| Stage | Released authority | Disposition |
|---|---|---|
| A — framework-neutral contract core | PR #23 merge `5c2244c2c860234d0df49cf0a42ad950c6495717`, composed by PR #25 into `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | **Released/pass.** Evidence: 56/56, 65/65 invalid fixtures, 16 operations, final 4/4, inherited 19/19 + 1/1 + 13/13. Existing bytes stay immutable/readable. |
| B — Vite consumer identifier binding | Issue #7 PR #22 merge `1806b6d515f2f7a2ace2be7077af84a745ff221f`, Stage A release, exact Issue #6 fixture/Vite hashes | **Required and separately planned.** Add one closed binding schema/document plus reader/check/tests; no manifest/registry/OpenAPI/Make/UI/runner mutation. |

## Phases

| Phase | Name | Status |
|---|---|---|
| 1 | [Authority freeze and Stage A TDD RED](./phase-01-authority-freeze-and-stage-a-tdd-red.md) | Completed |
| 2 | [Stage A schemas validators and canonicalization](./phase-02-stage-a-schemas-validators-and-canonicalization.md) | Completed |
| 3 | [Stage A operations completion and guidance](./phase-03-stage-a-operations-completion-and-guidance.md) | Completed |
| 4 | [Stage A OpenAPI evidence and promotion manifest](./phase-04-stage-a-openapi-evidence-and-promotion-manifest.md) | Completed |
| 5 | [Stage A compatibility release and staged handoff](./phase-05-stage-a-compatibility-release-and-staged-handoff.md) | Completed |
| 6 | [Post-release Stage B dependency decision](./phase-06-stage-b-vite-binding-and-final-handoff.md) | Completed — Stage B required |

## Current Authority

- Exact audit/release input: `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, freshly proven as
  local HEAD, live remote integration head, and PR #25 merge commit.
- Issue #7 is closed/shipped. PR #22 merge
  `1806b6d515f2f7a2ace2be7077af84a745ff221f` and Issue #8 PR #23 merge
  `5c2244c2c860234d0df49cf0a42ad950c6495717` are ancestors of the input.
- Stage A release evidence is Issue #8 comment
  [5043195549](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549).
- The current conflict report is Issue #8 comment
  [5043335319](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043335319).
- Issue #8 owns shared lesson/lab and first-manifest contract seams. Issue #9 owns the runner and
  Issue #10 owns the portal; both consume the released shared surface read-only.
- Historical validation/readiness reports remain provenance for Stage A. Their pre-merge Stage B
  wording is superseded by the exact post-release dependency decision.

## Immutable Stage A Surface

- Contract set: `learning/contracts/learning-contract-set-v1.json`, 21 entries, byte SHA-256
  `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`.
- Version registry: `learning/contracts/learning-contract-version-registry-v1.json`, SHA-256
  `a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb`.
- Promotion manifest: `learning/manifests/promotion-trust-v1.json`, SHA-256
  `553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac`.
- Completion authority: `learning-progress-authority-v1`; browser state/bindings remain
  non-authoritative projections.
- Existing public command contract remains:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"
```

## Stage B Boundary

The fresh Stage B package is authoritative for new scope. In summary:

- create one closed `promotion-trust-vite-binding-v1` schema/document that pins the exact Stage A,
  Issue #6 fixture, and Issue #7 Vite identities and carries only the proven identifier aliases;
- add a read-only v1 binding reader and integrate it into the existing I5-03 contract check;
- add exact real-path RED fixtures/tests before behavior;
- preserve the Stage A set/registry/manifest, OpenAPI/operation matrix, completion authority,
  command activation/Make fragment, Issue #6/#7 paths, root Make, runner, portal, and data pipeline;
- publish the Stage A set hash and binding hash as two immutable components. No tracked artifact
  embeds its own future containing commit.

Generated TypeScript or portal modules are deliberately absent: Vite can import the closed JSON
binding, while any portal-local types/codegen belong to Issue #10. The Stage B binding may select
presentation field names only; it cannot validate requests, authorize actions, mutate data, or
complete progress.

## Lease, Migration, and Rollback

- The I5-03 shared-contract lease remains active and exclusive only through the bounded Stage B
  binding release. It is released after exact-head review, human approval, remote merge/release
  identity, and final handoff.
- The binding is a new v1 family with no fictional predecessor. Stage A v1 readers remain intact;
  the new reader is additive. Future binding versions retain v1 readability and explicit lossless
  migration edges.
- Rollback deselects the binding and retains Stage A, binding schema/reader, evidence, and every old
  reader. It never rewrites the Stage A manifest, falls back to an unverified alias, or deletes
  downstream/product state.

## Next Gate

Use the fresh [Stage B plan](../260722-008-stage-b-release/plan.md) as the only cook scope. Stage B
implementation remains subject to tests-first execution, fresh exact-head independent review,
repository checks, separate human exact-head approval, and a remotely observed release SHA. No
product implementation, PR merge, or cloud action is authorized by this planning commit.
