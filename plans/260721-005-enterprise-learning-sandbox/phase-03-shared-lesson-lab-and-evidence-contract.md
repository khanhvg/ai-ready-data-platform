---
phase: 3
title: "Shared Lesson Lab and Evidence Contract"
status: pending
priority: P1
dependencies: [1, 2]
effort: "L"
---

# Phase 3: Shared Lesson Lab and Evidence Contract

<!-- Updated: Validation Session 1 - fixed shared-core ownership and cross-track contract inputs. -->

## Overview

Implement the versioned lesson, lab, progress/state, OpenAPI and evidence contracts that the
portal, runner, curriculum, local/AWS adapters and future AI consume.

## Context Links

- [Normative lesson/lab contract](./lesson-lab-contract.md)
- [Requirements traceability](./requirements-traceability.md)
- [Architecture decisions](./architecture-decisions.md)
- Phase 1 golden/evidence schema and Phase 2 accepted web ADR

## Requirements

- JSON Schemas cover every required lesson/lab/evidence field and reject unknown
  security-sensitive fields.
- Validate prerequisite DAG, competency/view/ADR/pattern/failure/remediation references.
- Implement the legal state machine, operation/idempotency IDs, evidence binding and migration.
- OpenAPI covers synchronous lesson/workspace/operation/reset/verify/evidence boundaries with
  typed problem details, correlation and idempotency.
- Mark logical API layer in contract metadata; do not turn taxonomy into services.
- Do not create AsyncAPI unless an actual channel is introduced.
- Provide promotion-trust lesson/lab manifests and failure/remediation codes.
- Preserve backward reading/migration from every released schema version.
- Consume, without forking, Phase 1 `retail-golden-v1.json` and the tracked promotion-trust
  fixture/manifest; later P7 data-platform contracts are not a first-journey dependency.
- Publish the normative operation matrix for lesson/progress, workspace, operation status,
  reset/verify/evidence, tool status/deep links, data query, and health/readiness with logical
  taxonomy, physical owner, trust, idempotency, and evidence fields.
- Define one local state-authority/completion transaction and reconciliation protocol; do not let
  portal SQLite, runner journals, and evidence files each imply independent completion authority.
- Add machine-readable non-mutating prerequisite checks and ordered hint ladders; hints/solution
  reveal are evidence events and never set completion.

## Architecture

Contract files are source-of-truth; generated TypeScript/Python types are build artifacts checked
for drift, not independently edited. Portal and runner validate at boundaries. Evidence is
canonicalized and hashed by a framework-neutral library.

I5-03 receives a time-bounded sequential shared-core write lease after I5-01 merges. The owner may
be different, but no concurrent shared-contract writer is allowed and the lease ends at an exact
contract release SHA.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create/modify | `learning/contracts/{lesson,lab,lab-state,evidence}.schema.json` | 500-800 lines | Schema fixtures |
| Create | `contracts/openapi/learning-platform-v1.yaml` | 500-800 lines | API lint/examples |
| Create | `learning/contracts/registry.yaml` | 100-180 lines | Version/ID registry |
| Create | `learning/lessons/promotion-trust/{lesson.yaml,content.mdx}` | 400-650 lines | First lesson |
| Create | `learning/labs/promotion-trust/lab.yaml` and fixtures | 250-400 lines | First lab |
| Create | `packages/learning-contracts/**` or winning-stack equivalent | 300-500 LOC | Generated/shared validators |
| Create | `tests/contracts/learning/**`, `tests/contracts/openapi/**` | 600-900 LOC | Valid/invalid/migration/tamper |
| Create | `mk/issue-5/i5-03.mk` | 20-40 lines | Contract targets via root include |

## Interface Checklist

- [ ] `validateLesson`, `validateLab`, `validateEvidence`
- [ ] `transition(current, event) -> next | typed conflict`
- [ ] `canonicalizeEvidence` and `verifyEvidenceHash`
- [ ] version registry and migration reader
- [ ] OpenAPI operation IDs aligned to runner command IDs/use cases
- [ ] generated type drift check

## Dependency Map

- Depends on Phase 1 evidence core and Phase 2 web decision.
- Blocks Phases 4-7 and 12.
- Contract writes stay with the active serialized shared-core lease holder; downstream changes
  require an additive version and a new exact contract-release SHA.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Illegal reset/verify transition | Typed conflict; no state/evidence mutation |
| Critical | Duplicate idempotency key | Same operation result; conflicting payload rejected |
| Critical | Tampered evidence/artifact/verifier hash | Completion rejected |
| High | Missing prerequisite/view/remediation | Authoring validation fails |
| High | Old schema evidence | Explicit migration/read or unsupported-version error |
| High | AsyncAPI absent | Inventory passes while no async channel exists |
| Medium | Unknown extension field | Allowed only in namespaced extension policy |

## Tests Before

Create valid golden fixtures plus one failure fixture for every schema rule, state transition,
tamper case, unresolved reference, migration boundary and OpenAPI error/example.

## Refactor

Consolidate Phase 1 evidence primitives behind the shared package without changing canonical
bytes. Generate portal/runner types from source schemas.

## Tests After

Property-test state transitions/idempotency; snapshot canonical payloads; round-trip generated
types; lint OpenAPI; validate first lesson and lab; test previous-version readers.

## Regression Gate

```bash
make learning-contracts-check
make api-contracts-check
make evidence-contracts-check
make data-contracts-check
```

## Implementation Steps

1. Write failing schema/reference/state/API/tamper/migration fixtures.
2. Finalize version registry and source schemas.
3. Implement validators, canonicalization and state transition library.
4. Author OpenAPI with logical taxonomy metadata and problem examples.
5. Author the first lesson/lab manifests against real Phase 1 evidence.
6. Generate language types and drift checks.
7. Document additive migration and AsyncAPI admission policy.

## Success Criteria

- [ ] All contract fields and first manifests validate.
- [ ] Illegal transitions/races/tampering cannot produce completion.
- [ ] OpenAPI is lint-clean and maps logical layers without multiplying services.
- [ ] No AsyncAPI exists without a real channel.
- [ ] Previous released evidence remains readable or fails with a safe explicit error.

## Risk, Security, and Rollback

Risk is premature over-generalization. Keep one real journey as the design oracle and version only
observed needs. Reject secret/PII/raw plan fields. Rollback keeps the prior schema/reader and
reverts new version references; never rewrite existing evidence.

## Next Steps

Release the contract package/version to the runner and portal worktrees.
