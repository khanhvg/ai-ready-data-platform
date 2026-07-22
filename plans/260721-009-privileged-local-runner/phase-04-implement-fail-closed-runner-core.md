---
phase: 4
title: "Implement fail-closed runner core"
status: pending
priority: P1
dependencies: [3]
effort: "2.5 implementation days"
---

# Phase 4: Implement Fail-Closed Runner Core

## Overview

Implement the app-owned typed registry, private transport, secure workspace allocator, exact
environment, macOS containment launcher, bounded single worker and service readiness. Keep existing
pipeline seams read-only and turn the corresponding Phase 3 security RED families GREEN.

`BLOCKED`: exact dbt currently requires a resource-tracker child. No source step in this phase is
authorized until all eight reviewed fixed in-process adapters pass the capability amendment gate.

## Context Links

- [Private transport and registry](./implementation-boundary-and-design.md#private-transport)
- [Host containment and quotas](./implementation-boundary-and-design.md#host-containment-and-process-quotas)
- [RUN-TRN/CMD/FS/ENV/NET/RES](./requirements-risk-threat-traceability.md#requirement-crosswalk)

## Requirements

- Python 3.12.3, Darwin/arm64/macOS-build and hash-complete runtime lock preflight.
- UDS owner-only default; explicit 127.0.0.1 ephemeral fallback; strict admission before parsing.
- Released API/operation/request schema versions and the exact eight zero-argument lab commands
  only; no synthetic command-version or generated binding.
- Pinned read-only entrypoints, Python `-I`, generated workspace dbt configuration.
- Descriptor-owned workspace paths, Seatbelt write/read/network policy and fail-closed probe.
- Conditional exact single-worker execution with zero descendants and sanitized output.
- Seatbelt denial before first child plus exact PID/start TERM→KILL→wait; no process-tree discovery,
  process-group, launchd, or polling cleanup authority.
- Released per-command ceilings are 120 seconds and 536,870,912 bytes; released workspace quota is
  268,435,456 bytes. The runner may be stricter but never wider.
- Keep service not-ready unless the exact I5-04 activation path validates with measured
  registry/fragment/instance hashes and the 16,384-byte private request ceiling is active.

## Architecture

```text
BFF-only request
  -> transport admission (Host/Origin/auth/CSRF/fetch/content/idempotency)
  -> released typed operation
  -> fixed command descriptor
  -> descriptor-owned workspace + generated exact env
  -> launcher (fchdir, rlimits, close FDs, new session)
  -> sandbox-exec profile
  -> pinned Python -I / fixed in-process adapter
  -> exact single-worker resource/output monitor (zero descendants)
```

## Related Code Files

- Extend only if behavior packaging requires it: `apps/lab-runner/pyproject.toml`; any change
  invalidates the Phase 3 RED attestation and requires a fresh pre-behavior RED commit
- Consume/verify: `apps/lab-runner/requirements/runner-py312-macos-arm64.{in,lock,metadata.json}`
- Extend only with re-attested RED: `apps/lab-runner/config/runtime-policy-v1.toml`
- Consume/rehash: `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`
- Create: `apps/lab-runner/src/lab_runner/{__init__,__main__,contract,registry,transport,containment,launcher,adapters,workspace,process,service}.py`
- Create: `apps/lab-runner/tests/integration/test_bounded_pipeline.py`
- Conditional modify: `orchestration/airflow/callables/pipeline.py` only if Phase 1 still proves
  the characterized runner-reserved path refusal is necessary before `_run`
- Consume read-only: Phase 1 seams, Issue #6 release schema, Issue #8 release contracts
- Delete: none

## Tests Before

Use the committed Phase 3 RED manifest. Implement in this order: dependency/runtime refusal,
transport pre-admission, registry/argv, workspace/path, environment/import, containment/network,
then quotas/output/descendants. A later class cannot be used to hide an earlier failing oracle.

## Implementation Steps

1. Verify the Phase 3 wheel-only hash-complete app lock and metadata on the exact supported
   host/runtime; bootstrap below an app-owned private tool root keyed by lock hash. No runtime
   install/network. Any lock or gate-scaffold change requires a new contemporaneous RED commit
   before behavior resumes.
2. Parse `runtime-policy-v1.toml` with strict unknown-field rejection, enforce exactly
   `RUNNER_REQUEST_BODY_LIMIT_BYTES=16384`, and verify its own hash from the released-contract lock.
3. Implement contract/registry loading through the released readers. Resolve only the exact eight
   zero-argument commands and construct fixed
   descriptors with absolute interpreter/entrypoint/hash, argv template, env keys, CWD role,
   resource class, write set and network deny.
4. Implement workspace allocation through directory FDs, exclusive marker/nonce, private modes,
   type/link/device/inode checks, relative safe operations and marker-verified cleanup refusal.
5. Implement UDS service and explicit loopback fallback. Enforce the 16,384-byte request policy
   by rejecting invalid framing or an excessive declared length before body read, stopping a
   bounded streaming read at the ceiling, then validating the released request schema before
   audit/operation allocation; bind secrets to launch only and exclude them from child/evidence
   roots.
6. Implement the separate launcher: inherit only approved descriptors, `fchdir`, apply rlimits,
   close other FDs, and launch exactly one fixed Python worker through Seatbelt. Record exact
   PID/start identity before capability handoff.
7. Generate minimal Seatbelt profiles from fixed policy paths, including `deny process-fork`.
   Startup functional probes prove base read-only, workspace write, home/secret/network denial,
   all child attempts denied before first marker, and exact same-worker reap.
8. Implement exact worker CPU/RSS/disk/FD/output monitoring, protocol/image-failure detection,
   secret/private-path detection and bounded TERM→KILL→wait. Zero descendants is invariant; any
   fork/spawn/exec need makes readiness false before operation allocation.
9. Add eight fixed in-process adapters only after the capability gate passes. Current generator,
   loader, exporter and promotion verifier have feasible callables; current Airflow wrappers are
   expert-only. Exact dbt remains the blocker. Generate workspace-local dbt configuration and
   never mutate private multiprocessing context, start method, plugins, startup hooks, base
   profiles/targets/logs/packages, or the released command set.
10. If Phase 1 still proves the Airflow seam necessary, add the characterized guard for every
    explicit mutable/config path. Reject lexical or resolved runner-reserved paths before `_run`;
    preserve expert defaults and DAG import/task order. Otherwise leave the file byte-identical.
    In either case, turn the learner-targeted direct-call RED test GREEN through the narrowest
    already-admitted behavior.
11. Turn transport/registry/path/env/network/quota/output/descendant/base RED suites GREEN.

## Refactor

The only existing-seam refactor is the pre-spawn Airflow reserved-path guard; it does not make
Airflow participate in learner execution. Consolidate app-owned identity checks, request admission
and child termination so every runner command uses the same audited code path.

## Tests After

- Run all Phase 4 unit/security suites twice on the exact supported host.
- Run one bounded `small`/42 generate→load→dbt→export adapter flow in a private generation.
- Verify entrypoint/base/protected hashes, repository data/warehouse/dbt/export paths and expert
  namespace remain unchanged.
- Verify unsupported host/build, failed containment probe and contract drift report not-ready and
  allocate no operation/workspace.

## Regression Gate

- `RED-INT`, `RED-IMP`, `RED-ARGV`, `RED-PATH`, `RED-ENV`, `RED-NET`, `RED-QUOTA`,
  `RED-OUT`, `RED-DESC`, `RED-BASE`, and `RED-BROWSER` families are GREEN.
- Every refusal is typed and no required test skipped.
- No child, listener, secret file or temp path survives its owner lifecycle.

## Risk and Security

Seatbelt availability is a mandatory host capability, not a convenience. Process controls without
write/network containment are insufficient; if the functional profile cannot run the real pinned
pipeline, keep the runner disabled instead of widening rules until independent review accepts the
smallest measured addition.

## Success Criteria

- [ ] Only exact released typed commands reach pinned execution.
- [ ] Browser-direct, base-write, network, env/import and resource attacks fail safely.
- [ ] The supported 16 GiB host executes one bounded real local pipeline generation.
- [ ] Unsupported hosts and drift remain disabled without mutation.

## Next Steps

Phase 5 adds durable state, fencing, idempotency, audit and atomic release; Phase 4 must not publish
a current release or claim crash recovery by itself.
