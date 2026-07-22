---
phase: 2
title: "Add the closed binding and reader"
status: pending
priority: P1
dependencies: [1]
stage: "B"
---

# Phase 2: Add the Closed Binding and Reader

## Context Links

- [Exact binding contract](./plan.md#exact-binding-contract)
- [Browser/server trust boundary](./plan.md#browserserver-trust-boundary)
- [Exact field and semantic contract](./requirements-and-risk-traceability.md#exact-binding-field-and-semantic-contract)
- [S3 matrix](./requirements-and-risk-traceability.md#s3-threat-and-negative-test-matrix)

## Overview

Add the minimum Stage B behavior: one closed schema, one exact binding document, and one pure
read-only validator. Wire the existing I5-03 check to validate the binding. Close the frozen RED
suite without editing its IDs, fixtures, expectations, or released inputs.

## Requirements

- The binding schema uses Draft 2020-12, closes every object, bounds all strings/arrays, restricts
  paths to repository-relative syntax, and admits no extensibility bag or executable field.
- The binding document contains exactly the input identities and four rows defined in the plan.
- The reader uses existing strict I-JSON, descriptor-safe reading, JSON Schema, SHA-256, and
  `LearningContractError`; it adds no distribution, lock, parser, canonicalizer, or runtime.
- Semantic validation reads exact protected sources and proves total ordered bijection. It compares
  only identifiers/order/hashes and never transforms or emits data records.
- `scripts/learning_contracts/schema.py` adds only the `vite-binding` schema-family dispatch.
- `scripts/learning_contracts/check.py` adds binding validation to the existing
  `learning-contracts-check` path and fitness provenance; it does not alter public argv, Make,
  activation, evidence schema, command ownership, or timeouts.
- The Stage A invalid corpus stays exactly 65 and its fixture index is unchanged. The Stage B test
  owns a separate exact eight-fixture inventory.

## Architecture

```text
immutable Stage A manifest + set ──┐
immutable Issue #6 evidence ───────┼──> pure binding validator
immutable Issue #7 Vite source ────┘            |
                                                   v
                         promotion-trust-vite-binding-v1.json
                             identifiers + hashes only
                                                   |
                 browser projection (untrusted)   |   server authority unchanged
```

The JSON document is directly importable by Vite. No generated JavaScript/TypeScript artifact is
needed. The schema and Python reader are validation tooling, not alternate domain schemas.

## Exact Phase Allow-List

| Action | Exact path | Purpose |
|---|---|---|
| Create | `learning/contracts/promotion-trust-vite-binding-v1.schema.json` | closed additive binding shape |
| Create | `learning/bindings/vite/promotion-trust-v1.json` | exact four-row binding and immutable dependency refs |
| Create | `scripts/learning_contracts/vite_binding.py` | pure hash/ref/order/bijection/boundary validation |
| Modify | `scripts/learning_contracts/schema.py` | add only `vite-binding` schema dispatch |
| Modify | `scripts/learning_contracts/check.py` | call validator and add binding hashes to existing evidence |
| Modify | `tests/contracts/learning/test_vite_consumer_binding.py` | close frozen RED without weakening assertions |

Phase 1 fixture paths are read-only in Phase 2.

## Tests Before

Re-run the Phase 1 test unchanged and retain the expected RED. Before creating the binding
document, the reader/check may exist only after the test proves `VITE_BINDING_REQUIRED`; never
commit a test that passes because an expected file is silently optional.

## Implementation Steps

1. Add the closed schema and validate the schema itself with Draft 2020-12.
2. Add `vite_binding.py` using the existing safe reader/error types and exact immutable input refs.
3. Author the four-row document from the frozen mapping table; do not copy records, schema fields,
   UI strings beyond identifiers, or Vite code.
4. Add `vite-binding` dispatch to `schema.py` and integrate the validator into the existing check.
5. Close each RED in stable ID order: dependency hashes, grain/key source equality, totality,
   bijection, boundary, secret/path/no-record, and absence of generated downstream paths.
6. Run the focused Python suite and the unmodified Issue #7 Node suite.
7. Rehash all protected paths, compare Stage A command/result structure, and run the primary Issue
   #8 check before Phase 3.

## Tests After

```bash
python3 -m unittest tests.contracts.learning.test_vite_consumer_binding
node --test spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs
make learning-contracts-check api-contracts-check evidence-contracts-check
```

Required assertions:

- exact valid document passes and double-read produces the same canonical JSON model;
- all eight invalid documents fail with their stable expected codes;
- missing/extra binding/fixture row fails;
- source or target identifier/order/hash drift fails before consumer use;
- nullable `category_name` values remain untouched and do not invalidate key existence;
- adding raw records, URLs, commands, templates, completion/auth/state fields, or absolute/private
  paths fails schema/boundary validation;
- no Stage A/Issue #6/Issue #7 byte changes and no new distribution/import/lock/Make change.

## Refactor Boundary

Keep the validator specific to this binding family. A generic UI-mapping engine, code generator,
registry v2, new contract set, TypeScript emitter, or framework abstraction is out of scope. Reuse
existing safe reader/hash/error helpers only when it reduces duplication without changing their
public behavior.

## Success Criteria

- [ ] Schema/document are closed, bounded, and exact.
- [ ] Four rows, three field-alias applications, and one grain-ID alias are total, ordered,
  bijective, and value-preserving.
- [ ] Existing public check validates the binding and records exact hashes.
- [ ] All RED IDs close without fixture/test weakening.
- [ ] Stage A corpus remains 65 and all protected hashes remain exact.
- [ ] No generated types, portal/runner path, new Make target, dependency, or cloud action exists.

## Security and Rollback

The reader refuses traversal, remote refs, symlink/hardlink/special-file substitution, unknown
fields, raw records, secret/PII canaries, executable strings, authorization/completion claims, and
oversized input before use. It never executes Vite source; the separate released Node test is the
only source execution. Before release, rollback removes only uncommitted Phase 2 files. After
release, the binding remains readable; consumer selection can be disabled without deleting it.

## Next Steps

Proceed to Phase 3 only after focused and primary checks pass with protected bytes unchanged.
