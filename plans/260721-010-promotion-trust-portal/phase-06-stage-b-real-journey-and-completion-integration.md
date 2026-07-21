---
phase: 6
title: "Stage B real journey and completion integration"
status: pending
priority: P1
dependencies: [5]
effort: "L"
---

# Phase 6: Stage B real journey and completion integration

## Overview

Connect the Stage A lesson shell to the real released runner and complete the exact learner path:
business question → grain-honest four-mart context → controlled failure → canonical decision →
reset → fresh verified evidence → one completion transaction. Use real Issue #6 data truth and
released #8/#9 interfaces; no fake/ignored fixture or browser-direct privilege.

## Context Links

- [Exact journey data flow](./architecture-and-api-boundaries.md#exact-journey-data-flow)
- [Routing/history/reset](./architecture-and-api-boundaries.md#routing-history-and-reset)
- [Evidence display/download](./architecture-and-api-boundaries.md#evidence-display-and-download)
- [Requirements](./requirements-and-risk-traceability.md#requirement-catalogue)
- [Recovery cases](./verification-evidence-and-uat.md#runner-failure-and-idempotency-cases)

## Requirements

### Functional

- Execute the released controlled-failure operation and show its exact evidence/remediation.
- Present four marts without causal join and record only
  `insufficient-evidence / no-common-grain`.
- Reset idempotently, preserve prior evidence, and prove fresh ready/base/golden state.
- Execute the released verify operation and validate the fresh committed result/evidence.
- Commit completion exactly once through Issue #8 and expose safe evidence metadata/download.
- Recover honestly from runner unavailable/crash/retry/reload/response loss/conflict.

### Non-functional

- Keyboard, desktop/narrow, reduced-motion/static, and status/live-region paths remain complete.
- Browser history never replays a mutation and browser storage is not authoritative.
- Core path uses no Docker/optional service/cloud credential and stays within the local process
  shape.
- Evidence/local hashes are described as corruption detection only.

## Architecture

Interactive components submit only released logical actions to the same-origin BFF. The BFF
maps them to exact #9 registry operations, polls/reconciles using released semantics, validates
evidence, and commits completion through #8. Client route state remains presentation-only. Static
fallback and explicit unavailable mode remain deployable when execution is disabled.

## Related Code Files

- Modify: `apps/learning-portal/src/client/app/portal-app.tsx`
- Modify: `apps/learning-portal/src/client/app/portal-router.ts`
- Modify: `apps/learning-portal/src/client/features/promotion-trust/controlled-failure.tsx`
- Modify: `apps/learning-portal/src/client/features/promotion-trust/decision-panel.tsx`
- Modify: `apps/learning-portal/src/client/features/promotion-trust/reset-panel.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/verified-evidence.tsx`
- Create: `apps/learning-portal/src/client/features/promotion-trust/evidence-download.tsx`
- Modify: `apps/learning-portal/src/server/http/bff-router.ts`
- Modify: `apps/learning-portal/src/server/state/reconciliation.ts`
- Modify: `apps/learning-portal/src/server/evidence/evidence-service.ts`
- Create: `apps/learning-portal/tests/e2e/promotion-trust-real-journey.spec.ts`
- Create: `apps/learning-portal/tests/e2e/runner-crash-retry.spec.ts`
- Create: `apps/learning-portal/tests/e2e/reset-idempotency.spec.ts`
- Create: `apps/learning-portal/tests/e2e/evidence-integrity.spec.ts`
- Modify: focused unit/contract/accessibility/security tests under `apps/learning-portal/tests/**`
- Delete: none

## Tests Before

1. Add PTP-RED-B-015 and real journey assertions before enabling controls.
2. Start from one fresh namespaced real runner workspace and prove the shell cannot yet execute.
3. Add negatives for false attribution, wrong decision, environment failure mislabeled controlled,
   stale/baseline evidence completion, missing reset oracle, duplicate operations, crash/reload,
   response loss, corrupt download, and reflection/URL/browser-state completion.
4. Retain exact input/#7/#8/#9/fixture/registry/verifier hashes with the RED results.

## Refactor

Keep UI steps thin and driven by canonical server state. Reuse released problem/remediation and
state IDs. Avoid a client workflow engine, optimistic completion, generic action dispatcher, or
portal copy of runner logic.

## Tests After

- Real runner produces the expected controlled failure; environmental failures use a distinct
  state and do not advance progress.
- Four grains/limitations and exact canonical decision remain visible throughout.
- Reset/retry is idempotent, returns fresh ready, preserves prior evidence, and proves base hashes.
- Fresh verifier/evidence predicates pass and one completion record commits.
- Evidence display/download bytes, size, media type, digest, schema, release SHAs, and redaction
  metadata match.
- Back/reload/reverse navigation recovers canonical state without duplicate mutation.
- Keyboard/focus/live-region/narrow/reduced-motion/static fallback remain green.

## Regression Gate

Run focused unit/contract/S3/a11y suites, the released #9 real conformance/fault tests, and one
locked Chromium real-journey smoke at desktop/narrow. Include #6/#8 contract regression and
evidence download digest. The final exact Make aggregate remains Phase 7.

## Implementation Steps

1. Allocate a clean namespaced real workspace and retain failing full-journey evidence.
2. Enable the released start/operation controls through the same-origin BFF only.
3. Render real controlled-failure evidence and distinct environmental error/remediation states.
4. Record the exact released decision through canonical #8 state, never client inference.
5. Implement reset UI/BFF flow with stable idempotency key and reconciliation after loss/reload.
6. Execute fresh verify, validate all evidence/contract/fixture/verifier/dependency identities,
   and commit through the one #8 completion transaction.
7. Render safe evidence metadata/download and honest local-integrity language.
8. Inject runner crash/retry/conflict/artifact faults and make the smallest fixes.
9. Re-run full focused browser/accessibility/security/contract regression.

## Success Criteria

- [ ] One real clean local journey reaches the exact canonical decision, reset, verify, evidence,
  and one completion.
- [ ] No fake/ignored fixture, causal join, browser authority, arbitrary runner input, or optional
  service is used.
- [ ] Runner unavailable/crash/retry/idempotency/reload/conflict cases recover without false
  progress or evidence loss.
- [ ] Download bytes and displayed integrity metadata match canonical evidence.
- [ ] Stage A static fallback remains usable when Stage B is disabled.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| UI state races runner state | Canonical server reads; no optimistic completion; released journal |
| Reset reuses failed workspace | Exact fresh-ready oracle and base/fixture hash proof |
| Controlled failure copy masks infrastructure error | Separate released problem classes/live regions |
| Evidence table overwhelms browser | Safe summary + bounded/lazy details + attachment streaming |

## Security Considerations

Run real browser-direct runner denial, CSRF/Origin/Host, injection, artifact traversal/type,
output-redaction, credential/private-path, restart/replay, and completion-tamper tests. Never
include raw logs/env/paths or inline artifact HTML.

## Next Steps

Phase 7 runs exact Issue #10 commands, release evidence, cleanup/rollback, bounded UAT, and human
approval gates.
