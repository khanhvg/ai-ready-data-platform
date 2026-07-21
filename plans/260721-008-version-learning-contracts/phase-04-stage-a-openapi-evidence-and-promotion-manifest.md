---
phase: 4
title: "Stage A OpenAPI evidence and promotion manifest"
status: pending
priority: P1
dependencies: [3]
stage: "A"
---

# Phase 4: Stage A OpenAPI, Evidence, and Promotion Manifest

<!-- Updated: Validation Session 1 - exact wire/version/error and descriptor-bound evidence contracts. -->

## Context Links

- [Operation inventory](./phase-03-stage-a-operations-completion-and-guidance.md#operation-inventory)
- [Promotion-trust analytical contract](../260721-005-enterprise-learning-sandbox/execution-authority-and-release-contract.md#promotion-trust-analytical-contract)
- [Issue #6 promotion fixture handoff](../260721-006-freeze-golden-baseline/issue-7-fixture-and-merge-handoff.md)

## Overview

Publish the synchronous OpenAPI boundary and exact operation-matrix mapping, complete learner
evidence provenance/integrity semantics, and validate the first framework-neutral promotion-trust
lesson/lab/aggregate manifest against the shipped Issue #6 fixture. No selected stack, content
renderer, browser route, portal/runner implementation or completion mutation is introduced.

## Requirements

- Functional: OpenAPI 3.2.0 document with all sixteen operations, closed reusable schemas,
  relative refs, examples, typed problem details, correlation/idempotency and declared trust rules.
- Functional: exact two-way set equality among method/path, `operationId`, operation matrix and
  examples; no raw SQL or arbitrary command surface.
- Functional: exact per-operation request/success/error/version/auth/idempotency contract below;
  `verifyWorkspace` admission returns `202` and never returns completion.
- Functional: learner evidence binds lesson/lab/run/operation, actor mode, input/golden/dependency/
  contract/verifier/fixture hashes, state transitions, assertions, artifacts, tools/environment,
  timestamps, redaction/retention, canonical payload hash and rollback result.
- Functional: promotion-trust lesson/lab/aggregate manifests preserve four independent grains,
  explicit limitations, required probes, hints/remediation, conclusion and fixture hashes.
- Non-functional: OpenAPI is documentation/contract only. It does not claim auth/session/CSRF,
  process or persistence implementation; `enforcementStatus=downstream-required` is explicit.
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
- The locked YAML reader is constrained to a single JSON-compatible YAML 1.2-shaped document: no
  duplicate keys, aliases/anchors/merge keys, tags, multiple documents, implicit non-JSON scalars,
  BOM, trailing content or unsafe numbers. The normalized model is JCS-hashed after source checks.
- A future need outside this profile requires a manifest-admitted validator/tool decision and a
  fresh plan/readiness scope; the implementer may not fetch a linter or expand the profile silently.

### Evidence layers

1. Learner evidence: `learning-evidence-v1`, immutable domain proof used by progress completion.
2. Contract-check fitness evidence: additive `fitness-result-v2`, selected for I5-03 by its exact
   command activation and stored under the issue evidence root. It proves invocation, owner,
   tools/SHAs/hashes/results/redaction/retention/rollback; shipped v1 remains an I5-01
   compatibility/blast-radius input. Future reserved owners can consume v2 only through their own
   matching activation instance.

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
| Create | `scripts/learning_contracts/openapi.py` | constrained YAML parse/profile/ref/matrix/example/security checks |
| Create | `scripts/learning_contracts/evidence.py` | learner payload canonical hash, artifact/provenance/redaction verification |
| Create | `learning/lessons/promotion-trust/lesson-v1.json` | framework-neutral lesson manifest |
| Create | `learning/labs/promotion-trust/lab-v1.json` | framework-neutral lab manifest |
| Create | `learning/manifests/promotion-trust-v1.json` | aggregate promotion-trust release manifest |
| Modify | `tests/contracts/learning/test_evidence_provenance.py` | close complete provenance, locator, local-claim and redaction RED IDs |
| Modify | `tests/contracts/learning/test_openapi_contract.py` | profile/ref/example/matrix/AsyncAPI inventory checks |
| Modify | `tests/contracts/learning/test_evidence_tamper.py` | canonical/artifact/verifier/fixture/recursive tamper checks |
| Modify | `tests/contracts/learning/test_promotion_trust_manifest.py` | first manifest and four-grain mutation checks |
| Create | `tests/fixtures/learning/contracts/valid/learning-evidence-v1.json` | third-reader learner-evidence vector |
| Create | `tests/fixtures/learning/contracts/valid/promotion-trust-v1.json` | third-reader promotion-trust vector |
All invalid evidence/OpenAPI/promotion fixtures already exist from Phase 1. Phase 4 modifies tests,
not RED IDs, paths or expected codes.

The shipped `tests/fixtures/learning/promotion-trust/{evidence-v1.json,manifest.json}` and every
existing `learning/contracts/*` Issue #6 file are read-only inputs; no “normalized” replacement is
written back.

## Exact OpenAPI Wire Contract

API major negotiation is path-based: only `/v1`. JSON request bodies require
`Content-Type: application/json` and their named `schemaVersion`; responses return
`X-Learning-Contract-Version: learning-platform-v1` and echo `X-Correlation-ID`. There is no
implicit latest-version negotiation, content sniffing or downgrade. Unknown API path version is
`404 API_VERSION_UNSUPPORTED`; unsupported body schema version is `422
CONTRACT_VERSION_UNSUPPORTED`; unsupported media type is `415 MEDIA_TYPE_UNSUPPORTED`.

All non-health operations require `localSession`, `X-Correlation-ID` and the matrix authorization;
resource reads require actor ownership or catalog-read authorization. All five mutations also
require exact Host/Origin, CSRF, `Idempotency-Key`, and canonical request hashing. Health permits
public loopback only and has no credential detail. These are declared downstream requirements, not
Stage A enforcement claims.

The exact common problem set is rule-based, not “as applicable”: every non-health operation
declares `400 CORRELATION_ID_INVALID`, `401 AUTHENTICATION_REQUIRED`, `403
AUTHORIZATION_DENIED`, and `500 INTERNAL_CONTRACT_ERROR`. Every mutation additionally declares
`400 REQUEST_INVALID`, `403 ORIGIN_OR_CSRF_INVALID`, `409 IDEMPOTENCY_KEY_REUSE`, `415
MEDIA_TYPE_UNSUPPORTED`, and `422 CONTRACT_VERSION_UNSUPPORTED`. `404
API_VERSION_UNSUPPORTED` is the exact response for an unsupported API-major route and is not
attached to a valid operation. The table below adds the complete operation-specific set; no other
status/code pair is admitted in v1.

| Operation | Request | Success | Complete operation-specific typed errors in addition to the exact common set above |
|---|---|---|---|
| `listLessons` | query `cursor,limit`; no body | `200 LessonPage` | `400 PAGE_ARGUMENT_INVALID` |
| `getLesson` | path `lessonId`; no body | `200 Lesson` | `404 LESSON_NOT_FOUND` |
| `getProgress` | query `cursor,limit`; no body | `200 ProgressPage` | `400 PAGE_ARGUMENT_INVALID` |
| `getLessonProgress` | path `lessonId`; no body | `200 Progress` | `404 PROGRESS_NOT_FOUND` |
| `createWorkspace` | `CreateWorkspaceRequest-v1` | `201 Workspace` | `404 LAB_NOT_FOUND`, `409 WORKSPACE_ALREADY_EXISTS`, `412 PREREQUISITE_FAILED`, `422 LAB_PARAMETER_INVALID` |
| `getWorkspace` | path `workspaceId`; no body | `200 Workspace` | `404 WORKSPACE_NOT_FOUND` |
| `startWorkspaceOperation` | `StartOperationRequest-v1` | `202 OperationAccepted` | `404 WORKSPACE_NOT_FOUND`, `409 WORKSPACE_OPERATION_CONFLICT`, `412 WORKSPACE_REVISION_CONFLICT`, `422 COMMAND_ID_OR_ARGUMENT_INVALID` |
| `getOperation` | path `operationId`; no body | `200 Operation` | `404 OPERATION_NOT_FOUND` |
| `resetWorkspace` | `ResetWorkspaceRequest-v1` | `202 OperationAccepted` | `404 WORKSPACE_NOT_FOUND`, `409 WORKSPACE_OPERATION_CONFLICT`, `412 WORKSPACE_REVISION_CONFLICT` |
| `verifyWorkspace` | `VerifyWorkspaceRequest-v1` | `202 OperationAccepted` | `404 WORKSPACE_NOT_FOUND`, `409 WORKSPACE_OPERATION_CONFLICT`, `412 WORKSPACE_REVISION_CONFLICT`, `422 VERIFIER_INPUT_INVALID` |
| `getEvidence` | path `evidenceId`; no body | `200 LearningEvidence` | `404 EVIDENCE_NOT_FOUND`, `409 EVIDENCE_QUARANTINED` |
| `listTools` | no body | `200 ToolPage` | none beyond common set |
| `getTool` | path `toolId`; no body | `200 Tool` | `404 TOOL_NOT_FOUND` |
| `queryDataProduct` | `RegisteredQueryRequest-v1` | `202 OperationAccepted` | `404 DATA_PRODUCT_NOT_FOUND`, `409 QUERY_OPERATION_CONFLICT`, `422 QUERY_ID_OR_PARAMETER_INVALID` |
| `getLiveness` | no auth/body | `200 HealthStatus` | `500 HEALTH_INTERNAL_FAILURE` with bounded detail |
| `getReadiness` | no auth/body | `200 HealthStatus` | `503 DEPENDENCY_NOT_READY` with bounded dependency IDs only |

Closed mutation request field sets are exact:

| Request schema | Required fields |
|---|---|
| `CreateWorkspaceRequest-v1` | `schemaVersion,labVersion,contractSetSha256,parameters,expectedProgressRevision` |
| `StartOperationRequest-v1` | `schemaVersion,commandId,arguments,expectedWorkspaceRevision` |
| `ResetWorkspaceRequest-v1` | `schemaVersion,expectedWorkspaceRevision,preserveEvidence` where `preserveEvidence` is `true` in v1 |
| `VerifyWorkspaceRequest-v1` | `schemaVersion,verifierId,expectedWorkspaceRevision,expectedProgressRevision` |
| `RegisteredQueryRequest-v1` | `schemaVersion,workspaceId,queryId,parameters,expectedWorkspaceRevision` |

Closed response envelopes are also exact. Page envelopes require
`schemaVersion,items,nextCursor`; `Workspace` requires
`schemaVersion,workspaceId,labId,labVersion,state,revision,activeOperationId,links`;
`OperationAccepted` requires
`schemaVersion,operationId,status,requestSha256,workspaceRevision,pollAfterMs,links`;
`Operation` requires
`schemaVersion,operationId,workspaceId,kind,status,requestSha256,revision,resultRef,failure,
createdAt,updatedAt`; `Tool` requires
`schemaVersion,toolId,status,required,deepLink,remediationId`; `HealthStatus` requires
`schemaVersion,status,checks`. Nullable fields are explicitly typed and remain required so omission
cannot create a second shape. `Lesson`, `Progress` and `LearningEvidence` reference the Stage A
domain schemas directly rather than copying them.

Common `application/problem+json` has exactly `type,title,status,code,detail,correlationId,retryable,
remediationId,contractVersion`; it is closed and bounded. `detail` is learner-safe and never contains
stack trace, raw subprocess output, SQL/command text, secret, absolute path or existence-sensitive
authorization detail. Every declared status/example/profile reference is checked two ways against
the operation matrix. The released `/v1` wire contract is frozen: implementation changes may not
alter any declared request/response field, status, operation, idempotency rule, error code or
completion/state semantic. Any wire addition, removal, rename or semantic change requires `/v2`,
retained `/v1` contract/readers, explicit version negotiation and an accepted migration/rollback
plan.

## Additional OpenAPI Boundary Details

- Browser-facing mutations require `Idempotency-Key` and `X-Correlation-ID`; matrix records exact
  session/CSRF expectation and future enforcing owner.
- The HTTP contract never exposes a privileged execution transport. Its abstract process roles do
  not map to or read portal/runner modules in Stage A.
- `POST /v1/data-products/{productId}/queries` accepts a fixed registered query/assertion ID and
  typed parameters only. Raw SQL, filesystem paths, shell fragments and network destinations are
  absent.
- `GET /v1/operations/{operationId}` returns bounded status for polling. No webhook, queue, topic,
  SSE channel or bidirectional stream is claimed in v1.
- Health endpoints expose bounded state only; no secret, private path or dependency credential.
- Problem details use stable code, safe learner message, correlation ID, retryability and optional
  remediation ID; stack traces/raw subprocess output are forbidden.

## Evidence Provenance and Locator Contract

Every future check result under `.artifacts/evidence/learning-contracts/<run-id>/` records:

```text
schemaVersion, commandId, status, failureCode, exact command
inputSha, testedTreeSha, dependencyMergeShas, contract/fixture/schema hashes
toolchain and frozen-lock hash, startedAt/finishedAt/durationMs
redactionClass, retentionClass, artifacts {relative locator, mediaType, size, sha256}
rollback status/result, canonicalization profile, payloadSha256
```

The v2 `invocation` object stores bounded public argv, canonical role-based child argv, an optional
SHA-256 of actual private argv and a fixed working-directory role. It never stores an absolute
private executable/workspace path. `owner` and `commandId` are accepted only when the exact active
command row selects v2.

Learner evidence additionally records the lesson/lab versions, local actor mode/ID, workspace/run/
operation IDs, ordered transitions, verifier ID/hash, assertions, sanitized parameters and the
referenced data/contract release. It must never contain tokens, environment dumps, PII canaries,
Terraform plans/state, raw SQL/command output or absolute paths.

Every artifact locator is evidence-root-relative POSIX syntax with nonempty safe components and no
`.`/`..`, backslash, NUL, URI scheme, drive/absolute prefix or private home component. Validation
opens the prevalidated evidence root and each component descriptor-relative with no-follow,
requires a regular single-link file, rechecks device/inode, bounds bytes, then verifies declared
size and SHA-256 from the opened descriptor. Symlink, hardlink, device/FIFO/socket, race/substitution,
oversize and hash mismatch are distinct typed failures. Evidence verification is read-only and
never trusts a locator merely because its normalized string appears beneath the root.

## Tests Before

- Keep Phase 1 OpenAPI/evidence/promotion RED IDs unchanged.
- Add one mutation per operation metadata field and two-way missing/extra operation set.
- Reuse the Phase 1 missing/extra/remote/cyclic `$ref`, invalid example, unsupported profile,
  version-negotiation and orphan-AsyncAPI vectors.
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
2. Implement constrained offline YAML/profile/ref/example/matrix validation using only admitted
   `PyYAML 6.0.3`, `jsonschema 4.26.0` and standard-library modules.
3. Implement learner-evidence canonical integrity and safe provenance/artifact checks.
4. Author promotion lesson and lab manifests, then the aggregate hash/reference manifest.
5. Close API/evidence/promotion RED suites and run complete Stage A tests.
6. Re-run dependency-absence/decoy invariance and protected hashes.

## Success Criteria

- [ ] All sixteen operations validate and exactly match the matrix.
- [ ] Problem, idempotency, correlation, auth/CSRF intent and evidence metadata are complete.
- [ ] Every request, success, problem status, version rule and compatibility outcome above is exact.
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
before publication. Before release, rejected Issue #8 drafts are not published. After release,
rollback reselects the previous external contract while retaining every published OpenAPI/domain
manifest version and evidence record; Issue #6 files/evidence stay intact.

## Next Steps

Phase 5 builds public commands, compatibility/rollback proof and the candidate Stage A release
handoff for independent exact-head implementation review and human pre-merge approval—not an
automatic PR, merge or release authorization.
