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

Deliver the honest Stage A learner surface: business question, exact four-mart grain context,
controlled-failure explanation, canonical decision, reset explanation, baseline evidence label,
read-only reversible navigation, and static/no-JavaScript equivalence. Nothing runs or completes.

## Context Links

- [Architecture: routing and static path](./architecture-and-api-boundaries.md#routing-history-and-reset)
- [Issue #6 data truth](./requirements-and-risk-traceability.md#issue-6-data-truth)
- [Accessibility/browser scope](./verification-evidence-and-uat.md#practical-test-portfolio)
- [Threat model](./threat-model-and-security.md)

## Requirements

### Functional

- Render the exact released stakeholder/business question and all four independent grains.
- Show each mart's scope, filter, calculation, numerator/denominator, and limitation.
- Explain the expected `PROMOTION_HEADLINE_INSUFFICIENT` controlled failure and exact
  `insufficient-evidence / no-common-grain` conclusion.
- Provide back/forward/reload-safe read-only steps and an equivalent static page.
- Label Issue #6 evidence as a retained baseline fixture, never a fresh run.

### Non-functional

- Semantic headings/landmarks/table/list, visible focus, logical keyboard order, narrow reflow,
  no color-only meaning, reduced motion, and useful non-flooding status announcements.
- No JavaScript, animation, hover, scrolling, or optional tool is required to understand facts.
- No copied proprietary prose/assets/layout/style from the reference experience.

## Architecture

`portal-router.ts` validates the released lesson/step IDs and changes only presentation state.
The client and `promotion-trust-document.ts` share the same closed view model.
`render-static-fallback.mjs` produces the build output from that model. Static and interactive
fact IDs are compared in tests.

## Related Code Files

- Create: `apps/learning-portal/src/client/app/portal-router.ts`
- Create: `apps/learning-portal/src/client/app/route-state.ts`
- Create: `apps/learning-portal/src/client/features/promotion-trust/business-question.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/four-mart-context.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/controlled-failure.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/decision-panel.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/reset-panel.tsx`
- Create: `apps/learning-portal/src/client/styles/portal.css`
- Create: `apps/learning-portal/src/static/promotion-trust-document.ts`
- Create: `apps/learning-portal/scripts/render-static-fallback.mjs`
- Create: `apps/learning-portal/tests/unit/portal-router.test.ts`
- Create: `apps/learning-portal/tests/contracts/promotion-trust-view-model.test.ts`
- Create: `apps/learning-portal/tests/accessibility/promotion-trust-a11y.test.tsx`
- Create: `apps/learning-portal/tests/e2e/promotion-trust-static.spec.ts`
- Delete: none

## Tests Before

1. Add PTP-RED-A-010..016 for facts, no attribution, non-completion, history, no-JS, status, focus,
   reduced motion, and overflow.
2. Add explicit mutations for a fifth source, changed grain, causal wording, altered decision,
   raw row/identifier, false fresh-evidence label, enabled Run/Complete button, and missing static
   fact.
3. Start a JavaScript-disabled Chromium test and static parser test before implementing output.

## Refactor

Use stable released fact/step IDs rather than copying prose into tests. Share formatting helpers
only where interactive/static equivalence requires them. No broad content engine or animation
framework.

## Tests After

- Interactive and static modes expose identical required fact IDs and canonical outcome.
- Back/forward/reload changes view only and makes zero mutation requests.
- Stage A controls are links/navigation only; runner actions are unavailable with useful text.
- Desktop/narrow, keyboard/focus, reduced-motion, live-region, and no-overflow checks pass.
- No-JS Chromium and parser both understand the lesson without external services.

## Regression Gate

Run focused component/router/contract/accessibility/no-JS tests, the exact #7 locked Chromium,
production build twice, static-output digest comparison, axe Critical/Serious gate, package/bundle
scans, and `git diff --check`.

## Implementation Steps

1. Retain failing fact, mutation, history, accessibility, and no-JS assertions.
2. Map the exact released #8 lesson and Issue #6 baseline evidence into the closed view model.
3. Implement semantic business-question and four-mart context components.
4. Implement controlled-versus-environmental failure and canonical decision presentation.
5. Implement read-only router/history/reload behavior with validated released step IDs.
6. Generate the static document and no-JavaScript redirect/link from the same model.
7. Add responsive/focus/reduced-motion/live-region styling without motion-only meaning.
8. Run regression/equivalence checks and record Stage A evidence.

## Success Criteria

- [ ] The exact business question and all four honest grains are understandable in both modes.
- [ ] The only v1 decision shown is `insufficient-evidence / no-common-grain`.
- [ ] Baseline fixture is never presented as fresh run/completion evidence.
- [ ] Browser history/reload cannot replay or manufacture state.
- [ ] One locked Chromium desktop+narrow and no-JS/static checks pass.
- [ ] No runner, completion, cloud, Docker, optional profile, or external tool is required.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Static copy drifts from React | Single validated model + stable fact-ID equivalence |
| Grain cards imply joinability | Explicit independent-grain table and limitation adjacent to values |
| Back navigation repeats action later | Router owns view only; mutation state excluded |
| Animation hides content | Static DOM first; reduced motion; no animation dependency |

## Security Considerations

Escape every content/error field, allow only approved links, forbid raw HTML/MDX execution, and
apply the same CSP to interactive/static output. Fixture bytes remain read-only and are not
embedded with private provenance.

## Next Steps

Phase 4 runs the bounded Stage A verification/handoff without claiming the real journey.
