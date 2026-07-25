# GitHub Issue #38 Phase 4 verification evidence

Status: Phase 4 implementation and bounded pre-publication browser checks are complete.
Publication SHA, pull request, configured checks, and fresh detached exact-head verification are
recorded only after they exist and are not claimed by this tracked pre-publication record.

## Scope and provenance

Phase 4 began from immutable Phase 3 integration input
`752830b9f1d90bb71dc82ed56e784eaac63e8c55` and audited plan package
`0b5335d907397bb8fd4f7a8c794ff2e930b6fe6b`.

Package `0.4.0` adds only the local loopback FastAPI/Jinja2 architect workflow, revision-safe
forms/autosave, deterministic review/report orchestration, deep-dive selection with honest
content-pending state, bounded archive export/preflight/import/reopen, read-only catalog/demo
views, secure local sessions and request boundaries, and real Chromium acceptance evidence.

It adds no catalog content, architecture mapping, golden-pipeline evidence integration,
deep-dive question bank, command or pipeline control, arbitrary SQL, credential handling,
network fetch, hosted deployment, object store, cloud action, or customer data.

## Genuine RED/GREEN record

Before product code existed, the new focused web tests were added. Collection at the immutable
input failed with `ModuleNotFoundError: No module named 'assessment.web'`. After implementation,
the focused configuration and route suite passed. This is contemporaneous RED/GREEN evidence;
no retrospective failure was constructed.

## Real browser/runtime evidence

`make assessment-runtime-smoke` starts and tears down real loopback Uvicorn servers and pinned
Chromium 149.0.7827.55 through Playwright 1.61.0. The journey runs inside the repository's
loopback-only sandbox and produced:

- 30 saved quick-assessment answers and four readiness facts;
- visible Not-assessed/no-rating coordination and keyboard-driven autosave at revision 2;
- plain-form/no-JavaScript reset, back, reload, resume, and completion;
- all seven gate traces, findings/recommendations, and an architect accept record;
- one planned deep dive with honest content-pending state;
- a canonical 12-section JSON report and standalone HTML;
- deterministic export, preflight, import under a different root, reopen, state comparison,
  and byte-identical imported report JSON;
- attachment-only local evidence, read-only unavailable catalog/demo views, and security-header
  checks;
- current → source mutation → stale/no-download → regeneration → current report publication;
- full visible report digests without horizontal overflow at 375px and 200%/320px-equivalent
  reflow;
- no remote browser requests, browser console or page errors, or unexpected request failures,
  with expected attachment/navigation aborts recorded separately; and
- clean server logs plus clean browser and server shutdown.

Ignored evidence lives beneath `assessment/.generated/runtime-smoke/`: standalone HTML/JSON,
archive, imported report JSON, two screenshots, transcript, digest manifest, and semantic result.
Those paths and generated artifacts are not tracked.

At the pre-publication run, the canonical report and imported report shared digest
`fca45b70efc259a2aa4119495b2fa3173235ed3c74eb085e30416bda8d4fc448`.
The standalone HTML digest was
`6903af57560fe1d3266033522b3dab3503573ce02dfdc6be13f70a727a097952`.

## Verification contract

The final exact-head pass records exit codes for:

```text
make assessment-install
make assessment-browser-install
make assessment-schema assessment-contract assessment-store assessment-migration assessment-import-export assessment-portability assessment-security-scan
make assessment-scenarios assessment-calibration assessment-report assessment-test assessment-engine
make assessment-e2e
make assessment-runtime-smoke
make assessment-lint assessment-typecheck assessment-build
docker compose config --quiet
git diff --check
```

The focused web suite covers loopback configuration, unsupported override behavior, Host,
Origin, CSRF, signed session cookie flags, stale revisions, request and attachment limits,
template escaping, attachment-only downloads, absent control routes, and read-only unavailable
views. The browser journey supplies the real no-JavaScript, distinct-root portability,
keyboard/narrow-viewport, no-network, report/download, and teardown coverage.

## Rollback and residual boundary

Rollback removes the additive web package, browser/runtime targets, tests, and documentation.
Explicit engagement roots remain authoritative and are not deleted by assessment cleanup.

Phases 5–8 remain pending: catalog content and diagrams, golden-pipeline evidence/manifests,
mapping and deep-dive content execution, recipes, policy enforcement, and final release work.
The existing object-store contract test remains intentionally skipped because object storage is
documentation-only and out of scope.
