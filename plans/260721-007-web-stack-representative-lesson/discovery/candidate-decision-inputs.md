# Candidate decision inputs

## Purpose and non-decision

This document defines inputs the planner must hold equal across Astro + React islands, Next.js App Router, and React/Vite + typed API. It does not score a candidate, select a winner, or advance ADR-005.

The executable preview and the scored spike are separate artifacts:

- **Retained neutral preview:** framework-neutral, static, fixture-labelled, unscored, non-completing, and runnable without issue #6. It lives under `spikes/web/**`, consumes only a safe synthetic projection, and remains useful even if all candidates are eliminated.
- **Candidate implementations:** three isolated sources and lockfiles consuming one neutral candidate contract/test harness. Scores are created only after issue #6’s tracked fixture is merged and all candidates rerun from clean installs.

The neutral preview prevents the timebox/no-winner path from erasing the review surface. It is not a fourth scored candidate.

## Two-barrier execution model

| Barrier | Inputs | Permitted output | Explicitly forbidden |
|---|---|---|---|
| A — early review | Integration input plus a tiny safe static fixture labelled `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` | Common contract/test skeleton, neutral executable preview, novice/a11y/non-copy feedback | Scores, winner language, ADR evidence, completion mutation, runner/private API, release claim |
| B — decision | Issue #6 merge SHA; exact tracked fixture and schema hashes; common harness frozen; fresh browser available | Clean all-candidate rerun, raw evidence, must-pass dispositions, weighted scorecard, ADR-005 proposal evidence | Reusing provisional samples, candidate data workaround, scoring a killed candidate, bypassing a must-pass or no-winner outcome |

If issue #6 changes after Barrier B starts, invalidate all candidate results, update the recorded fixture hash, and rerun all candidates equally. A mixed-fixture scorecard is invalid.

## Framework-neutral candidate contract

The planner should place the source of this harness wholly under `spikes/web/**`. It must mirror issue #6 types read-only after merge; it must not create or edit shared contracts.

### Required logical objects

| Object | Required fields/behavior |
|---|---|
| `LessonManifestView` | lesson ID/version, contract version, fixture kind (`synthetic-preview` or `tracked-real`), fixture digest, minimum platform version, acts, prerequisite probes, hint levels, failure catalog, evidence declarations |
| `MartEvidenceView` | mart ID, display label, exact grain fields, time scope, filters, numerator, denominator, aggregation/weighting rule, observed values, limitations, source fixture evidence reference |
| `JourneyStateView` | stable attempt ID, `currentStepId`, `committedStepId`, transient answer/edit state, hint level, failure class, reset counter, verification/evidence status; preview mode has no completing state |
| `LabClient` | typed read-only replay methods in preview; later OpenAPI-compatible commands/events behind a same-origin BFF seam; no runner URL, token, or credential in browser types |
| `EvidenceIndexView` | deterministic evidence IDs, fixture digest, source mart, verifier result, timestamps normalized by fixture, and safe relative artifact paths |
| `CandidateEvidenceRecord` | candidate/mode/version/lock hash, environment, commands, timer, must-pass results, measurements, browser traces/screenshots, content schema results, dependency/CSP inventory |

### Preview state machine

Allowed preview states are `not-started`, `exploring`, `controlled-failure-shown`, `diagnosing`, `reset-demonstrated`, `fixture-verified`, `evidence-reviewed`, and `reflection-open`. The preview must not define, render, serialize, or emit `completed`.

State rules:

1. Scrolling never commits progress.
2. A named control or native link commits a step and updates the URL or isolated preview session state.
3. Back/forward and reload restore only the last committed step; transient answer text is either explicitly restored as a draft or explicitly discarded, never silently promoted.
4. Reset returns to the known preview baseline, increments a visible reset count, clears transient state, and explains that no repository/data asset was mutated.
5. Verify validates the static fixture projection and shows evidence; it cannot complete the lesson.
6. An environmental failure (missing/mismatched fixture or asset) cannot be presented as the controlled analytical failure.
7. Changing fixture kind or digest invalidates persisted preview state.

### Shared test IDs

The same test names and assertions must run unchanged against all candidates and the retained preview where applicable.

| ID | Assertion |
|---|---|
| WEB-CONTRACT-001 | Manifest and content schema reject missing/unknown grain, weighting, limitation, evidence, hint, and failure fields. |
| WEB-CONTRACT-002 | Every mart card exposes grain, time scope, filters, numerator, denominator, aggregation/weighting, and limitations. |
| WEB-CONTRACT-003 | No contract field or UI relationship represents a causal cross-mart join. |
| WEB-PREVIEW-001 | Fixture label and non-completing notice are present at the page start, state rail, verify result, and evidence export/view. |
| WEB-PREVIEW-002 | Preview network/mutation audit observes no runner, cloud, completion, or non-static request. |
| WEB-STATE-001 | Back, forward, and reload restore committed step and do not commit transient or scroll-only state. |
| WEB-STATE-002 | Reset is idempotent and returns the identical baseline digest. |
| WEB-FAIL-001 | Controlled analytical failure, environmental failure, and unexpected failure have distinct codes, copy, recovery, and evidence. |
| WEB-TRUST-001 | A naive promotion headline is rejected when the bundle is insufficient; the expected decision remains `insufficient evidence`. |
| WEB-TRUST-002 | No carrier/return/DQ fact is attributed to a promotion. |
| WEB-A11Y-001 | All actions and progressive disclosures work by keyboard with visible, logical focus. |
| WEB-A11Y-002 | Native landmarks/headings/tables/status/error relationships produce an understandable screen-reader sequence. |
| WEB-A11Y-003 | At 200% zoom/reflow the state rail cannot cover focus or content and no two-dimensional scrolling is required for narrative use. |
| WEB-A11Y-004 | `prefers-reduced-motion: reduce` removes non-essential motion without removing information or control. |
| WEB-STATIC-001 | With JavaScript disabled, the complete facts, evidence labels, limitations, and a linear navigation/fallback remain readable. |
| WEB-NOSCROLL-001 | Scrolling/animation/hover alone never verifies, commits, reveals the only copy of evidence, or advances completion. |
| WEB-API-001 | Browser bundle and network trace contain no credential, runner URL, privileged endpoint, wildcard CORS, or direct runner request. |
| WEB-E2E-001 | Full preview sequence frame → fail → diagnose → reset → verify → evidence → reflection produces a deterministic trace. |
| WEB-NONCOPY-001 | Project-owned inventory/reviewer record confirms principles only; no copied prose/assets/layout/style/source. |

## Exact first journey

### Entry and prerequisite probes

Before act 1, run three unscored, non-blocking probes. Their purpose is to choose an explanation path, not to grade or complete.

1. **Grain probe:** identify which fields define a row in two sample mart summaries.
2. **Weighted-measure probe:** choose between average-of-averages and a displayed numerator/denominator calculation.
3. **Failure probe:** distinguish a deliberately failing analytical assertion from a missing fixture/API.

Answers set the initial hint level locally. Wrong answers must not shame, trap, or lower an invisible score.

### Hint ladder

Every consequential prompt uses the same deterministic ladder:

1. **Orient:** point to the relevant grain/status/measure label and restate the decision question.
2. **Connect:** expose the numerator, denominator, weighting, or failure-class relationship needed for the next action.
3. **Explain:** show the worked reasoning and limitation, then let the learner retry or continue in review mode.

Hints cannot mutate verifier output or completion. The evidence record may state which hint level was viewed, without treating it as success or failure.

### Narrative and interaction pacing

- Start with the business decision and stakeholder consequence, not a framework tour.
- Present one act at a time with explicit previous/next controls and a linear semantic document order.
- Keep a compact state/evidence rail showing act, fixture kind, failure class, last committed action, reset/verify state, and evidence count.
- On narrow view/200% zoom, turn the rail into an in-flow summary landmark; it must not stay fixed over content.
- Use motion only to reinforce a state transition. A textual status and the final static state must exist before/without animation.
- Link deeper definitions rather than expanding every detail into the main sequence.
- Use project-owned wording, component structure, spacing, colors, diagrams, and timing. Do not reproduce the reference site’s visual grammar.

### Four-card decision evidence

The diagnosis act shows four independently titled cards/tables:

1. Promotion headline at `promo_name, channel`.
2. Fulfillment context at `carrier, region`.
3. Returns/refunds context at `return_reason, category, region`.
4. Global controlled DQ scenarios/counts.

Each card includes an explicit `What this supports` and `What this cannot establish` section. The conclusion control offers evidence-bounded alternatives, including `insufficient evidence`. It must not let a learner assert causal trust merely by visiting all cards.

## Failure taxonomy

| Class | Example code | Meaning | Recovery | May advance? |
|---|---|---|---|---|
| Controlled lesson failure | `PROMOTION_HEADLINE_INSUFFICIENT` | The bounded analytical assertion intentionally fails and creates the diagnosis task. | Diagnose grains/measures/limitations, reset, and verify. | To diagnosis only. |
| Environmental failure | `FIXTURE_UNAVAILABLE`, `FIXTURE_DIGEST_MISMATCH`, `STATIC_ASSET_UNAVAILABLE` | Required environment/input is absent, stale, or broken. | Stop, repair environment, restart with recorded digest. | No. |
| Unexpected product failure | `PREVIEW_UNEXPECTED` | Unclassified render/state/schema error. | Preserve trace, stop attempt, fix candidate. | No. |
| Future authorization failure | `SESSION_ORIGIN_REJECTED`, `CSRF_REJECTED` | Later BFF correctly rejects an unauthorised request. | Re-launch through valid portal flow; do not weaken control. | No. Not implemented in issue #7. |

## Candidate mode declarations

Each candidate starts its three-hour clock only after the common harness, Node/package-manager baseline, test command, fixture adapter, and declared mode are frozen. Changing mode resets evidence and does not extend the cap.

### Astro + React islands

- Default: statically rendered MDX/content collections with the smallest React lab-state island.
- Preview API: imported static fixture adapter only.
- Future seam: same-origin typed BFF client; Node adapter is evaluated as an evolution option, not used to smuggle runner behavior into preview.
- Kill evidence: island boundary swallows full lesson, content schema cannot express common contract, or committed state/static fallback requires a candidate-only contract fork.

### Next.js App Router

- Declare exactly one measured mode: recommended spike input is self-hosted standalone App Router with a prerenderable lesson page, narrow Client Component, and read-only Route Handler replay adapter. Record why static export was or was not used.
- Do not use Server Actions as a substitute for the shared OpenAPI-compatible boundary.
- Freeze MDX/frontmatter/schema stack before timing; measure the actual client boundary and runtime.
- Kill evidence: common content contract requires a framework-specific fork, client boundary captures the full lesson, or static/reduced-motion output loses facts.

### React/Vite + typed API

- Static build plus explicit typed API adapter seam; the preview adapter reads only bundled safe fixture data.
- Supply a genuine pre-rendered/MPA semantic route or equivalent deterministic static artifact. An empty `<div id="root">` is a must-pass failure.
- Use a declared production-like static host for startup/RSS; `vite preview` may be a developer check but is not deployment evidence.
- Kill evidence: no meaningful no-JS artifact, secret-bearing `VITE_*` design, or content-schema/MDX composition cannot stay within common contract/cap.

These inputs do not assume the recommended Next mode will win. They make its BFF/runtime advantage and cost measurable.

## Must-pass gate

A candidate is eliminated, receives no numeric score, and cannot participate in the tie rule if any item is red at three hours:

1. Same common lesson manifest, state transitions, failure codes, fixture adapter, and E2E IDs.
2. Reversible question → progressive disclosure → controlled failure → diagnose → reset → verify → evidence → reflection journey.
3. Correct committed/transient state after back, forward, reload, and reset.
4. Distinct controlled/environmental/unexpected failures.
5. Four-grain evidence bundle and `insufficient evidence`; no cross-grain attribution.
6. No preview completion, runner, credentials, AWS/model dependency, or direct privileged boundary.
7. Semantic HTML, keyboard, screen reader, 200% zoom/reflow, reduced motion, and no-JS/static equivalent.
8. No scroll-, animation-, hover-, or JS-only fact/control/completion.
9. Project-owned trusted MDX/content schema validation and deterministic browser E2E.
10. Typed OpenAPI-compatible BFF seam with no shared-contract edit.
11. Clean local startup, reset, and shutdown with exact reproducible commands.
12. Non-copy inventory and safe dependency/CSP record.

The 90-minute early kill applies if the candidate cannot clean-install, render its semantic static lesson route, and consume the common lesson contract.

## Equal time and 14-hour kill protocol

| Work | Cap | Stop behavior |
|---|---:|---|
| Common contract/harness and neutral early preview | 3h | Reduce preview polish, never acceptance semantics. If contract cannot stabilize, stop the spike and return to planner. |
| Astro candidate | 3h | Kill at 90m foundation gate or 3h must-pass gate. |
| Next candidate | 3h | Same clocks/gates. |
| React/Vite candidate | 3h | Same clocks/gates. |
| Clean rerun, scorecard, ADR-005 proposal | 2h | No score/ADR if evidence cannot complete. |
| **Total** | **14h, at most two implementation days** | Stop. ADR remains Proposed; retained neutral preview remains runnable. |

Timer records contain UTC start/end, active minutes, pauses and reason. Only an external outage or required user decision may pause a timer; debugging, installs, authoring, tests, and measurement count. No candidate receives compensating time.

## Measurement protocol

All raw samples and the exact environment record are retained. Do not summarize before preserving raw evidence.

### Environment record

- input/issue #6 merge SHAs and fixture digest;
- OS/kernel/architecture, CPU model/count, physical memory;
- Node and package-manager versions;
- candidate manifest/lock digest and declared build/runtime mode;
- browser/Playwright versions, viewport/device scale, locale/timezone, reduced-motion setting;
- commands, ports, readiness condition, repetitions, measurement order, and background-load note.

### Cold/warm startup and RSS

- **Install time is separate.** Run the same frozen clean-install command for reproducibility evidence; do not fold network registry time into app startup.
- **Cold app start:** a new production-like process from already built artifacts to the first successful semantic page/readiness assertion, after candidate-local build/runtime caches are removed by an explicit safe candidate-local command.
- **Warm app start:** a new process immediately after a clean shutdown with build artifacts and candidate-local caches unchanged.
- Collect at least three cold and three warm samples within the shared rerun; report all samples, median, and range. Rotate candidate measurement order across rounds (A→N→V, N→V→A, V→A→N).
- Sample steady-state process-tree RSS after readiness and after the full preview journey. Do not report only the shell parent or browser memory as server RSS.
- Static candidates must identify the production-like host being measured. Development servers do not count.

### JS payload and bundle

- Record emitted client assets and build manifest, raw and transfer-compressed sizes, route-level initial JS, and lab-island/lazy chunks.
- Capture browser network bytes for initial semantic route and for opening the interactive lab.
- Keep source maps/evidence out of client production transfer calculations while recording whether they are generated.
- Record total built artifact size separately from initial JS; do not combine server and browser bytes.

### Authoring and schema ergonomics

Use the identical authoring task: add one project-owned explanation callout, one new mart limitation field, one prerequisite probe, and one hint level; then intentionally break a required content field and record the validation error. Evidence includes files touched, active minutes, generated types/editor support, error location/clarity, hot-reload behavior, and required framework glue. Subjective notes remain notes; only predefined rubric anchors receive points.

### Browser E2E, visual, and accessibility

- Chromium baseline plus one additional engine for the full common journey.
- JavaScript-off, reduced-motion, offline/environmental failure, back/reload/reset, and 200% reflow projects.
- Normalized screenshots for entry, controlled failure, four-card evidence, reset, verification, and reflection; trace on first retry/failure.
- Automated axe is necessary but insufficient. Record manual keyboard path, named screen reader/browser/OS, heading/landmark/table/status/error experience, focus after disclosure/reset, and zoom/reflow observations.
- Visual diffs run in the same pinned container/OS/browser/font environment; differing hosts invalidate comparison rather than penalize a candidate.

## Weighted scoring and no-winner behavior

Only candidates passing every must-pass receive a score.

| Category | Weight |
|---|---:|
| Authoring, content schema, MDX ergonomics | 20 |
| Accessibility and static/reduced-motion behavior | 20 |
| Lab state, evidence, and typed API boundary | 20 |
| Cold/warm startup, RSS, and client JS | 15 |
| Unit/E2E/visual evidence quality | 10 |
| Hosted/ECS evolution and rollback | 10 |
| Maintenance, dependency, and supply-chain burden | 5 |

Use predefined 0–5 anchors per category, multiply by weight/5, and preserve reviewer rationale and raw evidence. Highest passing total wins. If passing candidates are within five points, the binding default is Astro + React islands because the product is content-heavy and benefits from progressive hydration—but only if Astro itself passes every must-pass and complete evidence exists.

No winner is the required result when:

- no candidate passes every must-pass;
- issue #6 real-fixture evidence is absent or mixed;
- fresh browser/a11y evidence is unavailable;
- measurement comparability is invalid and cannot be rerun within 14 hours; or
- the time cap expires before a complete scorecard.

In that case ADR-005 stays Proposed and I5-05 remains blocked. The owner must narrow requirements or explicitly authorize a new spike; the tie default cannot bypass no-winner.

## Retention, rollback, and losing spikes

Before I5-05 merges, retain all three candidate source trees, lockfiles, exact commands, fixture and contract digests, tests, measurements, browser artifacts, timer logs, and eliminations. Exclude losing candidates from any product build/workspace entry point, but do not delete their reproducibility evidence.

The neutral executable preview and common contract/test harness remain tracked regardless of winner. After I5-05 merge, a separately authorized cleanup may remove losing install/build outputs and then source only when:

1. a reproducible source bundle/archive and SHA-256 is retained;
2. lockfile, commands, fixture/schema digests, scorecard, raw measurements, browser evidence, and non-copy inventory remain tracked;
3. the common contract and tests remain framework-neutral and executable against the winner;
4. a clean checkout can reproduce the winning preview; and
5. changed-path evidence proves no shared contract, runner, root Makefile, portal root, protected docs, or release manifest was removed or modified.

Rollback for any failed candidate or contaminated score is to remove it from winner consideration, delete its numeric score, restore the neutral preview as the only executable issue #7 surface, and keep ADR-005 Proposed.

## Local private boundary and ECS implications

### Preview

- Loopback-only binding and collision-safe port.
- No browser credential, session, CSRF token, CORS exception, runner URL, subprocess, or privileged container.
- Static safe fixture has a deterministic digest and no secret/PII/host path.

### Future portal boundary compatibility

Candidate types must permit a later same-origin portal BFF. The BFF—not browser code—will hold the runner relationship. The future security contract includes exact Host/Origin allowlists, no wildcard CORS, launch-secret/session exchange, HttpOnly/SameSite cookies, CSRF on mutations, DNS-rebinding/cross-origin negatives, and preferably a Unix socket. Candidate scoring tests interface compatibility and absence of contradictions; it does not implement the privileged side.

### ECS/rollback analysis

- Static assets and server bundles must be immutable/version-addressed.
- Runtime candidates must expose readiness, handle termination, avoid in-container durable state, and declare cache/version-skew behavior.
- A later ECS owner can use versioned task definitions/image digests and health-gated circuit-breaker rollback to the last completed deployment.
- The spike performs no cloud operation. It records a local production-like start and a written mapping from candidate artifact/process model to ECS task/revision/rollback behavior.

## Planner decisions that remain

1. Confirm whether issue #7 may create only the master-assigned `mk/issue-5/i5-02.mk` fragment or must expose preview/score commands another way entirely within `spikes/web/**`; root `Makefile` and `.gitignore` remain forbidden.
2. Freeze the neutral preview location and minimal no-build/start command under `spikes/web/**`.
3. Freeze exact candidate package/Node versions, common schema adapter, timer recorder, measurement host command, and score anchors immediately before implementation.
4. Record the exact issue #6 merge and fixture hashes that open Barrier B.
5. Schedule a browser-capable, screen-reader-capable scoring environment; without it the correct outcome is no winner.
