---
phase: 3
title: "Stage B Local Runner and Data Fault Exercises"
status: pending
priority: P1
dependencies: [1, 2]
externalDependencies: [issue-9-reset-rerun-repair-release]
effort: "12 paths after exact I5-04 repair handoff"
---

# Phase 3: Stage B Local Runner and Data Fault Exercises

## Context links

- [Plan](./plan.md)
- [Dependency and authority register](./dependency-and-authority-register.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Protected baseline](./protected-baseline-manifest.md)

## Overview

Issue #9's runner is released, but Stage B remains blocked by the fresh reset-rerun defect recorded
in the register. After I5-04 publishes the bounded repair, implement only three Vietnamese-first
runner-backed labs: deterministic ingest, model/quality and weighted metrics. Do not modify runner,
golden data, pipeline/dbt/Airflow/OpenMetadata, portal, curriculum, shared contracts or root Make.

## Requirements

### Functional

- Each lab is runnable as: prerequisite → starter → controlled failure → exact fixed runner
  operation(s) → verify → immutable evidence reference → `workspace.reset` → full rerun/
  idempotency → reflection.
- Deterministic ingest uses `workspace.prepare`, `retail.generate`, `retail.load`; proves
  `small`/42, 18 tables, 6,812 rows and manifest/projection identity without editing generator data.
- Model/quality uses `retail.dbt-build` after ingest; reads the private DuckDB/dbt artifacts to
  prove 51 models and the released warn/pass/fail semantics without editing SQL/YAML.
- Weighted metrics uses `retail.export`, `promotion.configure`, `promotion.verify`; the I5-07
  verifier reads the private Rill-compatible `mart_fulfillment_performance` Parquet with DuckDB and
  proves weighted `5.456625` versus invalid average-of-averages `5.34`, weight 800.
- The verifier maps contextual starter failures to existing lab codes while retaining the raw
  runner failure code. It never changes or broadens the runner's closed operation registry.
- Learning evidence references the runner `runId`, workspace revision and verified
  `runner-evidence-index-v1` SHA; it does not copy or rewrite runner evidence.

### Non-functional

- One serial writer, exact 12-path Issue #12 lease, exact base `8ffbd420...`.
- OrbStack engine and exact released/repaired image are mandatory; missing capability is failure.
- `RUNNER_TIMEOUT`, `RUNNER_RESOURCE_LIMIT`, output/resource bounds, evidence tamper, reset,
  rerun/idempotency, no staged-temp/container residue and golden immutability are functional tests.
- The only new public command is already-reserved `data-labs-e2e`; direct fragment and root Make
  composition must match.

## Architecture

`verify_stage_b.py` is an I5-07 orchestration/verifier boundary, not a runner implementation. It
invokes only the released owner CLI and exact zero-argument operation IDs, validates the released
workspace/evidence contracts, and writes learning evidence only under an ignored I5-07 run root;
the runner continues to own `apps/lab-runner/.local-state`. Focused timeout/resource tests reuse
the released runner's fixed test fixtures and containment helpers, never a new learner operation
or copied executor. The local `stage-b-operation-bindings.json` maps the three labs to exact
operation sequences; it is not a shared registry or API.

Runtime flow:

```text
Vietnamese starter/private I5-07 run
  -> fixed Issue #9 operation
  -> private runner workspace generation
  -> DuckDB/dbt/Parquet observation
  -> immutable runner evidence index
  -> learning-evidence reference
  -> workspace.reset
  -> same full semantic cycle again
```

Airflow, Iceberg and OpenMetadata remain optional/blocked: the released eight-operation manifest
has no operation for them. Stage B must state this truthfully and may not create a shared seam.

## Exercise matrix

| Lab | Controlled failure | Fixed released operations | Verify/evidence |
|---|---|---|---|
| Deterministic ingest | Private starter checksum/count mismatch; prerequisite `retail.load` failure retains raw `RUNNER_OPERATION_FAILED` | `workspace.prepare`, `retail.generate`, `retail.load` | `GOLDEN_INPUT_MISMATCH`, 18/6,812, manifest/projection hashes, runner evidence index |
| Model/quality | Starter misclassifies warn as error; prerequisite `retail.dbt-build` failure retains raw code | ingest sequence + `retail.dbt-build` | `QUALITY_WARNING_MISMATCH`, 51 models, released dbt outcome/grain evidence |
| Weighted metrics | Starter uses equal-weight average | ingest/model + `retail.export`, `promotion.configure`, `promotion.verify` | `AVERAGE_OF_AVERAGES_INVALID`, 25 rows, weight 800, 5.456625 vs 5.34, 11 assets |

`workspace.reset` closes every exercise; the acceptance reruns the entire eight-operation cycle,
not only a static verifier.

## Related code files

Exact 12-path write set and lease are authoritative in the
[register](./dependency-and-authority-register.md#exact-stage-b-write-set-12-paths).
No other file may be staged.

## Implementation steps

1. STOP until the I5-04 repair release passes the two-cycle acceptance, is verified as a descendant
   of current base `8ffbd420...`, and becomes the amended cook base with exact rebuilt image digest.
2. Add behavior-first REDs for all three starter failures, raw/context failure pairing, evidence
   tamper, timeout/resource, reset, second-cycle export/recovery and golden drift.
3. Extend only the six Stage A descriptors/content files with exact runnable operation sequences
   and Vietnamese lifecycle; retain Stage A semantic constants and remediation codes.
4. Add the local operation binding, controlled-failure fixture, Stage B verifier/tests and
   activation; implement the minimum `data-labs-e2e` recipe in the existing fragment.
5. Run the 16 verification entries serially on OrbStack, including direct/root Make and pristine
   detached checkout; missing repaired image/evidence is a hard failure.
6. Focused exact-head code review must report Critical=0 and Important=0. Then PR/CI, authorized
   merge and post-merge smoke may proceed; no separate security/red-team/human ceremony.

## Tests before

- Stage A focused unit/verifier/Make commands remain GREEN.
- Each Stage B RED fails for observed behavior, not expected-code echo or unconditional failure.
- The blocker regression must reproduce on `671201f...`/`8ffbd420...`: first cycle passes; second
  `retail.export` returns `RUNNER_RELEASE_POINTER_INVALID`; next CLI recovery crashes.

## Tests after

- All eight operations pass twice with fresh keys and identical released stable projections.
- Contextual failures retain raw runner codes and produce schema-valid learning evidence only after
  expected/actual verification.
- Timeout/resource fixed probes report their exact codes and cgroup-v2 bounds.
- Every runner evidence index binds exact result bytes; mutation is rejected.
- Reset preserves progress/evidence, removes exercise state, and full rerun succeeds.
- No staged evidence temp, runner container or unowned run state remains; protected hashes match.
- Direct/root `data-labs-e2e` and detached clean-checkout smoke pass.

## Success criteria

- [ ] Exact I5-04 repair release is reviewed, merged, pinned and passes two-cycle recovery.
- [ ] Three Vietnamese labs complete the full lifecycle with real DuckDB/dbt/Parquet semantics.
- [ ] All eight operations, three failure classifications, timeout/resource and evidence binding
      pass on OrbStack.
- [ ] Reset plus full rerun/idempotency passes with no committed-but-client-failed export.
- [ ] Golden, runner, pipeline, portal and curriculum trees remain unchanged by I5-07 cook.
- [ ] Focused review reports Critical=0 and Important=0; 16 commands pass on exact head.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Repeated semantic release collides on volatile data-run identity | Committed failure and unusable recovery | Block until I5-04 two-cycle repair release |
| Context wrapper hides generic runner failure | False diagnosis | Persist raw runner code plus lab-context code |
| Verifier duplicates runner logic | Contract drift | Invoke/validate released runner boundaries; no copied executor/reset/evidence code |
| Optional service overclaim | Fake lab | Airflow/Iceberg/OpenMetadata explicitly optional/blocked |
| Lease overlap | Portal/curriculum/shared drift | Exact 12 paths, one writer, fixed expiry and staged allowlist |

## Rollback

Before merge, revert only the 12 Stage B paths. Runtime rollback calls only released
`workspace.reset`, preserves immutable evidence, verifies no runner container/staged temp, and
never deletes runner/golden/shared state by glob. If reset or recovery returns
`RUNNER_RELEASE_POINTER_INVALID`, stop and hand back to I5-04; do not clean around it.

## Next steps

Current next step is I5-04 runner repair, then refresh only the repair SHA/image fields and rerun
this bounded Standard-lane readiness check. Stage C remains blocked on merged Issue #10 Stage B.
