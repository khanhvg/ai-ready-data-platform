---
phase: 1
title: "Freeze exact authority and capture real-path RED"
status: pending
priority: P1
dependencies: []
stage: "B"
---

# Phase 1: Freeze Exact Authority and Capture Real-Path RED

## Context Links

- [Verified inputs](./plan.md#verified-inputs)
- [Exact implementation allow-list](./plan.md#exact-implementation-allow-list)
- [Stable RED catalog](./requirements-and-risk-traceability.md#stable-real-path-red-catalog)
- [Requirement audit](./audit/post-stage-a-requirement-audit.md)

## Overview

Freeze the exact Stage A/Issue #6/Issue #7 release bytes, sole shared-contract writer, protected
hash inventory, and eight invalid binding fixtures before any binding schema, reader, or document
exists. The RED suite must reproduce the observed identifier mismatch from real released paths;
synthetic-only or guessed mappings do not qualify.

## Requirements

- Local HEAD, tracking branch, fresh live integration ref, and authorized implementation input all
  equal `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; tree/index are clean before RED writes.
- PR #22 and PR #23 merge SHAs are ancestors; Issue #7 is closed/shipped; Issue #8 is open with the
  I5-03 lease and no conflicting writer.
- Rehash every exact input in the plan and all 21 Stage A contract-set members before writes.
- The Stage A manifest must still yield `region`,`category`,`dq`; Issue #6 evidence and Issue #7
  source must still yield `region_name`,`category_name`,`data-quality` in the exact order.
- Create only the Stage B test module and eight invalid fixtures. The binding schema/document and
  reader/module must be absent for the initial RED run.
- RED evidence records exact input/dependency SHAs, source hashes, test IDs, expected failure codes,
  tool versions, protected hashes, and bounded sanitized logs.

## Tests Before

`tests/contracts/learning/test_vite_consumer_binding.py` first freezes:

- `I8B-AUTH-001` exact input/live/ancestry/clean/lease authority;
- `I8B-PROTECTED-002` Stage A/Issue #6/Issue #7 protected hash equality;
- `I8B-MISMATCH-010` the exact released source mismatch is present and no binding path exists;
- `I8B-BINDING-ABSENT-011` fails `VITE_BINDING_REQUIRED` before behavior;
- all invalid-fixture IDs `I8B-ALIAS-020` through `I8B-BOUNDARY-027` fail for the exact codes in
  traceability, not for import, syntax, missing dependency, or fixture metadata noise;
- `I8B-NO-COPY-030` fails any attempted copied schema/default/value/record/operation/completion rule;
- `I8B-NO-GENERATED-TYPES-031` proves no Issue #8 `.ts`, `.tsx`, `.d.ts`, portal, or runner output.

The focused test command is:

```bash
python3 -m unittest tests.contracts.learning.test_vite_consumer_binding
```

Expected RED: the real-path characterization passes, then product assertions fail because the
binding schema/document/reader are absent. All eight negative fixtures are enumerated by exact
path; missing/extra fixture is `BINDING_FIXTURE_INDEX_INCOMPLETE`.

## Exact Phase Allow-List

| Action | Exact path |
|---|---|
| Create | `tests/contracts/learning/test_vite_consumer_binding.py` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/absolute-path.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/completion-authority-override.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/contract-key-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/dependency-hash-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/duplicate-target-key.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/fixture-key-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/grain-id-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/raw-record-leak.json` |

All product/behavior files are forbidden in Phase 1.

## Implementation Steps

1. Fresh-fetch and prove exact local/tracking/live input, required ancestry, clean state, branch,
   issue/PR states, and exclusive lease.
2. Hash all protected inputs and verify the Stage A 21-entry set byte-for-byte.
3. Run the released Issue #7 focused Node suite read-only; retain its five passing test names and
   exact source/fixture hashes.
4. Create the test module and eight closed input-only fixtures; do not put expected outcomes inside
   fixture bytes.
5. Run read-only characterizers, then the RED suite. Reject syntax/import-only failures.
6. Scan changed/opened paths, subprocesses, secrets/private paths, and output/resource ceilings;
   retain bounded RED evidence and stop before Phase 2 if any boundary fails.

## Success Criteria

- [ ] Exact authority, ancestry, live ref, clean state, and single writer pass.
- [ ] Protected input hashes and all 21 Stage A set members pass.
- [ ] The exact cross-release mismatch is reproduced from real files.
- [ ] All stable RED IDs fail for intended missing/invalid binding behavior.
- [ ] Only the nine Phase 1 test/fixture paths change; no behavior path exists.
- [ ] RED evidence is bounded, sanitized, hash-bound, and contains no future SHA.

## Security and Rollback

Phase 1 reads only public/repository-relative source paths. It executes one dependency-free Node
test and one Python test; no npm install, network, browser, service, cloud credential, AWS,
Terraform, or mutation outside test-owned temp/evidence roots. Rollback removes only uncommitted
Phase 1 paths and marker-verified ignored scratch data; retained failure evidence and all released
inputs remain.

## Next Steps

Proceed to Phase 2 only after valid real-path RED provenance exists and the behavior-file absence
check passes.
