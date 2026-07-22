# Stage A v4 Post-Review Amendment

## Decision

This is the plan author's corrected proposal. It is **ready only for fresh independent plan
validation**. It is not a readiness result, cook authority, implementation approval, or release
claim. The eight findings in
[PR #30 review 5050486239](https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239)
are corrected under the exact recovery authority in
[Issue #11 comment 5050513064](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064).

Historical v1/v2/v3 validation, readiness, product, tests, renders, and evidence stay immutable at
their old SHAs and have no v4 authority. In particular, `c07c9a080be7be88447aac497bdf0a2b5fddd020`
is forbidden as an input. No failed branch, PR, feature worktree, or evidence bundle may be
cherry-picked, copied, or relabelled.

## Eight-Finding Correction Map

| Finding | Corrected contract |
|---|---|
| `RC-01` | [Integration derivation and byte equality](#integration-derivation-and-byte-equality) |
| `RC-02` | [Repository-level scaffold-first TDD](#repository-level-scaffold-first-tdd) |
| `RC-03` | [Exact command allowlist](#exact-command-allowlist) |
| `RC-04` | [Closed template lifecycle](#closed-template-lifecycle) |
| `RC-05` | [Visible render parity](#visible-render-parity) |
| `RC-06` | [Twenty-module lifecycle](#twenty-module-lifecycle) |
| `RC-07` | [Critical flows and governance bridge](#critical-flows-and-governance-bridge) |
| `RC-08` | [Evidence truth and cleanup](#evidence-truth-and-cleanup) |

## Integration Derivation and Byte Equality

Exact integration release and tree:

```text
commit 5644f01b4c0443a81f3af0bcce80f44c847cd986
tree   a38594d420fe7df2b30265a8a72bb5fad1698012
```

The v4 plan branch is a direct descendant of that integration commit. The author correction,
future independent validation, and future readiness commits may change only
`plans/260721-011-architecture-curriculum/**`. The exact pushed readiness head, if one later
passes, becomes `cookInput`. These sets are disjoint and closed:

| Range | Required diff |
|---|---|
| `5644f01b… -> cookInput` | Plan-provenance paths only; every path is under this plan directory |
| `cookInput -> candidate` | Exactly the 50 create-only paths below; no plan change |
| `5644f01b… -> candidate` | Plan-provenance paths union the exact 50 create-only paths; no third set |

At author, validation, readiness, cook preflight, C1, C2, each semantic commit, final candidate,
rollback, and reviewer checkout:

1. prove integration is an ancestor and record commit/tree/parent identities;
2. compare local HEAD, upstream tracking ref, a newly fetched remote ref, and the live GitHub ref;
3. parse `git diff --name-status` and reject paths outside the applicable closed set;
4. prove all 50 product/test paths absent at `cookInput` and create-only thereafter;
5. recompute all 33 protected identities and all 21 released-contract identities from Git blobs
   and working-tree bytes, with exact per-path equality to integration;
6. prove the direct integration-to-cook diff is plan-only and that stripping the exact 50 paths
   from a candidate tree leaves the same non-plan bytes as integration; and
7. prove failed v1/v2/v3 product/test/evidence commits are neither ancestors nor byte sources.

No merge, no-ff reconciliation, rebase during cook, history synthesis, undocumented conflict
resolution, `c07c9a0…`, or failed-feature cherry-pick/copy may replace this derivation.

## Released Read-Only Boundaries

The released `learning/contracts/learning-contract-set-v1.json` closes exactly 21 read-only
contract/content identities. The protected architecture inventory closes exactly 33 identities:
25 Issue #6 source/manifest/render rows and eight tool/lock/package identities. Their exact
path/blob/content-hash inventories are in
[Verification, Evidence, and Protected Assets](./verification-evidence-and-protected-assets.md#protected-identities).
Every item must remain byte-identical. `contracts/**`, `learning/contracts/**`, OpenAPI,
`scripts/learning_contracts/**`, protected local C4, protected renders, root `Makefile`,
`release-manifest.json`, README/docs, portal, runner, Vite, cloud, AWS, and Terraform are outside
the write set.

Stage A may read the released OpenAPI operation matrix, golden Python lock, command admission,
contract version registry, promotion schema, and architecture tool lock. It emits no learner
evidence, progress, completion, runtime result, hosted/deployed result, or `fitness-result-v2`.
The static promotion object remains exactly:

```json
{
  "decision": "insufficient-evidence",
  "reason": "no-common-grain"
}
```

## Exact Stage A Tracked Write Allowlist

Exactly 50 paths may be created. There are no modifies and no deletes.

```text
architecture/expansions/i5-06/likec4/model/architecture-curriculum.c4
architecture/expansions/i5-06/likec4/specification.c4
architecture/expansions/i5-06/likec4/view-manifest.yaml
architecture/expansions/i5-06/likec4/views/C4-L2-AWS.c4
architecture/expansions/i5-06/likec4/views/DEP-AWS.c4
architecture/expansions/i5-06/likec4/views/DYN-OFFICE.c4
architecture/expansions/i5-06/likec4/views/DYN-PUBLISH.c4
architecture/expansions/i5-06/likec4/views/DYN-RESTORE.c4
architecture/expansions/i5-06/rendered/C4-L2-AWS.svg
architecture/expansions/i5-06/rendered/C4-L2-AWS.txt
architecture/expansions/i5-06/rendered/DEP-AWS.svg
architecture/expansions/i5-06/rendered/DEP-AWS.txt
architecture/expansions/i5-06/rendered/DYN-OFFICE.svg
architecture/expansions/i5-06/rendered/DYN-OFFICE.txt
architecture/expansions/i5-06/rendered/DYN-PUBLISH.svg
architecture/expansions/i5-06/rendered/DYN-PUBLISH.txt
architecture/expansions/i5-06/rendered/DYN-RESTORE.svg
architecture/expansions/i5-06/rendered/DYN-RESTORE.txt
architecture/expansions/i5-06/rendered/render-manifest.json
learning/curriculum/architecture-curriculum-v1.json
learning/curriculum/command-owner-activation-i5-06-stage-a-v1.json
learning/curriculum/release-binding-i5-06-stage-a-v1.json
learning/curriculum/assessments/architecture-assessment-v1.json
learning/curriculum/contracts/architecture-curriculum-v1.schema.json
learning/curriculum/contracts/architecture-module-collection-v1.schema.json
learning/curriculum/contracts/architecture-release-binding-v1.schema.json
learning/curriculum/contracts/architecture-template-registry-v1.schema.json
learning/curriculum/contracts/architecture-trace-v1.schema.json
learning/curriculum/contracts/architecture-view-extension-v1.schema.json
learning/curriculum/examples/promotion-publication-architecture-v1.json
learning/curriculum/mappings/local-aws-conceptual-v1.json
learning/curriculum/modules/data-v1.json
learning/curriculum/modules/foundation-v1.json
learning/curriculum/modules/junior-v1.json
learning/curriculum/modules/mid-v1.json
learning/curriculum/patterns/system-design-patterns-v1.json
learning/curriculum/templates/architecture-templates-v1.json
learning/curriculum/tools/__init__.py
learning/curriculum/tools/architecture-render.mjs
learning/curriculum/tools/architecture_expansion.py
learning/curriculum/tools/check_curriculum.py
learning/curriculum/tools/check_traceability.py
learning/curriculum/tools/content_io.py
learning/curriculum/traces/architecture-trace-v1.json
mk/issue-5/i5-06.mk
tests/fixtures/learning/curriculum/invalid-cases-v1.json
tests/learning/curriculum/test_architecture_expansion.py
tests/learning/curriculum/test_curriculum_contract.py
tests/learning/curriculum/test_security_and_bounds.py
tests/learning/curriculum/test_traceability.py
```

The list is literal, not glob authority. Runtime, evidence, fitted inspection HTML, raw DOT/SVG,
caches, package roots, and logs are owned untracked state and never become additional product
paths.

## Exact Command Allowlist

The reviewer/cook controller first allocates a private mode-0700 parent and candidate directory,
sets `umask 077`, exports the single candidate-root variable `I11_RUNTIME`, fixes the clean
checkout as cwd, admits a closed environment, rejects caller overrides of root/interpreter/PATH,
and computes `I11_RUNTIME_SHA256` from exactly `$I11_RUNTIME/venv/bin/python`. Because the released
runtime requires a candidate direct child of its root, every public Make call uses
`LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.."` and
`LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME"`. This controller admission is a prerequisite protocol,
not an extra operator command shape.

The machine-parsed allowlist contains exactly these 16 unique nonblank top-level command shapes,
in this order and literally with the same runtime shape:

```text
make help
python3.12 -m venv "$I11_RUNTIME/venv"
"$I11_RUNTIME/venv/bin/python" -m pip install --disable-pip-version-check --no-input --require-hashes --only-binary=:all: --no-deps -r requirements/golden-py312-macos-arm64.lock
"$I11_RUNTIME/venv/bin/python" -m pip check
make learning-runtime-admit LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make learning-contracts-check LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make lesson-check LESSON=promotion-trust LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make api-contracts-check LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
"$I11_RUNTIME/venv/bin/python" -m learning.curriculum.tools.architecture_expansion run-focused-tests
"$I11_RUNTIME/venv/bin/python" -m learning.curriculum.tools.architecture_expansion verify-expansions
make curriculum-check LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make traceability-check LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make architecture-check LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
make architecture-render LEARNING_RUNTIME_ROOT="$I11_RUNTIME/.." LEARNING_RUNTIME_CANDIDATE="$I11_RUNTIME" LEARNING_RUNTIME_INTERPRETER_SHA256="$I11_RUNTIME_SHA256"
git diff --check
"$I11_RUNTIME/venv/bin/python" -m learning.curriculum.tools.architecture_expansion clean-handoff
```

The private controllers launch only fixed argv from code, each child in its own session/process
group, using admitted executable hashes. They do not accept shell text or caller executable names.
Network opens only for the exact hash/lock-verified Python and Node bootstrap and closes before
checks/renders. Missing or alternate tools fail; mocks, fallback renderers, native Graphviz,
browser substitutes, undocumented layout correction, and skipped commands are forbidden. A
future independent reviewer repeats the exact 16 shapes in a fresh detached checkout of the exact
tested pushed head with matching tree, fixture, source, and tool hashes.

## Repository-Level Scaffold-First TDD

Scaffold-first ordering exists only because callable public paths do not exist at integration.
The audited chronology is fixed:

1. `C1` creates exactly seven generic callable paths: `mk/issue-5/i5-06.mk`, the five Python files
   under `learning/curriculum/tools/`, and `architecture-render.mjs`. It may contain strict generic
   repository traversal, bounded parsing, process ownership, locked-tool invocation, render
   plumbing, CLI/Make routing, evidence indexing, and cleanup ownership, but none of the 82 target
   codes or Issue #11 semantic constants.
2. Direct-child `C2` creates exactly the four test files and one fixture file. Their bytes remain
   unchanged through the first semantic GREEN.
3. At C2, complete controls and mutations execute through real repositories and reach production
   `check_repository()`, `_verify_repository()`, `_toolchain_verification()`, and
   `_repository_handoff()`, plus the matching public Python CLI and Make commands.
4. Contemporaneous RED is the absence of each named semantic rule after all file/import/tool/path
   preconditions pass. Only after the closed RED bundle exists may C3+ add semantic rules and the
   remaining 38 paths.

For every one of the 22 families and all 82 exact codes, tests create a reviewer/agent-owned
mode-0700 temporary repository copy or bounded fixture Git repository containing all real required
files, registries, sources, renders, manifests, evidence roots, and Git state. A valid control is a
complete repository that passes the full production stack at GREEN. Each mutation changes exactly
the real state named by its code and must return that exact code through both the callable and its
public CLI/Make route.

Required real mutations include file bytes/types/modes, JSON schema/registry/instance rows,
prerequisite and trace references, LikeC4 relation source/target/label/technology/order, deployment
topology and reciprocal bridge links, raw Graphviz output, SVG/HTML/text visible semantics,
subprocess descendants/RSS/output/files/TERM handling, raw/sanitized evidence, index closure, and
actual initialized-Git tracked/untracked/ignored/dirty porcelain. Resource helpers really spawn
descendants, ignore TERM, allocate memory, flood output, and create files. Cleanup parses bytes
from a real Git subprocess; it never accepts injected porcelain.

The fixture `expectedCode` is test assertion metadata. The harness removes it, IDs, and assertion
text before copying state or calling production code. Forbidden behavior oracles include
`rssExceeded`, `supersessionValid`, `overlap`, `porcelainBytes`, or any other abstract Boolean or
dictionary predicate; expected-code echo/fallback; fixture-ID dispatch; hardcoded pass/fail;
predicate-only checking; mocks; monkeypatches; skips; missing-tool/import/path failures; and
test-only implementations. Each run retains exact source/tree/fixture/tool hashes.

### Closed 22-Family / 82-Code Catalogue

| RED family | Exact codes |
|---|---|
| `I11-RED-REF-001` | `I11_REF_MISSING`, `I11_REF_STALE`, `I11_REF_NONRECIPROCAL` |
| `I11-RED-PREQ-001` | `I11_PREQ_UNKNOWN`, `I11_PREQ_SELF`, `I11_PREQ_CYCLE`, `I11_PREQ_UNREACHABLE`, `I11_PREQ_FORGED_SKIP` |
| `I11-RED-VIEW-001` | `I11_VIEW_DUPLICATE`, `I11_VIEW_DECORATIVE`, `I11_VIEW_CONCERN_MISSING`, `I11_VIEW_ABSTRACTION_MIXED` |
| `I11-RED-ADR-001` | `I11_ADR_INCOMPLETE` |
| `I11-RED-PATTERN-001` | `I11_PATTERN_FAILURE_MISSING`, `I11_PATTERN_VERIFIER_MISSING` |
| `I11-RED-TRACE-001` | `I11_TRACE_GAP`, `I11_TRACE_NONRECIPROCAL` |
| `I11-RED-RENDER-001` | `I11_RENDER_STALE`, `I11_RENDER_NONDETERMINISTIC`, `I11_RENDER_UNSAFE`, `I11_RENDER_SEMANTIC_ERASURE` |
| `I11-RED-READONLY-001` | `I11_PROTECTED_IDENTITY_DRIFT` |
| `I11-RED-API-001` | `I11_API_OPERATION_UNRELEASED`, `I11_ASYNC_CHANNEL_UNRELEASED` |
| `I11-RED-S3-001` | `I11_S3_SECRET`, `I11_S3_PRIVATE_PATH`, `I11_S3_EXTERNAL_URL`, `I11_S3_CLOUD_ACTION` |
| `I11-RED-TEMPLATE-001` | `I11_TEMPLATE_SCHEMA_TOKEN_INVALID`, `I11_TEMPLATE_COMPATIBILITY_INVALID`, `I11_TEMPLATE_UNREGISTERED`, `I11_TEMPLATE_HASH_DRIFT`, `I11_TEMPLATE_NONRECIPROCAL`, `I11_TEMPLATE_SUPERSESSION_INVALID`, `I11_TEMPLATE_REMOVAL_INVALID` |
| `I11-RED-CRITICAL-FLOW-001` | `I11_CRITICAL_FLOW_COVERAGE_MISSING`, `I11_CRITICAL_FLOW_GENERIC_STEPS` |
| `I11-RED-ASSESSMENT-001` | `I11_STAGE_BOUNDARY_RUNTIME_FORGERY` |
| `I11-RED-BOUND-001` | `I11_BOUND_SIZE`, `I11_BOUND_DEPTH`, `I11_BOUND_DUPLICATE_KEY`, `I11_BOUND_SPECIAL_FILE` |
| `I11-RED-EVIDENCE-001` | `I11_EVIDENCE_MISSING`, `I11_EVIDENCE_DUPLICATE`, `I11_EVIDENCE_ORPHAN`, `I11_EVIDENCE_STALE`, `I11_EVIDENCE_TAMPERED`, `I11_EVIDENCE_PRIVACY` |
| `I11-RED-PROMOTION-001` | `I11_PROMOTION_DECISION_DRIFT`, `I11_PROMOTION_REASON_DRIFT` |
| `I11-RED-BRIDGE-001` | `I11_BRIDGE_MISSING`, `I11_BRIDGE_DIVERGENCE_MISSING`, `I11_BRIDGE_RUNTIME_CLAIM` |
| `I11-RED-RESOURCE-001` | `I11_RESOURCE_DEADLINE`, `I11_RESOURCE_RSS`, `I11_RESOURCE_PROCESS_COUNT`, `I11_RESOURCE_OUTPUT`, `I11_RESOURCE_FILE_COUNT`, `I11_RESOURCE_FILE_BYTES`, `I11_RESOURCE_OWNERSHIP`, `I11_RESOURCE_TERM`, `I11_RESOURCE_KILL`, `I11_RESOURCE_REAP`, `I11_RESOURCE_MEASUREMENT_MISSING` |
| `I11-RED-VISUAL-001` | `I11_VISUAL_LANGUAGE`, `I11_VISUAL_NUMBERING`, `I11_VISUAL_FIT_FONT`, `I11_VISUAL_ASPECT`, `I11_VISUAL_CANVAS`, `I11_VISUAL_OVERLAP`, `I11_VISUAL_CLIPPING`, `I11_VISUAL_CONTRAST`, `I11_VISUAL_ACCESSIBILITY`, `I11_VISUAL_TEXT_PARITY`, `I11_VISUAL_HUMAN_REVIEW_MISSING` |
| `I11-RED-CLEANUP-001` | `I11_CLEAN_NONIGNORED_DIRTY`, `I11_CLEAN_IGNORED_UNOWNED`, `I11_CLEAN_PORCELAIN_NONEMPTY`, `I11_CLEAN_OWNERSHIP_DRIFT`, `I11_CLEAN_ROLLBACK_SCOPE` |
| `I11-RED-RELATION-ORDER-001` | `I11_RELATION_ORDER_MISMATCH` |
| `I11-RED-TOPOLOGY-001` | `I11_TOPOLOGY_BINDING_MISMATCH` |

Module lifecycle missing fields use `I11_REF_MISSING`; a duplicate canonical learning signature
uses `I11_REF_STALE`; a one-way lifecycle/trace binding uses `I11_REF_NONRECIPROCAL`; and a level
or progression regression uses `I11_PREQ_FORGED_SKIP`. These are real repository mutations under
the existing catalogue, not new families or codes.

## Twenty-Module Lifecycle

Exactly these 20 distinct IDs and prerequisite vectors are admitted:

```text
F01:[] F02:[F01] F03:[F02] F04:[F03]
J01:[F03,F04] J02:[F04] J03:[J02] J04:[J03] J05:[J03,J04] J06:[J03]
D01:[F03] D02:[D01] D03:[D02,J04] D04:[D02] D05:[D02,D03,D04] D06:[D05]
M01:[J02,J03,J04,J05,J06,D05] M02:[M01,J04] M03:[D04,D05,M01] M04:[J05,M01]
```

Every module schema requires nonempty, correctly typed, module-specific `starter`, `task`,
`controlledFailure`, `verify`, `evidence`, `reset`, ordered progressive `hints`, a `solution` with
an explicit reveal gate, `tradeOffReflection`, and `operationsConsequence`. Consequences cover
operations, resilience, security, cost, and governance. Each object has stable reciprocal trace
IDs and `executionStatus=not-executed-static-only`. Solutions never set progress or completion.

The validator computes a canonical learning signature over outcome, capability, concern, task
artifact, controlled failure, required views, verifier, evidence, trade-off, and operations
consequence. All 20 signatures and the normalized task/failure/reflection/consequence bodies must
be distinct. Boilerplate, renamed clones, duplicate meaningful content, empty fields, count-only
content, or one generic lifecycle repeated 20 times fails. Foundation modules are guided; junior
modules require bounded choice among viable options; data modules connect authority/grain/quality;
mid modules challenge failure, operability, security, cost, recovery, or governance forces. The
fixed graph must remain acyclic, reachable, and progressively harder.

## Closed Template Lifecycle

The sole registry `architecture-templates-v1.json` has exact schema token
`i5-06-architecture-template-registry-v1`, registry ID
`i5-06-architecture-template-registry`, registry version `1.0.0`, and exactly this closed set:

| Template ID | v1 version | Required compatibility purpose |
|---|---|---|
| `tpl-stakeholder-concern` | `1.0.0` | actor/decision/outcome/concern |
| `tpl-fr-nfr-asr` | `1.0.0` | measurable owned requirement |
| `tpl-option-matrix` | `1.0.0` | forces/options/failures/trade-offs |
| `tpl-c4-view` | `1.0.0` | concern-driven view and text alternative |
| `tpl-dynamic-sequence` | `1.0.0` | ordered critical flow |
| `tpl-deployment` | `1.0.0` | topology/state/trust/recovery |
| `tpl-adr` | `1.0.0` | alternatives/consequences/evidence |
| `tpl-pattern-admission` | `1.0.0` | force/failure/verifier/removal |
| `tpl-fitness-function` | `1.0.0` | deterministic oracle/evidence boundary |
| `tpl-capacity-cost` | `1.0.0` | assumptions/units/sensitivity/residual cost |
| `tpl-dr-recovery` | `1.0.0` | authority/restore/RTO/RPO/rollback |
| `tpl-security-review` | `1.0.0` | assets/threats/controls/residual risk |

For every row, the cook computes `contentSha256` from the canonical hash-excluded template body
and writes that exact hash into the registry and every instance binding. Repository discovery must
equal the 12-ID registry set exactly once; all v1 rows are active, have `supersedes=null`, declare
the closed schema and compatibility object, and list sorted unique consuming instance IDs. Every
instance reciprocally declares a stable unique `instanceId`, exact `registryId`, `templateId`,
`version`, `contentSha256`, and the exact registry-row `compatibility` object. Repository
discovery by `instanceId` must equal every row's sorted `consumingInstanceIds` set with no
duplicate, unbound, or multiply bound instance.

Future successors must increase semantic version monotonically and contain a `supersedes` object
with the predecessor's exact ID/version/hash, reader compatibility, migration proof, and rollback
proof. A referenced predecessor stays registered/readable as deprecated. Removal requires zero
instances, a registered compatible replacement, completed migration/rollback evidence, and a
later release tombstone. Unknown copies, 11/13 rows, duplicates, unregistered versions, hash drift,
invalid supersedes objects, unknown predecessors, removals without tombstones, and orphan/one-way
instances are rejected through real repository fixtures using the seven existing template codes.
The fixtures also independently duplicate or change `instanceId` and drift the instance
compatibility object while leaving the registry row canonical; those mutations must fail
`I11_TEMPLATE_NONRECIPROCAL` and `I11_TEMPLATE_COMPATIBILITY_INVALID`, respectively.

## Critical Flows and Governance Bridge

The trace closes exactly 11 distinct ordered flow IDs:

```text
CF-LEARNER-FIRST-JOURNEY
CF-PUBLISH-STAGE-COMMIT
CF-PUBLISH-RETRY-RESUME
CF-CATALOG-INGEST-HANDOFF
CF-OFFICE-OPEN
CF-OFFICE-READINESS
CF-OFFICE-CLOSE
CF-RESTORE-OBJECT-CATALOG
CF-RESTORE-ANALYTICS
CF-RESTORE-GOVERNANCE
CF-RESTORE-EVIDENCE
```

Every step binds an exact canonical dynamic relation identity `(viewId, ordinal, sourceId,
targetId, label, technology)` and an exact deployment topology identity. The eight conceptual-only
bridges are `BR-ANALYTICS-01`, `BR-BI-01`, `BR-GOVERNANCE-01`, `BR-LAKE-01`, `BR-COMPUTE-01`,
`BR-STATE-01`, `BR-SECURITY-01`, and `BR-COST-01`; none proves runtime, deployment, readiness,
security, RTO/RPO, or cost.

`BR-GOVERNANCE-01` binds the actual protected local model relation
`learning.adapters -> retail` and exact local deployment path
`local.developer_host.adapters_instance -> local.developer_host.retail_instance`. It also binds
the exact `DYN-PUBLISH` physical/logical ingestion relation identities and the `DEP-AWS`
OpenMetadata compute/database/search topology. The bridge, every bound relation, and every
deployment path reciprocally list each other. It preserves the honest `retail_iceberg` physical
and `retail_duckdb` logical catalog views and does not invent cross-service lineage.

Real fixtures independently replace `adapters_instance`, change a dynamic endpoint/order while
deployment remains canonical, change deployment topology while the relation remains canonical,
remove either reciprocal reference, and change both sides to the same wrong identity. The first
four fail nonreciprocity/relation-order/topology codes; changing both still fails the protected
canonical-source identity. No Boolean `overlap` or nominal bridge record can satisfy the rule.

## Visible Render Parity

For each of the five expansion views—`C4-L2-AWS`, `DEP-AWS`, `DYN-OFFICE`, `DYN-PUBLISH`, and
`DYN-RESTORE`—locked LikeC4 `export json --skip-layout --pretty` and `gen dot` form the sole
semantic authority. Locked WASM Graphviz renders that DOT. The published SVG is only a
deterministic safety/accessibility normalization of the actual Graphviz SVG; structured text and
evidence-only script-free fitted HTML derive from the same semantics-preserving parsed
LikeC4/DOT/SVG representation. Hard-coded Python node/relation cards, parallel trace literals,
manual edges, undocumented layout correction, and hidden hash-only semantics are forbidden.

The checker compares source, manifest, parsed projection, DOT, visible SVG DOM, fitted HTML, and
text. Visible nodes, boundaries, relations, endpoints, labels, technologies, dynamic ordinals,
and ordering must match exactly. A real source mutation to any relation source, target, label,
technology, or ordinal reruns the locked pipeline and must visibly change the corresponding SVG
edge/label/ordinal, fitted HTML, and text, with corresponding hashes. A projection/freshness hash
change that leaves visible markup/text unchanged fails `I11_RENDER_SEMANTIC_ERASURE`.

Two isolated runs must have identical projection, DOT, SVG, text, manifest, and fitted-HTML
hashes. All five views pass Vietnamese-first titles and primary labels, one numbering authority,
text alternatives, safe SVG/HTML, exact semantic parity, WCAG contrast, no overlap/clipping/off-
canvas content, and useful concern/audience coverage at fitted 1440 and 1024 CSS-pixel widths.
Evidence-only HTML is retained for inspection and is not a 51st tracked path.

## Resource and S3 Bounds

- Focused tests: one owned process group, 120 seconds.
- Whole locked tool bootstrap, two isolated renders, and validation: one 180-second parent
  deadline, sequential children, maximum 16 live group processes, aggregate RSS 1.5 GiB.
- Combined stdout/stderr: 1 MiB per command, exact raw bytes retained within that bound; human log
  excerpt at most 16 KiB.
- Each isolated tool root: 1 GiB; both roots plus staging: 2.5 GiB; staging: 4096 files; final
  rendered set: 2 MiB.
- On timeout or breach: signal only the owned PGID, TERM, wait 5 seconds, KILL remaining members,
  wait/reap leader, and prove zero descendants. Retain PID/PGID, samples, peak RSS, process/file/
  byte counts, output hashes, TERM/KILL/wait results, and failure code.
- Reject secrets, credentials, tokens, environment dumps, absolute/private paths, external/local
  URLs, account/resource IDs, unsafe SVG/HTML, scripts, event handlers, `foreignObject`, data URLs,
  symlinks/special files, cloud actions, Terraform/provider actions, deployment claims, and missing
  tools or measurements.

## Evidence Truth and Cleanup

The primary retained root is `.claude/evidence/issue-11-stage-a/{run-id}/`, with root/run mode 0700
and regular files 0600, or an independently allocated external root with the same symbolic owner
contract. `owner.json` records issue, run, repository identity hash, input/C1/C2/RED/semantic/final
SHAs, owner nonce, role, and privacy class without a private locator. `index.json` is a closed
relative path/media type/byte count/mode/type/SHA-256 inventory; `index.sha256` hashes the index.
Closure rejects missing, duplicate, orphan, stale, extra, linked, executable, or wrong-mode bytes.

For every RED mutation, retain contemporaneously and without reconstruction:

- metadata-stripped fixture/repository mutation bytes and exact source/tree/fixture/tool hashes;
- bounded byte-exact raw stdout and raw stderr plus their hashes;
- exact production result record and public CLI/Make result;
- a separate sanitized human-readable log with source hashes and redaction summary;
- resource/process records, render projection/DOT/raw-SVG/normalized-SVG/text/fitted-HTML records,
  S3 result, owner markers, privacy scan, and cleanup/rollback result.

Passing evidence never deletes raw bytes and then claims them by hash. Raw files are private,
indexed, scanned, and retained. If S3/privacy scanning detects unsafe content, the run fails and
the bounded raw bytes remain quarantined under private ownership for incident review; they are not
misreported as passing evidence. A missing-raw/hash-only mutation fails `I11_EVIDENCE_MISSING`.

The cook-authored visual record says `reviewClass=cook-self-inspection`, names the cook/author
role, sets `independent=false`, and reports `synthesized=true` whenever an agent or automation
authored it. It never says fresh-independent and never writes `synthesized=false` unless a real
human performed that record. A later independent reviewer creates a separate immutable exact-head
bundle with `reviewClass=independent`; the cook bundle is never overwritten and cannot satisfy the
future gate.

Temporary package/cache roots are removed only after marker/path/device/inode/manifest checks;
retained raw evidence and fitted HTML are never cleanup targets. Nonignored cleanliness requires a
real `git status --porcelain=v1 --untracked-files=all` exit 0 with zero stdout bytes. The ignored-
inclusive NUL scan classifies every byte as pre-existing unchanged or within the exact owned
retained root. Any new unowned ignored byte fails. Rollback removes only verified Issue #11
temporary state and the exact 50 creates, preserves plan provenance and evidence, and re-proves
33/33 protected and 21/21 released identities.

## Hard Stops and Next Gate

Stop if lineage, remote equality, counts, paths, runtime shape, tools, repository RED, template
closure, module uniqueness, bridge reciprocity, visible parity, resource bounds, evidence truth,
S3, protected/released identities, or Stage B block differs. Stop on product/test edits during
this plan correction, cloud/container/AWS/Terraform action, merge, approval, feature-worktree
write, or any attempt to inherit failed evidence.

After this author correction is pushed and local/upstream/live equality is proven, the only next
phase is fresh independent plan validation. A later separate readiness audit is required before
any cook. Stage B remains blocked with empty authority until a passing merged Issue #10 journey.
