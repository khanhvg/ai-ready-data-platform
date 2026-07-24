---
type: journal
date: 2026-07-24
issue: 38
branch: feature/issue-38-phase-2-contracts-portability
status: implementation-complete-publication-pending
authority: historical-record
---

# Issue 38 Phase 2 implementation

## Context

Work started from the clean, exact Phase 1 integration merge
`3d464b402a3af9cac03ad7a99e7992839f9ff2cd` on
`feature/issue-38-phase-2-contracts-portability`, using the audited Phase 2
document as the implementation authority. The boundary remained v1
contracts/models, safe content validation, authoritative local folders,
prototype migration, deterministic export, staged safe import, portability,
tests, documentation, and evidence.

FastAPI/Jinja/Playwright workflow work, the final Phase 3 engine/report service,
catalog/diagrams, demo manifest instances, golden pipeline, policy, dbt, S3,
cloud, deployment, customer data, and skill changes remain excluded.

## What happened

1. Provenance checks confirmed the expected branch, clean worktree, and exact
   input SHA before the first product write.
2. Public-behavior tests were written first. The clean hash-locked bootstrap
   succeeded, then the focused Phase 2 run failed during collection with exit
   `2` because `assessment.content`, `assessment.domain`, and
   `assessment.storage` did not exist. This was the genuine RED state.
3. Seven Draft 2020-12 schemas, strict typed v1 models, bounded safe YAML and
   Markdown loaders, and semantic reference/version validation were added. The
   first implemented run reached 21 passes and exposed a real schema defect:
   the observable-anchor length rule rejected the shorter readiness label
   `Not ready`. Separating label and anchor definitions fixed the contract.
4. The narrow engagement-store interface and local implementation added
   canonical JSON, relative POSIX keys, checksums, locking, atomic replace,
   supported directory fsync, and crash recovery. Symlink-component and
   no-follow protections were strengthened during edge-case scouting.
5. The pure `0.1.0-prototype -> 1.0.0` migration registry added source/target
   validation, deterministic receipts, source immutability, idempotence, and
   rejection of unsupported newer versions before destination mutation.
6. Deterministic `ZIP_STORED` export and preflight/staged import added normalized
   metadata, canonical manifest coverage, allowlisted evidence canonicalization,
   versioned limits, hygiene checks, and hostile-archive rejection without
   destination mutation. Different-root folder and ZIP roundtrips proved the
   portable-folder authority.
7. The future object-store boundary was documented as a skipped-with-reason
   contract only; no SDK, credential, upload, bucket, Terraform, or cloud action
   was introduced.

## Review history

The required specification-first review initially reported `0 Critical / 4
Important`. The contract, parity, validation, and rejection-proof gaps were
corrected; the final specification rerun passed at `0 Critical / 0 Important /
0 Minor`.

The subsequent code-quality review was deliberately iterative. Its Important
counts moved `6 -> 2 -> 1 -> 1 -> 0`, with no Critical findings. Corrections
hardened root/parent swap handling, no-follow descriptor traversal,
no-clobber promotion, crash-atomic creation, descriptor-bound recovery, and
descriptor-bound failure cleanup. The final code-quality rerun also passed at
`0 Critical / 0 Important / 0 Minor`.

## Verification

The final prepublication verification passed `92` tests with one intentional
skip for the documentation-only `ObjectEngagementStore` contract. Schema,
contract, store, migration, hostile import/export, portability, Phase 1
scenario/calibration/report regressions, Ruff, mypy, build, Compose
configuration, entrypoint compilation, offline enforcement, and generated-file
hygiene all exited `0`. Both final review stages reported
`0 Critical / 0 Important / 0 Minor`.

Independent same-state and distinct-path portability produced:

- ZIP SHA-256:
  `0bc0a8641fe97d08556e0326689fdeabb3e4988d537b4ddf7f3b60fe9c2bf629`
- Canonical manifest digest:
  `ee7eb92a3708e329e03ee0d465760d15255b503d27620f401c7b8c65b2331c1e`

The archive bytes and canonical manifest digest were stable, and explicit
secret, credentialed-URI, and machine-absolute-path scans passed.

## Reflection and decisions

- Engagement folders remain the portable authority; SQLite and object storage
  were not introduced.
- Import remains fail-closed: validate completely, stage beside the destination,
  then atomically promote without overwrite.
- Review-driven race fixes were retained because they close observed
  time-of-check/time-of-use paths and are covered by filesystem regressions.
- This journal is historical context. The tracked verification report, pushed
  commit, PR, and Issue #38 comment are the immutable publication authorities.

## Residual limitations

Directory fsync is best-effort where the host rejects it. Byte identity is
pinned to Python 3.12.3 on the audited macOS arm64 runtime. V1 evidence remains
limited to canonicalizable text, JSON, CSV, PNG, and JPEG. Store roots reject
symlink components, and atomic no-replace directory promotion requires the
supported macOS/Linux primitives. Object-store/S3 support remains
documentation-only.

## Next

Publication is pending: fix the immutable head, commit only scoped product,
tests, docs, and evidence, push, verify local/remote SHA equality, open the PR,
record configured-check state, and comment on Issue #38. This worker must not
merge; the controller owns exact-head verification, merge, and post-merge
smoke.
