---
phase: 5
title: "Stage B runner release and BFF gate"
status: pending
priority: P1
dependencies: [4]
effort: "L"
---

# Phase 5: Stage B runner release and BFF gate

> Blocked: Issue #9 is OPEN and unreleased at this correction. Every Issue #9 plan/cook candidate
> is non-release provenance. Stage B path, command, dependency, transport, execution, evidence,
> reset, progress, and completion authorities are all `[]`.

## Overview

Fail closed on the exact released Issue #9 runner, then establish the server-only client,
completion repository, evidence service, and crash/reconciliation seams through tests first.
This phase is hard-blocked today and never edits runner/shared-contract source.

## Context Links

- [Gate B](./dependency-and-release-gates.md#gate-b--real-journey-authority)
- [Stage separation](./architecture-and-api-boundaries.md#stage-separation)
- [Capability boundary](./architecture-and-api-boundaries.md#capability-boundary)
- [S3 matrix](./threat-model-and-security.md#stride-and-negative-test-matrix)
- [Blocked result verification](./verification-evidence-and-uat.md#blocked-fitness-result-v2-verification)

## Requirements

### Functional

- Prove GB-01..GB-05 and exact #8/#9 cross-release compatibility.
- Bind only the released #9 private client/API, registry, problems, idempotency, readiness, and
  verified-artifact interface.
- Implement one server-side completion/reconciliation binding exactly as the released #8
  authority specifies, with no second progress/evidence truth.
- Keep all runner credentials/config server-only and all browser calls same-origin.

### Non-functional

- No invented endpoint, command, registry entry, state transition, artifact path, or fallback.
- No fake execution, synthetic success/evidence, browser-to-host command, browser-to-engine
  authority, raw shell, or local-shell fallback.
- Unknown/stale/mismatched API/version/status/evidence fails closed.
- Crash, duplicate, response loss, reset/verify conflict, orphan evidence, and restart are
  deterministic and idempotent.
- If host containment/readiness is unavailable, retain Stage A and keep runner disabled.

## Architecture

One server-only BFF→runner adapter consumes the exact #9 released module or generated client path
and authenticates over its private transport. The portal never implements runner commands. One
completion/reconciliation binding implements the exact #8 CAS, transaction, idempotency, and
recovery protocol; one evidence boundary accepts only verified immutable #9 handles and safe #8
evidence metadata. Exact modules remain deferred to the later #9 amendment.

## Related Code Files

- Authorized Stage B create/modify/delete paths now: `[]`.
- Authorized Stage B implementation commands now: `[]`.
- Consumable Stage B dependency SHAs now: `[]`.
- A later amendment may authorize only the smallest released-#9 integration subset beneath
  `apps/learning-portal/**` (including portal tests) and the issue fragment after revalidation
  and readiness.

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

1. Stop unless a later amendment pins accepted Stage A, an exact reviewed/merged/pristine #9
   release, and exact Stage B
   file/command allow-lists, then passes fresh independent revalidation and Stage B readiness.
2. Prove GB-01..GB-05, exact #8 compatibility, protected hashes, clean state, and lease ownership.
3. Retain RED failures before creating any runner client or completion binding.
4. Bind the exact #9 server client/API/registry/problem/idempotency/evidence interfaces.
5. Add strict BFF mapping, portal session/CSRF, and runner capability/readiness reduction.
6. Implement the exact released #8 CAS/completion transaction and startup reconciliation once,
   using only the storage binding authorized by the amended release matrix.
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
| Released #8 storage binding incompatible with #7 Node | Readiness decision; exact lock; do not switch storage or duplicate authority silently |
| BFF becomes generic runner proxy | Closed operation mapping and unknown-operation negative |
| Orphan evidence completes on startup | Exact #8 reconciliation/quarantine tests |

## Security Considerations

Complete PTP-S3-01..14 with the real released transport and conformance seams. Redact bounded
problems/logs; keep runner/session credentials distinct; require same-origin/CSRF on every
mutation; preserve repository/home/network isolation evidence from #9.

## Next Steps

Only after the server boundary is green may Phase 6 connect real learner controls and the exact
journey.
