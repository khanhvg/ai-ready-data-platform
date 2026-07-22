# Web and repository inventory

## Discovery result

Planning may proceed with two independent gates:

1. **Preview gate — open:** a safe, static, fixture-labelled, unscored `learn-preview` may be planned and implemented wholly under issue #7 ownership before issue #6 merges. It must remain runnable, must not call a runner, and must have no completing state.
2. **Decision gate — closed:** candidate scoring, a winner, and ADR-005 decision evidence must wait for issue #6’s tracked `promotion-trust-v1` fixture and shared schemas. All three candidates must then rerun against the same merged fixture bytes.

No framework is selected in discovery. Current official guidance shows all three candidates remain feasible, but each has a distinct risk that must be tested rather than argued away.

## Immutable state and drift gate

| Check | Observed value | Result |
|---|---|---|
| Worktree | `/Users/khanhvg/Documents/work/ai-ready-data-platform-issue-7` | Correct |
| Branch | `plan/issue-7-web-stack-representative-lesson` | Correct |
| Local HEAD | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Exact input |
| Tracking ref | `origin/integration/issue-5-local-learning` at `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Exact input |
| Live remote integration ref | `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` | Exact input |
| Master audit commit | `e440c5855732d5d8f5d634e3cc1359c010cc5ed3` | Present and ancestor of input |
| Initial worktree | Clean | Passed |

The current plan branch did not exist remotely at preflight; publication will create it without changing the integration branch.

## Repository capability inventory

### Present and usable read-only

- Four current mart implementations and serving definitions:
  - `transform/dbt/models/marts/mart_promotion_effectiveness.sql`: one row per `promo_name, channel` for completed orders.
  - `transform/dbt/models/marts/mart_fulfillment_performance.sql`: one row per `carrier, region`.
  - `transform/dbt/models/marts/mart_returns_analysis.sql`: one row per `return_reason, category, region` after the mart’s category selection rule.
  - `transform/dbt/models/marts/mart_data_quality.sql`: global controlled scenario/count rows.
- Existing Rill measures preserve weighted calculations, including `SUM(net_revenue)/SUM(order_count)`, `SUM(discount_amount)/SUM(gross_revenue)`, shipment-weighted on-time performance, delivered-shipment lead-time weighting, and return-count-weighted average refund.
- Existing local data, dbt, Rill, Airflow, and verification documentation establishes the current product context but provides no web lesson shell.
- The full audited issue #5 planning corpus is present under `plans/260721-005-enterprise-learning-sandbox/` and is binding.

### Absent and dependency-owned

At the input SHA, none of the following issue #6 outputs exists:

- `contracts/data/retail-golden-v1.json`
- `contracts/data/promotion-trust-v1.yaml`
- `tests/fixtures/learning/promotion-trust/evidence-v1.json`
- `tests/fixtures/learning/promotion-trust/manifest.json`

There is also no `spikes/web/**`, scorecard, ADR-005 proposal, or I5-02 make fragment. Consequently:

- hardcoded surrogate “real” fixture data is forbidden;
- a preview may use a small synthetic static fixture only when every screen and artifact labels it as non-scoring fixture data;
- an unavailable/mismatched real fixture is an environmental failure, never the controlled lesson failure;
- scoring and ADR advancement are blocked until the actual issue #6 merge SHA and fixture hash are recorded.

## Exact path ownership

Issue #7 discovery establishes the following implementation boundary from the user instruction plus the binding master plan.

| Path | Authority | Discovery disposition |
|---|---|---|
| `spikes/web/**` | Issue #7 | Allowed implementation area for shared candidate harness, preview, all candidates, evidence, and non-copy inventory. |
| `docs/decisions/evidence/adr-0005-web-stack-scorecard.md`, `docs/decisions/evidence/adr-0005-web-stack-scorecard.json`, and `docs/decisions/0005-web-stack.md` | Issue #7 | Allowed, but score/winner/accepted ADR evidence must not exist before the issue #6 fixture rerun. A pre-fixture ADR file may only be an unmistakable Proposed shell if the planner finds it useful. |
| `plans/260721-007-web-stack-representative-lesson/**` | Issue #7 phase artifacts | Allowed; ignored by default and may be force-added only at this exact directory. |
| `mk/issue-5/i5-02.mk` | Named by master P2, but not named in the user’s latest “only” list | **Planner must reconcile before implementation.** Do not create it merely from discovery. Root `Makefile` is prohibited either way. This ambiguity does not block the preview design, but it blocks exposing a root `make learn-preview` command until authority is explicit. |
| `.gitignore` | Repository shared configuration; master P2 once anticipated a selected allow-list change, but the latest “only” boundary excludes it | Prohibited for issue #7. Use exact `git add -f` for ignored issue-owned artifacts; do not broaden ignore rules. |
| `contracts/**`, `schemas/**`, `tests/fixtures/learning/**` | Issue #6 / I5-03 | Read-only consumer after merge; issue #7 must not edit. |
| Runner code, runner routes, container privilege | I5-04 | Prohibited. |
| Portal product root/application | I5-05 | Prohibited. |
| Root `Makefile` | Issue #6/shared core | Prohibited. |
| `docs/code-standards.md` | User-owned/protected (currently absent) | Prohibited. |
| Root `release-manifest.json` | Protected release owner; current SHA-256 `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` | Prohibited and must remain byte-identical. |

## Representative journey inventory

### Business question

For a Retail Operations Director or Data Product Owner:

> Can we trust a promotion decision when fulfillment delays, returns/refunds, and controlled data-quality failures may distort the headline performance?

The first journey must not promise causal campaign attribution. It presents four separately grained evidence cards and permits `insufficient evidence` as the correct `promotion-trust-v1` conclusion.

### Ten acts, with preview semantics

| Act | Learner intent | Preview behavior before issue #6 |
|---|---|---|
| 1 | Frame the decision, stakeholder, capability, and success threshold. | Static narrative plus novice prerequisite probes. |
| 2 | Inspect system context and the promotion-oriented dynamic view. | Project-owned static diagram/table; reversible disclosure. |
| 3 | Run bounded generator/load/dbt/export. | Explicitly labelled simulation; no command or runner call. |
| 4 | Observe the naive headline-revenue assessment fail operational/quality assertions. | Controlled failure fixture replay only. |
| 5 | Trace anomalies, lineage, grains, time/filter scope, numerator/denominator, weighted measures, and limitations across four marts. | Four independent evidence cards; no visual join line or combined row. |
| 6 | Compare alternatives and record a bounded decision. | Ephemeral preview choice; cannot be accepted as a product decision. |
| 7 | Reset the workspace and prove base/golden assets unchanged. | Reset the preview state and show a simulated integrity explanation. |
| 8 | Apply lesson-owned typed decision configuration in a fresh workspace. | Display schema-shaped example; do not write shared contract/config. |
| 9 | Verify query, metric, quality rules, and evidence; optionally replay. | Fixture-only verifier explanation and evidence view; state remains non-completing. |
| 10 | Reflect on trade-offs and AWS evolution without cloud activity. | Reflection prompt; no completion mutation or cloud call. |

### Evidence bundle, not a composite

| Mart | Grain | Required disclosure | Forbidden inference |
|---|---|---|---|
| Promotion effectiveness | `promo_name, channel` | filters/time scope, order count, gross/discount/net, weighted AOV and discount ratio | A carrier, return, or DQ event was caused by or belongs to a promotion. |
| Fulfillment performance | `carrier, region` | shipment denominator, on-time numerator/rate, in-transit exclusion/lead-time rules | A specific promotion caused delivery delay. |
| Returns analysis | `return_reason, category, region` | return count, refund numerator/denominator, category selection/limitations | A specific promotion caused a return or refund. |
| Data quality | global scenario/count | scenario identity, controlled-vs-environmental type, affected scope | A global DQ scenario belongs to a specific promotion. |

The UI may align cards by question and evidence type. It must not join or visually imply a row-level causal path. `insufficient evidence` must remain a normal result, with an explicit statement of what common-grain data would be required for causal analysis later.

## Interaction reference inventory

The allowed learning is at the interaction-principle level:

- one concrete narrative with a clear start and end;
- progressive disclosure paced by the learner;
- a persistent state/evidence summary that does not become the only navigation mechanism;
- reversible navigation and motion;
- inline definitions/evidence at the moment of need, with optional deeper links;
- discrete state and time labels rather than position-only meaning.

This phase’s in-app browser probe found no available browser instance. Current public page text was reachable, while the binding master discovery records an earlier clean-browser observation. Neither permits copying. Candidate acceptance therefore requires:

- a project-owned non-copy inventory naming every external principle and the independent project expression;
- no copied prose, assets, layout, styling, colors, timing, or implementation;
- fresh candidate interaction screenshots/traces and reviewer attestation before ADR scoring.

## Candidate feasibility inventory

### Astro + React islands

Current official guidance aligns well with a static, content-heavy route: Astro emits HTML by default and hydrates only explicitly directed islands. Content collections offer schema validation, and MDX maps authored components. The spike must prove:

- the lab controls form the smallest practical React island boundary;
- state survives committed back/reload navigation without making the whole lesson an island;
- Astro/React child parsing and MDX optimization do not corrupt authored lesson content;
- a future typed BFF remains a clean same-origin adapter seam;
- static output and, if evaluated, Node-adapter output are clearly distinguished.

### Next.js App Router

Server Components default to low-client-JS content, with Client Components for lab state. App Router route handlers can host a same-origin BFF, while static export removes many request-time capabilities. The spike must freeze one declared deployment mode before timing and prove:

- a narrow `use client` boundary rather than accidentally client-bundling the lesson tree;
- deterministic MDX content-schema/frontmatter validation despite `@next/mdx` not supplying it by default;
- static/reduced-motion output without hiding facts behind hydration;
- whether self-hosted standalone runtime/caching/version-skew complexity is justified;
- CSP choice does not silently force dynamic rendering and invalidate static/resource claims.

### React/Vite + typed API

Vite supplies a direct client build and explicit backend integration, but not a content model or production server. The spike must prove:

- a real semantic pre-rendered/static lesson artifact when JavaScript is disabled, not an empty SPA mount point;
- MDX and schema validation assembled with no candidate-specific contract fork;
- the typed API adapter cannot leak `VITE_*` credentials and never reaches a runner directly;
- the measured server is a declared production-like static host/BFF, not `vite preview`;
- the extra composition burden remains understandable within the 3-hour candidate cap.

## Security inventory

### Issue #7 posture

- Synthetic static fixture only; no secrets, personal data, raw logs, absolute user paths, credentials, cookies, or tokens.
- Trusted project-owned MDX compiled at build time only. No runtime `evaluate`, remote MDX, fixture-authored JSX, or learner-authored executable content.
- Browser network allow-list for preview is empty except its own static assets and optional same-origin non-mutating fixture replay. No browser-to-runner or browser-to-cloud call.
- No privileged runner, Docker socket, subprocess execution, or host mutation.
- Dependency locks, clean installs, lifecycle-script inventory, advisory/signature review, license inventory, and content security policy are candidate evidence.

### Future contract, not implementation authority

The candidate seam must remain compatible with a later portal BFF that enforces exact loopback Host and Origin allowlists, a high-entropy launch secret exchanged for an HttpOnly/SameSite session, CSRF protection for mutations, DNS-rebinding/cross-origin negative tests, and preferably a Unix-domain-socket runner boundary. No candidate may implement, weaken, or bypass those controls in issue #7.

## Deployment and rollback inventory

- Local preview: bind loopback explicitly, choose a collision-safe port, expose a non-mutating readiness probe, cleanly terminate child processes, and work without AWS/model credentials.
- Static candidates: produce immutable, content-hashed assets and an independently runnable retained preview; rollback means serve the prior complete artifact set.
- Node candidates: record signal handling, readiness, host/port configuration, process-tree RSS, and absence of local mutable state. Later ECS deployment would use a versioned image/task definition and health-gated rollback.
- No candidate receives points for cloud provisioning. ECS evidence is a documented compatibility/rollback analysis plus reproducible local build/start behavior.
- The later deployment owner must preserve the browser/BFF/runner contract even if static hosting and application runtime are separate tasks.

## Critical/high discovery findings

| ID | Severity | Finding | Acceptance evidence | Rollback/removal | Dependency | Boundary blocked if unresolved |
|---|---|---|---|---|---|---|
| WD-C01 | Critical | Scoring before the issue #6 tracked fixture would create false ADR evidence. | Recorded issue #6 merge SHA, fixture SHA-256, schema validation, and all-candidate rerun IDs. | Delete all provisional measurements/scores; keep only clearly unscored preview observations. | Issue #6. | ADR scoring; later portal cook. Preview is not blocked. |
| WD-C02 | Critical | Joining incompatible mart grains can manufacture promotion causality. | Four independent cards, grain/time/filter/numerator/denominator/weighting/limitations assertions, and explicit insufficient-evidence test. | Remove composite dataset/chart and score evidence; revert to evidence bundle. | Existing marts; issue #6 contract. | Preview content, ADR scoring, later portal cook. |
| WD-C03 | Critical | A preview that calls a runner or reaches `completed` forges release/completion authority. | Zero mutation/runner requests, fixture label on every state, state-machine test proving no `completed` transition. | Disable/remove offending route/control and return to static replay. | Master lesson contract; I5-04/I5-05 later. | Preview, ADR scoring, later portal cook. |
| WD-C04 | Critical | Executable/untrusted MDX or browser credentials creates a code/secret boundary breach. | Project-owned build-time MDX only, environment/bundle scan, CSP test, empty preview network allow-list. | Remove remote/runtime MDX and credential path; regenerate safe static fixture and bundles. | Framework/MDX toolchain; future I5-04 boundary. | Preview, ADR scoring, later portal cook. |
| WD-H01 | High | Candidate-specific contracts/tests make the score incomparable. | One neutral fixture adapter, one state-transition table, identical E2E IDs and commands, no shared-contract edits. | Discard candidate-specific workaround and rerun; eliminate at cap if still red. | Issue #6 schema; common harness. | ADR scoring. |
| WD-H02 | High | State rail, animation, or scroll can hide facts/controls and fail keyboard, screen reader, 200% zoom, reduced motion, or no-JS use. | Automated semantics/axe plus manual keyboard, named screen-reader, 200% reflow, reduced-motion, no-JS, focus, and no-scroll completion evidence. | Remove/flatten animation and sticky rail; retain semantic static sequence. | Fresh browser available; WCAG evidence. | ADR scoring and later portal cook; preview review may proceed but cannot pass acceptance. |
| WD-H03 | High | Cold/warm/RSS/JS results can be biased by cache, process-tree, mode, or candidate order. | Frozen environment record, declared runtime mode, rotated measurement order, raw samples, process-tree RSS, emitted bundle manifest. | Invalidate biased samples and rerun all candidates equally; no partial score. | Common measurement harness; issue #6 rerun. | ADR scoring. |
| WD-H04 | High | Timebox drift or synthetic scoring can force an unsupported winner. | Timestamped 3+3+3+3+2 budget, 90-minute/3-hour kill logs, eliminated candidates unscored, explicit no-winner outcome. | Stop at 14 hours; keep ADR Proposed and retained neutral preview; request requirement narrowing/new authority. | Planner protocol. | ADR scoring and later portal cook. |
| WD-H05 | High | Development servers or undeclared runtime topology produce invalid local/ECS/rollback evidence. | Production-like local start command, readiness/signal/RSS evidence, immutable artifact/image plan, rollback test description. | Remove deployment points and artefacts; revert to retained static preview. | Later deployment owner; no cloud in issue #7. | ADR scoring and later portal cook. |
| WD-H06 | High | Dependency/CSP differences can hide supply-chain risk or invalidate static performance claims. | Per-candidate lock, clean install, lifecycle/provenance/advisory/license inventory, exact CSP headers/meta and bundle test. | Remove suspect dependency or eliminate candidate; rerun after lock change. | Package registries/current tooling. | Preview if exploitable; otherwise ADR scoring/later portal cook. |
| WD-H07 | High | The latest path boundary conflicts with the master’s anticipated `mk/issue-5/i5-02.mk` and `.gitignore` changes. | Planner records explicit authority before creating the fragment; `.gitignore` stays unchanged; changed-path test excludes root/protected/shared paths. | Remove the fragment/command exposure if not authorized; retain preview executable directly under `spikes/web/**`; force-add only exact ignored artifacts. | User decision/master reconciliation. | Root make exposure; not preview design or candidate research. |
| WD-H08 | High | No browser instance was available for fresh interaction observation in discovery. | Fresh browser interaction capture for every candidate, normalized screenshots/traces, manual a11y record, non-copy review. | Withhold score/winner/ADR; retain unscored static preview and source. | Browser-capable scoring environment. | ADR scoring. Preview/planner handoff not blocked. |
| WD-H09 | High | Copying the reference would create legal/design integrity risk and contaminate the comparison. | Non-copy inventory and reviewer attestation; independent content/layout/style/source review. | Remove derivative content/assets/style and rebuild project-owned expression. | Project review. | Preview publication and ADR scoring. |
| WD-H10 | High | Novices can misread controlled failure, weighted measures, or grain and “succeed” by guessing. | Prerequisite probes, deterministic three-level hints, reflection/evidence explanation, assistive-technology labels, attempt/replay tests. | Simplify narrative/probes and remove misleading interaction; do not lower verifier semantics. | Lesson contract/fixture vocabulary. | Preview acceptance, ADR scoring, later portal cook. |

## Discovery conclusion

The evidence supports `GO_TO_PLANNER`, not framework selection. The planner must build a two-barrier execution plan, preserve the no-winner path, resolve the make-fragment authority before exposing root commands, and make issue #6 plus fresh browser evidence explicit ADR-scoring blockers.
