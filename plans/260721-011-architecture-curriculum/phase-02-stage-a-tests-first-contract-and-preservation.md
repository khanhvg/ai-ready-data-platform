---
phase: 2
title: "Stage A tests-first contract and preservation"
status: pending
priority: P1
dependencies: [1]
effort: "M after Stage A readiness"
---

# Phase 2: Stage A tests-first contract and preservation

<!-- Updated: Validation Session 1 - added template-version and evidence-index RED obligations. -->

## Context Links

- [Plan](./plan.md)
- [Architecture and Curriculum Design](./architecture-and-curriculum-design.md)
- [Threat Model](./threat-model-and-security.md)
- [Verification and Protected Assets](./verification-evidence-and-protected-assets.md)

## Overview

Under a future exact Stage A readiness output, write every required broken fixture before
curriculum/template/static expansion behavior. Prove the exact released Issue #8 consumer
boundary and freeze Issue #6 local architecture bytes, rows, IDs, semantics, and renders.

At the current planner output this phase is blocked and has no file or command authority.

## Requirements

- Functional: RED cases for reference, prerequisite, view, ADR, pattern-without-failure,
  traceability, render, read-only protection, API/channel admission, and S3 scans.
- Non-functional: deterministic failure codes; bounded fixtures; no fake pass; exact contract
  versions/hashes; protected pre-state captured before any behavior write.
- Security: negative content/path/secret/cloud-action/render cases fail before publication.

## Architecture

Tests consume released Issue #8 validators and the lease-bound architecture extension seam. They
do not copy validators or modify Issue #6 checkers/tool locks. RED evidence is staged separately
from implementation output and binds the exact input/dependency/tool hashes.

## Related Code Files

- Current Create/Modify/Delete: none (`[]`).
- Future exact test/fixture paths must be enumerated by the Stage A amendment; “tests somewhere
  under the repository” or a wildcard outside the ownership ceiling is invalid.

## Implementation Steps

1. Re-run Phase 1 preflight and capture exact Stage A authority plus protected pre-hashes/blob IDs.
2. Instantiate amendment-authorized fixtures for `I11-RED-REF-001`, `I11-RED-PREQ-001`,
   `I11-RED-VIEW-001`, `I11-RED-ADR-001`, `I11-RED-PATTERN-001`, `I11-RED-TRACE-001`,
   `I11-RED-RENDER-001`, `I11-RED-READONLY-001`, `I11-RED-API-001`, and `I11-RED-S3-001`.
3. Use exact released Issue #8 examples only when the release explicitly permits fixture
   consumption. Never carry ignored or another worktree’s runtime fixture.
4. Assert every fixture fails for its named semantic reason. A parser crash, missing tool, or
   unrelated schema error does not satisfy RED.
5. Add prerequisite graph mutations: unknown/self/cycle/unreachable/forged skip/optional-as-pass.
6. Add trace mutations across every business-to-operations link and reciprocal edge.
7. Add pattern mutations, including the mandatory plausible pattern with no failure/verifier.
8. Add view/render mutations for ID/key/path overlap, missing concern/text, stale output,
   nondeterminism, semantic erasure, script/external URL/private path, and protected byte drift.
9. Add OpenAPI/AsyncAPI teaching admission mutations: no real operation/channel and logical
   taxonomy misrepresented as physical services.
10. Record failing assertion IDs, exit status, bounded output hashes, input/dependency/tool hashes,
    and protected pre-state before any implementation behavior changes.
11. Add template identity/version/supersession mutations and evidence-index missing/duplicate/
    orphan/tamper mutations under the existing stable reference/trace fixture classes.

## Tests Before

All ten `I11-RED-*` fixture classes above. This entire phase is tests-before; no production
curriculum/template/view expansion is written until the RED bundle is complete.

## Refactor

None. Do not refactor Issue #6 sources/checkers or released Issue #8 contracts. If the exact
extension seam cannot host the fixtures without a protected edit, stop and return to Phase 1.

## Tests After

After Phase 3, rerun every fixture and prove each remains rejected while the matching valid
content passes. Compare protected hashes/blobs and ensure no test weakens an existing six-view
assertion.

## Regression Gate

Exact future command(s) come only from the Stage A amendment. The final acceptance names
`curriculum-check`, `architecture-check`, `architecture-render`, and `traceability-check`, but
those names are not current authority.

## Success Criteria

- [ ] Every required failure fixture fails for the intended stable reason before behavior writes.
- [ ] RED evidence binds exact stage input, #8 release, tool/fixture hashes, and protected baseline.
- [ ] No protected/shared/portal/root/cloud path changes.
- [ ] No fixture uses fake data, ignored state, or duplicate contract truth.
- [ ] Stage A remains non-runtime and makes no lab/portal/completion claim.

## Risk Assessment

Fixtures can overfit syntax instead of architecture semantics. Require semantic mutation classes
and reciprocal trace checks. If a released validator cannot express a required assertion, stop
for amendment/contract-owner resolution; do not add a shadow validator.

## Security Considerations

Malicious fixture bytes stay bounded and isolated. Secret/path canaries are synthetic and must
never resemble live credentials. Failure output is scanned before retention.

## Next Steps

Proceed to Phase 3 only with complete RED evidence and unchanged protected bytes.
