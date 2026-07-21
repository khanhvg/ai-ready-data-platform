---
phase: 3
title: "Private workspace and provenance envelope"
status: pending
effort: "2.0-2.5 implementation days"
dependsOn: [1, 2]
---

# Phase 3: Private workspace and provenance envelope

## Overview

Build the smallest issue-local workspace/process/evidence core that safely executes the golden pipeline. This is not generalized runner containment; security boundaries and residuals are fixed in [workspace-security-s3-disposition.md](./workspace-security-s3-disposition.md).

## Requirements

- Private `0700` workspace and evidence run roots, generated IDs, exclusive owner marker/lease and no-follow descriptor operations.
- Reject absolute/parent/symlink/hardlink/special/pre-existing-foreign paths; defend check/use/cleanup races.
- Allow-listed environment, secret/private-path scanning, bounded stdout/stderr/time and full process-group cleanup.
- Temp-in-destination+fsync+atomic rename+directory fsync; failure evidence preserved.
- `golden-clean` never calls broad root `clean`, follows links or deletes evidence.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | `scripts/golden/workspace*.py` | secure allocation, descriptor-bound IO, cleanup |
| Create | `scripts/golden/process*.py` | allow-listed child execution/bounds/reaping |
| Create | `scripts/golden/evidence*.py` | atomic bounded raw result writes |
| Create | `tests/golden/test_workspace_security.py` | path/symlink/TOCTOU/concurrency/cleanup cases |
| Create | `tests/golden/test_process_security.py` | env/output/time/descendant cases |
| Create | `tests/contracts/test_fitness_result_envelope.py` | pass/fail evidence shape |

## Dependency map

- Uses phase 2 pinned environment and phase 1 protected/semantic observers.
- Blocks phase 4 canonical evidence, phase 6 tool staging and phase 8 full execution.
- General browser/runner/hostile multi-tenant containment remains I5-04.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| absolute/`..`/NUL/alternate path | reject before allocation |
| component/child/cleanup symlink swap | remain on opened safe inode or typed fail |
| foreign directory/marker, hardlink, FIFO/device/socket | no reuse/write/delete |
| two runs/publishers or stale lease | one owner; other fails without breaking lease |
| kill around flush/rename | old complete set or new complete set; no partial current |
| output flood/timeout/TERM-resistant grandchild | bounded capture, TERM/KILL/reap, typed failure |
| credentials/private URL/home path/raw ID canary | absent from child or publication blocked |
| unrelated ignored sentinel/protected file | exact pre/post state |

## Interface checklist

- [ ] Run root cannot be caller-selected in production.
- [ ] All destructive operations require descriptor, marker nonce and device/inode match.
- [ ] Process API owns CWD, env, process group, deadlines, caps and result hash.
- [ ] Failure result remains schema-valid where safe root allocation succeeded.
- [ ] Cleanup never operates by glob/broad repository traversal.

## Tests Before

1. Write every security negative with attacker coordination barriers to force race windows.
2. Pre-create foreign/linked/special destinations and verify any naïve path implementation would be unsafe.
3. Add output flood, secret env, timeout and child-leak helpers inside test-private roots.
4. Require typed failure envelopes and protected hashes; fail because the workspace/process core is absent.

## Implementation

Implement allocation, open-relative writes, owner markers, publication lease, process groups and safe cleanup in the smallest separable modules. Use the exact 300-second step/deadline policy and output limits from the handoff. Fail if the filesystem cannot provide the required semantics.

## Refactor

Consolidate descriptor/identity verification into one audited helper. Keep destructive cleanup, immutable write and replaceable atomic write as different functions with different preconditions.

## Tests After

- Run each attacker case repeatedly and concurrently.
- Inject failure before/after every atomic boundary and verify recovery.
- Scan all retained output and staged tracked candidates.
- Verify protected paths and unrelated ignored sentinels unchanged.

## Regression Gate

- No path-based reopen after validation without identity binding.
- No child remains after timeout; bounds are evidenced.
- Failed roots/evidence are retained with sanitized relative locator.
- F-02/F-12 and SC-02/SC-03/SC-04/SC-06/SC-11 pass.

## Failure Evidence, Rollback and STOP

Retain only schema-valid, sanitized, relative failure evidence plus the marker-verified failed
issue-owned root. Rollback restores the prior atomic pointer/complete evidence state and removes
only a cook-created root after descriptor, marker, nonce, device/inode and purpose checks; never
touch foreign state. STOP on any lexical/realpath/parent/link/race/permission escape, pre-existing
destination acceptance, unsanitized output, bound overrun, child leak or refusal-cleanup failure.

## Success criteria

- [ ] Workspace and evidence writes are scoped, private and race-defended.
- [ ] Process/environment/output failures are bounded and typed.
- [ ] `golden-clean` semantics cannot invoke broad cleanup.
- [ ] S3 residual risks are accurately retained, not overclaimed away.
