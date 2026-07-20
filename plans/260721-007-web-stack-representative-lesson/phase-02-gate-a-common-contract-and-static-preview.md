---
phase: 2
title: "Gate A Common Contract and Static Preview"
status: pending
priority: P1
dependencies: [1]
effort: "3 active hours maximum"
barrier: authorized-after-gate-0-by-fresh-readiness-audit
---

# Phase 2: Gate A Common Contract and Static Preview

## Context Links

- [Preview journey contract](./preview-journey-contract.md)
- [Acceptance and test matrix](./acceptance-and-test-matrix.md)
- [Candidate protocol](./candidate-protocol.md)
- [Security S3 disposition](./security-s3-disposition.md)

## Overview

Within three active hours, create one narrow logical contract/test harness and the retained
framework-neutral static preview. This is the first runnable artifact and survives every
candidate/no-winner outcome. It uses a deterministic, safe synthetic fixture only and never
claims completion, release, runner verification, or decision evidence.

## Requirements

- Share only `LessonManifestView`, `MartEvidenceView`, `JourneyStateView`, `LabClient`,
  `EvidenceIndexView`, `CandidateEvidenceRecord`, failure codes, and shared test semantics.
- Do not share component APIs, rendering primitives, layout, routing, state library, framework
  lifecycle, or styling implementation.
- Implement the ten acts, three unscored prerequisite probes, orient/connect/explain hints,
  controlled/environmental/unexpected failure separation, explicit reset, fixture-only verify,
  evidence review/export, and reflection.
- Use exactly four separate grain-honest cards. The expected conclusion is
  `insufficient evidence`; no relationship in data, DOM, copy, diagram, state, or evidence may
  attribute fulfillment, return, or global DQ facts to a promotion.
- Put `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` at entry, state rail, verify/evidence,
  and export. The state vocabulary must not contain `completed`.
- Explicit controls commit navigation. Scroll, motion, hover, elapsed time, card visitation,
  reflection, and JavaScript alone never commit or verify.
- Semantic HTML is the source. With JavaScript disabled, facts, limitations, labels, evidence,
  failure distinctions, and a linear previous/next review remain understandable. Reduced motion
  removes only animation.
- Use project-owned prose, diagrams, styles, spacing, timing, and source. Record principle-level
  inspiration in a non-copy inventory.
- No network authority beyond same-origin static assets; no credentials, runner URL, private API,
  mutation, cloud endpoint, service worker, runtime MDX, or unsafe HTML.

## Architecture

Semantic static HTML is the authoritative view. Plain logical JSON/state vectors and dependency-
light tests sit beside it. Optional JavaScript progressively enhances explicit navigation/reset/
verify/evidence; it never owns facts or authority. A small common static host manages loopback
readiness/lifecycle/CSP only and renders no framework route.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `spikes/web/common/contracts/*.json` | 150-250 lines | Valid/invalid logical fixtures |
| Create | `spikes/web/common/fixtures/synthetic-promotion-trust-v1.json` | small, deterministic | Safe preview input only |
| Create | `spikes/web/common/state/preview-state.mjs` and `*.json` | 120-220 lines | Pure transition/reset reducer and vectors |
| Create | `spikes/web/common/tests/*.test.mjs` | 300-500 lines | Shared WEB contract/state/trust/security tests |
| Create | `spikes/web/preview/index.html` | 250-400 lines | Semantic ten-act/static route |
| Create | `spikes/web/preview/preview.css` | 150-250 lines | Reflow/reduced-motion/focus |
| Create | `spikes/web/preview/preview.mjs` | 150-250 lines | Optional progressive/reversible enhancement |
| Create | `spikes/web/harness/scripts/static-host.mjs` | small | Loopback/status/shutdown/CSP for preview and static candidates |
| Create | `spikes/web/harness/scripts/preview-control.mjs` | small | Scoped PID/port/start/status/reset-check/down |
| Create | `spikes/web/non-copy-inventory.md` | concise | Source/reviewer gate |
| Modify | `mk/issue-5/i5-02.mk` | small | Preview/common direct targets |

The no-build fallback is `python3 -m http.server` against `spikes/web/preview`; it is a review
fallback only. The planned issue-local target uses the dependency-free Node static host so it can
emit readiness/CSP/status and stop only its recorded process.

The Node host hardcodes the real preview root and serves only `/`, `/index.html`, `/preview.css`,
`/preview.mjs`, and `/__i5_02_ready`. It rejects directory listings, dotfiles, symlinks, traversal,
unknown routes, wildcard binds/CORS, and any resolved path outside that root. Responses use a
strict self-only CSP with `default-src 'none'`, no connect/object/worker/manifest/font authority,
and no inline/eval/data script authority.

## Related Code Files

- Create only the Gate A `spikes/web/common/**`, `spikes/web/preview/**`, harness, non-copy, and
  issue-local Make entries listed above.
- Consume Gate 0 registries read-only.
- Delete nothing.

## Dependency Map

```text
Gate 0 freeze
  -> common logical shapes + failing shared WEB tests
  -> safe synthetic fixture + semantic static document
  -> optional reversible enhancement + loopback lifecycle
  -> candidate phases 3/4/5
```

Issue #6 is intentionally not a dependency for Gate A. Synthetic output is structurally unable to
enter scorecard/ADR evidence.

## Interface Checklist

- [ ] Fixture kind/digest binds state and evidence; a digest change clears persisted state.
- [ ] Allowed preview states omit `completed` and use explicit committed/transient fields.
- [ ] Reset is idempotent for resettable lesson state, returns the same baseline digest, and its
      separate visible audit counter increments exactly once per explicit invocation.
- [ ] Default port is `4173`; an explicit `PREVIEW_PORT` may choose one other loopback port, but an
      occupied/invalid port fails rather than silently selecting another. Readiness times out after
      10 seconds, terminates only the just-started owned process, and records the failure.
- [ ] Runtime locator is exactly `.artifacts/runtime/i5-02/learn-preview/<port>.json` and records
      PID, process group, process-start fingerprint, command hash, cwd, real preview root, host,
      port, run ID, fixture digest, and implementation input. Status/down signal nothing unless all
      identity fields and the readiness run ID match.
- [ ] Verify checks only the fixture projection and displays the non-completing label.
- [ ] Export is sanitized, relative-path-only, synthetic-labelled, and unscored.
- [ ] Failure code, learner copy, recovery, progression, and evidence differ by class.
- [ ] Static and enhanced paths expose the same facts and limitations.
- [ ] Four-card invariant is covered by `WEB-CONTRACT-002/003` and `WEB-TRUST-001/002`.

## Test Scenario Matrix

| Priority | Scenario | Shared IDs |
|---|---|---|
| Critical | Synthetic preview cannot complete or reach privilege | `WEB-PREVIEW-001/002`, `WEB-API-001` |
| Critical | Four grains remain separate; insufficient result | `WEB-CONTRACT-002/003`, `WEB-TRUST-001/002` |
| Critical | Hostile fixture text is data/rejected, never executable | `WEB-CONTRACT-001`, `WEB-API-001` |
| High | Back/forward/reload/transient/reset | `WEB-STATE-001/002`, `WEB-NOSCROLL-001` |
| High | Controlled vs environmental vs unexpected | `WEB-FAIL-001` |
| High | Keyboard/semantics/reflow/reduced motion/static | `WEB-A11Y-001..004`, `WEB-STATIC-001` |
| High | Full deterministic journey and non-copy | `WEB-E2E-001`, `WEB-NONCOPY-001` |

## Implementation Steps

1. Write common logical failure fixtures and shared WEB tests.
2. Implement the pure dependency-free state reducer and deterministic vectors.
3. Implement semantic static acts/cards/labels/fallback navigation.
4. Add accessible styling/reflow/reduced-motion behavior.
5. Add the smallest reversible enhancement, then the exact-route static host and owned lifecycle
   controller; run evidence gates.

## Tests Before

1. Write valid/invalid logical fixtures and the shared tests named above before preview HTML/JS.
2. Confirm the missing preview fails each applicable test for the intended reason; retain the
   failure list and input SHA in Gate A evidence.
3. Add negative fixtures containing script/JSX-like strings, unsafe URLs, unknown fields,
   cross-grain relationship fields, fake `completed`, old fixture digests, and secret canaries.

## Refactor

Implement semantic HTML first, then CSS/reduced-motion/reflow, then the smallest optional script
for explicit controls/history/reset/verify/evidence. The script derives no trusted completion or
score. Keep the shared contract plain data and test semantics rather than a rendering framework.

## Tests After

- Run all shared non-browser tests against the static preview.
- Run parser/static checks proving every fact/label/card/limitation exists before JavaScript.
- Record static/logical checks for landmark/heading/control structure, no-JS content, native
  keyboard baseline, CSS 200% reflow rules, and reduced-motion rules as Gate A results. Actual
  browser navigation, keyboard use, named screen-reader use, 200% rendering, reduced-motion
  rendering, and no-JS manual comprehension remain `required-pending` Gate C evidence. They cannot
  be reported as passed by source inspection.
- Inspect bundle/source/network allow-list and non-copy inventory.

## Regression Gate

Planned future commands:

```bash
node --test spikes/web/common/tests/*.test.mjs
node --test spikes/web/harness/tests/preview-control.test.mjs
make -f mk/issue-5/i5-02.mk web-common-test IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
node spikes/web/harness/scripts/preview-control.mjs start --lesson promotion-trust --port 4174 --implementation-input <full-40-hex-authorized-sha>
node spikes/web/harness/scripts/preview-control.mjs status --port 4174 --implementation-input <full-40-hex-authorized-sha>
node spikes/web/harness/scripts/preview-control.mjs reset-check --lesson promotion-trust --implementation-input <full-40-hex-authorized-sha>
node spikes/web/harness/scripts/preview-control.mjs down --port 4174 --implementation-input <full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk learn-preview LESSON=promotion-trust PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk learn-preview-status PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk learn-preview-reset-check LESSON=promotion-trust IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
make -f mk/issue-5/i5-02.mk learn-preview-down PREVIEW_PORT=4174 IMPLEMENTATION_INPUT_SHA=<full-40-hex-authorized-sha>
python3 -m http.server 4174 --bind 127.0.0.1 --directory spikes/web/preview
```

Port `4174` is the documented audit-time verification port; it is not auto-selected and the cook
must stop if it is occupied. `web-common-test` emits
`.artifacts/evidence/web-spike/<run-id>/gate-a/common-tests.json` and exits
non-zero for any applicable WEB failure. `learn-preview` prints the loopback URL, PID locator,
fixture digest, label, evidence root, fixed port, and 10-second readiness deadline; it binds only
`127.0.0.1` and exits non-zero on an invalid/occupied port, unsafe host, missing assets, wrong
lesson, stale PID, or timeout. `status` exits non-zero unless the recorded process identity and
semantic readiness probe match. `learn-preview-reset-check` applies the same reducer used by the
visible Reset control to the canonical persisted-state vector twice, proving the unchanged
resettable-state/baseline digest, one audit-counter increment per invocation, history replacement,
and idempotency without pretending to mutate an open
browser. `down` is idempotent when no locator exists, stops only a process whose PID, start
fingerprint, command, cwd, preview root, and run ID still match, and exits non-zero if an owned
process survives. A mismatched/reused PID or foreign listener is reported and never signalled. The
Python command is a direct foreground fallback and creates no PID lifecycle, CSP, security,
fitness, or score claim; callers stop it with Ctrl-C.

## Success Criteria

- [ ] The retained preview is understandable and navigable as a static semantic document.
- [ ] Enhanced navigation is progressive, reversible, and never scroll/motion/hover-authoritative.
- [ ] Synthetic/non-completing labels appear on all four required surfaces.
- [ ] Four cards and insufficient-evidence tests pass with no causal attribution.
- [ ] Common harness and preview finish within three active hours or the spike stops for replanning.
- [ ] No issue #6, runner, portal, cloud, completion, or score workaround exists.

## Risk, Security, and Rollback

If the contract cannot stabilize inside three hours, stop; reduce presentation polish, never test
semantics. If unsafe content, privilege, completion, or false causality appears, remove the
offending path and stop for review. Operational rollback stops only the verified owned preview
process, removes transient `.artifacts/runtime/i5-02/**` and raw Gate A evidence after the
sanitized retention subset exists, and leaves tracked preview/common/harness source, plans,
retained evidence, and protected files unchanged. Source removal/revert requires later review and
is not an automated rollback.

## Next Steps

Freeze the Gate A contract digest and stop. Candidate foundations require a later readiness audit;
Barrier B, Gate C, Gate D, scoring, ADR, review, PR, and merge remain blocked.
