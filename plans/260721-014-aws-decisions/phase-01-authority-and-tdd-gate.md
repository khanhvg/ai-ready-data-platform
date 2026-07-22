---
phase: 1
title: "Authority and TDD Gate"
status: pending
priority: P1
dependencies: []
effort: "M"
---

# Phase 1: Authority and TDD Gate

## Context links

- [Plan authority boundary](./plan.md#planner-boundary-and-current-authority)
- [Current source inventory](./current-source-inventory.md)
- [Requirements and TBC register](./requirements-and-risk-traceability.md)
- [Protected input baseline](./protected-input-baseline.md)

## Overview

After the required Issue #11 release and exact-SHA amendment, freeze a non-empty implementation
lease and write the failing authority/schema/security fixtures before any decision model or ADR
behavior. This phase never calls AWS or Terraform.

## Requirements

- Functional: satisfy FR-001, FR-017..020 and establish stable assertion IDs for FR-002..016.
- Non-functional: NFR-001/002/004/010/011/012/014.
- Dependency: exact released Issue #11 SHA/concern IDs, amended allow-lists, independent
  revalidation, and fresh readiness must exist before this phase can start.
- Authority: wrong input, dirty tree, empty allow-list, conflicting lease, or protected mismatch
  stops before test creation.

## Architecture

```text
exact authority ledger
  -> strict schema registry and duplicate-aware parsers
  -> failing fixtures grouped by stable RED assertion IDs
  -> protected/changed-path guard
  -> only then production decision/model work
```

The authority ledger binds exact input/dependency SHAs, allowed files/commands, protected digests,
released concern IDs, evidence schema mapping, and no-cloud execution policy. It treats empty/TBC
values as typed blockers rather than defaulting them.

## Related code files

- Current implementation allow-list: `[]`.
- Exact files to create/modify: `TBC` in the dependency amendment.
- Candidate ownership envelope only: `docs/decisions/aws/**`, cost/state decision models/tests,
  `mk/issue-5/i5-09.mk`.
- Delete: none planned.
- Protected: every path/digest/absence in `protected-input-baseline.md`.

## Tests before

1. Wrong input/dependency SHA, dirty tree, missing release and protected hash mismatch.
2. Empty/duplicate/contradictory file or command authority.
3. Missing/duplicate requirement, concern, owner, TBC, evidence or rollback mapping.
4. Duplicate-key/non-finite/overflow/oversize parser fixtures.
5. Credential/account/private-path/PII and path/link/special-file/process-injection fixtures.
6. Attempted network/AWS/credential/account access by a deterministic core test.

Each test must fail for its named reason while all product/model outputs are still absent.

## Refactor

No product refactor. Reuse released Issue #6 evidence/canonicalization concepts only through an
exact compatibility mapping; do not edit shared contracts or golden code.

## Tests after

- Authority preflight accepts only the exact amended lease and emits a safe failure bundle for
  every negative case.
- Network-denied/no-credential deterministic test process passes.
- Exact changed-path and protected tree/absence checks pass.
- Every RED assertion ID is registered to later GREEN work; no disabled or expected-failure test
  may satisfy the gate.

## Regression gate

Future exact commands are amendment-owned. At minimum, this phase feeds:

```text
make state-matrix-check
make cost-model-check
make aws-decision-check
```

They remain non-runnable at the current planner SHA.

## Implementation steps

1. Re-read GitHub Issue #14 and the exact released Issue #11 handoff from fresh remote state.
2. Verify exact input/ancestry/cleanliness and regenerate protected baselines.
3. Apply the independently validated/readiness-approved exact file and command allow-lists.
4. Define stable schema/assertion/error/status vocabulary without changing released shared
   contracts.
5. Write RED-A and RED-E fixtures before model/ADR code.
6. Add deterministic execution containment and safe failure-evidence finalization.
7. Prove tests fail for intended causes and only then open Phase 2.

## Success criteria

- [ ] Exact non-empty authority exists and matches the amended/revalidated/readiness artifact.
- [ ] All incomplete/duplicate/contradictory/TBC and S3 boundary fixtures fail first.
- [ ] Core tests have no network/AWS/account/credential dependency.
- [ ] Protected paths, semantics and absences match the approved input.
- [ ] No product behavior, ADR selection, rate, BOM, resource, or cloud claim was created early.

## Risk assessment

The main risk is laundering a branch candidate or registry declaration into implementation
authority. Mitigation is exact GitHub release read-back, explicit empty-state failure, and a
single-writer lease. Rollback removes only issue-owned test/model additions and restores the
prior authority file while retaining safe RED evidence.

## Security considerations

Treat model inputs and evidence as hostile. Do not read ambient AWS configuration, environment
secrets, home-directory credentials, or account data. Reject shell interpolation and unsafe file
types before parsing.

## Next steps

Proceed to Phase 2 only when the complete authority and RED gate passes at one clean exact SHA.
