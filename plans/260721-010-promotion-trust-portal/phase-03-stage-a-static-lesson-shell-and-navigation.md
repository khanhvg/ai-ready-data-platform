---
phase: 3
title: "Stage A static lesson shell and navigation"
status: pending
priority: P1
dependencies: [2]
effort: "M"
---

# Phase 3: Stage A static lesson shell and navigation

## Overview

Deliver the useful learning surface: a reusable Vietnamese-first catalog → module → lesson →
narrative-step shell whose first content is the released promotion-trust vertical slice. Render
the same facts in static/no-JavaScript and React modes, with reversible read-only navigation and
explicit non-execution/non-completion semantics.

## Context Links

- [PortalCatalog seams](./architecture-and-api-boundaries.md#portalcatalog-and-extension-seams)
- [Protected lesson truth](./requirements-and-risk-traceability.md#protected-data-and-contract-truth)
- [No-JS verification](./verification-evidence-and-uat.md#no-javascript-and-static-equivalence)
- [Stage A scenarios](./stage-a-release-amendment.md#requirements-and-scenario-catalogue)

## Requirements

### Functional

- Derive one module/lesson entry from released `promotion-trust-v1`; never call it the full course.
- Render the stakeholder question, four independent grains/limitations, released controlled
  failure, and `insufficient-evidence / no-common-grain` without causal attribution.
- Provide semantic catalog/module/lesson/step navigation with back/forward/reload view-only state.
- Render explanation-only run/reset/verify narrative steps with runner unavailable.
- Generate all admitted static routes from the same safe model.

### Non-functional

- No hand-maintained duplicate lesson, raw HTML/MDX, copied #7 lesson contract, or copied fixture.
- Semantic landmarks/headings/lists, visible focus, 360px reflow, reduced motion, live status.
- #11/#12 can later add released manifests through provider/catalog seams without redesign;
  no future content is invented now.

## Authorized Files

Create only:

```text
apps/learning-portal/scripts/generate-static-routes.mjs
apps/learning-portal/src/app/lesson-navigation.jsx
apps/learning-portal/src/app/module-navigation.jsx
apps/learning-portal/src/catalog/module-catalog.mjs
apps/learning-portal/src/catalog/released-module-provider.mjs
apps/learning-portal/src/features/promotion-trust/promotion-trust-lesson.jsx
apps/learning-portal/src/render/static-document.mjs
apps/learning-portal/src/routing/portal-router.mjs
apps/learning-portal/tests/unit/module-catalog.test.mjs
apps/learning-portal/tests/unit/portal-router.test.mjs
apps/learning-portal/tests/unit/render.test.mjs
```

## Tests Before

1. Retain PTP-RED-A-010..016 through the real provider/catalog/router/render paths.
2. Retain PTP-RED-A-020/021 for unknown descriptors and static/React disagreement.
3. Mutate a fifth source, grain, causal wording, decision, raw field, false fresh-evidence label,
   enabled action, missing static fact, and route/history behavior.
4. Start built-output parser and JavaScript-disabled browser assertions before output exists.

## Tests After and Regression

- Provider/catalog accept exact registered released descriptors only.
- Promotion-trust is visibly one vertical slice in a reusable foundation-to-mid shell.
- Static and React stable fact IDs, values, ordering, routes, and escaping agree.
- Back/forward/reload make zero mutation/network/storage effects.
- Four grains/limitations and canonical decision are honest in every admitted route.
- Unit/adapter/render/router/build/no-JS/axe/diff checks stay green.

## Implementation Steps

1. Write provider/catalog/router/render RED cases and mutation fixtures in memory.
2. Implement released module provider and ordered catalog over the closed safe model.
3. Implement generic module/lesson navigation and read-only router.
4. Implement promotion-trust presentation as a feature renderer, not a portal-wide switch.
5. Implement deterministic static document and route generation from the same model.
6. Prove Vietnamese-first semantics, canonical English values, focus/reflow/reduced motion.
7. Run equivalence/history/negative regression and verify only these 11 paths are added.

## Success Criteria

- [ ] One honest promotion-trust vertical slice is useful with runner absent.
- [ ] Shell/provider/router seams admit later released content without redesign.
- [ ] Static and React modes expose equivalent released facts and navigation.
- [ ] Navigation cannot execute, reset, verify, progress, evidence, or complete.
- [ ] Only the 11 authorized files are added.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Promotion lesson hard-coded as whole course | generic provider/catalog/router plus copy tests |
| Static copy drifts | one safe model and fact-ID equivalence |
| Four cards imply joinability | adjacent independent-grain limitations and attribution negatives |
| Future seam becomes permissive plugin system | exact registered release descriptors only |

Rollback removes only these 11 unmerged additions.

## Next Steps

Phase 4 adds the bounded static server lifecycle, Chromium journey, review artifacts, and Make
handoff.
