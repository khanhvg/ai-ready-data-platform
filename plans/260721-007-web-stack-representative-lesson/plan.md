---
title: "Issue #7: Web Stack with Representative Promotion-Trust Lesson"
description: "Plan a retained synthetic preview, equal three-candidate web spike, real-fixture decision barrier, and evidence-gated ADR-005 without implementation authority."
status: pending
priority: P1
issue: 7
branch: "plan/issue-7-web-stack-representative-lesson"
tags: [frontend, accessibility, decision-gate, security-s3, tdd]
blockedBy: []
blocks: []
created: "2026-07-20T21:29:33.691Z"
createdBy: "ck:plan"
source: skill
mode: deep-tdd
plannerPhase: fresh-initial-plan
requestedPlannerModel: "gpt-5.6-sol"
requestedModelReasoningEffort: "xhigh"
plannerOutputSha: "0890c4abab46f81d110be6cbd6de3560e631a735"
inputDiscoverySha: "a39251d45a56124322b9143ad16b926b2656073b"
integrationInputSha: "f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c"
masterReadinessSha: "e440c5855732d5d8f5d634e3cc1359c010cc5ed3"
barriers:
  gate0: ready-to-start
  gateA: ready-after-gate0
  candidateFoundations: provisional-only-after-gateA
  barrierB: blocked-on-issue-6-merge-and-digests
  gateC: blocked-on-barrierB-and-fresh-browser-manual-a11y
  gateD: blocked-on-complete-gateC-evidence
---

# Issue #7: Web Stack with Representative Promotion-Trust Lesson

## Overview

Deliver the earliest actually runnable artifact before choosing a web framework: a project-owned,
framework-neutral, semantic static `learn-preview` for the ten-act promotion-trust journey. It uses
only a safe synthetic projection and permanently says
`SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` at entry, state rail, verify/evidence, and
export. It has no `completed` state, runner, browser credential, mutation/cloud path, or release
claim. JavaScript may enhance reversible navigation; the complete facts and linear journey remain
understandable without JavaScript and with reduced motion.

After the common logical contract is frozen, time-box equal foundations for Astro + React islands,
Next.js App Router, and React/Vite + typed API. Every pre-issue-#6 result is provisional and
unscored. Hard Barrier B opens only after issue #6 is merged into the tested tree and exact SHA-256
digests for the two contracts and two tracked fixture files validate. Gate C then performs one
clean, identical real-fixture/browser/manual-accessibility rerun. Must-pass precedes scoring;
incomplete or invalid evidence yields no winner. Gate D writes ADR-005 as a winner proposal or an
explicit no-winner proposal and retains reproducibility evidence through I5-05.

This is a planning-only package. It does not claim any planned command or product artifact exists,
and it authorizes no implementation, package/browser installation, candidate execution, score,
validation, audit, cloud action, migration, PR, or merge.

## Authority and Current Blockers

| Boundary | Status at planner input | Consequence |
|---|---|---|
| Planner provenance | Planner output is `0890c4abab46f81d110be6cbd6de3560e631a735`; discovery, integration, and readiness inputs are the immutable SHAs in frontmatter | Validation/audit may add planning-only descendants; none authorizes implementation by itself |
| Future implementation input | Not yet assigned; the later readiness handoff must name one exact full SHA | Gate 0 must first prove local HEAD, tracking, and live remote equal that SHA, then retain it as the changed-path base and ancestor of every tested tree |
| Issue #7 path authority | `spikes/web/**`, ADR-005 proposal/evidence paths, and `mk/issue-5/i5-02.mk` are allowed | Issue-local Make commands are valid; root Make alias is a later shared-owner handoff |
| Issue #6 handoff | Four required files are absent; #6 is open and `triaged` | Barrier B, score, winner, and decision-grade ADR remain blocked |
| Browser/manual accessibility | Discovery had no browser instance | Gate C and any score/winner remain blocked until fresh current-browser and named-AT evidence exists |
| Root/shared/protected paths | Forbidden and hash/absence protected | Any change is a hard STOP, not a workaround |

## Scope Boundary

Allowed future implementation paths:

- `spikes/web/**`
- `docs/decisions/0005-web-stack.md`
- `docs/decisions/evidence/adr-0005-web-stack-scorecard.md`
- `docs/decisions/evidence/adr-0005-web-stack-scorecard.json`
- `mk/issue-5/i5-02.mk`
- this plan package for plan-state sync, except immutable `discovery/**`

Generated execution state is permitted only under `.artifacts/evidence/web-spike/**` and
`.artifacts/runtime/i5-02/**` while issue-local commands run. It is not a tracked implementation
or publication path. Before commit, sanitize/hash-index the retention set under
`spikes/web/evidence/retained/**`, stop owned processes, and remove transient runtime/output that
has no approved retention purpose.

Forbidden paths include root `Makefile`, `.gitignore`, root `release-manifest.json`,
`docs/code-standards.md`, shared `contracts/**`/`schemas/**`, dependency-owned
`tests/fixtures/learning/**`, portal/runner roots, existing data/config/runtime code, ignored
runtime fixtures, and unrelated files. Issue #6 outputs are consumed read-only after merge.

## Phases

| Phase | Name | Status | Runtime gate |
|-------|------|--------|--------------|
| 1 | [Gate 0 Authority and Freeze](./phase-01-gate-0-authority-and-freeze.md) | Pending | Ready after independent plan gates authorize implementation |
| 2 | [Gate A Common Contract and Static Preview](./phase-02-gate-a-common-contract-and-static-preview.md) | Pending | Gate 0; 3 active hours maximum |
| 3 | [Astro React Islands Foundation](./phase-03-astro-react-islands-foundation.md) | Pending | Gate A; provisional/unscored; 90m/3h kills |
| 4 | [Next App Router Foundation](./phase-04-next-app-router-foundation.md) | Pending | Gate A; provisional/unscored; 90m/3h kills |
| 5 | [React Vite Typed API Foundation](./phase-05-react-vite-typed-api-foundation.md) | Pending | Gate A; provisional/unscored; 90m/3h kills |
| 6 | [Barrier B Issue 6 Fixture Handoff](./phase-06-barrier-b-issue-6-fixture-handoff.md) | Pending / blocked | Merged #6 SHA + four exact digests + schema result |
| 7 | [Gate C Real Fixture Rerun and Score](./phase-07-gate-c-real-fixture-rerun-and-score.md) | Pending / blocked | Barrier B + fresh browser + manual accessibility; shares final 2h window |
| 8 | [Gate D ADR Retention and Handoff](./phase-08-gate-d-adr-retention-and-handoff.md) | Pending / blocked | Complete Gate C; no extra budget beyond the final 2h window |

## Dependencies and Timing

```text
Gate 0 -> Gate A -> Astro foundation ----+
                 -> Next foundation -----+-> Barrier B (#6 merged/digests)
                 -> Vite foundation -----+        + fresh browser/manual AT
                                                  -> Gate C must-pass/score
                                                  -> Gate D ADR/retention
```

- Active spike budget is exactly `3h common + 3h Astro + 3h Next + 3h Vite + 2h
  decision rerun/score/ADR = 14h` over at most two implementation days.
- Gate 0 preflight and external Barrier B waiting do no product work and do not start the active
  timers. Any contract, preview, candidate, measurement, or ADR work counts in its assigned cap.
- Gate D uses the remaining portion of the same final two-hour decision window; it does not add
  time. At cap, stop with the retained preview and ADR-005 `Proposed`/no-winner.
- Candidate phases may begin before #6 only after Gate A freezes the common harness. Their results
  are `PROVISIONAL_UNSCORED` or `ELIMINATED`, never numeric.

## Companion Contracts

- [Acceptance and test matrix](./acceptance-and-test-matrix.md)
- [Candidate protocol](./candidate-protocol.md)
- [Preview journey contract](./preview-journey-contract.md)
- [Security S3 disposition](./security-s3-disposition.md)
- [Issue #6 fixture handoff](./issue-6-fixture-handoff.md)
- [Implementation handoff](./implementation-handoff.md)
- Preserved [discovery package](./discovery/planner-handoff.md)

## Plan Acceptance

- The first runnable artifact is framework-neutral, direct/no-build-capable, synthetic-labelled,
  non-completing, semantic, reversible, safe, and retained regardless of the framework outcome.
- Four evidence cards remain grain-honest and conclude `insufficient evidence`; fulfillment,
  returns, and global DQ facts are never joined or causally attributed to a promotion.
- Common sharing is limited to manifest/state/failure/evidence/client logical shapes and test
  semantics; candidate rendering/routing remains native and measurable.
- Each candidate has an independent lockfile, identical caps, an executable foundation/must-pass
  kill, and no score when killed. Because the repository ignores `package-lock.json`, the three
  exact candidate lockfiles are force-added explicitly and their tracked state is a hard gate.
- Barrier B records an actual merged #6 SHA and exact file digests; any drift invalidates every
  candidate result and persisted browser state.
- Gate C records fresh screenshots/traces and manual keyboard, named screen-reader, 200% reflow,
  reduced-motion, and no-JS review plus fair raw performance/resource evidence.
- Scoring is impossible before every must-pass is complete. The weighted rubric and within-five-
  point Astro default apply only to complete passing candidates; otherwise the result is no winner.
- The complete 0-5 category anchor registry is written, tested, and digest-frozen at Gate 0 before
  candidate work; no observed candidate result may influence an anchor.
- Losing sources/build entrypoints are excluded without deleting reproducibility evidence; later
  cleanup is separately authorized and reversible.

## Planner Boundary

Independent validation and a fresh readiness audit are the next external phases. This fresh
initial planner performed only authority research, plan authoring, planner self-checks, and
publication. It did not validate, red-team, audit, implement, install, build, score, or merge.

## Validation Log

### 2026-07-21 — Independent initial validation

- Validator input: planner output `0890c4abab46f81d110be6cbd6de3560e631a735` with discovery
  `a39251d45a56124322b9143ad16b926b2656073b`, integration
  `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`, and master readiness
  `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`.
- Corrected only planning artifacts: future implementation-input authority, deterministic preview
  lifecycle/reset evidence, pre-Barrier-B foundation versus Gate C browser scope, ignored lockfile
  retention, and pre-candidate score-anchor freeze.
- Raw `discovery/**` remained immutable. See
  [initial validation report](./validation/initial-validation-report.md) for sampled evidence,
  findings, commands, blockers, and verdict.
