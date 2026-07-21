---
phase: 7
title: "Stage B evidence release rollback and approval"
status: pending
priority: P1
dependencies: [6]
effort: "L"
---

# Phase 7: Stage B evidence release rollback and approval

## Overview

Converge the full vertical slice at one exact head: implement final lifecycle/Make delegates,
run every Issue #10 command unchanged, capture bounded evidence/visual/UAT artifacts, rehearse
cleanup/rollback, preserve retention, and require independent review plus human exact-head
pre-merge approval. No PR/merge is implied by this plan.

## Context Links

- [Exact commands and acceptance](./verification-evidence-and-uat.md#exact-issue-command-contract)
- [Visual/UAT contract](./verification-evidence-and-uat.md#deterministic-portal-visual-review)
- [Release gate](./verification-evidence-and-uat.md#release-gate)
- [Threat retention/rollback](./threat-model-and-security.md#retention-cleanup-and-rollback)
- [Hard STOP conditions](./requirements-and-risk-traceability.md#hard-stop-conditions)

## Requirements

### Functional

- Provide exact `learn`, `learn-status`, `learn-down`, `portal-test`, `portal-a11y`,
  `portal-e2e`, `lesson-e2e`, `local-journey-e2e`, and `portal-visual-review` targets through the
  I5-05 Make fragment.
- Run the exact Issue #10 Verify block and complete one fresh real local journey.
- Capture dependency/input/tested-tree/evidence/cleanup/rollback and bounded visual artifacts.
- Preserve prior evidence and prove idempotent teardown/rollback/static fallback.

### Non-functional

- Required missing tool/evidence is fail; no skipped required gate.
- One Chromium desktop+narrow and axe Critical/Serious only; no broad native/browser matrix.
- No cloud/AWS/Terraform/Docker/optional-profile action.
- Exact-head human approval is separate, mandatory, and cannot be synthesized.

## Architecture

`portal-lifecycle.mjs` owns only the portal process record and delegates runner lifecycle through
the exact #9 API/launcher contract. `i5-05.mk` is a thin command registry fragment. All results
write atomically under one run root and refer to artifacts by relative locator/hash. Status/down
validate PID start identity/process group/namespace; rollback disables Stage B and verifies the
Stage A static route before any code rollback.

## Related Code Files

- Modify: `apps/learning-portal/scripts/portal-lifecycle.mjs`
- Create/modify: `apps/learning-portal/tests/e2e/promotion-trust-real-journey.spec.ts`
- Create/modify: `apps/learning-portal/tests/e2e/runner-crash-retry.spec.ts`
- Create/modify: `apps/learning-portal/tests/e2e/reset-idempotency.spec.ts`
- Create/modify: `apps/learning-portal/tests/e2e/evidence-integrity.spec.ts`
- Modify: `apps/learning-portal/tests/visual/portal-visual-review.spec.ts`
- Create: `apps/learning-portal/tests/e2e/lifecycle-cleanup.spec.ts`
- Create: `apps/learning-portal/tests/e2e/rollback-static-fallback.spec.ts`
- Modify: `apps/learning-portal/playwright.config.ts`
- Modify: `mk/issue-5/i5-05.mk`
- Runtime only, untracked: `.artifacts/evidence/local-journey/{run-id}/**`
- Delete: none

## Tests Before

1. Add failing exact-target/command/delegate/evidence-schema tests before final Make/lifecycle
   changes.
2. Add PTP-RED-B-016 plus stale/reused PID, foreign process, symlinked root, active operation,
   duplicate down, retained evidence, and static rollback failures.
3. Add missing artifact/trace/axe/digest/dependency/human-approval metadata negatives.
4. Prove the visual target cannot auto-approve its UAT checklist.

## Refactor

Keep Make recipes thin, non-interactive, and deterministic. Share run-root allocation, atomic
result writing, and scoped process identity only inside the app. Do not add root scripts,
repository-wide cleanup, CI, release automation, native OS driver, or generic process manager.

## Tests After

- Every exact target delegates correctly and produces schema-valid success/failure evidence.
- Full clean real journey passes in one locked Chromium at both fixed viewports.
- Axe reports zero Critical/Serious; no-JS/static and runner-unavailable paths pass.
- Crash/retry/idempotency/reset/evidence-download/lifecycle tests pass.
- Visual manifest/artifacts/checklist are complete and bounded; manual result remains external.
- Status/down twice, rollback rehearsal, protected hashes, evidence retention, and clean tree pass.

## Regression Gate

Execute exactly:

```bash
make portal-test portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
make learn-status
make learn-down
```

Also run `make learn LESSON=promotion-trust` for lifecycle acceptance, exact #6/#8/#9
contract/security/race blast-radius commands named by their released handoffs, frozen install/
build/audit, changed/protected/credential/private-path/bundle scans, `git diff --check`, and final
clean/local=tracking=fresh-live checks.

## Implementation Steps

1. Retain failing lifecycle/command/evidence/cleanup/rollback assertions at the exact head.
2. Complete thin I5-05 Make delegates and scoped portal/runner lifecycle orchestration.
3. Start from a clean namespace with Docker unavailable and no cloud/model credentials.
4. Run the exact real journey, fault/retry/idempotency, accessibility, no-JS, and download checks.
5. Generate deterministic visual artifacts and the bounded unapproved UAT checklist.
6. Run `learn-status`, `learn-down` twice, stale/foreign PID negatives, evidence retention, and
   static-fallback rollback rehearsal.
7. Run full exact commands/blast radius/S3/audit/protected-path checks and capture the closed
   FitnessResult/artifact graph.
8. Obtain fresh independent exact-head code/security/accessibility review with zero unresolved
   Critical/High findings.
9. Obtain named human exact-head pre-merge approval; any later head change invalidates it.
10. Only a separately authorized Git workflow may create/merge a PR; this phase stops at evidence
    and approval readiness if no such authority exists.

## Success Criteria

- [ ] Every exact Issue #10 Verify command passes at one exact clean head.
- [ ] Complete Docker-free, credential-free local journey evidence is retained.
- [ ] One #8 completion authority and private #9 runner boundary remain intact.
- [ ] S3, accessibility, Chromium desktop/narrow, axe, no-JS/static, failure/recovery, and
  evidence-integrity gates pass.
- [ ] Visual/UAT artifact is bounded and does not claim automated conformance/human approval.
- [ ] Teardown/cleanup/rollback is scoped, idempotent, evidence-preserving, and leaves a clean tree.
- [ ] Human exact-head pre-merge approval is recorded before any merge.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Aggregate target hides failing child | Each child writes/returns required status; aggregate fails closed |
| Evidence contains recursive commit claim | Separate tested tree, later attestation, external merge identity |
| Cleanup/rollback harms unrelated state | Namespace/PID/marker/symlink checks and deny-list |
| UAT artifact mistaken for approval | Deterministic hash excludes reviewer fields; explicit external sign-off |
| Head changes after review | Approval binds full 40-hex; rerun review/approval on any change |

## Security Considerations

Re-run all PTP-S3 tests with real release mode, dependency/bundle/scanner checks, output canaries,
browser-direct runner denial, and artifact integrity. Validate no tracked/staged `.artifacts`,
private data, cloud credentials, source maps with secrets, or absolute local paths.

## Next Steps

After the plan itself receives fresh independent validation and readiness, staged cook may begin
only when its dependency gate clears. After implementation evidence/human approval, a separate
authorized Git phase decides PR/merge. Issue #10 closes only after Stage B merges and post-merge
verification passes.
