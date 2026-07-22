# Issue #6 Fixture Handoff

## Current Barrier Status

`BLOCKED` at issue #7 discovery SHA `a39251d45a56124322b9143ad16b926b2656073b`.
GitHub issue #6 is open/`triaged`, and all four required tracked files are absent. Therefore no
merge SHA or file digest is available to record. This is an explicit dependency state, not a
placeholder that implementation may fill with synthetic or ignored bytes.

## Exact Required Inputs

| Dependency path | Owner | Required digest at Barrier B | Consumption |
|---|---|---|---|
| `contracts/data/retail-golden-v1.json` | I5-01 / #6 | `UNAVAILABLE until merged; record SHA-256 of observed merged bytes` | Read-only golden contract |
| `contracts/data/promotion-trust-v1.yaml` | I5-01 / #6 | `UNAVAILABLE until merged; record SHA-256 of observed merged bytes` | Read-only four-grain query/assertion contract |
| `tests/fixtures/learning/promotion-trust/evidence-v1.json` | I5-01 / #6 | `UNAVAILABLE until merged; record SHA-256 of observed merged bytes` | Read-only sanitized evidence fixture |
| `tests/fixtures/learning/promotion-trust/manifest.json` | I5-01 / #6 | `UNAVAILABLE until merged; record SHA-256 of observed merged bytes` | Read-only producer/contract/fixture/tool/retention manifest |

The Barrier B record must additionally include each Git blob ID, the full 40-character issue #6
merge SHA, tested tree SHA, producer SHA declared by the manifest, schema result/version, lesson
ID/version, fixture kind `tracked-real`, and exact cross-file references.

## Merge Gate

Barrier B opens only when all conditions are true:

1. A reviewed issue #6 change is merged into the integration history used by issue #7.
2. `I5_01_MERGE_SHA` resolves to a commit and is an ancestor of the tested issue #7 HEAD.
3. All four paths are tracked at that merge/current tree; no ignored/untracked/worktree-local copy
   participates.
4. SHA-256 and Git blob values are computed from the exact merged bytes and match the manifest's
   internal references.
5. Issue #6's schema/data/evidence validation result is present, and the issue #7 neutral adapter
   independently validates the read-only handoff.
6. The promotion-trust contract exposes four independent grains and the expected bounded result
   `insufficient evidence`; it contains no causal cross-mart join.
7. Changed-path evidence proves issue #7 did not edit any dependency/shared path.

The planned command is:

```bash
make -f mk/issue-5/i5-02.mk web-barrier-b-check I5_01_MERGE_SHA=<full-40-hex-merged-sha>
```

It writes the canonical record to
`.artifacts/evidence/web-spike/<run-id>/barrier-b/fixture-handoff.json` and the frozen safe copy of
its digest metadata to `spikes/web/harness/fixture-handoff.json`. It exits non-zero for any absent,
unmerged, dirty, mixed, unsafe, schema-invalid, causally invalid, or internally inconsistent input.

## Required Manifest/Schema Checks

- Producer commit and merge provenance are non-empty full SHAs and consistent with ancestry.
- Contract and fixture SHA-256 strings are lowercase 64-hex and match bytes.
- Evidence/manifest use safe relative paths and known schema versions.
- Ordered fixture records are deterministic; normalized fixture time is not wall-clock generated
  during the candidate run.
- Every mart evidence declaration includes source mart, grain, time scope, filters, numerator,
  denominator, weighting/aggregation, limitations, and evidence reference.
- Unknown security-sensitive fields, raw source data, secrets/PII, absolute paths, executable
  content, remote URLs/imports, and browser/private credentials are rejected.
- Promotion, fulfillment, returns, and DQ objects remain independent; no common key/relationship
  pretends causal attribution.

## Read-Only Adapter Rule

Issue #7 may mirror or generate candidate-local types under `spikes/web/**`, but may not change
the shared schema, contract, fixture, or manifest. Every candidate maps the same neutral logical
projection. If a field cannot be consumed consistently:

1. stop the affected target and timer;
2. retain the failing adapter/schema evidence;
3. coordinate a correction with the #6 owner under its authority;
4. wait for a new merged SHA;
5. update the Barrier B record and rerun every surviving candidate.

A candidate-specific fixture, type assertion without runtime validation, ignored file, hardcoded
surrogate, or shared edit is not a workaround and cannot pass.

## Invalidation Behavior

Any change to issue #6 merge SHA, any file/blob/SHA-256, schema version/result, candidate mode,
common test-ID digest, or projection output after Barrier B:

- closes Barrier B immediately;
- marks every real-fixture measurement, score, screenshot, trace, manual review, browser state,
  and ADR input tied to the old set `invalidated`;
- removes all old numeric scores/winner selection from active decision data;
- safely clears only candidate-scoped runtime/browser state bound to old digests;
- retains the old raw record in an `invalidated` index with reason/time/superseding handoff;
- requires clean installs/builds and the identical all-survivor Gate C rerun.

Provisional synthetic evidence remains retained and labelled but never becomes decision evidence.
No partial candidate result or unaffected-looking category survives a mixed handoff.

## Failure and Rollback

Barrier B failure leaves the neutral preview runnable, Gate C/D blocked, scorecard without a
winner, ADR-005 Proposed, and I5-05 blocked. Rollback removes only issue-owned generated adapter/
runtime state, preserves all evidence and dependency bytes, and never edits #6, shared contracts,
root Make, protected files, portal, or runner paths.
