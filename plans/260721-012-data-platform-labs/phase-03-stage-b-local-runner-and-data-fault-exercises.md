---
phase: 3
title: "Stage B Local Runner and Data Fault Exercises"
status: pending
priority: P1
dependencies: [1, 2]
externalDependencies: [issue-9-released-runner, serialized-data-contract-and-pipeline-lease]
effort: "unresolved until exact Stage B amendment"
---

# Phase 3: Stage B Local Runner and Data Fault Exercises

## Context links

- [Plan](./plan.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Protected baseline](./protected-baseline-manifest.md)

## Overview

Sau exact released Issue #9 runner và exact serialized lease, nối lab candidates vào local runner
và xây các exercises thật cho orchestration, atomic 11-asset release, Iceberg và OpenMetadata.
Stage B không sửa portal/renderer và không claim browser/complete learner experience.

## Requirements

### Functional

- Airflow 3 local TaskFlow/operator-callable path demonstrates retry, idempotency, timeout và
  backpressure with real run-scoped effects; preserve `airflow.sdk` semantics, do not resurrect
  `PythonOperator`, and allow no privileged browser action.
- Publisher makes exactly eleven assets visible all-or-none via validated manifest hash and one
  atomic current pointer; crash recovery covers every boundary.
- Iceberg uses empirically verified local object-store/catalog commit, snapshot, conflict and
  orphan semantics; no mock-only acceptance.
- OpenMetadata reconcile uses exact namespace/FQN/managed sets, explicit idempotent create/update/
  delete policy, prefix-collision safety and rollback.
- Every service/pattern is bound to named failure and retained evidence.

### Non-functional

- Private run root only; repository/golden paths read-only.
- Serial 16GB execution. Core has no Docker/cloud requirement; real optional-service labs run one
  profile at a time and absence is honest.
- Additive seam, old reader/adapter retained, atomic rollback and run-owned cleanup only.

## Architecture

Use released #9 operation/workspace/idempotency/evidence boundaries verbatim. Exact runner command
IDs, pipeline paths and service operations remain unresolved until amendment. `mk/issue-5/i5-07.mk`
may register only released commands through the existing include seam; root `Makefile` stays
untouched.

Data flow follows [data architecture](./data-architecture-and-recovery.md): private workspace →
immutable 11-asset staging → manifest/hash → atomic pointer → real local Iceberg/OpenMetadata →
evidence index.

## Exercise matrix

| Level | Exercise | Controlled failure | Stable IDs | Recovery/evidence |
|---|---|---|---|---|
| Junior | Airflow retry/idempotency | Failure after effect before acknowledgement; duplicate key | `DL-ORCH-001` | One effect, same outcome, state journal |
| Junior/Mid | Timeout/backpressure | Slow child + concurrent reset/publish/queue pressure | `DL-ORCH-002/003/004` | Child stopped, conflict/rejection, bounded resource trace |
| Mid | Atomic curated release | Crash after asset N/manifest/pointer boundary | `DL-REL-001/002/003` | Old or full new only; prior pointer/replay/quarantine |
| Mid | Iceberg lifecycle | Stale snapshot writer and orphaned run object | `DL-ICE-001/002/003` | Winner snapshot, loser conflict, run-only orphan cleanup |
| Mid | OpenMetadata reconcile | Stale managed entity + prefix neighbor + mid-run crash | `DL-OM-001/002/003/004` | Exact set, neighbor/unmanaged survive, replay/rollback |

## Related code files

- Create/modify after amendment: exact verifier/runner binding paths from #8/#9 releases.
- Create: dependency-derived lab paths under `learning/labs/data-platform/**`.
- Create: `mk/issue-5/i5-07.mk` recipes only after command ownership resolves.
- Modify after lease: only exact data-contract/publisher/Airflow/OpenMetadata paths named in the
  serialized lease.
- Preserve: root `Makefile`, golden contracts/models/views/fixtures/readers, portal and runner
  outside exact released extension points.
- Exact current Stage B implementation path/command list: empty.

## Implementation steps

1. Amend exact #9 release SHA, registry/workspace/evidence paths/commands and blast radius; attach
   exact serialized shared-contract/data/pipeline lease; independent revalidation + readiness.
2. Characterize real runner/Airflow/service behavior before change and record version/topology.
3. Add `DL-ORCH-*` behavior-specific REDs using real run-scoped operations and failure boundaries;
   then implement minimum released extension-point bindings.
4. Add `DL-REL-*` real crash/polling tests against private releases; implement the smallest
   admitted staged manifest/hash/pointer seam while retaining old reader/adapter.
5. Verify real local Iceberg semantics, then add commit/conflict/orphan RED/GREEN. If capability is
   absent, block the seam or serialize; do not claim a primitive that was not observed.
6. Add exact OpenMetadata collision/reconcile/rollback RED/GREEN in a run-owned namespace; foreign
   sentinels must survive.
7. Bind verifier/evidence/reset without portal. Add Make fragment only for released command IDs.
8. Run stage suite, final four-command contract subset available at this stage, exact #6/#8/#9
   blast radius, protected hashes, cleanup and rollback rehearsal.

## Tests before

- All `DL-CHAR-*` remain GREEN.
- Each RED injects one real boundary fault and asserts an end-to-end invariant; no expected-code
  echo, unconditional failure or fake service/fixture.
- Fault injectors are private-run-only and prove base/foreign state unchanged.

## Refactor

Extract shared fault-boundary/ownership/evidence helpers only after at least two exercises need the
same semantics and released contracts permit the abstraction. No new service or pattern for
teaching aesthetics.

## Tests after

- Stable `DL-ORCH-*`, `DL-REL-*`, `DL-ICE-*`, `DL-OM-*`, `DL-SEC-*`, `DL-EVD-*` suites.
- Repeated idempotency, crash, poller consistency, conflict and rollback runs.
- Core Docker-free lane plus real optional-service lane; unavailable states remain non-pass.
- Exact dependency blast radius and protected hash/tree checks.

## Success criteria

- [ ] Local runner exercises work without browser privilege or repository mutation.
- [ ] Readers never see mixed 11-asset releases; every crash boundary recovers honestly.
- [ ] Iceberg conflict/orphan behavior is verified against actual local semantics.
- [ ] OpenMetadata exact reconciliation preserves collision/unmanaged/foreign entities.
- [ ] Stage B evidence is retained but does not claim portal or complete learner experience.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Lease too broad or concurrent writer | Shared semantic corruption | Exact path lease, serialized owner, expiry and STOP |
| Current drop/create loop exposed as “atomic” | Mixed release/false success | Real poller/crash RED before seam; one pointer oracle |
| Catalog behavior assumed | Lost update/orphans | Empirical versioned two-writer and orphan tests |
| Prefix/broad delete | Foreign metadata loss | Canonical equality and ownership-set checks |
| Optional service absent | Fake pass | `not-run-optional`; service lab remains unpublished/unverified |

## Security considerations

Run full S3 negative suite for path/ref/link/FIFO/socket/device/other special file, SQL/template
injection, credential/PII/private paths, object/catalog scope, evidence tamper/replay and
resource/process limits. Cleanup refusal is safer than deleting unknown state.

## Next steps

Stage C remains blocked until Issue #10 real journey/renderer is passing, merged and amended by
exact SHA.
