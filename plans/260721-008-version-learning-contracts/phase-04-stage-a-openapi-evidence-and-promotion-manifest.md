---
phase: 4
title: "Stage A OpenAPI evidence and promotion manifest"
status: pending
priority: P1
dependencies: [3]
stage: "A"
---

# Phase 4: Stage A OpenAPI, Evidence, and Promotion Manifest

## Context Links

- [Operation inventory](./phase-03-stage-a-operations-completion-and-guidance.md#operation-inventory)
- [Promotion-trust analytical contract](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md#promotion-trust-analytical-contract)
- [Issue #6 promotion fixture handoff](../260721-006-freeze-golden-baseline/issue-7-fixture-and-merge-handoff.md)

## Overview

Publish the synchronous OpenAPI boundary and exact operation-matrix mapping, complete learner
evidence provenance/integrity semantics, and validate the first framework-neutral promotion-trust
lesson/lab/aggregate manifest against the shipped Issue #6 fixture. No selected stack, content
renderer, browser route, runner implementation or completion mutation is introduced.

## Requirements

- Functional: OpenAPI 3.2.0 document with all sixteen operations, closed reusable schemas,
  relative refs, examples, typed problem details, correlation/idempotency and declared trust rules.
- Functional: exact two-way set equality among method/path, `operationId`, operation matrix and
  examples; no raw SQL or arbitrary command surface.
- Functional: learner evidence binds lesson/lab/run/operation, actor mode, input/golden/dependency/
  contract/verifier/fixture hashes, state transitions, assertions, artifacts, tools/environment,
  timestamps, redaction/retention, canonical payload hash and rollback result.
- Functional: promotion-trust lesson/lab/aggregate manifests preserve four independent grains,
  explicit limitations, required probes, hints/remediation, conclusion and fixture hashes.
- Non-functional: OpenAPI is documentation/contract only. It does not claim auth/session/CSRF,
  runner or persistence implementation; those states are explicit in the matrix.
- Protocol: bounded HTTP polling is the only long-operation pattern in v1. No channel/broker exists,
  so no AsyncAPI file, directory or command is created.

## Architecture

### JSON Schema / OpenAPI boundary

- JSON Schema files remain the source of truth for lesson, lab, progress, learner evidence,
  completion and operation documents.
- `learning-platform-v1.yaml` references those schemas by repository-relative path and defines
  HTTP parameters, request/response envelopes, problem details and examples. It does not copy a
  second divergent schema body.
- `learning-platform-openapi-profile-v1.schema.json` is a closed, project-owned offline profile
  for the exact OpenAPI 3.2.0 subset used here. The semantic validator also resolves every `$ref`,
  checks operation/matrix equality and rejects unsupported or security-ambiguous features. This is
  not represented as a universal OpenAPI validator.
- A future need outside this profile requires a manifest-admitted validator/tool decision and a
  fresh plan/readiness scope; the implementer may not fetch a linter or expand the profile silently.

### Evidence layers

1. Learner evidence: `learning-evidence-v1`, immutable domain proof used by progress completion.
2. Contract-check fitness evidence: existing `fitness-result-v1`, stored under the issue evidence
   root and proving commands/tools/SHAs/hashes/results.

Both use strict I-JSON/RFC 8785/SHA-256 but are never interchangeable. The local digest provides
corruption detection only. Hosted signing/key authority remains I5-14.

### Promotion-trust documents

- `lesson-v1.json`: stakeholder question, outcome, acts, refs, probes, hints, evidence threshold,
  accessibility/static requirements and remediation.
- `lab-v1.json`: typed inputs/workspace/registered command IDs, controlled failure, state/reset/
  verify/evidence rules. It defines authorization intent but executes nothing.
- `promotion-trust-v1.json`: aggregate manifest referencing the exact lesson, lab, evidence schema,
  read-only Issue #6 data contract and tracked fixture hashes. Stage A omits any web binding.

The aggregate records promotion (`promo_name, channel`), fulfillment (`carrier, region`), returns
(`reason, category, region`) and global DQ (`scenario`) as independent evidence grains. It must
conclude `insufficient-evidence` with reason `no-common-grain`; no campaign-level causal join is
permitted.

## Related Code Files

| Action | Exact path | Purpose |
|---|---|---|
| Create | `contracts/openapi/learning-platform-v1.yaml` | synchronous API source contract |
| Create | `contracts/openapi/learning-platform-openapi-profile-v1.schema.json` | closed offline subset/profile validator schema |
| Create | `contracts/openapi/learning-platform-problem-details-v1.schema.json` | typed bounded problem response |
| Create | `scripts/learning_contracts/openapi.py` | YAML parse/profile/ref/matrix/example/security checks |
| Create | `scripts/learning_contracts/evidence.py` | learner payload canonical hash, artifact/provenance/redaction verification |
| Create | `learning/lessons/promotion-trust/lesson-v1.json` | framework-neutral lesson manifest |
| Create | `learning/labs/promotion-trust/lab-v1.json` | framework-neutral lab manifest |
| Create | `learning/manifests/promotion-trust-v1.json` | aggregate promotion-trust release manifest |
| Create | `tests/contracts/learning/test_evidence_provenance.py` | complete provenance, local-claim and redaction tests |
| Modify | `tests/contracts/learning/test_openapi_contract.py` | profile/ref/example/matrix/AsyncAPI inventory checks |
| Modify | `tests/contracts/learning/test_evidence_tamper.py` | canonical/artifact/verifier/fixture/recursive tamper checks |
| Modify | `tests/contracts/learning/test_promotion_trust_manifest.py` | first manifest and four-grain mutation checks |
| Add fixtures | `tests/fixtures/learning/contracts/valid/{learning-evidence-v1,promotion-trust-v1}.json` | third-reader valid vectors |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/evidence/{stale-verifier-hash,recursive-identity,missing-dependency-sha}.json` | evidence negatives |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/openapi/{missing-idempotency,raw-sql-query,remote-ref}.json` | API negatives |
| Add fixtures | `tests/fixtures/learning/contracts/invalid/promotion-trust/{missing-limitation,fixture-hash-drift}.json` | grain/provenance negatives |

The shipped `tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}` and every
existing `learning/contracts/*` Issue #6 file are read-only inputs; no “normalized” replacement is
written back.

## OpenAPI Boundary Details

- Browser-facing mutations require `Idempotency-Key` and `X-Correlation-ID`; matrix records exact
  session/CSRF expectation and future enforcing owner.
- Browser never calls the runner directly. Operations map to portal BFF modules and private runner
  adapters without multiplying physical services.
- `POST /v1/data-products/{productId}/queries` accepts a fixed registered query/assertion ID and
  typed parameters only. Raw SQL, filesystem paths, shell fragments and network destinations are
  absent.
- `GET /v1/operations/{operationId}` returns bounded status for polling. No webhook, queue, topic,
  SSE channel or bidirectional stream is claimed in v1.
- Health endpoints expose bounded state only; no secret, private path or dependency credential.
- Problem details use stable code, safe learner message, correlation ID, retryability and optional
  remediation ID; stack traces/raw subprocess output are forbidden.

## Evidence Provenance Contract

Every future check result under `.artifacts/evidence/learning-contracts/<run-id>/` records:

```text
schemaVersion, commandId, status, failureCode, exact command
inputSha, testedTreeSha, dependencyMergeShas, contract/fixture/schema hashes
toolchain and frozen-lock hash, startedAt/finishedAt/durationMs
redactionClass, retentionClass, artifacts {relative locator, mediaType, size, sha256}
rollback status/result, canonicalization profile, payloadSha256
```

Learner evidence additionally records the lesson/lab versions, local actor mode/ID, workspace/run/
operation IDs, ordered transitions, verifier ID/hash, assertions, sanitized parameters and the
referenced data/contract release. It must never contain tokens, environment dumps, PII canaries,
Terraform plans/state, raw SQL/command output or absolute paths.

## Tests Before

- Keep Phase 1 OpenAPI/evidence/promotion RED IDs unchanged.
- Add one mutation per operation metadata field and two-way missing/extra operation set.
- Add missing/extra/remote/cyclic `$ref`, invalid example, unsupported profile feature and orphan
  AsyncAPI inventory vectors.
- Tamper learner payload, artifact, verifier, dependency, fixture, state transition and integrity;
  inject secret/private-path/PII canaries and recursive commit fields.
- Mutate each promotion grain/order/calculation/filter/limitation, expected conclusion and exact
  fixture/data contract hash.

## Refactor

Keep transport validation separate from domain schema/state validation. Reuse one ref resolver and
one safe bounded error type. Promotion manifests reference canonical contract IDs/hashes; they do
not embed copied Issue #6 evidence or preview/Vite schema.

## Tests After

- OpenAPI/profile/refs/examples and operation matrix are exactly aligned.
- No AsyncAPI path exists and the channel inventory is empty.
- Valid learner evidence canonicalizes and verifies; every tamper/leak vector fails.
- Promotion lesson/lab/aggregate manifests validate against the exact Issue #6 fixture hashes and
  cannot assert a common grain or completion before trusted evidence.
- Read-only Issue #6 data/evidence/migration suites pass with unchanged hashes.

## Implementation Steps

1. Add the closed OpenAPI profile/problem schema, then author the sixteen-operation OpenAPI source.
2. Implement offline YAML/profile/ref/example/matrix validation using only admitted Python modules.
3. Implement learner-evidence canonical integrity and safe provenance/artifact checks.
4. Author promotion lesson and lab manifests, then the aggregate hash/reference manifest.
5. Close API/evidence/promotion RED suites and run complete Stage A tests.
6. Re-run dependency-absence/decoy invariance and protected hashes.

## Success Criteria

- [ ] All sixteen operations validate and exactly match the matrix.
- [ ] Problem, idempotency, correlation, auth/CSRF intent and evidence metadata are complete.
- [ ] No AsyncAPI artifact exists without a channel.
- [ ] Learner and fitness evidence are distinct, closed, provenance-complete and tamper-detecting.
- [ ] Promotion-trust manifests preserve the four grains and exact Issue #6 fixture/data hashes.
- [ ] No Vite/ADR/preview byte or framework-specific field exists in Stage A outputs.

## Risk Assessment

- A project OpenAPI profile can be mistaken for full spec validation. Mitigation: name/claim it as
  the exact supported subset, cover used semantics exhaustively and STOP before unsupported use.
- YAML parsing can introduce ambiguity. Mitigation: OpenAPI alone uses safe YAML parsing plus
  duplicate-key rejection; executable domain/evidence manifests remain strict JSON.
- Manifest authoring can copy the provisional preview contract. Mitigation: derive only from master
  normative contract + shipped Issue #6 fixture; Stage A boundary scan forbids Issue #7 refs.

## Security and Rollback

Remote refs, raw queries/commands, sensitive examples, recursive identity and hash mismatch fail
before publication. Rollback removes only new OpenAPI/domain manifest versions and reselects the
previous external contract release; Issue #6 files/evidence stay intact.

## Next Steps

Phase 5 builds public commands, compatibility/rollback proof and the candidate Stage A release
handoff for independent validation/readiness—not an automatic merge authorization.
