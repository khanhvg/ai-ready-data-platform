---
phase: 5
title: "Prove Recovery Blast Radius and Release Handoff"
status: pending
priority: P1
dependencies: [4]
effort: "L"
---

# Phase 5: Prove Recovery Blast Radius and Release Handoff

## Overview

Prove ownership-safe failure recovery with an actual foreign Compose sentinel, complete evidence
under released authority, run exact dependency/golden blast radius, update only bounded user docs,
and rehearse non-destructive rollback. This phase hands evidence to the later release owner; it
does not edit the release manifest, create a PR or merge.

## Context Links

- [Requirements and traceability](./requirements-and-traceability.md)
- [TDD, fitness, evidence, migration, and recovery](./tdd-fitness-evidence-recovery.md)
- [S3 threat model](./threat-model.md)
- Phase 4 complete or typed-blocked live evidence

## Requirements

- Functional: actual foreign project/container/network/volume/port sentinel remains byte/label/
  identity unchanged through failed/interrupted run and repeated teardown.
- Functional: remove only run-owned project/container/network/ephemeral volume/temp/process/port/
  log bytes; preserve retained evidence/data and foreign objects.
- Functional: current/N-1 evidence readers and additive migration/rollback behave exactly under
  released authority.
- Functional: run four exact I5-08 commands plus exact #10/#12/golden blast radius.
- Non-functional: root/shared/contracts/views/portal/runner/labs/migrations/golden semantics,
  release manifest, code standards and unrelated Compose/docs stay protected.
- Non-functional: docs state measured facts/blocks with exact date/head/normalization; no synthetic,
  portability, cost, cloud or production claim.

## Architecture

Recovery targets are selected by immutable ownership manifest plus engine labels, never ambient
Compose env, default project or name glob. Evidence completion occurs after teardown, residue,
rollback and protected checks. Bounded docs consume final summaries only. The later I5-13 release
owner consumes this bundle read-only.

## Related Code Files

- Finalize: `scripts/profiles/teardown.py`, `scripts/profiles/measure.py`, `scripts/profiles/admit.py`
- Finalize: `tests/profiles/**`, `tests/compose/**`, `mk/issue-5/i5-08.mk`
- Conditionally modify: `README.md`, `docs/demo-runbook.md`, `.env.example`
- Runtime evidence: `.artifacts/evidence/local-profiles/<run-id>/`
- Protected/read-only: root `Makefile`, `release-manifest.json`, `docs/code-standards.md`, shared
  contracts/registries, portal/runner/labs/migrations/golden/architecture, unrelated docs/Compose

## Tests Before

- `LP-RECOVERY-FOREIGN-SENTINEL-016` and `LP-EVIDENCE-INTEGRITY-021` RED before recovery logic.
- N-1/current migration, interrupted cleanup and retained-evidence cases RED.
- Protected path/hash and dependency blast-radius baseline frozen at exact Stage A input/head.

## Refactor

Consolidate all deletion through one ownership verifier; no cleanup logic remains in sampler/admit
beyond calling teardown. Keep evidence publication atomic and schema-driven. Do not copy released
completion/reader code or fork shared contracts.

## Tests After

- Create a uniquely labelled foreign sentinel project with bounded harmless resources on the
  admitted engine; capture exact IDs/labels/volume bytes/port state.
- Force bounded failure and interruption in a separate run-owned project, run teardown twice, and
  prove only run-owned ephemeral state is gone.
- Verify evidence/retained data and foreign sentinel unchanged; then remove the sentinel only by
  its own explicitly scoped test cleanup.
- Run tamper/replay/truncation/duplicate/stale/N-1/current/rollback reader cases.
- Run final commands, dependency/golden blast radius, protected hash, secret/private-path,
  placeholder/link and clean-tree checks.

## Regression Gate

```bash
make compose-check compose-security-check profile-budget-check recovery-test
```

Then exact dependency amendment commands for passing merged #10, released #12 and golden/shared
blast radius. If Stage B engine acceptance is blocked, final Issue #13 acceptance remains blocked
even when static commands/core pass.

## Implementation Steps

1. Implement manifest+label+nonce ownership verification and a dry enumeration result before any
   delete action.
2. Add interrupted/idempotent cleanup and mismatched/missing manifest denial.
3. Run actual foreign sentinel recovery scenario; retain before/after hashes and residue.
4. Validate raw/summary/index/completion/tamper/replay and current/N-1 reader behavior under exact
   released authority.
5. Rehearse rollback to the exact pre-I5-08 dependency-amended configuration in a disposable
   branch/workspace or non-destructive config selection; do not reset/delete user work.
6. Run the four exact fitness commands and all exact dependency/golden/shared-contract commands.
7. Compare diff against future writable allowlist and protected manifest. Stop on any extra path or
   semantic/hash drift.
8. Update only root README/demo runbook/.env example where final behavior requires it. Record exact
   supported commands, core independence, loopback endpoints, allowed combinations, resource
   bounds, engine-blocked behavior, evidence location and ownership-safe teardown.
9. Complete evidence only after rollback/protected/residue checks; retain it for I5-13.
10. Obtain required independent security/review/human approvals in their separate workflows before
    any future PR/merge. This phase itself creates neither.

## Success Criteria

- [ ] Actual foreign sentinel survives failed/interrupted run and repeated teardown unchanged.
- [ ] Only exact run-owned ephemeral resources are removed; retained evidence/data survive.
- [ ] Current and N-1 readers, tamper/replay rejection and rollback pass under released authority.
- [ ] Four exact I5-08 commands and all exact dependency/golden blast-radius commands pass at one
  clean head, or heavy acceptance is explicitly blocked with no false pass.
- [ ] Diff is confined to exact future allowlist; protected hashes/semantics are unchanged.
- [ ] Bounded docs match actual behavior/evidence and make no cloud/production/general portability
  claim.
- [ ] Evidence bundle is complete, hash-indexed, strict-locator, private/redacted and recoverable.
- [ ] Rollback is bounded, non-destructive and verified.

## Risk Assessment

Cleanup is the highest destructive risk. Require two independent ownership facts and enumerate
before delete. A test cleanup must remove the foreign sentinel only after its preservation proof
and by its own exact project identity. Never use broad `down -v`, volume prune, name glob or repo
cleanup.

## Security Considerations

Evidence is retained but sanitized/private. Docs contain no local absolute paths, tokens, image
credentials or private logs. Human pre-merge approval and separate validation/readiness/security
review remain mandatory and cannot be inferred from passing tests.

## Next Steps

Hand the exact bundle/head/rollback to I5-13 release evidence. If blocked, keep Issue #13 blocked
for implementation/release while preserving Docker-free core and all diagnostic evidence.
