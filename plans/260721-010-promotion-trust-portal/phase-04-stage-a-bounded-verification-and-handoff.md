---
phase: 4
title: "Stage A bounded verification and handoff"
status: pending
priority: P1
dependencies: [3]
effort: "M"
---

# Phase 4: Stage A bounded verification and handoff

## Overview

Prove and package the independently useful Stage A shell without overstating it. Run the focused
Vite/unit/contract/security/accessibility/Chromium/no-JavaScript/build gates, create bounded
visual/UAT artifacts, add only the I5-05 Make fragment, and preserve an explicit non-completion
handoff for later Stage B.

## Context Links

- [Exact command contract](./verification-evidence-and-uat.md#exact-issue-command-contract)
- [Visual review](./verification-evidence-and-uat.md#deterministic-portal-visual-review)
- [Stage A claim boundary](./dependency-and-release-gates.md#gate-a-claim-boundary)
- [Retention and rollback](./threat-model-and-security.md#retention-cleanup-and-rollback)

## Requirements

### Functional

- Make portal test/a11y/static/start/status/down functions discoverable from
  `mk/issue-5/i5-05.mk` without root Make edits.
- Run one locked Chromium smoke at desktop/narrow for Stage A states.
- Produce deterministic visual artifacts/checklist and no-JS/static equivalence evidence.
- Hand off exact Stage A head/dependencies/digests/results with `runner: unavailable` and
  `completion: disabled`.

### Non-functional

- No runner API import, real-lab claim, optional tool, Docker, cloud, or native OS automation.
- Required failure is non-zero and schema-valid after safe evidence-root allocation.
- Cleanup/status affect only the single portal process and preserve evidence.
- Human exact-head review remains separate.

## Architecture

Stage A lifecycle starts only the portal/BFF in `stage-a-static` mode. The Make fragment delegates
to locked app scripts and emits evidence below the registered local-journey root with stage and
claim fields. The visual target is deterministic capture + checklist generation; it never marks
the checklist approved.

## Related Code Files

- Create/promote: `apps/learning-portal/playwright.config.ts`
- Create: `apps/learning-portal/tests/e2e/promotion-trust-static.spec.ts`
- Create: `apps/learning-portal/tests/e2e/no-js-static-fallback.spec.ts`
- Create: `apps/learning-portal/tests/e2e/runner-unavailable.spec.ts`
- Create: `apps/learning-portal/tests/visual/portal-visual-review.spec.ts`
- Create: `apps/learning-portal/tests/security/bundle-and-private-path.test.ts`
- Create: `apps/learning-portal/scripts/portal-lifecycle.mjs`
- Create: `mk/issue-5/i5-05.mk`
- Delete: none

## Tests Before

1. Add failures for missing exact target mapping, wrong stage claim, runner import/config,
   completion capability, unbounded capture, missing evidence fields, unsafe PID cleanup, and
   omitted Stage A limitation.
2. Capture failing Chromium/no-JS/axe/visual assertions before implementing the harness.
3. Assert the full Issue #10 journey targets cannot pass/claim Stage B in static mode.

## Refactor

Keep lifecycle/evidence helpers issue-local. Reuse the accepted #7 Playwright harness and #8
FitnessResult writer if released. Do not create a second command registry or generalized root
Make integration.

## Tests After

- `portal-test` and `portal-a11y` runner-independent subsets pass if Stage A readiness authorizes
  those exact targets.
- Locked Chromium desktop/narrow and JavaScript-disabled/static tests pass.
- Visual artifact list is fixed, complete, hashed, and accompanied by an unapproved UAT checklist.
- Status/down correctly report/stop one portal process and preserve evidence.
- Full journey/completion targets remain blocked with an explicit Stage B dependency result.

## Regression Gate

Run frozen install/build, focused tests, one Chromium smoke, axe Critical/Serious gate, no-JS
browser/parser, deterministic render comparison, high-confidence scans, dependency audit,
`git diff --check`, exact changed-path/protected-hash checks, and cleanup twice.

## Implementation Steps

1. Retain RED IDs for command/claim/evidence/cleanup failures.
2. Add Stage A lifecycle and exact I5-05 Make fragment delegates without root Make edits.
3. Configure the one locked Chromium desktop+narrow smoke and no-JS context.
4. Implement deterministic bounded visual capture/manifest/checklist.
5. Emit closed FitnessResult/dependency/evidence manifests with explicit non-completion fields.
6. Rehearse status/down/cleanup, stale PID, foreign process/path, and rollback to static build.
7. Run Stage A regression checks at an exact clean head.
8. Obtain independent review and human exact-head pre-merge approval only if a fresh readiness
   phase authorizes a Stage A PR; this plan itself authorizes neither.

## Success Criteria

- [ ] Stage A static shell has complete focused evidence and deterministic artifacts.
- [ ] All claims say runner unavailable and completion disabled.
- [ ] The exact #7/#8 release/input identities and Issue #6 hashes are retained.
- [ ] No Stage B command/result is falsely passed or skipped.
- [ ] Lifecycle/cleanup is idempotent, scoped, and evidence-preserving.
- [ ] Any future Stage A merge remains an open Issue #10 partial delivery.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Partial stage mistaken for issue completion | Closed claim fields, issue remains OPEN, full targets blocked |
| Visual target becomes flaky OS automation | Locked Chromium, fixed viewports/state list, artifact-only checklist |
| Root Make ownership violated | I5-05 fragment only; pre/post root hash |
| Cleanup kills reused/foreign PID | PID + start identity + namespace marker negative tests |

## Security Considerations

Run the full Stage A-applicable S3 matrix, bundle scan, dependency audit, Host/Origin/CSP/XSS
tests, credential/private-path scan, and protected hash checks. No browser session grants runner
capability.

## Next Steps

Wait for Gate B. Stage A may remain deployed as the safe fallback indefinitely.
