---
phase: 4
title: "Stage A evidence and bounded handoff"
status: pending
priority: P1
dependencies: [3]
effort: "M"
---

# Phase 4: Stage A evidence and bounded handoff

<!-- Updated: Validation Session 1 - made evidence compatibility and the immutable run index explicit. -->

## Context Links

- [Verification, Evidence, and Protected Assets](./verification-evidence-and-protected-assets.md)
- [Threat Model](./threat-model-and-security.md)
- [Dependency Gates](./dependency-and-release-gates.md)

## Overview

Prove the future readiness-authorized Stage A candidate is contract-valid, trace-complete,
deterministic, evidence-backed, rollback-safe, and restricted to static claims. Stage A may be
reviewed or later merged only under its exact readiness and human gates; it does not unlock Stage B
automatically.

This phase remains blocked; it becomes eligible only after fresh plan validation/readiness and
Phases 1–3 pass at the exact future candidate tree.

## Requirements

- Functional: collect RED/GREEN/static/render/trace/security/protected/rollback evidence.
- Non-functional: exact hashes/commands/tools/dependencies; bounded output; immutable prior runs;
  clean exact-head handoff.
- Security: no sensitive content, no runtime/portal/cloud claim, evidence-preserving rollback.

## Architecture

Evidence is produced under ignored app-owned
`.claude/evidence/issue-11-stage-a/<run-id>/` or an auditor-approved external mode-0700 root. The
old nonignored `.artifacts/**` location is forbidden. Evidence uses `fitness-result-v1` command
envelopes, not Issue #8 learner evidence, and distinguishes plan input, scaffold, tests, RED tree,
first semantic commit, final semantic head, optional attestation commit, and external merge/
approval. A closed `index.json` + `index.sha256` envelope rejects missing, duplicate, orphaned,
unindexed, stale, or recursively self-hashed bytes. Stage A never synthesizes an
`architecture-lab-e2e` or portal `architecture-visual-review` pass.

## Related Code Files

- Future candidate tracked Create: exact proposed amendment paths only after Gate A2; Modify/Delete:
  none (`[]`).
- Evidence is bounded runtime/local state and is never staged by this authority.

## Implementation Steps

1. Repeat dependency, lease, exact allow-list, and protected preflight.
2. Audit commit chronology and evidence: exact seven-path scaffold, direct-child five-path tests,
   `scaffold-plus-tests semantic RED` through all four entrypoints, then semantic commits; reject
   tests-only-from-pristine or precondition-only claims.
3. Run the exact 16 Stage A command shapes in order and enforce the 120-second focused and one
   180-second whole sequential expansion deadline, owned process groups, TERM→KILL→wait,
   aggregate RSS/output/file/process bounds, and complete measurements.
4. Verify all RED fixtures still fail and all valid content passes, including frozen promotion,
   template registry/bindings, 11 critical flows, deployment/bridge claims, resource and cleanup.
5. Render expansion twice in isolated roots; verify semantic/text/byte determinism and mutation
   sensitivity; run exact static geometry/fit/font/contrast/language/numbering/parity gates and
   compare protected six hashes/blobs/rows/paths.
6. Require a fresh independent human inspection of all five new SVGs at fitted widths 1440 and
   1024, with per-view readability, overlap, clipping, off-canvas, ordering, contrast and language
   disposition. This is distinct from the blocked portal visual command.
7. Generate reciprocal trace coverage for every module/template/view/ADR/pattern/test/evidence
   and operations consequence.
8. Run S3 scans over source, generated render/text, evidence metadata, logs, and staged diff.
9. Rehearse rollback: restore the exact pre-Stage-A tracked set, preserve evidence, prove protected
   and unrelated bytes unchanged, then reapply/reverify the candidate only if the authorized
   workflow supports a deterministic reconstruction.
10. Run `clean-handoff`: require zero-byte stdout from nonignored porcelain, then parse the NUL-
    terminated ignored-inclusive inventory and classify every entry as pre-existing unchanged or
    exact owned retained evidence. Exit 0 alone is not a cleanliness result.
11. Prove only Issue #11 temporary workspace/render staging was removed; retain failure and
    rollback evidence under privacy modes and a closed index.
12. Require independent implementation review and human exact-head pre-merge approval before any
   future Stage A merge. This phase cannot generate either approval itself.
13. Publish a bounded handoff stating: static candidate only; portal/lab/reset/completion/fresh
    learner evidence not delivered; Stage B still blocked on passing merged #10. Classify
    user-facing docs/release-note impact and route any required `README.md`, `docs/**`, or release
    metadata change to a separate owner-authorized serialized handoff.

## Tests Before

- Evidence schema/canonicalization/tamper/stale-dependency mutations from exact #8.
- Protected-manifest mismatch, incomplete rollback, sensitive-content, and false Stage A runtime
  claim negatives.

## Tests After

- Exact evidence schema/hash verification.
- All required Stage A commands and artifacts present; no Stage B result.
- Protected/deny-list/staged-path, zero-byte nonignored porcelain, and ignored-inclusive ownership
  checks.
- Rollback result proves no protected/evidence/unrelated loss.

## Regression Gate

Future readiness-authorized Stage A command list plus static checks. The immutable command name
`architecture-lab-e2e` remains excluded and unclaimed.

## Success Criteria

- [ ] Scaffold/tests/RED/semantic/GREEN/static/render/trace/security/resource/visual/rollback
      evidence is complete at exact tested tree.
- [ ] I5-06 command evidence uses the existing `fitness-result-v1` registry contract; released
      `fitness-result-v2`, learner evidence, progress, and completion remain non-authorities.
- [ ] The immutable run index is complete and rejects missing, duplicate, orphaned, stale, or
      tampered results/artifacts.
- [ ] Protected six and dependency/portal/root/cloud deny-list remain unchanged.
- [ ] Cleanup and rollback preserve prior evidence and unrelated state.
- [ ] Retained evidence is ignored/app-owned or external, private, closed-indexed and honestly
      separated from zero-record worktree cleanliness.
- [ ] Stage A handoff explicitly denies portal/executable/completion claims.
- [ ] Docs/release impact is recorded without adding external-owner paths to Stage A authority.
- [ ] Stage B remains blocked until a separate exact amendment/revalidation/readiness.

## Risk Assessment

The largest risk is evidence overclaim. Keep Stage A result taxonomy explicit and reject any
runtime field that implies an executed lab. Rollback is removal/restoration of Issue #11-owned
candidate bytes only; no dependency history rewrite.

## Security Considerations

Local hashes provide corruption detection, not non-repudiation. Human approval is external and
exact-head; it cannot be inferred from passing evidence.

## Next Steps

Wait for exact passing merged Issue #10 real journey/renderer. Then repeat Phase 1 as Phase 5; do
not carry Stage A cook authority into Stage B.
