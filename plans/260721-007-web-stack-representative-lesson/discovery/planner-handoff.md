# Planner handoff

## Handoff verdict

`DISCOVERY_VERDICT=GO_TO_PLANNER`

This verdict authorizes planning only. It does not authorize `$ck:plan` in this phase, implementation, candidate scoring, ADR advancement, product/config/data changes, cloud actions, runner work, merge, or label promotion.

## Immutable authority

- Repository: `khanhvg/ai-ready-data-platform`
- Worktree: `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-7`
- Branch: `plan/issue-7-web-stack-representative-lesson`
- Integration input: `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`
- Master audit commit: `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`
- Issue state/labels at discovery: open, `triaged`, `risk:high` retained

The planner must re-run local HEAD, tracking ref, and live remote integration-ref drift checks. If any differs from the input without an explicitly accepted rebase/restart, stop rather than combining evidence bases.

## Reports to consume

1. [Web and repository inventory](web-and-repository-inventory.md)
2. [Prediction report](prediction-report.md)
3. [Scenario report](scenario-report.md)
4. [Scenario results](scenario-results.tsv)
5. [Candidate decision inputs](candidate-decision-inputs.md)
6. [Source register](source-register.md)

These issue #7 artifacts refine, but do not override, the binding issue #5 master plan and audit.

## What discovery established

### Ready to plan now

- A retained, framework-neutral, static `learn-preview` under `spikes/web/**`.
- Safe synthetic fixture projection with a persistent `SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE` label.
- Shared candidate logical contract, state table, test IDs, measurement protocol, non-copy inventory, and equal timer protocol, all under `spikes/web/**`.
- Three isolated candidate spikes with independent lockfiles.
- Novice prerequisite probes and a three-level hint ladder.
- Static/reduced-motion/no-JS/keyboard/screen-reader/200% test design.
- Local production-like startup/RSS/bundle evidence design and written ECS/rollback mapping, without cloud operations.

### Not ready and hard-blocked

- Any candidate numeric score.
- Any winner/tie decision.
- Any ADR-005 decision evidence beyond an explicitly Proposed template.
- Any completion claim or portal product integration.
- Any private/privileged runner integration.

Those remain blocked until issue #6’s tracked fixture/schema outputs merge. ADR scoring also requires fresh browser interaction and manual accessibility evidence; the in-app browser had no available browser instance during this discovery.

## Required plan shape

The implementation plan should have explicit gates rather than a single uninterrupted phase.

### Gate 0 — authority and drift

- Verify exact integration SHA and master audit ancestry.
- Reconcile authority for `mk/issue-5/i5-02.mk`. The master assigns it to P2, but the user’s latest “only” boundary does not name it. Do not edit root `Makefile` or `.gitignore` in either case.
- Freeze allowed changed paths and protected-file hashes.
- Freeze Node/package-manager baseline, candidate versions/modes, common schema adapter, timer format, and test IDs.

### Gate A — common harness and retained preview, cap 3h

- Create only under `spikes/web/**`, `docs/decisions/evidence/adr-0005-web-stack-scorecard.{md,json}`, and `docs/decisions/0005-web-stack.md`, plus explicitly requested phase artifacts. Scorecard/winner evidence remains gated.
- Use safe synthetic data, clearly fixture-labelled at entry, state rail, verify/evidence, and any export.
- No completion state/API, runner, credentials, cloud, product root, or shared contract.
- Implement the first ten-act promotion-trust journey as static/simulated replay.
- Capture early novice, accessibility, non-copy, and narrative feedback without score language.

If the neutral contract cannot stabilize in three hours, stop and return to planning; do not steal candidate time.

### Gate B1 — candidate spikes, cap 3h each

- Astro + React islands.
- Next.js App Router in one predeclared measured mode.
- React/Vite + typed API with a true semantic no-JS artifact and production-like static host.
- Kill each at 90 minutes if clean install, semantic static route, or common-contract consumption fails.
- Kill each at three hours if any must-pass remains red.
- Killed candidates are `ELIMINATED`, with no numeric score.

Candidate implementation can occur before issue #6 only against the synthetic adapter if every result remains provisional/unscored. The decision-grade rerun cannot.

### Gate B2 — issue #6 handoff

Wait for and record:

- issue #6 merge SHA;
- `contracts/data/retail-golden-v1.json` digest;
- `contracts/data/promotion-trust-v1.yaml` digest;
- `tests/fixtures/learning/promotion-trust/evidence-v1.json` digest;
- `tests/fixtures/learning/promotion-trust/manifest.json` digest;
- shared schema validation result.

Consume read-only. If the contract cannot be consumed without a shared edit or candidate-specific workaround, stop and coordinate with issue #6; do not patch around it.

### Gate C — clean real-fixture rerun and decision, cap 2h

- Clean-install/build/start all remaining candidates against the same fixture digest.
- Run identical common contract/E2E/a11y/static/security tests.
- Collect rotated three-sample cold/warm runs, process-tree RSS, client payload/build manifests, authoring/schema task, browser visuals/traces, and dependency/CSP evidence.
- Enforce must-pass before numeric scoring.
- Apply weights and the within-five-point Astro tie default only to complete passing candidates.
- Produce no winner if evidence is incomplete or the 14-hour total expires.

### Gate D — retention and handoff

- Keep all candidate source/locks/commands/hashes/raw evidence through I5-05 merge.
- Keep the neutral executable preview and framework-neutral tests regardless of winner.
- Exclude losing candidates from product build; do not delete source early.
- Later removal needs explicit authority, retained source bundle/hash, and reproducibility proof.

## Exact representative lesson contract

### Decision question

For the Retail Operations Director/Data Product Owner: can a promotion decision be trusted when fulfillment delays, returns/refunds, and controlled DQ failures may distort the headline?

### Evidence rule

The journey must show four evidence cards, never a composite join:

| Mart | Grain | Minimum disclosed calculation/limitation |
|---|---|---|
| Promotion effectiveness | `promo_name, channel` | completed-order filters; order/gross/discount/net; weighted AOV and discount ratio |
| Fulfillment performance | `carrier, region` | shipment/on-time denominator/numerator; in-transit and lead-time rules |
| Returns analysis | `return_reason, category, region` | return/refund count and weighted average; category selection rule |
| Data quality | global scenario/count | controlled scenario identity/count and global scope |

No carrier, return, or DQ symptom may be assigned to a promotion. The verified `promotion-trust-v1` decision is `insufficient evidence` unless a later additive common-grain product is introduced under separate authority.

### Journey order

1. Frame decision/stakeholder/success threshold.
2. Inspect system context and promotion view.
3. Simulate bounded generator/load/dbt/export in preview.
4. Show naive headline assessment fail.
5. Diagnose four marts, grains, scope, filters, weighted measures, lineage, and limitations.
6. Compare evidence-bounded alternatives.
7. Reset and explain base/golden integrity.
8. Show schema-shaped lesson-owned remediation in a fresh simulated workspace.
9. Verify fixture/query/metric/quality/evidence and optionally replay.
10. Reflect on trade-offs and AWS evolution without cloud action.

The enhanced journey is progressive and reversible. The static sequence remains complete and understandable.

## Non-negotiable candidate contract

- One neutral manifest/evidence/state/failure/client model under `spikes/web/**`; mirror shared schemas read-only after issue #6.
- Fixture kind/digest bind state, evidence, scorecard, and ADR input.
- Preview state model contains no `completed`.
- Controlled, environmental, unexpected, and future authorization failures are distinct.
- Scrolling, motion, hover, and mere card visitation do not commit, verify, or complete.
- Explicit navigation preserves committed state after back/forward/reload; transient draft behavior is declared.
- Reset is idempotent; verify/evidence do not complete preview.
- Typed browser client ends at a future same-origin BFF seam; no browser credential/runner URL.
- Trusted project-owned MDX is compiled at build; no remote/runtime evaluation.
- All candidates use identical test IDs and the same test data projection.

## Must-pass and score contract

Must-pass includes journey/state correctness, failure separation, four-grain evidence, insufficient-evidence rule, preview non-completion, no runner/credential, semantic HTML, keyboard, named screen reader, 200% zoom/reflow, reduced motion, no-JS facts/fallback, no-scroll authority, typed API compatibility, content/schema validation, deterministic browser E2E, local startup without AWS/model credentials, dependency/CSP evidence, and non-copy attestation.

Only must-pass candidates receive a score:

- authoring/content schema/MDX: 20;
- accessibility/static/reduced motion: 20;
- lab/evidence/API: 20;
- cold/warm/RSS/JS: 15;
- unit/E2E/visual: 10;
- hosted/ECS evolution/rollback: 10;
- maintenance/dependency/supply chain: 5.

No synthetic score is allowed. A tie within five points defaults to Astro only after every gate and must-pass succeeds. If no candidate wins, ADR-005 stays Proposed and I5-05 is blocked.

## Critical/high planner risk register

This register maps the discovery finding families; the prediction/scenario reports contain the complete individual rows.

| ID | Severity | Planner control | Acceptance evidence | Rollback/removal | Dependency | Preview | ADR scoring | Portal cook |
|---|---|---|---|---|---|---|---|---|
| PH-C01 | Critical | Enforce tracked-fixture Barrier B | Issue #6 merge/digests + clean all-candidate reruns | Delete provisional scores/ADR; rerun | Issue #6 | Open with label | Blocked now | Blocked |
| PH-C02 | Critical | Prohibit cross-grain composite/causality | Four-card schema/DOM/verifier tests; insufficient result | Remove join/chart/conclusion and dependent evidence | Existing marts + issue #6 | Blocks acceptance | Blocks | Blocks |
| PH-C03 | Critical | Preview has no completion or privilege | State schema + network trace + no-completion tests | Remove route/control/state; restore neutral preview | Master contract; I5-04/I5-05 | Blocks | Blocks | Blocks |
| PH-C04 | Critical | Trusted build-time MDX and no client secrets | Negative content tests, CSP/network/bundle scan | Remove unsafe eval/credential and regenerate/eliminate | Toolchain/future security contract | Blocks | Blocks | Blocks |
| PH-H01 | High | One narrow common contract/harness | Identical schema/test IDs/digests; no shared edits | Remove fork/workaround; rerun/eliminate | Issue #6/common harness | Reviewable | Blocks | Blocks |
| PH-H02 | High | Manual + automated a11y/static gate | Keyboard/AT/200%/reduced/no-JS evidence | Flatten rail/motion; keep semantic fallback | Browser/AT environment | Blocks acceptance | Blocks | Blocks |
| PH-H03 | High | Freeze modes and fair raw metrics | Rotated runs, environment, process-tree RSS, bundle manifest | Invalidate and equally rerun; else no winner | Measurement host/issue #6 | Open | Blocks | Decision dependency |
| PH-H04 | High | Enforce 3+3+3+3+2 and no-winner | Timer/kill logs and scorecard rejection of partial score | Stop at 14h; retain preview; ADR Proposed | Planner protocol | Open | Blocks when cap reached | Blocks |
| PH-H05 | High | Production-like local/ECS/rollback evidence only | Start/readiness/signal/RSS/hashes/CSP and ECS mapping | Delete deployment score; revert preview | Later deployment owner | Open | Blocks category/decision | Blocks |
| PH-H06 | High | Lock/supply-chain/CSP review | Clean installs, locks, lifecycle/signature/advisory/license/CSP evidence | Remove dependency/config or eliminate | Registry/toolchain | Blocks if exploitable | Blocks | Blocks |
| PH-H07 | High | Resolve make-fragment authority; keep `.gitignore` unchanged | Explicit authority + changed-path allow-list | Remove fragment/command; execute inside spike; force-add only exact ignored artifacts | User/master reconciliation | Design open | Command blocked | Later command wiring |
| PH-H08 | High | Require fresh browser/non-copy review | Current traces/screenshots/manual AT/non-copy attestation | Withhold score/ADR; remove derivative work | Browser/project reviewer | Preview can run | Blocked now | Blocks |
| PH-H09 | High | Teach novice grain/failure/weighting explicitly | Probes/hints/failure E2E and novice review | Simplify narrative, not verifier | Lesson vocabulary | Blocks acceptance | Blocks | Blocks |
| PH-H10 | High | Sanitize evidence and bind browser state to fixture | Credential scan, tamper tests, digest-bound evidence | Regenerate artifacts/clear state/remove client authority | Evidence harness | Blocks publication | Blocks | Blocks |

## Security handoff

Issue #7 implementation should contain:

- no runner, subprocess, Docker socket, host mount, cloud SDK call, mutation endpoint, or completion service;
- no browser credential, secret-shaped fixture, personal data, raw header/cookie, absolute user path, or source-map environment leakage;
- no remote/untrusted MDX or runtime evaluation;
- locked candidate dependency trees and explicit lifecycle/provenance/advisory/license/CSP evidence;
- loopback-only local preview by default, clean shutdown, collision-safe port, static fixture digest;
- only a typed compatibility seam for the future exact Host/Origin, session, CSRF, DNS-rebinding/cross-origin negative, and Unix-socket-oriented boundary.

If a candidate requires weakening that future boundary, it fails the must-pass; issue #7 must not implement a privileged workaround.

## Deployment/rollback handoff

No cloud action is authorized. Candidate evidence is local and analytical:

- immutable/versioned static and server artifacts;
- production-like local start, readiness, clean signal shutdown, and process-tree RSS;
- no durable state inside the web container/process;
- declared cache/version-skew and CSP/rendering behavior;
- local prior-artifact rollback demonstration;
- mapping to later ECS image digest/task revision/health/circuit-breaker rollback.

Static and runtime topologies can differ, but the scorecard must label them rather than hide their costs or pretend a development server is production.

## Publication and changed-path handoff

The implementation plan must include:

1. Probe `.gitignore`; force-add only the exact issue-owned ignored directory when necessary.
2. Structural Markdown/TSV/schema/test-ID checks and local link validation.
3. `git diff --check`.
4. Changed-path allow-list rejecting shared contracts, runner, portal root, root `Makefile`, `docs/code-standards.md`, and root `release-manifest.json`.
5. Protected-file digest checks.
6. High-confidence credential scan over changed files/artifacts.
7. Commit and push on the issue branch only.
8. Issue #7 comment with input/output SHA, runtime/phase, report/evidence paths, verdict, and blockers.
9. Preserve `triaged` and `risk:high`; do not promote.

## Planner acceptance checklist

- [ ] Two barriers distinguish preview from decision evidence.
- [ ] Issue #6 dependency and all four expected fixture/schema paths are explicit.
- [ ] Exact first journey and four incompatible grains are explicit.
- [ ] `insufficient evidence` is asserted as the expected result.
- [ ] Retained neutral preview is executable and non-completing even on no-winner.
- [ ] Common contract/test IDs and framework-native boundaries are defined.
- [ ] Keyboard, screen reader, 200%, reduced motion, no-JS, and no-scroll checks are named.
- [ ] Controlled/environmental/unexpected failures, reset, verify, evidence, reflection, probes, and hints are planned.
- [ ] Cold/warm/RSS/JS/bundle/authoring/schema/E2E/visual measurements use one declared protocol.
- [ ] 90-minute, per-candidate three-hour, and total 14-hour kills are executable.
- [ ] Must-pass, weights, tie default, and no-winner behavior cannot be bypassed.
- [ ] Candidate retention and later losing-spike removal preserve contract/evidence.
- [ ] No direct browser credential/runner privilege; future boundary remains exact.
- [ ] CSP/dependency/supply-chain and safe fixture evidence are planned.
- [ ] ECS/local behavior and rollback are evidence-only; no cloud work.
- [ ] Exact path authority is enforced and make-fragment ambiguity is resolved before creation.
- [ ] Fresh browser interaction evidence is a hard ADR-scoring gate.

## Planner start condition

The planner may start after verifying this discovery commit against the immutable input lineage. It should pause only for the make-fragment authority decision if root command exposure is required; all other planning can proceed with the constraints above. Candidate scoring must remain explicitly blocked on issue #6 and a browser-capable evidence environment.
