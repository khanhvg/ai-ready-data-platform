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

Fail closed before the first Stage A product write. Pin the exact merged Issue #7 Vite handoff,
the exact released Issue #8 Stage A contracts, and the shipped Issue #6 data truth at a fresh
readiness-authorized implementation input. This phase remains externally blocked today.

## Context Links

- [Plan](./plan.md)
- [Dependency gates](./dependency-and-release-gates.md#gate-a--static-portal-authority)
- [Requirements and exact hashes](./requirements-and-risk-traceability.md#issue-6-data-truth)
- [Verification RED IDs](./verification-evidence-and-uat.md#tests-before-matrix)
- [Issue #6 fixture handoff](../260721-006-freeze-golden-baseline/issue-7-fixture-and-merge-handoff.md)

## Requirements

### Functional

- Prove GA-01..GA-05 with exact remote identities, ancestry, versions, paths, bytes, Git blobs,
  SHA-256 digests, tools, package/lock, operation matrix, validators, completion protocol, and
  rollback metadata.
- Generate a closed app-owned release-binding manifest only from the released #7/#8 handoffs.
- Preserve Issue #6 fixture/contract bytes and protected root `release-manifest.json`.

### Non-functional

- No future SHA/version/API is guessed.
- Local HEAD, upstream, and fresh remote input are equal and the worktree is clean.
- Missing tool/release/digest/lease result is typed `fail`.
- Changed paths stay under I5-05 ownership.

## Architecture

The later-amendment release gate reads release metadata and files only after readiness provides
their exact locators. It verifies before generating any app-owned binding. The binding is an
index of externally owned interfaces, not a schema copy or migration. The portal build and tests
depend on this gate; no permissive default exists.

## Related Code Files

- Authorized Stage A create/modify/delete paths now: `[]`.
- Authorized Stage A implementation commands now: `[]`.
- Consumable Stage A dependency SHAs now: `[]`.
- Later amendment ceiling: `apps/learning-portal/**` (including portal tests) and
  `mk/issue-5/i5-05.mk`; the four Issue #6 handoff files remain read-only.
- The amendment must derive exact paths from merged #7 and released #8, then pass revalidation
  and readiness before this phase can execute.

## Tests Before

1. Add PTP-RED-A-001 for absent, draft, non-ancestor, malformed, wrong-hash, wrong-version, wrong
   operation, and changed package/lock release inputs.
2. Add PTP-RED-A-002 for each Issue #6 SHA-256/Git blob and protected manifest drift.
3. Assert the current unpublished #7/#8 candidate heads fail as consumable releases.
4. Retain failure evidence with the exact implementation input and dependency observations.

## Refactor

Keep one release-gate reader and one digest/ancestry path. Do not add a portal-specific contract
registry, schema fork, copied fixture, or generalized release framework.

## Tests After

- Valid released handoffs generate byte-stable bindings twice.
- One-byte/path/version/operation/lock mutation fails with a stable code.
- Bindings contain no runner API/registry at Stage A.
- Changed-path/protected-path/credential/private-path checks pass.

## Regression Gate

Run only the exact locked contract/test/build commands pinned from merged #7 and released #8 by
the later amendment, plus its focused I5-05 release-gate test. Record results in the exact
portal-compatible #8 result/evidence schema; `fitness-result-v1` is not a fallback. Do not run
Stage B or claim the Issue #10 Verify block.

## Implementation Steps

1. Stop unless a later amendment pins exact #7/#8 SHAs and file/command allow-lists, then passes
   fresh independent revalidation and Stage A readiness at one exact input.
2. Fetch the authorized integration ref and prove local/tracking/fresh-live equality, clean state,
   ancestry, ownership, and absence of conflicting leases.
3. Verify GA-01 and copy/promote only the exact accepted Vite foundation/path map and lock.
4. Verify GA-02 and bind only the exact released #8 validators/types/operation/completion paths.
5. Verify GA-04 Issue #6 hashes and schema-version identities read-only.
6. Write and retain the RED failures before the smallest gate/binding implementation.
7. Generate bindings twice, compare bytes, run mutations, and emit the dependency manifest.
8. Recheck scope/protected hashes. Stop on any mismatch.

## Success Criteria

- [ ] GA-01..GA-05 pass at one exact readiness-authorized input.
- [ ] PTP-RED-A-001/002 fail before implementation and pass after without weakened fixtures.
- [ ] #7/#8 release bindings are deterministic, exact, and contain no #9 assumptions.
- [ ] Issue #6 four handoff hashes/blobs and root protected manifest match.
- [ ] No product behavior or Stage B runner integration precedes this gate.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Candidate plan mistaken for release | Require remotely observed merge/release and ancestry/blob equality |
| Contract path differs from plan | Stop and return to #8; never guess |
| Ignored app lock omitted | Verify exact tracked lock; force-add only its exact app path |
| Gate script becomes shared release framework | Keep issue-local and delete duplication during review |

## Security Considerations

Run PTP-S3-11/13/14, high-confidence credential/private-path scans, dependency audit, and exact
path allow-list. No network/cloud action occurs beyond authorized Git/GitHub dependency checks and
locked dependency installation.

## Next Steps

Only after this phase passes may Phase 2 create the tests-first Stage A portal foundation.
