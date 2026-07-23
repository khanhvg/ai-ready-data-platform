---
phase: 4
title: "Stage C Portal Publication and Real Journey"
status: pending
priority: P1
dependencies: [1, 2, 3]
externalDependencies: [issue-10-merged-runner-backed-stage-b]
effort: "unresolved until exact Stage C amendment"
---

# Phase 4: Stage C Portal Publication and Real Journey

## Context links

- [Plan](./plan.md)
- [Requirements traceability](./requirements-traceability.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)

## Overview

Issue #10 static Stage A is merged at `041d4ca866e927a331e159fdf8216838b481a595`, nhưng Stage C
vẫn blocked. Chỉ sau passing merged runner-backed Issue #10 Stage B mới publish Stage A/B labs
through exact released
content/API/renderer seams and run real learner journeys. Đây là stage duy nhất có thể claim
complete learner experience; content/static/runner-only evidence không đủ.

## Requirements

### Functional

- Map released lab contracts and #9 runner operations into #10 renderer/API without inventing
  routes, fields, command IDs or component paths.
- Foundation→mid journey exposes prerequisite, starter, task, controlled failure, hints, verify,
  evidence, reset, solution and reflection in Vietnamese-first order.
- Browser triggers only released API/runner authority; no direct privileged action.
- Controlled, environmental and unexpected failures remain distinct; optional unavailable state
  gives remediation and cannot complete that lab.
- Completion requires fresh live verifier + evidence integrity + legal state transitions.
- Back/forward/reload/reset/replay cannot duplicate effects or corrupt progress/evidence.

### Non-functional

- Preserve #10 accessibility/static/keyboard/reduced-motion behavior and exact blast radius.
- Core journey serial on 16GB without Docker/cloud. Service-backed journey publishes as verified
  only with real local service evidence; otherwise visible honest unavailable state.
- Portal/runner files outside released extension points are protected.

## Architecture

Use exact merged #10 renderer/API paths, operations and test commands recorded by Stage C
amendment. Portal is presentation/orchestration client; #9 runner owns privileged local execution,
workspace and evidence. Completion reads fresh verified evidence rather than browser state,
solution visibility, reflection text or file presence.

## User-flow matrix

| Flow | Required result | Stable IDs |
|---|---|---|
| Foundation deterministic data | Learner diagnoses grain/hash/anomaly mismatch, resets, verifies | `DL-ING-001`, `DL-DQ-001`, `DL-PUB-001` |
| Junior modeling/metric | Learner traces layer/grain and fixes invalid weighting | `DL-MOD-001`, `DL-MET-001/002`, `DL-PUB-001` |
| Junior orchestration | Retry/timeout/backpressure failure visible with typed recovery | `DL-ORCH-001/002/003/004` |
| Mid release/Iceberg | Learner diagnoses crash/conflict/orphan without mixed current release | `DL-REL-*`, `DL-ICE-*` |
| Mid governance | Learner reconciles exact namespace, preserves collision/unmanaged entities | `DL-OM-*` |
| Accessibility/replay | Keyboard/static path completes only from fresh evidence; replay/tamper denies | `DL-LAB-002`, `DL-EVD-002`, `DL-PUB-002` |

## Related code files

- Modify/create after amendment: exact #10 released renderer/API/content registration paths only.
- Consume read-only: exact #8 contracts and #9 runner registry/API.
- Preserve: root Makefile, shared contracts/views, golden semantics, portal/runner internals outside
  extension points.
- Exact current Stage C implementation path/command list: empty.

## Implementation steps

1. Amend exact passing merged runner-backed #10 Stage B SHA, renderer/API/content extension points,
   accessibility/E2E commands and blast radius; verify #8/#9 ancestry; run one Standard-lane
   combined dependency/readiness pass.
2. Add publication REDs: contract-valid lab absent from released registry/renderer, privileged
   browser bypass attempt, and optional-service unavailable state incorrectly marked complete.
3. Register lab content through the exact released extension path; no shared contract/API change
   without a new serialized lease.
4. Connect released runner operations and evidence views; keep browser passive and typed.
5. Implement progression/hint/solution/reflection rules so only live verification completes.
6. Run foundation→mid real journeys including reset, reload, back/forward, timeout, duplicate,
   crash, unavailable, tamper and replay states.
7. Run released #10 accessibility/static/browser suite plus exact #6/#8/#9/#10 blast radius.
8. Retain Stage C evidence and mark only fully verified journeys complete.
9. Use one implementer/reviewer/tester/PR context with zero Critical/Important findings, fresh real
   browser+runner tests, PR/CI, merge and post-merge journey smoke.

## Tests before

- Stage A/B stable suites pass on exact amended dependency SHAs.
- REDs exercise actual released #10 integration points and browser flow; no DOM-only completion
  shortcut or fake runner response.

## Refactor

Reuse #10 renderer components and state patterns. Add no bespoke data-lab renderer unless the
released generic contract cannot express a required field and a separate contract amendment is
approved.

## Tests after

- Real browser + runner + evidence journeys for all published lab levels.
- Keyboard/static/reduced-motion/reload/back-forward/accessibility blast radius from #10.
- Browser authority, CSRF/origin/object-ID and direct-command negative tests from released #9/#10.
- Honest optional service unavailable/error/ready transitions.

## Success criteria

- [ ] All published labs render from released contracts and use released runner authority.
- [ ] Complete learner experience claim is backed by passing real journey and valid evidence.
- [ ] No browser direct privileged action or solution/reflection completion shortcut exists.
- [ ] Optional unavailable states are honest, accessible and non-completing for affected lab.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Guessed renderer/API path | Forked portal contract | Exact #10 amendment only |
| UI state sets completion | Evidence bypass | Fresh server/runner evidence authority |
| Browser gains local privilege | S3 boundary break | Released API/registry only; negative bypass tests |
| Service-dependent lab shown green without service | False learning outcome | Typed unavailable state + no completion |

## Security considerations

No command strings, raw SQL, arbitrary refs/paths/env or service credentials reach browser.
Evidence is sanitized and object-bound. All S3 portal/runner blast-radius tests released by #9/#10
are mandatory.

## Next steps

Phase 5 consolidates exact evidence, rollback, focused review/test evidence and PR handoff.
