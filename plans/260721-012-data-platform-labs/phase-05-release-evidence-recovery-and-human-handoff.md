---
phase: 5
title: "Release Evidence, Recovery, and PR Handoff"
status: pending
priority: P1
dependencies: [2, 3, 4]
externalDependencies: [issue-8-released-contracts, issue-9-released-runner-and-data-lease, issue-10-passing-merged-real-journey]
effort: "unresolved until all stage amendments pass"
---

# Phase 5: Release Evidence, Recovery, and PR Handoff

## Context links

- [Plan](./plan.md)
- [Requirements traceability](./requirements-traceability.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Protected baseline](./protected-baseline-manifest.md)

## Overview

Consolidate deterministic evidence, rollback/cleanup proof, dependency blast radius and Standard
review/test/PR handoff. Phase này không nới dependency authority và không biến optional unavailable
evidence thành pass.

## Requirements

### Functional

- Run full Vietnamese-first foundation→mid journey: prerequisite → starter → task → controlled
  failure → hints → verify → evidence → reset → solution → reflection.
- Prove additive migration/N-1 reader compatibility, atomic pointer rollback, Iceberg snapshot/
  orphan recovery and OpenMetadata exact-set rollback.
- Prove cleanup deletes only run-owned bytes/entities and preserves evidence/foreign sentinels.
- Produce evidence hash/index bound to exact input/tested tree, #6/#8/#9/#10 SHAs, content,
  registry, verifier and service versions.
- Prove a pristine detached checkout can reproduce required gates without prior workspace,
  generated data or retained runtime evidence.
- Retain a redacted observability projection binding run/operation/fault boundary, typed failure,
  resource ceilings, remediation and final result to the evidence index.
- Record docs/release impact as `none` or exact separately owned paths/review gates; protected root
  release/code-standard files remain untouched without separate authority.

### Non-functional

- Serial 16GB profile. Core no Docker/cloud requirement; heavy optional profiles one at a time.
- Required missing dependency/tool/test fails. Optional absence may be `not-run-optional` only and
  cannot support a service-backed pass/completion claim.
- Focused review and fresh tests bind the delivery head; any later change reruns affected review
  and tests before merge.

## Architecture

Release evidence is append-only and indexed by hashes. Completion references only a fresh,
schema-valid evidence record from the exact tested tree. Rollback switches to known complete
manifest/snapshot/managed-set/reader state; it never resets the repository or deletes unrelated
state.

## Related code files

- Modify: exact Stage A/B/C implementation paths recorded by amendments.
- Verify: `mk/issue-5/i5-07.mk` owns Issue #12 recipes; root Makefile unchanged.
- Preserve: protected baseline and every path outside exact amendments/leases.
- Exact current implementation path/command list: empty except user-defined future final verify
  contract documented below.

## Implementation steps

1. Confirm the relevant Standard-lane dependency amendment is an exact ancestor; confirm active
   leases and no concurrent writer.
2. Run two serial deterministic core journeys in disjoint private run roots; compare semantic
   evidence and protected trees.
3. Run real service-backed fault/recovery suites in the admitted local topology; record explicit
   optional unavailable states separately.
4. Rehearse rollback for reader/migration, current pointer, Iceberg snapshot/orphans,
   OpenMetadata managed set, progress and workspace reset.
5. Verify evidence index/artifact hashes, tamper/replay/tree/dependency mismatch and redaction.
6. Run final four-command contract and exact released #6/#8/#9/#10 blast radius serially.
7. Verify changed paths, protected objects, private/credential/PII scan, no AWS/Terraform/cloud
   action, and clean run-owned cleanup.
8. Run the exact required gates from a pristine detached checkout, verify observability closure,
   and complete the docs/release-impact disposition (`DL-CLEAN-001`, `DL-OBS-001`, `DL-DOC-001`).
9. Run focused code review (`DL-REV-001`) in the same delivery context; require zero unresolved
   Critical/Important findings.
10. Run fresh focused and blast-radius tests (`DL-TEST-001`) on the reviewed head, open/update the
   PR, require CI, merge only through the authorized workflow, then run post-merge smoke
   (`DL-MERGE-001`).

## Final verify contract

```bash
make data-labs-e2e lake-fault-test metadata-reconcile-test data-contracts-check
```

Append exact released blast-radius commands; do not substitute similar targets. If a required
target is missing, fail. If real Iceberg/OpenMetadata evidence has never passed, those labs cannot
be published as verified even when the core lane passes.

## Tests before

- Every stable behavior ID has a retained real RED and stage GREEN evidence.
- Baseline characterization and protected hashes pass before rollback/fault rehearsal.

## Refactor

No broad release abstraction. Consolidate evidence/index/rollback helpers only within released
contracts and exact leases; preserve N-1 readers/adapters until compatibility proof is complete.

## Tests after

- Full stable-ID suite and exact final command.
- #6/#8/#9/#10 exact blast radius.
- Two serial core evidence projections.
- Real Iceberg/OpenMetadata fault, conflict, orphan, reconciliation and rollback evidence.
- Protected paths, secret/private/PII, evidence tamper/replay and cleanup scope.

## Success criteria

- [ ] Final command and exact dependency blast radius pass at exact tested head.
- [ ] Every requested behavior has stable-ID RED/GREEN/recovery evidence.
- [ ] Core is serial/Docker-free/cloud-free; optional status is honest.
- [ ] Additive migration, old readers, atomic rollback and run-only cleanup are proven.
- [ ] Evidence hash/index detects tamper/replay and contains no secrets/PII/private paths.
- [ ] Pristine-checkout reproduction, redacted observability closure and explicit docs/release
      impact disposition pass.
- [ ] Focused review has zero Critical/Important findings; fresh tests, PR/CI and post-merge smoke
      are recorded.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Core pass hides skipped service labs | False release | Separate service-backed publication gate; `not-run-optional` is non-pass |
| Evidence retained but mutable/incomplete | False completion | Append-only artifacts + hash index + live verifier |
| Rollback deletes foreign state | Data loss | Exact run ownership; refusal on mismatch |
| Local artifacts make the gate pass only in the author workspace | Non-reproducible release | Pristine detached checkout with exact released setup/test authority |
| Missing telemetry or implicit docs/release ownership hides failure | Unreviewable handoff or protected-path drift | Redacted observability projection plus explicit `none`/exact owner disposition |
| Head changes after review/test | Stale evidence | Rerun affected review/tests before merge |
| Final command omits dependency regressions | Blast-radius escape | Append released exact commands from all four dependencies |

## Security considerations

Threat disposition in [risk model](./risk-and-threat-model.md) must be fully green or explicitly
blocked. Local hash is integrity, not authenticity. No cloud/AWS/Terraform action, destructive
repository operation, PR or merge is implied by this plan.

## Next steps

Use the Standard delivery context for focused review, fresh tests, PR/CI, authorized merge and
post-merge smoke. This amendment authorizes only Stage A cook, not the audit itself to open or
merge a product PR.
