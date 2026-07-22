---
phase: 2
title: "Stage A tests-first portal foundations"
status: pending
priority: P1
dependencies: [1]
effort: "M"
---

# Phase 2: Stage A tests-first portal foundations

## Overview

Create the minimal Vietnamese-first React/static shell and strict GET/HEAD-only serving
foundation. The real adapter feeds one safe view model into semantic shell/status components.
There is no BFF/API, runner mock, storage, mutation, or completion path.

## Context Links

- [Architecture](./architecture-and-api-boundaries.md)
- [Threat model](./threat-model-and-security.md)
- [Stage A commands](./stage-a-release-amendment.md#exact-stage-a-command-allowlist)
- [TDD matrix](./verification-evidence-and-uat.md#tests-before-matrix)

## Requirements

### Functional

- Build with the exact frozen #7 Vite/React graph.
- Render semantic catalog/module/lesson placeholders from the validated model, not hard-coded
  contract copies.
- Present Vietnamese-first status and explicit runner-unavailable/completion-disabled language.
- Serve strict production documents over loopback with no API surface.

### Non-functional

- External compiled assets, exact CSP, escaped text, closed Host/method/path behavior.
- No cookies, browser storage, service worker, external network, secrets, source maps, or #9 import.
- One Node process and exact production-output ceilings.

## Authorized Files

Create only:

```text
apps/learning-portal/index.html
apps/learning-portal/vite.config.mjs
apps/learning-portal/src/app/app-shell.jsx
apps/learning-portal/src/app/portal-status.jsx
apps/learning-portal/src/main.jsx
apps/learning-portal/src/styles.css
apps/learning-portal/tests/unit/security.test.mjs
```

## Tests Before

1. Retain PTP-RED-A-010/012/015/016 through the real shell/status render.
2. Retain PTP-RED-A-021/022 for renderer escaping/import/bundle/storage/cloud boundaries.
3. Retain applicable PTP-RED-S3-01..14 negatives before enabling serving.
4. Prove missing shell semantics and unsafe mutations fail for the intended reason.

## Tests After and Regression

- Frozen production build succeeds with no source maps and bounded regular output.
- Semantic shell/status is useful in Vietnamese and distinguishes canonical English values.
- Exact static headers/CSP, Host, methods, paths, XSS, storage, network, secret, cloud, and #9
  absence tests pass.
- Missing runner never blocks render and never becomes the controlled failure.
- Unit/contract/security/build/audit/diff gates stay within exact time/output bounds.

## Implementation Steps

1. Write shell/status/security RED assertions against the real entry/render path.
2. Add the minimal Vite entry/config from the released toolchain, without spike product code.
3. Build semantic app shell and status from the safe model.
4. Add external styles for focus, logical order, narrow reflow, reduced motion, and no color-only
   state.
5. Add strict production build and security constraints.
6. Run GREEN/refactor/regression and confirm only these seven paths are added.

## Success Criteria

- [ ] Exact Vite graph builds reproducibly.
- [ ] Vietnamese-first shell and runner-unavailable state render from validated data.
- [ ] Stage A exposes no BFF/API/runner/mutation/storage/completion capability.
- [ ] CSP/XSS/Host/path/bundle/storage/cloud security foundation is green.
- [ ] Only the seven authorized files are added.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Spike code leaks into product | Build purpose-built files; import/bundle scan |
| Static server evolves into BFF | GET/HEAD closed map only; method/API negatives |
| CSP relaxed for Vite | Test built output with exact CSP and external assets |
| Unavailable becomes lesson result | Distinct typed copy and contract assertions |

Rollback removes only these seven unmerged additions.

## Next Steps

Phase 3 adds reusable navigation and the promotion-trust vertical slice.
