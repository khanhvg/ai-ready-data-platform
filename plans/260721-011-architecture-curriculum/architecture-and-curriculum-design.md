# Architecture and Curriculum Design

## Design Boundary

Stage A is a Vietnamese-first, machine-valid static learning product. It creates exactly 20
modules, 12 registered templates, 11 critical flows, eight conceptual bridges, and five useful
source-derived views. It does not execute a learner journey, reset, progress, completion, portal,
hosted environment, cloud action, or learner evidence. Exact paths and verification behavior are
in the [Stage A v4 amendment](./stage-a-release-amendment.md).

## Reciprocal Learning Trace

Every stable module closes and reciprocally references:

```text
business outcome -> capability/value stream -> stakeholder concern
-> FR plus measurable NFR/ASR or owner-blocking TBC
-> options/forces/trade-offs -> C4/data/integration/security/deployment views
-> ADR/admitted pattern -> implementation intent -> automated verifier/evidence
-> operations/resilience/security/cost/governance consequences
```

A heading, filename, non-reciprocal identifier, generic pattern name, or duplicate learning
signature does not count.

## Exact Twenty-Module Progression

| ID | Level | Vietnamese-first outcome | Prerequisites | Distinct controlled failure |
|---|---|---|---|---|
| F01 | Foundation | Kết nối bên liên quan với kết quả kinh doanh | None | Correct output is not decision-useful |
| F02 | Foundation | Mô hình hóa năng lực và dòng giá trị | F01 | Local optimization loses ownership |
| F03 | Foundation | Chuyển FR/NFR/ASR thành tiêu chí đo được | F02 | Adjectives have no threshold/owner |
| F04 | Foundation | Chọn bộ C4 tối thiểu hữu ích | F03 | One giant diagram hides boundaries |
| J01 | Junior | Ghi ADR và fitness function kiểm chứng được | F03, F04 | Decision drifts from evidence |
| J02 | Junior | Thiết kế API, xác thực và biên mạng | F04 | “Private” is only convention |
| J03 | Junior | So sánh biên module/service theo lực | J02 | Logical categories become services |
| J04 | Junior | Thiết kế trạng thái và khả năng chịu lỗi | J03 | Retry duplicates and overload cascades |
| J05 | Junior | Bảo vệ biên thực thi và dữ liệu | J03, J04 | Input becomes traversal/RCE/object abuse |
| J06 | Junior | Quyết định lúc tách service | J03 | Framework count drives extraction |
| D01 | Foundation/Junior | Hiểu grain, hợp đồng và nguồn quyết định | F03 | Equal totals hide semantic drift |
| D02 | Junior | Mô hình hóa dbt, chất lượng và lineage | D01 | Warning is failed or silently erased |
| D03 | Junior | Điều phối, retry và phục hồi pipeline | D02, J04 | Partial publication reports success |
| D04 | Junior | So sánh metric/BI theo grain | D02 | Aggregate-of-aggregates changes KPI |
| D05 | Junior/Mid | Phân biệt object, Iceberg metadata và pointer | D02, D03, D04 | Data exists without current catalog |
| D06 | Mid | Gắn data product với ownership/governance | D05 | Lineage lacks owner/classification |
| M01 | Mid | Thiết kế topology, state, scale và chi phí | J02, J03, J04, J05, J06, D05 | Compute stops but state/cost remains |
| M02 | Mid | Thiết kế readiness, DR, RTO/RPO | M01, J04 | Office opens before hydration |
| M03 | Mid | So sánh local/AWS trung thực | D04, D05, M01 | Engines silently diverge |
| M04 | Mid | Rà soát bảo mật hosted có gate | J05, M01 | Object ID is authorization |

The graph is exact, acyclic, reachable, and progressive. Foundation is guided; junior requires a
bounded choice among viable options; data connects authority/grain/quality; mid challenges
failure, operability, security, cost, recovery, or governance.

## Required Module Lifecycle

Every module has module-specific, nonempty, typed objects for:

1. `starter` — bounded versioned initial artifact and non-mutating prerequisite probes;
2. `task` — one observable architecture decision/artifact;
3. `controlledFailure` — stable symptom, safe boundary, and learning purpose;
4. `verify` — deterministic oracle through a real public route;
5. `evidence` — expected static proof and reciprocal trace identity;
6. `reset` — scoped idempotent design returning to starter without claiming execution;
7. `hints` — ordered progressive disclosure that does not mutate state;
8. `solution` — versioned content behind an explicit reveal gate;
9. `tradeOffReflection` — module-specific options/forces/consequences; and
10. `operationsConsequence` — operations, resilience, security, cost, and governance.

All carry `executionStatus=not-executed-static-only`. Canonical task/failure/reflection/
consequence bodies and the whole learning signature are unique across 20 modules. Missing fields,
renamed clones, generic repeated prose, duplicate signatures, or level regression fail through
the existing 22-family/82-code catalogue.

## Exact Twelve-Template Catalogue

The one registry contains exactly `tpl-stakeholder-concern`, `tpl-fr-nfr-asr`,
`tpl-option-matrix`, `tpl-c4-view`, `tpl-dynamic-sequence`, `tpl-deployment`, `tpl-adr`,
`tpl-pattern-admission`, `tpl-fitness-function`, `tpl-capacity-cost`, `tpl-dr-recovery`, and
`tpl-security-review`. All v1 rows use `1.0.0`, exact schema/registry tokens, canonical
hash-excluded body hashes, closed compatibility, active status, `supersedes=null`, and reciprocal
instance bindings. Every consuming binding has one stable unique `instanceId` and repeats the
exact registry ID, template ID, version, content hash, and registry-row compatibility object; the
registry's sorted consuming-ID set and discovered instance-ID set are identical.

Successors increase semantic version and bind exact predecessor ID/version/hash plus migration,
rollback, and compatibility. Referenced predecessors remain readable/deprecated. Removal requires
zero instances, a compatible replacement, successful migration/rollback, and a later tombstone.
The [closed lifecycle contract](./stage-a-release-amendment.md#closed-template-lifecycle) defines
the real 11/13/duplicate/hash/supersedes/removal/orphan fixtures.
Those fixtures include independent duplicate/drifted instance-ID and instance-compatibility
mutations through the existing nonreciprocal and compatibility codes.

## Exact Flows and Conceptual Bridges

The 11 flow IDs and eight bridge IDs are closed in the amendment. Every flow step equals one exact
ordered dynamic relation and deployment topology identity. Generic step arrays, nonempty/prefix
checks, or a conceptual bridge used as runtime evidence fail.

The governance row is concrete:

```text
protected relation: learning.adapters -> retail
protected local path: local.developer_host.adapters_instance -> local.developer_host.retail_instance
expansion relations: exact DYN-PUBLISH physical/logical ingestion identities
expansion topology: exact DEP-AWS OpenMetadata compute/database/search identities
bridge: BR-GOVERNANCE-01, claimClass=conceptual-only
```

All references are reciprocal. The invariant is asset identity/owner/classification intent while
topology and recovery differ. The content preserves honest `retail_iceberg` physical and
`retail_duckdb` logical catalog views and does not fabricate cross-service lineage.

## Five-View Architecture Contract

| ID | Type | Decision concern |
|---|---|---|
| `DYN-PUBLISH` | Dynamic | partial publication, ingestion, retry/resume, verification |
| `C4-L2-AWS` | Container | stateless/stateful ownership and trust boundaries |
| `DEP-AWS` | Deployment | topology, IAM/network intent, durable state, residual cost |
| `DYN-OFFICE` | Dynamic | open/readiness/drain/checkpoint/close lifecycle |
| `DYN-RESTORE` | Dynamic | empty-environment authority recovery and equivalence |

Locked LikeC4 export and DOT are the sole semantic source; locked WASM Graphviz produces the raw
SVG. Normalized published SVG, structured text, and evidence-only fitted HTML are derived from the
same semantics-preserving representation. Hardcoded node/relation cards and hidden hash-only
freshness are forbidden. Visible identities/order/labels match source/text/manifest; real relation
mutations visibly change SVG/HTML/text. Two isolated runs are byte-deterministic.

All five views are Vietnamese-first, singly numbered, safe, text-equivalent, readable without
horizontal scrolling, and geometry/contrast/fit checked at 1440 and 1024 CSS-pixel widths. The
cook records truthful self-inspection; future independent inspection is a separate bundle.

## Real Platform Teaching Boundaries

- OpenAPI teaching references only the 16 released operations. No competing spec is created.
- AsyncAPI states no released channel and invents no broker/channel/schema.
- Local DuckDB/Rill/OpenMetadata/Iceberg and AWS ClickHouse/Superset/OpenMetadata/S3/ECS-EC2 are
  conceptual mappings only, with explicit divergences and no deployability claim.
- AWS content contains no account, endpoint, credential, resource ID, current price, provider
  invocation, plan/apply command, or cloud action.
- Protected Issue #6 views and tools are referenced read-only and never copied into tracked Issue
  #11 paths as a second truth.

## Stage B Boundary

The top-level curriculum manifest and stable IDs are the only future renderer seam. No Issue #10
route, module, viewport, completion signal, or lab behavior is predicted. A later Stage B
amendment must bind an actual passing merged Issue #10 journey and released renderer.
