---
phase: 5
title: "Runnable Portal Vertical Slice"
status: pending
priority: P1
dependencies: [2, 3, 4]
effort: "L"
---

# Phase 5: Runnable Portal Vertical Slice

<!-- Updated: Validation Session 1 - defined the first usable command and expansion gate. -->

## Overview

Deliver the first runnable product: one accessible, credential-free promotion-trust learning
journey using the selected web stack, the real isolated runner, existing retail data products,
deterministic reset/verify and evidence.

## Context Links

- [First representative journey](./lesson-lab-contract.md#first-representative-journey)
- [First journey rubric](./curriculum-and-competency-map.md#first-journey-competency-rubric)
- Accepted ADR-005 from Phase 2
- Released contracts from Phase 3 and runner API from Phase 4

## Requirements

- Portal is the selected content-capable modular monolith: lesson rendering, progress/evidence
  state, BFF, status/deep-link adapters and local persistence.
- Journey covers stakeholder/business question, capability/FR/NFR, C4/dynamic view, raw data,
  model/lineage, controlled DQ/metric failure, decision/trade-off, reset, verified four-mart data
  product, evidence and reflection.
- No cloud/model credential; bounded local core only. Rill is a deep link/enhancement, not a
  completion dependency.
- External tool absent/starting/ready/error states use shared vocabulary and useful action.
- Static/reduced-motion route preserves all facts and controls; progress is verifier-driven.
- Browser never sees runner secret and cannot request arbitrary command/paths.
- Local state and evidence survive browser reload; reset does not forge or delete prior evidence.
- `make learn LESSON=promotion-trust` is the one stable future start command. It starts loopback
  portal/private runner/core only, prints URL/evidence/teardown instructions, exits non-zero with
  remediation before mutation on unsafe prerequisites, and requires no optional profile.

## Architecture

The browser talks only to the portal. Server-side BFF loads validated content, owns local
progress/evidence repository and calls the private runner. Initial local state may use SQLite plus
filesystem evidence through a Repository interface; migrations and hosted adapter seam are
versioned. Do not introduce a database/service beyond what this slice needs.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `apps/learning-portal/**` in winning stack | 2,000-3,500 LOC | Portal/BFF |
| Create | `apps/learning-portal/src/features/lessons/**` | 600-900 LOC | Narrative/views |
| Create | `apps/learning-portal/src/features/labs/**` | 700-1,000 LOC | State/actions |
| Create | `apps/learning-portal/src/features/evidence/**` | 350-550 LOC | Evidence display/verify |
| Create | `apps/learning-portal/src/server/runner-client/**` | 250-400 LOC | Private BFF boundary |
| Create | `apps/learning-portal/tests/{unit,a11y,e2e,visual}/**` | 1,200-1,800 LOC | Release gates |
| Create | `apps/learning-portal/public/architecture/**` generated | generated | Rendered views/text |
| Modify | root package scripts/lock allow-list and `Makefile` | small | Start/test commands |

## Interface Checklist

- [ ] `LessonRepository`, `ProgressRepository`, `EvidenceRepository`
- [ ] server-only `RunnerClient`
- [ ] shared `ToolStatus`: absent/starting/ready/error/degraded
- [ ] verifier-driven completion selector
- [ ] deep-link adapter with safe target/status
- [ ] architecture renderer/text alternative component
- [ ] motion/static preference persisted without affecting completion

## Dependency Map

- Requires accepted stack, contracts and runner.
- Blocks local resource measurement/release; curriculum/data phases may extend after slice.
- AWS/AI decisions are not dependencies.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Complete novice journey | Real runner/evidence; all critical assertions pass |
| Critical | Forge URL/state/evidence | No completion; typed error/remediation |
| High | Runner/Rill unavailable | Lesson and architecture remain usable; status/action clear |
| High | Reload/back/reverse | Committed progress correct; no duplicate operation |
| High | Keyboard/screen reader/200%/reduced motion | Full completion without hidden control/content |
| High | Controlled vs environmental failure | Distinct language/state; no blame or false progress |
| Medium | Challenge route | Instruction can skip; verifier cannot |

## Tests Before

Write component contract tests, reducer/state tests, a11y checks and complete Playwright journey
against failing route shells. Use roles/labels and real Phase 4 runner fixture.

## Refactor

Only portal-local abstractions. Do not refactor data services while composing the UI. Route any
contract change through shared-core versioning.

## Tests After

Unit, integration, axe, browser E2E, visual baselines, manual keyboard/screen-reader/zoom and
reduced-motion/static audit. Run with optional tools absent and network-disabled after install.

## Regression Gate

```bash
make portal-test
make portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
make runner-security-test
```

## Implementation Steps

1. Lock winning dependencies/build mode and create portal shell/IA from validated lesson manifest.
2. Implement architecture/narrative/static-equivalent components.
3. Implement BFF runner client and typed lab operation states.
4. Add local progress/evidence repositories and migrations.
5. Connect real promotion-trust starter, controlled failure, decision, reset, typed configuration,
   verifier and evidence flow.
6. Add Rill/OpenMetadata/Airflow status/deep-link vocabulary without making them mandatory.
7. Complete automated and manual accessibility/browser/visual reviews.
8. Record exact resource/start/e2e evidence for Phase 8.

## Success Criteria

- [ ] `make learn LESSON=promotion-trust` starts portal/runner and one complete journey works;
  `make local-journey-e2e` proves it from a clean workspace.
- [ ] Completion requires real verification and valid evidence.
- [ ] No AWS/model credential or optional heavy service is required.
- [ ] Full journey passes keyboard/static/reduced-motion route and manual accessibility review.
- [ ] Direct runner access/arbitrary execution is impossible from browser.
- [ ] Existing data spine and expert commands remain intact.

## Risk, Security, and Rollback

Main risks are content-shell drift, client-side trust and accessibility regressions. Browser E2E
must exercise the real runner and evidence, while all authority stays server-side. Rollback
feature-flags interactive execution and serves the versioned static lesson; runner and data spine
can be disabled independently.

## Next Steps

Expand curriculum/data labs only after this slice is runnable; measure portal with each admitted
profile in Phase 8.
