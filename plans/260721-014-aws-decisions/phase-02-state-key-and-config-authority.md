---
phase: 2
title: "State Key and Config Authority"
status: pending
priority: P1
dependencies: [1]
effort: "L"
---

# Phase 2: State Key and Config Authority

## Context links

- [Minimum state matrix](./decision-state-and-cost-contract.md#minimum-state-authority-matrix)
- [State coverage requirements](./requirements-and-risk-traceability.md#state-row-coverage-map)
- [Recovery and key threats](./security-recovery-and-evidence.md)

## Overview

Implement the strict state/key/config authority model and complete every minimum component row.
The result defines ownership and recovery obligations; it does not select AWS resources or claim
that a backup/restore has run.

## Requirements

- Functional: FR-002, FR-005..008, FR-015/016.
- Non-functional: NFR-002/006/007/008/013/014.
- Every logical state has one authoritative writer or an explicit fenced multi-step protocol,
  named readers, and no circular undeclared ownership.
- RPO/RTO/retention/deletion values supplied by owners remain required; missing values are
  `blocked-tbc`, never zero or “best effort.”

## Architecture

```text
strict state rows -> semantic uniqueness/fencing -> key/config dependency DAG
                  -> backup consistency groups -> restore/rebuild DAG
                  -> teardown/lifecycle/cost/BOM references
```

Keys and config are first-class state. Derived search/index/projection state must name the durable
rebuild source and readiness oracle. Durable authorities must name backup and restore; a rebuild
claim must prove source completeness and bounded readiness.

## Related code files

- Current implementation allow-list: `[]`.
- Exact model/schema/test/ADR files: `TBC` in the dependency amendment.
- Candidate ownership envelope: issue-owned state decision model/tests and
  `docs/decisions/aws/**` only.
- Protected shared evidence/data/architecture contracts remain read-only.

## Tests before

- Missing each required field in turn; blank versus explicit TBC distinction.
- Duplicate `stateId`, semantic authority, writer or conflicting lifecycle.
- Contradictory durability, stopped behavior, deletion mode, or backup method.
- Missing key/config state; cyclic key/config/restore ordering.
- Writer fencing and lock/replay failures.
- Backup success without consistency manifest/restore oracle.
- Search/index/projection marked durable without authority or rebuild source.
- Preserve/destroy ambiguity, foreign ownership, active dependency and key-loss cases.

## Refactor

Keep one canonical state schema and one semantic validator. ADRs reference state IDs rather than
copying state contracts into prose. Do not generalize into a cross-project framework.

## Tests after

- Every minimum row in the plan table exists exactly once and has all required fields.
- Writer/readers, key/config dependencies, backup groups, restore DAG, RPO/RTO, retention,
  deletion, migration and residual cost links reconcile.
- Empty current owner values yield an explicit apply-blocking TBC report.
- Malicious/oversize/duplicate/link/special-file inputs fail before semantic evaluation.

## Regression gate

```text
make state-matrix-check
make aws-decision-check
```

These are future commands and must remain offline/non-applying.

## Implementation steps

1. Write a closed schema from the contract in the companion document.
2. Implement duplicate-aware canonical parsing and structural validation.
3. Implement semantic uniqueness, writer fencing and dependency-DAG checks.
4. Populate all required rows with owner-supplied values or explicit `blocked-tbc` fields.
5. Define backup consistency groups and restore/rebuild oracles for each selected authority.
6. Link each row to FR/NFR/released concerns, ADR options, cost dimensions, future BOM bindings,
   evidence and rollback.
7. Run the complete negative and positive matrix without AWS/network access.

## Success criteria

- [ ] No minimum state/key/config row is missing, duplicated, contradictory or unowned.
- [ ] Every durable row has a recovery method; every derived row has a complete rebuild source.
- [ ] Key loss, corrupt backup and preserve/destroy behavior are explicit.
- [ ] All apply-blocking owner values remain visibly TBC until supplied.
- [ ] No actual AWS resource, principal, account ID or Terraform address is invented.

## Risk assessment

The biggest failure is treating component restartability as data durability. The model forces
separate server/process, data, index, configuration, secret, key and evidence rows. Rollback
restores the prior model/ADR version and invalidates dependent selections rather than migrating
state destructively.

## Security considerations

State may contain secrets even when model fields do not. Use safe metadata/projections only;
never include live state, plan, secrets, ARNs, account IDs or private locators in fixtures/evidence.

## Next steps

Phase 3 consumes only complete state interfaces and explicit TBCs; it may not erase them during
option scoring.
