---
phase: 6
title: "Stage B Vite binding and final handoff"
status: pending
priority: P1
dependencies: [5]
stage: "B"
blockedOn: "exact merged Issue #7 Vite ADR/handoff SHA"
---

# Phase 6: Stage B Vite Binding and Final Handoff

## Context Links

- [Stage A release conditions](./phase-05-stage-a-compatibility-release-and-staged-handoff.md#stage-a-independent-merge-decision-record)
- [Master ADR-005 boundary](../260721-005-enterprise-learning-sandbox/architecture-decisions.md#adr-005-web-stack-scorecard)
- [Owner Vite decision](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177)

## Overview

Bind the immutable Stage A contract IDs, operation IDs and hashes to the selected Vite/React
consumer format, prove lossless compatibility with the exact merged Issue #7 handoff, and publish
the final I5-03 contract handoff. This phase is deliberately empty of guessed dependency identity:
Issue #7 is OPEN/unmerged at planning time, so no SHA is written until a real merged handoff exists.

## Hard Entry Gate

All conditions are mandatory:

1. Stage A has an accepted contract release SHA recorded externally and is present in tested
   ancestry, whether through an authorized staged merge or one full implementation branch.
2. Fresh fetch proves Issue #7 is merged and its exact merge SHA is in tested ancestry.
3. The merged handoff contains an accepted Vite ADR, exact read-only Vite/common source and lock
   paths/hashes, exact install/test/build/smoke/security commands, accepted residual risks and a
   downstream contract handoff.
4. The Issue #7 merge passed its own required reviews/checks and exact-head human approval. The
   owner comment alone, an unmerged branch head, proposed ADR or old scorecard cannot satisfy this.
5. A fresh Stage B readiness decision authorizes the exact I5-03 binding paths/commands/head after
   comparing the merged handoff with this plan. If the handoff paths or semantics differ from this
   plan, stop and amend/revalidate; do not guess.
6. Local = tracking = freshly fetched live remote at the authorized Stage B input; tree clean; the
   Issue #8 shared-contract lease remains exclusive.

Until every condition passes, Phase 6 status is `blocked-on-issue-7-merged-sha`; no binding file,
placeholder SHA, copied preview contract or framework-specific workaround is permitted.

## Requirements

- Functional: read exact merged Issue #7 Vite ADR/handoff, Vite manifest/lock and common-contract
  source as read-only inputs; record their real hashes and merge SHA in the binding handoff.
- Functional: generate Vite-facing ESM constants/type declarations for Stage A contract IDs,
  versions, operation IDs and content hashes only.
- Functional: provide a binding manifest that maps every selected-stack view/field/action to one
  Stage A schema/ref/operation without changing semantics or canonical bytes.
- Functional: map any merged Issue #7 provisional preview shape through an explicit lossless
  adapter. No provisional field becomes a shared contract by copying it.
- Non-functional: no runtime validator fork, alternate canonicalizer, copied schema/default,
  second completion rule, package workspace or new dependency. Use built-in Node test plus the
  exact manifest-admitted Vite runtime/lock from the accepted handoff.

## Architecture

Stage B is a generated consumer binding, not a contract version:

```text
Stage A contract set (source of truth)
    ├── schema IDs / versions / hashes
    ├── OpenAPI operation IDs / paths
    └── completion/evidence canonical rules
             |
             v
  generated Vite ESM constants + declarations
             |
             v
  binding manifest with exact Issue #7 merge/lock/source hashes
```

The ESM module contains immutable strings/records only. Runtime boundary validation remains the
Stage A validator and future portal/runner adapters. A browser hint, cache state or preview view
cannot mutate completion. If the Vite consumer needs different fields or canonical behavior, the
binding fails and a separately planned additive Stage A v2 is required.

## Related Code Files

Future Issue #8 writes are exact and additive:

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/bindings/vite/contract-bindings-v1.json` | exact Stage A↔merged Vite view/action/hash mapping and dependency identity |
| Create | `learning/contracts/bindings/vite/contract-ids-v1.mjs` | generated ESM contract/version/operation/hash constants |
| Create | `learning/contracts/bindings/vite/contract-ids-v1.d.ts` | generated declarations matching the ESM constants |
| Create | `tests/contracts/learning/test_vite_binding.py` | Stage A source/hash/semantic/no-drift and dependency-handoff checks |
| Create | `tests/contracts/learning/vite-binding.test.mjs` | dependency-free ESM import/export/exact-value checks under accepted Node runtime |
| Modify | `learning/contracts/learning-contract-set-v1.json` | **Forbidden if Stage A was released.** Instead the final handoff hashes Stage A set + binding separately. |
| Modify | `scripts/learning_contracts/check.py` | add binding-present validation path without changing Stage A results |
| Modify | `tests/contracts/learning/test_command_and_release.py` | final two-set handoff and external identity assertions |

Read-only dependency paths are not frozen by this planner. The merged Issue #7 handoff must name
them exactly. Current unmerged `spikes/web/**` and ADR files are non-authoritative and must not be
edited by Issue #8.

## Tests Before

Write/freeze these failures after the real dependency handoff is available and before binding:

- missing/unmerged/wrong Issue #7 merge SHA or ancestry;
- ADR not Accepted/Vite, dependency path/hash/lock/tool/command mismatch;
- missing/extra/renamed schema ID, version, operation ID, field/action mapping;
- copied/divergent schema/default/canonicalizer/completion authority;
- provisional preview field that cannot map losslessly;
- stale Stage A contract set or binding regenerated from dirty/uncommitted bytes;
- Node/Vite runtime or lock not exactly manifest-admitted.

Retain the expected failures with exact Stage A and Issue #7 identities before generating binding
bytes. No test may hard-code a guessed future SHA.

## Refactor

Generation is deterministic: sorted Stage A IDs/hashes and operation matrix produce one ESM/`.d.ts`
pair. Hand-authored contract semantics in the generated module are forbidden. Keep dependency
provenance in the JSON binding manifest; do not embed it in schema IDs or alter Stage A files.

## Tests After and Final Blast Radius

Issue #8 commands:

```bash
node --test tests/contracts/learning/vite-binding.test.mjs
make learning-contracts-check
make api-contracts-check
make evidence-contracts-check
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
```

Also run the exact Vite install/unit/build/Chromium/axe/no-JS/security commands copied verbatim
from the accepted merged Issue #7 handoff. They are intentionally not invented in this plan before
that handoff exists. The evidence records each exact command and exit status. Any missing command,
runtime, browser/tool or artifact required by the handoff is `fail`, not skip.

Re-run:

- Stage A canonical hashes and results byte-for-byte;
- full binding generation twice in separate temp roots;
- Vite import/consumer mapping and lossless preview-adapter vectors;
- no-network/no-cloud-credential and S3 secret/private-path scans;
- changed-path/protected hash/Issue #7 read-only checks;
- rollback removing only the binding selection while Stage A stays readable.

## Implementation Steps

1. Fresh-fetch and verify the hard entry gate, real merge/ADR/handoff/lock/tool/command identities
   and exclusive lease.
2. Add binding RED tests tied to the real dependency identity.
3. Generate deterministic ESM constants/declarations from the Stage A contract set and operation
   matrix; generate the binding manifest with real dependency paths/hashes/SHA.
4. Implement binding validation in the existing check runner without changing Stage A output.
5. Close Python/Node binding tests and run the complete Issue #8 + Issue #6 + accepted Vite blast
   radius at one exact clean committed head.
6. Rehearse binding-only rollback and prove Stage A remains usable/readable.
7. Publish non-recursive final evidence and external final contract release SHA after required
   reviews, repository checks and human exact-head approval. No tracked file claims its own commit.
8. Hand downstream owners the exact Stage A set hash, binding hash, Issue #7 merge SHA, final
   contract release SHA, commands, compatibility/rollback result and remaining residual risks.

## Success Criteria

- [ ] Exact accepted merged Issue #7 Vite handoff—not owner direction/provisional bytes—is consumed.
- [ ] Binding maps every Stage A schema/version/operation/hash exactly and losslessly.
- [ ] Generated ESM/`.d.ts` output is deterministic and contains no parallel schema/state logic.
- [ ] Stage A canonical bytes, operation matrix, completion authority and migration rules do not drift.
- [ ] Issue #8, Issue #6 and accepted Vite blast-radius commands pass at one exact head.
- [ ] Binding rollback leaves Stage A and retained evidence intact.
- [ ] Final external contract release SHA and exact-head human approval are recorded truthfully.

## Risk Assessment

- The future Issue #7 handoff may use different paths/commands than today’s unmerged branch.
  Mitigation: do not freeze them here; readiness compares and amends/revalidates before cook.
- Generated types can imply runtime validation. Mitigation: declarations/constants only; boundary
  validation remains the Stage A source contract.
- Updating the Stage A release set after staged merge would rewrite a released artifact. Mitigation:
  hash Stage A set and binding as two immutable components in external final handoff.

## Security and Rollback

Issue #7 paths are strictly read-only. Binding evidence is scanned for dependency secrets, local
paths, bundle/source-map leakage and recursive identities. Rollback deselects/removes only the
binding version through a reviewed additive change; never rewrites Stage A schemas/evidence,
Issue #7 sources, old readers or fixtures.

## Next Steps

After final release, downstream issues consume the exact externally attested contract release SHA
read-only. No downstream cook or merge is authorized by this phase; each issue retains its own
dependency, validation, readiness and human gates.
