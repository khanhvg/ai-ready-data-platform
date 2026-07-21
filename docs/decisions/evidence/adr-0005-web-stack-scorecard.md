# ADR-005 Web Stack Decision Evidence

## Current v3 owner-selected decision

- Status: `Accepted`
- Decision: `Vite + React` for the local learning sandbox
- Selection basis: `owner-selected-unscored`
- Numeric score: `null`

The owner selected Vite + React without reviving the historical candidate comparison or applying score anchors. The owner's final-review clarification removed prerequisite reviews before cook. Two fresh independent final exact-head reviews remain mandatory after the cook and ADR update.

The retained `i5-02-simple-vite-v3` run is `v3-20260721T174126318Z-af388ddf`. It tested source `9b12de130ee5e2f68b7c351d9a736a33017173fa` and tree `75302b2cf968573329f419ccb90a7e3b5b810bdc`, with contemporaneous RED test-only commit `d644c4fbb0e88bd4d77567a705b835a9c0eb79a0`.

All seven blocking groups, `V3-01` through `V3-07`, passed. The retained audit reports zero info, low, moderate, high, or critical vulnerabilities. S3 redaction/security checks passed, and cleanup/rollback passed for run-owned candidate runtime only.

- Manifest: `spikes/web/evidence/retained/simple-vite-v3/v3-20260721T174126318Z-af388ddf/manifest.json`
- Manifest SHA-256: `d3c09e372df3e6f6a9e8609000074391ec0973630e8f2ae2477360b5b507a85b`
- Hash index: `spikes/web/evidence/retained/simple-vite-v3/v3-20260721T174126318Z-af388ddf/hash-index.json`
- Hash-index SHA-256: `60eb775851648c62119bc8e0660748919132bb2bacead71fb8c015c59e12d225`

This evidence supports the local learning sandbox decision only. Production accessibility testing and manual UAT are deferred. Chromium and axe automation are not a full WCAG, screen-reader, production-accessibility, or production-conformance claim.

## Historical v1 scorecard — preserved no-winner record

- Status: `Proposed`
- Decision: `no-winner`
- Issue #7 acceptance: blocked

Barrier B passed exact M2 ancestry, four SHA-256/blob identities, manifest v2 portable local-integrity semantics, four independent grains, and `insufficient-evidence` / `no-common-grain`.

Gate C ran in rotated order Vite → Astro → Next using installed Chrome 150.0.7871.129 and Playwright Firefox 151.0 (revision 1532). Vite and Next passed automated semantic, keyboard-path, axe A/AA, reflow, reduced-motion emulation, no-JS facts, same-origin network, CSP, and storage checks. Astro was eliminated after `target-size` serious violations in both engines. Eliminated and incomplete candidates have no numeric score.

The actual macOS manual gate was incomplete. `System Events` waited for OS Automation/Accessibility permission and exposed no operable UI state, so no actual macOS keyboard traversal or VoiceOver spoken traversal could be captured. Actual 200% Chrome zoom, OS reduced-motion review, and actual no-JS comprehension were not performed. Playwright evidence was not relabeled as manual evidence.

Therefore the frozen score anchors were not applied, no framework was selected by the v1 scorecard, and Issue #7 acceptance could not advance under that historical authority. Every historical candidate numeric score remains `null`.
