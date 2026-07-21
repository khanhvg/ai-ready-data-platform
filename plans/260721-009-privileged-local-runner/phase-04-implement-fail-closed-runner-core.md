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
environment, macOS containment launcher, bounded process tree and service readiness. Keep existing
pipeline seams read-only and turn the corresponding Phase 3 security RED families GREEN.

## Context Links

- [Private transport and registry](./implementation-boundary-and-design.md#private-transport)
- [Host containment and quotas](./implementation-boundary-and-design.md#host-containment-and-process-quotas)
- [RUN-TRN/CMD/FS/ENV/NET/RES](./requirements-risk-threat-traceability.md#requirement-crosswalk)

## Requirements

- Python 3.12.3, Darwin/arm64/macOS-build and hash-complete runtime lock preflight.
- UDS owner-only default; explicit 127.0.0.1 ephemeral fallback; strict admission before parsing.
- Released Issue #8 typed operation/command inputs only.
- Pinned read-only entrypoints, Python `-I`, generated workspace dbt configuration.
- Descriptor-owned workspace paths, Seatbelt write/read/network policy and fail-closed probe.
- Complete bounded process-tree execution and sanitized output.

## Architecture

```text
BFF-only request
  -> transport admission (Host/Origin/auth/CSRF/fetch/content/idempotency)
  -> released typed operation
  -> fixed command descriptor
  -> descriptor-owned workspace + generated exact env
  -> launcher (fchdir, rlimits, close FDs, new session)
  -> sandbox-exec profile
  -> pinned Python -I / fixed entrypoint
  -> process-tree/resource/output monitor
```

## Related Code Files

- Create: `apps/lab-runner/pyproject.toml`
- Create: `apps/lab-runner/requirements/runner-py312-macos-arm64.{in,lock,metadata.json}`
- Create: `apps/lab-runner/config/runtime-policy-v1.toml`
- Create: `apps/lab-runner/src/lab_runner/{__init__,__main__,contract,registry,transport,containment,launcher,workspace,process,service}.py`
- Create: `apps/lab-runner/tests/integration/test_bounded_pipeline.py`
- Modify: `orchestration/airflow/callables/pipeline.py` only to add the characterized runner-reserved path refusal before `_run`
- Consume read-only: Phase 1 seams, Issue #6 release schema, Issue #8 release contracts
- Delete: none

## Tests Before

Use the committed Phase 3 RED manifest. Implement in this order: dependency/runtime refusal,
transport pre-admission, registry/argv, workspace/path, environment/import, containment/network,
then quotas/output/descendants. A later class cannot be used to hide an earlier failing oracle.

## Implementation Steps

1. Compile a wheel-only hash-complete app lock and metadata from the exact supported host/runtime;
   bootstrap below an app-owned private tool root keyed by lock hash. No runtime install/network.
2. Parse `runtime-policy-v1.toml` with strict unknown-field rejection and verify its own hash from
   the released-contract lock.
3. Implement contract/registry loading. Resolve only the exact eight commands and construct fixed
   descriptors with absolute interpreter/entrypoint/hash, argv template, env keys, CWD role,
   resource class, write set and network deny.
4. Implement workspace allocation through directory FDs, exclusive marker/nonce, private modes,
   type/link/device/inode checks, relative safe operations and marker-verified cleanup refusal.
5. Implement UDS service and explicit loopback fallback. Enforce exact request admission before
   body read or audit/operation allocation; bind secrets to launch only and exclude them from child
   and evidence roots.
6. Implement the separate launcher: inherit only approved descriptors, `fchdir`, apply rlimits,
   close other FDs, start session/process group, and `execve` Seatbelt + pinned command.
7. Generate minimal Seatbelt profiles from fixed policy paths. Startup functional probes prove
   base read-only, workspace write, home/secret/network denial, required imports and child cleanup.
8. Implement process-tree PID/start tracking, 100 ms aggregate CPU/RSS/disk/process monitoring,
   output limits, secret/private-path detection, TERM/KILL/reap and typed failure results.
9. Add adapters that invoke current generator/loader/dbt/export with workspace paths only. Generate
   a dbt profile below the generation; never write base profiles/targets/logs/packages.
10. Add the characterized Airflow callable guard for every explicit mutable/config path. Reject
    lexical or resolved runner-reserved paths before `_run`; preserve expert defaults and DAG
    import/task order. Turn the learner-targeted direct-call RED test GREEN.
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
