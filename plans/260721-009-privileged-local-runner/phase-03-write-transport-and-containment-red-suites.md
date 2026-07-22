---
phase: 3
title: "Write transport and containment RED suites"
status: pending
priority: P1
dependencies: [1, 2]
effort: "1.5 implementation days"
---

# Phase 3: Write Transport and Containment RED Suites

## Overview

Commit the complete security/race/crash/idempotency suite RED before runner behavior. Tests use
the exact released Issue #8 schemas/readers and Phase 1 harmless fixtures. Every RED execution
enters through the real public `make runner-test`, `make runner-security-test`, or
`make runner-race-test` path and reaches its named fixture marker; helper-only or missing-command
failure is not evidence. Required absence/tool/dependency conditions fail explicitly and cannot be
converted to skips.

## Context Links

- [RED assertion families](./verification-evidence-and-rollback.md#red-assertion-families)
- [Threat matrix](./requirements-risk-threat-traceability.md#threat-and-abuse-case-matrix)
- [Private transport](./implementation-boundary-and-design.md#private-transport)
- [Containment/quotas](./implementation-boundary-and-design.md#host-containment-and-process-quotas)

## Requirements

- Cover every user-required negative class before behavior changes.
- Deterministic barriers force race/TOCTOU/crash windows; timing-only sleeps are insufficient.
- Assert zero process/operation/audit allocation for pre-admission request failures.
- Assert base/protected/foreign state unchanged on every attack.
- Retain a machine-readable RED manifest tied to exact Issue #6/#8/input SHAs.
- Use every exact stable ID and pre-behavior oracle in the verification companion; prefixes or
  dynamically assigned IDs are insufficient.
- Retain the exact test-only RED commit before any production runner module/behavior commit. RED
  reruns after implementation are regression evidence, not a substitute for that contemporaneous
  pre-behavior commit.

## Related Code Files

- Create test/gate scaffolding only: `apps/lab-runner/pyproject.toml`, the three exact
  `apps/lab-runner/requirements/runner-py312-macos-arm64.{in,lock,metadata.json}` files,
  `apps/lab-runner/config/runtime-policy-v1.toml`,
  `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`,
  `apps/lab-runner/tools/run-gate.py`, and `mk/issue-5/i5-04.mk`
- Extend/rehash: `apps/lab-runner/config/released-contract-lock.json` created in Phase 2 with
  release pins; add the measured fragment/activation hashes after their Phase 3 bytes exist
- Create: `apps/lab-runner/tests/security/test_{interpreter_import,argv_registry,path_toctou,environment_network,quotas_output_descendants,base_immutability,browser_transport}.py`
- Create: `apps/lab-runner/tests/race/test_{fencing,cross_entrypoint,release_atomicity,crash_recovery,idempotency}.py`
- Create: `apps/lab-runner/tests/unit/test_{transport_policy,runtime_policy,workspace_policy,state_machine,release_policy,evidence_policy}.py`
- Create: `apps/lab-runner/tests/red-manifest.json`
- Reuse read-only: Phase 1 test fixtures and released Issue #8 schema/reader modules; Stage A
  releases no generated binding procedure or generated output list
- Modify/Delete: no existing path; the new Make fragment owns only the three reserved targets

## Tests Before

This phase is the tests-before phase. Each family must:

1. Fail with its stable `RED-*` assertion because runner behavior is absent or deny-by-default.
2. Prove fixture/precondition reached with an independent marker.
3. Cap its own runtime, output, paths, child count and cleanup.
4. Record expected denial/state/pointer/base/process oracle.
5. Refuse skipped/xfail/expectedFailure treatment for required cases.

## Implementation Steps

1. Create the pinned test environment and minimal non-behavior gate dispatcher. Add only the three
   exact recipes to the new I5-04 Make fragment; create its exact activation instance from actual
   fragment bytes and verify `fitness-result-v2` authority. No production runner module exists yet.
2. Add pure policy/type/registry/property tests using Issue #8 bindings; unknown fields and command
   variants must fail before process resolution.
3. Add UDS and explicit loopback-fallback tests for exact Host, absent Origin, auth, CSRF, Fetch
   Metadata, content type/framing/body bounds, launch replay, no CORS and browser-direct denial.
4. Add import/startup/entrypoint/env tests with canary modules/configs and an argv/env spy.
5. Add descriptor/path/TOCTOU/base tests with barriers that swap parent, child, pointer and temp
   entries between check and use.
6. Add CPU/RSS/disk/file/FD/process/output/descendant tests, including TERM-ignore, rapid
   fast-exit parents, double-fork/reparent and new-session descendants, with no host-wide limit or
   kill primitive.
   The suite must fail admission if Phase 1 did not prove a non-poll-only descendant mechanism.
7. Add deterministic OS containment probes for network denial, base write denial, workspace write,
   required import and process cleanup.
8. Add runner/runner, reset/export/verify, Make expert non-overlap and learner-targeted Airflow
   denial barriers. The Airflow case must initially prove current explicit-path acceptance, then
   require `RUNNER_LEARNER_NAMESPACE_RESERVED` before child/import/write.
9. Add kill/fault points before/after SQLite, audit, file fsync, manifest, pointer rename/fsync,
   result commit and response acknowledgment; add replay/conflicting-request cases.
10. Run all three public Make targets, generate the RED manifest, and prove every listed assertion
    fails after its marker for the intended absent/refusing behavior. Commit these test-only bytes
    and evidence before Phase 4 creates any runner source module.

## Refactor

None. Only test/gate scaffolding, tests, fixtures and read-only released schema/reader interfaces
exist. Do not create a generated binding or production helper that makes tests pass in this phase.

## Tests After

- Run the RED suite twice through the exact public Make targets with randomized safe IDs and
  deterministic barriers.
- Verify no fixture/process/socket/temp state remains outside marker-owned test roots.
- Verify protected hashes/Git tree and previous current pointer are unchanged.

## Regression Gate

- Every required family is represented and RED.
- No pass caused by missing tool, missing contract, unsupported host, or fixture/setup failure.
- RED manifest has stable IDs, exact SHAs, expected failure and future owning module.

## Risk and Security

Adversarial helpers are themselves attack surfaces. They live only below the app tests, accept
only test-created descriptors/paths, use hard timeouts, never use sudo/network/cloud/container,
and are excluded from runtime package entrypoints.

## Success Criteria

- [ ] All mandatory negatives exist and are demonstrably RED first.
- [ ] Race/crash tests use deterministic barriers at every commit boundary.
- [ ] Browser/request failures allocate no privileged operation.
- [ ] Base, expert namespace, foreign state, and host processes remain untouched.

## Next Steps

Phase 4 implements only enough fail-closed core behavior to turn the relevant RED suites GREEN.
