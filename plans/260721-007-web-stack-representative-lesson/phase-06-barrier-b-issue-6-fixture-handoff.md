---
phase: 6
title: "Barrier B Issue 6 Fixture Handoff"
status: pending
priority: P1
dependencies: [3, 4, 5]
effort: "external wait and fail-closed preflight; no active spike work"
barrier: blocked-on-issue-6-merge-and-four-digests
---

# Phase 6: Barrier B Issue 6 Fixture Handoff

## Context Links

- [Issue #6 fixture handoff contract](./issue-6-fixture-handoff.md)
- [Candidate protocol](./candidate-protocol.md)
- [Master execution authority](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md)

## Overview

Stop all decision-grade work until issue #6 is merged and its exact content-addressed handoff is
present in the tested tree. Barrier B consumes those files read-only, validates them once through
the neutral adapter, and binds their merge/file/schema digests to every candidate run. Waiting
does not consume candidate time; adapting data or shared contracts is forbidden.

## Requirements

- Require a full 40-character issue #6 merge SHA, prove it is an ancestor of the tested HEAD, and
  prove the four files come from that merged history rather than an unmerged worktree or ignored
  artifact.
- Require and record exact SHA-256 digests for:
  - `contracts/data/retail-golden-v1.json`
  - `contracts/data/promotion-trust-v1.yaml`
  - `tests/fixtures/learning/promotion-trust/evidence-v1.json`
  - `tests/fixtures/learning/promotion-trust/manifest.json`
- Validate producer commit, contract/fixture cross-references, schema/manifest result, lesson ID,
  fixture kind `tracked-real`, and expected conclusion `insufficient evidence`.
- Reject absolute paths, secrets/PII, executable content, unknown security fields, inconsistent
  digests, and any promotion-to-fulfillment/returns/DQ causal relationship.
- Consume all files read-only. If a candidate/common adapter cannot consume them, stop and
  coordinate with #6; never edit dependency-owned paths or introduce candidate-specific data.
- A later #6 merge/content/schema change invalidates all real-fixture samples, score fields,
  browser state, screenshots/traces, and ADR input. Preserve them only as clearly invalidated
  records; rerun every non-eliminated candidate from clean state.

## Architecture

One neutral read-only loader validates Git ancestry, file/blob/SHA-256 provenance, schema and
cross-file references, then writes a digest-only issue-owned handoff record. Candidates consume
the same projection; none reads or reshapes dependency files independently.

## File Inventory

| Action | Planned path | Purpose | Test impact |
|---|---|---|---|
| Read only | Four dependency files above | Real decision fixture/contracts | Hard gate |
| Create | `spikes/web/harness/fixture-handoff.json` | Merge SHA, file/blob/SHA-256/schema result | Single digest authority |
| Create | `spikes/web/harness/scripts/barrier-b-check.mjs` | Ancestry/path/digest/schema/read-only checks | Non-zero until complete |
| Create | `spikes/web/harness/tests/barrier-b.test.mjs` | Absent/mixed/unmerged/tampered fixtures | TDD negatives |
| Modify | `mk/issue-5/i5-02.mk` | Issue-local barrier target | No root Make change |

## Related Code Files

- Read the four dependency-owned paths without modifying them.
- Create only the issue-owned handoff/check/test/Make paths listed above.
- Delete nothing; invalidated evidence is retained with status metadata.

## Dependency Map

```text
issue #6 reviewed merge SHA + four tracked files + schema evidence
  -> neutral read-only adapter validation
  -> fixture-handoff.json single digest set
  -> invalidate all provisional/mixed real-fixture state
  -> Gate C
```

## Interface Checklist

- [ ] Merge SHA is full, merged, ancestor, and recorded in every Gate C evidence item.
- [ ] File Git blob IDs and SHA-256 digests are both recorded.
- [ ] Manifest references the exact evidence/contract bytes.
- [ ] Shared schema result is present and independently replayed read-only by the common adapter.
- [ ] Candidate adapter outputs are byte-equivalent logical projections.
- [ ] No dependency/shared file appears in `git diff`.

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | #6 open/unmerged or merge SHA absent | Barrier closed, non-zero |
| Critical | Any file absent/digest mismatch/mixed merge | Non-zero; all decision data invalid |
| Critical | Schema/manifest or four-grain invariant fails | Non-zero; no workaround |
| High | #6 changes after first candidate run | Quarantine/invalidate all real results and rerun equally |
| High | Persisted browser state uses old digest | State rejected/cleared; no evidence carries forward |
| High | Candidate needs shared edit | Stop and coordinate #6; no timer compensation |

## Implementation Steps

1. Write absent/unmerged/mixed/tampered/read-only tests.
2. Implement one neutral provenance/schema/projection checker.
3. Populate exact observed merge/file/blob/digest values only after the merged handoff exists.
4. Invalidate stale results and prove dependency paths have zero issue #7 diff.

## Tests Before

Write failing cases for absent files, fake/unmerged SHA, wrong ancestry, altered bytes, crossed
manifest references, schema failure, unsafe content, false cross-grain relationship, and old
browser state before implementing the check.

## Refactor

Implement one neutral read-only handoff loader/checker. Do not create data migration, fixture copy,
shared schema patch, score, or ADR decision. The actual digests remain `UNAVAILABLE/BLOCKED` in
this plan because the files do not exist at discovery SHA; only observed merged bytes may populate
the implementation record.

## Tests After

- Re-run all negative fixtures and the actual merged handoff.
- Compare logical projections from all surviving candidate adapters without writing the inputs.
- Record invalidation IDs for every provisional or stale result; ensure score fields are absent.
- Run the changed-path and protected-hash gates again.

## Regression Gate

Planned future commands:

```bash
node --test spikes/web/harness/tests/barrier-b.test.mjs
make -f mk/issue-5/i5-02.mk web-barrier-b-check I5_01_MERGE_SHA=<full-40-hex-merged-sha>
```

The target emits `.artifacts/evidence/web-spike/<run-id>/barrier-b/fixture-handoff.json` and exits
non-zero while #6 is unmerged, the SHA is not an ancestor, any file/digest/schema/reference is
missing or inconsistent, an unsafe field appears, the four-grain rule fails, a dependency file is
dirty, or invalidation is incomplete. There is no optional or synthetic success mode.

## Success Criteria

- [ ] One exact merged SHA and four exact digests open Barrier B.
- [ ] All candidate logical inputs are equal and issue #6 paths remain byte-unchanged.
- [ ] Stale/provisional evidence cannot enter Gate C or ADR-005.
- [ ] Barrier stays closed until every requirement is observed, not assumed.

## Risk, Security, and Rollback

The primary risk is provenance laundering. On drift, mark affected runs invalid, clear only scoped
browser/runtime state, remove all numeric score fields, and return to Barrier B. Preserve raw
invalidated evidence for audit; never delete/modify issue #6 or unrelated data.

## Next Steps

Gate C may start only when Barrier B passes and the browser/manual-accessibility environment is
also scheduled and available.
