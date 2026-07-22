---
phase: 7
title: "Verification Evidence Rollback and Human Gates"
status: pending
priority: P1
dependencies: [6]
effort: "M"
---

# Phase 7: Verification Evidence Rollback and Human Gates

<!-- Updated: Validation Session 1 - required clean-checkout replay and explicit amended S3 scans. -->

## Context links

- [Future verification contract](./implementation-handoff.md#required-future-verification)
- [Evidence and rollback](./security-recovery-and-evidence.md)
- [Acceptance criteria](./plan.md#acceptance-criteria)
- [Protected baseline](./protected-input-baseline.md)

## Overview

Run the complete deterministic Issue #14 gate, exact Issue #6/#11 blast radius, evidence
finalization, rollback rehearsal and independent human handoff. Apply-blocking TBCs may leave the
decision boundary `blocked-tbc`; they can never be suppressed to claim AWS readiness.

## Requirements

- Functional: all FR-001..020.
- Non-functional: all NFR-001..014.
- Required targets and exact dependency blast radius run at one clean exact tested tree and replay
  from a fresh clean checkout of that tree.
- Evidence and rollback remain compact, redacted, hash-indexed and repeatable offline.
- Independent exact-head review and human pre-merge approval remain external gates.

## Architecture

```text
clean exact head -> required offline targets + dependency/protected blast radius + S3 scans
  -> fresh clean-checkout replay of the exact tested tree
  -> evidence manifest/hash/redaction/replay verification
  -> issue-owned rollback rehearsal -> exact-head independent review
  -> human pre-merge approval -> merge workflow
  -> separate later cloud/apply authorization (not this phase)
```

Exit code, local hash, or planner assertion alone is insufficient. GitHub remote SHA, comment,
labels and clean tracking equality are part of publication; implementation completion additionally
requires independent review and human approval.

## Related code files

- Current implementation allow-list: `[]`.
- Exact implemented files/evidence schemas and blast-radius paths: amendment-owned `TBC`.
- Evidence is generated only below `.artifacts/evidence/aws-decisions/<run-id>/` and is not
  broadly staged by default.
- No AWS/Terraform/PR/merge action is part of the offline command gate itself.

## Tests before

- Missing required target/tool/evidence/artifact/hash/rollback result.
- Foreign input/tested-tree/dependency/model/snapshot/topology hash.
- Extra/missing/duplicate artifact, non-canonical bytes, replayed/expired authority.
- Sensitive/account/private/PII canary or absolute locator in evidence.
- Protected path/hash/absence drift or changed path outside exact allow-list.
- Clean-checkout replay drift or an S3 scan that misses credential/account/private-path/PII,
  malicious input, unsafe command/path, link/special-file, protected-scope, or tamper/replay cases.
- Rollback removes evidence, prior ADR/snapshot, protected/unrelated file, or leaves command drift.
- Human approval/comment references a different exact head.

## Refactor

Do not weaken tests or statuses to close TBCs. If aggregate output exposes inconsistency, correct
the canonical upstream model and rerun all affected gates; do not patch the report projection.

## Tests after

- All required deterministic target groups pass or correctly return `blocked-tbc` for only the
  declared apply boundary.
- Optional live source refresh is clearly `not-run-optional` and cannot satisfy required gates.
- Exact Issue #6 and released Issue #11 hashes/commands/semantics and the named S3 scans pass from
  the amended contract.
- The complete required suite replays from a fresh clean checkout at the exact tested tree.
- Evidence replay succeeds offline and tamper/replay/redaction negatives fail.
- Issue-owned rollback restores pre-implementation behavior and preserves safe evidence.

## Regression gate

```text
make state-matrix-check cost-model-check aws-decision-check
```

Plus the exact amended Issue #6/#11 blast-radius commands. No guessed command is allowed.

## Implementation steps

1. Verify clean exact tested tree, input/dependency ancestry, allow-list and protected baseline.
2. Run the three required targets in a credential-free network-denied environment.
3. Run exact dependency/blast-radius and amended S3/static/security checks.
4. Replay the complete required suite from a fresh clean checkout of the exact tested tree.
5. Finalize the compact manifest and verify every artifact/hash/redaction/status offline.
6. Rehearse issue-owned rollback and prove protected/unrelated/retained evidence is unchanged.
7. Commit/push only exact implementation artifacts after staged-name/diff/security inspection.
8. Request fresh independent exact-head code/security review and resolve evidence-backed findings.
9. Obtain mandatory human exact-head pre-merge approval and use the repository merge workflow.
10. Keep AWS apply blocked; any later cloud work starts a separate named authorization process.

## Success criteria

- [ ] Required commands and exact dependency/protected blast radius are truthfully complete.
- [ ] Fresh clean-checkout replay and the exact amended S3 scans pass at the tested tree.
- [ ] Evidence is compact, replayable, tamper-detecting and contains no prohibited data.
- [ ] Rollback is proven without touching protected/unrelated state or deleting evidence.
- [ ] Independent exact-head review has zero unresolved Critical/High findings.
- [ ] Human pre-merge approval names the exact reviewed head.
- [ ] No AWS/Terraform/account/credential/resource action or production/readiness claim occurred.

## Risk assessment

The principal risk is conflating offline decision correctness with real service compatibility or
apply readiness. Evidence status separation and explicit TBCs prevent that. Rollback removes only
Issue #14-owned additions; real cloud rollback remains outside scope and authority.

## Security considerations

Before publication, inspect staged names and content for credentials, account IDs, ARNs, private
paths, PII, malicious URLs and unsafe file modes. Plan/validation/audit publication may force-add
only the exact `plans/260721-014-aws-decisions/` directory after staged-name and staged-diff
inspection; never force-add the parent `plans/` tree or an unapproved implementation path.

## Next steps

After this phase and merge, Issue #10 may consume the accepted non-applying interfaces. Separate
explicit human authority is still required before any real AWS/Terraform action.
