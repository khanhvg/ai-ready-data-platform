---
phase: 1
title: "Freeze authority and dependency gates"
status: pending
priority: P1
dependencies: []
effort: "Gate; repeated before each staged cook"
---

# Phase 1: Freeze authority and dependency gates

## Context Links

- [Plan](./plan.md)
- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Requirements and Risk Traceability](./requirements-and-risk-traceability.md)
- [Protected Assets](./verification-evidence-and-protected-assets.md)
- [Issue #11](https://github.com/khanhvg/ai-ready-data-platform/issues/11)

## Overview

Convert real released dependencies into one exact, closed stage authority. This phase is not a
cook task at the current plan output: no dependency release, implementation input, file path,
command, renderer, fixture, or fitness schema is authorized. It must be performed first as a
fresh plan amendment, independently revalidated, then readiness-audited.

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

- Current Create: none (`[]`).
- Current Modify: none (`[]`).
- Current Delete: none (`[]`).
- Later amendment may list only exact paths inside the Issue #11 ownership ceiling and exact
  additions-only/shared seams explicitly granted by released owners.

## Implementation Steps

1. Fetch origin and read Issue #8, Issue #10, Issue #11, relevant PR/merge/release attestations,
   and owner lease decisions fresh.
2. Require exact branch, clean worktree, required ancestry, and local HEAD = tracking = fresh-live
   at the prospective stage input.
3. For Stage A, reject current Issue #8 plan/readiness commits. Accept only an exact released
   contract SHA plus registry/schema/validator/fixture/canonicalization paths and hashes.
4. Bind the Issue #11 `fitness-result-v1` acceptance name to the exact released Issue #8 schema
   path/hash. If absent/incompatible, stop for plan correction; never use the current base copy as
   fallback.
5. For Stage B, additionally reject current Issue #10 plan/validation commits. Accept only the
   passing merged real-journey SHA with exact portal renderer/registry/publication seams and test
   evidence.
6. Verify the released portal seam requires no portal-source edit. If it does, stop for a new
   serialized portal integration authority.
7. Resolve the Issue #6 additions-only view lease: exact owner, start SHA, extension seam, files,
   commands, duration, conflict rule, protected baseline, and rollback. Do not infer Structurizr
   or modify the hard-coded six-view toolchain without explicit authority.
8. Derive and document exact stage implementation file/command allow-lists, tool versions,
   time/resource/output bounds, dependency reads, evidence layout, and deny-list.
9. Submit the amendment to a fresh independent validator, then a fresh readiness auditor. Neither
   role may be this planner/cook actor.
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

No implementation command is legal now. The later amendment supplies exact gate commands. The
planner-level gate is inspection only and cannot mark a stage cookable.

## Success Criteria

- [ ] Exact released dependency SHA(s), blobs, evidence, and compatibility/rollback are pinned.
- [ ] Exact stage file and command allow-lists are non-empty, closed, and owner-valid.
- [ ] Fitness schema and, for Stage B, portal renderer are bound to released paths/hashes.
- [ ] Protected view/tool/shared-contract/portal boundaries and lease are proven.
- [ ] Fresh independent validation and fresh readiness authorize one exact stage input.
- [ ] Any unmet item keeps the stage `blocked`, with no partial cook.

## Risk Assessment

Primary risk is mistaking planning/readiness for release. Mitigation is external exact-SHA release
proof, blob verification, empty current authority, and a repeated gate. Rollback is no write: an
invalid amendment is abandoned; no dependency branch or worktree is altered.

## Security Considerations

No credentials or mutable external state are required. A dependency or lease mismatch is a
security failure, not a scheduling inconvenience.

## Next Steps

After a Stage A readiness output only, proceed to Phase 2. After Stage A release plus a separate
Stage B readiness output, proceed to Phase 5.
