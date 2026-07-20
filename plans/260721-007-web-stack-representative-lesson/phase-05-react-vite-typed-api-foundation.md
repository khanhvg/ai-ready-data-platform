---
phase: 5
title: "React Vite Typed API Foundation"
status: pending
priority: P1
dependencies: [2]
effort: "3 active hours; 90-minute foundation kill"
barrier: provisional-unscored-before-issue-6
---

# Phase 5: React Vite Typed API Foundation

## Context Links

- [Candidate protocol](./candidate-protocol.md)
- [Preview journey contract](./preview-journey-contract.md)
- [Acceptance and test matrix](./acceptance-and-test-matrix.md)

## Overview

Build a React/Vite candidate with an explicit typed API seam and a genuine prerendered/MPA
semantic artifact. An empty SPA mount point is an immediate must-pass failure. Built assets use the
same common static measurement host as Astro; `vite preview` is permitted only for developer
diagnosis and never appears in decision evidence.

## Requirements

- Pin Vite `8.1.5` and React/React DOM `19.2.7`; own independent npm 10 lockfile with exact
  top-level versions. Explicitly force-add only that ignored lockfile and prove it is tracked.
- Generate complete semantic HTML at build time using a bounded candidate-native prerender/MPA
  approach, then progressively enhance only explicit controls.
- Keep the typed adapter explicit and read-only in issue #7. `VITE_*` values are public by design;
  reject secret-shaped values and never define a runner/private URL.
- Use trusted project-owned build-time content and schema validation. No runtime MDX/eval/fixture
  JSX and no common contract fork to compensate for missing framework behavior.
- Measure built output with the common static host and record Vite asset manifest, raw/compressed
  route JS, lazy chunks, CSP, source maps, and exact lifecycle.

## Architecture

Vite builds a genuine prerendered/MPA semantic artifact; React progressively enhances named
controls; an explicit read-only typed adapter maps common logical shapes. The common static host
serves built files for evidence. The candidate does not invent a shared SSR framework.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `spikes/web/candidates/vite/package.json` | small | Exact dependency policy |
| Create | `spikes/web/candidates/vite/package-lock.json` | generated, independent | Reproducible clean install |
| Create | `spikes/web/candidates/vite/vite.config.*` | small | MPA/manifest/mode assertions |
| Create | `spikes/web/candidates/vite/src/**` | bounded | React controls + typed adapter |
| Create | `spikes/web/candidates/vite/content/**` | bounded | Trusted authored lesson |
| Create | `spikes/web/candidates/vite/scripts/prerender.*` | bounded | Semantic build artifact |
| Create | `spikes/web/candidates/vite/tests/**` | bounded | Static/adapter/env tests |
| Create | `spikes/web/evidence/retained/vite/**` | sanitized decision artifacts only | Retention through I5-05 |

## Related Code Files

- Create only the Vite candidate and retained evidence paths above.
- Read common contract/tests and Gate 0 registries.
- Delete nothing; never alter other candidates or shared/dependency paths.

## Dependency Map

```text
Gate A logical contract
  -> content/schema + typed read-only adapter
  -> prerendered semantic MPA artifact
  -> progressive React controls + asset manifest
  -> common static host
  -> Barrier B/Gate C clean rerun
```

## Interface Checklist

- [ ] Built HTML contains all required facts/acts/cards/limitations/labels before JS.
- [ ] Adapter maps the unchanged common client shape and exposes no raw fetch/runner authority.
- [ ] No secret-shaped `VITE_*`, remote endpoint, wildcard CORS, or service worker.
- [ ] Manifest identifies initial route JS separately from interaction chunks/build total.
- [ ] Prerender source remains candidate-native and does not become a shared rendering framework.
- [ ] `vite preview` is absent from measurement/evidence commands.

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | Clean install/build/semantic HTML by 90m | Pass or `ELIMINATED` |
| Critical | Empty `<div id="root">` without facts | Immediate fail |
| Critical | Secret/public-env or direct runner path | Hard fail |
| High | Common state/grain/failure semantics | Identical WEB outcomes |
| High | Prerender/content schema task exceeds cap | Eliminate; no framework build-out |
| High | Production evidence uses `vite preview` | Evidence invalid |

## Implementation Steps

1. Add missing-candidate/semantic-build/adapter/env/host tests and start the timer.
2. Pin/install the independent candidate and reach the 90-minute semantic foundation.
3. Complete executable must-pass, manifest/CSP/supply-chain/lifecycle evidence.
4. Emit provisional/eliminated evidence and stop at three hours.

## Tests Before

1. Run unchanged common tests against the absent candidate and retain failing IDs.
2. Add candidate-only tests for semantic built HTML, Vite manifest, typed adapter runtime
   validation, public-env canaries, no `vite preview`, and static-host lifecycle.
3. Start the timer before first install/authoring action.

## Refactor

At 90 minutes, require clean install, successful static build, semantic route, and common-contract
consumption. Kill otherwise. Complete the provisional executable must-pass by three hours without
building a general SSR framework. Manual AT/real-fixture comparison remains Gate C.

## Tests After

- Run candidate unit/schema/static/env checks and unchanged applicable common tests.
- Record package/lock, lifecycle/advisory/license/provenance, build manifest, initial/interactive
  JS, CSP, start/stop, timer, and non-copy evidence.
- Mark only `PROVISIONAL_UNSCORED` or `ELIMINATED` at cap; score remains null.
  A provisional record is `foundation` scope and enumerates browser/manual/real-fixture checks as
  required pending `decision` scope.

## Regression Gate

Planned future commands:

```bash
make -f mk/issue-5/i5-02.mk web-vite-install
make -f mk/issue-5/i5-02.mk web-vite-build
make -f mk/issue-5/i5-02.mk web-vite-test
make -f mk/issue-5/i5-02.mk web-vite-evidence SCOPE=foundation
```

Targets emit `fitness-result-v1` evidence and exit non-zero on missing tools, empty/non-semantic
HTML, unsafe public env, dev-server substitution, test/mode/fixture drift, or required must-pass
failure. Evidence rejects any pre-Gate-C numeric score/winner.
It also rejects a provisional record missing the required pending decision-scope gate list.
`web-vite-a11y` and `web-vite-e2e` remain mandatory Gate C targets and are not optional
foundation results.

## Success Criteria

- [ ] The candidate builds a true semantic no-JS artifact by the equal foundation gate.
- [ ] React/API enhancement remains explicit, safe, and common-contract compatible.
- [ ] Production-like measurement never uses `vite preview`.
- [ ] Candidate remains provisional/unscored or is eliminated at cap.

## Risk, Security, and Rollback

Risks are SPA-only output, custom-framework creep, public environment leakage, and invalid dev-
server evidence. Fail/kill rather than expand scope. Rollback removes transient install/build
state and candidate execution entry, retaining source/lock/evidence and the neutral preview.

## Next Steps

All three foundation dispositions feed Barrier B. A killed candidate remains retained and is never
resurrected or scored without a separately authorized new spike.
