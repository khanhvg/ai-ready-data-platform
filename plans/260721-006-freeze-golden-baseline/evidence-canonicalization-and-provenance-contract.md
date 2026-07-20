# Evidence canonicalization and provenance contract

## Three non-interchangeable layers

| Layer | Purpose | Planned locator | Equality rule |
|---|---|---|---|
| Raw run bundle | Immutable diagnostic capture of actual tool output, bounded logs, timing and inputs | `.artifacts/evidence/golden/<run-id>/raw/**` | Compare only the normalized raw index after removing the five declared volatile pointers; vendor files are hashed diagnostic inputs |
| Semantic projection | Stable, tool-neutral facts used by contract readers and the tracked promotion fixture | `.artifacts/evidence/golden/<run-id>/projection.json` | RFC 8785 canonical bytes and SHA-256 must be exactly equal across runs; no drift pointers |
| Provenance/integrity envelope | Schema/tool/lock/tree identities, artifact hash graph, status and local-corruption checks | `.artifacts/evidence/golden/<run-id>/envelope.json` plus issue #7’s tracked `manifest.json` | Validate schema, non-recursive hash graph and external attestation relationship |

No layer may impersonate another. A dbt vendor artifact is not the stable projection; a projection hash is not publisher authenticity; a tracked fixture is not the complete raw run.

## Planned schemas and registry

Issue-owned base contract paths may include:

```text
learning/contracts/fitness-result-v1.schema.json
learning/contracts/golden-evidence-v1.schema.json
learning/contracts/evidence-envelope-v1.schema.json
learning/contracts/promotion-trust-evidence-v1.schema.json
learning/contracts/promotion-trust-fixture-manifest-v1.schema.json
learning/contracts/schema-version-registry.json
learning/contracts/canonicalization-v1.json
```

Every JSON Schema declares `$schema: "https://json-schema.org/draft/2020-12/schema"`, a stable `$id`, `type`, required fields, bounded strings/arrays, `additionalProperties: false` unless explicitly justified, and domain formats/patterns. Schema files are themselves hashed in the envelope.

`schema-version-registry.json` is the only current-version pointer for evidence readers. For each family it records `family`, `currentVersion`, immutable `readableVersions`, schema path/hash, reader ID, migration edges, canonicalization profile, status and rollback version. Initial v1 families legitimately have only v1 readable and an identity migration; no fictional predecessor is published. The generic dispatcher and migration/rollback protocol are still tested with private generated v0→v1 and v1→v2 registry copies. When v2 is admitted, the tracked registry must keep v1 readable, add an explicit pure v1→v2 migration and v2→v1 rollback where lossless; a lossy edge is a STOP and requires a new fixture, not silent coercion.

Readers reject an unregistered family/version, schema hash mismatch, duplicate registry key, multiple current versions, migration cycle, absent rollback, or a payload that validates only after dropping an unknown property. Registry updates are additive and atomic with reader/schema tests. Rollback restores registry, schema, reader and fixture-manifest hashes together.

Historical issue #3 evidence is parsed through a dedicated contextual adapter that labels source issue/SHA/platform/date and preserves “historical-context” status. It may support compatibility rationale but can never satisfy a current golden assertion.

## Canonical envelope shape and non-recursive integrity

Normative shape:

```json
{
  "schemaVersion": "golden-evidence-envelope-v1",
  "payload": {
    "testedTreeSha": "<40-lower-hex>",
    "profile": "small",
    "seed": 42,
    "lockSha256": "<64-lower-hex>",
    "toolchain": {},
    "projection": {},
    "artifacts": []
  },
  "integrity": {
    "canonicalization": "rfc8785-jcs-v1",
    "algorithm": "sha-256",
    "payloadSha256": "<64-lower-hex>"
  }
}
```

Only the `payload` object is canonicalized for `integrity.payloadSha256`; the sibling digest is excluded by construction. Each artifact entry hashes the artifact bytes and records a repository-relative or evidence-root-relative locator. The envelope never contains its own byte digest, its containing commit SHA, `attestationCommitSha`, or `mergeOrTagSha`.

Provenance identities have distinct meanings:

- `testedTreeSha`: clean commit containing producer, schemas, readers and tests that was run twice.
- `attestationCommitSha`: child commit containing authorized fixture bytes; recorded externally in the issue/PR handoff, never recursively in those bytes.
- `mergeOrTagSha`: remotely observed merged identity; recorded externally by issue #7 after blob verification.

An unkeyed SHA-256 detects local corruption. It does **not** authenticate a publisher or protect against a same-account actor who can replace bytes and recompute hashes. Hosted signing/trusted publisher remains I5-14.

## RFC 8785 / I-JSON canonicalization profile

The profile `rfc8785-jcs-v1` is fully specified:

- validate raw JSON as I-JSON and JSON Schema 2020-12;
- parse UTF-8 only; reject BOM, invalid UTF-8 and trailing non-whitespace data;
- reject duplicate object names **before** conversion to a normal map;
- reject lone surrogates and all NaN, positive Infinity and negative Infinity tokens/programmatic values;
- serialize recursively using RFC 8785 ECMAScript-compatible number/string rules;
- sort object property names by raw UTF-16 code units; preserve array order;
- preserve Unicode code points exactly; perform no NFC/NFD normalization on JSON payload strings;
- canonical numeric `-0` becomes `0`; business fixed-decimal strings such as `-0.00` are schema-invalid;
- emit UTF-8 with no BOM, insignificant whitespace or trailing newline.

Primary authorities are [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), [I-JSON RFC 7493](https://www.rfc-editor.org/rfc/rfc7493.html), and [JSON Schema 2020-12](https://json-schema.org/draft/2020-12/json-schema-core).

### Mandatory vectors

| Input / construction | Expected result |
|---|---|
| RFC primitive object | `{"literals":[null,true,false],"numbers":[333333333.3333333,1e+30,4.5,0.002,1e-27],"string":"€$\u000f\nA'B\"\\\\\"/"}` |
| `{"n":-0}` | canonical `{"n":0}` |
| raw `{"a":1,"\u0061":2}` | duplicate-name rejection before map creation |
| raw `{"n":NaN}`, `{"n":Infinity}`, `{"n":-Infinity}` | three separate rejections |
| `{"s":"é"}` and `{"s":"e\u0301"}` | both valid, remain distinct, hash differently |
| raw `{"s":"\uDEAD"}` | lone-surrogate rejection |
| property names CR, `1`, U+0080, `ö`, `€`, 😀, U+FB33 | exact RFC UTF-16 sort order: CR, `1`, U+0080, `ö`, `€`, 😀, U+FB33 |
| business decimal string `"-0.00"` | schema rejection; it is not numeric canonical `-0` |

Tests run the same vectors through the raw-token parser, in-memory encoder, schema reader and digest verifier. A permissive library default is never accepted as the contract.

## Raw capture ordering and immutability

The golden runner gives every step a separate output directory. Immediately after `dbt build`, before `dbt docs generate`, it copies and hashes the complete build `manifest.json`, `run_results.json`, graph/performance data and bounded log into a newly exclusively created `raw/dbt/build/` directory and marks the raw index immutable to the runner. `dbt docs generate` uses a different target/log directory under `raw/dbt/docs/`; it must not overwrite the captured build artifacts. Tests pre-seed distinguishable build/docs manifests and fail if inode/path reuse, mutation after hash, or an overwrite occurs.

The bounded normalized raw-run record may differ only at these exact JSON pointers:

```text
/run/runId
/run/startedAt
/run/finishedAt
/run/durationMs
/run/workspaceLocator
```

There is no prefix/wildcard drift. Tool versions, tested tree, lock, profile/seed, source/model/test counts, warning identities, semantic values/statuses, schema hashes and artifact hashes must be equal. Absolute workspace values are redacted into a stable run-relative locator before the raw index is retained.

## Deterministic projection

Projection construction uses allow-listed fields, explicit source ordering, explicit record ordering/null placement, fixed decimal-string scale and stable assertion IDs. It contains no run ID, timestamp, duration, hostname, username, absolute path, process/container identity, credential, private URL, attestation commit, merge SHA, score or ADR. All 18 input summaries, dbt result semantics, 11 mart summaries, Rill expressions, Airflow graph, curated identities and four promotion grains map from raw artifact hashes into projection fields defined in [golden-contract-matrix.md](./golden-contract-matrix.md).

Projection creation is pure: same raw semantic facts plus schemas produce identical canonical bytes. Mutation tests cover missing/extra field, reordered set represented as an ordered list, duplicate ID, changed count/hash, wrong decimal scale, negative zero, Unicode normalization, foreign path, unknown schema, altered source artifact after capture, and digest mismatch.

## FitnessResult and failure evidence

Every planned public command emits a `fitness-result-v1` envelope under `.artifacts/evidence/<fitness-id>/<run-id>/`, even on failure after run-root allocation. Required fields include command ID/owner, schema version, requested profile/seed, status (`pass` or `fail` for I5-01 required gates), typed failure code, bounded remediation, tested tree, tool/lock hashes, started/finished/duration, raw/projection/envelope locators and artifact hashes. A missing tool/evidence/schema is `fail`; no I5-01 required gate uses `skip` or `not-run-optional`.

If failure happens before safe root allocation, the command emits a minimal schema-valid result to a newly allocated evidence root or, if even that is unsafe, writes a bounded typed error to stderr and exits non-zero without claiming evidence. Evidence write uses temp-in-destination, fsync, atomic rename and directory fsync. Failure evidence is preserved; `golden-clean` never deletes it.

## Migration and rollback tests

1. Read current v1 and re-emit identical canonical payload bytes.
2. Reject unknown v0/v2 unless a private test registry supplies an exact schema/hash and migration edge.
3. In a private registry copy, migrate synthetic v0→v1, read with both dispatch paths, roll back v1→v0, and prove semantic equality; reject lossy/ambiguous/cyclic edges.
4. Simulate a future v2 registry update and prove the N-1 reader remains usable before the current pointer changes.
5. Restore the previous registry pointer and verify old fixture/envelope bytes without regeneration.
6. Mutate the canonical payload, artifact, schema hash, reader version and registry separately; each must fail with a distinct typed result.
