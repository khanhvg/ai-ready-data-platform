---
phase: 2
title: "Bind released Issue 8 Stage A contract"
status: pending
priority: P1
dependencies: [1]
effort: "0.5 implementation day after dependency release"
---

# Phase 2: Bind Released Issue #8 Stage A Contract

## Overview

Bind the future implementation to the exact released Issue #8 Stage A integration tree and consume
its contracts and validators read-only. The generic command-owner activation/version/evidence seam
is compatible with I5-04 without a shared-contract write. This finding is not plan validation,
readiness, cookability, or implementation authority.

## Context Links

- [Dependency assimilation](./implementation-boundary-and-design.md#released-dependency-assimilation-without-contract-invention)
- [RUN-DEP-01](./requirements-risk-threat-traceability.md#requirement-crosswalk)
- Live dependency: <https://github.com/khanhvg/ai-ready-data-platform/issues/8>
- Released handoff: <https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549>

## Requirements

- Exact released SHA, ordered parents, tree, live integration identity, and ancestry.
- Exact file paths, schema IDs/versions, content SHA-256 values, public commands, operation/lab
  boundaries, and activation/evidence rules from that Git tree.
- Read-only runner command authority, operation matrix, state/idempotency/problem/CSRF rules,
  evidence schemas, and generic command-owner activation semantics.
- Exact version placement and no implicit fallback/downgrade. Stage A defines no separate command
  version field and no generated-binding procedure; Issue #9 must not invent either.
- No modification or duplication of Issue #8-owned files.

## Released Dependency Identity

| Identity | Exact released value |
|---|---|
| Integration branch | `integration/issue-5-local-learning` |
| PR #23 merge | `5c2244c2c860234d0df49cf0a42ad950c6495717` |
| PR #25 merge / Stage A release / live integration head | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` |
| PR #25 ordered parent 1 | `5c2244c2c860234d0df49cf0a42ad950c6495717` |
| PR #25 ordered parent 2 | `734cf637a20ae186597e23d96a194ed4e30220ea` |
| Release tree | `27fc3667ef37892dad5c3fbfd76769f65a0760be` |
| Issue #7 / Make-fragment composition fix | shipped in the same current integration SHA |

PR #23 and its approved feature head are ancestors of the release. The future implementation head
is recorded only after it exists and must descend from the Stage A release; this plan never
fabricates that future SHA.

The release handoff records Stage A `56/56`, invalid fixtures `65/65`, operation matrix `16`, final
gate `4/4`, and inherited data/migration/evidence `19/19 + 1/1 + 13/13`, with zero owned
process/listener/temp leaks and `CLOUD_ACTION=none`.

## Exact Read-Only Interface Pins

| Path | Version / schema ID | SHA-256 | I5-04 use |
|---|---|---|---|
| `versions.md` | exact released tool/version matrix | `a87ec218bdcbb1e69f12b06662ee0ecb3a6a467aea09a7552b98c61bcf5f54e8` | Python 3.12.3 and released dependency/runtime placement |
| `learning/contracts/learning-contract-set-v1.json` | `learning-contract-set-v1`; set `issue-8-stage-a-v1` | `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638` | Sorted released file/hash closure |
| `learning/contracts/learning-contract-set-v1.schema.json` | `learning-contract-set-v1`; `https://contracts.local/learning/learning-contract-set-v1.schema.json` | `1cf55a7eeeff3d4a08340ae903d5f4e1812deb34849d99600296be507dd19648` | Closed schema for the release closure |
| `learning/contracts/learning-contract-version-registry-v1.json` | `learning-contract-version-registry-v1`; companion schema ID `https://contracts.local/learning/learning-contract-version-registry-v1.schema.json` | `a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb` | Exact readable/current families; adds readable fitness v2 while base current remains v1 and `emissionFallback` is null |
| `learning/contracts/learning-contract-version-registry-v1.schema.json` | `learning-contract-version-registry-v1`; `https://contracts.local/learning/learning-contract-version-registry-v1.schema.json` | `d8c1881982e39e727a95f7491e6efeb288335bbef4a80d76efa891c3a8009ab8` | Closed schema for the released overlay |
| `learning/contracts/schema-version-registry.json` | released base registry referenced by the overlay | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` | Immutable base readable/current-version authority |
| `learning/contracts/canonicalization-v1.json` | released RFC 8785 canonicalization profile | `2b985ef9c28e78c05b192c105b7f9d15fd60516c3a2c698d7da1bc315c605fce` | Canonical request/evidence hashing |
| `learning/contracts/command-owner-registry-v1.json` | `command-owner-registry-v1` | `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80` | Three reserved I5-04 rows and exact fragment/evidence-root identifiers |
| `learning/contracts/command-owner-activation-v1.schema.json` | `command-owner-activation-v1`; `https://contracts.local/learning/command-owner-activation-v1.schema.json` | `8fe337b7646fddc2dff4d1fc30e4a9120d0edec3f7eb293e8ead0e5d82f7a1f0` | Generic owner activation instance shape bound to base-registry and fragment hashes |
| `learning/contracts/command-owner-activation-i5-03-v1.json` | released `command-owner-activation-v1` instance | `d20c5db284c4528106a0943a1970e665c6dbcc33dfc3dd05f2a9b01570ae8941` | Read-only concrete instance demonstrating base/fragment/command/v2 binding; never copied as I5-04 authority |
| `learning/contracts/operation-matrix-v1.json` | `operation-matrix-v1`; companion schema ID `https://contracts.local/learning/operation-matrix-v1.schema.json` | `ffabcc11ca3943e3e520cd7b98c535032be439b1e2d1b920fe9ee17806180b1e` | 16 synchronous operations, five mutations, exact auth/CSRF/idempotency/CAS/problem/evidence rows |
| `learning/contracts/operation-matrix-v1.schema.json` | `operation-matrix-v1`; `https://contracts.local/learning/operation-matrix-v1.schema.json` | `98d77f883da45c47c6e277956ad31614003410ff43fea585fcdb432c4a12a128` | Closed schema for exact operation rows |
| `learning/contracts/completion-reconciliation-v1.json` | `completion-reconciliation-v1`; companion schema ID `https://contracts.local/learning/completion-reconciliation-v1.schema.json` | `8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff` | One progress authority, SHA-256+JCS idempotency, four-step commit and three reconciliation outcomes |
| `learning/contracts/completion-reconciliation-v1.schema.json` | `completion-reconciliation-v1`; `https://contracts.local/learning/completion-reconciliation-v1.schema.json` | `64fed79f088cff1d0d548448c7d40fdbc4b8e60b6d4e57c0f08cdfbcd0c2f769` | Closed schema for completion/reconciliation policy |
| `learning/contracts/fitness-result-v1.schema.json` | base current `fitness-result-v1`; `urn:ai-ready-data-platform:fitness-result-v1` | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` | Remains readable/current in the immutable base; not the activated I5-04 emission version |
| `learning/contracts/fitness-result-v2.schema.json` | `fitness-result-v2`; `https://contracts.local/learning/fitness-result-v2.schema.json` | `d53f9b7b68b9f313bf0b9259fe5042bfb8cdbca0001570c18cd937de4971d6c6` | Generic owner/command fitness envelope selected by an activation instance |
| `learning/contracts/learning-evidence-v1.schema.json` | `learning-evidence-v1`; `https://contracts.local/learning/learning-evidence-v1.schema.json` | `52a68529b72ecb7f24c59ebe52e16e4ee5f21660164b1d20570827b18be3fe47` | Learner verification evidence and immutable artifact references |
| `learning/contracts/lab-v1.schema.json` | `lab-v1`; `https://contracts.local/learning/lab-v1.schema.json` | `891c41100a28548e603ca1714aeaf5be2d541cd1780ab2ef72e3ef0740c6c16d` | Closed runner command/profile/workspace/resource contract |
| `learning/labs/promotion-trust/lab-v1.json` | `lab-v1`, document `1.0.0` | `89ece51f41a17821d3266d2ba1fb7680cb70b07c2e9c5566d473aac9978d42d8` | Exact eight zero-argument commands and bounded-local policy |
| `learning/contracts/lesson-v1.schema.json` | `lesson-v1`; `https://contracts.local/learning/lesson-v1.schema.json` | `9ece4e9cf5bf2a4dc375da13ce33ac7a696a374a225b0a7f9d1b9e089e7ea505` | Released lesson reader boundary |
| `learning/lessons/promotion-trust/lesson-v1.json` | `lesson-v1` | `758c6fb1ad75b283c313536d61bee61655bba6d27a2e685825ca20a28c838675` | Exact lesson input for the public lesson gate |
| `learning/contracts/progress-v1.schema.json` | `progress-v1`; `https://contracts.local/learning/progress-v1.schema.json` | `a24c27b0c9abf0d553f1005c6ff4b19506fa2b9be3888b5315356b91cdc30767` | Read-only progress authority referenced by completion reconciliation |
| `learning/contracts/promotion-trust-learning-manifest-v1.schema.json` | `promotion-trust-learning-manifest-v1`; `https://contracts.local/learning/promotion-trust-learning-manifest-v1.schema.json` | `6b04b9acdc6097c43ede39f22d048b1b3095b96563e568ec6e2bc52527bd0255` | Closed promotion-trust manifest schema |
| `learning/manifests/promotion-trust-v1.json` | `promotion-trust-learning-manifest-v1` | `553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac` | Exact lesson/lab/operation/completion binding |
| `learning/contracts/make-input-contract-v1.json` | released Make input grammar | `9ed76af1fca630de17acfcb904680f53d5d99a9692c2b2e10751c93587ca85c1` | Public Make scalar-input admission |
| `contracts/openapi/learning-platform-v1.yaml` | OpenAPI `3.2.0`, API `learning-platform-v1` | `f82434b815decd5f200aac08650e3d2cd7f572a600d0a0d7e5a4e8d2f09efe87` | Exact request/response/problem/version boundary |
| `contracts/openapi/learning-platform-openapi-profile-v1.schema.json` | `learning-platform-openapi-profile-v1`; `https://contracts.local/openapi/learning-platform-openapi-profile-v1.schema.json` | `208fa1686caf9685483ba889e38974fb696c1d0015721bd639ad6d27fe6439bd` | Exact semantic OpenAPI profile and schema hash for the YAML |
| `contracts/openapi/learning-platform-problem-details-v1.schema.json` | `https://contracts.local/openapi/learning-platform-problem-details-v1.schema.json` | `1af9440068c722732784d6c8a606da436de333ea8a77c12b4e545530ea11a1e9` | Closed redacted problem details |
| `scripts/learning_contracts/schema.py` | released reader/activation semantics | `caa137de02542a330a3621a057912eefce95c64775e423db6c61a8ef5f58d005` | `read_document`, `validate_document`, `validate_activation_semantics` |
| `scripts/learning_contracts/registry.py` | released version/command registry reader | `ca854421cef9880363929f3bea882f654cf3c8359ce3feecd3018febd1ce195d` | Exact readable/current and activation resolution |
| `scripts/learning_contracts/openapi.py` | released OpenAPI/profile verifier | `792e9805b2fa0d98fdd30a5b266457597c9b1f19d317a26c130a87cecb43c2c6` | API/operation/problem consistency |
| `scripts/learning_contracts/state.py` | released state verifier | `8149c9e976e2460570932d11b706a384587f00485ac078c63203d076f7e5c6a8` | Progress/workspace/operation transition validation |
| `scripts/learning_contracts/completion.py` | released completion verifier | `ce557d4f03d574a902ea2d20c60b3f62e292e92fa6507c45ef8e393b6405f0ac` | Idempotency/CAS/reconciliation validation |
| `scripts/learning_contracts/fitness.py` | released fitness verifier | `63c9729ffaa09f85d95d798c622565e106a9a730234e9102e5b6f20e3b060c20` | `verify_fitness(..., activation=...)` |
| `scripts/learning_contracts/evidence.py` | released learner evidence verifier | `aae9633c26e3e210e5f5b294bb44534795bae7e6002b8acbf9ecf46232b4949b` | Evidence/artifact/replay validation |
| `scripts/learning_contracts/canonical.py` | released RFC 8785 profile | `8649585335007e4afebf113263901f7ed84a28163ff648db95c930bf42e59113` | Exact canonical bytes and strict JSON parsing |
| `scripts/learning_contracts/check.py` | released aggregate contract checker | `7734233a9d704ef5720f7a97f97ce822900c9c880021fc843cfd529b86b3c955` | Contract-set/type/state/OpenAPI gate orchestration |
| `mk/issue-5/i5-03.mk` | released public Stage A command surface | `566acfb4956eafca4d91cf5efdc7f4205198a60cc5b988249975a614ff742576` | Runtime admission and the four public contract/evidence gates |

All 21 entries in `learning-contract-set-v1.json` reproduce their embedded content SHA-256, and
the registry pointer reproduces `a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb`.

### Exact readable/current version matrix

- Current/readable identity only: `lesson-v1`, `lab-v1`, `progress-v1`, `learning-evidence-v1`,
  `completion-reconciliation-v1`, `operation-matrix-v1`,
  `promotion-trust-learning-manifest-v1`, `learning-contract-version-registry-v1`,
  `command-owner-activation-v1`, and `learning-contract-set-v1`.
- `fitness-result` keeps base current/readable `fitness-result-v1`, adds readable
  `fitness-result-v2`, and has `emissionFallback: null`; I5-04 emits v2 only through its exact
  activation instance.

### Released compatibility boundaries

- The base registry reserves exactly `runner-test`, `runner-security-test`, and
  `runner-race-test` for owner `I5-04`, fragment `mk/issue-5/i5-04.mk`, security `S3`; their base
  rows remain `future-owner`/`not-runnable` until an I5-04-owned activation instance selects
  `implemented` plus `fitness-result-v2`.
- `fitness-result-v2` accepts owner `I5-04`, verifies exact activation owner/command/evidence
  version, requires SHA/hash/toolchain/invocation/artifact closure, caps `durationMs` at `120000`,
  and caps each referenced artifact at `10485760` bytes. Runner-specific detail belongs in hashed
  referenced artifacts, not unknown top-level fields.
- The promotion-trust lab pins profile `small-42`, workspace quota `268435456` bytes, and the exact
  zero-argument commands `workspace.prepare`, `retail.generate`, `retail.load`,
  `retail.dbt-build`, `retail.export`, `promotion.configure`, `promotion.verify`, and
  `workspace.reset`. Each command has `timeoutSeconds: 120`, `memoryBytes: 536870912`, network
  `denied`, risk `bounded-local`, and privilege `unprivileged`. A request cannot elevate or add an
  argument.
- API version is `learning-platform-v1`; operation rows are `apiVersion: v1`; mutation request
  schema versions are the released `*-request-v1` constants. There is no command-version field,
  implicit-latest rule, range, alias, or downgrade to implement.
- The OpenAPI request objects are closed, but minimum-only integer fields mean Stage A does not
  publish one finite maximum serialized HTTP-body byte count. The private runner therefore adopts
  a compatible stricter `RUNNER_REQUEST_BODY_LIMIT_BYTES=16384` before parse/allocation.
- No generated-binding command, output list, or hash appears in the release tree. Direct use of the
  released schemas/readers is the only currently pinned interface; generated output is forbidden.

### Released public commands

The future implementation clean-checkout gate may call only the public Stage A Make interfaces;
this amendment did not execute them or create their runtime state:

```bash
make learning-runtime-admit LEARNING_RUNTIME_CANDIDATE=<exact-candidate> LEARNING_RUNTIME_INTERPRETER_SHA256=<64-hex>
make learning-contracts-check LEARNING_RUNTIME_INTERPRETER_SHA256=<64-hex>
make api-contracts-check LEARNING_RUNTIME_INTERPRETER_SHA256=<64-hex>
make lesson-check LESSON=promotion-trust LEARNING_RUNTIME_INTERPRETER_SHA256=<64-hex>
make evidence-verify EVIDENCE=<emitted-repository-relative-locator> LEARNING_RUNTIME_INTERPRETER_SHA256=<64-hex>
```

`LEARNING_RUNTIME_ROOT` may be set only to the admitted private runtime root. Public `LESSON` and
`EVIDENCE` values remain scalar data; missing hashes/tools or hostile Make expansion fail closed.

## Related Code Files

- Create: `apps/lab-runner/config/released-contract-lock.json`
- Admit for Phase 3 creation: `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`
- Create: `apps/lab-runner/tests/unit/test_released_contract_lock.py`
- Consume read-only: only the exact released paths and hashes in the table above
- Modify/Delete: none outside `apps/lab-runner/**`

## Dependency Gate

`DEPENDENCY_COMPATIBILITY=pass`: Stage A intentionally provides the generic activation and
`fitness-result-v2` seam for later owners including I5-04. No shared-contract patch is needed.
The exact runner-owned activation path and 16,384-byte request ceiling are also resolved. Future
file/head hashes, host containment, and implementation behavior remain contemporaneous cook gates.

## Tests Before

1. Create mutation fixtures for wrong/missing SHA, non-ancestor release, changed contract bytes,
   unknown schema/API version, invented command version, absent operation, unexpected command/
   field/argument/environment key, wrong activation/base/fragment hash, evidence owner mismatch,
   oversized/ambiguous request framing, and backward-reader failure.
2. Make every dependency fixture fail with one typed `RUNNER_DEPENDENCY_*` code before startup or
   workspace allocation.
3. Assert no test reads a copied/fake contract under `apps/lab-runner/tests/fixtures`.

## Implementation Steps

1. Freshly fetch the integration and plan refs; reproduce the identity/ancestry/tree table above.
2. Verify every pinned path directly from the exact release Git tree and reproduce each SHA-256.
3. From the eventual implementation head, run the released public interfaces with their admitted
   runtime: `learning-runtime-admit`, `learning-contracts-check`, `api-contracts-check`,
   `lesson-check LESSON=promotion-trust`, and `evidence-verify EVIDENCE=<emitted-relative-locator>`.
   These commands are future gates and were not run by this amendment.
4. Validate the exact eight lab commands, API/operation versions, problem rows, completion/CAS/
   idempotency rules, closed evidence fields, durations, artifacts, and resource ceilings without
   a local contract extension.
5. Record only `apps/lab-runner/config/command-owner-activation-i5-04-v1.json` as the future
   activation path and its required binding to base registry SHA
   `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80`, the exact future fragment
   hash, owner `I5-04`, only the three reserved commands, and evidence version
   `fitness-result-v2`. Phase 3 creates the fragment first, then the instance, and computes/locks
   their hashes from actual bytes.
6. Record released SHA/path/version/hash references and the validated runner-owned policy values in
   `released-contract-lock.json`; do not copy a schema or claim a future containing commit.
7. Use the released readers directly. Do not create `generated/**`, a generated-type test, a
   command-version field, or a generator record because Stage A releases none.
8. Rerun all dependency mutation fixtures and retain the lock/result as runner-owned evidence.

## Refactor

None. Issue #8 contracts and validators remain read-only. Runner-local adapters may only call the
released readers; they must never become a competing public contract.

## Tests After

- Exact release passes; every one-byte/version/SHA/registry/activation mutation fails before
  readiness.
- Backward-reader/migration tests named by Issue #8 pass.
- `git diff` contains no `learning/contracts/**`, shared schema, or Issue #8 plan change.

## Regression Gate

- `released-contract-lock.json` is complete, non-recursive, and contains no guessed value.
- Runtime reports ready only when all locked inputs match.
- Missing required dependency tools are failure, not skip.
- The exact activation path, 16,384-byte body ceiling, release ancestry, and all read-only hashes
  are startup/readiness gates; any mismatch keeps the service disabled.

## Risk and Security

The primary risk is silently forking a shared security contract to unblock the runner. The only
accepted behavior is STOP and owner handback. Compatibility aliases, permissive unknown fields,
or locally patched schema copies are prohibited.

## Success Criteria

- [ ] Exact released Stage A SHA and contract identities are pinned and reproducible.
- [ ] Shared registry/evidence/operation ownership supports I5-04 without local writes.
- [ ] Exact I5-04-owned activation path and 16,384-byte runner limit are enforced; actual future
      fragment/instance hashes are measured and locked without prediction.
- [ ] All drift/mismatch cases fail closed before mutation.
- [ ] No fake contract, generated binding, command version, or future SHA exists.

## Next Steps

The capability amendment supersedes the earlier cook authorization. Phase 3 cannot begin even
after these release pins pass until the owner/platform resolves the exact dbt child requirement
and fresh validation/readiness restores a non-empty cook scope.
