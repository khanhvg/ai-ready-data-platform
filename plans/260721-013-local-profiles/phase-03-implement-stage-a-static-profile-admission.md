---
phase: 3
title: "Implement Stage A Static Profile Admission"
status: pending
priority: P1
dependencies: [2]
effort: "L"
---

# Phase 3: Implement Stage A Static Profile Admission

## Overview

Implement the declarative profile contract, static admission/security/budget gates and supported
pre-start lifecycle integration. Turn Phase 2 static RED tests GREEN without starting, building or
pulling containers. Freeze the exact Stage A head for Stage B.

## Context Links

- [Resource model](./resource-model.md)
- [S3 threat model](./threat-model.md)
- [TDD and fitness contract](./tdd-fitness-evidence-recovery.md)
- Phase 1 exact dependency amendment and Phase 2 RED evidence

## Requirements

- Functional: one canonical config maps actual groups/services/closure, allowed combinations,
  resource/deadline/security/image/port/volume/project rules and evidence authority hashes.
- Functional: deny every invalid request and all-three before the supported Compose runner call;
  admit only actual single groups and exact `lake+governance` guarded pair.
- Functional: integrate preflight with every documented/supported heavy Make start path through
  `mk/issue-5/i5-08.mk` while leaving root `Makefile` unchanged.
- Non-functional: Docker-free core and protected semantics/contracts remain unchanged.
- Non-functional: no live engine acceptance, container operation or fabricated evidence.

## Architecture

```text
CLI/Make request
  -> strict request parser
  -> load exact config + authority hashes
  -> static Compose render and recursive closure
  -> combination + per-service + aggregate + S3 checks
  -> live ownership/resource preflight interface
  -> immutable admitted run manifest
  -> argv-array Compose runner (not invoked in Stage A tests)
```

`config/profiles/local-profiles.yaml` is the single I5-08 policy source. Compose remains the
service topology source. Admission rejects disagreement rather than allowing one to override the
other. Scripts accept explicit arguments, clear ambient Compose/env controls and never shell-join
user data.

Supported Make integration must bind the exact admitted manifest to the actual Compose invocation.
The fragment may add target-specific variables/prerequisites or new thin targets because root Make
already includes fragments. If GNU Make composition cannot guarantee that binding for current
`up`, `airflow`, `lake-up`, `catalog`, `catalog-ingest`, and teardown paths without recipe override,
Stage A stops and requests the exact root-Make serialized lease. Do not emit duplicate-recipe
warnings, silently leave a bypass, or edit root Make under current authority.

## Related Code Files

- Create: `config/profiles/local-profiles.yaml`
- Create: `scripts/profiles/admit.py`
- Create: `mk/issue-5/i5-08.mk`
- Modify: `docker-compose.yml`
- Continue: `tests/profiles/**`, `tests/compose/**`
- Conditionally modify after tests prove need: `.env.example`
- Protected/read-only: root `Makefile`, shared registries/contracts, portal/runner/labs, golden code

## Tests Before

- Phase 1 characterization GREEN.
- Phase 2 intended static behavior RED with exact assertion IDs/evidence.
- Capture Compose render and root Make target graph before modification.

## Refactor

- Add explicit loopback binds, labels, limits, log caps, deadlines/security options and project-
  scoped ownership while preserving actual service images/commands/dependencies and semantics.
- Replace the current Airflow RW repo-root exposure with exact dependency-amended RO code and
  bounded writable workspace mounts. If released workflow cannot tolerate this, block for threat
  disposition; do not preserve broad RW by default.
- Parameterize collision-prone names only if legacy documented behavior and owner-scoped teardown
  remain proven. Collision denial is preferable to unsafe adoption.
- Attach pre-start admission to supported Make lifecycle without root file modification.

## Tests After

- Turn every Stage A-applicable RED ID GREEN.
- Render each single group, exact guarded pair, every denied pair and all-three.
- Mutation-test each required service field, dependency, port, volume, network and image authority.
- Prove Compose runner call count zero on denial and exactly one canonical argv call on admission
  through a recording boundary.
- Prove Docker-free command closure/protected hashes unchanged.

## Regression Gate

Focused static tests, then future Stage A static portions of:

```bash
make compose-check compose-security-check profile-budget-check recovery-test
```

`profile-budget-check`/`recovery-test` output must be explicitly Stage A/static-incomplete until
Stage B. It cannot be reported as final default pass.

## Implementation Steps

1. Define strict schema/types and canonical ordering for groups, services, combinations, resources,
   deadlines, ownership, image policy and authority hashes.
2. Implement safe YAML/config loading with a pinned released dependency; reject duplicate keys,
   aliases/merge surprises, unknown fields, unsafe tags and non-canonical units.
3. Implement strict request grammar and recursive Compose dependency closure from the exact static
   render; compare both directions against the config.
4. Implement single/pair/all-three, engine-allocation and host-reserve budget math with
   overflow-safe byte/CPU units.
5. Implement S3 checks for interpolation/env, ports, volumes, mounts, socket, privilege, caps,
   networks, paths, images, log/PID/disk/deadlines and owner labels.
6. Add current per-service limits and loopback/private/RO hardening to Compose; preserve commands,
   health semantics and current group service membership.
7. Bind documented Make start paths to preflight and exact admitted manifest. Stop for a root-Make
   lease if fragment-only composition cannot enforce the boundary.
8. Emit only released-schema-valid static result/evidence. If completion authority is missing or
   incompatible, keep output local/test-only and Stage A blocked.
9. Run GREEN matrix and protected/hash/placeholder scans without contacting the engine.
10. Commit/push the exact Stage A head and record it; no live measurement may run against a dirty
    or later tree.

## Success Criteria

- [ ] Every supported start path runs exact static admission before its Compose invocation.
- [ ] Actual service closure and config allowlist are equal; hidden dependencies cannot start.
- [ ] All current services have required memory/CPU/PID/disk/log/start/stop/ownership/security fields.
- [ ] Single/pair host budgets pass; all-three and all unauthorized pairs deny deterministically.
- [ ] Ports are loopback/owned; no portal/web Docker socket, privilege or broad RW base mount exists.
- [ ] Phase 2 static RED tests are GREEN without weakening assertions.
- [ ] Docker-free core, protected hashes and golden semantics remain green/unchanged.
- [ ] Exact clean Stage A head and released authorities are recorded for Stage B.

## Risk Assessment

Make/Compose are not authorization systems, and direct Docker CLI users remain privileged. The
supported path must still be impossible to bypass accidentally. Root-Make ownership conflict is a
hard blocker, not a reason to duplicate or override recipes silently. Image hardening may expose
incompatibility; fail with exact service/remediation.

## Security Considerations

No ambient `.env` or user environment may alter topology/security-sensitive fields. Store private
manifests outside tracked paths with safe modes. No socket, cloud credential, real secret, private
path or raw env enters output.

## Next Steps

Phase 4 only at the exact clean Stage A head with admitted engine/images/tools. Otherwise static
Stage A remains useful but Issue #13 heavy acceptance is blocked.
