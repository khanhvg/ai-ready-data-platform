---
phase: 4
title: "Privileged Local Lab Runner and Security Boundary"
status: pending
priority: P1
dependencies: [1, 3]
effort: "L"
---

# Phase 4: Privileged Local Lab Runner and Security Boundary

<!-- Updated: Validation Session 1 - classified all file destinations as planned artifacts. -->

## Overview

Build the isolated local runner that executes only typed, allow-listed retail lab operations in a
scoped workspace. Protect repository files, secrets and state transitions even though the first
release has one localhost learner.

## Context Links

- [Runner boundary ADR](./architecture-decisions.md#adr-002-portal-and-runner-boundary)
- [Runner command/state contract](./lesson-lab-contract.md)
- PH-C05/PH-C06, SC-02/03/14 in [traceability](./requirements-traceability.md)
- Current reusable entrypoints: `orchestration/airflow/callables/pipeline.py`

## Requirements

- Separate process; prefer Unix socket, otherwise random loopback port plus private startup token.
- Browser never receives runner credential; portal BFF is the only caller.
- Typed Pydantic/domain models from released schemas; `subprocess` argument arrays,
  `shell=False`, sanitized allow-listed env and fixed command registry.
- Base checkout/scripts mounted/readable only; workspace under ignored runtime root; reject
  symlinks, traversal, device files, oversized inputs and user-controlled cwd/network targets.
- Per-workspace lock, idempotency ledger, transition journal, timeout/cancel and CPU/memory/disk
  quotas.
- Atomic reset from every state. Evidence binds last committed verified run.
- No Terraform apply/destroy, arbitrary shell, package install, external URL or AWS credential.
- Preserve static lesson and expert direct-command paths when runner is disabled.

## Architecture

```text
Portal BFF -> private transport -> runner API
  -> auth/correlation -> schema -> workspace ownership/path -> command policy -> resource admission
  -> command registry -> child process in workspace
  -> state journal -> verifier/evidence staging
```

Leading runtime is a small Python service with framework-independent domain core; FastAPI is the
bounded default transport because it matches typed OpenAPI/Pydantic and existing Python, but the
domain/command/workspace code must not depend on HTTP.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `apps/lab-runner/pyproject.toml`, locked deps | small | Reproducible runner |
| Create | `apps/lab-runner/src/lab_runner/{domain,policy,commands,workspace,state,evidence}.py` | 1,200-1,800 LOC | Core |
| Create | `apps/lab-runner/src/lab_runner/transport/http.py` | 250-400 LOC | Private API |
| Create | `apps/lab-runner/tests/unit/**` | 800-1,200 LOC | Policy/state/commands |
| Create | `apps/lab-runner/tests/security/**` | 600-900 LOC | Fuzz/traversal/secret/base write |
| Create | `apps/lab-runner/tests/race/**` | 400-700 LOC | Barrier/crash/replay |
| Create | `scripts/labs/verify-promotion-trust.py` | 200-350 LOC | Real verifier |
| Modify | `orchestration/airflow/callables/pipeline.py` and existing CLIs | narrow, contract-protected | Explicit workspace paths |
| Modify | `Makefile` | 20-40 lines | Runner test targets |

## Interface Checklist

- [ ] `CommandDescriptor(id, args, timeout, resources, networkPolicy)`
- [ ] `CommandRegistry.resolve(id)` has no raw command override; typed configuration writers are schema-bound
- [ ] `WorkspaceManager.prepare/reset/resolve_safe_path`
- [ ] `LabStateRepository.compare_and_transition`
- [ ] `IdempotencyRepository.begin/complete/reconcile`
- [ ] `EvidenceStager.commit_verified`
- [ ] transport auth, correlation, problem responses and health/readiness

## Dependency Map

- Depends on golden workspace seams and released learning/OpenAPI/evidence contracts.
- Blocks Phase 5 and runner-backed portions of Phase 7.
- Does not depend on web framework internals, AWS or hosted identity.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Metacharacter/traversal/symlink/device/oversize | Reject before child process |
| Critical | Reset races verify/publish | Serialize/typed conflict; no mixed evidence |
| Critical | Base repo write/secret canary/env injection | Denied; base tree/hash unchanged |
| Critical | Duplicate/replayed operation | Same result or safe conflict; no duplicate work |
| High | Child timeout/crash/host restart | Journal last committed state; recover/reset |
| High | Browser/direct caller reaches runner | Auth/transport denial |
| High | Terraform-like command/flag | No registry entry; denial |
| Medium | Runner unavailable | Portal-compatible typed unavailable state |

## Tests Before

Write security/race/state tests using harmless probe executables and real golden workspace
fixtures. Assert child argv/env/cwd exactly. Capture pre/post repository tree and secret canary.

## Refactor

Parameterize existing Python entrypoints/callables to accept workspace paths; keep defaults and
Airflow graph unchanged under Phase 1 characterization.

## Tests After

Run real bounded prepare→generate→load→dbt→export→configure→verify→reset; inject failures at every
state and write boundary; fuzz APIs; kill/restart runner; verify evidence and base integrity.

## Regression Gate

```bash
make runner-test
make runner-security-test
make runner-race-test
make golden-clean PROFILE=small SEED=42
git status --short
```

## Implementation Steps

1. Threat-model actors/resources/actions, base/workspace, secrets and transport.
2. Write failing policy/state/race/crash tests.
3. Implement domain state/idempotency/workspace core.
4. Implement the fixed command registry, safe typed configuration writer and resource-limited process adapter.
5. Add private transport aligned to OpenAPI; keep browser out of trust zone.
6. Add promotion verifier and evidence commit.
7. Refactor only required current path seams behind characterization tests.
8. Run complete security/race/golden regression suite and document disable/rollback.

## Success Criteria

- [ ] Only declared command IDs and typed args can execute.
- [ ] Repository/control files and secrets remain unreachable/unmodified.
- [ ] Same-user reset/verify races and retries are recoverable and deterministic.
- [ ] Real bounded retail journey commands execute in an isolated workspace.
- [ ] Runner can be disabled without losing lesson content or direct expert workflows.

## Risk, Security, and Rollback

This is the highest-risk local boundary. Default deny, minimal environment/network, resource
limits and read-only base are mandatory. Rollback disables the runner/BFF integration and removes
workspaces; existing Make/Airflow commands and static portal content remain.

## Next Steps

Phase 5 integrates only through the typed BFF; no direct browser/runner coupling.
