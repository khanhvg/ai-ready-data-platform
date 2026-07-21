# ADR-005 Web Stack Scorecard Evidence

Status: `Proposed`  
Decision: `no-winner`  
Issue #7 acceptance: blocked

Barrier B passed exact M2 ancestry, four SHA-256/blob identities, manifest v2 portable local-integrity semantics, four independent grains, and `insufficient-evidence` / `no-common-grain`.

Gate C ran in rotated order Vite → Astro → Next using installed Chrome 150.0.7871.129 and Playwright Firefox 151.0 (revision 1532). Vite and Next passed automated semantic, keyboard-path, axe A/AA, reflow, reduced-motion emulation, no-JS facts, same-origin network, CSP, and storage checks. Astro was eliminated after `target-size` serious violations in both engines. Eliminated and incomplete candidates have no numeric score.

The actual macOS manual gate is incomplete. `System Events` waited for OS Automation/Accessibility permission and exposed no operable UI state, so no actual macOS keyboard traversal or VoiceOver spoken traversal could be captured. Actual 200% Chrome zoom, OS reduced-motion review, and actual no-JS comprehension were not performed. Playwright evidence was not relabeled as manual evidence.

Therefore the frozen score anchors were not applied, no framework is selected, and Issue #7 acceptance cannot advance. A fresh authorized Gate C session with observable OS-level manual evidence is required.
