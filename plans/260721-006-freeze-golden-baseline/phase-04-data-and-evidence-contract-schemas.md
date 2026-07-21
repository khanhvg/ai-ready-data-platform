---
phase: 4
title: "Data and evidence contract schemas"
status: pending
effort: "2.0-2.5 implementation days"
dependsOn: [1, 2, 3]
---

# Phase 4: Data and evidence contract schemas

## Overview

Implement JSON Schema 2020-12 readers, RFC 8785/I-JSON canonicalization, raw/projection/envelope separation and the version registry. Producer and verifier implementations must be independently exercised to avoid correlated false passes.

## Requirements

- Fully specified duplicate/NaN/Infinity/Unicode/lone-surrogate/negative-zero vectors.
- Only payload is hashed; sibling integrity excludes itself; local SHA is not authenticity.
- Exactly five raw normalized drift pointers; deterministic projection has none.
- Immutable dbt build capture before docs; schema mutation tests cannot silently drop fields.
- Registry, reader dispatch, private migration vector, N-1 policy and rollback.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | `learning/contracts/*-v1.schema.json`, version registry and canonicalization profile | base evidence contracts |
| Create | `scripts/golden/canonical*.py`, `schema-reader*.py`, `projection*.py` | raw parser/JCS/readers/projection |
| Create | `tests/contracts/test_canonicalization.py` | exact RFC/I-JSON vectors |
| Create | `tests/contracts/test_schema_mutations.py` | missing/extra/type/duplicate/version/hash changes |
| Create | `tests/contracts/test_version_migration.py` | current/backward/private migration/rollback |
| Create | `tests/golden/test_dbt_capture_order.py` | immutable build versus docs |

## Dependency map

- Uses secure writes/processes from phase 3 and anchor fields from phase 1.
- Blocks phase 5 business schemas/fixture and phase 8 evidence publication.
- I5-14, not this phase, owns future signing.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| duplicate names before map, NaN/±Infinity, lone surrogate | reject raw token/programmatic input |
| numeric `-0`; decimal string `-0.00` | first canonicalizes `0`; second schema-invalid |
| composed/decomposed Unicode | remain distinct and hash differently |
| semantic field omitted or added to drift | schema/drift policy failure |
| payload or artifact changed after hash | integrity failure |
| unknown schema/current pointer/reader hash | registry failure, no fallback |
| private v0→v1→v0 and future v2/N-1 | lossless equality; cycle/loss rejected |

## Interface checklist

- [ ] Raw JSON parser detects duplicates/non-I-JSON before normal map.
- [ ] JCS encoder and independent verifier agree on official vectors.
- [ ] Schema dispatch is by registry family/version/hash, never file guess.
- [ ] Projection allow-list is exhaustive and mutations prove no semantic omission.
- [ ] `testedTreeSha`, external C2 and external M have distinct types/locations.

## Tests Before

1. Add exact canonical vectors and invalid tracked/private cases.
2. Add schema tests for every required/additional/type/range/format/version/digest mutation.
3. Add drift-policy tests and build/docs inode/content overwrite test.
4. Add private registry migration/cycle/loss tests.
5. Confirm failures against missing schemas/readers rather than accepting library defaults.

## Implementation

Implement strict raw token parsing, schema validation, canonical payload serialization, sibling digest, artifact index, registry dispatch and pure migrations. Capture build artifacts into exclusive immutable paths before running docs. Emit separate raw, projection and envelope files atomically.

## Refactor

Keep parser, schema validator, canonicalizer, projection builder and verifier as separable layers. Use the `rfc8785==0.1.4` library only behind conformance tests; reject unsupported inputs before it.

## Tests After

- Run official/custom vectors through raw and programmatic APIs.
- Cross-check canonical bytes/digests with an independent implementation path.
- Mutate every projection/artifact/registry identity independently.
- Prove retained v1 remains readable after private simulated promotion/rollback.

## Regression Gate

- Raw/projection/envelope cannot be conflated.
- Five-pointer drift list is exact; semantic projection equality is byte exact.
- No recursive digest/commit identity exists.
- F-01/F-09/F-10 and SC-07/SC-08/SC-15 pass.

## Failure Evidence, Rollback and STOP

Retain the named parser/schema/JCS/drift/migration mutation, raw bytes, expected typed error and
independent canonical-byte comparison. Rollback atomically restores the prior coherent
schema/registry/reader/writer set while keeping v1 readable and all raw evidence immutable. STOP
on accepted invalid I-JSON, canonical-byte disagreement, raw/projection/envelope conflation,
undeclared drift, build/docs overwrite, migration cycle/loss or recursive/authenticity claim.

## Success criteria

- [ ] JSON Schema/JCS behavior is fully deterministic and mutation-tested.
- [ ] Version readers/migrations/rollback are explicit and retained.
- [ ] Build evidence is immutable before docs.
- [ ] Integrity claims remain distinct from publisher authenticity.
