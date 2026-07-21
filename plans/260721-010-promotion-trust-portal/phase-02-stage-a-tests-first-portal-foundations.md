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

Promote the exact merged Vite/React foundation and establish portal-only client/BFF/security
seams through failing tests first. The result is a buildable Stage A foundation with validated
Issue #8 content and a hard-coded capability outcome of runner unavailable—not a runner mock or
completion path.

## Context Links

- [Plan](./plan.md)
- [Architecture](./architecture-and-api-boundaries.md)
- [Threat model](./threat-model-and-security.md)
- [Tests-before matrix](./verification-evidence-and-uat.md#tests-before-matrix)

## Requirements

### Functional

- Build the exact Vite/React shell and Node BFF from the #7 release.
- Load Issue #8 released lesson data into one closed safe view model.
- Provide semantic status/error/live-region components and explicit unavailable/offline states.
- Enforce Stage A non-completion at UI, API, and storage boundaries.

### Non-functional

- Same-origin, loopback-only BFF with strict production CSP and no CORS.
- No browser storage authority, runner client, runner endpoint, or completion database mutation.
- Frozen lock install/build and 16 GiB-friendly single portal process.

## Architecture

The BFF serves built/static assets and only the exact read operations from the #8 release. Its
released Stage A capability reports runner unavailable and contains no runner configuration.
Client state is presentation-only. Security filtering runs before BFF routing and rejects
unknown host, origin, content type, method, version, and body.

## Related Code Files

- Authorized Stage A create/modify/delete paths now: `[]`.
- Authorized Stage A implementation commands now: `[]`.
- Consumable Stage A dependency SHAs now: `[]`.
- A later amendment may authorize only the smallest #7/#8-derived subset beneath
  `apps/learning-portal/**` (including portal tests) and `mk/issue-5/i5-05.mk` after revalidation
  and readiness.

## Tests Before

1. Add PTP-RED-A-010/011/012/015/016 component and state assertions using only released content.
2. Add PTP-RED-S3-01..06 and 08..11/13/14 at the portal boundary.
3. Prove the route shell initially lacks the required question/grain/unavailable semantics.
4. Prove any completion mutation, runner configuration, unsafe content, wrong version, foreign
   Host/Origin, missing CSRF on a mutation-shaped request, or browser storage authority fails.

## Refactor

Share one safe view-model mapper between client/static/BFF. Keep presentation components local.
Do not generalize a design system, state framework, API proxy, service worker, or plugin system.

## Tests After

- Frozen `npm ci` and production build pass with the exact released toolchain.
- Safe view model rejects unknown/unreleased fields and attribution language.
- Stage A has no mutation route, completion write, runner import, or browser-direct privileged
  capability.
- The production/browser bundle and static startup contain no eager Stage B runner or optional-tool
  import; missing optional capabilities cannot break Stage A.
- Security headers and same-origin negative cases pass.
- Component semantics, focus, live regions, narrow layout primitives, and reduced motion pass.

## Regression Gate

Run focused locked unit/contract/security/accessibility tests, typecheck, production build,
`npm audit --audit-level=high`, bundle scan, and `git diff --check`. Record exact results without
calling Stage B targets.

## Implementation Steps

1. Stop until the later amendment pins real dependencies and exact Stage A paths/commands, then
   retain the failing tests and exact dependency/input identities.
2. Promote the minimal accepted #7 Vite files inside the authorized portal subset; remove all loser
   candidate code and unneeded score/timer machinery from the product copy.
3. Add released #8 content loader and safe shared view model; do not copy shared schemas.
4. Build the loopback BFF with strict headers and exact released read-only operations within the
   amended allow-list.
5. Build the semantic application/status/error skeleton with Stage A banner and no completion.
6. Add closed runtime mode, offline detection, focus/live-region primitives, and safe errors.
7. Run focused green/refactor/regression checks and preserve evidence.

## Success Criteria

- [ ] Exact Vite foundation installs/builds reproducibly from the tracked lock.
- [ ] Stage A loads only exact #8 released content and exact Issue #6 fixture identity.
- [ ] Runner is explicitly unavailable and impossible to configure/call from Stage A.
- [ ] No client or BFF action can claim or persist completion.
- [ ] PTP-S3 and accessibility foundation tests pass with no High/Critical package finding.

## Risk Assessment

| Risk | Mitigation |
|---|---|
| Vite spike code imports provisional fixture/score logic | Promote only handoff path map; scan bundles/import graph |
| BFF grows into a second framework | Node/Vite boundary only; no broker/plugin/proxy abstraction |
| CSP relaxed for development | Test built release with exact strict header; no unsafe directives |
| “Unavailable” treated as controlled failure | Separate released environmental problem state and language |

## Security Considerations

Implement the HTTP/XSS/storage controls in the S3 contract before adding any interactive
mutation. The portal session is distinct from the runner credential; Stage A never receives the
latter.

## Next Steps

Phase 3 adds read-only lesson navigation and the deterministic static/no-JavaScript document.
