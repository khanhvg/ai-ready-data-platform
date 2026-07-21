---
phase: 4
title: "Run Stage B Cold Warm Resource Evidence"
status: pending
priority: P1
dependencies: [3]
effort: "L"
---

# Phase 4: Run Stage B Cold Warm Resource Evidence

## Overview

At the exact Stage A head, implement the bounded sampler/lifecycle and run the practical actual
matrix: one cold plus two warm sequential repetitions for each admitted current single group and
the exact guarded pair. Raw measurements corroborate static admission; they never replace it.

## Context Links

- [Resource and measurement model](./resource-model.md)
- [S3 threat model](./threat-model.md)
- [Evidence/recovery contract](./tdd-fitness-evidence-recovery.md)
- Exact Stage A head and dependency amendment

## Requirements

- Functional: require exact admitted engine allocation, host architecture, images, toolchain,
  Stage A/config/dependency/lab/command/completion authorities before live work.
- Functional: sample peak working set/RSS, CPU, wall time, disk growth, readiness, restart/OOM and
  teardown residue for one cold + two warm reps after readiness gates.
- Functional: use only real released group workloads; no noop/sleep/generated fallback.
- Non-functional: repetitions sequential, input/config/image/allocation stable, raw samples retained,
  image pull/build time separate and acceptance uses no-pull exact images.
- Non-functional: sampling count/bytes, command streams, derived documents and the total retained
  bundle stay within the deterministic caps in the resource model.
- Non-functional: engine unavailable/mismatch is typed blocked; Docker-free core stays independent.

## Architecture

`admit.py` freezes a run manifest and invokes the engine by argv. `measure.py` samples host,
engine VM/process and per-container/cgroup layers separately from pre-start through teardown.
`teardown.py` uses only immutable run ownership. Raw JSONL is append-only/private; summary is
derived after each repetition and hash-linked. The released completion authority commits the
bundle only after teardown/residue.

## Related Code Files

- Create: `scripts/profiles/measure.py`
- Create: `scripts/profiles/teardown.py`
- Modify: `scripts/profiles/admit.py` only for the tested live runner interface
- Continue: `tests/profiles/**`, `tests/compose/**`, `mk/issue-5/i5-08.mk`
- Runtime only: `.artifacts/evidence/local-profiles/<run-id>/` (ignored/private)
- Product/docs/shared contracts: no modification in this phase

## Tests Before

- All Stage A static RED IDs GREEN.
- Measurement schema/integrity/engine-unavailable/timeout/restart/disk/residue cases RED against the
  production sampler/teardown boundaries.
- Prove no samples are emitted for missing engine/image/workload/authority.

## Refactor

Keep collectors and teardown small and platform-adapted behind explicit interfaces. Do not fold
measurement into admission decision math or sum container memory with engine VM RSS. Reuse the
released evidence/ownership primitives rather than copying them.

## Tests After

- Unit: parsing/normalization/peak/delta/readiness/restart/residue/timeout and malformed sample.
- Integration: actual group lifecycle, limit observation and retained-state warm classification.
- Negative live: failed health, timeout, restart/OOM where safely inducible by bounded fixture,
  disk cap and interrupted teardown; never mutate real dependency data.
- Matrix: exactly three repetitions for each actual admitted scenario; no all-three start.

## Regression Gate

Run static gates first. Then run exact Stage B commands/workloads from the dependency amendment.
Final `make profile-budget-check` remains blocked until every required scenario has three complete
same-head repetitions and teardown evidence.

## Implementation Steps

1. Verify clean HEAD exactly equals recorded Stage A head and all dependency/config/image/tool
   hashes match. Refuse dirty/stale state.
2. Resolve host/engine normalization including engine memory/CPU allocation and platform image
   digests. Block on missing/unreliable accounting.
3. Verify SBOM/signature/provenance policy for every exact image, pre-pull/build only under the
   admitted preparation step, then require no-pull acceptance invocations.
4. Implement bounded process/container/host/volume/log/readiness sampling, exact byte/sample caps
   and private raw writes.
5. Implement run ownership and idempotent teardown used after every repetition/failure.
6. For `orchestration`, run cold, warm-1 and warm-2 sequentially with its exact released workload.
7. Repeat for `lake` and `governance` only if their exact workloads/authorities exist.
8. Run exact `lake+governance` guarded ingest: prove orchestration absent before start and after
   closure expansion; run one cold + two warm repetitions.
9. For each repetition, wait for every required health/one-shot gate, run workload, sample through
   teardown, verify zero restart/OOM/residue and preserve declared warm state only.
10. Derive summaries from raw, retain all values/distributions, link hashes and compare to static
    ceilings without averaging away a violation.
11. Re-run Docker-free core independently after live matrix.

## Success Criteria

- [ ] Every required current scenario has one cold + two warm complete actual repetitions.
- [ ] All repetitions use identical exact head/config/images/allocation/workload and pass readiness.
- [ ] Raw+summary capture every required metric with correct attribution and hashes.
- [ ] No hard resource/deadline/disk/log/PID/port/ownership bound, restart/OOM or residue fails.
- [ ] Guarded pair contains exact `lake+governance`; orchestration is absent; all-three never starts.
- [ ] Engine/image/tool/workload absence yields typed blocked evidence and no synthetic sample.
- [ ] Docker-free core remains green regardless of heavy-profile outcome.

## Risk Assessment

Host noise and Docker Desktop accounting can mislead. Use hard config as primary, sequential reps,
normalized inputs and separate accounting layers. Any engine update, image digest change or host
allocation change invalidates comparability and requires a fresh set, not selective reruns.

## Security Considerations

Acceptance uses exact local images with pulls disabled. Sampler reads only required metrics and
never dumps env, secrets, private paths or container files. All subprocesses/timeouts/outputs are
bounded. Failure always attempts ownership-scoped teardown.

## Next Steps

Phase 5 proves actual foreign sentinel recovery, evidence compatibility, blast radius, bounded docs
and rollback. A Stage B block is carried honestly; it is not converted into a release pass.
