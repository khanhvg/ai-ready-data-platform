---
phase: 2
title: "Repository-level scaffold-first TDD and preservation"
status: pending
priority: P1
dependencies: [1]
effort: "Exact C1/C2 and complete 22-family RED"
---

# Phase 2: Repository-level scaffold-first TDD and preservation

## Context Links

- [Repository-level TDD](./stage-a-release-amendment.md#repository-level-scaffold-first-tdd)
- [Requirements](./requirements-and-risk-traceability.md)
- [Threat model](./threat-model-and-security.md)

## Overview

Create the seven-path generic callable scaffold only because the public paths are absent, then the
direct-child five-path complete tests/fixture commit. Before semantic code, record real repository
RED for all 22 families and 82 exact codes through production callables and matching CLI/Make
routes.

## Requirements

- C1 contains generic repository traversal, bounded parsing/process/render/evidence/cleanup
  plumbing only; it contains no target code, module/template/flow constants, fixture dispatch, or
  pass/fail oracle.
- C2 contains complete immutable tests/fixtures. Every valid control is a complete bounded
  repository that passes at GREEN; every mutation changes actual file/schema/source/render/
  process/evidence/Git state.
- Production routes are `check_repository()`, `_verify_repository()`,
  `_toolchain_verification()`, and `_repository_handoff()` plus exact public CLI/Make commands.
- Expected-code metadata is stripped. Booleans/dictionaries, echo/fallback, mocks, monkeypatches,
  skips, predicate-only checks, injected porcelain, and missing tools are forbidden.

## Files

- C1: exact seven scaffold paths named in the amendment.
- C2: exact four tests and `invalid-cases-v1.json` fixture.
- No other product/test path exists before the RED bundle closes.

## Implementation Steps

1. Re-run Phase 1 and create/inspect C1.
2. Create C2 as direct child; hash all five test/fixture files.
3. Allocate real temporary repository copies or bounded Git repositories under private ownership.
4. Run complete valid controls and single real mutations through callables and public routes.
5. Retain contemporaneous raw stdout/stderr, sanitized logs, source/tree/fixture/tool hashes, and
   exact absent-code assertions at C2.
6. Freeze C2 bytes through the first semantic GREEN.

## Tests and Validation

Real cases include relation/topology mutations, 11/13/duplicate/orphan template repositories,
visible render changes, spawned descendants/TERM resistance/RSS/output/files, raw-evidence/index
changes, and initialized-Git tracked/untracked/ignored dirt.

## Acceptance Criteria

- [ ] C1=7 creates; direct-child C2=5 creates; all other Stage A paths absent.
- [ ] All 22 families and 82 codes have a full valid control and named real mutation.
- [ ] All four production callables and matching public routes are reached with preconditions pass.
- [ ] Raw RED evidence is closed, truthful, bounded, private, and tests remain unchanged.

## Risks and Rollback

False RED or fixture-driven behavior blocks implementation. Rollback removes only verified C1/C2
creates and owned temporary state, preserves raw evidence, and re-proves integration/33/21 bytes.
