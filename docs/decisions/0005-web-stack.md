# ADR-005: Web Stack for the Learning Sandbox

- Status: Accepted
- Decision: Vite + React for the local learning sandbox
- Date: 2026-07-21
- Basis: owner-selected and unscored

## Context

Issue #7 originally evaluated Astro 7.1.3 + React islands, Next 16.2.10 standalone App Router, and Vite 8.1.5 static MPA + progressive React. That v1 evaluation ended honestly with `no-winner`: no numeric scores were assigned, the OS-level manual evidence was incomplete, and Astro had automated target-size failures. Those facts remain historical evidence and are not a score or comparison input for the current decision.

The owner subsequently selected Vite + React for the local learning sandbox. The owner's final-review clarification removed prerequisite reviews before the cook; it did not remove the requirement for two fresh final reviews of the exact post-cook head.

The serialized `i5-02-simple-vite-v3` cook retained run `v3-20260721T174126318Z-af388ddf`. It passed all seven blocking groups against tested source `9b12de130ee5e2f68b7c351d9a736a33017173fa` and tested tree `75302b2cf968573329f419ccb90a7e3b5b810bdc`. Contemporaneous RED provenance is test-only commit `d644c4fbb0e88bd4d77567a705b835a9c0eb79a0`. The run reports zero audit vulnerabilities, and passing S3, cleanup, and rollback checks.

## Decision

Accept Vite 8.1.5 with React 19.2.7 as the web stack for the local learning sandbox.

This is an owner-selected, unscored decision. It is not the result of a revived Vite/Next/Astro comparison, a numeric score, a tie-break, performance measurement, native/manual automation, or historical timer. The retained v1 scorecard remains an explicit historical `no-winner` record with all numeric scores `null`.

The accepted implementation is a static Vite document with progressively attached React controls. It presents the tracked Issue #6 promotion-trust fixture as four independent grains and preserves the exact `insufficient-evidence` / `no-common-grain` conclusion. It adds no portal, runner, privileged action, persistence, external request, cloud path, or production framework commitment.

## Evidence

- Acceptance revision: `i5-02-simple-vite-v3`
- Retained run: `spikes/web/evidence/retained/simple-vite-v3/v3-20260721T174126318Z-af388ddf/`
- Manifest SHA-256: `d3c09e372df3e6f6a9e8609000074391ec0973630e8f2ae2477360b5b507a85b`
- Hash-index SHA-256: `60eb775851648c62119bc8e0660748919132bb2bacead71fb8c015c59e12d225`
- Blocking groups: `7/7` passed
- Security: zero audit vulnerabilities; S3 passed
- Lifecycle: cleanup and rollback passed

## Consequences

- Vite + React is selected only for the local learning sandbox covered by Issue #7.
- Historical candidate dispositions and missing manual evidence remain preserved; they are not reinterpreted as current gating evidence.
- Two fresh independent final reviews must inspect the exact post-cook ADR head. Any further commit invalidates those reviews.
- Production accessibility validation and manual UAT remain deferred downstream responsibilities.
- Chromium, axe, keyboard, reflow, and no-JS automation do not establish full WCAG conformance, screen-reader conformance, production accessibility conformance, or production UAT.
- No CI workflow, portal, runner, cloud integration, release path, or Issue #8+ behavior is introduced by this decision.

## Rollback

If the selected local sandbox implementation must be withdrawn, use a normal reviewed corrective or revert change. Preserve the v1 historical scorecard and the immutable v3 retained evidence; remove only run-owned transient artifacts and do not rewrite shared history or expand the decision into production scope.
