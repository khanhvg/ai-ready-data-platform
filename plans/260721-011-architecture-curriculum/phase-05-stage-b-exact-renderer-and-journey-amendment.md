---
phase: 5
title: "Stage B exact renderer and journey amendment"
status: pending
priority: P1
dependencies: [4]
effort: "Gate; blocked on Issue #10"
---

# Phase 5: Stage B exact renderer and journey amendment

## Context Links

- [Dependency and Release Gates](./dependency-and-release-gates.md)
- [Architecture and Curriculum Design](./architecture-and-curriculum-design.md)
- [Threat Model](./threat-model-and-security.md)

## Overview

Create a new exact Stage B authority only after Stage A is accepted and Issue #10 publishes a
passing merged real journey plus released portal renderer. This phase resolves exact content
discovery, rendering, lifecycle, reset, verifier, evidence, completion, and cleanup seams without
editing portal source or duplicating Issue #8/#10 truth.

At the current planner output this phase is hard-blocked and has no file or command authority.
The post-review Stage A amendment passed independent validation but still awaits readiness, so even
an Issue #10 release cannot advance this phase until the corrected Stage A plan and implementation
have separately passed their gates.

## Requirements

- Functional: pin exact #10 merge/renderer/journey and current #8/Stage A release; derive closed
  Stage B paths/commands/tests.
- Non-functional: same exact-head amendment/revalidation/readiness chain; no guessed routes,
  modules, viewports, schemas, errors, or fallbacks.
- Security: browser/renderer/private execution boundary and evidence authority remain released
  owner truth; no portal-source overlap.

## Architecture

Stage B is a consumer integration:

```text
Issue #11 lab/content
  -> released Issue #10 content discovery + renderer
  -> released portal/BFF journey boundary
  -> released Issue #8 lifecycle/verification/evidence/completion
```

No arrow authorizes Issue #11 to copy or modify the target component.

## Related Code Files

- Current Create/Modify/Delete: none (`[]`).
- Later Stage B amendment must enumerate exact Issue #11 lab/publication paths and every
  read-only #8/#10 dependency path/hash. Portal/shared-contract files remain excluded.

## Implementation Steps

1. Fetch and verify exact passing merged Issue #10 real-journey/renderer release and exact current
   Issue #8/Stage A releases, including the validated scaffold/tests/RED/semantic provenance and
   clean ignored-root evidence disposition introduced by the corrected Stage A amendment.
2. Verify #10 evidence includes real controlled failure, reset, fresh verify, completion/evidence,
   dependency hashes, renderer build/test, cleanup, review, and human approval at the merge head.
3. Copy exact renderer/content-discovery/registry/publication paths, versions, hashes, accepted
   content types, safe rendering rules, error/unavailable/static/no-JS semantics, and test commands
   into the amendment.
4. Copy exact #8 lifecycle, prerequisite, hint, reset, verifier, evidence, completion, and
   reconciliation bindings; do not infer field names from Stage A content.
5. Prove a new architecture lab can register/publish through released seams with Issue #11-owned
   content only. If a portal edit is required, stop for separate serialized authority.
6. Derive exact Stage B file/command/test/evidence/cleanup allow-lists and resource/output bounds.
7. Update threat/trace/rollback mapping for renderer injection, history/reload, duplicate request,
   process kill, stale/tampered evidence, unavailable tool, and solution/reflection bypass.
8. Run fresh independent validation and fresh readiness at the amended exact head.
9. Before first Stage B write, repeat all release/blob/hash/lease/protected/remote checks.

## Tests Before

- Wrong/stale #10 SHA; renderer path/hash drift; missing real-journey evidence; direct portal edit;
  missing #8 completion/reset field; conflicting content ID; unsafe content; duplicated route/
  schema; empty Stage B authority.
- All fail before any lab/publication write.

## Tests After

- Amendment frontmatter/authority consistency.
- Exact #8/#10/Stage A release and blob verification.
- Read-only dependency imports and zero portal/shared-contract diff.
- Independent validation/readiness reference the same exact amendment head.

## Regression Gate

No implementation command is legal now. Stage B readiness must publish the exact command list,
including the full practical acceptance line, before Phase 6.

## Success Criteria

- [ ] Exact passing merged Issue #10 journey/renderer and exact #8/Stage A releases are pinned.
- [ ] Content registration/publication needs no portal/shared-contract write.
- [ ] Stage B file/command/test/evidence authority is closed and non-empty.
- [ ] Exact released lifecycle/error/security/renderer semantics replace all unknowns.
- [ ] Fresh independent validation and readiness authorize one exact Stage B input.

## Risk Assessment

Main risk is treating the Issue #10 plan as renderer API documentation. Only released blobs and
passing evidence count. If the released renderer lacks a content seam, the correct outcome is
blocked scope expansion, not a guessed adapter.

## Security Considerations

Reject browser-direct runner access, privileged tokens in client storage/content, unsafe raw HTML,
wildcard CORS, or completion derived from client/reflection/solution state.

## Next Steps

Proceed to Phase 6 only at exact Stage B readiness input.
