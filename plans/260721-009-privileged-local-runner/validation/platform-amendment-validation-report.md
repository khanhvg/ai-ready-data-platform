---
type: independent-platform-amendment-validation
issue: 9
date: "2026-07-22"
startHead: "4774c711208ef9cb7050b72c88106dffc7016f04"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
issue13PlanHead: "4a5ad724c94a606e0708064a536870f124ab8a2f"
backend: "local-rootless-container-pid-namespace"
verdict: PASS
readiness: READY_TO_COOK
cookScope: whole-plan
securityS3: PASS
resourceBudget: PASS
ownershipOverlap: PASS
operationFeasibility: "8/8-planned"
cloudAction: none
containerAction: none
---

# Independent Validation of the Local Container Platform Amendment

## Verdict

`PASS`; `READY_TO_COOK`; `COOK_SCOPE=whole-plan`.

A fresh read-only Herdr invocation used Codex `gpt-5.6-sol` with xhigh reasoning against the final
semantic plan diff. It found no Critical/High finding and no unresolved owner choice. Its terminal
result was:

```text
INDEPENDENT_VERDICT=PASS; SECURITY_S3=pass; RESOURCE_BUDGET=pass; OWNERSHIP_OVERLAP=pass; OPERATION_FEASIBILITY=8/8-planned; PLAN_VALIDATION=pass; COOK_SCOPE=whole-plan
```

The reviewed semantic diff SHA-256 was
`4282969cbc37e7b79cc4633011f2a68a707ca5787125f8364eacf3d01bc549a7`.
This is a review-input digest, not an image, release, commit or implementation identity.

## Review Closure

| Finding challenged during independent review | Final closure |
|---|---|
| Mixed create/copy/start ordering | Every lifecycle and recovery oracle is create, start-awaiting-input, copy, verify, execute |
| Older Issue #10/#13 Docker-free semantic wording | Owner direction makes engine absence typed preflight only; real journeys/profiles require the admitted engine |
| Unignored durable runtime evidence | App-owned exact `/.local-state/` rule, fixed state/evidence roots, baseline-delta and neighbor controls, context exclusion |
| Activation hash before i5-04.mk exists | Phase 2 closes shape only; Phase 3 hashes actual RED fragment bytes, emits and validates activation |

The active platform amendment supersedes only the historical backend/readiness conclusions. The
host capability evidence remains immutable: Seatbelt fork denial was 7/7, exact PID reap passed,
and host operation feasibility was 7/8 because pinned dbtRunner legitimately creates a Python
multiprocessing resource tracker.

## Deterministic Closure

| Check | Result |
|---|---|
| CK CLI | 4.5.2 |
| Strict plan validation | valid, zero issues, six phases |
| CK status | 0/6 complete; six pending, as required before cook |
| Released Stage A pins | 38/38 exact Git-object SHA-256 rows |
| Released contract set | 21/21 members plus registry pointer |
| Operations | 8/8 exact order; zero args; 120 seconds; 536870912 bytes; network denied |
| Release assets | 11/11 exact released order |
| Planned create paths | 87/87 unique and absent at start head |
| Catalogs | 24 RUN, 20 THR, 52 RED, 14 S3 |
| Local plan links | 21/21 at semantic review; zero broken |
| Scope | zero changed path outside the Issue #9 plan directory during validation |
| Root ignore policy | exact base/current hash match |
| Diff and safety scans | whitespace, protected paths, private paths, secrets, placeholders and predicted digest checks pass |

## Backend and Security Decision

The Linux PID namespace backend is the narrowest fit that preserves all eight operations. It
allows the pinned dbt resource tracker only inside a fresh operation namespace while init,
subreaper, cgroup and exact stop/KILL/wait/remove lifecycle—not polling—own descendant cleanup.
The host is a narrow owner control plane and exposes no raw execution or Docker authority to the
browser or container.

Plan-level S3 closure includes non-root UID 65532, read-only root, private tmpfs, no source/socket
mount, network none, zero ports, cap-drop ALL, no-new-privileges, seccomp, private namespaces,
closed environment, hostile archive checks, pids/memory/CPU/disk/file/FD/output/wall limits,
actual-digest admission, SBOM/provenance/license/vulnerability gates, CAS/audit/reset, rollback and
atomic eleven-asset release. Cook must prove each control from effective runtime state.

## Local Readiness Observation

Read-only discovery found Docker client 29.4.0 arm64 and OrbStack 2.2.1 installed, with the
orbstack context selected, engine stopped and socket absent. This is a typed
RUNNER_ENGINE_UNAVAILABLE prerequisite, not a planning blocker or fallback authorization. No
engine, image, container, registry, credential, cloud or other-worktree action occurred.
