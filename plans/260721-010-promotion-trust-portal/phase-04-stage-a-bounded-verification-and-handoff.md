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

Add the GET/HEAD-only production server, scoped lifecycle, exact Issue #10 Make fragment, one
Chromium desktop+narrow/no-JS journey, bounded visual artifacts, cleanup/rollback, and exact-head
review handoff. Stage A remains explicitly runner-unavailable and non-completing.

## Context Links

- [Exact commands](./verification-evidence-and-uat.md#exact-stage-a-command-contract)
- [Chromium journey](./verification-evidence-and-uat.md#chromium-journey)
- [Security/resource bounds](./threat-model-and-security.md#resource-and-artifact-security)
- [Claim boundary](./dependency-and-release-gates.md#gate-a-claim-boundary)

## Requirements

### Functional

- Serve only bounded built routes/files on `127.0.0.1`, runtime-selected port, GET/HEAD.
- Implement `learn`, status, down, portal test/a11y/e2e/visual targets through the issue fragment.
- Make both Stage B acceptance targets return typed non-zero unavailable without runner action.
- Run fixed 1280x800 and 360x800 Chromium/no-JS/axe journey and bounded visual review.
- Preserve review artifacts while stopping only the owned process, safely twice.

### Non-functional

- Exact wall-time/file/byte/process/request/artifact limits and marker/nonce containment.
- No root Make edit, BFF/API, runner, Docker, cloud, native OS automation, or false approval.
- Two independent implementation reviews and human exact-head approval remain future merge gates.

## Authorized Files

Create only:

```text
apps/learning-portal/playwright.config.mjs
apps/learning-portal/command-owner-activation.stage-a.json
apps/learning-portal/scripts/portal-lifecycle.mjs
apps/learning-portal/scripts/serve-built-portal.mjs
apps/learning-portal/scripts/write-review-artifacts.mjs
apps/learning-portal/tests/e2e/stage-a.spec.mjs
apps/learning-portal/tests/e2e/visual-review.spec.mjs
mk/issue-5/i5-05.mk
```

Across Phases 1–4 the total must equal the amendment's 33 creates, no modifies/deletes.

## Tests Before

1. Retain PTP-RED-A-023/024 through real server/lifecycle/artifact paths.
2. Retain browser RED for desktop/narrow history, no-JS, axe, CSP, network/storage, and unavailable
   states before the harness is green.
3. Assert wrong Host/method/path/body, traversal/ambiguity, output overflow, special file/alias,
   stale/reused PID, foreign path/process, repeated cleanup, and artifact overflow fail closed.
4. Assert Stage B commands cannot pass, skip, import, start, or call a runner.

## Tests After and Regression

- All exact amendment commands have the required Stage A result.
- One-worker/zero-retry Chromium passes both viewports, axe zero Critical/Serious, no-JS parity,
  no unexpected console/CSP/network/storage state.
- Production output and review artifacts meet exact type/count/byte limits.
- Status/down use PID/start identity and marker/nonce; down twice preserves review artifacts.
- Audit has zero High/Critical; protected hashes, command ownership, changed paths, diff hygiene,
  and secret/cloud/runner scans pass.

## Implementation Steps

1. Write server/lifecycle/browser/artifact/cleanup RED cases.
2. Add closed static server and marker/nonce/PID lifecycle.
3. Add frozen Playwright config and one Stage A journey.
4. Add bounded visual artifact writer and unapproved human checklist.
5. Add `mk/issue-5/i5-05.mk` delegates for all nine reserved targets, including Stage B negatives;
   finalize and validate the app-owned activation against the immutable registry and final
   fragment hash.
6. Run exact released validators, frozen install, unit/build, Stage A browser/visual/audit/public
   targets, both Stage B negatives, cleanup twice, and rollback rehearsal.
7. Verify the final diff is exactly 33 creates, protected hashes unchanged, generated state
   untracked/cleaned, and no cloud action.
8. Obtain two fresh exact-head implementation reviews, bounded human UAT, and human exact-head
   approval before any human merge.

## Success Criteria

- [ ] Stage A portal is useful with JS enabled or disabled and runner absent.
- [ ] Exact commands, Chromium/axe, S3, output, audit, cleanup, and rollback gates pass.
- [ ] Claims remain static/read-only, runner unavailable, completion disabled.
- [ ] Final tracked diff is exactly 33 creates and no other product/config/data path.
- [ ] Stage B remains blocked and Issue #10 remains open after any Stage A partial release.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Partial slice mistaken for issue completion | closed claim text, Stage B negative commands, issue stays open |
| Server becomes application API | GET/HEAD closed file map and method negatives |
| Visual gate becomes flaky ceremony | one Chromium, two fixed viewports, bounded named artifacts |
| Cleanup kills foreign PID or evidence | PID/start identity, nonce/marker, path/alias negatives, retain review root |

Rollback removes only the exact 33 Stage A additions at a reviewed Git point; no released or
retained evidence byte is deleted.

## Next Steps

Stage A can be handed to exact-head review. Phase 5 remains blocked until Issue #9 has a released
runner and a new exact Stage B amendment passes readiness.
