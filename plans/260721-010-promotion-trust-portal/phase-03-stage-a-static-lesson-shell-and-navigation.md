---
phase: 3
title: "Stage A released-registry semantics and portal slice"
status: pending
priority: P1
dependencies: [2]
effort: "L"
---

# Phase 3: Stage A released-registry semantics and portal slice

## Overview

Implement semantics only after the closed RED generation. First admit the exact released
descriptor registry; then deliver the Vietnamese-first catalog → module → lesson → step slice
from that single authority in React and static/no-JavaScript modes.

## Context Links

- [Released registry admission](./architecture-and-api-boundaries.md#released-descriptor-registry-admission)
- [Generic structural tests](./architecture-and-api-boundaries.md#test-only-structural-descriptors)
- [Released product truth](./verification-evidence-and-uat.md#released-product-truth)
- [Current generation](./stage-a-release-amendment.md#current-generation-evidence-publication)

## Requirements

### First semantic commit

- Bind exact integration, 85 inputs, contract-set root, promotion manifest/lesson/lab, shared Vite
  binding, released validators, protected inputs, operations, runtime, and locks.
- Build one immutable `ReleasedPortalDescriptorRegistry`; current production admits only those
  exact Issue #8 descriptor/binding/contract hashes.
- Reject unknown/extra/test-only/unhashed/draft/wrong-family/version/path/hash/field/state before
  catalog construction.
- Record the actual first semantic commit/tree. Re-run unchanged tests and prove RED families
  begin turning GREEN for authority only.

### Portal semantic commit

- Derive catalog, current routes, static documents, and React views from the one registry.
- Add the three remaining product paths: lesson navigation, module navigation, and the
  promotion-trust renderer.
- Present Vietnamese-first navigation/status/guidance and keep canonical released English IDs,
  questions, codes, and decision visibly distinct.
- Render four independent grains and limitations without causal attribution; show only
  `insufficient-evidence/no-common-grain`.
- Make `/module` presentation-only. Describe promotion-trust as one Stage A vertical slice, not
  the course or full product.
- Make run/reset/verify explanation-only with runner unavailable, execution/progress/completion
  disabled, reset not-run, and fresh evidence false.
- Provide equivalent stable facts/links with JavaScript disabled; back/forward/reload change only
  view state.

### Generic seam

- No `defaultCatalog`, `STEP_IDS`, 13-route table, promotion switch, copied fixture/schema/route,
  or duplicate alias mapping in production.
- Metamorphic tests over current release plus branded test-only structure prove generic pure
  functions. Production negative gates reject and exclude every test-only token.
- Map future #11/#12 entry only through later released contract-set/binding hashes and a later
  exact-SHA amendment; no future ID or authority is invented.

## Related Code Files

Create exactly:

```text
apps/learning-portal/src/app/lesson-navigation.jsx
apps/learning-portal/src/app/module-navigation.jsx
apps/learning-portal/src/features/promotion-trust/promotion-trust-lesson.jsx
```

Modify only scaffold paths within the final 33-path set for adapter/provider/catalog/router/
render/app/static generation/styles/release admission. Modify no test or released file.

## Tests Before

Use the closed Phase 2 RED without changing its test blobs. Specifically preserve RED for release
admission, registry authority, generic route/render, current product truth, four-grain decision,
no-JS parity, history-only state, accessibility, and prohibited capabilities.

## Implementation Steps

1. Implement production registry admission only; commit and record the first semantic tree.
2. Run exact release/runtime/lock controls plus registry mutations and production negative gates.
3. Implement catalog and route pure functions over the admitted registry.
4. Add the three remaining product paths and wire app/static renderers through the same catalog.
5. Implement Vietnamese-first current content, grain honesty, Stage A non-claims, semantic
   keyboard/focus/reflow/reduced-motion behavior, and no-JS parity.
6. Run unchanged unit/build/public/Chromium tests. Preserve raw/sanitized GREEN candidate logs as
   pending only; final current GREEN is Phase 4's final head.
7. Prove the union is 33 created paths, test blobs equal Commit 2, released bytes unchanged, and
   test-only tokens absent from build/runtime.

## Success Criteria

- [ ] First semantic commit/tree is separately bound after contemporaneous RED.
- [ ] One exact released descriptor registry drives every production consumer.
- [ ] Current production admits only released Issue #8 hashes and rejects test-only structure.
- [ ] Vietnamese-first 13-document static/React slice is honest and accessible.
- [ ] Exactly three remaining paths are added; final path union is 33/33.
- [ ] No Stage B, runner, progress, completion, container, cloud, or future-content authority exists.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Router recreates local truth | Explicit registry argument; AST/string test forbids default/step tables and switches |
| Test descriptor leaks into production | Branded test-only value, production rejection, bundle/runtime inventory scan |
| Static/React divergence | One catalog/model/route derivation plus fact-ID equivalence |
| Partial product overclaimed | Visible static-slice/not-full-product and machine-readable non-claims |

Rollback returns to the scaffold/tests head and preserves RED/current negative history. It removes
no released input or failed-review evidence.

## Next Steps

Phase 4 completes defensive semantics, final GREEN, and atomic current-generation evidence.
