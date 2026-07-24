# GitHub Issue #38 Phase 2 verification evidence

Status: the second bounded corrective implementation, worker review, and
pre-publication verification are complete after the replacement-head verifier
rejected PR head `4bf7646338bbe291f2f38a13fa9e57150ba6d906`.
The immutable replacement-head identity and publication state are recorded in
Issue #38 after push; a completely fresh independent verifier is still
required.

## Scope

This evidence covers only Phase 2: seven v1 schemas and typed consumers, safe
content/semantic validation, authoritative atomic local engagement folders,
pure prototype migration, deterministic archive export, staged safe import,
distinct-path portability, and the documentation-only future object-store
boundary.

It does not claim Phase 3+ engine/web/catalog/golden/demo-manifest-instance work,
S3/cloud/deployment, customer data, or any learning/lab capability.

## Verification contract

### Corrective verification after the independent failure

The independent verifier rejected prior head
`b625d82a3929cca5c2629df390761184a206fba1` with three Important findings:
canonical JSON could grow beyond the archive limit after the exporter checked
source bytes, authored YAML/Markdown used a separate stat plus unbounded read,
and distribution artifacts contained no public schemas while an empty
repository root returned success.

Focused regressions were added first and all four focused assertions failed
against that starting behavior: canonical expansion and authored growth each
reported `DID NOT RAISE`, the packaged resource inventory was empty, and the
empty-root command emitted `{"schema_version":"1.0.0","schemas":0}` with exit
`0`. The corrective implementation:

- enforces per-file and total limits on every canonical payload actually stored
  by export, including checksums and manifest, and proves a successful
  limit-bounded exporter/importer roundtrip;
- opens authored content once with no-follow where supported, verifies the
  descriptor is regular, and reads at most the configured limit plus one byte
  before strict UTF-8/YAML/Markdown processing;
- packages exact byte mirrors of all seven public schemas, defaults schema
  validation to installed resources, makes an empty/incomplete explicit root
  fail, and requires exactly seven schemas in both wheel and sdist.

The pre-commit corrective matrix recorded 18 contract tests, 25 archive tests
plus the one documented object-store skip, 96 full-suite tests plus that skip,
Ruff clean, mypy clean over 22 source files, and build inventory of 32 required
files with exactly seven schemas in both artifacts. Specification-first and
code-quality review each finished with `0 Critical / 0 Important`; exact-head
commands are repeated after commit before publication.

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

### Export path-replacement consistency correction

The replacement-head verifier found one additional Important finding at
`4bf7646338bbe291f2f38a13fa9e57150ba6d906`: export checked each source pathname
with `is_symlink()`/`is_file()` and later read it through `Path.read_bytes()`.
A deterministic synthetic swap replaced `evidence/files/proof.txt` with a
symlink in that interval and printed:

```text
EXPORT_SYMLINK_SWAP_FOLLOWED True True True Sanitized external proof.
```

A local reproduction on the unchanged input head repeated that exact result.
The focused regression was then added before production changes and failed for
both `engagement.json` and an evidence entry with `DID NOT RAISE` (exit 1).

The bounded correction binds export traversal to a no-follow root descriptor,
opens child directories and files relative to their already-bound parent
descriptors, verifies scanned/opened filesystem identity and regular type,
reads at most the versioned file limit plus one byte, and rejects mutation
during a read. `engagement.json` is validated from the same descriptor-bound
bytes collected for the archive instead of a separate pathname read.

The focused replacement selection passed all four parameterized cases:
`engagement.json` and `evidence/files/proof.txt`, each replaced by a regular
file and a symlink between scan and descriptor open. The combined focused
selection, including the four earlier corrective regressions, passed all eight
pytest cases.

The fresh pre-publication worker matrix completed with:

- schema authority 7; contract 18 passed; local store 10 passed; migration 10
  passed;
- import/export 29 passed plus the documented object-store skip; portability 1
  passed; security 28 passed plus the same skip;
- scenarios 48 assertions across 8 raters; calibration 117/119 within one level
  (98.3%); reports 36 byte-stable artifacts;
- full assessment suite 100 passed plus the documented skip; Ruff clean; strict
  mypy clean over 22 source files;
- wheel and sdist build inventory 32 required files; independent inventories
  of 42 wheel entries and 57 sdist entries, with exactly seven schemas in each;
  both artifacts validated all seven schemas from isolated installs and an
  explicit empty root failed with exit 2;
- `exact-head-proof` two-export/distinct-root import/re-export byte identity,
  ZIP SHA-256
  `0bc0a8641fe97d08556e0326689fdeabb3e4988d537b4ddf7f3b60fe9c2bf629`,
  and manifest digest
  `ee7eb92a3708e329e03ee0d465760d15255b503d27620f401c7b8c65b2331c1e`;
- `docker compose config --quiet`, compilation of the 10 tracked non-test
  Python entrypoints, diff checks, ignored-artifact assertions, nonignored
  untracked-file check, and bounded scope/privacy scans.

The pending-diff review passed specification compliance first and code quality
second with `0 Critical / 0 Important` findings. The correction preserves the
public API and contains no credential, customer data, local absolute home path,
cloud action, upload, deployment, SQLite authority, object-store
implementation, Phase 3+ code, destructive engagement behavior, or skill
change. Cloud actions performed: zero.

This is producing-worker evidence, not independent verification. PR #40 must
remain unmerged until a completely fresh verifier passes the exact immutable
replacement head with zero Critical and Important findings.
