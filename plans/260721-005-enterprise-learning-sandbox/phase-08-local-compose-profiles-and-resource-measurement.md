---
phase: 8
title: "Local Compose Profiles and Resource Measurement"
status: pending
priority: P1
dependencies: [5, 7]
effort: "M"
---

# Phase 8: Local Compose Profiles and Resource Measurement

## Overview

Package portal/runner and existing optional services into explicit local profiles, enforce
mutual-exclusion/security rules before startup, and measure cold/warm resource/readiness evidence
on a 16 GiB laptop.

## Context Links

- Existing `docker-compose.yml`, `Makefile`, README resource model
- PH-H01/H08/H13 and SC-04/06
- Phase 5 portal/runner and Phase 7 admitted labs

## Requirements

- Preserve container-free `core`; add a `learning` profile for portal+runner packaging without
  making heavy profiles mandatory.
- Keep `orchestration`, `lake`, `governance` mutually exclusive by default. Only the
  documented catalog-ingest window may co-run lake+governance; Airflow stays down.
- Bind local ports to `127.0.0.1`; runner is not browser/public-facing. Base code read-only,
  dedicated workspace/evidence volumes writable.
- Preflight estimates/actuals and rejects unsupported combinations before startup.
- Capture host/Docker/browser/process RSS, CPU, disk, network, readiness, teardown and raw
  environment context. Compose `mem_limit` is not measurement.
- Credential placeholders stay local and cannot satisfy AWS schema.
- Support arm64 and amd64 where pinned images/tools permit; fail with remediation otherwise.

## Bounded Local Defaults

| Profile/journey | Provisional pass gate on 16 GiB machine |
|---|---|
| Core + portal + runner + test browser | Peak observed sandbox/browser RSS ≤4 GiB; ready ≤90s after dependencies installed; generated workspace ≤3 GiB |
| Learning + one of orchestration/lake/governance | Peak observed sandbox/browser/container RSS ≤10 GiB; host available memory remains ≥4 GiB; swap growth ≤512 MiB; no OOM/restart |
| Guarded learning + lake + governance ingest | Same ≤10 GiB/≥4 GiB headroom; Airflow confirmed down; ready ≤8 min; automatic lake teardown |
| Unsupported all-heavy combination | Denied before `docker compose up` |

Cold image/dependency download time is recorded separately and does not count toward service
readiness, but failures are surfaced. Threshold changes require a measured ADR, not silent doc
edits.

## Architecture

`profile-admission` resolves requested services, declared budgets, current host availability and
conflicts. It emits a run manifest, then Compose starts. `profile-measure` samples all relevant
process/container/browser resources and health endpoints until teardown, producing JSON consumed
by evidence/portal status.

## File Inventory

| Action | Likely path | Rough size | Test impact |
|---|---|---:|---|
| Modify | `docker-compose.yml` | 150-250 lines | Learning services, bindings, mounts, limits |
| Create | `config/profiles/local-profiles.yaml` | 120-200 lines | Admission source |
| Create | `scripts/profiles/{admit,measure,teardown}.py` | 600-900 LOC | Cross-platform resource evidence |
| Create | `tests/profiles/**` | 700-1,000 LOC | Matrix/overbudget/health/teardown |
| Create | `tests/compose/**` | 400-650 LOC | Render/security/mount/port |
| Modify | `Makefile`, `.env.example` | 80-140 lines | `learn`, checks, unique worktree project |
| Modify | README/runbook | 100-180 lines | Supported sequences/remediation |

## Interface Checklist

- [ ] `ProfileSpec(services, conflicts, budget, readiness, teardown)`
- [ ] `admit(profileSet, hostSnapshot) -> allow | reasons`
- [ ] resource sample/evidence schema
- [ ] unique Compose project/worktree/port derivation
- [ ] portal `ToolStatus` health adapter
- [ ] teardown verifies no container/process/temporary secret remains

## Dependency Map

- Requires runnable portal and admitted data labs.
- Blocks local release in Phase 13.
- Independent of AWS apply/cost TBCs.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| High | All heavy profiles requested | Pre-start denial with staged alternative |
| High | Memory headroom drops mid-run | Warning/cancel/teardown policy; evidence |
| High | Public bind or RW base mount | Compose security check fails |
| High | Worktrees collide on ports/volumes | Unique project resolution |
| High | Optional image/tool absent/arm mismatch | Core journey remains; remediation |
| High | Service healthy but lesson not ready | Readiness stays false |
| Medium | Teardown interrupted | Idempotent cleanup/recovery |

## Tests Before

Encode current profile matrix, ports, volumes and historical measured values. Add invalid
combination/public-bind/RW-mount/collision/overbudget fixtures.

## Refactor

Add learning services and explicit profile metadata. Tighten existing mounts/bindings without
breaking documented expert paths; coordinate Airflow path changes with Phase 7 tests.

## Tests After

Render every profile combination, run cold/warm measurements, force denial/pressure/failed-health,
verify teardown, and complete local journey with optional services absent.

## Regression Gate

```bash
make compose-check
make compose-security-check
make profile-budget-check
make local-journey-e2e
make recovery-test
docker compose config --quiet
```

## Implementation Steps

1. Write profile/admission/resource schemas and failing matrix/security tests.
2. Add learning Compose services with loopback/private/read-only boundaries.
3. Implement cross-platform admission and measurement collectors.
4. Add readiness and portal status integration.
5. Run cold/warm matrices on supported arm64/amd64 machines where available.
6. Enforce thresholds/conflicts and automatic teardown.
7. Update docs with measured, dated values and explicit exclusions.

## Success Criteria

- [ ] First journey fits the bounded local gates and completes without heavy services.
- [ ] Every supported heavy profile combination has raw measured evidence.
- [ ] Unsupported combinations are denied before start.
- [ ] Ports, mounts, placeholders and runner transport meet local security contract.
- [ ] Teardown is idempotent and leaves no active containers/processes or tracked artifacts.

## Risk, Security, and Rollback

RSS sources differ by OS/Docker VM; retain raw metrics and measurement method, not one opaque
number. Never collect environment secrets. Rollback removes the learning Compose profile while
preserving host-run portal/runner and existing profiles.

## Next Steps

Hand resource/readiness evidence to Phase 13. Do not extrapolate local measurements into AWS cost
claims.
