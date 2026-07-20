---
phase: 3
title: "Astro React Islands Foundation"
status: pending
priority: P1
dependencies: [2]
effort: "3 active hours; 90-minute foundation kill"
barrier: provisional-unscored-before-issue-6
---

# Phase 3: Astro React Islands Foundation

## Context Links

- [Candidate protocol](./candidate-protocol.md)
- [Preview journey contract](./preview-journey-contract.md)
- [Acceptance and test matrix](./acceptance-and-test-matrix.md)

## Overview

Build the smallest Astro static candidate that renders the common ten-act contract and hydrates
only the reversible lab-state controls as a React island. It has an independent exact lockfile and
the same clocks/tests as the other candidates. Before Barrier B/Gate C its only successful
disposition is `PROVISIONAL_UNSCORED`; no numeric score or winner language is legal.

## Requirements

- Pin Astro `7.1.3` and React/React DOM `19.2.7` with no top-level ranges; generate the candidate's
  own npm 10 lockfile. Explicitly force-add only that ignored lockfile and prove it is tracked.
- Freeze `output: static`. Use trusted project-owned build-time MDX/content collections with
  schema validation. Fixture strings remain data, never MDX/JSX or raw HTML.
- Render complete semantic HTML before hydration. Hydrate the smallest practical React control
  island; importing the entire lesson/content tree into the island is a kill condition.
- Consume common logical data through an Astro adapter without changing common/shared or issue #6
  contracts. Future same-origin BFF compatibility is a type seam only.
- Serve built output with the common production-like static measurement host, not the Astro dev
  server. Record emitted client assets, island chunks, initial/lab transfer, CSP, and source maps.

## Architecture

Astro owns static routing/content rendering; one React island owns only interactive controls and
local reversible state. The common contract enters through a thin candidate adapter. Built assets
are served by the measurement host; no candidate server/BFF is introduced.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `spikes/web/candidates/astro/package.json` | small | Exact dependency policy |
| Create | `spikes/web/candidates/astro/package-lock.json` | generated, independent | Reproducible clean install |
| Create | `spikes/web/candidates/astro/astro.config.*` | small | Static mode assertion |
| Create | `spikes/web/candidates/astro/src/content.config.*` and trusted content | bounded | Schema/MDX authoring task |
| Create | `spikes/web/candidates/astro/src/pages/**` | bounded | Semantic static route |
| Create | `spikes/web/candidates/astro/src/components/**` | bounded | Small React island/native Astro content |
| Create | `spikes/web/candidates/astro/tests/**` | bounded | Adapter/component/static tests |
| Create | `spikes/web/evidence/retained/astro/**` | sanitized decision artifacts only | Retention through I5-05 |

## Related Code Files

- Create only the Astro candidate and retained evidence paths above.
- Read Gate A common fixtures/tests and Gate 0 registries.
- Delete nothing; never modify other candidates or shared/dependency paths.

## Dependency Map

```text
Gate A manifest/state/failure/evidence/test semantics
  -> Astro content adapter + static page
  -> narrow React controls island
  -> common static host + common tests
  -> Barrier B/Gate C clean rerun
```

## Interface Checklist

- [ ] Common manifest/fixture/state digest is unchanged.
- [ ] Astro adapter adds no candidate-only field or transition.
- [ ] Static HTML includes all acts/cards/limitations/labels/fallback navigation.
- [ ] React client graph contains only lab controls and their state dependencies.
- [ ] Browser/client types contain no runner URL, credential, mutation, or cloud endpoint.
- [ ] Build-time content schema gives field-local errors for missing/unknown required data.

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | Clean install/build/static route by 90m | Pass or `ELIMINATED`; no extra time |
| Critical | Common four-grain/non-completion/security IDs | Identical assertions, no adapter exception |
| High | No-JS output and smallest island | Complete facts; measured client boundary |
| High | Back/reload/reset/reduced motion | Common state semantics unchanged |
| High | Trusted content schema negative | Build/validation fails at authored field |
| High | Static host readiness/CSP/shutdown | Deterministic lifecycle and evidence |

## Implementation Steps

1. Add missing-candidate/mode/content/island tests and start the timer.
2. Pin/install the independent candidate and reach the 90-minute static foundation.
3. Complete the narrow island/content/schema/static/security executable must-pass.
4. Emit provisional/eliminated evidence and stop at three hours.

## Tests Before

1. Point the unchanged common suite at the absent Astro candidate and retain the failing IDs.
2. Add candidate-specific tests only for Astro mode, static build, content schema, and island
   boundary; do not duplicate or weaken shared WEB semantics.
3. Start the candidate timer immediately before the first install/authoring action after the
   common freeze.

## Refactor

At 90 minutes, require clean install, a successful static build, a semantic lesson route, and
common-contract consumption. Kill if any is missing. Continue only to complete the provisional
candidate-local/shared automated must-pass set. Manual named-AT and real-fixture evidence remain
pending Gate C and never become provisional passes.

## Tests After

- Run candidate unit/schema/static checks and all applicable common tests unchanged.
- Capture package/lock hashes, install-script inventory, advisory/license/provenance disposition,
  build manifest, CSP, initial/island JS, start/stop and timer evidence.
- At three hours, mark `PROVISIONAL_UNSCORED` only when all currently executable must-passes are
  green in `foundation` scope; otherwise mark `ELIMINATED` with a null numeric score. Enumerate
  fresh browser E2E/manual and real-fixture checks as required pending `decision` scope.

## Regression Gate

Planned future commands:

```bash
make -f mk/issue-5/i5-02.mk web-astro-install
make -f mk/issue-5/i5-02.mk web-astro-build
make -f mk/issue-5/i5-02.mk web-astro-test
make -f mk/issue-5/i5-02.mk web-astro-evidence SCOPE=foundation
```

Every command first runs Gate 0. Install/build/test exit non-zero on a required foundation failure
or missing tool. `web-astro-evidence SCOPE=foundation` writes `fitness-result-v1`, timer, hashes,
command results, provisional disposition, retained-artifact index, and an explicit list of required
Gate C browser/manual/real-fixture inputs; it exits non-zero if foundation evidence is incomplete,
a score is present, or mode/fixture/test IDs drift. Before Gate C it must say
`PROVISIONAL_UNSCORED` or `ELIMINATED`. `web-astro-a11y` and `web-astro-e2e` remain mandatory
future `decision`-scope targets invoked by Gate C; they are neither run nor marked optional here.

## Success Criteria

- [ ] Foundation gate closes by 90 minutes and provisional must-pass by three hours.
- [ ] Static semantic facts survive no-JS and the React boundary remains narrow.
- [ ] Common contract/test semantics are unchanged.
- [ ] Candidate is unscored and cannot select itself.

## Risk, Security, and Rollback

Astro-specific risks are island creep and executable/ambiguous content. Remove unsafe content or
island imports; if unresolved at cap, eliminate. Rollback excludes the candidate from execution,
deletes only its transient install/build state, retains source/lock/evidence, and leaves the
neutral preview intact.

## Next Steps

Wait at Barrier B after all three equal foundations; no synthetic evidence crosses into scoring.
