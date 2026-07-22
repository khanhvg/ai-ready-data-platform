---
phase: 4
title: "Stage A truthful evidence and bounded handoff"
status: pending
priority: P1
dependencies: [3]
effort: "Closed evidence, cleanup, rollback, and review handoff"
---

# Phase 4: Stage A truthful evidence and bounded handoff

## Context Links

- [Evidence truth and cleanup](./stage-a-release-amendment.md#evidence-truth-and-cleanup)
- [Verification and protected assets](./verification-evidence-and-protected-assets.md)
- [Threat model](./threat-model-and-security.md)

## Overview

Close command, RED, render, resource, S3, ownership, cleanup, and rollback evidence without
inventing independence or deleting raw bytes. Stop for a separate fresh implementation review;
do not merge, approve, or begin Stage B.

## Requirements

- Retain metadata-stripped mutation bytes, exact bounded raw stdout/stderr, production/CLI results,
  and separate sanitized logs with source hashes/redaction summaries.
- Index source/tree/fixture/tool hashes, owner markers, resource/render/S3 records, counts, sizes,
  modes, types, links, privacy, ignored-inclusive cleanup, and 33/21 results.
- Cook visual evidence says `cook-self-inspection`, `independent=false`, and truthful synthesis.
  Independent review is a future separate immutable bundle.
- Real Git subprocess output governs cleanliness; ignored evidence is owner-classified, never
  hidden by a clean claim.

## Files

No additional tracked path. Evidence and fitted HTML stay in a private owned ignored/external
root. Temporary package/cache/render staging is separately owned and removable.

## Implementation Steps

1. Run exact 16 commands under the closed runtime and capture bounded raw/sanitized records.
2. Close the evidence index and self-excluded index hash; verify privacy/mode/type/link closure.
3. Record truthful self-inspection for all five views at both widths.
4. Prove zero nonignored porcelain bytes and classify every ignored-inclusive record.
5. Rehearse exact-owner rollback while preserving evidence and re-proving 33/21/unrelated bytes.
6. Push exact candidate, prove remote equality, and stop for independent implementation review.

## Tests and Validation

Mutate missing raw/hash-only evidence, stale sanitized source hash, orphan/duplicate index member,
wrong mode/link/owner, self-inspection independence/synthesis, real Git dirt, and rollback scope.
Every failure traverses `_repository_handoff()` and the public clean-handoff CLI.

## Acceptance Criteria

- [ ] Closed evidence retains exact raw bytes and separate sanitized derivatives.
- [ ] Resource/render/S3/owner/privacy/count/size/mode/type/link/cleanup records all pass.
- [ ] Self-inspection is truthful; no fresh-independent claim exists in the cook bundle.
- [ ] Exact candidate is pushed/equal and handed off; no merge/approval/Stage B/cloud action occurs.

## Risks and Rollback

Missing raw bytes, misleading review metadata, unowned ignored content, or cleanup ambiguity is a
hard stop. Quarantine unsafe raw bytes privately; never delete them and claim hash-only proof.
