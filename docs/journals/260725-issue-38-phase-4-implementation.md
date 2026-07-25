---
type: journal
date: 2026-07-25
issue: 38
branch: feature/issue-38-phase-4-loopback-web-workflow
status: publication-pending
authority: historical-record
---

# Issue 38 Phase 4 implementation

## Context

Phase 4 began from immutable Phase 3 input
`752830b9f1d90bb71dc82ed56e784eaac63e8c55`. Scope was limited to the
audited local loopback workflow and its real-browser evidence. This historical
record is not product or architecture authority.

## What happened

- Added focused tests first; their genuine RED state was a missing
  `assessment.web` package.
- Added a dependency-injected FastAPI/Jinja2 app factory, explicit-root
  services, loopback-only CLI and Make target, signed local sessions/CSRF,
  Host/Origin/request-size controls, CSP, and local-only assets.
- Added accessible ordinary forms for create/resume, 30 answers, readiness
  facts, attachment-only evidence, deterministic review, architect finding
  disposition, content-pending deep-dive planning, report generation, and
  archive export/preflight/import/reopen.
- Kept routes as orchestration. The Phase 1–3 framework, engine, report,
  archive, and store remain authoritative. Optimistic revision comparison and
  web payload publication run under the engagement writer lock.
- Added a one-worker Playwright journey that starts real servers under two
  different roots, blocks non-loopback network, verifies the full
  no-JavaScript path and enhanced autosave, compares imported state/report
  bytes, writes ignored evidence, and tears down cleanly.

## Verification history

The browser path exposed and corrected real integration defects in sequence:
the pinned browser executable differed from Playwright's optional headless
shell, the macOS sandbox needed local Unix socket access, sandboxed Chromium
sent an opaque `Origin: null` for same-origin form navigation, uploaded files
needed Starlette's concrete type, and a form pattern needed standards-compliant
HTML. The final journey passed with 30 answers, seven gate traces, 12 report
sections, no remote requests or console errors, deterministic distinct-root
import/reopen, and clean teardown.

The final exact-head test counts, review findings, publication references, and
configured-check state belong in the pull request and Issue evidence after
those facts exist.

## Decisions

- Keep the web layer replaceable and dependency-injected; do not duplicate
  scoring, gates, questions, report, or archive rules.
- Require ordinary POST/Redirect/GET completion. JavaScript is enhancement
  only, coordinates the explicit no-rating state, and serializes autosave to
  preserve revision order.
- Accept opaque browser origin only when Fetch Metadata proves a same-origin
  navigation; Host and CSRF checks remain mandatory.
- Treat deep dives as selection/planning records until Phase 7 content exists.
- Preserve generated browser/report artifacts as ignored run evidence, never
  repository content.

## Residual limitations

Catalog content, diagrams, AWS mappings, pipeline evidence, deep-dive execution,
object storage, cloud behavior, deployment, and final release work remain out
of scope in Phases 5–8. The web server is local tooling, not a hosted service.

## Independent-verification fix

The first detached Phase 4 verification found report hash overflow, stale report
publication after source changes, ambiguous resource-package discovery, and
missing browser failure-event coverage. The bounded repair reuses the canonical
source-state digest at publication reads, withholds stale downloads until
regeneration, preserves full wrapping SHA-256 values at narrow and 200% reflow,
makes template/static package discovery explicit, and records page errors plus
expected and unexpected request failures in the real Chromium lifecycle.
