---
phase: 1
title: "Freeze authority and dependency gates"
status: pending
priority: P1
dependencies: []
effort: "Gate; repeated at every exact-head handoff"
---

# Phase 1: Freeze authority and dependency gates

## Context Links

- [Plan](./plan.md)
- [Stage A v4 amendment](./stage-a-release-amendment.md)
- [Dependency and release gates](./dependency-and-release-gates.md)
- [Protected identities](./verification-evidence-and-protected-assets.md#protected-identities)

## Overview

Create no product/test bytes. Establish exact integration `5644f01b…` as ancestor, plan-only
provenance through the eventual readiness head, fresh local/upstream/fetched/live equality, exact
50-path absence, and 33/21 byte equality. Independent validation and readiness remain separate
future roles; this phase cannot pass from author self-checks.

## Requirements

- Direct integration-to-cook diff contains only this plan directory.
- All 50 Stage A paths are absent; failed v1/v2/v3 product/test/evidence commits are not inputs.
- The exact 16-command runtime contract has one private root and
  `$I11_RUNTIME/venv/bin/python` everywhere.
- Stage B lists remain empty and blocked on a passing merged Issue #10 journey.

## Files

No future product file may change in this phase. Authority/evidence writes are plan-only and must
be separately validated. Historical reports are immutable.

## Implementation Steps

1. Fetch and compare branch identities; verify worktree and writer ownership.
2. Record integration commit/tree/ancestry and direct plan-only name-status.
3. Parse exact 50/16 catalogues and prove the 50 paths absent.
4. Compare 33 protected and 21 released identities per path/blob/content bytes.
5. Run S3/private-path/secret/diff checks and record Stage B empty authority.
6. Stop for fresh independent plan validation, then separate readiness.

## Tests and Validation

- CK 4.5.2 strict plan validation/status, links, anchors, placeholders, counts, hashes, and diff.
- Negative gates for remote mismatch, wrong ancestor, extra path, protected/released drift, failed
  feature ancestry, mixed runtime shape, or a readiness/cook claim without separate evidence.

## Acceptance Criteria

- [ ] Exact independently validated and readiness-bound cook input is recorded.
- [ ] Integration-to-input diff is plan-only and local/upstream/fetched/live are equal.
- [ ] 50 paths are absent; 33/33 and 21/21 identities pass individually.
- [ ] No implementation, merge, approval, cloud/container/AWS/Terraform action occurred.

## Risks and Rollback

Any mismatch blocks the phase. Rollback removes only the unaccepted plan-only correction commit;
it never rewrites integration, touches historical evidence, or cleans a feature worktree.
