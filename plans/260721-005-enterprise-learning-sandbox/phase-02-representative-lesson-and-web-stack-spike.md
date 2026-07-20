---
phase: 2
title: "Representative Lesson and Web Stack Spike"
status: pending
priority: P1
dependencies: []
effort: "M"
---

# Phase 2: Representative Lesson and Web Stack Spike

<!-- Updated: Validation Session 1 - made the scorecard, web-quality gates and failure behavior exact. -->

## Overview

Time-box three serious web stacks against the same promotion-trust lesson and real golden evidence.
Select the winner by an auditable scorecard before the portal implementation. This is a decision
spike, not a passive site or production portal.

## Context Links

- [ADR-005 scorecard](./architecture-decisions.md#adr-005-web-stack-scorecard)
- [Lesson/lab contract](./lesson-lab-contract.md)
- [Curriculum map](./curriculum-and-competency-map.md)
- Discovery source register entries S22-S24

## Requirements

- Prototype Astro + React islands, Next.js App Router, and React/Vite + typed API.
- Use identical project-owned content, interactions, architecture diagram/text alternative,
  evidence fixture, failure/remediation states and test assertions.
- Exercise the full reversible teaching sequence with progressive disclosure:
  question→controlled failure→diagnose→reset→verify→evidence→reflection; back/reload must preserve
  only committed progress and reset must be idempotent.
- Use Phase 1's real golden evidence fixture before accepting the decision; no fake business data.
- Test no-JS/static value, hydration, keyboard, screen-reader semantics, 200% zoom, reduced
  motion, reverse navigation and status/evidence interaction. No completion control may require
  scroll position, hover, animation, or client JavaScript without a semantic/static equivalent.
- Capture dependency/build mode, cold/warm start, RSS, browser JS payload, accessibility, test
  ergonomics, API/BFF fit, hosted evolution and rollback complexity.
- Complete within two implementation days. Eliminate must-pass failures before weighted scoring.
- Copy no proprietary prose, assets, layout, style or source from the inspiration site; retain a
  project-owned source/non-copy inventory in the scorecard evidence.

## Architecture

The spike is isolated under `spikes/web/`. A contract replay harness serves the real
machine-readable golden evidence and known state transitions without privileged execution. It
tests teaching interaction and BFF shape; the real runner arrives in Phase 4.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `spikes/web/shared/promotion-trust/**` | 300-500 lines | Shared content/evidence/test vectors |
| Create | `spikes/web/astro/**` | bounded prototype | Candidate |
| Create | `spikes/web/next/**` | bounded prototype | Candidate |
| Create | `spikes/web/vite/**` | bounded prototype | Candidate |
| Create | `spikes/web/tests/representative-lesson.spec.ts` | 200-300 LOC | Identical Playwright assertions |
| Create | `spikes/web/measure/**` | 150-250 LOC | Bundle/start/RSS/JS JSON |
| Create | `docs/decisions/0005-web-stack.md` | 100-180 lines | Accepted ADR |
| Create | `plans/260721-005-enterprise-learning-sandbox/reports/web-stack-scorecard.md` | 150-250 lines | Human decision evidence |
| Create | `plans/260721-005-enterprise-learning-sandbox/reports/web-stack-scorecard.json` | 100-180 lines | Machine must-gates/scores/artifact hashes |
| Modify | `.gitignore` / selected lock allow-list | small | Reproducible dependencies |

## Interface Checklist

- [ ] identical `LessonViewModel`, lab-state and evidence fixtures
- [ ] diagram text alternative and definition/evidence disclosures
- [ ] BFF contract adapter matching planned OpenAPI
- [ ] shared Playwright selectors based on roles/labels, not framework internals
- [ ] measurement JSON schema and normalized environment metadata
- [ ] controlled-vs-environmental failure copy, progressive-disclosure checkpoints, reset oracle
- [ ] source/non-copy inventory and identical role/label assertion manifest

## Dependency Map

- Can start with Phase 1 in a separate worktree/path.
- Final ADR depends on Phase 1 real evidence fixture and draft lesson contract.
- Blocks Phase 5. Feeds authoring decisions in Phase 3.

## Test Scenario Matrix

| Priority | Scenario | Assertion |
|---|---|---|
| Critical | Complete representative lesson | Every required act/state/evidence view is renderable |
| High | Keyboard/reduced motion/static | No content/control/completion loss |
| High | Controlled failure/remediation | Clear state, evidence, next action; no false completion |
| High | Reverse navigation/reload | UI state is reversible; committed progress remains correct |
| High | BFF/evidence contract | Typed errors and real fixture integrity |
| Medium | Performance | Comparable bundle/start/RSS/JS results |

## Tests Before

Write the shared browser/a11y/contract suite and intentionally incomplete candidate pages so each
fails the same assertions.

## Refactor

Not applicable to product code. Keep candidates isolated and share only content/test vectors.

## Tests After

Run identical suite and measurements for each candidate on the same machine/tool versions. Verify
the selected candidate again after its lockfile is recreated from a clean install.

## Regression Gate

```bash
make web-spike-scorecard-check
# Candidate-specific clean install, unit, a11y and Playwright commands are recorded in the report.
```

The target exits non-zero for missing candidate command/version/artifact hashes, unequal lesson
assertions, any must-pass failure, missing non-copy inventory, or a declared winner without a
complete weighted score. That leaves ADR-005 `Proposed` and blocks Phase 5.

## Implementation Steps

1. Freeze representative lesson view model and real Phase 1 evidence fixture.
2. Write common browser/a11y/measurement tests.
3. Build the smallest complete candidate in each stack; stop at the time box.
4. Record pass/fail must-gates and normalized measurements.
5. Score using ADR-005 weights and tie rule.
6. Commit the winning ADR, chosen build/runtime mode and lock strategy.
7. Delete or archive non-winning executable spikes; retain scorecard, tests and content contract.

## Success Criteria

- [ ] All three serious candidates evaluated with identical content/data/tests.
- [ ] Winner passes every must-pass and has reproducible measurements.
- [ ] ADR-005 records decision, consequences, rejected alternatives and rollback.
- [ ] Phase 5 can begin without reopening framework choice.
- [ ] No proprietary content copied.

## Risk, Security, and Rollback

Framework familiarity can bias results; shared assertions and measured evidence constrain it.
Prototype servers bind loopback and never execute lab commands. Rollback deletes spike code and
reopens ADR-005 while retaining the framework-neutral lesson/contract/test fixtures.

## Next Steps

Phase 3 finalizes contracts using the winning authoring/runtime constraints; Phase 5 builds only
the selected portal.
