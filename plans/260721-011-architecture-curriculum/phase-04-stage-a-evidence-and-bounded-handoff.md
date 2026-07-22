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

Prove the exact-authorized Stage A candidate is contract-valid, trace-complete, deterministic,
evidence-backed, rollback-safe, and restricted to static claims. Stage A may be reviewed or later
merged only under its exact readiness and human gates; it does not unlock Stage B automatically.

This phase is ready to cook only after Phases 1–3 pass at the exact candidate tree.

## Requirements

- Functional: collect RED/GREEN/static/render/trace/security/protected/rollback evidence.
- Non-functional: exact hashes/commands/tools/dependencies; bounded output; immutable prior runs;
  clean exact-head handoff.
- Security: no sensitive content, no runtime/portal/cloud claim, evidence-preserving rollback.

## Architecture

Evidence is produced under the amendment's two I5-06 run-owned roots and the existing protected
architecture evidence roots. It uses `fitness-result-v1` command envelopes, not Issue #8 learner
evidence. It distinguishes input, tested tree, optional attestation commit, and external merge/
approval. One closed immutable run index enumerates every required result/artifact and byte hash;
missing, duplicate, orphaned, or unindexed bytes fail. Stage A never synthesizes an
`architecture-lab-e2e` or `architecture-visual-review` pass.

## Related Code Files

- Current tracked Create: exact amendment paths only; Modify/Delete: none (`[]`).
- Evidence is bounded runtime/local state and is never staged by this authority.

## Implementation Steps

1. Repeat dependency, lease, exact allow-list, and protected preflight.
2. Run the exact Stage A static command subset from the amendment in the recorded order and with
   exact tool/time/resource/output bounds.
3. Verify all RED fixtures still fail and all valid content passes.
4. Render expansion twice in isolated roots; verify semantic/text/byte determinism and mutation
   sensitivity; compare protected six hashes/blobs/rows/paths.
5. Generate reciprocal trace coverage for every module/template/view/ADR/pattern/test/evidence
   and operations consequence.
6. Run S3 scans over source, generated render/text, evidence metadata, logs, and staged diff.
7. Rehearse rollback: restore the exact pre-Stage-A tracked set, preserve evidence, prove protected
   and unrelated bytes unchanged, then reapply/reverify the candidate only if the authorized
   workflow supports a deterministic reconstruction.
8. Record cleanup ownership and prove only Issue #11 temporary workspace/render staging was
   removed; retain failure and rollback evidence.
9. Require independent implementation review and human exact-head pre-merge approval before any
   future Stage A merge. This phase cannot generate either approval itself.
10. Publish a bounded handoff stating: static candidate only; portal/lab/reset/completion/fresh
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
- Protected/deny-list/staged-path/clean-status checks.
- Rollback result proves no protected/evidence/unrelated loss.

## Regression Gate

Exact Stage A amendment-authorized command list plus static checks. The immutable command name
`architecture-lab-e2e` remains excluded and unclaimed.

## Success Criteria

- [ ] RED/GREEN/static/render/trace/security/rollback evidence is complete at exact tested tree.
- [ ] I5-06 command evidence uses the existing `fitness-result-v1` registry contract; released
      `fitness-result-v2`, learner evidence, progress, and completion remain non-authorities.
- [ ] The immutable run index is complete and rejects missing, duplicate, orphaned, stale, or
      tampered results/artifacts.
- [ ] Protected six and dependency/portal/root/cloud deny-list remain unchanged.
- [ ] Cleanup and rollback preserve prior evidence and unrelated state.
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
