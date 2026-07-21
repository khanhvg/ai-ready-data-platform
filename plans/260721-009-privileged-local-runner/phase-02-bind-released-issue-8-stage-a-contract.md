---
phase: 2
title: "Bind released Issue 8 Stage A contract"
status: pending
priority: P1
dependencies: [1]
effort: "0.5 implementation day after dependency release"
---

# Phase 2: Bind Released Issue #8 Stage A Contract

## Overview

Hard dependency gate. Bind the implementation to the exact merged/released Issue #8 Stage A SHA
and consume its contracts read-only. Absence or incompatibility blocks all implementation; no
future schema, SHA, version, operation, type, or registry activation may be invented here.

## Context Links

- [Dependency assimilation](./implementation-boundary-and-design.md#dependency-assimilation-without-contract-invention)
- [RUN-DEP-01](./requirements-risk-threat-traceability.md#requirement-crosswalk)
- Live dependency: <https://github.com/khanhvg/ai-ready-data-platform/issues/8>

## Requirements

- Exact 40-hex Issue #8 Stage A reviewed merge/release SHA from owner-published handoff.
- Ancestry from implementation base and exact file/hash/schema/type-generation evidence.
- Compatible runner command authority, operation matrix, state/idempotency/problem/CSRF rules,
  evidence owner/schema, and command-owner registry activation.
- No modification or duplication of Issue #8-owned files.

## Related Code Files

- Create: `apps/lab-runner/config/released-contract-lock.json`
- Create: released-procedure-derived bindings only under `apps/lab-runner/src/lab_runner/generated/**` if the release requires generation
- Create: `apps/lab-runner/tests/unit/test_released_contract_lock.py`
- Create: `apps/lab-runner/tests/unit/test_generated_types.py`
- Consume read-only: exact paths named by Issue #8's release handoff
- Modify/Delete: none outside `apps/lab-runner/**`

## Dependency Gate

The current input cannot pass this phase: Issue #8 is OPEN, the runner targets are still
`future-owner`, and the current `fitness-result-v1` schema fixes owner `I5-01`. These are known
implementation blockers, not planner defects. A future readiness audit must keep cook blocked
until the released handoff resolves them through Issue #8 ownership.

## Tests Before

1. Create mutation fixtures for wrong/missing SHA, non-ancestor release, changed contract bytes,
   unknown schema version, stale generated types, absent operation, unexpected command, registry
   still future, evidence owner mismatch, and backward-reader failure.
2. Make every dependency fixture fail with one typed `RUNNER_DEPENDENCY_*` code before startup or
   workspace allocation.
3. Assert no test reads a copied/fake contract under `apps/lab-runner/tests/fixtures`.

## Implementation Steps

1. Fetch `origin` and the live Issue #8 handoff; resolve exact release SHA and owner-declared Stage A
   paths/versions/hashes.
2. Prove review/merge/release identities and `git merge-base --is-ancestor` against the candidate
   implementation base. STOP on mismatch.
3. Validate contract schemas/examples/migrations using Issue #8's own released commands.
4. Verify the eight semantic runner commands and exact typed fields can be represented without
   local extensions. Verify runner-authority operations, problem details, idempotency/correlation,
   CSRF/auth rules, state transitions and I5-04 evidence.
5. Verify the command-owner registry accepts only I5-04's three Make targets through its released
   activation seam and that physical evidence maps to `runner/<run-id>/`.
6. Write only SHA/path/version/hash/generator references to `released-contract-lock.json`.
7. Generate local bindings through the released deterministic procedure when required; compare
   generated hash twice and fail on dirty output.
8. Rerun all dependency mutation fixtures and record the lock/result in evidence.

## Refactor

None. Issue #8 contracts remain read-only. Generated runner-local adapter code is replaceable and
must never become a competing public contract.

## Tests After

- Exact release passes; every one-byte/version/SHA/registry/type mutation fails before readiness.
- Backward-reader/migration tests named by Issue #8 pass.
- `git diff` contains no `learning/contracts/**`, shared schema, or Issue #8 plan change.

## Regression Gate

- `released-contract-lock.json` is complete, non-recursive, and contains no guessed value.
- Runtime reports ready only when all locked inputs match.
- Missing required dependency tools are failure, not skip.

## Risk and Security

The primary risk is silently forking a shared security contract to unblock the runner. The only
accepted behavior is STOP and owner handback. Compatibility aliases, permissive unknown fields,
or locally patched schema copies are prohibited.

## Success Criteria

- [ ] Exact released Stage A SHA and contract identities are pinned and reproducible.
- [ ] Shared registry/evidence/operation ownership supports I5-04 without local writes.
- [ ] All drift/mismatch cases fail closed before mutation.
- [ ] No fake contract or future SHA exists.

## Next Steps

Phase 3 may begin only after this gate and prior independent plan validation/readiness authority.
