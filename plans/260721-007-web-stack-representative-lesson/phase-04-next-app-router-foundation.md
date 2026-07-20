---
phase: 4
title: "Next App Router Foundation"
status: pending
priority: P1
dependencies: [2]
effort: "3 active hours; 90-minute foundation kill"
barrier: provisional-unscored-before-issue-6
---

# Phase 4: Next App Router Foundation

## Context Links

- [Candidate protocol](./candidate-protocol.md)
- [Preview journey contract](./preview-journey-contract.md)
- [Security S3 disposition](./security-s3-disposition.md)

## Overview

Build one frozen Next.js App Router mode: a self-hosted standalone runtime with a prerenderable
semantic lesson page, narrow Client Component for reversible state, and read-only Route Handler
fixture replay. This measures Next's integrated future-BFF evolution without implementing a
runner or using Server Actions as a private-boundary shortcut.

## Requirements

- Pin Next `16.2.10` and React/React DOM `19.2.7`; independent npm 10 lockfile and exact top-level
  versions.
- Freeze `output: standalone`. Production command is the generated standalone server bound to
  loopback. Do not switch to static export, dev, edge, or another server mode to improve a metric.
- Keep the lesson in Server Components/prerendered output where supported. Place only explicit
  controls/state below a narrow `use client` boundary and record its dependency graph.
- Route Handler is read-only fixture replay/readiness only. No Server Action, mutation, runner
  URL, credential, or cloud path.
- Add explicit trusted MDX/frontmatter/schema validation; `@next/mdx` alone is not treated as a
  complete content schema.
- Record CSP/render-mode interaction. No wildcard origin, `unsafe-eval`, remote script, or hidden
  dynamic-mode switch can pass.

## Architecture

The App Router server/prerender path owns semantic content, a narrow Client Component owns only
reversible controls, and one read-only Route Handler represents fixture replay. Standalone output
is the frozen production-like mode; no Server Action or runner path exists.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `spikes/web/candidates/next/package.json` | small | Exact dependency policy |
| Create | `spikes/web/candidates/next/package-lock.json` | generated, independent | Clean standalone install |
| Create | `spikes/web/candidates/next/next.config.*` | small | Standalone/mode/CSP assertions |
| Create | `spikes/web/candidates/next/app/**` | bounded | App Router semantic route/read-only handler |
| Create | `spikes/web/candidates/next/content/**` | bounded | Trusted MDX/schema authoring |
| Create | `spikes/web/candidates/next/lib/**` | bounded | Common adapter/future BFF interface |
| Create | `spikes/web/candidates/next/tests/**` | bounded | Server/client boundary and route tests |
| Create | `spikes/web/evidence/retained/next/**` | sanitized decision artifacts only | Retention through I5-05 |

## Related Code Files

- Create only the Next candidate and retained evidence paths above.
- Read common contract/tests and Gate 0 registries.
- Delete nothing; never alter other candidates or shared/dependency paths.

## Dependency Map

```text
Gate A logical contract
  -> Server Component/content schema + prerendered semantic page
  -> narrow Client Component + read-only replay Route Handler
  -> standalone build/start/readiness/shutdown
  -> Barrier B/Gate C clean rerun
```

## Interface Checklist

- [ ] Common contract is imported/adapted read-only with identical WEB IDs.
- [ ] `use client` boundary excludes the lesson/content/evidence tree.
- [ ] Route Handler exposes no mutation and no future runner type/URL/token.
- [ ] Static/no-JS response contains every fact, card, limitation, label, and linear navigation.
- [ ] Standalone mode and CSP are explicit in build/runtime evidence.
- [ ] Server/client/source-map bundles pass credential and absolute-path scans.

## Test Scenario Matrix

| Priority | Scenario | Expected result |
|---|---|---|
| Critical | Clean install/standalone build/semantic route by 90m | Pass or `ELIMINATED` |
| Critical | Server Action/direct privilege shortcut attempted | Hard fail |
| Critical | Common grain/non-completion/content safety | Same WEB outcomes |
| High | Client boundary absorbs lesson tree | Eliminate if not corrected by cap |
| High | CSP changes render/runtime mode | Evidence invalidated; mode cannot drift |
| High | Standalone signal/readiness/cache behavior | Exact startup/shutdown record |

## Implementation Steps

1. Add missing-candidate/standalone/client-boundary/route/schema tests and start the timer.
2. Pin/install the independent candidate and reach the 90-minute semantic standalone foundation.
3. Complete executable must-pass, CSP/bundle/lifecycle/supply-chain evidence.
4. Emit provisional/eliminated evidence and stop at three hours.

## Tests Before

1. Run unchanged common tests against the absent Next candidate and retain failing IDs.
2. Add candidate-only tests for standalone mode, semantic initial response, client graph size,
   read-only Route Handler, no Server Actions, content schema, and process lifecycle.
3. Start the timer before first install/authoring action.

## Refactor

At 90 minutes, require clean install, standalone build, semantic route, and common contract. Kill
otherwise. Finish the candidate-local/shared executable must-pass by three hours. Real fixture,
fresh browser comparison, and manual named-AT review stay pending Gate C; they cannot be claimed
from unit output.

## Tests After

- Run unit/schema/static/route/process checks and unchanged applicable common tests.
- Record standalone output, Server/Client graph, initial/lab JS, process-tree RSS hooks, cache
  behavior, CSP, locks/supply-chain evidence, and exact timer.
- At cap, record only `PROVISIONAL_UNSCORED` or `ELIMINATED`; numeric score must be null.

## Regression Gate

Planned future commands:

```bash
make -f mk/issue-5/i5-02.mk web-next-install
make -f mk/issue-5/i5-02.mk web-next-build
make -f mk/issue-5/i5-02.mk web-next-test
make -f mk/issue-5/i5-02.mk web-next-a11y
make -f mk/issue-5/i5-02.mk web-next-e2e
make -f mk/issue-5/i5-02.mk web-next-evidence
```

Commands emit evidence and exit non-zero on missing tools, unsafe routes/CSP, non-semantic output,
mode/test/fixture drift, lifecycle failure, or any applicable must-pass failure. The evidence
target also exits non-zero if pre-Gate-C data contains a numeric score or winner field.

## Success Criteria

- [ ] Foundation and provisional gates close within equal caps.
- [ ] Next mode is standalone, stable, semantic, and explicit.
- [ ] Client and API boundaries stay narrow/read-only/no-privilege.
- [ ] Common tests remain unchanged and result stays unscored.

## Risk, Security, and Rollback

Risks are accidental full-client rendering, implicit runtime drift, CSP weakening, and Route
Handler privilege creep. Fail closed and eliminate at cap. Rollback disables the candidate start
entry, removes transient build/install state, retains source/lock/evidence, and restores the
neutral preview as the only executable surface.

## Next Steps

Wait at Barrier B after equal foundations. Any change to standalone/render mode requires full
candidate evidence invalidation without added time.
