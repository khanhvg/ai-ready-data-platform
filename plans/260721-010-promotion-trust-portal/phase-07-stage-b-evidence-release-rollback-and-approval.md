---
phase: 7
title: "Stage B evidence release rollback and review"
status: pending
priority: P1
dependencies: [6]
effort: "S"
---

# Phase 7: Stage B Evidence, Rollback, and Review

## Overview

Converge the Phase 6 implementation at one exact head under Lane S. This phase adds no product
scope and no new path/command authority.

## Requirements

- Run all 15 Phase 6 commands unchanged at the final head.
- Retain bounded evidence for the controlled failure, exact runner results, immutable evidence
  verification, reset, completion, browser desktop+narrow/keyboard/axe/no-JS, and cleanup.
- Run authenticated `learn-down` twice and prove public/control ports, owned child, pending record,
  and runner containers are absent while progress/evidence remain.
- Rehearse evidence-preserving rollback to the shipped Stage A static/no-JS portal.
- Run one focused code review. Critical and Important findings must be zero.
- Do not require a separate red-team, security-audit, second-review, or human-approval ceremony.
  Functional security/safety tests remain mandatory product behavior.

## Exact Scope

- Writable paths: the same 18 Phase 6 paths only.
- Commands: the same 15 Phase 6 command shapes only.
- Dependencies: portal merge `041d4ca…`, runner/integration `671201f…`, implementation base
  `671201f…`.
- Protected: runner/shared contracts/root Make/golden data/README/docs/CI/container/cloud.

## Evidence Gate

The final retained record must bind:

1. tested implementation commit/tree;
2. portal Stage A merge/reviewed head;
3. runner merge/reviewed head/image digest;
4. exact eight operation IDs and validated result/evidence digests;
5. `progress-v1`, `learning-evidence-v1`, and completion contract identities;
6. controlled-failure and learner-fix facts;
7. successful verify, evidence publication, reset, and one completion;
8. desktop/narrow Chrome identity, keyboard/focus, axe and no-JS results;
9. lifecycle/process/port/container cleanup and rollback result;
10. focused review result Critical=0 and Important=0.

Retained evidence excludes tokens, cookies, CSRF, runner control records, absolute private paths,
raw environment, unbounded logs, raw records, source maps, and cloud/model credentials.

## Regression Gate

Run the Phase 6 command table, followed by:

- exact-path diff equals 18;
- runner/shared/root-Make/golden protected trees unchanged;
- `git diff --check`;
- high-confidence credential/private-path scan;
- ignored runtime state absent from the tracked/staged set;
- local head = tracking head = fresh live head;
- clean worktree.

## Acceptance Criteria

- [ ] One real local journey reaches controlled failure, learner fix, verify, immutable evidence,
  truthful reset, and one completion.
- [ ] All functional safety, accessibility, no-JS, persistence, idempotency, cleanup, and
  clean-checkout tests pass.
- [ ] Rollback is scoped, idempotent, evidence-preserving, and restores truthful Stage A.
- [ ] Final review has zero Critical and zero Important findings.
- [ ] No extra ceremony, product scope, cloud action, or protected-path change is introduced.

## Next Steps

After a final green head, use the separately authorized Git workflow for PR/merge. Issue #10
closes only after Stage B merges and post-merge smoke passes.
