---
phase: 6
title: "Prove S3 evidence rollback and handoff"
status: pending
priority: P1
dependencies: [5]
effort: "1.5 implementation days plus independent review"
---

# Phase 6: Prove S3 Evidence, Rollback, and Handoff

## Overview

Finalize only the three issue-owned Make targets, run the exact verification and S3 scans, emit the
released evidence envelopes, rehearse safe rollback, and prepare two independent exact-head review
handoffs plus human approval. This phase creates no PR/merge/cloud action by implication.

This phase remains unreachable while the capability amendment is `BLOCKED`; no gate or evidence
may claim an all-eight lifecycle until exact dbt runs under the admitted zero-descendant backend.

## Context Links

- [Exact commands and S3 scans](./verification-evidence-and-rollback.md#exact-future-commands)
- [Evidence layout](./verification-evidence-and-rollback.md#evidence-layout-and-manifest)
- [Rollback](./verification-evidence-and-rollback.md#rollback-procedure)
- [RUN-EVD/GATE/ROL/APP](./requirements-risk-threat-traceability.md#requirement-crosswalk)

## Requirements

- `mk/issue-5/i5-04.mk` exposes exactly three non-interactive required gates.
- Every gate uses the pinned app environment and emits a valid activated `fitness-result-v2`
  envelope with bounded hashed runner-detail artifacts.
- Exact aggregate commands and S3 static/dependency/policy/secret/protected scans pass.
- Rollback stops/removes only proven runner-owned mutable state and preserves evidence/expert paths.
- Two fresh independent reviews in separate contexts, each bound to the same exact remote head,
  and a separate human approval of that exact head remain mandatory before merge.

## Related Code Files

- Extend: `apps/lab-runner/tools/run-gate.py` created as test-only gate scaffolding in Phase 3
- Rehash/validate: `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`
- Extend: `apps/lab-runner/src/lab_runner/evidence.py` created in Phase 5
- Create: `apps/lab-runner/tests/integration/test_{evidence_manifest,rollback,full_runner_flow}.py`
- Create: `apps/lab-runner/README.md`
- Extend only if required for final gate wiring: `mk/issue-5/i5-04.mk` created in Phase 3; it must
  still own exactly the same three targets, and any change requires RED re-attestation
- Extend: app-owned gate/test/config files only
- Consume read-only: released command-owner/evidence contracts and I5-01 `data-contracts-check`
- Modify/Delete: none outside the issue-owned paths

## Tests Before

1. Add failing manifest tests for missing command/tool/SHA/dependency/hash/assertion/artifact/
   redaction/rollback data, duplicate JSON names, unknown fields and recursive commit claims.
2. Add failing Make ownership tests for extra/missing targets, interactive behavior, wrong evidence
   root, registry mismatch and hidden skip.
3. Add rollback attacks: forged/wrong marker, symlink, device/inode/mount change, foreign PID,
   current evidence reference, expert namespace and repeated rollback.

## Implementation Steps

1. Complete `run-gate.py` so it verifies supported host/dependency/lock/source state, bootstraps the
   private pinned environment, generates a run ID, dispatches one fixed suite, validates evidence,
   and returns exact non-zero status on failure.
2. Recompute the Phase 3 fragment and activation-instance hashes from actual bytes and update only
   the Issue #9 lock/instance when necessary. Preserve exactly the three Make recipes. No root
   Make/help edit or shared activation file.
3. Build structured gate evidence under `.artifacts/evidence/runner/<run-id>/`, canonicalize and
   validate each public envelope against released `fitness-result-v2` plus the exact activation,
   validate learner verification against `learning-evidence-v1`, and hash every retained artifact.
4. Run compile, Bandit, pip-audit and app-owned AST/policy/credential/private-path/protected-path/
   no-Terraform/no-cloud scans with pinned tools. Treat required missing tools or unsanctioned
   suppression as failure.
5. Execute the exact commands individually and as the requested aggregate:
   `make runner-test runner-security-test runner-race-test data-contracts-check`.
6. Run one bounded real `small`/42 lifecycle through eight reviewed in-process adapters with
   `deny process-fork`, all eleven assets, verification, repeated reset/restart, exact worker
   PID/start reap, zero descendants and final base/pointer/evidence checks.
7. Rehearse rollback twice, including active/incomplete/crashed states and adversarial foreign
   markers. Restore only a previously validated pointer; preserve evidence/audit.
8. From a fresh clean checkout of the exact candidate head, run final changed-path/protected-hash/
   secret/private-path/Git cleanliness checks and the full required gate; retain the exact evidence
   index without runner state outside the owned artifact roots.
9. Run two fresh independent exact-head reviews in separate contexts/checkouts: Review A focuses
   correctness/contracts/TDD/recovery and Review B focuses S3/containment/race/evidence/rollback.
   Both must report zero unresolved Critical/High findings at the identical remote head.
10. After both independent PASS results, re-prove remote head equality and obtain separate human
    approval of that exact head. Any code change invalidates both reviews and approval.

## Refactor

Consolidate only app-owned evidence manifest construction and gate bootstrapping. Do not replace
I5-01 evidence/data commands or Issue #8 schema/registry validators.

## Tests After

- Validate every pass/fail manifest and artifact hash from a clean tested tree.
- Prove required failures remain non-zero and preserve bounded sanitized evidence.
- Run rollback twice and confirm no owned process/socket/temp state, while evidence and expert
  namespace remain.
- Re-run exact four commands after rollback/re-enable rehearsal.

## Regression Gate

```bash
make runner-test
make runner-security-test
make runner-race-test
make data-contracts-check
git diff --check
```

All commands must pass at the exact tested tree. S3 scans and manifest/rollback checks are required
sub-gates, not optional commentary.

## Risk and Security

Evidence can become a second secret channel. Persist only released allow-listed fields, bounded
sanitized previews and hashes. A detected canary/private path fails publication. Rollback ambiguity
preserves state for manual inspection; it never broadens deletion authority.

## Success Criteria

- [ ] Exact four-command gate and all S3 scans pass with valid evidence.
- [ ] Rollback/recovery is idempotent, narrow and evidence-preserving.
- [ ] Changed paths remain within authority and contracts/data semantics remain unchanged.
- [ ] Two fresh independent exact-head reviews have zero unresolved Critical/High findings.
- [ ] Human exact-head pre-merge approval is recorded before any merge.

## Next Steps

End this issue's implementation pipeline at reviewed/approved handoff. PR creation, merge, portal
integration, Issue #10 work and any release transition require their own authorized phases.
