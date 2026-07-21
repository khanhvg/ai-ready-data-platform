---
phase: 2
title: "Stage A schemas validators and canonicalization"
status: pending
priority: P1
dependencies: [1]
stage: "A"
---

# Phase 2: Stage A Schemas, Validators, and Canonicalization

## Context Links

- [Phase 1 RED and authority](./phase-01-authority-freeze-and-stage-a-tdd-red.md)
- [Normative lesson/lab fields](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md#required-lesson-fields)
- [Issue #6 canonicalization contract](../260721-006-freeze-golden-baseline/evidence-canonicalization-and-provenance-contract.md)

## Overview

Add new, closed Issue #8 schema families and a framework-neutral Python reader/validator using the
existing manifest-admitted Python 3.12, `jsonschema`, `rfc8785`, and strict Issue #6 canonical
profile. Existing Issue #6 files remain immutable; new family dispatch composes them read-only and
rejects any family collision.

## Requirements

- Functional: Draft 2020-12 schemas for lesson, lab, progress, learner evidence, completion/
  reconciliation, operation matrix, promotion manifest and the scoped version registry.
- Functional: validate closed field sets, format/bounds, schema hashes, family/version dispatch,
  refs, uniqueness, prerequisite DAG and additive migration graph.
- Functional: strict UTF-8/I-JSON parsing before mapping and RFC 8785 canonical bytes for payload
  integrity; no field dropping, coercion, Unicode normalization, YAML ambiguity or float shortcuts.
- Non-functional: no new distribution, lock, runtime, framework, Node package or network fetch.
  Required runtime mismatch fails with typed remediation to establish the existing golden runtime.

## Architecture

Executable contract documents are JSON. This keeps duplicate-name detection, strict I-JSON parsing,
canonicalization and evidence hashing on one byte path. MDX/prose remains outside the executable
contract and is consumed later by the portal. No YAML-to-JSON conversion becomes a second source of
canonical truth.

Two registries have disjoint ownership:

- existing `schema-version-registry.json`: Issue #6 families, read-only;
- new `learning-contract-version-registry-v1.json`: Issue #8 families only.

The dispatcher loads both, rejects duplicate family/version/schema IDs, validates each registered
schema hash and migration edge, and never rewrites either registry at runtime. New v1 families have
v1 as current/readable/rollback plus identity reading. Reversible private vectors exercise the
migration engine without publishing a fictional v0.

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
| Create | `learning/contracts/learning-contract-version-registry-v1.json` | v1 current/readable/rollback entries for Issue #8 families |
| Create | `scripts/learning_contracts/__init__.py` | module boundary |
| Create | `scripts/learning_contracts/canonical.py` | strict parser/domain payload canonicalizer delegating to existing JCS profile |
| Create | `scripts/learning_contracts/registry.py` | disjoint registry composition and migration graph |
| Create | `scripts/learning_contracts/schema.py` | Draft 2020-12 schema loading/hash/closed validation |
| Create | `scripts/learning_contracts/references.py` | repository-relative ref resolver and semantic graph checks |
| Modify | Phase 1 schema/ref/migration tests and valid/private fixtures | close RED assertions |

No existing file in `learning/contracts/` is modified. If the new schemas cannot reference or
compose the Issue #6 concepts without changing their bytes, stop and request a new additive shared
contract version; do not patch I5-01 files.

## Tests Before

- Re-run Phase 1 schema/ref/migration RED IDs unchanged.
- Add property/mutation vectors for minimum/maximum IDs, arrays, strings, semver, 40/64-hex, UTC
  timestamps, duplicate semantic IDs, unknown formats and local/remote/traversal `$ref` attempts.
- Add registry collisions against every current Issue #6 family and `$id`.
- Add raw-byte parser vectors for duplicate escaped names, invalid UTF-8, BOM, surrogate, NaN,
  infinities and unsupported numeric values before mapping.

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
- Existing Issue #6 families dispatch/read exactly as before and all protected hashes remain equal.
- Stage A boundary test still reports zero Issue #7/framework dependency.

## Implementation Steps

1. Add schemas in dependency order: registry, lesson/lab, progress/completion, evidence, operation
   matrix, promotion manifest.
2. Register only new Issue #8 family/version/schema paths and their exact content hashes.
3. Implement strict parse/canonical payload primitives and cross-reader byte tests.
4. Implement registry composition with family/version/schema-ID/hash collision rejection.
5. Implement closed Draft 2020-12 validation and bounded errors.
6. Implement safe repository-relative `$ref` resolution; reject remote URLs, traversal, symlinks,
   wrong family/version and reference cycles.
7. Implement semantic graph checks for IDs, lesson↔lab, verifier/failure/remediation and prerequisite
   acyclicity.
8. Make Phase 1 schema/ref/migration RED green, then run Issue #6 evidence/migration regressions.

## Success Criteria

- [ ] All eight schema files and the new scoped registry are closed, hashed and Draft 2020-12 valid.
- [ ] No family/version/schema ID overlaps Issue #6.
- [ ] Strict parse/JCS cross-reader vectors agree and tampered payloads fail.
- [ ] Ref, uniqueness, cycle and migration negatives fail with stable bounded codes.
- [ ] No new runtime/dependency/lock/framework byte is introduced.
- [ ] Existing Issue #6 contracts, registry, fixtures, readers and canonical bytes remain unchanged.

## Risk Assessment

- Multiple registries can create two “current” pointers. Mitigation: disjoint family ownership and
  composite uniqueness; one current pointer per family, never overlapping families.
- JSON Schema alone cannot enforce semantic uniqueness/acyclicity. Mitigation: required second
  semantic pass with mutation coverage.
- Reimplementing JCS can drift. Mitigation: domain wrapper over the existing profile/library and
  exact cross-reader vectors; no alternate serialization.

## Security and Rollback

Reject remote refs, traversal, sensitive fields, schema-hash drift and unregistered migrations
before dereference. Rollback removes only the new family files/module and returns dispatch to the
unchanged Issue #6 registry; retained evidence stays immutable.

## Next Steps

Phase 3 supplies the machine-readable operation/state/completion/probe/hint documents that these
schemas validate.
