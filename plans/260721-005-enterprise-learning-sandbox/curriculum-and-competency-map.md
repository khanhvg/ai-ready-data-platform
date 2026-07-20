# Curriculum and Competency Map

## Curriculum Contract

Audience spans foundation/junior through mid-level. Progress is competency-based, not
scroll-based. Every module must point to a business outcome, a quality attribute or failure, the
architecture/pattern that addresses it, and executable evidence. Named technology without that
chain is excluded.

Priority:

1. Enterprise architecture, business outcomes, C4, FR/NFR/ASR, ADR, API/network/system design.
2. Data pipeline, modeling, quality, lakehouse, governance.
3. Optional governed AI.

## Personas

| Persona | Entry capability | Learning need | Completion evidence |
|---|---|---|---|
| Foundation learner | Can use a browser and terminal with guided commands | Connect stakeholder concern to system behavior; read context/container/dynamic views | Guided journey evidence plus reflection; may use remediation |
| Junior engineer/architect | Reads code/SQL/API schemas; basic Git/Docker | Turn FR/NFR into boundaries, contracts, patterns, tests, and ADRs | Runs labs, diagnoses controlled failures, changes a bounded artifact, passes verify |
| Mid-level engineer/architect | Owns components and operational trade-offs | State ownership, resilience, security, cost, recovery, migration, hosted evolution | Challenge path, alternative ADR, recovery/equivalence evidence |

Diagnostic entry may skip instruction but never verification. Imported or edited evidence cannot
mark completion.

## Competency Graph

```text
F01 business outcomes/stakeholders
 └─► F02 capability/value stream
      └─► F03 FR/NFR/ASR traceability
           ├─► F04 C4 context/container/dynamic/deployment
           │    └─► J01 ADRs and architecture fitness functions
           └─► J02 network and API boundaries
                └─► J03 modular monolith, DDD and logical API taxonomy
                     ├─► J04 resilience/state/idempotency
                     ├─► J05 safe execution boundary
                     └─► J06 service extraction criteria

D01 raw data/grain/contracts
 └─► D02 dbt modeling/quality/lineage
      ├─► D03 orchestration/reset/retry
      ├─► D04 metrics/BI/data products
      └─► D05 Iceberg/catalog
           └─► D06 governance/data products

F03 + J01 + J04 + D06
 └─► M01 AWS deployment/state/cost/recovery
      ├─► M02 scheduled readiness/recovery
      ├─► M03 cross-engine analytics
      └─► M04 hosted multi-user security/operations

D06 + J04 + M04
 └─► A01 governed retrieval and evaluation
      └─► A02 optional agents/tools/approval/recovery
           └─► A03 AgentCore deployment admission
```

## Learning Sequence

| ID | Level | Module / outcome | Required failure or question | Architecture/pattern taught | Evidence | Prerequisites |
|---|---|---|---|---|---|---|
| F01 | Foundation | Stakeholders and business outcomes | A dashboard number is technically correct but not decision-useful | Stakeholder/concern map; outcome metric | Concern-to-measure mapping test | None |
| F02 | Foundation | Capability and value-stream map | Teams optimize local tasks but lose end-to-end ownership | Capability map, value stream, bounded context | Trace from promotion decision to data product | F01 |
| F03 | Foundation | FR/NFR/ASR | “Fast, secure, reliable” has no threshold or owner | FR/NFR/ASR template; measurable acceptance | Requirement schema + threshold/TBC classification | F02 |
| F04 | Foundation | Minimum useful C4 | One giant diagram hides deployment/state boundaries | Context, container, one component, selected dynamic/deployment views | Structurizr validate/render and concern coverage | F03 |
| F05 | Foundation | First promotion-trust journey | Gross revenue ignores fulfillment, returns, and DQ warnings | Business/data/control flow; verified data product | Failure-reset-verify-evidence E2E | F01-F04, D01 intro |
| J01 | Junior | ADRs and fitness functions | Architecture decisions drift from code/config | ADR status/decision/consequence; executable fitness | ADR-to-test link check | F03-F04 |
| J02 | Junior | Network fundamentals | A service is “private” only by convention | DNS, TLS, gateway, LB, subnet, route, SG, service discovery, mTLS where justified | Deployment view + reachability/policy tests | F04 |
| J03 | Junior | API and domain boundaries | Five logical API categories become five premature services | Experience/Process/System/Backend/Technical taxonomy; DDD; BFF | OpenAPI taxonomy lint; physical container count rationale | J02 |
| J04 | Junior | State and resilience | Reset races publish; retry duplicates an effect | State, Command, Strategy, idempotency, timeout/jitter, circuit breaker/bulkhead when failure demands | Race/replay/fault evidence | J03 |
| J05 | Junior | Safe execution boundary | Learner parameters become shell/traversal/RCE | Facade, typed Command allow-list, Chain of Responsibility validation | Fuzz/traversal/secret-canary tests | J03-J04 |
| J06 | Junior | Modular monolith to services | Framework/service count drives architecture | Modular monolith, Adapter, Repository, extraction criteria | ADR and dependency rule tests | J03 |
| D01 | Foundation/Junior | Data grain and deterministic input | Same row totals hide changed anomaly semantics | Schema/data contract, deterministic generation | Double-run checksums/anomaly summary | F03 |
| D02 | Junior | dbt modeling and quality | Controlled warnings are mistaken for failure or silently removed | Source/staging/intermediate/core/mart, quality severity | dbt contract/lineage/warning oracle | D01 |
| D03 | Junior | Orchestration and recovery | Partial publish/retry reports false success | Task graph, state/idempotency, reset/resume | Airflow graph + injected-failure recovery | D02, J04 |
| D04 | Junior | Metrics, BI and product contract | Aggregate-of-aggregates produces wrong KPI | Metric grain/weighting, semantic contract, local Rill | DuckDB/Rill query equivalence | D02 |
| D05 | Junior/Mid | Iceberg and catalog | Data exists but pointer is absent, or stale catalog survives rename | Adapter/Factory, snapshot/pointer, schema evolution/time travel, reconciliation | Lifecycle/fault/read-back/OpenMetadata evidence | D02-D04 |
| D06 | Mid | Governance and data products | Lineage exists but owner/classification/access intent does not | Product owner, catalog, policy, logical vs physical assets | OpenMetadata entity/lineage/tag/reconcile tests | D05 |
| M01 | Mid | AWS topology, IAM and cost | EC2 zero is claimed as “zero cost” while stateful services remain | Deployment view, IAM, state owner, cost BOM | Terraform static/policy/mock plan + priced inventory | J02-J06, D05 |
| M02 | Mid | Scheduled readiness/recovery | Office opens but portal/data is not ready; close loses active work | State machine, drain/checkpoint, readiness, RTO/RPO | Clock/open/close/restore drills | M01, J04 |
| M03 | Mid | Cross-engine analytics | DuckDB and ClickHouse silently diverge | Adapter/Strategy, contract equivalence, rebuild projection | Cross-engine edge/query/metric suite | D04-D05, M01 |
| M04 | Mid | Hosted identity and object authorization | Learner guesses another workspace/evidence ID | Identity/trust, object authorization, audit, tenant isolation | Cross-user denial and non-enumeration | J05, M01 |
| A01 | Optional Mid | Governed RAG | Retrieval crosses ACL or cites wrong version | Repository/Adapter, provenance, ACL propagation, evaluation | Denial/citation/groundedness/redaction evals | D06, M04 |
| A02 | Optional Mid | Agent workflow and tools | Retry duplicates spend or side effect | State/Command, approval, idempotency; LangGraph/Restate only if needed | Replay/approval/crash/cost kill-switch evals | A01, J04 |
| A03 | Optional Mid | AgentCore deployment | Managed runtime is treated as durable state | Runtime vs durable workflow state, IAM, OTel, cost | Admission checklist and credential-gated non-core E2E | A02, M01-M02 |

## Pattern Admission Map

| Pattern | Admit only when | Example lab | Do not teach as |
|---|---|---|---|
| Factory / Abstract Factory | Local/AWS adapter construction would otherwise leak engine choice | DuckDB/ClickHouse or Lakekeeper/Glue adapter selection | Class hierarchy trivia |
| Builder | A versioned lesson/evidence object has staged validation | Lesson authoring/compiler pipeline | Fluent API for its own sake |
| Lifecycle-scoped Singleton via DI | One expensive catalog/client per process needs controlled lifecycle | Catalog client fixture | Global mutable state |
| Adapter | External engines expose different physical APIs behind a shared learning contract | BI, catalog, analytics adapters | Pretend local/AWS behavior is identical |
| Facade | Portal needs one safe use-case API over several tools | Lab BFF | God service |
| Strategy | Verification/reset/resource policy varies by profile | Local/AWS verifier | Conditionals moved without value |
| State | Legal lab/run transitions and recovery matter | failure-reset-verify | UI enum only |
| Command | Privileged actions need typed allow-list, audit, idempotency | generate/load/verify/reset | Arbitrary shell wrapper |
| Observer | Real status updates exist | in-process/SSE run status | Broker added for a demo |
| Chain of Responsibility | Ordered validation/policy checks need isolated reasons | input/workspace/authz/resource checks | Long middleware chain without distinct policy |
| Repository | Progress/evidence storage must evolve from local to hosted | evidence repository | Generic CRUD abstraction everywhere |
| BFF | Browser must not receive runner credential or external-tool complexity | Portal server proxy | Separate service per page |
| Saga / Outbox / Idempotent Consumer | Hosted async multi-step side effects exist | Later publish/agent workflow | First local synchronous slice |

## First Journey Competency Rubric

| Competency | Foundation pass | Junior pass | Mid-level extension |
|---|---|---|---|
| Business framing | Names stakeholder and decision | Maps outcome to FR/NFR and data product | Challenges threshold and ownership |
| Architecture views | Reads context/container/dynamic | Explains runner/data boundaries | Proposes justified alternative and consequence |
| Data quality | Identifies controlled warning | Traces raw anomaly through dbt/mart | Defines contract/migration guard |
| Decision | Selects a documented trade-off | Records rationale in bounded ADR response | Compares alternatives with measurable ASR |
| Recovery | Runs reset safely | Explains state transition/idempotency | Diagnoses injected race/fault |
| Verification | Passes deterministic verifier | Interprets failed assertion and remediation | Audits evidence integrity/equivalence |
| Accessibility | Completes without motion dependency | Uses keyboard/static architecture view | Reviews accessibility fitness evidence |

Completion requires verifier success and evidence integrity. Reflection improves competency
feedback but cannot override a failed lab.

## Curriculum Release Gates

- No lesson publishes without a valid lesson/lab contract and prerequisite graph.
- No pattern/service appears without a controlled failure or quality attribute it resolves.
- Every numeric claim points to generated evidence, not hand-maintained prose.
- Foundation route completes without AWS credentials, optional tools, or animation.
- Challenge route may skip instruction but cannot bypass reset/verify/evidence.
- AI modules stay hidden/off until admission; their absence does not reduce core completion.
