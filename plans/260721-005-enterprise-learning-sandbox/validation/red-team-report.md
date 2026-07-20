# Independent Adversarial Plan Red-Team Report

## Verdict

**PASS_AFTER_FIXES** for progression to the separate plan/readiness audit. The immutable input had
five Critical and ten High planning failures after deduplication. All accepted findings received
bounded planning fixes inside this issue plan directory. No finding required replacing the
business outcome, local-first architecture, preserved data spine, or staged AWS/AI boundary.

This verdict is not `ready to cook`. It is not a readiness/plan-to-cook audit and does not attest
that future commands, product files, Terraform modules, cloud resources, or AI components exist.

## Identity and Immutable Inputs

| Item | Value / result |
|---|---|
| Phase identity | Independent adversarial plan red-team; distinct from discovery, planner and initial validator |
| Red-team input | `5962316b8113ece592a26fe6211a97ae77eb70fb` |
| Golden main | `3cd3d41f71582774e8d9656a51d1044035f4503c` |
| Discovery | `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430` |
| Branch | `plan/issue-5-enterprise-learning-sandbox` |
| Pre-edit local/tracking/remote | All exactly `5962316b8113ece592a26fe6211a97ae77eb70fb`; worktree clean |
| Tree ancestry | Golden and discovery SHAs are ancestors; reviewed golden tree equality retained |
| Runtime request | Codex `gpt-5.6-sol`, reasoning `xhigh`, as requested by the launcher; model identity is not exposed as a repository command |

The output SHA is the commit that contains this report and therefore cannot be embedded in the
same tracked commit without creating a recursive SHA. It is published in the issue comment and
final phase response together with the exact input SHA.

## Adversarial Method

The red team read the complete GitHub issue and comment history, every discovery/plan/validation
artifact in this package, project documentation, current Make/Compose/runtime entrypoints, the
four first-journey marts, Rill/dbt/lineage assets, Iceberg publication, OpenMetadata ingestion and
verification, and Terraform/AWS/AI plans. Four independent hostile reviews were run:

1. security and privilege-boundary abuse;
2. state, failure, concurrency and recovery destruction;
3. architecture/data/AWS assumption destruction;
4. novice learning and delivery/scope skepticism.

Findings were replayed against repository evidence, deduplicated, adjudicated, and capped at 15.
For mutable external facts, the review used current primary sources. HashiCorp documents that
Terraform mock providers generate fake values and apply only to `terraform test`, so a mocked test
is not real provider/deployment evidence
([Terraform test mocks](https://developer.hashicorp.com/terraform/language/tests/mocking)). AWS
documents that managed ECS capacity can launch from zero with two instances and that managed
scale-in behavior is alarm/time-window driven, so an office schedule is not instantaneous
scale-to-zero truth
([ECS capacity providers](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/asg-capacity-providers.html),
[ECS cluster auto scaling](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/cluster-auto-scaling.html)).
AWS Price List APIs expose region/effective price-list data; the plan must bind price dimensions
and freshness instead of treating a prose estimate as current
([AWS Price List API](https://docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_pricing_ListPriceLists.html)).

## Adjudicated Findings

| ID | Severity | Primary perspective | Boundary |
|---|---|---|---|
| RT-01 | Critical | Security engineer | Blocks local cook |
| RT-02 | High | Security engineer | Blocks local cook |
| RT-03 | High | SRE/recovery + delivery | Blocks local cook |
| RT-04 | Critical | Lakehouse/governance + SRE | Blocks local cook |
| RT-05 | High | Data/product learner | Blocks local cook |
| RT-06 | High | Security/evidence | Blocks local cook |
| RT-07 | Critical | Learning product + delivery skeptic | Blocks local cook |
| RT-08 | High | Enterprise architect + delivery skeptic | Blocks local cook |
| RT-09 | High | Delivery/SRE | Blocks local cook; full measurement/provenance parts block local release |
| RT-10 | High | Enterprise architect + novice learner | Blocks local cook for API/prerequisites; architecture-lab part blocks later release |
| RT-11 | Critical | AWS/data architect | AWS only |
| RT-12 | High | AWS operator/recovery | AWS only |
| RT-13 | High | FinOps/SRE | AWS only |
| RT-14 | Critical | AWS security/operator | AWS only |
| RT-15 | High | AI governance skeptic | AI only |

### RT-01 — An allow-listed interpreter was still privileged RCE

- **Pre-fix location:** `phase-04-privileged-local-lab-runner-and-security-boundary.md` →
  Requirements, Architecture, Test Scenario Matrix; `lesson-lab-contract.md` → Runner Command
  Contract.
- **Repository evidence:** the current delegate inherits the process environment and executes
  child processes with repository/workspace cwd (`orchestration/airflow/callables/pipeline.py:23-31`);
  the current Airflow container mounts the entire repository read-write
  (`docker-compose.yml:35-41`).
- **Failure scenario:** a registry entry invokes Python/dbt against a learner-writable cwd. A
  malicious module, plugin, startup hook, macro, config, or path swap executes even though argv is
  typed and `shell=False`; descendants outlive timeout or stdout leaks a token/path.
- **Why it matters:** the browser-triggered runner crosses the highest-risk local trust boundary.
  A typed command ID limits intent but is not process isolation.
- **Smallest exact planning fix:** require pinned/hash-verified read-only entrypoints, no learner
  imports/plugins/hooks, sanitized runtime, OS containment/no ambient home/cloud/network, use-time
  path identity checks, process-group kill, bounded/redacted output, and malicious import/TOCTOU/
  descendant tests. If the host cannot enforce containment, the runner stays disabled.
- **Applied:** normative Local Execution and Browser Security contract; P4 requirements, scenarios,
  steps and I5-04 acceptance.

### RT-02 — Loopback was treated as browser authentication

- **Pre-fix location:** P4 required a Unix socket or random loopback port/private runner token but
  did not bind portal browser mutations to Host/Origin/session/CSRF policy; ADR-006 called the
  first release localhost-only.
- **Failure scenario:** a hostile web origin posts to a predictable localhost portal endpoint, a
  rebinding hostname changes resolution, or permissive CORS/Host handling reaches a mutating BFF.
  The browser still never sees the runner token, yet the trusted portal becomes the confused
  deputy.
- **Smallest exact planning fix:** exact Host/Origin allow-lists, no wildcard CORS, launch-scoped
  high-entropy secret, HttpOnly/SameSite session, CSRF protection, random port, and cross-origin/
  DNS-rebinding tests; prefer runner Unix socket.
- **Applied:** normative browser boundary plus P4 requirement/scenario and I5-04 acceptance.

### RT-03 — Completion and mutation had multiple authorities without a commit/fencing protocol

- **Pre-fix location:** P4 owned runner journals and `EvidenceStager`; P5 independently owned
  portal SQLite `ProgressRepository`/`EvidenceRepository`; `lesson-lab-contract.md` → State
  Machine locked only a workspace operation.
- **Repository evidence:** direct Make targets mutate shared default data/export/catalog state
  (`Makefile:43-83,90-115`), while Airflow delegates to those shared defaults
  (`orchestration/airflow/callables/pipeline.py:35-50,72-89`).
- **Failure scenario:** evidence rename succeeds and SQLite completion fails, or progress commits
  before durable evidence; a runner reset overlaps direct `make bi`, `make lake-publish`, catalog
  ingest, or Airflow. Restart exposes orphan evidence, duplicate completion, or mixed state.
- **Smallest exact planning fix:** one state-authority matrix, blob flush/atomic rename followed by
  a single portal CAS transaction, unique run/evidence IDs, startup orphan reconciliation, and a
  common lease/fencing token across runner/Make/Airflow namespaces with cross-entrypoint barriers.
- **Applied:** normative Local State authority table/protocol; P3/P5 authority requirements; P4/P7
  fencing scenarios; PH-C06 trace.

### RT-04 — Eleven marts could be published as a mixed generation

- **Pre-fix location:** P7 planned a per-publish staged/current pointer but not one release spanning
  every asset/consumer; ADR-009 called current local publication recoverable without specifying a
  dataset-wide commit.
- **Repository evidence:** Parquet files are overwritten sequentially
  (`serving/export_marts_snapshot.py:31-44`); Iceberg drops/recreates each table sequentially
  (`lake/publish_iceberg.py:167-173`); read-back checks only existence/non-zero rows
  (`lake/publish_iceberg.py:217-231`). OpenMetadata current verification accepts nonzero table
  sets (`governance/openmetadata/verify_catalog.py:67-89`) rather than an exact release identity.
- **Failure scenario:** the process dies after six of 11 writes. Each surviving table is readable,
  so Rill/ClickHouse/OpenMetadata/evidence can report ready while combining two generations.
- **Smallest exact planning fix:** an all-11 `CuratedReleaseManifest` with source/dbt/semantic
  hashes, schemas/counts/checksums/snapshot IDs; stage and verify all, then atomically move one
  current pointer; every consumer pins `releaseId`. Reconciliation uses workspace/release namespace,
  managed marker, exact FQNs/edges and unmanaged-object preservation.
- **Applied:** schema owned by P1, local atomic export owned by P4 before P5, P7 extension to
  Iceberg/serving/governance, normative release protocol and PH-C06.

### RT-05 — The four marts cannot support campaign-level operational attribution

- **Pre-fix location:** `plan.md` Overview, `lesson-lab-contract.md` → First Representative Journey,
  and P5 called the result a verified four-mart product without a query/grain contract.
- **Repository evidence:** promotion is grouped by promotion/channel
  (`transform/dbt/models/marts/mart_promotion_effectiveness.sql:5-18`); fulfillment by
  carrier/region (`transform/dbt/models/marts/mart_fulfillment_performance.sql:4-15`); returns by
  reason/category/region (`transform/dbt/models/marts/mart_returns_analysis.sql:24-34`); DQ is
  global scenario/count (`transform/dbt/models/marts/mart_data_quality.sql:1-61`).
- **Failure scenario:** delays/returns from unrelated orders/campaigns are presented as evidence
  against one promotion. The result is deterministic and visually persuasive but analytically
  false.
- **Smallest exact planning fix:** define `promotion-trust-v1` with exact queries, grain, filters,
  weighted measures, thresholds/TBCs, limitations and failure IDs. Treat the four marts as
  independently labelled decision context; causal attribution requires a later additive common-
  grain product while preserving all 11 marts.
- **Applied:** P1 owns the query/assertion contract; overview, lesson, P5 and OWN-02 now say
  grain-honest evidence bundle; normative analytical boundary forbids hidden joins.

### RT-06 — Local unkeyed hashes overclaimed anti-forgery

- **Pre-fix location:** ADR-018, `lesson-lab-contract.md` → Evidence Record/Completion Threshold,
  requirements PH-H11 and SC-16.
- **Failure scenario:** the owner of the same local account edits evidence and SQLite, changes the
  verifier code, recomputes canonical SHA-256, and passes a self-contained hash check. Binding the
  hash inside learner-writable state does not authenticate its producer.
- **Smallest exact planning fix:** scope local SHA-256 to corruption/inconsistent-edit detection;
  accept completion only from a fresh private-runner result rechecked by the portal. Reserve
  cryptographic authorship/non-repudiation for I5-14 with an external key authority.
- **Applied:** ADR-018, lesson Evidence Record, NFR-04, PH-H11 and SC-16 now state the honest threat
  model. The TBC hosted signer remains honest.

### RT-07 — Parallel Wave 0 could score fake data, lose its fixture, and delay all feedback

- **Pre-fix location:** implementation graph Wave 0/I5-01/I5-02; P2 Dependencies/Implementation;
  ADR-005 time box; P1 emitted ignored evidence but no tracked handoff.
- **Repository evidence:** all `plans/**/*` and generated raw/DuckDB/Parquet assets are ignored
  (`.gitignore:62,101-107`); the repository has no existing frontend. A merge SHA therefore did
  not carry the assumed generated evidence across worktrees.
- **Failure scenario:** I5-02 adapts candidates to a provisional fixture, records measurements and
  an ADR, then the real I5-01 fixture disagrees; or it waits for I5-01 and no novice sees a page
  until I5-05. Three complete candidates consume the two-day cap with no runnable winner.
- **Smallest exact planning fix:** two-stage barrier: early `make learn-preview` is clearly fixture-
  backed/unscored/non-completing; I5-01 publishes a sanitized tracked fixture+manifest; all scores
  rerun after its merged SHA. Allocate 14 hours with 90-minute/3-hour kill rules, no synthetic
  score, explicit no-winner stop, and executable candidate retention through I5-05.
- **Applied:** normative earliest-outcome/spike contract; P1/P2 inventories and dependencies;
  ADR-005 and issue graph Wave 0. Scorecards moved to tracked
  `docs/decisions/evidence/adr-0005-web-stack-scorecard.*`.

### RT-08 — Shared-core, architecture assets, and root Make ownership serialized the wrong work

- **Pre-fix location:** I5-01→I5-03 required the same long-lived owner/worktree; P5 needed local C4
  assets while P6 exclusively owned them after P5 and also said it could start after P3; almost
  every phase planned to edit root Makefile while P6/P7 ran in parallel.
- **Repository evidence:** current Makefile has no help/include registry and only the shipped
  direct targets (`Makefile:1-20`). Existing generator/loader/export CLI path seams already exist;
  the missing propagation is concentrated in Airflow defaults
  (`orchestration/airflow/callables/pipeline.py:35-50,84-89`).
- **Failure scenario:** fake architecture placeholders unblock P5, P6 rewrites shared IDs later,
  or P6/P7 conflict in Makefile. A single person/worktree becomes the first-wave bottleneck while
  P1 reimplements seams and AWS contracts not needed by the preview.
- **Smallest exact planning fix:** I5-01 owns a minimal release, six local rendered views, root
  Make help/include and only proven Airflow forwarding. I5-03/P7 get serialized, time-bounded
  shared-contract leases that may have different owners. Later issues own disjoint
  `mk/issue-5/i5-<nn>.mk`; P6 preserves local view sources and starts only after merged P5 E2E.
- **Applied:** P1/P3/P6/P7, architecture view plan, command inventories and issue graph ownership/
  dependencies were reconciled.

### RT-09 — Commands, Docker-free lifecycle, resource gates, and release identity were not exact

- **Pre-fix location:** plan Artifact/Command contract, fitness catalogue, P1/P5/P8/P13 gates and
  file inventories.
- **Repository evidence:** current `core` deliberately starts no containers
  (`Makefile:32-38`), but the P1 gate required `docker compose config`; current `down` always invokes
  Docker (`Makefile:40-41`). The root `release-manifest.json` is unrelated ClaudeKit provenance
  (`release-manifest.json:1-8`).
- **Failure scenario:** a Docker-less learner cannot clear the claimed core path; future agents run
  nonexistent/inconsistently named targets or silently skip required tools; provisional RSS
  numbers are called pass despite double-counting Docker VM/container RSS; tracked evidence tries
  to embed its own final commit SHA or overwrites the reserved root manifest.
- **Smallest exact planning fix:** one target→owner→tier→status→artifact/failure registry, disjoint
  Make fragments, Docker-free `learn/status/down`, optional Compose-only Docker status, normalized
  repeated resource accounting with candidate thresholds until owner approval, an inherited
  reserved-path deny-list, exact runtime evidence path, and tested-tree/attestation/merge-tag SHA
  separation.
- **Applied:** normative command/lifecycle/resource/provenance registry; P1 Docker gate removed;
  P5/P8/P13 and issue graph updated. This exposes one local owner gate honestly: Phase 8 numeric
  thresholds block the full local release until approved, but do not block P1–P7 implementation or
  the P5 runner-backed acceptance.

### RT-10 — Architecture-first learning, API taxonomy, prerequisites, and hints were descriptive

- **Pre-fix location:** P6 inventories contained templates/diagrams/tests but no executable
  architecture lab; `lesson-lab-contract.md` listed taxonomy categories but omitted progress,
  tool-status/deep-link, data-query and health/readiness operations; remediation had no ordered
  hint or executable prerequisite schema.
- **Failure scenario:** a novice gets a binary missing-tool error or full solution reveal; an
  agent implements framework-local routes with no authority/idempotency trace; the highest-priority
  architecture curriculum releases as downloadable templates rather than hands-on learning.
- **Smallest exact planning fix:** machine-readable non-mutating prerequisite probes and ordered
  logged hints; complete operation matrix with taxonomy/physical owner/trust/idempotency/evidence;
  at least one executable F01→F04→J01/J04/J05 controlled-failure/reset/fitness/evidence journey.
- **Applied:** lesson contract/API list, P3/P5, P6 file inventory/gate, curriculum release gate,
  requirements outcome matrix and I5-06 acceptance.

### RT-11 — AWS durable resources and office lifecycle had no complete Terraform/composition owner

- **Pre-fix location:** P10 owned network/IAM/ECS/office/observability only; P11 was prohibited from
  Terraform but required S3/catalog/DB/search/portal state; P10/P11 could finish independently with
  no exact integration closure.
- **Failure scenario:** ECS tasks exist while S3/Iceberg/catalog, Superset/OpenMetadata DB/search,
  portal evidence/progress, KMS/secrets and backups are undefined or instance-local. A mocked office
  workflow never invokes the actual P11 images/descriptors/health/state transitions.
- **Smallest exact planning fix:** P10 owns Terraform for every accepted P9 state/key/backup row;
  P11 never edits Terraform. After parallel work, a sequential composition gate binds exact P10
  outputs and P11 descriptor/image hashes and simulates open→restore/hydrate→ready→drain→backup→
  close plus failures.
- **Applied:** P10 module inventory/acceptance, P11 composition files/gate, issue graph dependency/
  ownership and normative AWS ownership contract.

### RT-12 — Mocked offline checks were called a plan and real recovery evidence was circular

- **Pre-fix location:** requirements and P10/P13 used `terraform-plan-offline`; P11 real
  compatibility/empty restore was required before every apply while no environment could be
  created to obtain it.
- **Failure scenario:** fake provider values are published as deployability evidence, or AWS apply
  is permanently blocked because the restore evidence can only be produced after resource
  creation. An ad hoc “first apply” then bypasses the policy to break the circle.
- **Smallest exact planning fix:** rename gates to `terraform-validate-offline` and
  `terraform-test-mocked`, label evidence mocked, reserve `terraform-plan-aws` for real provider
  planning, and require a separate future disposable/pre-existing validation-environment
  authorization with account, role, budget, quota, TTL, teardown/residual scan and human gates.
  Its evidence may clear production admission but does not authorize production.
- **Applied:** P10/P11/P13, fitness catalogue, OWN-07, issue graph and normative AWS contract.

### RT-13 — FinOps modeled a schedule and prose BOM, not actual current topology behavior

- **Pre-fix location:** P9 `CostScenario` had only `sourceDate`; no reverse reconciliation to P10
  plan/inventory; alarms “flagged” cost but no enforcing authority was defined.
- **Failure scenario:** ALB, NAT/endpoints, RDS/search minimums, EBS/snapshots, retained S3 versions,
  KMS/secrets/logs/state/backup requests or scale-from-zero lag are omitted and the cost check still
  passes. A retry storm triggers an alarm but no component blocks new work or tears down resources.
- **Smallest exact planning fix:** every accepted topology/plan/inventory resource has priced
  quantity or exclusion with region/SKU/dimension/unit/currency/source/effective/retrieval/TTL;
  model ECS/ASG launch/warmup/readiness/drain/residual behavior; define a durable `CostGuard`
  admit/block/drain/teardown/break-glass/reconcile state machine.
- **Applied:** P9 interfaces/tests, PH-C04 and the normative cost contract. Numeric budgets,
  retention and SLOs remain honest owner TBCs and still block AWS apply/claims only.

### RT-14 — Hosted ingress, saved-plan authorization, state recovery, and key authority were loose

- **Pre-fix location:** P10 allowed an ingress design before I5-14; approval was bound to an
  ambiguous “plan SHA”; state rows omitted key/config authorities and separate recovery identity.
- **Failure scenario:** a learner reaches an AWS portal with no tenant/object authorization; an
  approval is replayed after variables/provider lock/backend serial change; state objects restore
  but rotated/deleted KMS/application keys or configuration make them unreadable; the same broad
  apply role can weaken deletion protection and “recover” state.
- **Smallest exact planning fix:** no learner-reachable ingress before I5-14; pre-I5-14 validation
  is private operator-only. Single-use authorization binds saved binary plan, Git/config/module/
  lock/vars, backend lineage+serial, account/region/env/role, approver, nonce/expiry/consumption and
  applies without replanning. Recovery role and key/secret/config rotation/escrow/deletion/restore
  ordering are separate and tested against old ciphertext.
- **Applied:** ADR-014/015 and AWS state gate, P9/P10, I5-10/I5-14 dependencies and normative AWS
  trust contract. No apply or validation environment was authorized or created.

### RT-15 — AI admission conflated local/hosted claims and could auto-scope a runtime

- **Pre-fix location:** P12 made I5-14 conditional “where multi-user is claimed,” listed
  `apps/agent-labs/**` in the same admission phase, and described LangGraph/Restate/AgentCore
  responsibilities without selecting one durable authority or binding approval arguments.
- **Failure scenario:** local single-actor eval marks ACL fields N/A and is promoted to hosted;
  passing the checklist scaffolds a credentialed runtime without a new authorization; LangGraph,
  Restate and AgentCore session memory each retry an effect; approval for one tool/target is reused
  with changed arguments or cost.
- **Smallest exact planning fix:** separate `local-single-actor-read-only` and
  `hosted-agentcore` profiles; hosted requires I5-14 plus AWS gates and no N/A ACL. Admission emits
  a report/ADR only; runtime is a separate human-authorized follow-up. Select one durable workflow/
  approval/idempotency authority and bind approval to actor, policy/data, exact tool/args/target/
  effect/key/cost/expiry/nonce/digest.
- **Applied:** P12 requirements/inventory/steps, I5-12 dependency/ownership and normative AI
  admission contract. AI remains optional and off.

## Specific Challenge Answers

| Challenge | Reconciled answer after fixes |
|---|---|
| Can I5-01/I5-02 run in parallel without fake fixtures choosing the ADR? | Only common tests and an unscored preview run in parallel. Scoring/ADR is blocked on the merged tracked I5-01 fixture and a complete rerun. |
| Is I5-05 the earliest runnable page? | No. I5-02 owns `learn-preview`; it is useful for feedback but visibly simulated and cannot complete. I5-05 remains the earliest accepted runner-backed outcome. |
| Is the three-candidate spike worth it? | It is bounded to 14 hours with common/per-candidate kill rules, no-winner stop, equal real-fixture tests, and executable retention. The audit may still cut it, but it can no longer consume unbounded delivery time. |
| Does I5-01→I5-03 create a bottleneck? | Contract writes remain serialized, but not to one person/worktree. I5-01 is narrowed; I5-03/P7 receive exact time-bounded leases and release SHAs. |
| Are Make targets/artifacts/status/security tiers actionable? | A normative registry now names owner, future availability, exact target, tier, evidence root, statuses and failure boundary. It explicitly says targets do not exist at planner input. |
| Can the first path run without Docker? | Yes by contract: host portal + contained runner + DuckDB. Compose tools are optional profiles. `learn/status/down` cannot invoke Docker in core. |
| Is durable authority separated from projections/indexes/metadata/evidence? | Yes in the authority and curated-release tables; Rill/ClickHouse/search/OpenMetadata are release-pinned projections, not hidden authorities. Portal progress, runner state, evidence bytes and completion each have one commit rule. |
| Are AWS modules testable offline without pretending deployability? | Yes for syntax/policy/mocked behavior only. Real plan/compatibility/restore retain distinct credentialed gates and separate authorization. |
| Is a hidden owner decision blocking local implementation? | No external AWS TBC blocks P1–P7. P8 threshold approval now visibly blocks only the full local release after measurement; ADR-005 and contract/runner choices are owned outputs of P2–P4, not hidden owner TBCs. |
| Can future agents follow the graph without touching protected/shared paths incorrectly? | Root Make, view sources, contract leases, ignored fixture handoff, `docs/code-standards.md`, root `release-manifest.json`, discovery history and exact-SHA handoffs now have explicit ownership/deny rules. |

## Disagreement Reconciliation and Rejected Alarms

- **Accepted despite existing typed argv:** the security reviewer demonstrated that
  `shell=False` does not stop interpreter imports/plugins, TOCTOU or output leaks. The abstract
  “arbitrary shell” concern was not duplicated; the stronger execution-boundary finding RT-01 was
  accepted.
- **Accepted despite per-workspace locks:** the failure reviewer showed direct Make/Airflow paths
  do not participate. RT-03 therefore requires cross-entrypoint fences, while a claim that no
  idempotency was planned at all was rejected.
- **Accepted despite atomic-pointer language:** it did not span all 11 assets/consumers. RT-04 was
  accepted at dataset-release scope, not as a claim that the plan had no recovery concept.
- **Rejected — model/metric inventory is wrong:** repository sweeps verified 18 staging inputs,
  six intermediate models, seven dimensions, nine facts, 11 marts, the 51-model lineage
  explanation, expected dbt warnings, curated asset membership, and weighted Rill measures.
- **Rejected — OpenMetadata must always show 51 physical entities:** the reviewed distinction
  between 45 materialized logical dbt assets and ephemeral models is valid. The accepted issue is
  namespace/exact-set reconciliation, not the count explanation.
- **Rejected — office hours is only cron:** the plan already had restore/hydrate/readiness and
  drain/checkpoint sequencing. The accepted deficiencies are exact P10/P11 composition, real
  scale behavior and enforcing CostGuard.
- **Rejected — ClickHouse is silently durable or EC2-zero is called zero cost:** ADR-010 and P9
  already describe ClickHouse as a disposable hypothesis and enumerate residual cost. RT-13 makes
  those claims mechanically reconciled/current rather than reversing the decision.
- **Rejected — Terraform apply was authorized:** P10 explicitly prohibited apply/destroy. RT-12
  and RT-14 distinguish validation evidence and harden any future authorization; they do not claim
  this plan authorized cloud action.
- **Rejected — AsyncAPI was forgotten:** ADR-017 deliberately excludes it until an actual channel
  exists. The operation-matrix fix stays in OpenAPI.
- **Rejected — local/AWS topologies must be identical:** ADR-004 correctly shares contracts, not
  physical services. No topology symmetry was added.
- **Rejected — controlled/environmental failure, reset, evidence, reflection, accessibility or
  non-copy boundary was absent:** those were already substantive. RT-10 adds novice prerequisite/
  hint and executable architecture depth without reopening verified behavior.
- **Rejected — exact-SHA handoffs are generally absent:** the issue graph already requires merged
  integration SHAs. RT-07 fixes the specific ignored fixture exception; RT-09 fixes recursive
  release-attestation identity.

## Bounded Fix Summary

The red team added one normative companion,
`execution-authority-and-release-contract.md`, and changed only this issue plan package. Fixes were
then wired into `plan.md`, the affected phase files, architecture/curriculum/lesson/traceability
companions, and the implementation issue graph. Raw discovery artifacts and the historical
initial-validation report were not rewritten.

No TBC was converted into a fact. Monthly budget/residual ceiling, retention by class,
cold-start/readiness SLO, production RTO/RPO, AWS account/environment, apply approver, managed
metadata/search topology, live compatibility, local measured resource thresholds, AI corpus/eval
thresholds and credentialed AI/AWS authority remain unresolved at their honest boundary.

## Residual Risks

1. The plan is still broad. The 14-hour web spike, I5-05 first journey, P8 measured release and
   non-applying AWS wave need scope enforcement during the separate readiness audit.
2. OS containment is platform-dependent. If macOS/Linux support cannot meet RT-01 without Docker,
   the plan intentionally falls back to static/direct expert mode rather than weaken the boundary;
   that may force an owner product decision later.
3. A grain-honest “insufficient evidence” journey may be less satisfying than causal promotion
   analysis. An additive common-grain product is allowed later but remains unapproved scope.
4. All exact future Make targets are planning contracts, not present commands. The readiness audit
   must verify issue bodies copy the registry and ownership rather than treating this report as
   executable proof.
5. AWS prices, service support and Terraform provider behavior remain mutable. Current-source and
   real validation gates intentionally prevent this red-team pass from certifying deployability.
6. No AWS validation account, budget, approver, RTO/RPO or retention choice exists. All AWS applies
   remain blocked; this does not block the credential-free local implementation path.
7. AI profiles and approval semantics are planned, not admitted. No runtime implementation or
   AgentCore use is authorized.

## Verification Contract and Publication

Before publication, this phase must record:

- `ck plan status plans/260721-005-enterprise-learning-sandbox/plan.md`;
- structure/frontmatter/link/ID/dependency/ownership sweeps;
- command registry/exactness sweep;
- `git diff --check`;
- changed-path allow-list proving only this plan directory changed;
- credential-signature scan;
- force-add only this ignored plan directory;
- commit/push and exact local/tracking/remote output SHA equality;
- issue #5 comment with phase identity, input/output SHAs, findings/fixes/residual risks,
  commands/results, verdict, label, and explicit no-audit/no-implementation statement.

The command results and immutable output SHA are published externally after the commit because a
tracked report cannot truthfully self-record the SHA of the commit containing itself.

## Final Verdict

All accepted Critical/High plan defects have bounded fixes and no contradictory local or AWS/AI
authority remains in the active plan artifacts. Remaining uncertainty is explicit, owned and
blocks only its declared boundary. Canonical state remains **`ready for plan audit`**, not
`ready to cook`.

`RED_TEAM_VERDICT=PASS_AFTER_FIXES`

`ISSUE_STATE=ready for plan audit`
