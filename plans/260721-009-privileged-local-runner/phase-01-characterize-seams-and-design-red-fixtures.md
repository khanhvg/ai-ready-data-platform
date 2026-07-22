# Phase 1 — Characterize Seams and Record Local Engine Gate

## Objective

Freeze the exact released implementation seams, confirm the implementation tree is an eligible
clean remote-equal Stage A descendant, and resolve the local engine prerequisite without executing
any semantic operation or weakening containment.

## Entry Gates

- Work only in the designated Issue #9 worktree and branch.
- Local, tracking and remote heads are equal and descend from
  fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9.
- Changed paths are empty before cook.
- Owner platform direction and whole-plan cook scope are recorded.

## Steps

1. Recompute all Phase 2 Stage A hashes directly from the implementation tree and released Git
   object. Stop on any missing path, changed byte or ancestry mismatch.
2. Characterize the real generator, loader, dbt project/profile/models/tests/macros, exporter,
   golden workspace/process/release helpers and exact eleven-asset order. Record callable/module
   identities without changing them.
3. Prove the eight command IDs are zero argument and each retains network denied, 120 seconds and
   536870912 bytes; prove workspace quota 268435456 and profile small/seed 42.
4. Record Docker CLI/app/context/socket discovery read-only. Service preflight against the stopped
   state must yield RUNNER_ENGINE_UNAVAILABLE and allocate no operation/container/fallback.
5. If the installed engine is still stopped, record the separate local-side-effect gate stating
   app name, expected user socket and that starting the app changes local state. Only after that
   gate may autonomous cook start OrbStack. Stop on admin/TCC prompts; never automate them.
6. Once reachable, accept only a local Unix socket owned by the effective user. Record Engine API,
   server architecture, linux/arm64 support, cgroup version, seccomp availability, init support and
   resource-control capability. Reject TCP/remote contexts and do not authenticate to a registry.
7. Write characterization tests and fixture manifest paths from the exact allow-list. Fixture
   content is inert until Phase 3 and cannot alter product behavior.
8. Record protected path hashes and an Issue #9/Issue #13 ownership scan baseline. Characterize
   current ignore behavior and retain an exact ignored-inclusive status baseline, then require the
   future app-owned apps/lab-runner/.gitignore to ignore only `/.local-state/`; the root .gitignore
   and unrelated pre-existing ignored entries remain protected.

## Verification

- Stopped-engine preflight is deterministic and fail-closed.
- No container, image or semantic operation is required for the stopped-engine assertion.
- If the gated engine start occurs, only engine capability inspection follows in this phase; no
  image pull/build or operation container starts before the later explicit build/test steps.
- Golden/expert paths remain byte-identical.
- Fixed workspace/evidence roles are ignored only by the app-owned rule, a neighboring unlisted
  file remains visible, and the deterministic context excludes the entire runtime state root.

## Exit Criteria

- Eligible exact implementation head and released inputs are recorded.
- Engine is either reachable through the admitted socket or cook is blocked with the exact local
  prerequisite; no insecure alternative is proposed.
- Characterization and fixture plan covers all eight operations and every adversarial family.
- No ownership overlap or protected-path drift exists.

## Rollback

This phase makes only Issue #9 test/plan artifacts plus an explicitly gated app start. If the local
app was started by cook and rollback policy authorizes returning it to its observed stopped state,
record that separate side effect; otherwise leave engine state to the owner. Never stop unrelated
processes or remove containers/images.
