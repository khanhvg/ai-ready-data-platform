# GitHub Issue #38 Phase 2 verification evidence

Status: implementation complete; final exact-head publication evidence is
recorded in PR and Issue #38 after the immutable pushed head is known.

## Scope

This evidence covers only Phase 2: seven v1 schemas and typed consumers, safe
content/semantic validation, authoritative atomic local engagement folders,
pure prototype migration, deterministic archive export, staged safe import,
distinct-path portability, and the documentation-only future object-store
boundary.

It does not claim Phase 3+ engine/web/catalog/golden/demo-manifest-instance work,
S3/cloud/deployment, customer data, or any learning/lab capability.

## Verification contract

The pre-publication verification run from the clean hash-locked Python 3.12.3
bootstrap recorded exit `0` for:

- `make assessment-install`;
- schema/contract: 7 schemas and 15 tests;
- Phase 1 scenarios: 48 assertions across 8 rater fixtures;
- calibration: 117/119 comparable pairs within one level (98.3%);
- reports: 36 artifacts, byte-stable;
- local store: 10 tests;
- migration: 10 tests;
- import/export: 24 passed and the one documented object-store skip;
- portability: 1 passed; security scan: 23 passed and the documented skip;
- full suite: 92 passed and the documented skip;
- Ruff, mypy over 21 source files, and the sdist/wheel build with 24 required
  packaged files;
- `docker compose config --quiet`, compilation of 10 existing Python
  entrypoints, and `git diff --check`.

All verification after dependency bootstrap executes through the assessment
network-denying wrapper. The hostile corpus covers traversal, absolute and
ambiguous names, archive/source/destination symlinks, duplicate/Unicode/case
collisions, encrypted and unsupported ZIP features, entry/depth/file/total/ratio
limits, corrupt hashes, unknown versions, secrets, credentialed URIs, opaque
evidence, and absolute path content. Every rejected import asserts that its
destination was not created or changed.

Independent review finished with both stages passing: specification compliance
`0 Critical / 0 Important / 0 Minor`, then code quality
`0 Critical / 0 Important / 0 Minor`. Review-driven race regressions cover
root/parent swaps, no-follow descriptor traversal, no-clobber promotion,
crash-atomic create, descriptor-bound recovery, and descriptor-bound failure
cleanup.

The independent deterministic portability proof produced ZIP SHA-256
`0bc0a8641fe97d08556e0326689fdeabb3e4988d537b4ddf7f3b60fe9c2bf629`
and canonical manifest digest
`ee7eb92a3708e329e03ee0d465760d15255b503d27620f401c7b8c65b2331c1e`.
Two same-state exports and the distinct-absolute-path re-export were
byte-identical; manifest digests matched and explicit secret,
credentialed-URI, and machine-path scans passed.

Verified dependency versions were package `0.2.0`, pip `25.1.1`, Pydantic
`2.11.7`, jsonschema `4.24.0`, PyYAML `6.0.2`, Pillow `11.3.0`, Jinja2
`3.1.6`, pytest `8.4.1`, Ruff `0.12.4`, mypy `1.16.1`, and build
`1.2.2.post1` on Python `3.12.3` / macOS arm64.

## Rollback and residual limitations

Rollback reverts the additive Phase 2 package/contracts/tests/docs/Make targets
while retaining every user-selected engagement folder and migration source.
Never downgrade or rewrite v1 folders in place; export them before removing v1
readers.

Parent-directory fsync is best-effort only where the operating system rejects
directory fsync. Byte-identical ZIP proof is pinned to Python 3.12.3 on the
audited macOS arm64 runtime. V1 accepts only inspectable/canonicalizable text,
JSON, CSV, PNG, and JPEG evidence; PDF, archives, executables, and opaque formats
remain rejected. Store roots reject every symlink path component; macOS callers
must use canonical paths such as `/private/var/...` instead of `/var/...`.
Atomic no-replace directory promotion currently requires macOS `renameatx_np`
or Linux `renameat2`; unsupported POSIX platforms fail closed. The
object-store/S3 boundary remains documentation-only.
