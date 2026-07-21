---
phase: 2
title: "Stage A schemas validators and canonicalization"
status: pending
priority: P1
dependencies: [1]
stage: "A"
---

# Phase 2: Stage A Schemas, Validators, and Canonicalization

<!-- Updated: Validation Session 1 - exact closed validators and additive fitness v2 compatibility. -->

## Context Links

- [Phase 1 RED and authority](./phase-01-authority-freeze-and-stage-a-tdd-red.md)
- [Normative lesson/lab fields](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md#required-lesson-fields)
- [Issue #6 canonicalization contract](../260721-006-freeze-golden-baseline/evidence-canonicalization-and-provenance-contract.md)

## Overview

Add new, closed Issue #8 schema families and a framework-neutral Python reader/validator using the
existing manifest-admitted Python 3.12, `jsonschema`, `rfc8785`, `PyYAML`, and strict Issue #6
canonical profile. Every Issue #6 file remains immutable. An Issue #8-owned registry overlay adds
`fitness-result-v2` as a readable version, while a generic activation schema binds each emitting
command to its real owner; every undeclared family or command collision is rejected.

## Requirements

- Functional: Draft 2020-12 schemas for lesson, lab, progress, learner evidence, completion/
  reconciliation, operation matrix, promotion manifest and the scoped version registry.
- Functional: validate closed field sets, format/bounds, schema hashes, family/version dispatch,
  refs, uniqueness, prerequisite DAG and additive migration graph.
- Functional: strict UTF-8/I-JSON parsing before mapping and RFC 8785 canonical bytes for payload
  integrity; no field dropping, coercion, Unicode normalization, YAML ambiguity or float shortcuts.
- Functional: ordered first-error validation and exact closed field/semantic sets are normative in
  traceability; evidence locators are descriptor-bound and unsafe integers fail before JCS.
- Compatibility: shipped `fitness-result-v1` has `owner: I5-01`; add v2 with registry-bound owner/
  command semantics, select it through the I5-03 activation instance, retain v1 schema/hash/
  evidence and the existing registry-driven reader, and never reinterpret a v1 document as v2.
- Non-functional: no new distribution, lock, runtime, framework, Node package or network fetch.
  Required runtime mismatch fails with typed remediation to establish the existing golden runtime.

## Architecture

Executable contract documents are JSON. This keeps duplicate-name detection, strict I-JSON parsing,
canonicalization and evidence hashing on one byte path. MDX/prose remains outside the executable
contract and is consumed later by the portal. No YAML-to-JSON conversion becomes a second source of
canonical truth.

Two Issue #8/Issue #6 registry roles are explicit:

- existing `schema-version-registry.json`: immutable Issue #6 families/current/readers at SHA-256
  `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e`, including the fitness
  v1 entry whose exact hash is pinned by the shipped promotion-trust fixture;
- new `learning-contract-version-registry-v1.json`: Issue #8-owned families plus one explicit
  fitness-family extension bound to the base registry SHA-256.

The Issue #8 dispatcher loads the immutable base plus the hash-bound overlay, rejects duplicate
family/version/schema IDs except the one declared extension, validates each registered schema hash
and identity edge, and never rewrites either document at runtime. New v1 families have v1 as
current/readable plus identity reading. The extension adds v2 as readable without changing the base
family current or claiming that the unmodified Issue #6 reader understands v2. The generic
activation schema requires an instance to match exact reserved base rows, owner, fragment and
evidence version; the I5-03 instance selects v2 for its four commands. V1 remains read-only
compatibility and is never an I5-03 emission fallback. Rollback disables I5-03 activation while
retaining v2 schema/readability/evidence. Reversible private vectors exercise the migration engine
without publishing a fictional v0.

Canonical learner evidence follows the existing profile `rfc8785-jcs-v1`: canonicalize only the
defined payload; keep the sibling digest outside the payload; reject recursive self/attestation/
merge identities. Cross-reader vectors must produce the same bytes as `scripts/golden/canonical.py`
without changing that module.

## Related Code Files

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/lesson-v1.schema.json` | closed lesson identity, outcomes, refs, acts, probes, hints, evidence, accessibility/remediation |
| Create | `learning/contracts/lab-v1.schema.json` | closed typed lab/workspace/command/failure/reset/verify/evidence contract |
| Create | `learning/contracts/progress-v1.schema.json` | versioned events/projection, expected version and completion reference |
| Create | `learning/contracts/learning-evidence-v1.schema.json` | learner evidence payload/integrity/provenance boundary |
| Create | `learning/contracts/completion-reconciliation-v1.schema.json` | one-authority commit/orphan/quarantine protocol |
| Create | `learning/contracts/operation-matrix-v1.schema.json` | operation metadata and coverage shape |
| Create | `learning/contracts/promotion-trust-learning-manifest-v1.schema.json` | first manifest link/hash/grain contract |
| Create | `learning/contracts/learning-contract-version-registry-v1.schema.json` | scoped family/version/hash/migration registry schema |
| Create | `learning/contracts/learning-contract-version-registry-v1.json` | base-hash-bound owned families plus sole fitness-v2 readable extension; no base/global emission change |
| Create | `learning/contracts/fitness-result-v2.schema.json` | additive closed/bounded registry-owner-bound result with invocation/provenance/rollback fields and JCS payload hash |
| Create | `learning/contracts/command-owner-activation-v1.schema.json` | generic closed activation schema bound to immutable reserved command rows |
| Create | `scripts/learning_contracts/__init__.py` | module boundary |
| Create | `scripts/learning_contracts/canonical.py` | strict parser/domain payload canonicalizer delegating to existing JCS profile |
| Create | `scripts/learning_contracts/registry.py` | disjoint registry composition and migration graph |
| Create | `scripts/learning_contracts/schema.py` | Draft 2020-12 schema loading/hash/closed validation |
| Create | `scripts/learning_contracts/references.py` | repository-relative ref resolver and semantic graph checks |
| Modify | `tests/contracts/learning/test_schema_contracts.py` | close schema/canonical RED without weakening IDs/errors |
| Modify | `tests/contracts/learning/test_reference_integrity.py` | close ref/graph RED without weakening IDs/errors |
| Modify | `tests/contracts/learning/test_version_migrations.py` | close registry/v1-v2/private migration RED without weakening IDs/errors |
| Modify | `tests/contracts/learning/test_runtime_dependencies.py` | close exact lock/import/parser dependency assertions |

No existing file in `learning/contracts/` is modified. The base registry and every shipped fixture
that pins its hash remain byte-identical. If any Issue #6 byte must change, stop and request
serialized shared-contract authority; do not patch I5-01 schemas/readers/fixtures.

## Tests Before

- Re-run Phase 1 schema/ref/migration RED IDs unchanged.
- Re-run every Phase 1 schema/ref/canonicalization/migration/fitness/dependency RED ID unchanged.
- Add property/mutation vectors for minimum/maximum IDs, arrays, strings, semver, 40/64-hex, UTC
  timestamps, duplicate semantic IDs, unknown formats and local/remote/traversal `$ref` attempts.
- Add registry collisions against every current Issue #6 family and `$id`.
- Use the already frozen raw-byte vectors for duplicate escaped names, invalid UTF-8, BOM,
  surrogate, NaN/infinities, unsafe integers and unsupported numeric values before mapping.

## Refactor

Keep schema loading, reference resolution, semantic validation and canonicalization separate. Share
one error shape (`code`, `document`, `jsonPointer`, bounded detail) without exposing absolute paths
or raw sensitive values. Avoid a generic framework/package abstraction; this module is the minimum
offline validator for the observed contract set.

## Tests After

- Valid v1 documents round-trip through parse→validate→canonicalize without byte ambiguity.
- Unknown properties fail; no validator branch silently strips/coerces them.
- Every schema and registry hash is checked before use.
- Private migration v0↔v1 round-trips exactly; unregistered/lossy/cyclic/ambiguous paths fail.
- Fitness v1 still validates through the old reader; v2 validates I5-03; neither version is silently
  rewritten or dropped on rollback.
- Existing Issue #6 families dispatch/read exactly as before and all protected hashes remain equal.
- Stage A boundary test still reports zero Issue #7/framework dependency.

## Implementation Steps

1. Add schemas in dependency order: registry, lesson/lab, progress/completion, evidence, operation
   matrix, promotion manifest.
2. Register new Issue #8 family/version/schema paths and exact hashes; add the one hash-bound
   fitness v2 extension to the Issue #8 registry and prove the shipped registry is unchanged.
3. Implement strict parse/canonical payload primitives and cross-reader byte tests.
4. Implement registry composition with family/version/schema-ID/hash collision rejection.
5. Implement closed Draft 2020-12 validation and bounded errors.
6. Implement safe repository-relative `$ref` resolution; reject remote URLs, traversal, symlinks,
   wrong family/version and reference cycles.
7. Implement semantic graph checks for IDs, lesson↔lab, verifier/failure/remediation and prerequisite
   acyclicity.
8. Make Phase 1 schema/ref/migration RED green, then run Issue #6 evidence/migration regressions.

## Success Criteria

- [ ] All new schemas and the new scoped registry are closed, hashed and Draft 2020-12 valid.
- [ ] No family/version/schema ID overlaps Issue #6 except the declared fitness-family extension;
  that extension adds v2 only and matches the exact immutable base hash/v1 entry.
- [ ] Strict parse/JCS cross-reader vectors agree and tampered payloads fail.
- [ ] Ref, uniqueness, cycle and migration negatives fail with stable bounded codes.
- [ ] No new runtime/dependency/lock/framework byte is introduced.
- [ ] Existing Issue #6 contracts, registry, fixtures, readers and canonical bytes remain unchanged;
  the Issue #8 extension is base-hash-bound and old v1 reader/fixture tests remain green.

## Risk Assessment

- Multiple registries can create two global “current” pointers. Mitigation: the base current stays
  v1; the overlay only adds v2 readability, while owner-specific emission requires a hash-bound
  activation instance and every undeclared overlap is rejected.
- JSON Schema alone cannot enforce semantic uniqueness/acyclicity. Mitigation: required second
  semantic pass with mutation coverage.
- Reimplementing JCS can drift. Mitigation: domain wrapper over the existing profile/library and
  exact cross-reader vectors; no alternate serialization.

## Security and Rollback

Reject remote refs, traversal, sensitive fields, schema-hash drift and unregistered migrations
before dereference. Before publication, abandonment is limited to uncommitted Issue #8-owned
changes. After release, rollback disables the I5-03 activation while retaining every released
schema, reader and evidence record, including fitness v2; it never emits owner-mismatched v1,
down-migrates owner identity or restores a registry by deleting additive history.

## Next Steps

Phase 3 supplies the machine-readable operation/state/completion/probe/hint documents that these
schemas validate.
