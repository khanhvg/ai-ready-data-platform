# GitHub Issue #38 Phase 5 verification evidence

Status: Phase 5 implementation and bounded pre-publication checks are complete only when the
commands below pass at the committed implementation head. The tested SHA, pull request identity,
configured-check state, and fresh detached exact-head verification are published on Issue #38
and the pull request after they exist; this tracked record does not claim them in advance.

## Scope and provenance

Phase 5 starts from immutable Phase 4 integration input
`4325f0a262d356f16298c31ea3aa8eeb80c58f42` and audited plan package
`0b5335d907397bb8fd4f7a8c794ff2e930b6fe6b`.

Package `0.5.0` adds only the exact ten-domain advisory capability catalog, nine
vendor-neutral logical patterns across the seven required architecture themes, content-only
technology option profiles, seven accessible Mermaid/SVG pairs, an independently versioned
read-only nine-stage Demo Guide, validated catalog services, and report/web presentation.

The AWS-first profile selects one planned tool for each role but performs no cloud action. The
existing sandbox is a separate local read-only illustration. Catalog content, diagram content,
technology presence, and demo artifact availability cannot influence maturity, confidence,
priority, findings, gates, or readiness.

Phase 6–8 golden evidence, policy execution, deep-dive execution content, recipes, object-store
implementation, AWS/Terraform execution, uploads, deployment, customer data, learning/lab
surfaces, and pipeline control remain out of scope.

## Diagram and runtime contract

The build-only Node 22/npm 10.9.8 toolchain pins Mermaid CLI and Puppeteer in a committed npm v3
lock. Dependency installation is explicit. Regeneration runs inside the repository's
network-denying wrapper, renders every diagram twice, normalizes reviewed SVG, and atomically
updates the seven outputs plus their source/tool/output digest manifest. Normal verification is
non-mutating and compares a fresh two-pass render with the committed bytes and manifest.

Every SVG has one matching title and description, a unique ID namespace suitable for the
standalone report, and no script, foreign object, image, link, event handler, remote asset/font,
metadata element, processing instruction, DTD/entity, or local machine path. Each report and web
view also provides an adjacent text/table alternative.

The real Chromium runtime journey exercises all seven local diagrams, available and unavailable
demo artifacts, wide and 375px catalog views, 640px 200%-equivalent demo reflow, browser
back/reload, zero control forms/buttons, local-only requests, console/page/request-failure
review, and clean browser/server teardown while preserving the complete Phase 4 journey.

## Verification contract

The final exact-head pass records exit codes for:

```text
make assessment-install assessment-browser-install assessment-diagram-install
make assessment-schema assessment-contract assessment-store assessment-migration assessment-import-export assessment-portability assessment-security-scan
make assessment-scenarios assessment-calibration assessment-report assessment-test assessment-engine
make assessment-diagrams
make assessment-e2e assessment-runtime-smoke
make assessment-lint assessment-typecheck assessment-build
docker compose config --quiet
git diff --check
```

Focused checks additionally cover exact domain/theme/finding/recommendation/reference resolution,
vendor neutrality, one AWS selection per role, safe repository-relative demo paths, unavailable
artifact honesty, SVG source/render/tool digests, isolated wheel/sdist package resources,
read-only routes, no scoring effect, and no pipeline/cloud/control surface.

Pending-diff review is specification-first and then code-quality. Every Critical and Important
finding must be fixed and its invalidated checks rerun before commit. A completely fresh
independent detached verifier remains mandatory after publication and before any merge.

## Rollback and residual boundary

Rollback reverts the additive catalog, Demo Guide, diagram tooling/assets, presentation,
tests, and documentation while retaining engagement folders and their source evidence. The
assessment framework, engine, engagement schemas, scoring/gates, and Phase 1–4 commands require
no data migration or rollback.

The first catalog version is advisory content and will age independently from logical patterns.
Headless Chromium is the bounded browser used for automation; no screen-reader session is
claimed. The future object-store contract remains documentation-only.
