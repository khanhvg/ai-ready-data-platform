---
phase: 2
title: "Write Static Admission and Security RED Tests"
status: pending
priority: P1
dependencies: [1]
effort: "L"
---

# Phase 2: Write Static Admission and Security RED Tests

## Overview

Encode real current behavior and every required denial as behavior-specific RED tests before
profile/admission implementation. Static tests must prove denial occurs before the production
Compose runner boundary and without foreign side effects.

## Context Links

- [TDD, fitness, evidence, migration, and recovery](./tdd-fitness-evidence-recovery.md)
- [S3 threat model](./threat-model.md)
- [Resource model](./resource-model.md)
- Phase 1 amended inventory and protected manifest

## Requirements

- Functional: implement every stable RED ID listed in the TDD contract, including
  `LP-BUDGET-OVER-AGGREGATE-022`, where applicable to static behavior.
- Functional: cover invalid/missing/duplicate/unknown/all-three/unauthorized pairs, limit
  omissions, dependency expansion, collisions, logs/PIDs, start/health/exit/stop timeouts,
  guarded pair, evidence shape, engine unavailable and foreign teardown sentinel.
- Non-functional: no unconditional failure, expected-code echo, production-subject replacement,
  container start, image pull, cloud action or synthetic performance acceptance.

## Architecture

Use table-driven mutation fixtures around one valid exact amended profile contract and Compose
render. Each fixture changes one semantic property. Invoke the production parser/resolver/security
checker boundary, and use a recording runner boundary only to assert Compose was not invoked.
Filesystem cases use private temp roots with real files/symlinks/FIFOs where safe. Live foreign
sentinel acceptance remains Stage B/Phase 5; static label/ownership parsing gets RED coverage here.

## Related Code Files

- Create: `tests/profiles/**`
- Create: `tests/compose/**`
- Read: `docker-compose.yml`, amended released contracts and exact allowlist
- Product/config implementation: none until the intended RED set is captured

## Tests Before

- Keep Phase 1 characterization GREEN.
- Write valid-fixture construction from actual config; fixture does not carry the expected result
  as executable output.
- Capture exact RED test IDs, node names, assertions and observed failures at the clean amended
  input.

## Refactor

None before RED capture. Test-only seams may expose a production command-runner boundary, but do
not implement admission behavior in fixtures/helpers.

## Tests After

Not in this phase. Phase 3 turns the same RED assertions GREEN without weakening them.

## Test Scenario Matrix

| Priority | Set | Scenarios |
|---|---|---|
| Critical | Request/combination | invalid, missing, duplicate, unknown, every pair, all-three, `LP-BUDGET-OVER-AGGREGATE-022` |
| Critical | Closure/security | hidden dependency, public port, external/foreign volume, socket, privilege, cap, network, RW base |
| Critical | Resource | missing/zero/overflow/unit mutation for memory/CPU/PID/disk/log/deadline/owner |
| Critical | Supply/evidence | tag-only/wrong platform/missing SBOM-signature; schema/tamper/replay/path attacks |
| High | Lifecycle | exact guarded pair, engine unavailable, timeout/restart, interrupted teardown, foreign sentinel |
| Medium | Portability | arm64/amd64 mismatch, engine allocation/accounting unavailable, path/case/Unicode normalization |

## Regression Gate

Characterization tests stay GREEN. New behavior tests must fail for the intended behavior mismatch,
not syntax/import/setup errors. Retain RED output under the released evidence authority only when
that authority exists.

## Implementation Steps

1. Build a canonical valid input from the exact Phase 1 service/config/authority inventory.
2. Write request grammar and combination cases, including all-three independent of numeric budget.
3. Write transitive dependency expansion and undeclared service/profile/port/volume/network cases.
4. Mutate each per-service/aggregate resource and start/stop deadline independently; cross every
   single/pair aggregate and host/engine reserve through the over-budget boundary.
5. Write loopback, collision, mount/socket/privilege/capability/network/interpolation/path cases.
6. Write image digest/platform/SBOM/signature/provenance authority cases without pulling images.
7. Write evidence locator/hash/completion/tamper/replay/N-1-reader contract cases against released
   authority; stop if authority is still missing.
8. Write engine-unavailable behavior that asserts no measurement files and a typed block/non-zero.
9. Write teardown ownership cases with recorded engine-object metadata; reserve actual foreign
   project integration for Phase 5.
10. Capture intentional RED results and prove Compose runner call count is zero for every preflight
    denial.

## Success Criteria

- [ ] Every required behavior has a stable unique RED ID and direct production-boundary assertion.
- [ ] All denial cases prove supported Compose startup was not invoked.
- [ ] No unconditional failure, expected-code echo or synthetic measurement exists.
- [ ] RED failures are behavior mismatches; characterization remains GREEN.
- [ ] Security mutations cover every TM-01..TM-20 boundary applicable before engine startup.
- [ ] Evidence/command tests use the exact released authority or phase remains blocked.

## Risk Assessment

Over-mocking would prove only the fixture. Keep parser/resolver/config/ownership code real and
replace only the external process boundary. Avoid brittle text assertions; assert typed semantic
result, closure and side-effect absence.

## Security Considerations

Never embed real credentials or home paths. Use canary secret strings only in private temp tests
and assert redaction. Clean special-file fixtures with the test framework's exact temp root; never
follow or broadly delete them.

## Next Steps

Proceed to Phase 3 only with reviewed RED evidence and zero protected drift.
