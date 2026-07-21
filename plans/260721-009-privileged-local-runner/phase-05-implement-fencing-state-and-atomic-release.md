---
phase: 5
title: "Implement fencing state and atomic release"
status: pending
priority: P1
dependencies: [4]
effort: "2 implementation days"
---

# Phase 5: Implement Fencing, State, and Atomic Release

## Overview

Add the shared learner-namespace mutation fence, released state/idempotency behavior, append-only
audit, crash reconciliation, atomic generation reset and exact eleven-asset local release pointer.
Prove cross-entrypoint safety while preserving current expert Make/Airflow paths.

## Context Links

- [Workspace, fencing, state and audit](./implementation-boundary-and-design.md#workspace-fencing-state-and-audit)
- [Atomic eleven-asset release](./implementation-boundary-and-design.md#atomic-eleven-asset-release)
- [RUN-FEN/STA/AUD/REL](./requirements-risk-threat-traceability.md#requirement-crosswalk)

## Requirements

- OS lock FD plus monotonic SQLite fence epoch spans every learner mutation.
- Released state transitions and canonical request idempotency survive restart.
- Audit events are insert-only, ordered, hash-chained and redacted.
- Expert namespace remains distinct; learner path requires inherited fence capability.
- Reset atomically selects a fresh generation and preserves immutable evidence.
- Export publishes exactly eleven complete assets through one atomic current pointer.

## Architecture

```text
workspace lease FD + fence epoch
  -> operation/idempotency transaction
  -> append-only audit transition
  -> contained command and staged artifacts
  -> compare fence/owner/request digest
  -> state/result or complete manifest commit
  -> atomic generation/current-release pointer
  -> startup reconciliation on crash
```

## Related Code Files

- Create: `apps/lab-runner/src/lab_runner/{fence,state,release,evidence}.py`
- Create: `apps/lab-runner/tests/unit/test_{fence,state,idempotency,audit,release}.py`
- Create: `apps/lab-runner/tests/race/test_{fencing,cross_entrypoint,release_atomicity,crash_recovery,idempotency}.py`
- Extend: `apps/lab-runner/src/lab_runner/{service,workspace,process}.py`
- Extend: app-owned fault fixtures and bounded pipeline integration tests
- Consume read-only: `contracts/data/curated-release-manifest.schema.json` and exact curated list
- Modify/Delete: none outside `apps/lab-runner/**`

## Tests Before

Use `RED-XRACE`, `RED-CRASH`, `RED-IDEMP`, and `RED-REL` suites unchanged. Every commit boundary
must have a deterministic barrier/fault point and an old-or-new-complete oracle.

## Implementation Steps

1. Create one private SQLite database per workspace with `FULL` synchronization, foreign keys,
   released transition version, operation/idempotency projection, monotonic fence epoch and audit
   tables. Add triggers that reject audit UPDATE/DELETE.
2. Acquire an advisory OS lock on a descriptor-verified lease file, then increment fence epoch in a
   transaction. Carry FD identity + epoch through every child/result/pointer commit.
3. Implement compare-and-transition and idempotency begin/complete/reconcile: same key/request
   returns original operation/result; changed request conflicts; stale fence cannot commit.
4. Append canonical audit events in the same transaction as state effects. Chain previous event
   digest, sequence, operation/request/contract identity and redacted result metadata.
5. Implement startup reconciliation using PID + process start identity, owned process tree,
   operation state, staging markers, audit chain and pointer/manifest validation. Reconciliation
   is repeatable and cannot fabricate verification/completion.
6. Implement atomic workspace reset: prepare/validate a new generation, commit selection under the
   live fence, preserve committed evidence/previous release, and quarantine only owned incomplete
   state. Never recursively clean a caller path.
7. Implement `retail.export` staging for the exact ordered eleven marts. Write each Parquet
   exclusively, fsync, verify regular/single-link identity/schema/content/row count and build the
   released manifest with one coherent generation/contract/runtime identity.
8. Validate/fsync manifest, atomically replace `current-release.json` in the same directory and
   fsync parent. Readers open pointer+manifest through retained FDs and verify digest/asset set.
9. Characterize direct expert Make/Airflow paths during live learner operations. Prove disjoint
   defaults and refusal of any learner-targeted direct call without inherited fence capability.
10. Turn all race/crash/idempotency/release suites GREEN without sleep-based correctness.

## Refactor

Keep mutable projections, append-only audit, immutable release assets and replaceable pointers as
separate APIs with different preconditions. Do not combine them into a generic file/database
helper that weakens ownership or atomicity.

## Tests After

- Race two runner instances and every reset/export/verify pair at each boundary.
- Kill before/after lock, fence, transaction, audit, asset fsync, manifest fsync, pointer rename,
  directory fsync, result commit and acknowledgment; restart twice.
- Replay same/different requests before, during and after restart.
- Run Make expert path concurrently and learner-targeted Airflow/direct denial; verify no mixed DB,
  export, pointer, audit or evidence.
- Verify old or new complete eleven-asset current release only.

## Regression Gate

- `RED-XRACE`, `RED-CRASH`, `RED-IDEMP`, and `RED-REL` are GREEN.
- Audit chain validates and cannot be updated/deleted through the application connection.
- No stale owner or incomplete release advances state/pointer.
- Reset/reconciliation/cleanup never touches foreign, expert, base or evidence state.

## Risk and Security

Advisory locks alone are insufficient; the fence epoch prevents a stale process from committing
after lock loss/restart. SQLite/audit hashes detect corruption but cannot authenticate against a
same-account attacker who can alter code/state; evidence must state that residual honestly.

## Success Criteria

- [ ] Shared learner mutation fencing and cross-entrypoint race safety are proven.
- [ ] Crash/restart and duplicate/conflicting operations resolve deterministically.
- [ ] Audit is append-only by application contract and tamper-evident.
- [ ] Current release always names one verified complete eleven-asset generation.

## Next Steps

Phase 6 packages the exact Make gates, S3 evidence, rollback rehearsal and independent handoff.
