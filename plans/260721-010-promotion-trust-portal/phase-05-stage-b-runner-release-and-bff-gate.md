---
phase: 5
title: "Stage B runner release and BFF gate"
status: pending
priority: P1
dependencies: [4]
effort: "L"
---

# Phase 5: Stage B runner release and BFF gate

## Overview

Fail closed on the exact released Issue #9 runner, then establish the server-only client,
completion repository, evidence service, and crash/reconciliation seams through tests first.
This phase is hard-blocked today and never edits runner/shared-contract source.

## Context Links

- [Gate B](./dependency-and-release-gates.md#gate-b--real-journey-authority)
- [Logical API boundary](./architecture-and-api-boundaries.md#logical-operation-boundary)
- [State authority](./architecture-and-api-boundaries.md#state-and-storage-authority)
- [S3 matrix](./threat-model-and-security.md#stride-and-negative-test-matrix)
- [Runner recovery cases](./verification-evidence-and-uat.md#runner-failure-and-idempotency-cases)

## Requirements

### Functional

- Prove GB-01..GB-05 and exact #8/#9 cross-release compatibility.
- Bind only the released #9 private client/API, registry, problems, idempotency, readiness, and
  verified-artifact interface.
- Implement portal SQLite/reconciliation exactly as the one #8 completion authority specifies.
- Keep all runner credentials/config server-only and all browser calls same-origin.

### Non-functional

- No invented endpoint, command, registry entry, state transition, artifact path, or fallback.
- Unknown/stale/mismatched API/version/status/evidence fails closed.
- Crash, duplicate, response loss, reset/verify conflict, orphan evidence, and restart are
  deterministic and idempotent.
- If host containment/readiness is unavailable, retain Stage A and keep runner disabled.

## Architecture

`released-runner-client.ts` is the only BFF→runner adapter. It consumes the exact #9 released
module or generated client path and authenticates over its private transport. The portal never
implements runner commands. `completion-repository.ts` and `reconciliation.ts` implement the
exact #8 transaction/recovery protocol; `evidence-service.ts` accepts only verified immutable #9
handles and safe #8 evidence metadata.

## Related Code Files

- Modify: `apps/learning-portal/src/server/contracts/release-bindings.generated.ts`
- Create: `apps/learning-portal/src/server/runner/released-runner-client.ts`
- Create: `apps/learning-portal/src/server/state/completion-repository.ts`
- Create: `apps/learning-portal/src/server/state/reconciliation.ts`
- Create: `apps/learning-portal/src/server/evidence/evidence-service.ts`
- Modify: `apps/learning-portal/src/server/config/runtime-config.ts`
- Modify: `apps/learning-portal/src/server/http/bff-router.ts`
- Modify: `apps/learning-portal/src/server/http/http-security.ts`
- Create: `apps/learning-portal/tests/contracts/runner-release-gate.test.ts`
- Create: `apps/learning-portal/tests/contracts/completion-authority.test.ts`
- Create: `apps/learning-portal/tests/security/runner-boundary.test.ts`
- Create: `apps/learning-portal/tests/security/evidence-download.test.ts`
- Create: `apps/learning-portal/tests/unit/reconciliation.test.ts`
- Read only: exact #8/#9 released interfaces and conformance assets
- Delete: none

## Tests Before

1. Add PTP-RED-B-001/010..014 and all Stage B PTP-S3 negatives.
2. Prove current #9 planning/validation heads fail the release gate.
3. Use the released #9 conformance/fault harness—not a fake promotion fixture—to fail
   absent/expired auth, unknown operation, duplicate, response loss, crash, conflict, stale
   result, orphan evidence, digest/handle/type/size mismatch, and containment-not-ready cases.
4. Prove reflection, URL, browser state, baseline fixture, and uncommitted verifier results cannot
   create completion.

## Refactor

Keep one runner client, one completion repository, one reconciliation path, and one evidence
service. Do not wrap released types in a second domain schema or add retry abstraction beyond
released idempotency/recovery semantics.

## Tests After

- GB-01..GB-05 and deterministic release bindings pass.
- Browser bundle/network cannot observe runner transport/credential or arbitrary input.
- Same idempotency key always returns/reconciles one committed result.
- Portal crash/orphan reconciliation cannot grant early or duplicate completion.
- Evidence download requires the exact verified handle/digest/size/media and safe headers.
- Runner unavailable/containment failure falls back to Stage A without mutation.

## Regression Gate

Run focused client/contract/completion/evidence/S3 tests, the exact #9 conformance/security/race
commands named by its release, #8 contract/evidence gates, #6 data-contract gates, app
typecheck/build/audit/bundle scans, and `git diff --check`. Do not yet claim full browser journey.

## Implementation Steps

1. Stop unless a fresh Stage B readiness audit authorizes an exact input containing accepted
   Stage A and the released #9 handoff.
2. Prove GB-01..GB-05, exact #8 compatibility, protected hashes, clean state, and lease ownership.
3. Retain RED failures before creating any runner client or completion store.
4. Bind the exact #9 server client/API/registry/problem/idempotency/evidence interfaces.
5. Add strict BFF mapping, portal session/CSRF, and runner capability/readiness reduction.
6. Implement the exact #8 SQLite completion transaction and startup reconciliation.
7. Implement safe verified-evidence metadata/download service without buffering unbounded bytes.
8. Run conformance/fault/security/refactor/regression checks and emit Gate B evidence.

## Success Criteria

- [ ] Gate B consumes one exact released #9 SHA and records all API/registry/evidence digests.
- [ ] #9 names the exact compatible #8 release and all versions validate.
- [ ] The browser cannot address or authenticate to the runner.
- [ ] One #8 completion authority handles commit/reconciliation; no competing UI state exists.
- [ ] Crash/retry/idempotency/artifact-integrity negatives pass.
- [ ] Unsupported runner containment leaves Stage A usable and Stage B disabled.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| #9 lacks required client/harness/verified handle | STOP and return upstream; no local substitute |
| SQLite driver incompatible with #7 Node | Readiness decision; exact lock; do not switch storage silently |
| BFF becomes generic runner proxy | Closed operation mapping and unknown-operation negative |
| Orphan evidence completes on startup | Exact #8 reconciliation/quarantine tests |

## Security Considerations

Complete PTP-S3-01..14 with the real released transport and conformance seams. Redact bounded
problems/logs; keep runner/session credentials distinct; require same-origin/CSRF on every
mutation; preserve repository/home/network isolation evidence from #9.

## Next Steps

Only after the server boundary is green may Phase 6 connect real learner controls and the exact
journey.
