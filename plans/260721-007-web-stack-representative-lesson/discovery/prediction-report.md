# Prediction report

## Executive summary

**Prediction verdict: CAUTION. Discovery disposition: GO_TO_PLANNER.**

The proposed two-barrier spike can produce a defensible stack decision within 14 hours, but only if the planner treats the preview and the ADR experiment as different releases of evidence. The unscored neutral preview is feasible now. Candidate scores and ADR-005 are not: they depend on issue #6’s tracked real fixture and fresh browser/accessibility evidence.

Across five independent perspectives, the strongest agreement is that framework choice is not the first-order risk. The first-order risks are evidence validity, incompatible mart grains, false preview authority, accessibility/static equivalence, and score comparability. Astro has the most naturally aligned static/content architecture, Next has the strongest integrated BFF/evolution story but the most runtime-mode ambiguity, and React/Vite has the clearest explicit API separation but must prove it can deliver a true semantic no-JS content route without accumulating custom framework work.

The report does not select a candidate. “Astro by default” applies only to a fully evidenced tie between must-pass candidates; it is not permission to skip the spike or the issue #6 barrier.

## Proposal under prediction

- Build a framework-neutral static `learn-preview` and shared harness under `spikes/web/**`.
- Spike Astro + React islands, Next.js App Router, and React/Vite + typed API under equal three-hour caps.
- Use one promotion-trust journey and four existing marts without joining their incompatible grains.
- Apply all must-pass criteria before weighted scoring.
- Rerun all candidates against issue #6’s tracked real fixture, then score and propose ADR-005.
- Stop at 14 hours; preserve a runnable neutral preview and return “no winner” when evidence is incomplete.

## Perspective 1 — architecture

### Position

The common lesson contract and browser/BFF seam should be the architecture; the rendering framework should be an adapter. If candidate code owns business semantics, failure classes, or evidence shape, the experiment has already lost comparability.

### Failure modes

| ID | Severity | Prediction | Likelihood | Impact |
|---|---|---|---|---|
| PR-A-C01 | Critical | A UI convenience creates a cross-mart composite that visually or computationally attributes carrier, return, or DQ facts to a promotion. | Medium | False business conclusion and corrupted lesson contract. |
| PR-A-H01 | High | Each framework develops its own state/evidence types or content frontmatter, so tests measure different products. | High | Scorecard is not decision evidence. |
| PR-A-H02 | High | Candidate runtime mode remains implicit: Next is measured as a server, Astro as static, Vite through a dev preview server, and the resource score becomes meaningless. | High | Biased winner and wrong ECS plan. |
| PR-A-H03 | High | Issue #7 edits shared schemas/fixtures or portal/runner boundaries to make a candidate pass. | Medium | Ownership violation and integration conflict. |

### Counter-position

An entirely framework-neutral abstraction can become a miniature framework and consume the spike. The contract should cover only lesson data, state transitions, failure/evidence semantics, and test selectors—not rendering primitives, routing APIs, or component conventions.

### Mitigations and evidence

- Freeze the neutral logical objects and E2E IDs before candidate timers.
- Require four independent evidence cards, with a test rejecting any causal cross-mart relationship.
- Require a one-page declared deployment/runtime mode for every candidate before measurement.
- Enforce the exact changed-path allow-list; shared contracts are read-only after issue #6.
- Keep framework-native rendering inside each candidate and measure the amount of adapter glue.

## Perspective 2 — security

### Position

The preview must be treated as untrusted browser code around trusted static project content. There is no legitimate reason for credentials, runner authority, arbitrary MDX evaluation, cloud access, or host mutation in issue #7.

### Failure modes

| ID | Severity | Prediction | Likelihood | Impact |
|---|---|---|---|---|
| PR-S-C01 | Critical | A browser bundle contains a runner token, `VITE_*` secret, private URL, or direct privileged endpoint. | Low–Medium | Credential exposure and bypass of future BFF controls. |
| PR-S-C02 | Critical | Remote, fixture-authored, or learner-authored MDX/JS is evaluated at runtime. | Low | Build/runtime code execution from content. |
| PR-S-H01 | High | A wildcard host/CORS development setting survives into the proposed private API design. | Medium | DNS-rebinding/cross-origin attack path later. |
| PR-S-H02 | High | Time pressure leads to unlocked dependencies, unreviewed lifecycle scripts, or a CSP choice that invalidates static/runtime assumptions. | High | Supply-chain risk or misleading deployment score. |
| PR-S-H03 | High | Evidence artifacts capture absolute paths, tokens, cookies, headers, or fixture data not safe for publication. | Medium | Secret/privacy leakage in git and GitHub. |

### Counter-position

The issue is static and local, so implementing full session/CSRF/Origin enforcement now would itself violate scope and could create a toy security design that the real runner later has to undo.

### Mitigations and evidence

- Empty preview network authority except its own safe static assets/read-only same-origin replay.
- Project-owned MDX compiled at build time; no `evaluate`, remote MDX, dynamic import from fixture, or unsafe HTML path.
- Browser bundle/trace and credential scan; no runner type/URL/token in client contract.
- Record the future exact Host/Origin/session/CSRF contract as compatibility requirements only.
- Per-candidate lockfiles, clean install, lifecycle/provenance/advisory/license inventory, and explicit CSP evidence.
- Sanitize traces/evidence and scan before commit.

## Perspective 3 — performance

### Position

Performance evidence is decision-grade only when startup, steady-state memory, and client JavaScript refer to the same functional journey, same fixture, same machine, and declared production-like mode.

### Failure modes

| ID | Severity | Prediction | Likelihood | Impact |
|---|---|---|---|---|
| PR-P-H01 | High | Warm package/build caches or fixed candidate order favor the later framework. | High | False relative startup/build result. |
| PR-P-H02 | High | RSS samples omit subprocesses or compare a static host to an integrated server without labeling topology. | High | Wrong local capacity/ECS cost conclusion. |
| PR-P-H03 | High | Bundle totals hide route-level initial JS or count server/source-map bytes as client payload. | Medium | Hydration/runtime choice is mis-scored. |
| PR-P-H04 | High | Visual/browser runs use different OS, font, browser, viewport, or motion settings. | Medium | Noisy diffs masquerade as framework instability. |

### Counter-position

The 14-hour cap cannot support a statistically rich benchmark. More repetitions could optimize noise while missing authoring and accessibility failures.

### Mitigations and evidence

- Separate clean-install/build time from app startup.
- Three cold and three warm starts per candidate, rotated order, raw samples plus median/range.
- Sample process-tree RSS at readiness and after the full journey; label static host versus application server.
- Record emitted client asset manifests and route-level browser transfer.
- Pin the browser/OS/font/viewport environment for visual comparison.
- Treat the values as bounded comparative spike evidence, not production capacity promises.

## Perspective 4 — end user and accessibility

### Position

The representative learner is a technically curious architecture/data practitioner who may not yet understand mart grain, weighted measures, or controlled failure. The lesson succeeds when the learner can explain why the evidence is insufficient—not when the animation ends or all cards have been visited.

### Failure modes

| ID | Severity | Prediction | Likelihood | Impact |
|---|---|---|---|---|
| PR-U-C01 | Critical | Scroll position, animation completion, or local state is treated as lesson completion/evidence. | Medium | Forged learning outcome and inaccessible flow. |
| PR-U-H01 | High | A sticky evidence rail covers content/focus at 200% zoom or becomes the only navigation mechanism. | High | Keyboard/low-vision learner cannot complete the review sequence. |
| PR-U-H02 | High | Reduced-motion or no-JS mode removes evidence, facts, or controls rather than motion/interactivity only. | Medium–High | Essential content is inaccessible. |
| PR-U-H03 | High | Controlled and environmental failures use similar styling/copy, so novices debug a missing fixture as if it were the lesson. | High | Confusion, unsafe troubleshooting habits, invalid score. |
| PR-U-H04 | High | Prerequisite probes become hidden grading, while hints disclose an answer without teaching grain/weighting. | Medium | Novices either churn or guess; reflection is meaningless. |
| PR-U-H05 | High | Interaction principles from the reference become copied visual/narrative expression. | Medium | Non-copy failure and project identity loss. |

### Counter-position

A completely linear, static fallback is not required to reproduce every lab manipulation. It must preserve all facts, limitations, evidence, state labels, and an understandable review path; enhanced reversible controls can remain progressive enhancement.

### Mitigations and evidence

- No `completed` state in preview; explicit controls, never scrolling, commit navigation.
- State rail reflows into an in-document summary; logical focus and skip/landmark paths.
- Same semantic content before hydration, with reduced-motion and JavaScript-off projects.
- Separate failure codes, copy, recovery, status roles, and evidence.
- Three unscored prerequisite probes and a deterministic orient/connect/explain hint ladder.
- Manual keyboard, named screen-reader, 200% zoom/reflow, and current browser traces in addition to axe.
- Project-owned non-copy inventory/reviewer attestation.

## Perspective 5 — operations and delivery

### Position

The spike must finish with a reproducible evidence package and an honest no-winner path. Retaining source and a neutral executable preview is more valuable than manufacturing a decision at hour 14.

### Failure modes

| ID | Severity | Prediction | Likelihood | Impact |
|---|---|---|---|---|
| PR-O-C01 | Critical | Provisional synthetic-fixture results are renamed as tracked-fixture scores or ADR evidence. | Medium | Irreproducible architecture decision and issue #6 bypass. |
| PR-O-H01 | High | A killed candidate receives a synthetic/partial score so a ranking can be published. | Medium | Must-pass policy defeated. |
| PR-O-H02 | High | All candidate sources are deleted immediately after choosing, losing contract and audit evidence. | Medium | Winner cannot be challenged/reproduced. |
| PR-O-H03 | High | `vite preview`, an ad hoc dev server, or local mutable cache is treated as ECS readiness/rollback proof. | High | Deployment failure and invalid rollback plan. |
| PR-O-H04 | High | The implementation creates the master-named make fragment despite the latest narrower path instruction, or touches `.gitignore`, root Makefile, or release manifest. | Medium | Authority violation and integration conflict. |
| PR-O-H05 | High | Browser infrastructure remains unavailable and the team scores from unit tests/screenshots alone. | Medium | Accessibility and interaction claims are unaudited. |

### Counter-position

Retaining every installed dependency/build output is wasteful. The binding requirement is to retain candidate source, lockfiles, commands, hashes, raw evidence, and reproducible bundles through I5-05—not `node_modules` or transient build caches.

### Mitigations and evidence

- Hard Barrier B gate on issue #6 merge SHA and fixture digest; invalidate every provisional sample.
- Eliminated candidate is `ELIMINATED`, never numerically scored.
- Preserve all sources/evidence through I5-05; keep losers out of product build. Later cleanup requires a retained source bundle/hash.
- Local production-like commands, readiness/signal/RSS evidence, immutable artifact description, and ECS rollback mapping; no cloud action.
- Planner must explicitly reconcile `mk/issue-5/i5-02.mk` authority; changed-path checks protect root/shared paths.
- Browser/a11y evidence is a scoring blocker and produces no-winner when unavailable.

## Agreements across perspectives

1. **The issue #6 fixture is a hard evidence barrier.** Architecture, operations, security, and user correctness all depend on its exact contract and bytes.
2. **The four marts are an evidence bundle, not a join.** `insufficient evidence` is an intended result, not a failure to make the lesson exciting.
3. **Preview authority must be visibly weaker.** Fixture-labelled, unscored, no runner, no completion, no release claim.
4. **The common contract is necessary but must remain narrow.** Share data/state/failure/evidence/test semantics, not rendering APIs.
5. **Accessibility is a must-pass, not a weighted trade.** A candidate cannot compensate for hidden facts or broken keyboard/zoom/reduced-motion behavior with better performance.
6. **Raw evidence and no-winner behavior are mandatory.** Partial scores, mixed fixtures, or inaccessible browser evidence cannot be averaged into validity.
7. **Deployment is compatibility evidence, not a cloud task.** Local production-like runtime, immutable output, readiness/shutdown, and rollback mapping are sufficient for issue #7.

## Conflicts and resolution rules

| Conflict | Resolution for planner |
|---|---|
| A broad neutral abstraction improves comparability but consumes the spike. | Share only manifest/state/failure/evidence/client interface and tests. Framework-native rendering/routing remains candidate-owned and measurable. |
| Next integrated runtime offers a realistic BFF, but static candidates naturally report lower RSS. | Freeze and label topology; score both actual resource cost and hosted evolution. Do not normalize away a real server, and do not pretend a static host includes a BFF. |
| Static fallback cannot reproduce every interactive manipulation. | Require all facts, limitations, state/evidence labels, and a linear review path; progressive lab controls may enhance but never become the only source of truth. |
| Supply-chain review takes time from feature work. | Lock and inventory are must-pass evidence. Deep remediation may eliminate a candidate; the cap cannot be extended by accepting unsafe dependencies. |
| Master P2 names `mk/issue-5/i5-02.mk`, while the latest instruction says issue #7 owns only spike/report/preview/ADR artifacts. | Planner must obtain/record explicit authority before creating the fragment. Root Makefile remains off-limits. Direct preview execution under `spikes/web/**` preserves progress meanwhile. |
| Astro is the default in a close tie, but discovery suggests it may fit best. | Do not preselect. Default applies only after complete Barrier B evidence and all must-pass checks. |

## Critical/high acceptance mapping

Every critical/high prediction is mapped below. “Blocks” distinguishes the early preview, ADR scoring, and later portal cook.

| Finding(s) | Acceptance evidence | Rollback/removal | Dependency | Blocks if unresolved |
|---|---|---|---|---|
| PR-A-C01 | `WEB-CONTRACT-002/003`, `WEB-TRUST-001/002`; four-card screenshot/DOM and schema tests | Delete composite/join visualization/data and related score; restore evidence cards | Existing marts + issue #6 contract | Preview, ADR scoring, portal cook |
| PR-S-C01, PR-S-C02 | Bundle/network/credential scan; trusted build-time MDX test; CSP and empty-authority preview trace | Remove credential/runner/remote-eval path; regenerate safe fixture/bundle; eliminate candidate if cap exceeded | Candidate toolchain; future I5-04 contract | Preview, ADR scoring, portal cook |
| PR-U-C01 | `WEB-PREVIEW-002`, `WEB-STATE-001/002`, `WEB-NOSCROLL-001`; no completing state in schema/DOM/events | Remove completion path and scroll/motion commit; return to neutral static preview | Master lesson contract; I5-05 later | Preview, ADR scoring, portal cook |
| PR-O-C01 | Issue #6 merge SHA/fixture digest; clean all-candidate rerun IDs; synthetic artifacts carry unscored labels | Delete provisional scores/ADR evidence and rerun; keep neutral preview | Issue #6 | ADR scoring, portal cook; not preview |
| PR-A-H01, PR-A-H03 | Same contract/tests/digests; changed-path allow-list; no shared path modifications | Remove candidate-specific fork/shared edit, reset candidate, eliminate at cap | Common harness + issue #6 | ADR scoring; shared edit also blocks publication |
| PR-A-H02, PR-O-H03 | Declared production mode, exact start/readiness/shutdown/RSS, immutable output and ECS mapping | Invalidate resource/deployment score; revert executable surface to neutral preview | Common measurement harness; later deployment owner | ADR scoring, portal cook |
| PR-S-H01 | Future-boundary compatibility assertions; no wildcard CORS/runner URL in source/bundle | Remove insecure API assumption; candidate cannot advance if contract requires it | I5-04/I5-05 future | ADR scoring, portal cook |
| PR-S-H02 | Lock/clean install, lifecycle/signature/advisory/license record, CSP/static-mode test | Remove suspect dependency/CSP, rerun or eliminate candidate | Registries/toolchain | Preview if exploitable; otherwise ADR/portal |
| PR-S-H03 | High-confidence credential scan and sanitized trace/evidence schema | Purge uncommitted artifact, regenerate sanitized evidence; rotate actual secret if ever exposed | Evidence harness | Publication/ADR; portal evidence later |
| PR-P-H01, PR-P-H02, PR-P-H03, PR-P-H04 | Frozen environment, rotated raw samples, process-tree RSS, bundle manifest, normalized browser evidence | Invalidate affected category/all candidate results and rerun equally | Browser/measurement environment + issue #6 | ADR scoring |
| PR-U-H01, PR-U-H02 | `WEB-A11Y-001..004`, `WEB-STATIC-001`; manual keyboard/screen-reader/200% evidence | Flatten/remove sticky/motion UI; retain semantic static sequence | Browser/AT environment | Preview acceptance, ADR, portal |
| PR-U-H03, PR-U-H04 | Failure-code tests, prerequisite probes, hint-ladder E2E and novice review | Rewrite/simplify explanations without weakening verifier; replay review | Lesson contract and fixture vocabulary | Preview acceptance, ADR, portal |
| PR-U-H05 | Non-copy inventory, fresh screenshots/source review, reviewer attestation | Remove derivative prose/assets/layout/style/source and rebuild independently | Project review | Preview publication, ADR |
| PR-O-H01 | Kill log and scorecard schema rejecting numeric score for failed must-pass | Delete partial/synthetic score; keep `ELIMINATED` | Timer/must-pass harness | ADR, portal |
| PR-O-H02 | Retention inventory and source-bundle hashes through I5-05 | Restore source from retained bundle; stop cleanup until reproducible | I5-05 merge/cleanup authority | Portal cook/reproducibility |
| PR-O-H04 | Explicit path-authority record and changed-path check | Remove unauthorized make/protected/shared change; run preview directly inside spike | User/master reconciliation | Make command publication; not preview design |
| PR-O-H05 | Fresh current candidate browser traces/screenshots and manual AT records | Withhold score/winner/ADR; retain preview and source | Browser-capable environment | ADR, portal; not preview/planning |

## Recommended controls before implementation

1. Planner records Barrier A and Barrier B as separate phases with separate acceptance and rollback.
2. Planner freezes one common contract/test ID list, candidate runtime modes, score anchors, timers, and measurement environment.
3. Planner adds an explicit waiting gate for issue #6 merge SHA and fixture digest before clean rerun/scoring.
4. Planner reserves browser-capable/manual accessibility review before scorecard completion.
5. Planner resolves only the `mk/issue-5/i5-02.mk` path ambiguity; no other implementation choice requires user escalation at discovery.
6. Planner encodes 90-minute, three-hour, and total 14-hour stop behavior plus an explicit no-winner output.
7. Planner keeps the retained neutral preview and losing-source retention/removal contract independent from the winning framework.

## Final prediction verdict

**CAUTION:** no critical issue makes the spike inherently unworkable, and every critical/high prediction has a concrete evidence and rollback path. Planning should proceed, but implementation must not score or select until issue #6 and fresh browser evidence are available.
