---
phase: 7
title: "Gate C Real Fixture Rerun and Score"
status: pending
priority: P1
dependencies: [6]
effort: "final 2 active hours shared with Gate D"
barrier: blocked-on-barrier-b-and-fresh-browser-manual-a11y
---

# Phase 7: Gate C Real Fixture Rerun and Score

## Context Links

- [Candidate protocol](./candidate-protocol.md)
- [Acceptance and test matrix](./acceptance-and-test-matrix.md)
- [Issue #6 fixture handoff](./issue-6-fixture-handoff.md)
- [Security S3 disposition](./security-s3-disposition.md)

## Overview

Run one clean, identical, decision-grade comparison on the merged real fixture. Gate C requires a
fresh current-browser/Playwright environment and manual accessibility review; discovery screenshots
or synthetic scores cannot substitute. Full must-pass is binary and precedes weights. Missing,
unequal, or invalid evidence consumes the remaining window and yields no winner.

## Entry Requirements

- Gate 0/A and Barrier B pass at one tested tree; all three foundation clocks/dispositions exist.
- Playwright `1.61.1` can launch a current stable Chrome channel plus one additional engine
  (WebKit or Firefox), with exact browser versions recorded. Required browser installation is
  prepared before the Gate C timer; if unavailable, Gate C does not pass.
- A manual review session is scheduled on the same functional build for keyboard, VoiceOver on
  the recorded macOS/Safari versions (or another explicitly named screen reader/browser/OS),
  200% zoom/reflow, reduced motion, and no-JS/static comprehension.
- Environment, ports, locale/timezone, viewport/device scale, fonts, background load, fixture
  digest, candidate modes, locks, and measurement order are frozen.

## Exact Must-Pass Before Scoring

1. Identical common manifest/state/failure/evidence/client logical shapes and unchanged WEB IDs.
2. Semantic HTML and complete no-JS/static facts/navigation.
3. Keyboard, named screen reader, 200% reflow, visible focus, reduced motion, non-color status.
4. Back/forward/reload/reset committed/transient state and digest invalidation.
5. Controlled/environmental/unexpected failure separation and safe recovery.
6. Four separate grains, `insufficient evidence`, and no promotion causality attribution.
7. No `completed`, privilege, runner, credential, cloud/model dependency, wildcard CORS, or unsafe
   runtime/remote content.
8. Scroll/motion/hover/card visitation never commits, verifies, or reveals unique evidence.
9. Trusted build-time content/schema validation and deterministic cross-browser E2E.
10. Read-only OpenAPI-compatible future BFF seam without shared edits.
11. Production-like startup/readiness/shutdown and no durable candidate-local state.
12. Safe CSP, locked/reviewed dependencies, sanitized evidence, and non-copy attestation.

Any red item makes that candidate `ELIMINATED` with `numericScore: null`. A required missing manual
or browser record makes the comparison incomplete and prevents all scoring/winner publication.

## Architecture

The common harness orchestrates, measures, and hashes candidate-native build/start/test commands;
it does not normalize away topology. A binary must-pass aggregator feeds a separate score function
that refuses incomplete candidates. Raw evidence is canonical; human scorecard prose is derived
later from its indexes.

## File Inventory

| Action | Planned path | Purpose | Test impact |
|---|---|---|---|
| Create | `.artifacts/evidence/web-spike/<run-id>/gate-c/**` | Canonical raw run evidence | Generated, sanitized, hash-indexed |
| Create | `spikes/web/evidence/retained/<run-id>/**` | Reviewable retained source/raw evidence subset | Tracked through I5-05 |
| Create | `spikes/web/harness/scripts/measure.mjs` | Startup/RSS/JS/order/raw samples | Equal definitions |
| Create | `spikes/web/harness/scripts/must-pass.mjs` | Binary gate aggregation | No score bypass |
| Create | `spikes/web/harness/scripts/score.mjs` | 0-5 anchored weights after pass | Rejects incomplete candidates |
| Create | `spikes/web/harness/tests/scoring.test.mjs` | Killed/incomplete/tie/no-winner negatives | TDD decision rules |
| Modify | `mk/issue-5/i5-02.mk` | Real-rerun/browser/manual/scorecard checks | Root Make unchanged |

## Related Code Files

- Create only measurement/must-pass/score tests, generated/retained evidence, and issue-local Make
  entries listed above.
- Re-run candidate sources without changing frozen modes/contracts except fixes within the shared
  final window, which invalidate prior samples.
- Delete no source or decision evidence.

## Measurement Definitions

- Clean install time is separate from app startup; use exact candidate lock and approved
  lifecycle-script policy.
- Cold start: built artifact, candidate-local runtime caches safely cleared, new production-like
  process to semantic readiness. Warm start: clean shutdown, unchanged built artifact/cache, new
  process to readiness.
- Run three cold and three warm samples for every surviving candidate. Rotate complete rounds
  `Astro→Next→Vite`, `Next→Vite→Astro`, `Vite→Astro→Next`; retain all raw values, median, range,
  anomaly/invalidation reason, and no selective retry.
- Sample process-tree RSS at readiness and after full journey; label static host versus integrated
  Next runtime and do not include browser memory as server RSS.
- Record built artifact total, emitted client manifest, raw/gzip/brotli client assets, route
  initial JS, interactive/lazy chunks, and browser transfer for initial page and lab opening.
- Run identical authoring task: add one explanation callout, one limitation field, one probe, one
  hint level, then break a required field. Record active time, files, types/editor support, error
  precision, hot reload, and framework glue.
- Capture normalized entry, controlled failure, four-card evidence, reset, verify, and reflection
  screenshots; trace first retry/failure; run offline/environment, JS-off, reduced-motion,
  back/reload/reset, 200% projects and full journey in Chrome plus one additional engine.

## Weighted Score

| Category | Weight |
|---|---:|
| Authoring/content schema/MDX ergonomics | 20 |
| Accessibility/static/reduced-motion behavior | 20 |
| Lab state/evidence/typed API boundary | 20 |
| Cold/warm startup, RSS, and client JS | 15 |
| Unit/E2E/visual evidence quality | 10 |
| Hosted/ECS evolution and rollback | 10 |
| Maintenance/dependency/supply-chain burden | 5 |

Use predefined 0-5 anchors and `points = weight * anchor / 5`. Highest complete passing total
wins. If passing totals are within five points, Astro is the default only if Astro itself is a
complete must-pass candidate. The default never rescues eliminated/incomplete evidence.

## Dependency Map

```text
Barrier B exact fixture + current browser/manual AT + frozen environment
  -> clean installs/builds
  -> identical must-pass/browser/manual/measurement evidence
  -> eliminate failures
  -> score complete survivors only
  -> Gate D winner or no-winner proposal
```

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | Synthetic/mixed fixture enters run | Reject all results; no score |
| Critical | Missing manual AT/current-browser artifact | No score/no winner |
| Critical | Candidate fails four-grain/no-privilege/static gate | `ELIMINATED`, score null |
| High | Cache/order/orphan/background-load bias | Invalidate equal round; rerun all or no winner |
| High | Killed candidate gets partial score | Score schema/check fails |
| High | Tie within five with Astro complete | Astro default with explicit evidence/rationale |
| High | Time expires/evidence incomparable | No winner; stop at 14h |

## Implementation Steps

1. Write score rejection/tie/no-winner tests and freeze the comparison environment.
2. Run clean candidate installs/builds and full must-pass/browser/manual evidence.
3. Collect rotated startup/RSS/JS/authoring/security raw samples and verify comparability.
4. Score only complete survivors or emit no-winner; hand verified indexes to Gate D.

## Tests Before

Write scoring tests that reject synthetic fixtures, differing digests/modes/WEB IDs, missing raw
samples, missing manual/browser/non-copy/CSP evidence, killed-candidate numbers, invalid anchors,
unjustified retries, illegal tie default, and winner claims after cap.

## Refactor

Run clean installs/builds, exact must-pass, rotated samples, browser/manual reviews, and authoring
task without changing the frozen modes/contracts. Fixing a candidate inside Gate C is allowed only
within the shared final window and invalidates its earlier samples; no candidate gets extra time.

## Tests After

- Verify evidence schema, file hashes, redaction, single fixture/mode/test-ID digest, and timer.
- Review every must-pass before invoking scoring.
- Re-run protected-hash/changed-path/credential/non-copy checks.
- Preserve raw samples and candidate dispositions even when result is no winner.

## Regression Gate

Planned future commands:

```bash
make -f mk/issue-5/i5-02.mk web-real-fixture-rerun I5_01_MERGE_SHA=<full-40-hex-merged-sha>
make -f mk/issue-5/i5-02.mk web-browser-evidence
make -f mk/issue-5/i5-02.mk web-manual-a11y-check
make -f mk/issue-5/i5-02.mk web-spike-scorecard-check
```

The rerun target calls each candidate's install/build/test/a11y/E2E/evidence targets in rotated
measurement order. Browser and manual targets emit named version/checklist/artifact indexes and
exit non-zero when incomplete. `web-spike-scorecard-check` exits non-zero for Barrier B drift,
missing must-pass/raw/manual/browser/security/non-copy data, illegal score/tie/winner, cap overrun,
or unretained evidence. A valid explicit no-winner record passes the scorecard schema only when it
contains no unsupported winner and preserves blockers; it does not unblock I5-05.

## Success Criteria

- [ ] Complete, comparable real-fixture evidence exists for every scored candidate.
- [ ] Full binary must-pass precedes all numeric scoring.
- [ ] Measurements/manual/browser evidence follow one frozen protocol.
- [ ] Gate C plus Gate D finishes inside the final two-hour window and total 14 hours.
- [ ] Incomplete/invalid evidence produces no winner.

## Risk, Security, and Rollback

Bias, secret-bearing traces, unsafe CSP/content, and manual-gate laundering are hard failures.
Invalidate the affected comparison, remove scores, mark candidates/evidence accordingly, retain
the neutral preview, and return ADR-005 to Proposed/no-winner. Delete only scoped transient runtime
state; preserve raw/retained evidence and protected files.

## Next Steps

Gate D records the evidence-backed winner proposal or explicit no-winner state within the same
final two-hour window.
