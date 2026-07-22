# Phase 3 — Commit Public-Path Container RED Suites

## Objective

Commit tests and inert adversarial fixtures before production launcher/container behavior. Fast
contract/policy tests first fail through the three public I5-04 verifier targets. Long-running real
container cases first fail through the fixed no-argument shard harness for the intended missing
behavior, not because collection is broken.

## TDD Gate

Production source, Dockerfile behavior and image release records remain absent. Tests may define
schemas/helpers inside test code only. Capture a RED manifest containing assertion ID, threat,
suite/shard, verifier target, expected failing assertion and fixture hash. The fixed
apps/lab-runner/tools/run-gate.py invocation has no selector and runs every declared shard; no
caller can skip a case. Commit this test-only slice before Phase 4.

After the exact i5-04.mk RED verifier fragment exists, hash its actual bytes and emit the Issue #9
activation instance with the released base-registry hash and exactly the three fitness-result-v2
commands. Validate it with the released activation schema/verifier in the same RED commit. No
placeholder fragment or activation hash is permitted.

## Required RED Families

1. Transport: Host/Origin/CSRF/bearer/UDS peer, duplicate headers, cookies, Fetch Metadata, CORS,
   framing and 16384-byte body limit before allocation.
2. Registry: exact eight enum values and fixed zero-argument descriptors; raw argv/env/path/URL/
   SQL/plugin/install/image/Docker options rejected.
3. Engine: stopped/missing/wrong-owner/non-socket/remote endpoint, ignored effective fields and
   stale image identity fail closed with no host fallback.
4. PID lifecycle: rapid double-fork, reparent, setsid, daemonized child, TERM-ignore, main crash,
   resource-tracker, and zero survivors after stop/KILL/wait/remove.
5. Fork bomb: real fork pressure reaches pids-limit 64, remains bounded, and teardown removes the
   namespace. A polled list is asserted as evidence only.
6. Network: DNS, TCP, UDP, listener and cloud metadata probes fail under network none; no published
   port or resolvable DNS path exists.
7. Filesystem/archive: read-only root/base, traversal, symlink, hardlink, FIFO/socket/device,
   sparse/oversize, ownership/mode/count/hash mismatch and use-time swap.
8. Environment/output: cloud, credential, proxy, Docker, home, Python/dbt plugin and tracing
   canaries absent; stdout/stderr/protocol/output flood bounded without raw persistence.
9. Resources: memory/no-swap, CPU, pids, workspace/tmpfs, file, FD and 120-second TERM-to-KILL
   envelopes verified from effective state and observable enforcement.
10. Recovery: interrupted create/start-awaiting-input/copy/verify/execute/archive/stop/remove, main
    crash, stale/reused container identity, duplicate request, stale fence and restart
    reconciliation.
11. Atomicity: reset and exact eleven-asset export crash/concurrency matrices preserve old-or-new
    complete state.
12. Feasibility: one real-flow assertion per exact command, with retail.dbt-build requiring pinned
    dbtRunner and its tracker contained inside the namespace.

## Shards and Public Verifier Targets

The no-argument shard harness runs contract/unit, all-eight, expert compatibility, transport,
Engine, containment, supply-chain, race, recovery and rollback cases. Each shard records exact
head/image/policy/fixture identities, monotonic timing, result and artifact hashes. Long suites may
take more than 120 seconds overall; no shard or operation exceeds its own applicable limit.

- runner-test verifies the complete fresh functional shard set, all-eight/expert results and
  evidence closure, then emits one fitness-result-v2 verifier envelope in under 120000 ms.
- runner-security-test verifies the complete fresh security/S3 shard set, including the real
  110-second timeout shard, then emits one fitness-result-v2 verifier envelope in under 120000 ms.
- runner-race-test verifies the complete fresh race/recovery/rollback shard set and emits one
  fitness-result-v2 verifier envelope in under 120000 ms.

Each verifier rejects a missing, stale, duplicate, failed, skipped, foreign-head/image/policy or
hash-mismatched shard. It never claims the aggregate shard execution duration as its own
durationMs. data-contracts-check remains the released I5-01 fitness-result-v1 target and is not
modified.

## RED Acceptance

- All tests collect with stable fixture hashes and no skipped required assertion.
- Each behavior shard fails at its intended production seam; missing engine is used only by the
  dedicated preflight test, not to fake adversarial container coverage.
- No fixture can escape its future operation container or select host paths.
- Protected paths remain unchanged; only exact Issue #9 test, fixture, package metadata and
  i5-04.mk wiring appear in the test-only commit.

## Exit Criteria

- The complete RED catalog is committed separately.
- The fixed no-argument shard harness and exact four verifier commands are wired without root Make
  changes.
- The activation instance binds the actual i5-04.mk fragment hash and validates against the
  released schema; Phase 2 did not predict it.
- Reviewer can map every RUN and THR row to at least one RED assertion.

## Rollback

Revert only the Issue #9 RED commit. No container/image/runtime cleanup is necessary because this
phase does not build or run the production image.
