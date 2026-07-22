---
phase: 1
title: "Freeze authority and dependency gates"
status: pending
priority: P1
dependencies: []
effort: "Gate; repeated before each staged cook"
---

# Phase 1: Freeze authority and dependency gates

<!-- Updated: Validation Session 1 - separated Issue #6 command envelopes from future Issue #8 evidence bindings. -->

## Context Links

- [Plan](./plan.md)
- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Protected Assets](./verification-evidence-and-protected-assets.md)
- [Issue #11](https://github.com/khanhvg/ai-ready-data-platform/issues/11)

## Overview

Convert real released dependencies into one exact, closed stage authority. For Stage A, the
[exact-release amendment](./stage-a-release-amendment.md) completes this planning gate from
released integration `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; its fresh readiness audit
authorizes only the exact static scope. The cook must repeat the gate before its first write.

Stage A gate consumes exact released Issue #8 learning contracts. Stage B repeats the gate after
Stage A and consumes the exact passing merged Issue #10 real journey/portal renderer. No future
SHA or “compatible” seam is selected in advance.

## Requirements

- Functional: verify branch/input/remote/body/dependencies/leases fresh; pin exact released
  commits/blobs/evidence; derive a closed stage allow-list and command list.
- Non-functional: fail closed on drift; preserve single-writer leases; no rebase/merge/reset or
  fallback; retain machine-readable authority evidence.
- Security: prove no portal/shared-contract/view/toolchain/root/cloud authority is implied.

## Architecture

Authority is a staged chain, not a Boolean:

```text
real dependency release
  -> exact amendment with hashes and closed allow-lists
  -> fresh independent validation
  -> fresh readiness output / implementation input
  -> repeated exact-head preflight
  -> RED tests before first behavior write
```

Stage B starts a new chain; Stage A readiness cannot authorize Stage B.

## Related Code Files

- Current Stage A Create: exactly the 50 paths in the amendment.
- Current Stage A Modify/Delete: none (`[]`).
- Current Stage B Create/Modify/Delete: none (`[]`).

## Implementation Steps

1. Fetch origin and read Issue #8, Issue #10, Issue #11, relevant PR/merge/release attestations,
   and owner lease decisions fresh.
2. Require exact branch, clean worktree, required ancestry, and local HEAD = tracking = fresh-live
   at the prospective stage input.
3. For Stage A, reject Issue #8 plan/readiness/feature commits. Accept only exact released
   `fecf6bb8…` plus the amendment-pinned registry/schema/validator/example/canonicalization hashes.
4. Emit only the existing `fitness-result-v1` command envelope named by the released I5-06
   registry. Treat released `fitness-result-v2` (`emissionFallback: null`) and all learning,
   progress, and completion evidence as read-only negative boundaries; do not map or emit them.
5. For Stage B, additionally reject current Issue #10 plan/validation commits. Accept only the
   passing merged real-journey SHA with exact portal renderer/registry/publication seams and test
   evidence.
6. Verify the released portal seam requires no portal-source edit. If it does, stop for a new
   serialized portal integration authority.
7. Verify the admitted `i5-06-stage-a-architecture-expansion-v1` lease: exact owner, release SHA,
   19 extension paths, duration, conflict rule, protected baseline, and rollback. Do not infer
   Structurizr or modify the hard-coded six-view toolchain.
8. Verify the documented exact stage implementation file/command allow-lists, tool versions,
   time/resource/output bounds, dependency reads, evidence layout, and deny-list.
9. Require fresh strict validation and a readiness auditor independent from the original planner,
   validator, and future cook actor. The audit binds this exact amendment and release input.
10. Before first write, repeat steps 1-8 at the exact readiness output and stop on any change.

## Tests Before

- Authority mutation cases: stale SHA, feature/readiness SHA, unreachable merge, blob mismatch,
  missing evidence, missing exact schema/renderer path, dirty tree, remote divergence, active
  lease, protected hash drift, portal overlap, and empty stage allow-list.
- Every mutation must fail before any implementation or workspace mutation.

## Tests After

- Static parse of amended authority tables.
- Exact allow-list/command ownership uniqueness.
- Dependency blob/hash/release/evidence verification.
- Protected Issue #6 source/row/render/blob comparison.
- Independent validation and readiness outputs reference the same exact amended head.

## Regression Gate

Only the amendment's exact Stage A commands are legal. This planning gate does not itself execute
them or authorize Stage B.

## Success Criteria

- [ ] Exact released dependency SHA(s), blobs, evidence, and compatibility/rollback are pinned.
- [ ] Exact stage file and command allow-lists are non-empty, closed, and owner-valid.
- [ ] Released evidence schema plus command-result compatibility and, for Stage B, portal
      renderer are bound to exact released paths/hashes.
- [ ] Protected view/tool/shared-contract/portal boundaries and lease are proven.
- [ ] Fresh independent validation and fresh readiness authorize one exact stage input.
- [ ] Any unmet item keeps the stage `blocked`, with no partial cook.

## Risk Assessment

Primary risk is mistaking planning/readiness for release. Mitigation is external exact-SHA release
proof, blob verification, closed Stage A authority, and a repeated gate. An invalid preflight
stops before write; no dependency branch or worktree is altered.

## Security Considerations

No credentials or mutable external state are required. A dependency or lease mismatch is a
security failure, not a scheduling inconvenience.

## Next Steps

After a Stage A readiness output only, proceed to Phase 2. After Stage A release plus a separate
Stage B readiness output, proceed to Phase 5.
