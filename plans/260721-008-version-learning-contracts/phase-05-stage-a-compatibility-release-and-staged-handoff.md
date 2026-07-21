---
phase: 5
title: "Stage A compatibility release and staged handoff"
status: pending
priority: P1
dependencies: [4]
stage: "A"
---

# Phase 5: Stage A Compatibility, Release, and Staged Handoff

<!-- Updated: Validation Session 1 - truthful fitness v2, exact gates, rollback and review authority. -->

## Context Links

- [Stage decision](./plan.md#stage-decision)
- [Command/evidence matrix](./requirements-and-risk-traceability.md#command-and-evidence-matrix)
- [Issue #6 migration/rollback handoff](../260721-006-freeze-golden-baseline/implementation-handoff.md#curated-release-migrationrollback-handoff)

## Overview

Close all Stage A RED assertions, expose the registered Issue #8 commands through its disjoint Make
fragment, prove backward reading and Issue #6 immutability, run the full local blast radius, and
produce a non-recursive Stage A contract-set/evidence handoff. Then stop for fresh independent
validation/readiness. This phase assesses whether Stage A is a merge candidate; it does not approve
or merge it.

## Requirements

- Functional: one bounded check runner emits `fitness-result-v2` with `owner: I5-03` on pass/fail
  and validates the new learning-contract release, OpenAPI and promotion manifest. Shipped v1
  remains unchanged/readable for I5-01.
- Functional: public targets exactly match the immutable I5-03 ownership reservations plus their
  hash-bound activation overlay; no root Make edit and no duplicate I5-01
  `evidence-contracts-check` recipe.
- Functional: every shipped Issue #6 family remains readable with exact schema/fixture/reader bytes;
  new families have identity readers and private reversible migration vectors.
- Functional: a tracked contract-set document hashes all Issue #8 Stage A source contracts but does
  not recursively contain its own file/commit digest. Exact tested/attestation/merge identities are
  recorded in generated evidence and external GitHub attestations.
- Non-functional: primary and blast-radius commands are bounded, non-interactive, local, safe on
  16 GiB, and pass after install with network/cloud credentials absent.
- Non-functional: dependency/advisory proof is the immutable lock/freeze/manifest/import inventory
  plus `pip check` and an explicit inherited-advisory disposition; no new package/scanner, network
  fetch or automated dependency fix is introduced.

## Architecture

`scripts/learning_contracts/check.py` dispatches four registered public behaviors:

- `learning-contracts-check`: schemas, registry, refs, state, completion, probes, hints, migrations,
  promotion manifest and Stage A/B boundary;
- `lesson-check`: exact lesson ID manifest/fixture contract;
- `api-contracts-check`: OpenAPI profile/refs/examples/matrix/no-channel inventory;
- `evidence-verify`: validate one emitted learner or fitness evidence locator read-only.

The Make fragment is a thin wrapper using `env -u PYTHONPATH PYTHONDONTWRITEBYTECODE=1 python3.12`.
The runner locates a previously verified manifest-admitted Issue #6 golden environment or fails
`GOLDEN_RUNTIME_REQUIRED`; it never silently installs, rewrites a lock or uses an ambient package.

The immutable `command-owner-registry-v1.json` already lists all four I5-03 command names and
owners, so `make help` remains name/owner discovery-compatible. Because those rows truthfully described the
Issue #6 snapshot as `future-owner`, Stage A adds
`command-owner-activation-i5-03-v1.json`: a closed overlay containing base command-registry SHA-256
`a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80`, the
four exact rows, `availability=implemented`, the I5-03 fragment hash and `fitness-result-v2`. I5-03
checks compose that overlay; the Issue #6 registry/help reader stays byte-for-byte unchanged.
Consequently `make help` continues to display the immutable snapshot’s `future-owner` availability
for I5-03; that output is an expected compatibility view, not the activation truth. The Issue #8
check runner must validate the overlay as the sole I5-03 availability/evidence-version authority.

### Version and release semantics

- New v1 is the first released version of each Issue #8 family; no fictional v0 is tracked.
- `fitness-result-v2` is an Issue #8-owned extension of the existing family, not a new v1: it
  retains the base v1 schema/hash/reader unchanged, is selected only by the Issue #8 dispatcher,
  represents I5-03 truthfully and is never down-converted to v1.
- Private migration vectors prove the engine can traverse a lossless edge and reject loss/cycles.
- Future version admission must add a schema, readable-version/identity edge and any genuinely
  required additive reader support, keep every prior version readable, provide lossless rollback or
  declare a STOP/new fixture decision, and dual-run before an owner-scoped emit-version change.
- `learning-contract-set-v1.json` records path/family/version/schema/content hashes of the release
  inputs. Its own byte hash and the tested tree/attestation/merge SHAs live outside that document.
- A Stage A merge, if separately authorized, gets one externally recorded
  `STAGE_A_CONTRACT_RELEASE_SHA`. It does not complete Stage B or Issue #8.

## Related Code Files

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/learning-contract-set-v1.schema.json` | closed non-recursive release-set shape |
| Create | `learning/contracts/learning-contract-set-v1.json` | paths/families/versions/hashes for Stage A sources |
| Create | `learning/contracts/command-owner-activation-i5-03-v1.json` | exact base-command-registry-bound activation of four reserved I5-03 rows |
| Create | `scripts/learning_contracts/check.py` | bounded suite dispatch and result production |
| Create | `scripts/learning_contracts/runtime.py` | read-only manifest-admitted runtime discovery/freeze check |
| Create | `scripts/learning_contracts/fitness.py` | closed I5-03 `fitness-result-v2` pass/fail builder; v1 regression reader stays external/read-only |
| Create | `mk/issue-5/i5-03.mk` | four I5-03 recipes only |
| Modify | `learning/contracts/learning-contract-version-registry-v1.json` | add learning contract-set and command-activation families after their schemas stabilize |
| Modify | `tests/contracts/learning/test_command_and_release.py` | close owner/activation/recipe/set/provenance/changed-path/rollback RED IDs |
| Modify | `tests/contracts/learning/test_runtime_dependencies.py` | close lock/freeze/import/`pip check`/advisory-disposition RED IDs |

The command registry itself is Issue #6-owned and read-only. If its current I5-03 declarations do
not exactly support the required targets, stop for serialized authority rather than modifying it.

## Tests Before

- `learning-contracts-check` fails until all new schemas/docs/validators/manifest/release entries
  exist and all Phase 1 RED IDs are closed.
- Command tests fail duplicate owner/recipe, root Make diff, unregistered target, ambient runtime,
  wrong freeze/lock, activation/base-command-registry mismatch, invalid v1/I5-03 evidence and missing safe
  failure evidence.
- Release tests fail self digest/attestation/merge identity, unhashed/extra/missing path, wrong hash,
  family collision and unadmitted owner-scoped emit-version change.
- Compatibility tests fail on any changed Issue #6 byte, unreadable old family/fixture or migration
  coercion/drop.

## Refactor

Keep Make recipes declarative and the Python runner deterministic. One test inventory drives direct
unit tests and public commands so public checks cannot omit a negative suite. Do not merge the
existing I5-01 runner, change its owner field, or create a root package workspace.

## Tests After and Blast Radius

Run the primary issue contract exactly as one invocation at one clean committed testable head:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
```

Then run the remaining blast radius in this order:

```bash
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
```

Then:

1. obtain the evidence locator printed by `learning-contracts-check`;
2. run `make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"`;
3. rerun all three primary commands with network access unavailable and AWS/cloud environment
   variables absent, reusing only the verified local locked environment;
4. run exact lock/freeze/import/manifest, `pip check`, inherited-advisory disposition, changed-path,
   protected-hash, credential/private-path and AsyncAPI/channel inventory scans;
5. compare Stage A results with Issue #7 paths absent and with the inert decoy; require equality;
6. rehearse rollback in a disposable marker-owned copy and prove the previous Issue #6 readers/
   fixtures and tree remain intact.

Required missing runtime/tool/evidence is `fail`; no `not-run-optional` applies to Stage A. No
Docker, browser, Node install, data generation, service, AWS or Terraform command runs.

### Exact rollback rehearsal

Tracked rollback is a reviewed owner-scoped emit/fallback selection change, never file deletion of a
released schema/reader/evidence record. Runtime cleanup first enumerates the marker-bound Issue #8
run manifest, verifies root device/inode/nonce, refuses symlink/hardlink/special-file/foreign marker
or any path outside `.artifacts/{workspaces,evidence}/learning-contracts/<run-id>/`, and removes only
listed mutable workspace bytes. Committed/failure evidence is retained. The rehearsal places
unrelated and foreign-marker sentinels beside/inside candidate roots, exercises partial failure,
then proves their device/inode/content hashes plus every Issue #6 fixture/v1 reader and the Issue #8
dispatcher’s v1/v2 results are unchanged. `I8-ROLLBACK-SCOPE-190` requires refusal before deletion;
broad glob, recursive repository cleanup, reset, migration down, evidence rewrite and last-write rollback
are forbidden.

## Implementation Steps

1. Add release-set schema/document and exact content hashes after the Stage A files stabilize.
2. Implement verified-runtime discovery and bounded fitness/evidence result generation.
3. Add the command-activation overlay, disjoint Make recipes and command/release/compatibility tests.
4. Close every RED ID without changing the test intent; run focused suites first.
5. Commit the exact testable source head before final evidence; run the ordered primary/blast
   checks from that clean head and retain bounded artifacts.
6. Run rollback and Stage A dependency-independence proofs.
7. Produce a sanitized Stage A handoff report in generated evidence containing input/tested tree,
   schema/fixture/contract-set hashes, commands/tools, protected result and rollback result.
8. Stop. A fresh readiness auditor decides whether any Stage A cook scope is allowed. After
   implementation, at least one fresh independent exact-head read-only review and a separate human
   exact-head pre-merge approval are mandatory before PR merge; neither may be synthesized.

## Stage A Independent-Merge Decision Record

Planner answer: **Stage A can be an independently merged candidate in principle**, because every
planned input is present at the shipped Issue #6 integration and every planned output is
framework-neutral. This is conditional, not authorization. Before any staged merge, all must hold:

- this independent validation proves the corrected plan and zero Issue #7/framework/portal-runner-
  internal byte use; it does not authorize implementation;
- fresh readiness explicitly authorizes Stage A’s exact files, commands, branch/head and rollback;
- implementation evidence passes at one exact clean head and at least one fresh independent
  exact-head read-only review passes unconditionally;
- repository-required checks and a repository-authorized human approve that exact head;
- Stage A merge/release SHA is observed remotely and recorded externally;
- Issue #8 remains incomplete and Stage B/downstream authorization stays blocked unless separately
  cleared.

Any missing condition means “not cookable/mergeable yet,” not a planner waiver.

## Success Criteria

- [ ] All primary and blast-radius gates pass at one exact committed head.
- [ ] Public commands/owners are exact; root Make and Issue #6 fragments are unchanged.
- [ ] Existing contracts/fixtures/readers remain byte-identical and readable.
- [ ] New v1 families, additive fitness v2, retained v1 reader, private migrations, activation
  overlay and release set are closed and non-recursive.
- [ ] No framework/ADR bytes, network/cloud credentials, new runtime or heavy service are needed.
- [ ] Rollback preserves retained evidence and Issue #6 state.
- [ ] Stage A handoff says candidate-only and names fresh validation/readiness/human gates.

## Risk Assessment

- A clean command can depend on an old generated golden runtime. Mitigation: verify freeze/lock and
  record provenance; fail rather than install or trust ambient `.venv`.
- A release-set hash can become recursively impossible. Mitigation: exclude own byte/commit hash;
  external evidence binds it to tested/attestation/merge identities.
- Staged merge can be confused with full I5-03 completion. Mitigation: explicit external status,
  no Vite binding, and continued Stage B/dependency gate.

## Security and Rollback

Sanitize bounded stdout/stderr before evidence publication. Rollback uses only marker-verified
Issue #8 generated roots and a reviewed owner-scoped selection switch; never broad delete/reset,
fixture rewrite, old-reader deletion or protected-path mutation.

## Next Steps

If and only if independent gates later authorize and publish Stage A, wait for the exact merged
Issue #7 Vite ADR/handoff before Phase 6. No work may bridge the gap using provisional bytes.
