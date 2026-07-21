# ADR-005: Web Stack for the Learning Sandbox

- Status: Proposed
- Decision: no-winner
- Date: 2026-07-21

## Context

Issue #7 compared Astro 7.1.3 + React islands, Next 16.2.10 standalone App Router, and Vite 8.1.5 static MPA + progressive React against the same tracked Issue #6 promotion-trust fixture. Barrier B passed exact merge and content identities. The common contract, score anchors, candidate modes, fixture, and locks were frozen before Gate C.

## Proposed decision

No winner is proposed. Astro was eliminated by automated WCAG 2.2 target-size failures. Vite and Next passed the captured automated browser suite, but the required actual macOS keyboard, named VoiceOver spoken traversal, 200% browser zoom, OS reduced-motion, and no-JS comprehension evidence could not be obtained because the OS Automation/Accessibility boundary was unavailable.

No candidate receives a numeric score. This honest no-winner does not satisfy Issue #7 acceptance and does not unblock I5-05.

## Consequences

- The framework-neutral Gate A preview remains the only runnable retained artifact with prior review authority.
- All candidate source and exact locks remain retained for a fresh Gate C session.
- No root Make alias, portal, runner, cloud path, release path, or default framework selection is created.
- A fresh independent exact-head review is still required before any PR or merge.

## Rollback

Keep ADR-005 `Proposed`/`no-winner`, preserve source/locks/evidence, remove only candidate-owned transient installs/builds/profiles, and rerun Gate C only under fresh authorization with complete OS-level manual evidence.
