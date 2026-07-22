---
title: "I5-04 — Build isolated privileged local runner"
description: "Deep/TDD plan for a fail-closed local non-root Docker/OrbStack runner that executes all eight released operations in one Linux PID-namespace backend."
status: pending
priority: P1
issue: 9
branch: "plan/issue-9-privileged-local-runner"
tags: [feature, backend, security, critical, tdd, local-runner, containers]
blockedBy: []
blocks: []
created: "2026-07-21"
createdBy: "ck:plan"
source: skill
planningMode: "workflow-equivalent-deep-tdd-planner-only"
planningModel: "gpt-5.6-sol"
modelReasoningEffort: "xhigh"
originalPlanningBaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
amendmentStartSha: "4774c711208ef9cb7050b72c88106dffc7016f04"
issue6ReleaseSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
issue8ReleasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
issue8ReleaseTree: "27fc3667ef37892dad5c3fbfd76769f65a0760be"
requiredImplementationAncestorSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
dependencyCompatibility: "PASS"
backend: "local-rootless-container-pid-namespace"
containerPlatform: "linux/arm64"
runnerActivationInstancePath: "apps/lab-runner/config/command-owner-activation-i5-04-v1.json"
runnerRequestBodyLimitBytes: 16384
operationFeasibility: "8/8-planned-cook-proof-required"
implementationHeadPolicy: "record-the-actual-clean-remote-equal-descendant-after-it-exists"
implementationReadiness: "READY_TO_COOK"
cookScope: "whole-plan"
engineDiscovery: "Docker CLI 29.4.0 arm64 and OrbStack 2.2.1 installed; orbstack context selected; engine stopped and user socket absent"
sharedContractLease: "NO_WRITE_OVERLAP_READ_ONLY_STAGE_A_CONSUMPTION"
issue13Ownership: "DOWNSTREAM_IMAGE_AND_LAUNCHER_CONSUMER_ONLY"
cloudAction: "none"
containerActionDuringAmendment: "none"
platformValidationReport: "validation/platform-amendment-validation-report.md"
platformReadinessAudit: "audit/platform-readiness-audit-2026-07-22.md"
platformChecksumManifest: "validation/platform-readiness-sha256.txt"
---

# I5-04 — Build Isolated Privileged Local Runner

## Overview

Plan an Issue #9-owned local runner whose entire released eight-command execution truth lives
inside one dedicated Linux/arm64 container backend. The host service remains an owner-only control
plane: strict UDS or random-loopback admission, released request validation, CAS/idempotency/audit,
fixed Docker Engine lifecycle calls, verified output import, and atomic release publication. It
never executes a semantic operation on the host and never accepts a raw shell, executable,
environment, path, URL, SQL, plugin, package-install, Docker, or cloud override.

The [local container platform amendment](./platform-amendment.md) supersedes the active decision in
the [host capability amendment](./capability-amendment.md). The earlier evidence remains valid:
Seatbelt prevents seven child-creation families and reaps one exact worker, but the released
retail.dbt-build operation legitimately starts Python multiprocessing resource-tracker state.
That makes the host strategy 7/8 and unusable. A private Linux PID namespace plus init/subreaper,
container cgroup and whole-container stop/kill/remove lifecycle admits that required helper while
containing double-fork, reparent and setsid descendants.

Planning inspection observed Docker CLI 29.4.0 and OrbStack 2.2.1 on Darwin arm64, with the
orbstack context selected, OrbStack stopped, and no socket. This is a supported fail-closed
prerequisite state: runtime returns RUNNER_ENGINE_UNAVAILABLE and performs no host fallback. Cook
may start the local engine only after recording the separate local side-effect gate. No admin,
TCC, cloud, container, image pull, or image build action occurred during this amendment.

## Phases

| Phase | Name | Status |
|---|---|---|
| 1 | [Characterize seams and design RED fixtures](./phase-01-characterize-seams-and-design-red-fixtures.md) | Pending |
| 2 | [Bind released Issue 8 Stage A contract](./phase-02-bind-released-issue-8-stage-a-contract.md) | Pending |
| 3 | [Write transport and containment RED suites](./phase-03-write-transport-and-containment-red-suites.md) | Pending |
| 4 | [Implement fail-closed runner core](./phase-04-implement-fail-closed-runner-core.md) | Pending |
| 5 | [Implement fencing state and atomic release](./phase-05-implement-fencing-state-and-atomic-release.md) | Pending |
| 6 | [Prove S3 evidence rollback and handoff](./phase-06-prove-s3-evidence-rollback-and-handoff.md) | Pending |

## Dependencies and Direction

- Issue #6 remains shipped at 24be3b34c6b0fcdbd07c5800dcab349054e34713.
- Issue #8 Stage A remains released at
  fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9 with tree
  27fc3667ef37892dad5c3fbfd76769f65a0760be. Its exact contracts are read-only.
- Owner platform direction selects a local rootless/non-root Docker-compatible container backend
  for all eight operations. It does not approve a future implementation head, image digest, PR,
  merge, or cloud action.
- Exact image and base digests are deliberately absent now. Cook must observe the linux/arm64 base
  manifest, write the actual digest lock, build the image, capture its actual OCI manifest/config
  digests, and bind those measured values before any container acceptance test or PR handoff.
- Engine absence alone is not a planning blocker because the CLI and OrbStack app exist. Runtime
  and cook preflight fail closed until a separately gated local engine start makes the exact
  user-owned socket, API, cgroup v2, seccomp, init and resource controls observable.
- This owner platform direction resolves older downstream Docker-unavailable wording: Issue #10's
  real runner journey and Issue #13's runner profiles require the admitted engine. Their
  Docker-unavailable checks may assert only fail-closed RUNNER_ENGINE_UNAVAILABLE behavior, never
  semantic success or a host fallback; their owners carry that clarification into their own
  plans before cook.

## Ownership and Non-Overlap

Issue #9 owns only:

- apps/lab-runner/**, including runner source/tests, Linux lock files, container build files,
  seccomp profile, deterministic context builder, image lock/release record, and host launcher;
- mk/issue-5/i5-04.mk with only runner-test, runner-security-test and runner-race-test.

Issue #13 may later consume the released image identity and the Issue #9 launcher in local
profiles. It may not rebuild, duplicate, patch, mount over, or otherwise modify runner internals.
Issue #9 does not modify root Make, docker-compose.yml, any Compose/profile file, the Airflow
Dockerfile, Airflow callables/DAGs, shared contracts, golden core, portal paths, cloud, Terraform,
Kubernetes, or any Issue #13 path.

## Design and Traceability

- [Local container platform amendment](./platform-amendment.md)
- [Implementation boundary and design](./implementation-boundary-and-design.md)
- [Requirements, risks, and threat traceability](./requirements-risk-threat-traceability.md)
- [Verification, evidence, and rollback](./verification-evidence-and-rollback.md)
- [Exact planned paths and admission gates](./planned-paths-and-admissions.md)
- [Dependency-release amendment](./release-amendment.md)
- [Historical host capability amendment](./capability-amendment.md)
- [Independent platform validation](./validation/platform-amendment-validation-report.md)
- [Platform readiness audit](./audit/platform-readiness-audit-2026-07-22.md)
- [Protected artifact hashes](./validation/platform-readiness-sha256.txt)

## Cook Gate

COOK_SCOPE=whole-plan. The six phases remain ordered.

1. Phase 1 first revalidates clean Stage A ancestry, exact host/CLI/app identities and the stopped
   engine behavior. If engine start is needed, cook records the authorized local side-effect gate
   before starting OrbStack; any admin/TCC prompt or unavailable engine stops.
2. Phase 2 binds released contracts and measured supply-chain inputs. No base or runner digest is
   guessed.
3. Phase 3 commits real RED shards, the fixed no-argument shard harness and bounded public verifier
   tests before production container/launcher behavior.
4. Phase 4 implements one image/backend and proves all eight operations, including pinned
   dbtRunner with its resource tracker inside the namespace.
5. Phase 5 implements durable host CAS/audit/evidence and exact output/release publication without
   moving any semantic operation to the host.
6. Phase 6 runs the complete security, resource, recovery, evidence and exact-head review gates.

Any missing engine/image/digest/tool, ignored runtime flag, container leak, operation stub,
7/8 result, host fallback, ownership overlap, or unresolved Critical/High finding stops cook.

## Success Criteria

- All eight exact released semantic operations execute for real inside the same dedicated runner
  image/backend; no operation is dropped, stubbed, faked, or executed on the host.
- Linux PID namespace plus init/subreaper and container lifecycle are containment authority.
  Polling and process inventories are evidence only.
- Non-root UID, read-only root, private tmpfs workspace, no host source/socket mount, network none,
  cap-drop ALL, no-new-privileges, seccomp, private PID/IPC, no added host device/device request or
  privileged mode, and exact cgroup, disk, file, FD, output and wall limits are proven from
  effective Engine state.
- retail.dbt-build uses the released pinned dbtRunner path and contains its multiprocessing
  resource tracker in the namespace.
- Host/Origin/CSRF/launch-secret/private-listener rules remain strict; the browser never contacts
  Docker or the runner container.
- CAS, reset, crash reconciliation, append-only audit/evidence and atomic eleven-asset release are
  preserved with exact regular-file, link, owner, size and SHA-256 checks.
- Issue #9 and Issue #13 ownership is mechanically non-overlapping.
- A fresh exact-head whole-plan validation and readiness audit pass before cook handoff; two later
  independent implementation reviews and separate human exact-head approval remain pre-merge.

## Validation Log

### Historical sessions

The release and host-capability reports remain immutable evidence for their exact inputs. Their
READY/BLOCKED conclusions are superseded only by the active platform amendment; their measured
Stage A pins, 7/7 Seatbelt denial, exact worker reap and 7/8 operation result are not rewritten.

### Local container platform amendment — 2026-07-22

- Start head: 4774c711208ef9cb7050b72c88106dffc7016f04.
- Owner decision: one local rootless/non-root Docker-compatible PID-namespace backend for all
  eight operations; no mixed host/container truth.
- Engine inspection: Docker CLI 29.4.0 arm64 and OrbStack 2.2.1 installed; current context
  orbstack; app/engine stopped; socket absent; no state change.
- Backend decision: local-rootless-container-pid-namespace.
- Operation feasibility: 8/8 planned, with real cook proof mandatory.
- Exact future-create allow-list: 87 unique paths, all absent at amendment start.
- Catalogs: 24 requirements, 20 threats, 52 RED assertions and 14 S3 gates.
- Independent final exact-diff verdict: PASS; SECURITY_S3=pass; RESOURCE_BUDGET=pass;
  OWNERSHIP_OVERLAP=pass; OPERATION_FEASIBILITY=8/8-planned; PLAN_VALIDATION=pass;
  COOK_SCOPE=whole-plan.
- Open owner choices: none.
