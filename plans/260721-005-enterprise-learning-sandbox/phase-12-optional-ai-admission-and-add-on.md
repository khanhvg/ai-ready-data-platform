---
phase: 12
title: "Optional AI Admission and Add-on"
status: pending
priority: P3
dependencies: [7, 9, 11]
effort: "L"
---

# Phase 12: Optional AI Admission and Add-on

<!-- Updated: Validation Session 1 - classified all file destinations as planned artifacts. -->

## Overview

Keep AI, LangGraph, Restate and Bedrock AgentCore out of the core until a machine-readable
admission gate proves governed data, identity/ACL, citations/evals, policy, observability,
approval, durability, recovery and cost. Only then build an optional add-on; it cannot block the
first local site.

## Context Links

- [ADR-019/020](./architecture-decisions.md)
- [AI competencies A01-A03](./curriculum-and-competency-map.md)
- Discovery source register S19-S21 and PH-C07/PH-H10
- SC-11/12/15 and hosted identity follow-up I5-14

## Requirements

- Core independence test passes with no AWS account, model key or optional network.
- Every retrieval source is a versioned governed data product with owner, classification,
  contract, quality and OpenMetadata lineage.
- Hosted cross-role ACL propagates through indexing, retrieval, citation and tools; local
  single-user proof alone cannot claim multi-user safety.
- Provenance binds source/product/version/chunk/query/run and exposes unsupported claims.
- Fixed eval dataset covers retrieval, groundedness, safety, task success and regression.
- Deterministic policy outside model reasoning controls allowed tools/data/action/approval.
- OTel-compatible traces correlate run/retrieval/model/tool/approval/cost and implement
  redaction/retention/deletion.
- Side effects require explicit human approval, expiry, actor identity, idempotency and uncertain
  outcome reconciliation. Start read-only.
- Durable workflow/approval/idempotency state is not AgentCore Runtime session memory.
- Region availability, per-run limits, concurrency, monthly ceiling, alarm and kill switch pass
  before credentialed execution.
- AgentCore modules are selected individually; LangGraph/Restate responsibilities are explicit.

## Leading First Use Case

If admitted, begin with a **read-only governed retail architecture/data-product evidence
assistant** that answers from versioned architecture, ADR, mart contract and OpenMetadata
artifacts with citations. It has no write tool. Owner approval is still required after eval/cost
evidence.

LangGraph is a candidate for visible retrieval/reasoning steps. Restate is not admitted for this
read-only use case unless a durable workflow failure is demonstrated; it becomes relevant only
for later side-effect/recovery labs. AgentCore Runtime/Identity/Observability/Evaluations are
considered individually; Memory/Gateway/Browser/Code Interpreter are not default requirements.

## Architecture

```text
Portal -> AI BFF -> identity/ACL policy -> retrieval adapter -> governed index
  -> graph/workflow -> model -> citation/unsupported-claim verifier
  -> trace/eval/cost evidence
  -> (later only) approval -> allow-listed tool -> durable idempotency/reconciliation
```

Durable state sits in the admitted workflow/progress store, never ephemeral runtime memory.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `ai/admission/gates.yaml`, `ai/admission/check.py` | 300-500 LOC | Machine blocker |
| Create | `ai/contracts/{retrieval,citation,policy,approval,trace}.schema.json` | 500-800 lines | Contract tests |
| Create | `ai/evals/{dataset,thresholds,runner}/**` | 800-1,200 lines/LOC | Deterministic eval |
| Create | `apps/agent-labs/**` only after admission | 1,500-2,500 LOC | Optional app |
| Create | `platform/adapters/agentcore/**` only after module ADR | 500-900 LOC | Cloud adapter |
| Create | `tests/ai/{acl,injection,citation,redaction,approval,replay,recovery,cost}/**` | 1,500-2,200 LOC | Safety/eval |
| Modify | portal optional route/feature flag | bounded | Core-off regression |
| Modify | architecture optional AI component/dynamic views | bounded | Admission-rendered only |

## Interface Checklist

- [ ] `RetrievalRequest(actor, purpose, productVersions, query)`
- [ ] `Citation(sourceId, version, chunk, contentHash, accessDecision)`
- [ ] `PolicyDecision` deterministic and auditable
- [ ] `Approval` actor/scope/expiry/replay protection
- [ ] `WorkflowCheckpoint` and idempotency/reconciliation
- [ ] trace/redaction/retention/cost schema
- [ ] AgentCore adapter isolated from core payloads

## Dependency Map

- Requires governed data labs, AWS decisions/adapters and I5-14 for hosted cross-role claims.
- Entire phase is optional and does not block Phases 5, 8 or local Phase 13 release.
- Credentialed AgentCore work remains separately authorized after region/cost/apply gates.

## Admission Thresholds

Hard invariants:

- zero unauthorized cross-role retrieval/citation;
- 100% cited source existence/version/hash match;
- zero unapproved write/tool invocation;
- 100% duplicate side-effect suppression/reconciliation in admitted write tests;
- 100% secret/PII canary redaction from user-visible evidence and retained traces.

Retrieval recall/precision, groundedness/task-success and per-run cost/latency thresholds remain
TBC until a fixed corpus/baseline is measured. TBC blocks AI cook/credentialed tests, not core.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Cross-role document retrieved/cited | Deny without existence leak; admission fails |
| Critical | Prompt/tool injection bypasses policy | Deterministic deny; trace redacted |
| Critical | Runtime crash/retry around side effect | Resume/reconcile/idempotency; no duplicate |
| Critical | Approval expired/replayed/different actor | Deny and audit |
| Critical | PII/secret in source/prompt/citation/trace | Redact/delete per policy; admission fails on leak |
| High | Unsupported claim/citation mismatch | Mark unsupported; eval fails threshold |
| High | Retry storm/model/tool spend | Quota/kill switch; attempts accounted |
| High | AgentCore unavailable/no credentials | Core and optional-disabled portal pass |

## Tests Before

Write adversarial fixed evals and a failing admission report before any agent implementation.
Include ACL, injection, unsupported claims, redaction, approval/replay, crash/resume and cost.

## Refactor

No core refactor. Add optional adapter/route behind feature/admission flag; reuse identity,
evidence and governed-data contracts.

## Tests After

Run deterministic local/model-stub policy tests, then explicitly authorized model/AgentCore evals
with exact region/model/module/cost evidence. Re-run core with AI disabled and credentials absent.

## Regression Gate

```bash
make ai-admission-check
make local-journey-e2e AI_ENABLED=false
# make ai-evals is optional and credential-gated only after all TBC/authority gates clear.
```

## Implementation Steps

1. Define admission schema and failing adversarial evals.
2. Inventory governed products, identity/ACL and trace/retention readiness.
3. Measure corpus baseline; request owner thresholds/use-case/module/cost approval.
4. Stop if any gate/TBC remains. Do not scaffold agent runtime as a workaround.
5. If admitted, implement read-only retrieval/citation/policy/eval path.
6. Select LangGraph/Restate/AgentCore modules by explicit responsibility ADR.
7. Add optional portal experience, OTel/cost evidence and core-off regression.
8. Admit write tools only in a later issue with approval/idempotency/recovery proof.

## Success Criteria

- [ ] Admission is machine-readable and all required gates pass before implementation.
- [ ] Core remains credential/network/model independent.
- [ ] First AI use case is governed, read-only, cited and evaluated.
- [ ] ACL/redaction/approval/replay/recovery/cost hard invariants pass.
- [ ] No AgentCore module or framework is included without a lesson/responsibility.

## Risk, Security, and Rollback

AI can leak governed data and amplify cost/effects. Default off, deny-by-default retrieval/tools,
short retention and kill switch are mandatory. Rollback disables the feature, revokes
identities/tools, deletes indexes/traces under policy and preserves core evidence/data products.

## Next Steps

Only a separate authorized issue may run credentialed AgentCore deployment or add side-effect
tools.
