# Scenario report

## Run configuration

- Skill: `ck:scenario`
- Requested iterations: **15**
- Executed iterations: **15**
- Scope: issue #7 pre-plan discovery only
- Input SHA: `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`
- Binding master audit commit: `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`
- Full machine-readable rows: [scenario-results.tsv](scenario-results.tsv)

The run used one scenario per iteration. Iterations 1–12 deliberately rotated through all twelve scenario dimensions before iterations 13–15 combined timing/scale, persona/state, and environment/deployment. No scenario was dropped for similarity; the final three are explicit stress variants rather than duplicates.

## Saturation progress

### Iterations 1–5

- Scenarios: 5
- Dimensions: user types, input data, timing, scale, state transitions
- New high-risk themes: adaptive novice support, executable-content boundary, fixture drift, resource honesty, reversible state
- Saturation signal: low; every iteration added a distinct contract risk

### Iterations 6–10

- Scenarios: 10 cumulative
- Added dimensions: environmental, error cascades, authorization levels, data integrity, integration points
- New critical themes: browser privilege boundary and false cross-grain causality
- Saturation signal: moderate; shared fixture/state vocabulary emerged, but authorization/integration risks were still novel

### Iterations 11–15

- Scenarios: 15 cumulative
- Added base dimensions: compliance requirements and business logic
- Composite variants: measurement-order bias, hostile learner state, and local-to-ECS rollback/CSP behavior
- Saturation signal: high after iteration 15; the last three reused known invariants but exposed distinct combined failure paths. The requested fixed iteration count was completed rather than stopping early.

## Coverage metrics

| Metric | Result |
|---|---:|
| Scenarios generated | 15 |
| Unique base dimensions covered | 12 / 12 |
| Critical scenarios | 4 |
| High scenarios | 11 |
| Enumerated edge cases | 38 |
| Unique actor roles | 7 |
| Duplicate scenarios discarded | 0 |
| Scenario-to-evidence mappings | 15 / 15 |
| Scenario-to-rollback mappings | 15 / 15 |
| Scenario-to-dependency mappings | 15 / 15 |
| Scenario-to-boundary mappings | 15 / 15 |

Using the skill’s composite formula:

`15×10 + 38×15 + (12/12)×30 + 7×5 + 15×3 = 830`

The composite is a coverage signal, not a product score or ADR input.

## Scenario summaries

### SC-001 — novice prerequisite adaptation

A novice answers grain and weighting probes incorrectly and consumes the full hint ladder. Expected behavior is unscored adaptation: hints move from orienting labels, through numerator/denominator connections, to a worked limitation. No hidden grade, verifier change, or completion event is permitted.

Edge cases: skipped probes, delayed screen-reader feedback, changed answer after full explanation.

### SC-002 — hostile content boundary

Fixture strings contain JSX-like text, scripts, unsafe links, closing tags, secret-shaped canaries, and oversized values. Only project-owned MDX is compiled. Fixture values are data or rejected; they cannot become executable MDX/HTML, remote requests, or secrets in client code.

Edge cases: malicious URL scheme, closing-tag payload, oversized value, frontmatter import.

### SC-003 — fixture drift during scoring

Issue #6’s fixture or schema digest changes after one candidate runs. The harness rejects a mixed scorecard, invalidates all previous samples, and requires a clean all-candidate rerun. The unscored preview remains available.

Edge cases: schema changes under the same lesson version, evidence-only changes, persisted browser state bound to the old digest.

### SC-004 — upper content and state bounds

The maximum representative acts, evidence rows, hints, and limitations are rendered and traversed. Required facts cannot be truncated or hidden merely to improve bundle/RSS numbers. Bounds, raw resource data, and usability are evidence.

Edge cases: long labels, many evidence rows, large limitation copy, repeated reset/replay.

### SC-005 — reversible state interruption

Back/forward, reload, scroll, duplicate reset, stale tab, and verification are applied while committed and transient state differ. Only explicit actions commit; reset is idempotent; fixture changes invalidate state; preview cannot complete.

Edge cases: reload during animation, duplicate reset, stale tab, fixture digest change.

### SC-006 — accessibility environments

The full journey is inspected with keyboard, a named screen reader, 200% zoom/reflow, reduced motion, JavaScript disabled, and a narrow viewport. Facts and evidence remain in semantic order; the rail reflows and does not cover focus; motion is never informational authority.

Edge cases: sticky rail obscures focus, missing status announcement, inaccessible disclosure, static/print order mismatch.

### SC-007 — controlled/environmental error cascade

The intended analytical assertion fails, then the fixture becomes absent or mismatched. The UI preserves distinct codes, status, evidence, recovery, and progression. Environmental breakage stops the attempt rather than becoming the lesson challenge.

Edge cases: offline after cache, unexpected schema error, restored fixture has another digest.

### SC-008 — hostile-origin authority probe

A malicious local origin attempts cross-origin/rebinding-style access, while the bundle and browser storage are inspected. Issue #7 should expose no privileged operation at all. The future Host/Origin/session/CSRF/Unix-socket contract is a compatibility constraint, not an implemented toy runner.

Edge cases: wildcard development CORS, host alias, token in source map, public build-time env.

### SC-009 — plausible false causal inference

Promotion revenue and operational symptoms look correlated, with overlapping labels/counts. The learner cannot filter or join incompatible grains, and the verifier rejects causal trust. The correct decision remains `insufficient evidence` and identifies the missing common-grain data.

Edge cases: repeated region labels, coincidental counts, similar category/promotion names.

### SC-010 — framework integration drift

All candidates receive valid/invalid contract shapes. The same runtime/schema tests must pass without edits to shared contracts or browser-to-runner shortcuts. Framework mechanics stay behind `LabClient` and candidate adapters.

Edge cases: Next Server Action shortcut, Astro-only endpoint field, Vite compile-time assertion without runtime validation.

### SC-011 — publication/compliance review

Screenshots, traces, source, fixture, locks, dependencies, CSP, and non-copy inventory are reviewed together. No copied expression, secret, personal/host path, unlocked tree, unreviewed install script, or unexplained advisory/CSP trade-off may enter published evidence.

Edge cases: user path in screenshot, environment value in source map, transitive lifecycle script, unfixable advisory.

### SC-012 — synthetic authority laundering

A polished early preview is run end-to-end and its output is intentionally offered to the scorecard/ADR. Fixture-kind/digest constraints reject it. There is no preview completion transition or API, even under local browser tampering.

Edge cases: DOM edit, localStorage edit, query parameter claiming real fixture, renamed evidence file.

### SC-013 — measurement-order and load bias

Three measurement rounds rotate candidate order while one background-load anomaly, port collision, orphan process, or cache difference occurs. Raw data and predefined invalidation rules prevent selective retries; inability to rerun fairly within the cap yields no winner.

Edge cases: registry outage, orphan process, port collision, filesystem-cache difference.

### SC-014 — hostile learner state

An advanced learner edits URL/session/local storage, duplicates attempt IDs across tabs, rolls back the clock, and copies state between fixture versions. Browser claims cannot author verification/evidence; invalid state resets safely; no preview completion exists.

Edge cases: clock rollback, duplicate attempt, cross-fixture state copy.

### SC-015 — local artifact to ECS rollback

A production-like local candidate artifact is started, health-checked, terminated, deliberately replaced by a broken release, and rolled back locally. The evidence maps immutable artifacts, signal/cache behavior, image digest/task revision, and circuit-breaker rollback without making a cloud call.

Edge cases: nonce CSP changes rendering mode, mixed stale assets, Astro mode drift, Vite development server substitution.

## Critical/high mapping to evidence and recovery

Every generated scenario is Critical or High and therefore appears here.

| Scenario | Acceptance evidence | Rollback/removal | Dependency | Blocks if unresolved |
|---|---|---|---|---|
| SC-001 | Probe/hint state assertions, AT transcript, no completion/network event | Remove hidden scoring; use explicit static prerequisite explanation | Lesson contract vocabulary | Preview acceptance, ADR, portal cook |
| SC-002 | Negative schema/render tests, CSP/network trace, bundle/credential scan | Remove runtime/remote MDX and unsafe renderer; regenerate or eliminate | Candidate content toolchain | Preview, ADR, portal cook |
| SC-003 | Single fixture/contract digest invariant and invalidation/rerun log | Delete all affected scores/samples; rerun all candidates | Issue #6 | ADR, portal cook; not preview |
| SC-004 | Bound tests, complete DOM facts, raw bundle/startup/RSS data | Invalidate resource score; remove nonessential presentation or eliminate | Common bounds/harness | ADR, portal cook |
| SC-005 | Transition tests, persisted-state snapshot, repeatable baseline digest | Remove faulty persistence/motion; restore neutral state model | Common state and fixture digest | Preview, ADR, portal cook |
| SC-006 | Axe plus manual keyboard/screen-reader/zoom, reduced-motion/no-JS tests | Flatten rail/motion; preserve semantic static sequence; withhold pass | Browser/AT environment | Preview acceptance, ADR, portal cook |
| SC-007 | Distinct failure code/copy/recovery tests, offline/mismatch traces | Remove generic error path; restart attempt on correct fixture | Fixture adapter/API vocabulary | Preview, ADR, portal cook |
| SC-008 | Empty privileged-route inventory, bundle/storage/network scan, future negative contract | Remove credential/route/CORS assumption and eliminate if necessary | Future I5-04/I5-05 contract | Preview, ADR, portal cook |
| SC-009 | Grain/relationship tests, forbidden-attribution scan, expected insufficient result | Delete composite/join and dependent evidence/score | Existing marts + issue #6 | Preview, ADR, portal cook |
| SC-010 | Identical contract output, schema digest, changed-path/bundle report | Remove candidate fork/shortcut; reset adapter or eliminate | Issue #6/common harness | ADR, portal cook |
| SC-011 | Reviewer/non-copy attestation, sanitized evidence, credential/dependency/CSP scans | Remove/regenerate contaminated/derivative artifact; remove dependency or eliminate | Project/package review | Preview publication, ADR, portal cook |
| SC-012 | Fixture-kind/digest binding, scorecard rejection, no completion event/API | Delete score/ADR/completion artifacts; retain neutral preview | Issue #6 and I5-05 authority | ADR, portal cook; not preview |
| SC-013 | Rotated raw runs, environment/timer/process-tree data, invalidation rule | Rerun equal round/category or declare no winner | Measurement host + issue #6 | ADR |
| SC-014 | Tamper E2E, state schema/digest binding, non-client verifier source | Clear/restart state; remove client-authoritative evidence path | Common state; I5-05 later | Preview, ADR, portal cook |
| SC-015 | Local build/start/stop/rollback log, hashes/CSP, ECS mapping | Remove deployment points; revert to retained preview; keep ADR Proposed | Candidate runtime + later ECS owner | ADR, portal cook |

## Cross-scenario invariants for the planner

1. Fixture kind and digest bind content, browser state, evidence, scorecard, and ADR evidence.
2. Four mart views remain separate; no UI affordance may create causal promotion attribution.
3. Preview has no completion state or privileged network authority.
4. Committed navigation is explicit and reversible; scroll/motion/hover are never authority.
5. Environmental failure blocks advancement and cannot substitute for the controlled failure.
6. Accessibility/static behavior is a must-pass with manual and automated evidence.
7. Candidate comparison uses one contract, one test harness, one environment, frozen modes, equal caps, and raw measurements.
8. Killed candidates have no numeric score. Missing decision evidence yields no winner.
9. Retain a neutral executable preview and reproducibility evidence independent of framework outcome.
10. No cloud, runner, shared-contract, root Makefile, portal-root, protected-doc, or release-manifest mutation belongs to issue #7.

## Scenario disposition

No scenario requires stopping discovery or abandoning the spike. Every Critical/High case has an acceptance test and reversible response. The scenario result is therefore **GO_TO_PLANNER with explicit blockers on ADR scoring and later portal cook**, not permission to implement or score now.
