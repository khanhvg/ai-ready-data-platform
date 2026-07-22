# Architecture and Curriculum Design

## Product Contract

The output is a Vietnamese-first learning product, not a documentation dump.

- Vietnamese is the primary title, instruction, symptom, hint, remediation, solution explanation,
  reflection, and text-alternative language. Established English terms may follow in parentheses
  and stable machine IDs remain language-neutral.
- Foundation learners receive guided context and progressive hints. Junior learners make a
  bounded design decision. Mid-level learners challenge forces, failure modes, operability,
  security, cost, and recovery. Instruction may be skipped after a diagnostic; verification may
  never be skipped.
- Every module is independently versioned through the I5-06-owned machine-valid curriculum
  schema and exact release binding. Issue #11 does not duplicate Issue #8 lesson, lab, progress,
  completion, evidence, operation-matrix, or portal-rendering truth.
- Every reusable template uses exact schema token
  `i5-06-architecture-template-registry-v1`, registry ID
  `i5-06-architecture-template-registry`, registry version `1.0.0`, canonical content hash,
  compatibility/supersession/removal declaration, and reciprocal per-instance exact
  ID/version/hash registry binding.
- Every module must expose prerequisites, observable outcome, starter, task, controlled failure,
  verify, evidence, reset, progressive hints, gated solution, reflection, and next path. Stage A
  may describe and statically validate that structure but cannot claim the executable elements ran.
- Portal publication and executable lifecycle are Stage B only, through exact released Issue #10
  renderer/registry seams.

## Trace Spine

Every publishable module must close this exact chain:

```text
Business outcome
  -> capability/value stream
  -> stakeholder + named concern
  -> FR + measurable NFR/ASR or explicit owner-blocking TBC
  -> compared options + named forces
  -> C4/data/integration/security/deployment views
  -> ADR and admitted pattern
  -> implementation intent at a real boundary
  -> automated evidence
  -> operations/resilience/security/cost/governance consequence
```

A missing or cyclic link fails `traceability-check`. A link to a heading, filename, or pattern name
without a stable ID and reciprocal reference does not count.

## Modular Foundation-to-Mid Graph

The graph preserves IDs and intent from the accepted master curriculum. Exact serialized fields
come from the I5-06 schemas; released Issue #8 identifiers and operation truth are read-only
references. Runtime prerequisite status is `not-executed-static-only` in Stage A.

| ID | Level | Vietnamese-first outcome | Prerequisites | Required question/failure | Evidence class |
|---|---|---|---|---|---|
| F01 | Foundation | Kết nối bên liên quan với kết quả kinh doanh | None | A technically correct result is not decision-useful | Concern/outcome mapping |
| F02 | Foundation | Mô hình hóa năng lực và dòng giá trị | F01 | Local optimization loses end-to-end ownership | Capability/value trace |
| F03 | Foundation | Chuyển FR/NFR/ASR thành tiêu chí đo được | F02 | “Nhanh, an toàn, tin cậy” has no threshold/owner | Requirement/TBC validation |
| F04 | Foundation | Đọc và chọn bộ C4 tối thiểu hữu ích | F03 | One giant diagram hides trust/state/deployment | Concern/view coverage + render/text |
| J01 | Junior | Ghi ADR và fitness function có thể kiểm chứng | F03, F04 | Decision drifts from code/config/evidence | ADR-to-test-to-evidence trace |
| J02 | Junior | Thiết kế API, xác thực và biên mạng | F04 | “Private” exists by convention only | Contract/reachability/security evidence |
| J03 | Junior | So sánh biên module/service theo lực thực | J02 | Logical API categories become premature services | Option matrix + physical-boundary ADR |
| J04 | Junior | Thiết kế trạng thái và khả năng chịu lỗi | J03 | Retry duplicates effects; overload cascades | Fault/replay/backpressure evidence |
| J05 | Junior | Bảo vệ biên thực thi và dữ liệu | J03, J04 | Input becomes traversal/RCE/object abuse | Threat review + negative evidence |
| J06 | Junior | Quyết định khi nào tách modular monolith thành service | J03 | Framework/service count drives extraction, or an “up” service cannot protect the decision path | Extraction ADR/dependency rule plus SLI/SLO/degradation evidence |
| D01 | Foundation/Junior | Hiểu grain, hợp đồng và nguồn quyết định | F03 | Equal totals hide semantic drift | Grain/contract trace; architecture content only |
| D02 | Junior | Mô hình hóa dbt, chất lượng và lineage | D01 | Controlled warnings are treated as failures or silently removed | Contract/lineage/warning oracle; graph content only, no data-lab runtime claim |
| D03 | Junior | Điều phối, retry và phục hồi pipeline | D02, J04 | Partial publication or retry reports false success | Task/recovery/idempotency evidence contract; graph content only, no data-lab runtime claim |
| D04 | Junior | So sánh metric/BI theo grain | D02 | Aggregate-of-aggregates changes a KPI | DuckDB/Rill conceptual mapping |
| D05 | Junior/Mid | Phân biệt object, Iceberg metadata và catalog pointer | D02, D03, D04 | Data exists but current pointer/catalog is absent | Lifecycle/recovery design evidence |
| D06 | Mid | Gắn data product với ownership/governance | D05 | Lineage lacks owner/classification/access intent | OpenMetadata identity/governance review |
| M01 | Mid | Thiết kế topology, state, scale và chi phí | J02-J06, D05 | Compute reaches zero but durable state/cost remains | Capacity/cost/state matrix |
| M02 | Mid | Thiết kế readiness, DR, RTO/RPO | M01, J04 | Office opens before restore/hydration is ready | Recovery/deployment dynamic review |
| M03 | Mid | So sánh local và AWS không giả vờ tương đương | D04, D05, M01 | DuckDB/Rill and ClickHouse/Superset silently diverge | Explicit invariants/deviations |
| M04 | Mid | Rà soát bảo mật hosted như một tương lai có gate | J05, M01 | Object ID is treated as authorization | Threat/security review; no hosted claim |

Graph rules:

- Acyclic; all nodes reachable from at least one foundation node.
- Missing/unknown prerequisite, self-edge, cycle, unreachable required node, or illegal skip fails.
- `D02`/`D03` preserve accepted graph identity and trace handoff only. Issue #11 does not create
  the I5-07 data-platform labs, verifiers, pipeline seams, or runtime evidence; those remain a
  separate owner/release. Static graph inclusion is not executable data-lab delivery.
- Required environment/tool probes are non-mutating and return learner-language remediation.
- Optional tool absence never forges a pass. AWS credentials, cloud access, Docker-heavy profiles,
  Rill UI, OpenMetadata UI, or Superset never block the foundation route.
- Challenge placement may skip instruction only after exact released prerequisite evidence is
  validated. Imported, edited, stale, or solution-only artifacts never satisfy completion.

## Module Learning Loop

Every module follows the same product interaction contract:

1. **Bối cảnh/outcome:** actor, decision, capability, success signal.
2. **Prerequisite checks:** released non-mutating probes and actionable remediation.
3. **Starter:** project-owned, bounded, versioned starting state.
4. **Task:** one observable architecture decision or artifact change.
5. **Controlled failure:** stable code, safe boundary, expected symptom, named lesson purpose.
6. **Diagnose:** evidence-first explanation; controlled/environmental/unexpected states distinct.
7. **Hints:** progressive, ordered, logged; never mutate state or completion.
8. **Reset:** idempotent, scoped, preserves prior immutable evidence, returns a verified starter.
9. **Verify/evidence:** deterministic assertions against the exact released verifier contract.
10. **Solution:** versioned, gated by reveal policy; presence cannot complete a module.
11. **Reflection:** trade-off prompt; informative, never an authority for completion.

Stage A may ship this as schema-valid static content with text alternatives. Stage B must prove the
real lifecycle through the Issue #10 renderer and the Issue #8 completion/evidence authority.

## Reusable Template Catalogue

Templates are structured content governed by released contracts, not free-form Markdown files.

| Stable content ID | Template | Required sections | Reject when |
|---|---|---|---|
| `tpl-stakeholder-concern` | Stakeholder concern | Actor, decision, outcome, concern, capability/value stream, owner | No decision/outcome or generic “user” |
| `tpl-fr-nfr-asr` | FR/NFR/ASR | Stable ID, type, statement, metric/threshold or explicit TBC, owner, verifier | Adjective-only NFR; unowned TBC |
| `tpl-option-matrix` | Option matrix | Decision, forces, constraints, 2+ viable options, failure modes, cost/ops/security, evidence, rejection reason | Winner by preference or framework fashion |
| `tpl-c4-view` | C4 view | Stable external ID, audience, concern, scope, type, source, expected elements/relations, legend, text alternative, trace IDs; L1 context and L2 container only when useful, L3 component only for a valuable high-risk boundary | Decorative/unowned view, forced level/L3, or mixed abstraction |
| `tpl-dynamic-sequence` | Dynamic/sequence | One critical flow, ordered steps, failure/retry/reset/recovery branch, actor/authority | Sequence adds no ordering insight |
| `tpl-deployment` | Deployment | Environment, compute/network/state/trust nodes, ownership, residual state/cost, failure/recovery | Diagram implies deployment or scale-to-zero |
| `tpl-adr` | ADR | Context, forces, decision, alternatives, consequences, status, supersession, requirements/views/tests/evidence | No alternatives/evidence or accepted TBC |
| `tpl-pattern-admission` | Pattern admission | Pattern, named force, concrete failure, quality attribute, boundary, verifier/evidence, removal trigger | Pattern without failure/evidence |
| `tpl-fitness-function` | Fitness function | Claim, scope, input/version, deterministic oracle, command owner, result/evidence, false-positive boundary | Prose-only or missing failure behavior |
| `tpl-capacity-cost` | Capacity/cost | Workload, assumptions, units, active/off-hours, bottleneck, residual cost, source date/TBC, sensitivity | Hard-coded stale price or “free at zero EC2” |
| `tpl-dr-recovery` | DR/recovery | Authority, backup/rebuild, failure point, RTO/RPO/TBC, restore verification, rollback | Backup exit code substitutes for restore |
| `tpl-security-review` | Security review | Assets, actors, trust boundaries, threats, controls, negative tests, residual risk, owner | Generic checklist/no threat model |

`architecture-templates-v1.json` is the one stable registry/definition document. Every instance
records the same registry ID, stable template ID, semantic version, and recomputed canonical hash;
the registry row reciprocally lists the exact sorted instance ID. Each row also carries the exact
schema/registry tokens, compatibility range, status, nullable predecessor binding, and consumer
list. A successor names the predecessor's exact ID/version/hash; a predecessor remains readable
while referenced. Removal requires zero references, registered compatible successor, passing
migration/rollback evidence, and a later explicit tombstone. Stage A v1 has exactly 12 active
rows and no removal. Unregistered copy, hash drift, one-way binding, unknown successor, or early
removal fails. Stable IDs above are Issue #11 content identities, not invented Issue #8 fields.

A flow marked critical because it crosses authority, state, deployment, security, resilience, or
recovery boundaries must be one of the amendment's exact 11 flow IDs. Its distinct ordered step
vector must equal the complete ordered canonical relation identities from the linked dynamic view
and bind every endpoint to exact deployment topology nodes/edges. Nonempty arrays, shared generic
steps, or prefixes do not pass. C4 L1/L2 are included only when they answer a named concern; L3 is
admitted only for a valuable high-risk internal boundary. A critical flow cannot waive dynamic/
deployment coverage with prose.

## Frozen Promotion Decision

The static promotion-publication example is a negative decision, not a generic four-grain label:

```text
decision = insufficient-evidence
reason = no-common-grain
```

Both separate fields are constants in the exact released
`learning/contracts/promotion-trust-v1.schema.json`. The Issue #11 validator must apply that
schema and reject changed, combined, missing, swapped, case-drifted, or alias values independently;
checking only runtime status or grain IDs is insufficient.

## System-Design Coverage and Pattern Admission

Each topic is taught only through named forces, a real failure, and executable or explicitly
Stage-A-static evidence.

| Topic | Named forces | Failure to teach | Admitted response/evidence |
|---|---|---|---|
| API/auth | Consumer intent, least privilege, idempotency, object scope | Browser/learner reaches privileged action or guesses object ID | OpenAPI operation/security trace; denial/idempotency evidence |
| Network | DNS, TLS, gateway/LB, subnet/route/egress, SG, discovery, mTLS where justified | “Private” service is publicly/rebinding reachable | Deployment/reachability policy evidence |
| Scaling | arrival rate, service time, state ownership, startup/readiness | More replicas amplify a stateful bottleneck | Capacity model + readiness/deployment evidence |
| Queue/backpressure | burst, consumer rate, durability, ordering, retry | Unbounded queue or producer overload creates stale/duplicate decisions | Bounded queue/backpressure option + saturation evidence |
| Cache | latency, freshness, key scope, invalidation, sensitivity | Stale/cross-tenant result is treated as current truth | TTL/invalidation/partition evidence; cache may be rejected |
| Partitioning | access pattern, skew, key cardinality, rebalancing | Hot partition or cross-boundary query collapse | Option matrix + skew/capacity evidence |
| Timeout/retry/jitter | latency distribution, deadline budget, idempotency | Retry storm duplicates effect or exceeds caller deadline | Deadline/retry budget + delayed-success/replay evidence |
| Circuit breaker | dependency failure rate, recovery, fallback truth | Cascading calls keep failing and consume capacity | State transition/fault evidence; admit only after failure exists |
| Bulkhead | shared resource contention, priority, blast radius | Optional catalog work starves core verification | Isolation/capacity evidence |
| Graceful degradation | core outcome, optional features, stale-data policy | Tool outage blocks all learning or silently serves stale truth | Explicit unavailable/read-only path + browser/static evidence |
| SLI/SLO | stakeholder outcome, measurement window, error budget | “Healthy” infrastructure cannot complete the decision journey | Outcome SLI/SLO template + evidence query |
| DR | authority, backup, restore dependency, RTO/RPO | Backup is present but empty restore fails | Restore/rebuild sequence + verification oracle |
| Capacity/cost | demand, headroom, cold start, residual services | 16 GiB host thrashes or off-hours bill remains unexplained | Capacity/cost matrix; no live AWS price claim in this issue |

Admission predicate, expressed independently of any unreleased schema field names:

```text
admit(pattern) only if
  pattern.forceIds is non-empty
  and pattern.failureId resolves
  and pattern.qualityAttributeId resolves
  and pattern.boundaryId resolves
  and pattern.verifierId resolves to retained evidence
  and the option/ADR explains rejection or removal conditions
```

The required negative `pattern-without-failure` fixture names a plausible pattern but omits its
failure link. It must fail with a stable released-compatible error and must not be “fixed” by
adding generic prose, a null verifier, or a fabricated evidence ID.

## OpenAPI and AsyncAPI Teaching

- Teach OpenAPI only against synchronous operations that exist in the exact released Issue #8
  operation matrix. Content explains method/path, `operationId`, logical taxonomy, physical
  process, authority, auth/CSRF, idempotency, problem result, and evidence. Issue #11 creates no
  competing OpenAPI document.
- Teach AsyncAPI only if a released dependency introduces a real channel with operations,
  messages, correlation, retry/dead-letter behavior, and security. Its absence is the correct
  outcome otherwise. A broker or event-driven service cannot be introduced for curriculum theater.
- Experience/Process/System/Backend/Technical remain logical ownership categories, never five
  forced services.

## Local and AWS Architecture Mapping

The mapping is architecture content only. It creates no credentials, resources, plans, applies,
endpoints, or deployment claim.

| Concern | Local learning mapping | AWS learning mapping | Honest shared invariant / divergence |
|---|---|---|---|
| Analytics / `BR-ANALYTICS-01` | DuckDB | ClickHouse | Data-product/query intent shared; engine/type/performance behavior differs |
| BI / `BR-BI-01` | Rill | Superset | Decision/metric definition shared; runtime and metadata ownership differ |
| Governance / `BR-GOVERNANCE-01` | OpenMetadata local profile | OpenMetadata on ECS/EC2 with durable DB/search decisions | Asset identity/owner/lineage intent shared; topology/recovery differ |
| Lake/catalog / `BR-LAKE-01` | MinIO + Lakekeeper + Iceberg | S3 + admitted Iceberg catalog | Iceberg lifecycle concepts shared; auth/catalog/state differ |
| Compute / `BR-COMPUTE-01` | Host processes and mutually exclusive profiles | ECS on EC2/capacity provider | Workload intent shared; scheduling, network, IAM, readiness differ |
| State/recovery / `BR-STATE-01` | Local files/volumes and deterministic rebuild | S3/catalog/DB/search/evidence authorities | Every authority and restore oracle must be explicit |
| Security / `BR-SECURITY-01` | Single local actor, loopback/private runner | Hosted identity/object authorization remains gated | No hosted security claim from local evidence |
| Cost / `BR-COST-01` | 16 GiB resource envelope | Active/off-hours plus residual services | Units/assumptions visible; no apply or current-price claim here |

Each bridge binds exact source relations to exact target topology paths and records the preserved
invariant, explicit divergences, and `claimClass=conceptual-only`. It closes comparison trace only;
it cannot satisfy a local runtime, hosted runtime, deployment, readiness, RTO/RPO, security, or
cost claim.

## Architecture View Contract

### Immutable Issue #6 set

`C4-L0`, `C4-L1`, `C4-L2-LOCAL`, `C4-L3-RUNNER`, `DEP-LOCAL`, and `DYN-JOURNEY` are read-only in
source, manifest mapping/row semantics, rendered SVG/text, and semantic projection. They are
referenced, never copied or regenerated into Issue #11-owned paths as a second truth.

### Proposed Stage A additions-only expansion

| ID | Type | Audience / concern | Required content |
|---|---|---|---|
| DYN-PUBLISH | Dynamic | Data owner/operator / partial publication and recovery | stage, object write, catalog pointer, ingest, verify, retry/resume/rollback |
| C4-L2-AWS | Container | Architecture/security/operations / stateless vs stateful ownership | ingress, portal/BFF, jobs, ClickHouse, Superset, OpenMetadata, S3/Iceberg, state/readiness |
| DEP-AWS | Deployment | Network/IAM/FinOps / topology, trust, residual state/cost | DNS/TLS/LB, VPC/AZ/subnets/routes/egress/SG/endpoints, ECS/EC2, state/log/KMS/secrets annotations |
| DYN-OFFICE | Dynamic | Operations / usable office-hours readiness | open, capacity, restore/hydrate, health/equivalence, ready, drain/checkpoint/close/residual inventory |
| DYN-RESTORE | Dynamic | Reliability/data owner / empty-environment recovery | restore/register, hydrate/rebuild, metadata/search/evidence recovery, equivalence, RTO/RPO TBC |

These IDs and semantics come from accepted master inputs. The exact source/render paths are the 19
`architecture/expansions/i5-06/**` create-only paths in the
[Stage A amendment](./stage-a-release-amendment.md). A separate extension and render manifest bind
the protected base identities without appending or regenerating them.
AWS views use visible `TBC — blocks aws-apply` annotations for budget, retention, readiness SLO,
RTO/RPO, account/environment, and approver. A diagram never means a resource exists.

## Deterministic Render and Semantic Rules

The Stage A amendment binds exact tools/paths and the cook must prove:

1. Two isolated clean renders of every expansion view produce byte-identical normalized SVG and
   UTF-8/NFC/LF structured text outputs.
2. Source-closure, semantic-row, computed-projection, tool/lock/renderer/normalizer, SVG, and text
   SHA-256 values are retained without recursive self-hashing.
3. Text alternatives come from computed semantics, not SVG scraping, and contain audience,
   concern, scope, elements, relations, dynamic order/deployment hierarchy, limitations, and TBCs.
4. No expansion external ID, internal key, element ID, relationship identity, output path, or
   manifest row overwrites or semantically aliases the protected six.
5. A semantic mutation changes the projection/text/render freshness result; a layout-only change
   cannot erase meaning.
6. SVG rejects scripts, `foreignObject`, external URLs/images, credentials, private/absolute
   paths, and hidden deployment claims.
7. No browser, native GUI, manual broad matrix, Structurizr fallback, native Graphviz fallback,
   or unpinned resolver is introduced.
8. New titles and primary labels are Vietnamese-first; source relation labels have no ordinal and
   the renderer/text adds exactly one matching ordinal.
9. At fitted widths 1440 and 1024 CSS px, titles remain at least 18 px, primary node/relation text
   14 px, secondary text 12 px; aspect ratio is at most 2.4:1; WCAG contrast thresholds pass.
10. Painted/text bounds stay on canvas, peer content does not overlap, containment padding is at
    least 8 px, outer padding 4 px, and no label/relation clips or exits the canvas.
11. Text alternatives preserve exact ordered relation identities, deployment hierarchy, bridge/
    claim class, limitations and TBCs. Machine metrics plus fresh independent human inspection at
    both fitted widths are mandatory for the five new views.

## Stage B Executable Architecture Lab

The one lab covers F01 → F04 → J01/J04/J05 around a concrete retail publication decision:

- **Outcome:** preserve a trustworthy promotion evidence publication when a downstream
  governance/catalog dependency becomes slow or unavailable.
- **Starter:** bounded released-contract workspace containing stakeholder concern, FR/NFR draft,
  option matrix, view/ADR references, and no completed answer.
- **Task:** choose and justify a boundary/resilience design; link forces, failure, security,
  operability, cost, and evidence.
- **Controlled failure:** a pattern or boundary is proposed without a named failure/verifier, or
  retry behavior lacks deadline/idempotency/backpressure and fails the architecture fitness oracle.
- **Hints:** progressively expose concern → requirement → failure → option → ADR → verifier links.
- **Reset:** use the exact Issue #8/#10 released reset lifecycle; return to starter while retaining
  prior immutable evidence.
- **Verify:** deterministic trace, ADR, pattern-admission, view, and resilience assertions.
- **Evidence:** bind exact input/dependency/content/verifier/tool hashes and the committed reset and
  verified run. Completion flows only through Issue #8 authority.
- **Solution/reflection:** gated solution explains trade-offs; reflection cannot complete.

The lab does not implement a queue, broker, cache, AWS service, data pipeline, or portal route. It
teaches and verifies the architecture decision through released execution/rendering seams.

## Unresolved Questions

None for Stage A. Exact Stage B portal renderer fields remain delegated to a later Issue #10
release-bound amendment and are not guessed here.
