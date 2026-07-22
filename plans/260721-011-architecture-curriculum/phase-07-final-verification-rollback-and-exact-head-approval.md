---
phase: 7
title: "Final verification rollback and exact-head approval"
status: pending
priority: P1
dependencies: [6]
effort: "Blocked final release gate"
---

# Phase 7: Final verification rollback and exact-head approval

## Context Links

- [Dependency and release gates](./dependency-and-release-gates.md)
- [Verification and protected assets](./verification-evidence-and-protected-assets.md)

## Overview

Future final gate after both stages exist. Reproduce exact-head tests/evidence in a fresh checkout,
rehearse ownership-scoped rollback, obtain independent implementation review and repository-
authorized human exact-head approval, then follow separate merge/release authority. The current v4
plan performs and authorizes none of these actions.

## Requirements

- Bind exact pushed candidate, release dependencies, tools, fixtures, raw evidence, and review.
- Re-prove all protected/released/unrelated bytes and both stage boundaries.
- Treat approval, merge, and release as distinct explicit authorities.

## Files

None authorized while Phase 6 is blocked.

## Implementation Steps

1. Remain blocked.
2. If both stages later pass, create a new exact final-gate amendment and evidence plan.

## Tests and Validation

No current final-gate command may run.

## Acceptance Criteria

- [ ] Both stages are released and independently reviewed at exact heads.
- [ ] Exact rollback, approval, merge, and release authorities are separately present.

## Risks and Rollback

Never infer human approval or merge authority from tests, labels, comments, or author evidence.
Current rollback is no action.
