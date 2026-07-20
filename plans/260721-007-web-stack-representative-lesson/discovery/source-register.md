# Source register

Date accessed: 2026-07-21 (Asia/Ho_Chi_Minh)

This discovery was performed from immutable integration input `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`. The binding master readiness-audit commit is `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`. External framework guidance is volatile; the planner and spike runner must re-check it when package versions are frozen.

## GitHub authority

| ID | Source | Use |
|---|---|---|
| GH-05 | [Issue #5](https://github.com/khanhvg/ai-ready-data-platform/issues/5) and its 11 comments through [the readiness-audit publication](https://github.com/khanhvg/ai-ready-data-platform/issues/5#issuecomment-5027154466) | Epic authority, audit history, and implementation split. |
| GH-06 | [Issue #6](https://github.com/khanhvg/ai-ready-data-platform/issues/6) and its [pre-plan discovery comment](https://github.com/khanhvg/ai-ready-data-platform/issues/6#issuecomment-5027187045) | Tracked fixture and shared-contract dependency. Issue is open and remains `triaged`; its required fixture files are absent at the input SHA. |
| GH-07 | [Issue #7](https://github.com/khanhvg/ai-ready-data-platform/issues/7), [audited body publication](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5027145392), and [pre-plan phase comment](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5027187266) | Direct scope, timebox, acceptance, labels, and publication requirements. |

## Binding repository sources

All paths below are read at integration SHA `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c` unless a different commit is stated.

| ID | Path or commit | Blob SHA / role |
|---|---|---|
| R-README | [README.md](../../../README.md) | Blob `a600847c8f2685b4d65b9c3be0c1aa80a226ae34`; repository entry points and current local workflow. |
| R-MASTER | [Master plan](../../260721-005-enterprise-learning-sandbox/plan.md) | Blob `365184b9d06018c01324488daca7dfc7ed3decc3`; binding phase/dependency contract. |
| R-P2 | [Phase 2](../../260721-005-enterprise-learning-sandbox/phase-02-representative-lesson-and-web-stack-spike.md) | Blob `5dc343da3f8f36fc9b5a4c158cd5611726520db3`; I5-02 acceptance and spike protocol. |
| R-AUTH | [Execution authority and release contract](../../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md) | Blob `b2ed27959dad6ee4c163e9e73911e88964fbb541`; path ownership and release authority. |
| R-LESSON | [Lesson/lab contract](../../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md) | Blob `10771b400c2f376f9f3a00835d2a408454fdf3d0`; journey, state, evidence, and failure semantics. |
| R-ADR | [Architecture decisions](../../260721-005-enterprise-learning-sandbox/architecture-decisions.md) | Blob `a2ade9cce9eadc23cabe5f60f86c6282535d16e6`; proposed ADR-005 rubric and tie behavior. |
| R-GRAPH | [Implementation issue graph](../../260721-005-enterprise-learning-sandbox/implementation-issue-graph.md) | I5-01 through I5-05 ownership and handoff graph. |
| R-TRACE | [Requirements traceability](../../260721-005-enterprise-learning-sandbox/requirements-traceability.md) | P2 traceability and release-proof obligations. |
| R-DISC | [Master discovery handoff](../../260721-005-enterprise-learning-sandbox/discovery/planner-handoff.md) and adjacent discovery artifacts | Prior discovery constraints and risks; not a substitute for issue #7 scoring evidence. |
| R-VAL | [Initial validation](../../260721-005-enterprise-learning-sandbox/validation/initial-validation-report.md) | Validation finding that fresh browser observation was unavailable in the master validation environment. |
| R-RED | [Red-team report](../../260721-005-enterprise-learning-sandbox/validation/red-team-report.md) | Cross-grain inference, preview, evidence, and authority attacks. |
| R-AUDIT | [Readiness audit](../../260721-005-enterprise-learning-sandbox/audit/readiness-audit-report.md) | Blob `d0d5f0bad31fe7a3ad701bbbe157e85c00a2c0d8`, introduced by commit `e440c5855732d5d8f5d634e3cc1359c010cc5ed3`; binding audit disposition. |

## Current data-product sources

| ID | Path | Blob SHA / observation |
|---|---|---|
| D-PROMO | [Promotion mart SQL](../../../transform/dbt/models/marts/mart_promotion_effectiveness.sql) | `b1cfcb8966edad37365c1367584c650e949cfe82`; completed orders at `promo_name, channel`, with order, gross, discount, net, average-order-value, and discount measures. |
| D-FULFILL | [Fulfillment mart SQL](../../../transform/dbt/models/marts/mart_fulfillment_performance.sql) | `8242b48f74659a4cace331b74fd896a5f908fd78`; carrier/region shipment outcomes. |
| D-RETURN | [Returns mart SQL](../../../transform/dbt/models/marts/mart_returns_analysis.sql) | `1ac1f6c8f4666dc73b19e98dc8d3927746273c44`; return reason/category/region refund outcomes. |
| D-DQ | [Data-quality mart SQL](../../../transform/dbt/models/marts/mart_data_quality.sql) | `fb1d123e138f6252c86d0fc143b382f7bece044c`; global controlled scenario/count evidence. |
| D-RILL | [Serving models and metrics](../../../serving/rill/) | Existing promotion, fulfillment, and return measure definitions establish weighted numerator/denominator behavior. |
| D-ASSETS | [Curated asset registry](../../../lake/curated_assets.json) | Existing mart registration; the four lesson marts already exist. |

The required future files `contracts/data/retail-golden-v1.json`, `contracts/data/promotion-trust-v1.yaml`, `tests/fixtures/learning/promotion-trust/evidence-v1.json`, and `tests/fixtures/learning/promotion-trust/manifest.json` do not exist at the input SHA. Their names and authority come from GH-06 and the binding master artifacts, not from a local file observed in this phase.

## Current official web-stack guidance

| ID | Primary source | Decision-relevant guidance |
|---|---|---|
| A-ISLANDS | [Astro islands](https://docs.astro.build/en/concepts/islands/) | Static HTML is the default; explicitly directed islands hydrate independently. Candidate evidence must show that only lab controls hydrate. |
| A-REACT | [Astro React integration](https://docs.astro.build/en/guides/integrations-guide/react/) | React rendering/hydration integration; Astro-to-React children have a documented parsing caveat unless the experimental option is used. |
| A-MDX | [Astro MDX](https://docs.astro.build/en/guides/integrations-guide/mdx/) | MDX component mapping and build optimization constraints. |
| A-CONTENT | [Astro content collections](https://docs.astro.build/en/guides/content-collections/) | Zod-backed collection schemas validate content data and can generate editor schemas. |
| A-ENDPOINT | [Astro endpoints](https://docs.astro.build/en/guides/endpoints/) and [on-demand rendering](https://docs.astro.build/en/guides/on-demand-rendering/) | Static endpoints build files; request-time APIs require server rendering. |
| A-NODE | [Astro Node adapter](https://docs.astro.build/en/guides/integrations-guide/node/) | Standalone/middleware Node modes and host/port/CSP implications for a later BFF or ECS runtime. |
| N-APP | [Next.js App Router](https://nextjs.org/docs/app) | Current App Router authority. |
| N-MDX | [Next.js MDX guide](https://nextjs.org/docs/app/guides/mdx) | Local/remote MDX support; `@next/mdx` does not supply frontmatter semantics by default. |
| N-BOUNDARY | [Next.js Server and Client Components](https://nextjs.org/docs/app/getting-started/server-and-client-components) | Server components are default; the `use client` boundary pulls its dependency subtree into the client bundle and should be kept small. |
| N-ROUTES | [Next.js Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers) | Web Request/Response BFF surface available inside App Router. |
| N-EXPORT | [Next.js static exports](https://nextjs.org/docs/app/guides/static-exports) | Static export has explicit unsupported request-time features; candidate mode must be declared before timing. |
| N-SELF | [Next.js self-hosting](https://nextjs.org/docs/app/guides/self-hosting), [standalone output](https://nextjs.org/docs/app/api-reference/config/next-config-js/output), and [deployment](https://nextjs.org/docs/app/getting-started/deploying) | Reverse proxy, cache/version-skew, graceful shutdown, and minimal server-output considerations for local/ECS evolution. |
| N-CSP | [Next.js CSP guide](https://nextjs.org/docs/app/guides/content-security-policy) | Nonce-based CSP forces dynamic rendering and disables static optimizations; this trade-off must not be hidden in the score. |
| V-DEPLOY | [Vite static deployment](https://vite.dev/guide/static-deploy.html) | The build output is `dist`; `vite preview` is not a production server. |
| V-BACKEND | [Vite backend integration](https://vite.dev/guide/backend-integration.html) | The typed BFF is an explicit separate integration; Vite can emit an asset manifest. |
| V-ENV | [Vite env and mode](https://vite.dev/guide/env-and-mode) | `VITE_*` values are bundled into client code and must never contain secrets. |
| V-CSP | [Vite features/CSP](https://vite.dev/guide/features) | CSP nonce placeholders and asset inlining have security implications; `data:` must not be enabled for scripts. |
| V-SSR | [Vite SSR](https://vite.dev/guide/ssr) and [multi-page build](https://vite.dev/guide/build.html#multi-page-app) | SSR is deliberately low-level; a plain React/Vite candidate must prove a real semantic no-JS artifact, not an empty SPA root. |
| MDX-TRUST | [MDX getting started](https://mdxjs.com/docs/getting-started/) and [`@mdx-js/mdx`](https://mdxjs.com/packages/mdx/) | MDX is executable JavaScript; only trusted project-owned content may be compiled, and runtime evaluation of fixture/user content is forbidden. |

## Accessibility, testing, API, deployment, and supply chain

| ID | Primary source | Decision-relevant guidance |
|---|---|---|
| W-WCAG | [WCAG 2.2](https://www.w3.org/TR/WCAG22/) | Keyboard access, 200% text resize, and reflow are testable acceptance criteria. |
| W-REFLOW | [Understanding Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow) | Fixed or sticky rails can obscure content/focus under zoom; the evidence rail must collapse/reflow safely. |
| W-KEY | [ARIA APG keyboard interface](https://www.w3.org/WAI/ARIA/apg/practices/keyboard-interface/) and [read-me-first](https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/) | Use native semantics first, visible/predictable focus, and complete keyboard behavior. |
| T-EMU | [Playwright emulation](https://playwright.dev/docs/emulation) and [Page API](https://playwright.dev/docs/api/class-page) | Browser projects can exercise viewport, JavaScript-off, offline, and `prefers-reduced-motion`. |
| T-A11Y | [Playwright accessibility testing](https://playwright.dev/docs/accessibility-testing) | Axe catches only some issues; manual keyboard, screen-reader, zoom, and inclusive assessment remain mandatory. |
| T-VISUAL | [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots) and [trace viewer](https://playwright.dev/docs/trace-viewer) | Normalize browser/OS settings for visual evidence and retain failure traces. |
| API-OAS | [OpenAPI Specification](https://spec.openapis.org/oas/) | Current published versions include 3.2.0. The issue #6 schema is the authority; candidates consume generated/validated types without changing it. |
| AWS-ROLL | [ECS deployment circuit breaker](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-circuit-breaker.html) and [rolling update](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/deployment-type-ecs.html) | A later rolling ECS service can fail and roll back to the last completed deployment; image digest consistency and health checks matter. No cloud action belongs to issue #7. |
| NPM-CI | [`npm ci`](https://docs.npmjs.com/cli/commands/npm-ci/) | Frozen, clean install fails when manifest and lock disagree; commit a lockfile per isolated candidate. |
| NPM-SIG | [npm package provenance](https://docs.npmjs.com/viewing-package-provenance/) and [npm audit](https://docs.npmjs.com/cli/audit/) | Signature/provenance verification and advisory review are evidence inputs, not automatic permission to rewrite dependencies. |

## Interaction-reference evidence boundary

| ID | Source | Status and allowed use |
|---|---|---|
| REF-PUBLIC | [200 Milliseconds](https://200ms.thenodebook.com/) | Current public text was reachable on 2026-07-21 and corroborates a single timed narrative, explicit rules, pauses, and deeper-learning links. It is not a browser interaction capture. Do not copy prose, assets, layout, styles, colors, timing, or source. |
| REF-MASTER | [Master discovery source register](../../260721-005-enterprise-learning-sandbox/discovery/source-register.md) and [technology inputs](../../260721-005-enterprise-learning-sandbox/discovery/technology-decision-inputs.md) | Earlier clean-browser observation at master discovery input `d3ce0c...`: single concrete journey, persistent progress/evidence rail, reversible motion, inline explanation, and staged depth. Historical input only. |
| REF-FRESH | In-app browser probe on 2026-07-21 | `agent.browsers.list()` returned no browser; therefore no fresh visual/interactive observation is claimed. Fresh candidate browser evidence blocks ADR scoring, not the unscored preview or planner handoff. |

## Citation policy for implementation planning

- Treat R-MASTER, R-P2, R-AUTH, R-LESSON, R-ADR, R-AUDIT, GH-06, and GH-07 as binding.
- Treat framework pages as current discovery inputs, then pin exact package and Node versions in each spike lockfile and evidence record.
- Treat REF-PUBLIC and REF-MASTER only as interaction principles. The project must maintain its own non-copy inventory and must not inspect or reproduce the reference implementation.
- Do not infer a cross-mart causal join from D-PROMO through D-DQ. The four marts form a decision-evidence bundle with incompatible grains.
