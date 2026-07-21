# Requirements and Risk Traceability

## Traceability Rules

- A requirement is implementation-ready only after it has an owner, stage, exact dependency
  release, closed file/command allow-list, architecture/ADR link, test, evidence, rollback, and
  clearing authority.
- Every requirement below is a plan obligation. It is not current cook authority.
- Stable IDs are reciprocal: curriculum content, views, ADRs, tests, and evidence must point to
  each other. Filename or heading similarity is insufficient.
- Stage A can prove static/schema/render/trace behavior only. Stage B alone can prove runtime
  failure/reset/verify/evidence and portal publication.
- Required tools fail when missing. Only explicitly optional runtime profiles may use
  `not-run-optional`; an unresolved owner value uses `blocked-tbc`, never pass.

## Functional and Non-Functional Requirements

| ID | Requirement | Stage | Verification obligation |
|---|---|---|---|
| I11-AUTH-01 | Pin exact clean input, branch, remote/body, ancestry, dependency and lease state before each amendment/cook | A/B | Fresh preflight and authority evidence |
| I11-AUTH-02 | Keep current implementation file/command/dependency/renderer/schema authorities empty | Plan | Static authority scan |
| I11-AUTH-03 | Derive Stage A only from exact released #8; derive Stage B only from exact passing merged #10 plus #8 | A/B | Release SHA/blob/evidence verification |
| I11-CUR-01 | Vietnamese-first foundation-to-mid competency graph; reachable, acyclic, remediation-aware | A | Prerequisite/locale/coverage failures |
| I11-CUR-02 | Every module supplies prerequisite check, starter, task, controlled failure, verify, evidence, reset, hints, solution, reflection | A structure; B runtime | Schema/static then E2E lifecycle evidence |
| I11-CUR-03 | Learning product uses progressive disclosure and verification; no scroll/time/reflection/solution completion | A/B | Static contract + Stage B completion negatives |
| I11-TRACE-01 | Close business outcome → capability → concern → FR/NFR → option → views → ADR/pattern → implementation intent → evidence → operations chain | A/B | Broken/orphan/reciprocal trace fixtures |
| I11-TPL-01 | Structured templates have stable content IDs, released-contract version/hash and compatibility/supersession; cover concerns, FR/NFR/ASR, option matrix, C4, dynamic/deployment, ADR, fitness, capacity/cost, DR, security; every critical flow links ordered dynamic/sequence and deployment evidence | A | Template registry/version/supersession/required-field/critical-flow tests |
| I11-SYS-01 | Cover API/auth, network, scaling, queue/backpressure, cache, partitioning, timeout/retry/jitter, circuit breaker, bulkhead, graceful degradation, SLI/SLO, DR, capacity/cost | A | Topic-force-failure-evidence matrix |
| I11-PAT-01 | Admit a pattern only with named forces, failure, quality attribute, boundary, verifier/evidence, and removal/rejection condition | A/B | Admission mutations |
| I11-PAT-02 | Negative `pattern-without-failure` fixture fails deterministically and cannot pass with generic prose/null evidence | A | Required RED fixture |
| I11-VIEW-01 | Preserve all six Issue #6 local source/row/render semantics and blobs read-only | A/B | Exact SHA-256/blob pre/post matrix |
| I11-VIEW-02 | Add only lease-owned expansion sources/rows/renders after an exact extension seam exists | A | Closed diff/lease checks |
| I11-VIEW-03 | Deterministic SVG/text and semantic overlap/freshness checks cover every expansion | A | Two clean renders + mutation checks |
| I11-MAP-01 | Teach local DuckDB/Rill/OpenMetadata/Iceberg and AWS ClickHouse/Superset/OpenMetadata/S3/ECS-EC2 mappings as architecture content only | A | Content/wording/prohibited-call scans |
| I11-API-01 | Teach OpenAPI only for real released synchronous operations; no duplicate OpenAPI truth | A/B | Operation-matrix reciprocal links |
| I11-API-02 | AsyncAPI exists in teaching only if a real released channel exists; no broker/pattern theater | A/B | Channel inventory negative |
| I11-LAB-01 | Stage B lab consumes exact #8/#10 truth without copied schema/state/completion/renderer logic | B | Path/blob/consumer boundary inspection |
| I11-LAB-02 | Stage B covers F01→F04→J01/J04/J05 and real controlled failure→hint→reset→verify→evidence→reflection | B | `architecture-lab-e2e` evidence |
| I11-SEC-01 | Complete S3 threat/data-security disposition, negative tests, residual risks, secret/private-path controls | A/B | Threat crosswalk + scans |
| I11-EVID-01 | Emit exact-command/tool/input/output/tested-tree/dependency/contract/fixture/artifact/redaction/rollback evidence plus one closed immutable run index covering every required result and artifact hash | A/B | Released schema + digest/index completeness, duplicate/orphan/tamper validation |
| I11-ROLL-01 | Roll back only Issue #11-owned candidate/workspace state; preserve prior evidence, protected six, dependencies, and unrelated data | A/B | Rehearsal and pre/post hashes |
| I11-OPS-01 | Teach operations/resilience/security/cost/governance consequences without live cloud claims | A | Trace/content policy tests |
| I11-DOC-01 | Classify user-facing documentation and release-note impact at each staged handoff; keep `README.md`, `docs/**`, and release metadata outside Issue #11 cook authority and route required changes through a separate owner-authorized serialized handoff | A/B | Handoff impact record plus exact changed-path denial |
| I11-PREMERGE-01 | Require fresh independent implementation review and repository-authorized human exact-head pre-merge approval | A/B | External approval attestation |
| I11-SCOPE-01 | No root Makefile, docs-code-standards, release manifest, portal/shared contract, cloud/AWS/Terraform, other worktree write | Plan/A/B | Exact changed-path deny-list |

## Acceptance Command Contract

The immutable final acceptance names are:

```bash
make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check
```

They are not current command authority. A later amendment must bind each target to exact owner,
recipe path, dependency tools/versions, arguments, time/resource bounds, evidence output, and
failure behavior. Stage A may run only the amendment-authorized static subset and must mark
`architecture-lab-e2e` unavailable—not passed. Stage B must run the full line. Existing Issue #6
`architecture-check`/`architecture-render` targets remain read-only and cannot be redefined.

## TDD Failure Fixtures

Exact fixture paths remain empty until Stage A amendment. Required semantic cases are fixed:

| ID | RED case | Required failure |
|---|---|---|
| I11-RED-REF-001 | Missing/stale requirement, view, ADR, verifier, evidence, module, or reciprocal reference | Reference/trace check fails before content publication |
| I11-RED-PREQ-001 | Missing prerequisite, self-edge, cycle, unreachable required node, forged skip | Curriculum check fails; no mutation/completion |
| I11-RED-VIEW-001 | Undeclared/duplicate ID/key, no concern/audience/text, abstraction error, orphan relation | Architecture expansion check fails |
| I11-RED-ADR-001 | ADR has no forces/alternatives/consequences/test/evidence or accepts a blocker TBC | ADR check fails |
| I11-RED-PATTERN-001 | Pattern exists without concrete failure/verifier | `pattern-without-failure` failure |
| I11-RED-TRACE-001 | Business-to-operations chain has a gap, wrong-stage edge, or one-way link | Traceability check fails |
| I11-RED-RENDER-001 | Stale/nondeterministic SVG/text, semantic mutation erased, script/external URL/private path | Render check fails |
| I11-RED-READONLY-001 | Any protected Issue #6 byte/row/ID/path/semantic projection changes | Protected-hash check fails |
| I11-RED-API-001 | OpenAPI topic lacks a real operation or AsyncAPI topic lacks a real channel | Contract-teaching admission fails |
| I11-RED-S3-001 | Secret/credential/private path/cloud action/deployment claim enters content or evidence | S3 scan fails |

RED evidence must record failing assertion IDs against the exact authorized stage input before
implementation behavior changes. It may not use fake data or a test that passes before behavior.

## Requirement-to-Phase Trace

| Phase | Requirements | Exit evidence | Dependency |
|---:|---|---|---|
| 1 | I11-AUTH-01..03, I11-SCOPE-01 | Exact amendment/revalidation/readiness or blocked gate | Released #8 for A; #10 for B |
| 2 | I11-CUR-01..03, I11-TRACE-01, I11-PAT-02, I11-VIEW-01, I11-SEC-01 | RED bundle + protected pre-hash | Stage A authority |
| 3 | I11-TPL-01, I11-SYS-01, I11-PAT-01, I11-VIEW-02..03, I11-MAP-01, I11-API-01..02, I11-OPS-01 | Static/schema/render/trace results | Phase 2 RED |
| 4 | I11-EVID-01, I11-ROLL-01, I11-DOC-01, I11-PREMERGE-01 | Stage A evidence/rollback/docs-impact handoff; no runtime claims | Phases 2-3 |
| 5 | I11-AUTH-01..03, I11-LAB-01 | Exact #10 renderer/journey amendment | Passing merged #10 + Stage A |
| 6 | I11-LAB-01..02, I11-CUR-02..03, I11-SEC-01 | Full E2E failure/reset/verify/evidence | Stage B authority |
| 7 | All | Full command/evidence/rollback/docs-impact/approval bundle | Phases 1-6 |

## Risk Register

| ID | Risk | Impact | Mitigation / rollback | Clearing gate |
|---|---|---|---|---|
| I11-R-01 | #8/#10 draft/readiness SHA mistaken for release | Contract drift, duplicate truth, unsafe cook | Empty authorities; exact merged-release preflight | Stage amendment/readiness |
| I11-R-02 | Issue body’s Structurizr label overrides released LikeC4 decision | Split renderer truth, non-determinism | Treat as ownership label; use exact lease/toolchain or explicit migration authority | View-lease amendment |
| I11-R-03 | Existing six-view checker has no expansion seam | Protected code edit or unverified expansion | Require exact additions-only seam; STOP if absent | Stage A readiness |
| I11-R-04 | Markdown/topic dump masquerades as curriculum | Passive learning, unverifiable outcomes | Module loop, competency graph, templates, Stage B real lab | Curriculum checks/UAT |
| I11-R-05 | Pattern catalogue becomes technology theater | Wrong design heuristics and needless services | Force/failure/evidence predicate + negative fixture | Pattern fitness |
| I11-R-06 | Static Stage A implies portal/lab completion | False learner/release trust | Explicit non-runtime stage claim; no completion/evidence mutation | Stage A handoff |
| I11-R-07 | Curriculum duplicates #8 contract/state/evidence | Conflicting authorities and migration failure | Consume exact released validators/registries read-only | Contract boundary inspection |
| I11-R-08 | Lab duplicates #10 renderer/portal logic | Portal overlap and drift | Content-only released seam; STOP if portal change needed | Stage B amendment |
| I11-R-09 | Expansion overwrites local view IDs/rows/renders | Breaks released learning/portal assets | Protected hash/blob and semantic-overlap tests | Every render/release |
| I11-R-10 | Render appears stable while semantic meaning changes | Misleading architecture evidence | Computed semantic projection + mutation tests + text hash | Render gate |
| I11-R-11 | AWS mapping is interpreted as deployed or zero-cost | Security/cost/operations misinformation | Content-only labels; TBC/apply blockers; prohibited-call scan | Static policy check |
| I11-R-12 | Generic NFR/ADR/pattern passes without measurable oracle | Traceability theater | Threshold/owner-TBC and verifier requirements | Template/trace checks |
| I11-R-13 | Reset/cleanup deletes evidence or unrelated state | Irrecoverable audit/user loss | Marker-scoped cleanup; evidence immutable; protected pre/post hashes | Rollback rehearsal |
| I11-R-14 | Content/render/evidence carries secrets/private paths | Disclosure | Allow-listed fields; high-confidence S3 scans; fail, do not redact into pass | S3 gate |
| I11-R-15 | Required tool missing is silently skipped | False release | Missing required tool = fail; no renderer fallback | Command contract |
| I11-R-16 | Human approval is inferred from automation | Unapproved high-risk merge | Separate external exact-head approval and implementation review | Pre-merge |

## Hard STOP Conditions

- Dirty/wrong base, local/tracking/fresh-live mismatch, missing ancestry, or active conflicting lease.
- Missing exact released dependency, blob/hash/version mismatch, or unapproved fallback.
- Empty stage allow-list/command list at cook, or any path/command outside the closed amendment.
- Protected view/tool/portal/shared-contract/root path drift.
- Any TDD RED fixture does not fail for the intended reason before implementation.
- Missing required tool/test, nondeterministic render, trace gap, S3 regression, or unbounded evidence.
- Stage A claims runtime/portal/completion; Stage B lacks real reset/verify/evidence.
- Cleanup/rollback cannot preserve evidence and unrelated state.
- PR/merge/cloud/AWS/Terraform action lacks separate explicit authority.
- Independent revalidation/readiness or human exact-head approval is absent.

## Unresolved Questions

None. Dependency-produced exact values remain intentionally unavailable and are not planning gaps.
