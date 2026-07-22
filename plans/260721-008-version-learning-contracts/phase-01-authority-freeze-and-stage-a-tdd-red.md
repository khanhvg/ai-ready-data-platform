---
phase: 1
title: Authority freeze and Stage A TDD RED
status: completed
priority: P1
dependencies: []
stage: A
---

# Phase 1: Authority Freeze and Stage A TDD RED

<!-- Historical Stage A execution plan; released through PR #23 and PR #25, with current disposition in plan.md. -->

## Context Links

- [Plan outcome and stage decision](./plan.md#stage-decision)
- [Requirements and risk traceability](./requirements-and-risk-traceability.md)
- [Master Phase 3](../260721-005-enterprise-learning-sandbox/phase-03-shared-lesson-lab-and-evidence-contract.md)
- [Issue #6 implementation handoff](../260721-006-freeze-golden-baseline/implementation-handoff.md)

## Overview

Freeze the future readiness-authorized implementation head, exclusive lease, Issue #6 read-only
bytes, Stage A dependency boundary, and failing TDD corpus before any contract/validator behavior.
Stage A must prove it can execute with no selected-framework/Issue #7 path or ADR byte, portal or
runner implementation path, future SHA, Node/Vite dependency, browser, Docker, network, cloud
credential, or heavy profile.

## Requirements

- Functional: capture exact local/tracking/fresh-live identity, ancestry, protected hashes, command
  ownership, new-family namespace, test IDs, and expected failure reasons.
- Functional: characterize every shipped Issue #6 schema/registry/fixture/reader as read-only and
  passing before writing new behavior; capture the one discovered incompatibility that
  `fitness-result-v1` fixes `owner: I5-01` and therefore cannot represent I5-03.
- Non-functional: one writer/worktree; bounded local output; fail closed on missing required tools;
  no product/config/contracts beyond the future allow-list.
- Authority: implementation does not begin from this planner commit merely because it exists. A
  fresh independent validation and fresh readiness audit must publish the exact implementation
  input and explicitly decide Stage A cookability.
- Authority: the readiness-authorized implementation branch is
  `feature/issue-5-03-learning-contracts`, created once from the externally published audit output.
  One actor executes Phases 1-5 serially; no phase fan-out or second shared-core worktree is allowed.

## Architecture

The RED harness has three layers:

1. `authority`: repository identity, clean state, lease, protected hash and runtime-lock checks;
2. `boundary`: source/import/reference scan plus Python audit-event capture for file opens, imports
   and subprocesses; execute with forbidden Issue #7/framework/portal/runner paths absent and with
   an inert decoy tree to prove identical Stage A inputs/results;
3. `contract RED`: every fixture/test in the stable RED matrix—schema, ref, state, replay,
   completion, reconciliation, evidence/locator/tamper, canonicalization, migration, operation,
   OpenAPI, probe/hint, promotion, fitness-version, dependency and rollback failures.

The decoy test may create only marker-owned temporary bytes under the test workspace. It never
checks out or copies the unmerged Issue #7 branch. A result change caused by the decoy is
`STAGE_A_FRAMEWORK_DEPENDENCY` and a STOP.

## Related Code Files

Future implementation creates only these Phase 1 files before production behavior:

| Action | Exact path | Purpose |
|---|---|---|
| Create | `tests/contracts/learning/__init__.py` | Test package marker |
| Create | `tests/contracts/learning/test_authority_and_stage_boundary.py` | exact-head, lease, read/import/change boundary and dependency-absence tests |
| Create | `tests/contracts/learning/test_runtime_dependencies.py` | exact lock/freeze/import/manifests, `pip check`, advisory-delta and no-install RED IDs |
| Create | `tests/contracts/learning/test_schema_contracts.py` | schema RED IDs and read-only Issue #6 characterizers |
| Create | `tests/contracts/learning/test_reference_integrity.py` | missing/duplicate/cyclic reference RED IDs |
| Create | `tests/contracts/learning/test_state_and_completion.py` | illegal transition, idempotency, forged completion and dual-truth RED IDs |
| Create | `tests/contracts/learning/test_evidence_tamper.py` | hash, secret/path, recursive identity and provenance RED IDs |
| Create | `tests/contracts/learning/test_version_migrations.py` | unknown/lossy/cyclic/colliding migration RED IDs |
| Create | `tests/contracts/learning/test_openapi_contract.py` | missing/ref/matrix/auth/idempotency/no-channel RED IDs |
| Create | `tests/contracts/learning/test_promotion_trust_manifest.py` | four-grain, limitation, fixture-hash and attribution RED IDs |
| Create | `tests/contracts/learning/test_operation_matrix.py` | operation completeness/taxonomy/role/trust/evidence RED IDs |
| Create | `tests/contracts/learning/test_prerequisite_and_hints.py` | probe mutation/order/reveal/no-completion RED IDs |
| Create | `tests/contracts/learning/test_evidence_provenance.py` | locator/provenance/redaction/retention RED IDs |
| Create | `tests/contracts/learning/test_command_and_release.py` | fitness owner/version, command activation, release, provenance and rollback RED IDs |
| Create | `tests/fixtures/learning/contracts/fixture-index-v1.json` | closed ID→path→expected-error registry |
| Create | `tests/fixtures/learning/contracts/valid/private-migration-v0.json` | non-released reversible migration source vector |
| Create | [Every exact invalid fixture in the stable RED matrix](./requirements-and-risk-traceability.md#stable-tdd-red-fixture-and-failure-matrix) | complete indexed negative corpus before behavior |

No schema, validator, OpenAPI, manifest, Make, or binding file is created until the RED record is
captured. Issue #6 test/fixture files are never edited to create RED.

## Tests Before

Use the complete stable assertion/failure table in traceability, including:

```text
I8-AUTH-BASE-001        I8-AUTH-LEASE-002        I8-AUTH-PROTECTED-003
I8-STAGEA-NO-I7-010     I8-DEPS-IMPORT-181        I8-SCHEMA-CLOSED-100
I8-CANON-DUPLICATE-103  I8-REF-MISSING-110        I8-STATE-ILLEGAL-120
I8-IDEMPOTENCY-CONFLICT-122 I8-COMPLETION-FORGE-130 I8-RECONCILE-ORPHAN-132
I8-TAMPER-PAYLOAD-140   I8-MIGRATION-LOSS-151     I8-OPENAPI-MATRIX-160
I8-FITNESS-OWNER-180    I8-PROMO-GRAIN-170        I8-ROLLBACK-SCOPE-190
```

RED acceptance:

- read-only Issue #6 characterizers pass at the immutable base;
- each new behavior assertion fails for its named missing contract/validator, not import, syntax,
  fixture-index or runtime noise;
- the v1/I5-03 evidence vector fails exactly `FITNESS_RESULT_OWNER_VERSION_MISMATCH`, proving the
  additive v2 requirement before its schema/registry entry exists;
- sanitized RED evidence records exact input/dependency SHAs, test IDs, commands, tool/freeze
  hashes, pre-RED tree and expected failures;
- no generated contract or runtime artifact is staged.

## Implementation Steps

1. Prove the future implementation branch/worktree is absent, create it once from the externally
   published readiness output, push that unchanged branch with upstream tracking, then fresh-fetch
   and compare local, upstream and live remote full SHA. Verify required ancestry, clean status and
   the sole shared-core lease.
2. Verify the fresh readiness output explicitly authorizes either full I5-03 or bounded Stage A,
   names the exclusive lease, exact paths, tests and rollback, and has not been superseded.
3. Before tracked RED writes, verify the manifest-admitted Issue #6 golden runtime and exact
   package/freeze/lock identities from traceability. If absent, stop; only the existing I5-01
   `make golden-clean PROFILE=small SEED=42` pre-cook dependency step may establish it. Then hash
   every tracked Issue #6 contract, reader, lock, Make fragment and promotion-trust fixture;
   record `docs/code-standards.md` absent/present state without changing it.
4. Prove the root Make wildcard already exposes issue fragments and that every I5-03 public target
   has one registry owner while `evidence-contracts-check` remains I5-01-owned.
5. Write the fixture index and test modules. Run only the read-only characterizers first, then the
   intended RED suite.
6. Run the Stage A boundary test with Issue #7/framework/portal/runner paths unavailable, then with
   inert marker-owned decoys. Require identical allowed open/import/subprocess event sets, selected
   inputs, canonical outputs and failure IDs; any forbidden read/import is a STOP even if output is
   unchanged.
7. Finalize bounded RED evidence below
   `.artifacts/evidence/learning-contracts/<run-id>/tdd/red/` and leave the tree ready for Phase 2.

## Success Criteria

- [ ] Exact future implementation authority and one lease prove valid.
- [ ] All Issue #6 protected hashes and read-only characterizers pass.
- [ ] Every named RED assertion fails for the intended missing behavior.
- [ ] Stage A has zero selected-framework/Issue #7/ADR/portal-internal/runner-internal imports,
  refs, reads or output influence and no future SHA input.
- [ ] Every Stage A negative and every Stage A test module exists before production behavior.
- [ ] RED evidence is schema-valid, sanitized, bounded and tied to exact SHAs/tool hashes.
- [ ] Changed paths contain only the Phase 1 tests/fixtures; no behavior file exists yet.

## Risk Assessment

- A stale/unmerged Issue #7 path can leak into a “neutral” contract through copied preview schema.
  Mitigation: dependency-absent and decoy invariance checks; never import preview definitions.
- Pre-creating schemas can produce performative RED. Mitigation: capture missing-behavior failures
  before every production file and refuse syntax/import-only failures.
- New tests could mutate tracked fixtures. Mitigation: copy inputs into marker-owned temp roots and
  verify exact pre/post hashes.

## Security and Rollback

Wrong base, missing lease, protected drift, unadmitted tool, secret/private-path finding, or a
Stage A dependency on Issue #7/framework/portal/runner implementation stops work. Secret/PII and
absolute-private-path canaries are generated only in private test roots, never tracked. Rollback
removes only marker-owned ignored RED scratch workspaces when policy allows; retained failure
evidence and all tracked inputs remain.

## Next Steps

Proceed to Phase 2 only after RED provenance is complete and the behavior-file absence check passes.
