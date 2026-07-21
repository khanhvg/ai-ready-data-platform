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

Wire only the three issue-owned Make targets, run the exact verification and S3 scans, emit the
released evidence manifest, rehearse safe rollback, and prepare an exact-head independent review/
human-approval handoff. This phase creates no PR/merge/cloud action by implication.

## Context Links

- [Exact commands and S3 scans](./verification-evidence-and-rollback.md#exact-future-commands)
- [Evidence layout](./verification-evidence-and-rollback.md#evidence-layout-and-manifest)
- [Rollback](./verification-evidence-and-rollback.md#rollback-procedure)
- [RUN-EVD/GATE/ROL/APP](./requirements-risk-threat-traceability.md#requirement-crosswalk)

## Requirements

- `mk/issue-5/i5-04.mk` exposes exactly three non-interactive required gates.
- Every gate uses the pinned app environment and emits valid Issue #8 evidence.
- Exact aggregate commands and S3 static/dependency/policy/secret/protected scans pass.
- Rollback stops/removes only proven runner-owned mutable state and preserves evidence/expert paths.
- Independent code/security review and exact-head human approval remain mandatory before merge.

## Related Code Files

- Create: `apps/lab-runner/tools/run-gate.py`
- Create: `apps/lab-runner/src/lab_runner/evidence.py`
- Create: `apps/lab-runner/tests/integration/test_{evidence_manifest,rollback,full_runner_flow}.py`
- Create: `apps/lab-runner/README.md`
- Create: `mk/issue-5/i5-04.mk`
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

1. Implement `run-gate.py` to verify supported host/dependency/lock/source state, bootstrap the
   private pinned environment, generate a run ID, dispatch one fixed suite, validate evidence and
   return exact non-zero status on failure.
2. Add the three Make recipes only. No root Make/help edit; consume the exact Issue #8-released
   command-owner activation seam.
3. Build structured gate evidence under `.artifacts/evidence/runner/<run-id>/`, canonicalize and
   validate it against the released schema, and hash every retained artifact.
4. Run compile, Bandit, pip-audit and app-owned AST/policy/credential/private-path/protected-path/
   no-Terraform/no-cloud scans with pinned tools. Treat required missing tools or unsanctioned
   suppression as failure.
5. Execute the exact commands individually and as the requested aggregate:
   `make runner-test runner-security-test runner-race-test data-contracts-check`.
6. Run one bounded real `small`/42 lifecycle with containment, all eleven assets, verification,
   repeated reset/restart and final process/base/pointer/evidence checks.
7. Rehearse rollback twice, including active/incomplete/crashed states and adversarial foreign
   markers. Restore only a previously validated pointer; preserve evidence/audit.
8. Run final changed-path/protected-hash/secret/private-path/Git cleanliness checks and prepare the
   exact evidence index for fresh independent code/security review.
9. After independent PASS, prove remote PR head equality and obtain human approval of that exact
   head. Any code change invalidates review/approval and returns to review.

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
- [ ] Independent review has zero unresolved Critical/High findings.
- [ ] Human exact-head pre-merge approval is recorded before any merge.

## Next Steps

End this issue's implementation pipeline at reviewed/approved handoff. PR creation, merge, portal
integration, Issue #10 work and any release transition require their own authorized phases.
