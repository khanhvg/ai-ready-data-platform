---
phase: 6
title: "Stage B Vite binding and final handoff"
status: pending
priority: P1
dependencies: [5]
stage: "B"
blockedOn: "exact merged Issue #7 Vite ADR/handoff SHA"
gateStatus: "blocked-on-issue-7-merged-sha"
cookable: false
---

# Phase 6: Stage B Vite Binding and Final Handoff

<!-- Updated: Validation Session 1 - non-cookable gate with zero pre-handoff file/tool/adapter authority. -->

## Context Links

- [Stage A release conditions](./phase-05-stage-a-compatibility-release-and-staged-handoff.md#stage-a-independent-merge-decision-record)
- [Owner Vite decision](https://github.com/khanhvg/ai-ready-data-platform/issues/7#issuecomment-5036142177)

## Overview

After the hard gate is cleared and this phase is amended/revalidated, bind immutable Stage A
contract IDs, operation IDs and hashes to the exact selected Vite/React consumer boundary, prove
lossless compatibility with the merged Issue #7 handoff, and publish the final I5-03 contract
handoff. This current phase is deliberately empty of guessed dependency identity, file path, tool,
command, adapter shape or consumer format: Issue #7 is OPEN/unmerged at validation time.

## Hard Entry Gate

All conditions are mandatory:

1. Stage A has an accepted contract release SHA recorded externally and is present in tested
   ancestry, whether through an authorized staged merge or one full implementation branch.
2. Fresh fetch proves Issue #7 is merged and its exact merge SHA is in tested ancestry.
3. The merged handoff contains an accepted Vite ADR, exact read-only Vite/common source and lock
   paths/hashes, exact install/test/build/smoke/security commands, accepted residual risks and a
   downstream contract handoff.
4. The Issue #7 merge passed its own required reviews/checks and exact-head human approval. The
   owner comment alone, an unmerged branch head or proposed ADR cannot satisfy this.
5. After the dependency exists, amend this phase with the exact merged input paths/hashes/commands
   and any actually required mapping, then run fresh independent validation and Stage B readiness.
   This current phase cannot be cooked merely because the dependency later appears.
6. Local = tracking = freshly fetched live remote at the authorized Stage B input; tree clean; the
   Issue #8 shared-contract lease remains exclusive.

Until every condition passes and the amended phase is revalidated/readiness-authorized, Phase 6
status is `blocked-on-issue-7-merged-sha` and `cookable: false`; it has an empty implementation
allow-list. No binding file, placeholder adapter, guessed path/hash/command, copied preview
contract or framework workaround is permitted.

## Requirements

- Functional: read exact merged Issue #7 Vite ADR/handoff, Vite manifest/lock and common-contract
  source as read-only inputs; record their real hashes and merge SHA in the binding handoff.
- Functional after amendment: derive only the minimum consumer representation actually required
  by the accepted handoff for Stage A contract IDs, versions, operation IDs and content hashes.
- Functional after amendment: if a binding manifest is actually required, map each selected-stack
  view/field/action to one Stage A schema/ref/operation without changing semantics or canonical
  bytes; direct consumption is preferred and requires no adapter artifact.
- Functional: no adapter is planned in advance. If the exact merged handoff cannot consume Stage A
  IDs/hashes directly, stop and amend/revalidate a concrete lossless mapping or additive Stage A
  version; do not infer one from provisional preview bytes.
- Non-functional: no runtime validator fork, alternate canonicalizer, copied schema/default,
  second completion rule, package workspace or invented dependency/tool. Use only the exact
  runtime/lock/tool surface named by the accepted handoff after revalidation.

## Architecture

If the accepted handoff requires a generated consumer binding, it is not a contract version:

```text
Stage A contract set (source of truth)
    ├── schema IDs / versions / hashes
    ├── OpenAPI operation IDs / paths
    └── completion/evidence canonical rules
             |
             v
  dependency-defined read-only consumer representation
             |
             v
  binding manifest with exact Issue #7 merge/lock/source hashes
```

Any generated representation may contain immutable IDs/hashes only. Its exact format is not chosen
here. Runtime boundary validation remains the Stage A validator and future portal/runner adapters.
A browser hint, cache state or preview view cannot mutate completion. If the Vite consumer needs
different fields or canonical behavior, the future compatibility check fails and a separately
planned additive Stage A version is required.

## Related Code Files

Current implementation allow-list: **empty**. No Stage B create/modify/read path is authorized.
After the exact merged handoff exists, an amendment must name every Issue #8-owned output/test path,
every read-only Issue #7 input, and any Stage A checker integration separately. A released
`learning-contract-set-v1.json` remains immutable; any final handoff must hash the Stage A set and
any separately released binding without rewriting Stage A. Current unmerged Issue #7 implementation
and ADR paths are non-authoritative and must not be read or edited by Issue #8.

## Tests Before

Write/freeze these failures after the real dependency handoff is available and before binding:

- missing/unmerged/wrong Issue #7 merge SHA or ancestry;
- ADR not Accepted/Vite, dependency path/hash/lock/tool/command mismatch;
- missing/extra/renamed schema ID, version, operation ID, field/action mapping;
- copied/divergent schema/default/canonicalizer/completion authority;
- stale Stage A contract set or binding regenerated from dirty/uncommitted bytes;
- selected runtime, lock or tool not exactly manifest-admitted.

Retain the expected failures with exact Stage A and Issue #7 identities before generating binding
bytes. No test may hard-code a guessed future SHA.

## Refactor

After amendment, any generation must be deterministic from sorted Stage A IDs/hashes and the
operation matrix, with no hand-authored contract semantics. Keep dependency provenance outside
schema IDs and do not alter released Stage A files. The exact output format remains unset now.

## Tests After and Final Blast Radius

No Stage B command is authorized by this version of the phase. The amendment must repeat all
Stage A primary/blast-radius commands and copy the exact required Vite install/test/build/smoke/
security commands from the accepted merged Issue #7 handoff. It must not invent a Node, browser,
accessibility or package-manager command. Evidence will record each admitted command and exit
status; any missing handoff-required runtime/tool/artifact is `fail`, not skip.

Re-run:

- Stage A canonical hashes and results byte-for-byte;
- any amended generation twice in separate temp roots;
- the amended Vite direct-consumption or binding mapping against only the exact merged handoff;
- no-network/no-cloud-credential and S3 secret/private-path scans;
- changed-path/protected hash/Issue #7 read-only checks;
- rollback removing only the binding selection while Stage A stays readable.

## Implementation Steps

1. Fresh-fetch and verify the hard entry gate, real merge/ADR/handoff/lock/tool/command identities
   and exclusive lease.
2. Add binding RED tests tied to the real dependency identity.
3. Amend and revalidate the exact Issue #8 output format/paths, read-only dependency paths, tests,
   tools and commands; direct consumption may make an adapter unnecessary.
4. Only after fresh readiness, generate any authorized representation from the Stage A contract set
   and operation matrix and validate it without changing Stage A output.
5. Close the amended binding tests and run the complete Issue #8 + Issue #6 + accepted Vite blast
   radius at one exact clean committed head.
6. Rehearse binding-only rollback and prove Stage A remains usable/readable.
7. Require fresh independent exact-head read-only review, repository checks and separate human
   exact-head approval; then publish non-recursive final evidence and the external final contract
   release SHA. No tracked file claims its own commit.
8. Hand downstream owners the exact Stage A set hash, binding hash, Issue #7 merge SHA, final
   contract release SHA, commands, compatibility/rollback result and remaining residual risks.

## Success Criteria

- [ ] Exact accepted merged Issue #7 Vite handoff—not owner direction/provisional bytes—is consumed.
- [ ] Direct consumption or any dependency-required binding maps every Stage A
  schema/version/operation/hash exactly and losslessly.
- [ ] Any dependency-required generated output is deterministic and contains no parallel
  schema/state logic.
- [ ] Stage A canonical bytes, operation matrix, completion authority and migration rules do not drift.
- [ ] Issue #8, Issue #6 and accepted Vite blast-radius commands pass at one exact head.
- [ ] Binding rollback leaves Stage A and retained evidence intact.
- [ ] Final external contract release SHA and exact-head human approval are recorded truthfully.

## Risk Assessment

- The future Issue #7 handoff may use different paths/commands than today’s unmerged branch.
  Mitigation: do not freeze them here; readiness compares and amends/revalidates before cook.
- A generated consumer representation can imply runtime validation. Mitigation: immutable IDs/
  hashes only; boundary validation remains the Stage A source contract.
- Updating the Stage A release set after staged merge would rewrite a released artifact. Mitigation:
  hash Stage A set and binding as two immutable components in external final handoff.

## Security and Rollback

Issue #7 paths are strictly read-only. Stage B evidence is scanned for dependency secrets, local
paths, bundle/source-map leakage and recursive identities. Rollback deselects/removes only the
Stage B consumer selection through a reviewed additive change; never rewrites Stage A schemas/evidence,
Issue #7 sources, old readers or fixtures.

## Next Steps

After final release, downstream issues consume the exact externally attested contract release SHA
read-only. No downstream cook or merge is authorized by this phase; each issue retains its own
dependency, validation, readiness and human gates.
