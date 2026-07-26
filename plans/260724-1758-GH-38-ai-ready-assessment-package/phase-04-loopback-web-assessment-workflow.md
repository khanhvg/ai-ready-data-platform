# Phase 4: Loopback server-rendered assessment workflow

## Context links

- Parent: [plan.md](./plan.md)
- Dependencies: [Phase 2](./phase-02-versioned-contracts-local-store-and-portability.md), [Phase 3](./phase-03-deterministic-engine-and-report-generation.md)
- Decisions: [PD-01, PD-03, PD-13](./architecture-decisions.md)
- Traceability: [AC-05, AC-07; SM-16](./requirements-traceability.md)

## Overview

- Date: 2026-07-24
- Description: Deliver the complete loopback create-assess-review-deep-dive-select-report-export-import path with server-rendered pages.
- Priority: P2
- Implementation status: Completed
- Review status: Completed through merged Phase 4 verification evidence.

## Key Insights

- Server-rendered forms keep the local application understandable and operable without a Node build/runtime.
- Routes orchestrate domain/store services; they contain no scoring, question, gate, or catalog business content.
- Read-only demo artifact display is a separate capability from assessment evidence entry.
- Browser automation is bounded to the critical journey and must run without heavy services.

## Requirements

- Bind only to configurable loopback (`127.0.0.1` default), fail on non-loopback without explicit unsupported-development override.
- Create engagement; answer/resume quick assessment; review capabilities/gates/findings/confidence; select deep dives for a later workshop; generate report; export; import/reopen. Phase 7 supplies and executes the first deep-dive question banks.
- Explicit provenance and evidence-status controls at answer/evidence entry.
- Accessible forms/navigation, autosave with visible status, validation summary, keyboard operation, responsive local CSS.
- Read-only validated catalog/demo artifact pages; no pipeline-control route, subprocess, Docker, or cloud action.
- CSRF, upload limits, secure headers, escaped content, no remote assets.

## Architecture

`web/app.py` builds FastAPI with injected `LocalEngagementStore`, content registry, engine, report, catalog, and archive services. Thin routes use PRG (POST/Redirect/GET), signed session/CSRF tokens held in an ephemeral process key, optimistic document revision checks, and explicit engagement IDs. Jinja2 macros render questions/anchors/confidence consistently. Minimal JS enhances autosave and disclosure controls; standard form submission remains complete.

Route families: `/engagements`, `/quick`, `/review`, `/deep-dives`, `/report`, `/archive`, `/catalog`, `/demo`. In this phase `/deep-dives` records selections and planned workshop status; question-bank execution is enabled only after Phase 7 content validates. There is deliberately no `/run`, `/pipeline`, command execution, credential setting, authentication, or network fetch. Uploaded import/evidence files pass store/archive limits and are never executed or served inline with active content types.

## Related code files

- Create: `assessment/src/assessment/web/{app.py,config.py,csrf.py,routes.py,forms.py,dependencies.py}`
- Create: `assessment/src/assessment/web/templates/{base,index,engagement-create,quick,review,deep-dive-select,deep-dive,report,import,catalog,demo,error}.html`
- Create: `assessment/src/assessment/web/static/{app.css,app.js}`
- Create: `assessment/tests/integration/test_web_routes.py`
- Create: `assessment/tests/e2e/test_assessment_journey.py`, `assessment/scripts/runtime-smoke.py`
- Create: `assessment/tests/e2e/test_demo_read_only.py`
- Modify: `assessment/src/assessment/__main__.py`, `assessment/src/assessment/cli.py`
- Modify: `Makefile` for `assessment-browser-install`, `assessment-web`, `assessment-e2e`, and `assessment-runtime-smoke`

## Implementation Steps

1. Build the dependency-injected app factory, strict loopback configuration, CSP/security headers, local static assets, error handling, and health endpoint with no customer state.
2. Implement engagement create/list/open and quick assessment pages from versioned content; preserve draft/revision state and validate status/anchor inputs server-side.
3. Implement review pages showing capability maturity, coverage, independent confidence, all gate traces, blockers, findings, provenance, and architect review notes.
4. Implement deep-dive selection/planning with explicit selected/not-selected state and honest “content pending/not installed” handling; do not execute a deep dive before Phase 7.
5. Implement report generation/view and deterministic archive download; implement bounded archive upload, preflight result, import destination, and reopened engagement redirect.
6. Implement read-only catalog and demo-stage pages that display validated files/artifacts or honest unavailable status; forbid command/pipeline controls.
7. Add unit/integration accessibility checks and a single-worker bounded Playwright journey: create → 30 quick answers → review → select a deep dive → report → export → new-root import → reopen/compare.
8. Add `make assessment-runtime-smoke` as the architect workflow acceptance: start an ephemeral loopback server, drive the complete synthetic Solution Architect journey in a real Chromium process, assert the visible readiness/gates/confidence/findings/roadmap, save the generated standalone report and canonical JSON under an explicit temporary evidence root, verify report section headings and no remote requests, record digests/step transcript, then tear down the browser/server.
9. Verify no-network browser execution after the separately provisioned pinned browser, keyboard labels/focus/error summaries, narrow viewport, one browser worker, server teardown, and no heavy Docker profile.

## Todo list

- [x] Build loopback-only app and secure request boundary.
- [x] Complete create/resume/quick assessment forms.
- [x] Complete review/gate/finding/confidence pages.
- [x] Complete deep-dive selection/planning; defer question-bank forms to Phase 7.
- [x] Complete report/export/import/reopen journey.
- [x] Add read-only catalog/demo artifact display.
- [x] Pass bounded accessible Playwright smoke with network blocked.
- [x] Pass the artifact-producing Solution Architect runtime smoke.
- [x] Prove no pipeline-control surface or heavy service startup.

## Success Criteria

- `make assessment-e2e` completes the required journey and tears down its loopback server.
- `make assessment-runtime-smoke` produces and validates the real standalone HTML/JSON artifact plus a step transcript/digests from the same browser journey; it is not satisfied by unit tests alone.
- Imported engagement under a different root matches answers, evidence statuses, reviews, selections, report JSON, and pinned versions.
- The app works through plain form submissions; JS failure does not block the core path.
- Content/rules are absent from routes/templates; changing a versioned label/anchor appears without Python/UI changes.
- Security headers, CSRF, revision conflict, upload size/type, output escaping, and loopback tests pass.
- Demo page covers known stages/artifacts read-only and contains no run/control action.
- No container, pipeline command, external network, CDN, telemetry, auth, Node application runtime, or frontend build pipeline is introduced.

## Risk Assessment

- Autosave can overwrite concurrent edits; use revision tokens and visible conflicts.
- Large assessment forms can overwhelm users; paginate by domain and show progress without hiding unanswered items.
- File upload is a high-risk boundary; preflight, cap, quarantine to staging, and never serve active content inline.
- Browser tests can become broad/flaky; one critical journey plus focused route tests, fixed synthetic data, deterministic waits.
- Rollback: stop the loopback process and remove/revert only web routes/templates/static assets and targets. CLI/store/engine remain usable, and no engagement folder is deleted or migrated backward.

## Security Considerations

Use SameSite/HttpOnly session cookies, CSRF on all mutations, origin/host checks, CSP `default-src 'self'`, `frame-ancestors 'none'`, MIME sniff prevention, and referrer policy. Generate an ephemeral local secret at startup; never persist it in engagements. Evidence downloads use attachment disposition and safe content type. Do not expose network interfaces by default.

## Next steps

After the local workflow passes review, Phase 5 fills the versioned capability/architecture/mapping/Demo Guide catalog consumed by the existing read-only pages.
