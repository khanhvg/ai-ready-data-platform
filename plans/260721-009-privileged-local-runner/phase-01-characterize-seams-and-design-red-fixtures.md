---
phase: 1
title: "Characterize seams and design RED fixtures"
status: pending
priority: P1
dependencies: []
effort: "1 implementation day"
---

# Phase 1: Characterize Seams and Design RED Fixtures

## Overview

Dependency-independent pre-implementation work. Freeze current expert behavior and design harmless
malicious fixtures before any runner behavior exists. This phase is fully plan-able now, but the
issue pipeline must not authorize even this phase for cook until the exact Issue #8 Stage A release,
independent validation, and readiness gates clear.

## Context Links

- [Plan](./plan.md)
- [Implementation boundary](./implementation-boundary-and-design.md#existing-seam-characterization)
- [RED families](./verification-evidence-and-rollback.md#red-assertion-families)
- Master `PH-C05`, `PH-C06`, `PH-H13`, `SC-02`, `SC-03`, `SC-14` in
  [traceability](../260721-005-enterprise-learning-sandbox/requirements-traceability.md)

## Requirements

- Record exact input/host/tool/file identities without writing runtime/product state.
- Prove existing generator/load/dbt/export/Airflow expert semantics and path capabilities.
- Design deterministic, harmless malicious fixtures for every required RED family.
- Prove expert and future learner namespaces can be disjoint without changing existing defaults.
- Identify any truly missing seam; do not edit it in this phase.

## Architecture and Characterization Matrix

| Seam | Characterization | Required oracle |
|---|---|---|
| generator | exact argv/path, `small`/42 semantics, `--out` only | output remains caller root; base data untouched in fixture tests |
| loader | explicit raw/DB paths and writer closure | 18 tables; no open writer after exit |
| dbt | read-only project + generated profile/target/log/home | 51 models and expected warning contract; no base target/log |
| exporter | explicit DB/export paths and curated list | exact ordered 11 files; repository export untouched |
| Airflow callable | explicit alternate path behavior/import safety; current learner-path acceptance is captured as RED input | task order/defaults unchanged; future reserved-path guard denies before spawn |
| direct Make | default expert namespace only | no learner workspace/current-pointer path |

## Related Code Files

- Create: `apps/lab-runner/tests/characterization/test_current_entrypoints.py`
- Create: `apps/lab-runner/tests/characterization/test_expert_namespace.py`
- Create: `apps/lab-runner/tests/fixtures/{argv_probe,import_probe,startup_probe,process_tree_probe,path_race_probe,network_probe,resource_probe,output_probe}.py`
- Create: `apps/lab-runner/tests/fixtures/browser-requests.json`
- Create: `apps/lab-runner/tests/fixtures/fault-points.json`
- Create: `apps/lab-runner/tests/fixtures/fixture-manifest.json`
- Read only: current seams listed in the implementation-boundary companion
- Modify/Delete: none

## Tests Before

1. Add characterization assertions against the exact input behavior, not future runner behavior.
2. Give every malicious fixture a stable ID, expected side effect, maximum runtime/output, and
   cleanup oracle. Fixtures may touch only their temporary marker-owned root.
3. Prove fixture self-tests fail if a fixture silently skips, cannot create its intended harmless
   condition, or leaves a process/file behind.
4. Record pre/post Git tree, protected file hashes, running child list, and expert namespace state.

## Implementation Steps

1. Capture exact Git/input/Issue #6 identities, Darwin build/memory/Python/sandbox executable, and
   SHA-256/Git blobs for every current entrypoint/config/schema used later.
2. Characterize each existing seam with private temporary paths; do not run broad clean, Docker,
   Airflow service, network/cloud, or production-size data.
3. Model generated workspace profile paths for dbt and prove the base project can remain read-only.
4. Build only test fixtures and manifests. Fixture helpers never accept arbitrary host paths and
   terminate within their own hard timeout.
5. Exercise namespace maps with no mutation: existing Make/Airflow defaults are `expert`; future
   runner paths are `learner`; record the current explicit Airflow path gap for Phase 3 RED.
6. Produce `characterization.json` and `red-fixture-design.json` as future evidence artifacts
   under the issue evidence root when the phase is eventually cooked.
7. If an existing seam cannot be isolated, STOP with exact failing assertion/path and update the
   plan through independent validation/readiness before any seam modification.

## Refactor

None. This phase cannot change product behavior or existing seams.

## Tests After

- Repeat fixture self-tests and characterization twice from clean temporary state.
- Verify stable current outputs and no tracked/unrelated change.
- Verify every Phase 3 assertion maps to one bounded fixture or a pure in-process test.

## Regression Gate

- Characterization and fixture-design suites pass against the immutable input.
- `git diff --check` and changed-path allow-list pass.
- No implementation module, shared contract, runtime config, Make fragment, or existing seam is
  changed by this phase; the exact Airflow gap remains RED input.

## Risk and Security

Characterization executes repository-controlled current entrypoints only with bounded `small`/42
temporary paths. A fixture that can reach a caller-selected host path, network, credential, or
unbounded descendant is itself a security defect and blocks the phase.

## Success Criteria

- [ ] Current seams have exact, evidence-backed preservation oracles.
- [ ] All required RED fixture families exist with stable IDs and self-tests.
- [ ] Expert/learner namespace non-overlap is proven without changing defaults.
- [ ] No implementation or shared-contract assumption was introduced.

## Next Steps

Proceed only to Phase 2 after the exact released Issue #8 Stage A SHA exists and is freshly
verified. Planning/validation may complete while it is absent; cook may not start.
