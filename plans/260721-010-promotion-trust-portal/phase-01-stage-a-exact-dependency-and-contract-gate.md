---
phase: 1
title: "Stage A exact dependency and contract gate"
status: pending
priority: P1
dependencies: []
effort: "M"
---

# Phase 1: Stage A exact dependency and contract gate

## Overview

Start a cook branch from pristine released integration
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` and fail closed before portal rendering. Re-prove
remote release ancestry, every admitted dependency byte, exact toolchain/lock, protected hashes,
command ownership, and the released #8 validators. Build the closed release binding and safe
contract adapter through real RED tests.

## Context Links

- [Stage A amendment](./stage-a-release-amendment.md)
- [Dependency gates](./dependency-and-release-gates.md#gate-a--static-portal-authority)
- [Protected identities](./requirements-and-risk-traceability.md#protected-data-and-contract-truth)
- [TDD matrix](./verification-evidence-and-uat.md#tests-before-matrix)

## Requirements

### Functional

- Re-prove GA-01..GA-05 from the cook tree and fresh remote release refs.
- Through `verify-stage-a-release.mjs`, prepare/admit one exact-lock CPython 3.12.3 runtime, run
  `learning-contracts-check`, `lesson-check LESSON=promotion-trust`, and `api-contracts-check`,
  then remove only that runtime; require the released lesson/lab/manifest/registry and 16
  operations.
- Bind only exact current released #7/#8 paths, versions, blobs, bytes, hashes, operations, and
  package graph.
- Map released safe fields through the released validators; no schema/content copy.

### Non-functional

- Local/upstream/fresh integration equality, clean input, no conflicting writer.
- Frozen Node `22.22.3`/npm `10.9.8` lock v3 dependency graph; no install scripts or fallback.
- Any missing/mismatched release/tool/field/path/version/hash fails before rendering.
- No #9 value, BFF/API, browser state, or future identity.

## Authorized Files

Create only:

```text
apps/learning-portal/package.json
apps/learning-portal/package-lock.json
apps/learning-portal/release-binding.stage-a.json
apps/learning-portal/scripts/verify-stage-a-release.mjs
apps/learning-portal/src/contracts/released-learning-adapter.mjs
apps/learning-portal/src/contracts/safe-view-model.mjs
apps/learning-portal/tests/unit/release-binding.test.mjs
apps/learning-portal/tests/unit/released-learning-adapter.test.mjs
```

No modify/delete is authorized. Exact release sources are read-only.

## Tests Before

1. Retain PTP-RED-A-001 for wrong commit/tree/ancestry/blob/byte/hash/version/operation/lock.
2. Retain PTP-RED-A-002 for every protected identity mutation.
3. Retain PTP-RED-A-020 for unknown family/path/hash/version/field.
4. Make failures traverse the real release verifier and adapter, not an unavailable import.

## Tests After and Regression

- Exact release input generates byte-stable bindings twice.
- One-at-a-time mutations fail with stable closed codes.
- Adapter output contains only safe released fields and rejects attribution/unknowns.
- Binding contains two read compatibility operation identities and no HTTP/runner capability.
- Frozen install, released #8 checks, protected/ownership checks, audit input, and
  `git diff --check` pass within amendment ceilings.

## Implementation Steps

1. Create branch from the exact integration and record equality/clean/lease evidence.
2. Write RED tests and retain valid failure records.
3. Add exact app package/lock derived from the released #7 graph; only root name/scripts differ.
4. Add the closed release binding and verifier over cook-tree bytes, exact lock/freeze, admitted
   runtime lifecycle, and released validator commands.
5. Add the released validator adapter and closed safe model.
6. Run mutation, determinism, protected-hash, command-owner, frozen-install, and audit gates.
7. Confirm the phase diff equals these eight creates and no generated output is tracked.

## Success Criteria

- [ ] Exact pristine integration and all enumerated released bytes are re-proved.
- [ ] PTP-RED-A-001/002/020 have valid RED then GREEN evidence.
- [ ] Frozen lock/toolchain and released validators pass without copied contract truth.
- [ ] No Issue #9, API, mutation, progress, evidence, or completion authority exists.
- [ ] Only the eight authorized files are added.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Feature/worktree bytes mistaken for release | Remote merge/tree proof plus cook-tree digest catalogue |
| App binding becomes a second schema | Closed identity index and safe projection only |
| Ignored app lock omitted | Inspect then force-add only the exact app lock |
| Dependency acquisition drifts | Exact graph/integrity comparison, no scripts, audit |

Rollback removes only these eight unmerged additions. Any released/protected drift is a STOP.

## Next Steps

Phase 2 may start only after this exact gate is green.
