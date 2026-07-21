---
phase: 3
title: "Stage A operations completion and guidance"
status: pending
priority: P1
dependencies: [2]
stage: "A"
---

# Phase 3: Stage A Operations, Completion, and Guidance

## Context Links

- [Master state machine and API](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md#state-machine)
- [Master state authority table](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md#local-state-mutation-and-evidence-authority)
- [S3 threat matrix](./requirements-and-risk-traceability.md#s3-threat-and-negative-test-matrix)

## Overview

Publish machine-readable operation and completion/reconciliation contracts, implement the legal
state/idempotency engine, and define safe prerequisite probes and progressive hints. This phase
prevents portal state, runner journals, evidence files and browser/Vite state from becoming
independent completion authorities.

## Requirements

- Functional: implement every legal transition and typed conflict in the normative state machine.
- Functional: same idempotency key + same canonical request returns one committed result; same key
  + different canonical request fails before mutation.
- Functional: one progress-store compare-and-set transaction references a committed runner result
  and immutable evidence blob/hash. Only that transaction emits completion.
- Functional: startup reconciliation verifies orphan evidence/result, then attaches through the
  same transaction or quarantines; evidence presence never grants completion.
- Functional: required/optional non-mutating prerequisite probes and ordered hint/reveal events.
- Non-functional: framework-neutral descriptors; no SQLite implementation, runner, portal, shell,
  arbitrary command, raw SQL, browser persistence or network call in Issue #8.

## Architecture

### One completion authority

`authorityId: portal-progress-store` names the future durable adapter required by ADR-007. The
contract defines behavior, not a database implementation:

```text
runner result (sole runner writer) ─┐
immutable evidence blob/hash ───────┼─> verify refs/hashes/version
expected progress version ──────────┘          |
                                                v
                               one compare-and-set progress transaction
                                   evidence index + completion event
```

Browser/Vite state is a cache. Runner journal is operation truth, not completion truth. Evidence
blob is immutable proof material, not completion truth. A projection can be rebuilt from progress
events; it cannot author them.

### Commit/reconciliation order

1. Runner commits verifier result keyed by run/verifier/contract hashes.
2. Evidence writer stages, bounds/scans, fsyncs and atomically renames immutable bytes.
3. Progress transaction validates expected transition version, runner result and evidence bytes;
   unique run/evidence/idempotency constraints insert evidence index + completion event atomically.
4. Acknowledgment occurs only after commit.
5. On restart, orphan evidence/result is revalidated and either attached through step 3
   idempotently or quarantined with no completion.

### Probes and hints

Probe documents identify a fixed `probeId`, kind, required/optional class, expected safe result,
learner-language remediation and retry rule. They contain no shell, argv, writable path, SQL,
network destination or environment injection. The future runner maps only registered IDs.

Hints have stable order, reveal preconditions, solution-reveal policy and an evidence event. Hint
view/use cannot change verifier output, progress transition or completion. Reflection is recorded
but never completes a lesson.

## Related Code Files

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/operation-matrix-v1.json` | authoritative operation inventory and taxonomy/physical owner/trust/evidence metadata |
| Create | `learning/contracts/completion-reconciliation-v1.json` | single-authority commit, crash/orphan/quarantine and reset rules |
| Create | `scripts/learning_contracts/state.py` | pure transition, expected-version and idempotency decision functions |
| Create | `scripts/learning_contracts/completion.py` | pure commit precondition and reconciliation disposition functions |
| Create | `scripts/learning_contracts/guidance.py` | probe and hint semantic validation; no execution |
| Create | `tests/contracts/learning/test_operation_matrix.py` | matrix completeness/uniqueness/metadata tests |
| Create | `tests/contracts/learning/test_prerequisite_and_hints.py` | required/optional, mutation-spy, order/reveal/no-completion tests |
| Modify | `tests/contracts/learning/test_state_and_completion.py` | exhaustive transition/idempotency/fault/reconcile properties |
| Add fixtures | `tests/fixtures/learning/contracts/valid/{operation-matrix-v1,completion-reconciliation-v1}.json` | independent third-reader vectors |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/state/{stale-version,duplicate-effect}.json` | CAS/idempotency negatives |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/completion/{runner-direct-write,evidence-presence-completes}.json` | dual-truth negatives |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/guidance/{mutating-probe,out-of-order-hint,hint-completes}.json` | probe/hint negatives |

## Operation Inventory

Every row must later match exactly one OpenAPI operation; no taxonomy-only pseudo-operation:

| `operationId` | Method/path | Taxonomy | Physical owner | Mutation/idempotency |
|---|---|---|---|---|
| `listLessons` | `GET /v1/lessons` | Experience | portal lesson module | read-only |
| `getLesson` | `GET /v1/lessons/{lessonId}` | Experience | portal lesson module | read-only |
| `getProgress` | `GET /v1/progress` | Experience | progress adapter | read-only |
| `getLessonProgress` | `GET /v1/progress/{lessonId}` | Experience | progress adapter | read-only |
| `createWorkspace` | `POST /v1/labs/{labId}/workspaces` | Process | portal BFF→runner | required |
| `getWorkspace` | `GET /v1/workspaces/{workspaceId}` | System | portal BFF→runner | read-only |
| `startWorkspaceOperation` | `POST /v1/workspaces/{workspaceId}/operations` | Process | portal BFF→runner | required |
| `getOperation` | `GET /v1/operations/{operationId}` | System | portal BFF→runner | read-only polling |
| `resetWorkspace` | `POST /v1/workspaces/{workspaceId}/reset` | Process | portal BFF→runner | required |
| `verifyWorkspace` | `POST /v1/workspaces/{workspaceId}/verify` | Process | portal BFF→runner then progress transaction | required |
| `getEvidence` | `GET /v1/evidence/{evidenceId}` | Technical | evidence index/blob reader | read-only |
| `listTools` | `GET /v1/tools` | Experience | tool status adapter | read-only |
| `getTool` | `GET /v1/tools/{toolId}` | Experience | tool status/deep-link adapter | read-only |
| `queryDataProduct` | `POST /v1/data-products/{productId}/queries` | Backend | fixed query/assertion adapter | required; raw SQL forbidden |
| `getLiveness` | `GET /health/live` | Technical | portal process | read-only/public loopback |
| `getReadiness` | `GET /health/ready` | Technical | portal dependency aggregator | read-only/public loopback |

Every browser mutation also records exact Host/Origin rule, session/CSRF rule, correlation header,
idempotency header, request digest and evidence expectation. Actual auth/session enforcement belongs
to I5-04/I5-05; the matrix cannot falsely claim it is implemented here.

## Tests Before

- Enumerate the full state transition cross-product, expected legal next state or typed conflict.
- Property-test duplicate in-flight/committed keys, payload digest conflicts, stale expected
  versions and reset/verify/reconcile races.
- Inject failure before/after runner result commit, evidence write/fsync/rename, progress transaction
  and acknowledgment; assert exactly one completion or none.
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
- Portal SQLite wording can couple Stage A to a framework. Mitigation: contract names the durable
  progress adapter and transaction semantics; concrete DB/framework wiring remains downstream.
- Polling and operation status can be mistaken for a queue/channel. Mitigation: synchronous HTTP
  request plus bounded GET polling only; no broker/channel/AsyncAPI.

## Security and Rollback

Typed conflicts expose stable codes, not sensitive payloads/existence leakage. Rollback selects the
prior contract version and leaves committed progress/evidence immutable; it never edits runner or
portal state because those implementations do not exist in this issue.

## Next Steps

Phase 4 materializes the OpenAPI document, learner-evidence contract and first promotion-trust
manifest against these exact operation and authority definitions.
