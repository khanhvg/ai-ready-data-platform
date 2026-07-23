# Phase 5 — Implement CAS, Recovery and Atomic Release

## Objective

Make the container backend durable under duplicate requests, crashes and concurrent entrypoints
while retaining one exact operation execution and old-or-new complete state.

## Steps

1. Implement private marker-owned state roots, descriptor/no-follow admission and one runner-wide
   active-container lock plus per-workspace mutation locks.
2. Allocate monotonic fence epochs and bind request, container identity, image digest, operation and
   workspace revision. Recheck the live fence before every state/audit/evidence/release commit.
3. Implement released SHA-256 plus JCS idempotency. Same key/same request returns the committed
   result; same key/different request conflicts before container allocation.
4. Implement one owner-private SQLite database with foreign keys, WAL and synchronous FULL.
   Unique request digest, fence compare-and-update and append-only hash-chained audit triggers share
   the transaction. Deny UPDATE/DELETE and raw env/output/private path persistence.
5. Implement durable lifecycle transitions before external Engine actions. Reconcile interrupted
   create/start-awaiting-input/copy/verify/execute/inspect/archive/stop/remove by exact ID, owner
   labels, image and fence only.
6. Treat stale, missing, label-mismatched or reused identity as non-committable. Stop/remove only an
   exact owned identity; never enumerate and clean unrelated containers.
7. Import the validated workspace/result into unique host staging and commit with fsync plus atomic
   same-filesystem pointer. A crash before commit preserves prior state; a crash after commit before
   ack replays the committed result.
8. Implement workspace.reset as atomic ready-state generation creation that preserves released
   progress/evidence semantics and is idempotent.
9. For retail.export, revalidate the exact ordered eleven regular single-link Parquet assets,
   schema/content hashes, ownership, size and generation. Fsync immutable assets and manifest,
   recheck fence, atomically replace current and fsync parent.
10. Run deterministic barrier tests for runner-vs-runner, reset/export/verify, client disconnect,
    main crash, stale fence, teardown interruption and every commit/fsync/rename/ack point.

## Invariants

- Semantic operation execution remains entirely inside the container backend.
- No result can commit before successful archive admission and container removal.
- One request creates at most one operation effect despite crash/replay.
- Expert repository paths remain disjoint and byte-identical; Issue #9 does not patch Airflow.
- Readers see only the previous or next complete eleven-asset release.
- Cleanup refusal is safer than deleting an ambiguous/foreign target.

## Exit Criteria

- Crash, idempotency, stale identity, reconciliation, fencing, reset and release RED suites pass.
- Audit/evidence chains close for success and bounded failure paths.
- Exact eleven-asset publication is atomic and rollbackable.
- Zero process, namespace, mount, port or container residue exists after every terminal case.

## Rollback

Stop admission, remove only exact recorded containers, restore the previous verified current
pointer, preserve audit/evidence and quarantine ambiguous marker-owned staging. Never broad-delete
workspace roots or Docker objects.
