---
phase: 3
title: Stage A operations completion and guidance
status: completed
priority: P1
dependencies:
  - 2
stage: A
---

# Phase 3: Stage A Operations, Completion, and Guidance

<!-- Historical Stage A execution plan; released through PR #23 and PR #25, with current disposition in plan.md. -->

## Context Links

- [Master state machine and API](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md#state-machine)
- [Master state authority table](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md#local-state-mutation-and-evidence-authority)
- [S3 threat matrix](./requirements-and-risk-traceability.md#s3-threat-and-negative-test-matrix)

## Overview

Publish machine-readable operation and completion/reconciliation contracts, implement the legal
state/idempotency engine, and define safe prerequisite probes and progressive hints. This phase
prevents any transport cache, operation-result journal, evidence file or later web binding from
becoming an independent completion authority. It consumes no portal/runner implementation byte.

## Requirements

- Functional: implement every legal transition and typed conflict in the normative state machine.
- Functional: same idempotency key + same canonical request returns one committed result; same key
  + different canonical request fails before mutation.
- Functional: one `learning-progress-authority-v1` compare-and-set transaction references a
  committed operation result
  and immutable evidence blob/hash. Only that transaction emits completion.
- Functional: startup reconciliation verifies orphan evidence/result, then attaches through the
  same transaction or quarantines; evidence presence never grants completion.
- Functional: required/optional non-mutating prerequisite probes and ordered hint/reveal events.
- Non-functional: framework-neutral descriptors; no SQLite implementation, runner, portal, shell,
  arbitrary command, raw SQL, browser persistence or network call in Issue #8.

## Architecture

### One completion authority

`authorityId: learning-progress-authority-v1` names a framework-neutral contract role. It does not
name, inspect or assume a portal database/module or runner implementation:

```text
committed operation result ─────────┐
immutable evidence blob/hash ───────┼─> verify refs/hashes/version
expected progress version ──────────┘          |
                                                v
                               one compare-and-set progress transaction
                                   evidence index + completion event
```

Transport/browser state is a cache. An operation journal is operation truth, not completion truth.
Evidence is immutable proof material, not completion truth. A projection can be rebuilt from
progress events; it cannot author them.

### Commit/reconciliation order

1. The future operation authority commits a verifier result keyed by run/verifier/contract hashes.
2. Evidence writer stages, bounds/scans, fsyncs and atomically renames immutable bytes.
3. Progress transaction validates expected transition revision, operation result and evidence;
   unique run/evidence/idempotency constraints insert evidence index + completion event atomically.
4. Acknowledgment occurs only after commit.
5. On restart, orphan evidence/result is revalidated and either attached through step 3
   idempotently or quarantined with no completion.

### Deterministic idempotency and conflict semantics

The mutation key is `(authorityId, actorId, operationId, idempotencyKey)`. The authority stores the
canonical request SHA-256, expected revision, committed status/body hash, resulting revision and
effect identity atomically. Same key plus same canonical request returns the original status/body/
revision and performs no second effect. Same key plus a different request fails `409
IDEMPOTENCY_KEY_REUSE` before mutation. A stale expected progress revision fails `412
PROGRESS_VERSION_CONFLICT`. Concurrent equal requests converge on the single stored response;
concurrent unequal requests produce one commit and one typed conflict. No timestamp, arrival order,
retry count, evidence mtime or last-write-wins rule resolves a conflict.

Reconciliation has exactly three dispositions: `already-attached` returns the stored completion;
`attachable-orphan` revalidates every identity/hash and retries the same CAS/idempotency key;
`invalid-or-conflicting-orphan` is quarantined with a bounded reason and no progress change.

### Probes and hints

Probe documents identify a fixed `probeId`, kind, required/optional class, expected safe result,
learner-language remediation and retry rule. They contain no shell, argv, writable path, SQL,
network destination or environment injection. A future executor maps only registered IDs. A
required `fail` or unavailable probe blocks before mutation; an optional unavailable probe records
`not-run-optional`, never pass. Retries are read-only and return one of `pass|fail|unavailable`.

Hints have stable order, reveal preconditions, solution-reveal policy and an evidence event. Hint
view/use cannot change verifier output, progress transition or completion. Reflection is recorded
but never completes a lesson.

## Related Code Files

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/operation-matrix-v1.json` | authoritative operation inventory and taxonomy/abstract process-role/trust/evidence metadata |
| Create | `learning/contracts/completion-reconciliation-v1.json` | single-authority commit, crash/orphan/quarantine and reset rules |
| Create | `scripts/learning_contracts/state.py` | pure transition, expected-version and idempotency decision functions |
| Create | `scripts/learning_contracts/completion.py` | pure commit precondition and reconciliation disposition functions |
| Create | `scripts/learning_contracts/guidance.py` | probe and hint semantic validation; no execution |
| Modify | `tests/contracts/learning/test_operation_matrix.py` | close matrix completeness/uniqueness/metadata RED IDs |
| Modify | `tests/contracts/learning/test_prerequisite_and_hints.py` | close required/optional, mutation-spy, order/reveal/no-completion RED IDs |
| Modify | `tests/contracts/learning/test_state_and_completion.py` | exhaustive transition/idempotency/fault/reconcile properties |
| Create | `tests/fixtures/learning/contracts/valid/operation-matrix-v1.json` | independent third-reader vector |
| Create | `tests/fixtures/learning/contracts/valid/completion-reconciliation-v1.json` | independent third-reader vector |

## Operation Inventory

The matrix top level includes `channels: []`. Every row must later match exactly one OpenAPI
operation; no taxonomy-only pseudo-operation:

| `operationId` | Method/path | Taxonomy | Contract process role (not an implementation module) | Authn / authz / CSRF | Mutation/idempotency |
|---|---|---|---|---|---|
| `listLessons` | `GET /v1/lessons` | Experience | lesson-catalog-read | local-session / catalog-read / N/A | read-only |
| `getLesson` | `GET /v1/lessons/{lessonId}` | Experience | lesson-catalog-read | local-session / catalog-read / N/A | read-only |
| `getProgress` | `GET /v1/progress` | Experience | progress-authority-read | local-session / actor-owned / N/A | read-only |
| `getLessonProgress` | `GET /v1/progress/{lessonId}` | Experience | progress-authority-read | local-session / actor-owned / N/A | read-only |
| `createWorkspace` | `POST /v1/labs/{labId}/workspaces` | Process | workspace-operation-admission | local-session / actor-owned / required | required |
| `getWorkspace` | `GET /v1/workspaces/{workspaceId}` | System | workspace-operation-read | local-session / actor-owned / N/A | read-only |
| `startWorkspaceOperation` | `POST /v1/workspaces/{workspaceId}/operations` | Process | workspace-operation-admission | local-session / actor-owned / required | required |
| `getOperation` | `GET /v1/operations/{operationId}` | System | workspace-operation-read | local-session / actor-owned / N/A | read-only polling |
| `resetWorkspace` | `POST /v1/workspaces/{workspaceId}/reset` | Process | workspace-operation-admission | local-session / actor-owned / required | required |
| `verifyWorkspace` | `POST /v1/workspaces/{workspaceId}/verify` | Process | verification-admission→progress-authority | local-session / actor-owned / required | required |
| `getEvidence` | `GET /v1/evidence/{evidenceId}` | Technical | evidence index/blob reader | local-session / actor-owned / N/A | read-only |
| `listTools` | `GET /v1/tools` | Experience | tool-catalog-read | local-session / catalog-read / N/A | read-only |
| `getTool` | `GET /v1/tools/{toolId}` | Experience | tool-catalog-read | local-session / catalog-read / N/A | read-only |
| `queryDataProduct` | `POST /v1/data-products/{productId}/queries` | Backend | registered-query-admission | local-session / actor-owned+product-read / required | required; raw SQL forbidden |
| `getLiveness` | `GET /health/live` | Technical | http-process-health | public-loopback / public-health / N/A | read-only |
| `getReadiness` | `GET /health/ready` | Technical | dependency-readiness-aggregate | public-loopback / public-health / N/A | read-only |

Every HTTP mutation records exact Host/Origin intent, session/CSRF rule, correlation/idempotency
headers, canonical request digest, authorization class and evidence expectation. Reads record their
authn/authz class; health is public-loopback only. `enforcementStatus=downstream-required` makes
clear that Stage A specifies but does not implement transport/session enforcement. The role labels
above are contract vocabulary derived from the master architecture, not portal/runner internals.

## Tests Before

- Enumerate the full state transition cross-product, expected legal next state or typed conflict.
- Property-test duplicate in-flight/committed keys, payload digest conflicts, stale expected
  versions and reset/verify/reconcile races.
- Use the Phase 1 fault fixtures and inject failure before/after operation result commit, evidence
  write/fsync/rename, progress transaction and acknowledgment; assert exactly one completion or none.
- Spy on probe validation to prove no subprocess, write, network, environment or raw query action.
- Assert hint and reflection events cannot satisfy any completion predicate.

## Refactor

Keep pure state/decision functions separate from future persistence and transport adapters. Return
typed outcomes rather than throwing generic exceptions for expected conflicts. Do not create a
generic workflow engine or queue.

## Tests After

- All legal transition paths reach completion only through `verified → evidenced → completed` and
  the progress transaction.
- Illegal transition/race/replay/tamper paths leave authoritative state unchanged.
- Reconciliation is deterministic and idempotent across repeated restart passes.
- Operation IDs are unique; every row has all required metadata and no physical-service invention.
- Probe/hint fixtures validate; all mutating/forging variants fail.

## Implementation Steps

1. Publish the operation matrix and completion/reconciliation documents against Phase 2 schemas.
2. Implement pure state transition and canonical request-digest/idempotency decisions.
3. Implement completion commit preconditions and orphan attach/quarantine decisions.
4. Implement probe/hint semantic validators.
5. Close exhaustive state/idempotency/fault/reconcile tests.
6. Close operation and guidance tests; rerun Stage A boundary and Issue #6 regressions.

## Success Criteria

- [ ] Sixteen real operations have complete, unique metadata and no extra taxonomy rows.
- [ ] One completion authority/transaction is explicit; no browser/runner/evidence dual truth.
- [ ] Crash/orphan/replay/reset/verify cases cannot fabricate completion.
- [ ] Required probes block before mutation; optional absence is honest and non-completing.
- [ ] Hints/reflection are ordered evidence events and never completion inputs.
- [ ] Pure modules remain framework/runtime-adapter neutral.

## Risk Assessment

- A protocol document can look atomic without a testable order. Mitigation: machine-readable steps,
  fault points and expected dispositions plus exhaustive pure-state tests.
- Persistence/process wording can couple Stage A to future internals. Mitigation: contract names
  only framework-neutral roles and transaction semantics; concrete portal/runner/database wiring
  remains downstream and is absent from Stage A reads/imports.
- Polling and operation status can be mistaken for a queue/channel. Mitigation: synchronous HTTP
  request plus bounded GET polling only; no broker/channel/AsyncAPI.

## Security and Rollback

Typed conflicts expose stable codes, not sensitive payloads/existence leakage. Rollback selects the
prior contract version and leaves committed progress/evidence immutable; it never edits any
downstream process state because those implementations do not exist in this issue.

## Next Steps

Phase 4 materializes the OpenAPI document, learner-evidence contract and first promotion-trust
manifest against these exact operation and authority definitions.
