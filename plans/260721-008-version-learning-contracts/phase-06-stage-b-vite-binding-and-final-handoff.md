---
phase: 6
title: "Post-release Stage B dependency decision"
status: completed
priority: P1
dependencies: [5]
stage: "post-release-audit"
gateStatus: "stage-b-required"
cookable: false
implementationAllowList: []
stageBPlan: "../260722-008-stage-b-release/plan.md"
requirementAudit: "../260722-008-stage-b-release/audit/post-stage-a-requirement-audit.md"
---

# Phase 6: Post-Release Stage B Dependency Decision

## Context Links

- [Current stage decision](./plan.md#stage-decision)
- [Fresh Stage B release plan](../260722-008-stage-b-release/plan.md)
- [Post-Stage-A requirement audit](../260722-008-stage-b-release/audit/post-stage-a-requirement-audit.md)
- [Issue #7 Accepted Vite ADR](../../docs/decisions/0005-web-stack.md)
- [Stage A release evidence](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549)

## Overview

This phase was a conditional dependency checkpoint. Issue #7 and Stage A now coexist at exact
release integration `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, so the condition was evaluated
against real released bytes rather than historical prose.

The result is **Stage B required**. Stage A manifest
`learning/manifests/promotion-trust-v1.json` names fulfillment/returns keys as `region` and
`category`; the hash-pinned Issue #6 evidence and released Issue #7 Vite contract use
`region_name` and `category_name`. Stage A uses grain ID `dq`; Vite presents `data-quality`.
Neither release defines those aliases. The released Node contract suite passes its own exact
fixture/Vite identities, proving this is a cross-release seam rather than drift inside Issue #7.

## Decision and Scope Handoff

This completed phase authorizes no product change itself. It closes the old placeholder by handing
the concrete mismatch to the fresh [Stage B plan](../260722-008-stage-b-release/plan.md), whose
allow-list is exact and independently validated by CK.

The bounded resolution is one additive, closed, hash-bound Vite consumer binding plus its v1
reader/check/tests. It maps only:

- `promotion` → `promotion`, `promo_name` → `promo_name`, `channel` → `channel`;
- `fulfillment` → `fulfillment`, `carrier` → `carrier`, `region` → `region_name`;
- `returns` → `returns`, `reason` → `reason`, `category` → `category_name`,
  `region` → `region_name`;
- `dq` → `data-quality`, `scenario` → `scenario`.

The mapping is total, ordered, one-to-one, and value-preserving. It is derived from the exact
Stage A source order and the exact Issue #6/Vite order; it performs no coercion, defaulting,
aggregation, row/value transformation, or semantic join.

## Protected Boundary

- Stage A schemas, manifest, set, registry, OpenAPI, operation matrix, completion reconciliation,
  command activation, evidence, and Make fragment remain immutable.
- Issue #6 fixtures/data contracts and all Issue #7 ADR/Vite source/lock/Make bytes are read-only.
- Root Make, portal, runner, data pipeline, AWS, Terraform, and cloud paths are excluded.
- No TypeScript, portal module, runner adapter, generated data, browser bundle, or new public
  command is Issue #8-owned.
- Browser use is projection-only. Server-side Stage A validation and
  `learning-progress-authority-v1` remain the only validation/completion authority.

## Audit Assertions

- [x] `I8B-AUDIT-ANCESTRY-001`: PR #22 and PR #23 merge SHAs are ancestors of the exact input.
- [x] `I8B-AUDIT-MISMATCH-002`: the exact two key aliases and one grain-ID alias are absent from
  both released contract sets.
- [x] `I8B-AUDIT-OWNER-003`: Issue #8 owns the shared first-manifest seam; Issue #10 cannot repair
  it in portal-owned paths.
- [x] `I8B-AUDIT-BOUNDARY-004`: additive binding is sufficient; no Stage A rewrite, OpenAPI change,
  registry mutation, Make change, UI, or runner behavior is needed.
- [x] `I8B-AUDIT-S3-005`: the plan carries only public identifiers/hashes and no record values,
  credentials, private paths, cloud action, or destructive migration.

## Implementation Steps

1. Verify exact input, live refs, issue/PR/comment state, released hashes, ancestry, clean tree, and
   exclusive shared-contract lease.
2. Reproduce and freeze the real-path mismatch and all security/compatibility negatives before
   adding a binding reader or document.
3. Cook only the new Stage B plan in its serialized order and exact allow-list.
4. Preserve Stage A/readers and run the full Issue #8, Issue #6, and focused Issue #7 Node blast
   radius at one exact clean committed head.
5. Require fresh exact-head independent implementation review, repository checks, and separate
   human exact-head approval before merge/release; then publish the binding hash and remote release
   SHA externally.

## Success Criteria

- [x] The dependency is evaluated from released authority rather than presumed.
- [x] The incompatibility is concrete, bounded, and reproducible.
- [x] Exact ownership proves the binding is Issue #8 work and portal/runner work is excluded.
- [x] A fresh tests-first Stage B plan names every output/input path, command, hash, boundary,
  rollback rule, and human gate without inventing a future SHA.

## Next Steps

Proceed only through `plans/260722-008-stage-b-release/plan.md`. The old Phase 6 has no independent
implementation allow-list and is not a competing cook authority.
