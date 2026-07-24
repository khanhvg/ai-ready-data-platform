# Phase 2: Versioned contracts, local store, migration, and portability

## Context links

- Parent: [plan.md](./plan.md)
- Dependency: [Phase 1](./phase-01-rubric-report-prototype-and-calibration.md)
- Decisions: [PD-02, PD-04–PD-07, PD-19–PD-20](./architecture-decisions.md)
- Traceability: [AC-02, AC-05–AC-06; SM-02–SM-03, SM-09–SM-10](./requirements-traceability.md)
- Current state: [researcher-02](./research/researcher-02-repository-current-state.md)

## Overview

- Date: 2026-07-24
- Description: Establish final versioned content/data contracts, authoritative engagement folders, atomic local storage, migration, and safe deterministic import/export.
- Priority: P2
- Implementation status: Pending
- Review status: Pending; requires Phase 1 focused review pass.

## Key Insights

- The folder, not SQLite, is the portable source of truth.
- Import safety is a security boundary: validation must precede extraction/mutation.
- Version numbers are carried in every top-level contract and pinned by the engagement.
- Human-authored YAML/Markdown is accepted only through schema, safe-parser, and semantic-reference validation.

## Requirements

- Framework, engagement, answer/evidence, report, demo-stage/AI-ready-dataset manifest, and recipe JSON Schemas at `1.0.0`.
- Stable IDs and semantic cross-reference checks across capabilities/questions/gates/findings/recommendations/architectures/mappings/demo stages.
- Narrow store protocol, local atomic implementation, relative paths, checksums, and no global machine paths.
- Deterministic ZIP plus safe non-mutating validation/import, with versioned numeric limits, evidence-format admission, destination-collision refusal, and streaming expanded-size enforcement.
- Proven `0.1.0-prototype → 1.0.0` migration, idempotence, unknown-newer rejection, and different-path roundtrip.
- Future object-store/S3 interface documented only; no implementation or upload.

## Architecture

`EngagementStore` exposes `create`, `open`, `read_document`, `write_document`, `add_evidence`, `list_engagements`, and `snapshot`; all keys are validated relative POSIX paths. `LocalEngagementStore` owns one explicit root and uses adjacent temporary files, flush/fsync, `os.replace`, and parent-directory fsync where supported. A lock file prevents competing writers; read-only report/catalog views require no lock.

Archive manifest fields: format version, engagement ID, pinned schema/framework/catalog/demo versions, normalized entry list `{path,size,sha256,mode}`, and overall digest over canonical entry records excluding the manifest entry/digest field. Export uses normalized NFC POSIX names, lexical order, `ZIP_STORED`, the fixed ZIP epoch/mode, canonical JSON, excludes lock/tmp/cache, never follows symlinks, and fails hygiene checks. V1 admits normalized UTF-8 text/JSON/CSV plus re-encoded metadata-free PNG/JPEG evidence only; PDF, nested archives, executables, and other opaque evidence fail export with a diagnostic. Versioned defaults are 1,024 entries, depth 16, 32 MiB per file, 128 MiB total expanded bytes, and 100:1 maximum expanded-to-compressed ratio. Import first scans the central directory and raw names, then streams every accepted entry while enforcing expanded-byte/ratio limits; it rejects encrypted/unsupported ZIP features, absolute/drive/UNC/traversal/NUL/backslash ambiguity, archive and pre-existing destination symlinks, non-regular types, duplicate and Unicode/case-fold collisions, destination existence/overwrite, unsupported versions, checksum mismatch, secret patterns/URI credentials, and absolute path content. It validates into a trusted sibling staging directory and atomically renames only into a non-existent destination.

Migration is a pure document transform with source/target validation and a registry keyed by exact versions. It copies by default, writes a migration receipt, never edits the prototype fixture, and can be rerun without change. Unknown-newer versions return a typed compatibility error before extraction.

## Related code files

- Modify: `assessment/pyproject.toml`, `assessment/requirements{,-dev}.in`, `assessment/requirements{,-dev}.lock` created in Phase 1
- Create: `assessment/contracts/{framework,engagement,answer,report,recipe}-v1.schema.json`
- Create: `demo/contracts/{demo-stage-manifest,ai-ready-dataset-manifest}-v1.schema.json`
- Create: `assessment/src/assessment/domain/{models.py,versions.py,errors.py}`
- Create: `assessment/src/assessment/content/{loader.py,schemas.py,semantics.py,markdown.py}`
- Create: `assessment/src/assessment/storage/{protocol.py,local.py,migrations.py,archive.py,hygiene.py,limits.py}`
- Create: `assessment/tests/{contract,unit,integration}/` contract/store/migration/archive tests and malicious ZIP corpus
- Modify: `.gitignore` for `.assessment-venv/`, assessment build/cache/generated outputs, while leaving engagement locations user-selected and never broadly ignored/deleted
- Modify: `Makefile` for `assessment-install`, schema/contract/import-export/portability/security targets

## Implementation Steps

1. Extend the Phase 1 Python 3.12 package and hash-locked runtime/dev dependencies for Pydantic, FastAPI/Jinja2, JSON Schema, pytest/tooling, and bounded Playwright; normal bootstrap may fetch exact hashes, while post-bootstrap verification blocks outbound network. Keep `.assessment-venv/` isolated from `.venv/`.
2. Write all v1 JSON Schemas as public contract authority and typed consumers; add schema/model parity fixtures and formalize safe YAML/Markdown parsing, ID grammar, version grammar, evidence statuses, maturity values, and relative-path types.
3. Implement content loading and semantic validation: uniqueness, complete anchors, coverage, resolved references, allowed report sections, no demo→score dependency, and content-version isolation.
4. Implement `EngagementStore` and authoritative layout from `architecture-decisions.md`; atomic writes, lock behavior, canonical JSON, checksums, and crash-recovery tests.
5. Implement the pure prototype-to-v1 migration and registry; prove source immutability, receipt contents, idempotence, known-old upgrade, and unknown-newer rejection.
6. Implement deterministic `ZIP_STORED` export with normalized metadata/checksum manifest, evidence allowlist/canonicalization, numeric limits, secret/path checks, and exclusion policy; prove identical archive bytes for identical state on the pinned Python runtime and identical canonical manifest digests across distinct paths.
7. Implement preflight and staged safe import with traversal/archive-or-destination-symlink/duplicate/case-fold/destination-collision/size/depth/compression/version/checksum/secret/path defenses; copy/export to a distinct absolute path and compare canonical state.
8. Define, but do not implement, the future `ObjectEngagementStore`/S3 behavior (object keys, optimistic version token, atomic manifest promotion) as a protocol note and contract test placeholder marked skipped-with-reason.

## Todo list

- [ ] Lock isolated Python 3.12 runtime and dev dependencies.
- [ ] Complete JSON Schemas, typed models, and semantic validation.
- [ ] Implement atomic local store and recovery tests.
- [ ] Prove v0.1 prototype migration and unknown-newer rejection.
- [ ] Produce deterministic checksummed ZIPs.
- [ ] Reject the full hostile archive/hygiene corpus before extraction.
- [ ] Prove different-path roundtrip without data loss.
- [ ] Document future object store boundary only.

## Success Criteria

- After `make assessment-install` completes, `make assessment-schema assessment-contract assessment-test` passes without containers or outbound network.
- Every engagement and content document declares supported versions and uses relative paths.
- Interrupted writes preserve the previous valid document; lock and recovery tests pass.
- Prototype fixtures migrate to v1 deterministically and remain unchanged; unknown-newer input leaves no destination.
- Same engagement produces byte-identical ZIPs on the pinned runtime and the same canonical manifest digest after a different-path roundtrip.
- Traversal, archive/pre-existing symlinks, duplicate/Unicode/case/destination collisions, zip bombs/oversized archives, encrypted/unsupported ZIP features, corrupt hashes, secrets, opaque evidence, and POSIX/macOS/Windows absolute paths are rejected before destination mutation.
- No SQLite/S3/cloud implementation or customer data exists.

## Risk Assessment

- ZIP parsers differ on ambiguous names; normalize once, use stored entries for exporter determinism, reject ambiguity/unsupported features, and test macOS/Linux/Windows spellings.
- Atomic rename semantics vary; keep staging on the same filesystem and document reduced parent-fsync guarantees on Windows.
- Strict hygiene may false-positive notes; block export with precise path/field diagnostics and allow users to redact, never silently strip source.
- Schema evolution can strand content; require migration registry and compatibility fixtures for every future version.
- Rollback: restore the previous content-version pointer and package code while retaining every engagement folder and migration source. Never downgrade or rewrite a v1 engagement in place; export it before removing v1 readers.

## Security Considerations

Use `yaml.safe_load`, bounded UTF-8 decoding, strict JSON Schema, no object constructors, no Markdown raw HTML, and no archive extraction API before validation. Never follow evidence or destination symlinks. Secret scan includes common key/token markers, credentialed URIs, PEM material, high-risk key names, and conservative entropy checks with explicit diagnostics; path scan recognizes `/Users/`, `/home/`, drive-letter, UNC, and `file://` forms. V1 rejects evidence formats it cannot canonicalize and inspect instead of claiming a universal binary secret scan.

## Next steps

After contract/store review and green portability tests, Phase 3 replaces the prototype evaluator with final deterministic services against the v1 schemas.
