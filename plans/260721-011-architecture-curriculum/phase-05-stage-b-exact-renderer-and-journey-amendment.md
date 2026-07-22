---
phase: 5
title: "Stage B exact renderer and journey amendment"
status: pending
priority: P1
dependencies: [4]
effort: "Blocked gate"
---

# Phase 5: Stage B exact renderer and journey amendment

## Context Links

- [Dependency and release gates](./dependency-and-release-gates.md#stage-b-gate)
- [Architecture and curriculum design](./architecture-and-curriculum-design.md#stage-b-boundary)

## Overview

Hard-blocked until Stage A is independently reviewed/released and Issue #10 publishes a passing
merged real journey plus released renderer. Current file, command, dependency, and renderer lists
are empty. No Stage A result or label can satisfy this dependency.

## Requirements

- Pin exact released Stage A and Issue #10 merge/tree/contracts/evidence.
- Derive real discovery, renderer, lifecycle, reset, verifier, completion, security, and cleanup
  seams from released code; predict none.
- Author a new closed Stage B amendment, independent validation, and readiness result.

## Files

None authorized.

## Implementation Steps

1. Wait for external release-state change.
2. Re-scout the exact merged contracts in a clean checkout.
3. Propose a new amendment without modifying Stage A truth.

## Tests and Validation

No Stage B product/test/portal/browser command may run while blocked.

## Acceptance Criteria

- [ ] Passing merged Issue #10 real journey and renderer exist.
- [ ] New exact amendment passes independent validation/readiness.

## Risks and Rollback

Predicted or merely compatible seams are a hard stop. Current rollback is no action.
