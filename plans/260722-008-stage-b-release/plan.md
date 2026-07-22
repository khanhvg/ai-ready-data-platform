---
title: "Issue #8 Stage B: Release the promotion-trust Vite identifier binding"
description: "Tests-first additive binding for the exact Stage A versus released fixture/Vite identifier mismatch; no Stage A rewrite, portal, runner, or cloud scope."
status: pending
priority: P1
issue: 8
branch: "plan/issue-8-stage-b-amendment"
tags: [feature, shared-core, contracts, tdd, security-s3, vite, migration]
blockedBy: []
blocks: []
created: "2026-07-22"
createdBy: "ck:plan"
source: skill
planningMode: "auto-hard-post-release-amendment"
inputSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
stageAReleaseSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
issue7MergeSha: "1806b6d515f2f7a2ace2be7077af84a745ff221f"
stageARelease: "pass"
stageBRequired: true
sharedContractLease: "active-exclusive-i5-03"
cookable: true
requirementAudit: "audit/post-stage-a-requirement-audit.md"
traceability: "requirements-and-risk-traceability.md"
---

# Issue #8 Stage B: Release the Promotion-Trust Vite Identifier Binding

## Outcome

Release one additive, closed `promotion-trust-vite-binding-v1` document and its read-only validator
so downstream Vite/portal consumers can resolve the only proven cross-release identifier mismatch
without changing Stage A or inventing mappings in Issue #10.

The binding is presentation/lookup metadata only. It pins the exact Stage A contract set/manifest,
Issue #6 evidence, and Issue #7 merge/ADR/package/lock/source hashes. It maps two field aliases and
one grain-ID alias, preserves ordering and values, and explicitly carries no validation,
authorization, operation, progress, evidence, or completion authority.

This is the smallest behavior slice that closes the verified gap. Generated TypeScript, portal
components, runner adapters, data transforms, manifest/registry revisions, new Make targets, and
OpenAPI changes are unnecessary and excluded.

## Scope Challenge

| Candidate | Evidence | Decision |
|---|---|---|
| No Stage B / direct consumption | Stage A says `region`,`category`,`dq`; Issue #6/Vite says `region_name`,`category_name`,`data-quality`; no released alias exists | Rejected: Issue #10 cannot consume both releases exactly without inventing shared meaning |
| Rewrite Stage A manifest/set/registry | Would alter an accepted release and invalidate exact hashes/readers | Rejected: violates additive migration and released-byte immutability |
| Publish new manifest/registry v2 | Could correct names, but versions the complete shared manifest and registry for a three-alias presentation seam | Rejected as unnecessary scope; no domain/API/state semantic changed |
| Add one hash-bound alias binding | Resolves the exact mismatch while retaining Stage A and consumer ownership | **Selected** |
| Generate portal TypeScript/types | Belongs under `apps/learning-portal/**` and would duplicate Issue #10 ownership | Rejected |

## Verified Inputs

| Input | Exact identity | Role |
|---|---|---|
| Release integration | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | sole implementation base |
| Stage A merge | `5c2244c2c860234d0df49cf0a42ad950c6495717` | released I5-03 core ancestor |
| Issue #7 merge | `1806b6d515f2f7a2ace2be7077af84a745ff221f` | Accepted Vite handoff ancestor |
| Stage A contract set | `learning/contracts/learning-contract-set-v1.json` / `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` | immutable contract release index |
| Stage A promotion manifest | `learning/manifests/promotion-trust-v1.json` / `553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac` | immutable logical key source |
| Issue #6 promotion evidence | `tests/fixtures/learning/promotion-trust/evidence-v1.json` / `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5` | immutable physical key/order source |
| Issue #6 fixture manifest | `tests/fixtures/learning/promotion-trust/manifest.json` / `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341` | immutable fixture identity |
| Issue #7 ADR | `docs/decisions/0005-web-stack.md` / `6e26c48a027d226d8529fda939c07cca99e9f4e1d88cac12708deb98d6fe5eee` | Accepted/Vite decision |
| Issue #7 package | `spikes/web/candidates/vite/package.json` / `c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871` | React/Vite version pins |
| Issue #7 lock | `spikes/web/candidates/vite/package-lock.json` / `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c` | frozen dependency identity |
| Issue #7 lesson contract | `spikes/web/candidates/vite/src/lesson-contract.mjs` / `32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9` | immutable Vite grain/label source |
| Completion contract | `learning/contracts/completion-reconciliation-v1.json` / `8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff` | immutable server authority |

All paths above are read-only. Any mismatch at cook input is a STOP, not permission to refresh a
hash or widen scope.

## Exact Binding Contract

The new document must contain only these closed top-level fields:

```text
schemaVersion, bindingId, mode, stageA, issue7, fixture,
grainBindings, decision, trustBoundary
```

- `schemaVersion` and `bindingId`: `promotion-trust-vite-binding-v1`.
- `mode`: `lossless-identifier-alias-v1`.
- `stageA`: exact release SHA plus contract-set and promotion-manifest path/SHA-256 references.
- `issue7`: exact merge SHA plus ADR/package/lock/lesson-contract path/SHA-256 references.
- `fixture`: exact Issue #6 evidence and manifest path/SHA-256 references, marked
  `build-time-validation-only` so raw records are never a browser payload.
- `grainBindings`: four ordered rows and no extras:

| Stage A grain | Vite grain | Ordered Stage A keys | Ordered fixture/Vite keys | Non-identity aliases |
|---|---|---|---|---|
| `promotion` | `promotion` | `promo_name,channel` | `promo_name,channel` | none |
| `fulfillment` | `fulfillment` | `carrier,region` | `carrier,region_name` | `region → region_name` |
| `returns` | `returns` | `reason,category,region` | `reason,category_name,region_name` | `category → category_name`; `region → region_name` |
| `dq` | `data-quality` | `scenario` | `scenario` | grain ID only: `dq → data-quality` |

- `decision`: exact `insufficient-evidence/no-common-grain`; binding cannot add relationships,
  attribution, aggregation, joins, defaults, or data transformations.
- `trustBoundary`: exact projection-only browser role, Stage A server validation authority,
  `learning-progress-authority-v1` completion authority, and boolean `false` for authorize, mutate,
  validate, complete, or emit evidence.

The reader proves totality, order equality, one-to-one targets, exact input hashes, exact Vite
labels, target-key existence in every fixture source record (including nullable values), and zero
value transformation. A duplicate/missing/extra/renamed mapping fails closed.

## Phases

| Phase | Name | Status |
|---|---|---|
| 1 | [Freeze exact authority and capture real-path RED](./phase-01-authority-and-real-path-red.md) | Pending |
| 2 | [Add the closed binding and reader](./phase-02-additive-binding-and-reader.md) | Pending |
| 3 | [Compatibility, S3, release, and handoff](./phase-03-compatibility-release-and-handoff.md) | Pending |

Phases are serialized under one shared-contract writer. No phase fan-out is permitted because
Phase 2 modifies the same validator/check seam whose release is proven in Phase 3.

## Exact Implementation Allow-List

No unlisted tracked path may change.

| Action | Exact path |
|---|---|
| Create | `learning/contracts/promotion-trust-vite-binding-v1.schema.json` |
| Create | `learning/bindings/vite/promotion-trust-v1.json` |
| Create | `scripts/learning_contracts/vite_binding.py` |
| Modify | `scripts/learning_contracts/schema.py` |
| Modify | `scripts/learning_contracts/check.py` |
| Create | `tests/contracts/learning/test_vite_consumer_binding.py` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/absolute-path.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/completion-authority-override.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/contract-key-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/dependency-hash-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/duplicate-target-key.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/fixture-key-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/grain-id-drift.json` |
| Create | `tests/fixtures/learning/bindings/vite/invalid/raw-record-leak.json` |

The new invalid-fixture directory is separate from the released 65-entry Stage A corpus and its
immutable index. The Stage B test owns its exact eight-file inventory.

## Protected Deny-List

- all 21 files hashed by `learning-contract-set-v1.json`;
- `learning/contracts/learning-contract-version-registry-v1.json`, its schema, base registry,
  command activation, canonicalization, OpenAPI, operation matrix, completion contract, Stage A
  lesson/lab/manifest, and `mk/issue-5/i5-03.mk`;
- all Issue #6 fixture/data/reader/lock/Make paths and all Issue #7 ADR/Vite/package/lock/Make paths;
- root `Makefile`, `release-manifest.json`, `.gitignore`, `docs/code-standards.md`, portal, runner,
  data pipeline, AWS/Terraform/cloud, unrelated plans, and unrelated user work.

There is no protected-file exception. A required path outside the allow-list stops cook and
returns to planning.

## Verification Commands

Tests-first focused RED/GREEN:

```bash
python3 -m unittest tests.contracts.learning.test_vite_consumer_binding
node --test spikes/web/candidates/vite/tests/promotion-trust-contract.test.mjs
```

Final Issue #8 and inherited blast radius:

```bash
make learning-contracts-check api-contracts-check evidence-contracts-check
make lesson-check LESSON=promotion-trust
make data-contracts-check migration-contracts-check
make help
git diff --check
make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"
```

`EVIDENCE_LOCATOR` comes from the preceding contract check. No new Make target, npm install,
browser process, build, network fetch, or package/lock change is admitted. The Node command uses
only built-ins and the released Issue #7 test/source.

## Resource and Evidence Contract

- Focused Python and Node commands: 60 seconds each, 2 MiB stdout/stderr each.
- `learning-contracts-check`: existing 120-second ceiling; full ordered sequence: 600 seconds.
- Mutable evidence/workspace: at most 256 MiB; peak RSS: at most 2 GiB; commands run serially.
- Evidence remains under `.artifacts/evidence/learning-contracts/<run-id>/`, uses
  `fitness-result-v2`, and adds exact binding schema/document hashes plus every pinned input hash.
- Required missing runtime/tool/file/hash is `fail`; no optional skip applies.
- Run the final checks with network and cloud credentials absent after admitted runtimes exist.

## Browser/Server Trust Boundary

- Browser/Vite may import the closed binding as public projection metadata only.
- The binding never contains raw fixture records, private locators, commands, URLs, tokens, auth
  policy, executable expressions, templates, defaults, or learner evidence.
- Server adapters validate all requests/documents against Stage A schemas/OpenAPI and enforce the
  operation matrix. The binding cannot broaden a field or API operation.
- `learning-progress-authority-v1` is the only completion writer. A binding/browser flag, rendered
  label, cached state, fixture presence, or Vite test result cannot complete progress.
- Issue #10 may create portal-local types from this document in its own scope, but those types are
  projections and cannot become a second shared contract.

## Migration and Rollback

- `promotion-trust-vite-binding-v1` is a new additive family; no v0 or migration is invented.
- The v1 reader is retained after release. Any later version adds an explicit lossless edge and
  dual-read proof; unknown/lossy/cyclic/non-bijective mappings fail.
- Stage A readers/set/registry/manifest remain the rollback base and are never rewritten.
- Rollback deselects the binding in downstream consumption while retaining its released schema,
  reader, evidence, and external hash. There is no alias fallback and no value rewrite.
- Cleanup removes only marker-verified ignored Stage B test/evidence roots; no tracked file,
  retained evidence, fixture, schema, or downstream state is deleted.

## Release and Human Gate

At one exact clean committed implementation head:

1. all focused/final commands and S3/protected/hash/resource/rollback checks pass;
2. a fresh independent implementation reviewer verifies the exact head and rejects any scope or
   authority expansion;
3. repository-required checks pass;
4. a repository-authorized human approves that exact head before merge;
5. the remote merge/release SHA is observed rather than predicted;
6. Issue #8 publishes the Stage A set hash and new binding hash as two immutable components, plus
   commands, compatibility result, rollback result, and remaining residual risks;
7. only then is the shared-contract lease released and Issues #9/#10 may repin the new release.

No planning artifact embeds its own containing commit or a future release SHA.

## Success Criteria

- [ ] Every real-path RED ID fails for its intended missing/invalid binding behavior before GREEN.
- [ ] Binding contains exactly four ordered grain rows, two unique field-alias rules applied in
  three row positions, and one grain-ID alias.
- [ ] Exact input hashes and source/target keys match released bytes; no value transformation occurs.
- [ ] Browser remains projection-only and server/completion authorities remain unchanged.
- [ ] Stage A, Issue #6, Issue #7, OpenAPI, registry, activation, Make, and downstream paths remain
  byte-identical.
- [ ] Focused, primary, blast-radius, offline, S3, resource, cleanup, and rollback checks pass at
  one exact committed head.
- [ ] Fresh independent exact-head review and human exact-head approval precede the observed merge.
- [ ] Final external handoff names the exact Stage A and binding components and releases the lease.

## Next Gate

Cook this three-phase plan only from exact input
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` after confirming no competing shared-contract writer.
No implementation or merge authority is granted by the plan commit itself.
