# Implementation Issue Graph

## Authorization Boundary

This is a proposed follow-up graph, not authorization to create/cook the issues. Independent plan
validation and readiness audit must approve the master plan first. No issue may apply Terraform
or create cloud resources unless a later owner explicitly authorizes that separate action.

Every implementation issue must record:

- immutable main input `3cd3d41f71582774e8d9656a51d1044035f4503c`;
- reviewed tree head `d0273731a5077cc17c2f4398057623b83a50bb65`;
- discovery SHA `d3ce0c5832cca4f1b68299cbba111e7cc6c7a430`;
- immutable planner output `8ec96f92245c679d019ac3648c5c2d77a49f0429`, independent validation
  output `5962316b8113ece592a26fe6211a97ae77eb70fb`, red-team output/readiness input
  `bf740edb87452fe766591d0eeefd0bd5151220fa`, and later readiness-audit report SHA;
- files it exclusively owns, public contracts it consumes, and exact evidence command.

Every implementation issue inherits `risk:high`, `tdd`, and `security:S3` from the epic even when
its additional labels express a narrower specialty. `security:S3` requires a written disposition
of the epic S3/data-security threat model; it does not imply every issue touches AWS. Every merge
also requires the owner-mandated human pre-merge approval. An issue body may not weaken these
inherited gates.

## Shared-Contract Stewardship

I5-01 owns the first minimal shared-core release: golden preservation/command, evidence base,
tracked promotion fixture, six required local view sources, and the root Make include/help
registry. Shared contracts include:

- `learning/contracts/**`
- `contracts/openapi/**` and any future `contracts/asyncapi/**`
- `contracts/data/{retail-golden-v1.json,promotion-trust-v1.yaml,curated-release-manifest.schema.json}`;
  later data contracts use the I5-07 lease below
- architecture workspace/manifest schema, required IDs and include interfaces
- evidence schema/canonicalization/version registry
- golden baseline command/evidence envelope
- mappings for generator anomalies, dbt/marts/lineage/Rill metrics, and
  `lake/curated_assets.json`

I5-03 receives a time-bounded sequential lease after I5-01 merges; it may have a different owner
and worktree, but never overlaps another shared-contract writer. I5-07 later receives a similarly
serialized lease for equivalence/Iceberg/OpenMetadata/curated-release contracts before I5-11.
After the merged I5-05 E2E, I5-06 receives a separate time-bounded architecture-view lease for
P6-owned workspace includes and manifest rows only; it cannot modify I5-01 local view sources,
rows, IDs or rendered paths.
Other issues consume released versions read-only. Each lease uses additive-first versioning,
compatibility tests, a migration note, and a new exact contract release SHA before downstream
work resumes. This serialization protects contracts without making one person/worktree the
first-release bottleneck.

I5-01 is the only normal owner of root `Makefile` changes: it adds help and includes
`mk/issue-5/*.mk`. Each later issue exclusively owns `mk/issue-5/i5-<nn>.mk`; root edits require a
new serialized shared-core lease. Parallel P6/P7 never edit the same command file.

## Dependency Graph

```text
Validation + readiness audit
        +--> I5-01 Golden/shared core --------+
        +--> I5-02 Representative web spike --+--> I5-03 Lesson/lab/evidence contracts
                                                      |
                                                      +--> I5-04 Privileged runner
I5-02 + I5-03 + I5-04 -------------------------------> I5-05 Portal slice
                                                           |
                                                           +--> I5-06 Curriculum/C4
                                                           +--> I5-07 Data guided labs
I5-05 + I5-07 ---------------------------------------> I5-08 Local profiles
I5-05 + I5-06 + I5-07 + I5-08 ----------------------> I5-13 Local release

I5-01 + I5-06 --> I5-09 AWS decisions --> I5-10 Terraform (no apply)
                                      \--> I5-11 AWS adapters (no apply)
I5-10 + I5-11 ---------------------------> I5-11 composition gate (no apply)

I5-07 -----------------------------------> I5-12 local read-only AI admission
I5-09 + I5-10 + I5-11 + I5-14 ----------> I5-12 hosted-agentcore admission
```

AWS decision work does not block I5-02 through I5-08. AWS apply remains blocked regardless of
whether I5-09 through I5-11 merge.

## Wave and Parallelization Strategy

| Wave | Issues | Parallelism | Merge rule |
|---|---|---|---|
| 0 | I5-01, I5-02 | Start in parallel only for I5-02 common tests/unscored `learn-preview`; no provisional fixture measurement or score survives | I5-02 scoring/ADR waits for merged tracked I5-01 fixture manifest and records its SHA/hashes |
| 1 | I5-03, I5-04, I5-05 | Sequential contract→runner→portal integration; portal-only shell work may start after I5-02, but no product expansion merges before the runner-backed journey | Wave exits only when `make local-journey-e2e` passes the real promotion-trust journey |
| 2 | I5-06, I5-07 | Parallel only after I5-05 E2E; distinct architecture/curriculum vs data-lab ownership | Shared contract changes routed sequentially through the I5-01 owner |
| 3 | I5-08, I5-13 local gates | I5-08 measures profiles; I5-13 begins release harness after I5-05 | Local release requires I5-01..I5-08 |
| AWS | I5-09 then I5-10/I5-11 | Module and adapter work may parallel after interface freeze; composition is sequential after both exact outputs | Non-applying only; offline/mock evidence cannot claim deployability/readiness |
| Later | I5-14 then optional I5-12 | Hosted identity before multi-user/AI authorization | Separate approval and worktrees |

The first implementation wave is explicitly optimized for a runnable learning web vertical slice,
not a complete curriculum or cloud topology.

## Branch and Worktree Strategy

After validation and a separate readiness audit both pass, create the integration branch from the
exact readiness-audit output commit. That commit must descend from this immutable planner input
and contain the discovery, planner, independent-validation, red-team, and audit artifacts:

```text
integration/issue-5-local-learning
```

Each bounded issue uses:

```text
feature/issue-5-01-golden-contract
feature/issue-5-02-web-spike
feature/issue-5-03-learning-contracts  # sequential shared-contract lease; owner may differ
feature/issue-5-04-lab-runner
feature/issue-5-05-portal-vertical-slice
...
```

Use one sibling worktree per branch, for example
`{workspace-parent}/ai-ready-data-platform-issue-5-04-lab-runner`. Never share `.venv`,
`node_modules`, generated data, Docker project names, ports, evidence directories, or Terraform
working/state directories between worktrees. Each issue derives a unique Compose project name and
port range.

Merge policy:

1. Issue start evidence records integration input SHA, upstream merged dependency SHAs, contract
   versions, branch, and worktree. Any mismatch stops work.
2. Rebase/merge current integration branch before final verification and record the new input SHA.
3. Re-run the issue's golden/contract blast-radius commands and record issue output SHA.
4. A dependent issue starts only from the upstream issue's merged integration SHA, never its
   unmerged feature SHA.
5. Merge only through a reviewed PR with the inherited `risk:high`/TDD/security:S3/human gate.
6. Delete no old contract until dual-read/rollback acceptance passes.
7. Never force-push shared integration/main.

## Exact Dependency Matrix

| Issue | blockedBy | blocks |
|---|---|---|
| I5-01 | validation PASS, readiness-audit PASS | I5-02 scoring/ADR, I5-03, I5-04, I5-07, I5-09, all refactors |
| I5-02 | validation PASS for unscored preview; merged tracked I5-01 fixture before scoring/ADR | I5-03, I5-05 |
| I5-03 | I5-01 merged, I5-02 ADR merged | I5-04, I5-05 |
| I5-04 | I5-01 and I5-03 merged | I5-05, runner-backed I5-07 |
| I5-05 | I5-02, I5-03, I5-04 merged | I5-06, I5-07, I5-08, I5-13 |
| I5-06 | I5-03 and I5-05 merged | I5-09, I5-13 |
| I5-07 | I5-01, I5-03, I5-04, I5-05 merged | I5-08, I5-11, I5-12, I5-13 |
| I5-08 | I5-05 and I5-07 merged | I5-13 |
| I5-09 | I5-01 and I5-06 merged | I5-10, I5-11; AWS apply remains separately blocked |
| I5-10 | I5-09 interface release | I5-11 composition; optional non-applying release evidence only |
| I5-11 | adapter work: I5-07/I5-09; composition: exact I5-10 output plus frozen adapter output | hosted I5-12 profile; AWS readiness claim |
| I5-12 | local profile: I5-07; hosted profile: I5-09/I5-10/I5-11 composition and I5-14 | admission report only; runtime needs separate human authorization |
| I5-13 | I5-01..I5-08 merged | local release/owner merge decision |
| I5-14 | I5-13 and separate hosted-product decision | multi-user I5-12 claim |

## File Ownership Matrix

| Owner issue | Exclusive paths | Consumes read-only/shared |
|---|---|---|
| I5-01 | `scripts/golden/**`, `contracts/data/{retail-golden-v1.json,promotion-trust-v1.yaml,curated-release-manifest.schema.json}`, base `learning/contracts/**`, evidence core, six local view sources, dependency locks, root `Makefile` include/help | Current data spine |
| I5-02 | `spikes/web/**`, `docs/decisions/evidence/adr-0005-web-stack-scorecard.*`, ADR-005 proposal, `mk/issue-5/i5-02.mk` | Tracked golden evidence fixture + draft lesson |
| I5-03 | Sequential shared-contract lease for lesson/lab/progress schemas, operation matrix and first manifests; `mk/issue-5/i5-03.mk` | I5-01 evidence core, I5-02 score |
| I5-04 | `apps/lab-runner/**`, runner tests, workspace runtime config, `mk/issue-5/i5-04.mk` | Released contracts; existing pipeline entrypoints |
| I5-05 | Winning `apps/learning-portal/**`, portal tests, `mk/issue-5/i5-05.mk` | Released lesson/OpenAPI/evidence contracts; runner API |
| I5-06 | `learning/curriculum/**`, architecture lab, AWS/publish Structurizr expansions, implementation ADR templates, `mk/issue-5/i5-06.mk`; time-bounded view-workspace/manifest lease for expansion rows/includes/renders only | Six I5-01 local views, rows, rendered paths and include interfaces read-only; portal renderer |
| I5-07 | `learning/labs/data-platform/**`, data lab verifiers, later data-contract lease, narrowly approved pipeline seams, `mk/issue-5/i5-07.mk` | Golden data contracts; runner registry |
| I5-08 | Compose/profile admission/resource scripts/tests and `mk/issue-5/i5-08.mk` | Portal/runner images; existing profiles |
| I5-09 | `docs/decisions/aws/**`, cost/state models/tests and `mk/issue-5/i5-09.mk` | Architecture/deployment model |
| I5-10 | `infra/aws/terraform/**`, Terraform tests/policies and `mk/issue-5/i5-10.mk` | Accepted I5-09 interfaces |
| I5-11 | `platform/adapters/aws/**`, `platform/images/**`, portal-status descriptors/composition tests and `mk/issue-5/i5-11.mk`; never Terraform or portal source | Data contracts + released portal registry + I5-09 decisions + read-only exact Terraform outputs |
| I5-12 | AI admission/eval/contracts and `mk/issue-5/i5-12.mk`; no runtime/app/cloud adapter in admission issue | Governed data/identity/evidence interfaces |
| I5-13 | Release evidence orchestration, tracked runbook/docs and `mk/issue-5/i5-13.mk` | All merged outputs; does not change their contracts |
| I5-14 | `platform/identity/hosted/**`, `tests/hosted/{authz,isolation}/**`, `mk/issue-5/i5-14.mk`; any OpenAPI/portal adapter change requires a serialized shared-contract/portal integration lease | Local object-shaped contracts and released portal/runner/evidence interfaces |

## Proposed Follow-up Issues

### I5-01 — Freeze golden baseline and shared architecture contracts

- Labels: `risk:high`, `security:S3`, `tdd`, `shared-core`, `data-integrity`.
- Depends on: independent plan validation + readiness audit.
- Phase: 1.
- TDD:
  1. Write characterization tests for current generator bytes/anomalies, 18 raw tables,
     dbt warnings/51-model lineage/11 marts, Rill weighted metrics, Airflow graph,
     curated assets and historical evidence parsing.
  2. Add lock-hash environment setup, only the proven missing Airflow path forwarding,
     `make golden-clean`, tracked sanitized promotion fixture, evidence schema/canonicalization,
     root Make include/help, and the six rendered local views.
  3. Re-run current and new contract suites twice from clean generated state.
- Acceptance:
  - exact main/discovery/reviewed-tree inputs recorded;
  - `release-manifest.json` and unrelated files unchanged;
  - `docs/code-standards.md` hash-preserved if present at issue input, otherwise preservation
    manifest records `absent`; the issue never creates/overwrites/deletes it;
  - future command regenerates ignored fixtures and evidence without pre-existing venv/data;
  - tracked fixture/manifest crosses worktrees by merged SHA; no ignored artifact is a dependency;
  - preservation/migration mapping and rollback manifest committed.
- Verify:

```bash
make golden-clean PROFILE=small SEED=42
make data-contracts-check
make evidence-contracts-check
make architecture-check
git diff --check
```

### I5-02 — Select web stack with one representative lesson

- Labels: `risk:high`, `security:S3`, `tdd`, `frontend`, `accessibility`, `decision-gate`.
- Depends on: validated plan for unscored preview; scoring/ADR waits for the merged tracked I5-01
  fixture manifest.
- Phase: 2.
- Candidates: Astro+React islands, Next.js App Router, React/Vite+typed API.
- TDD: shared interaction/a11y/E2E test first; implement same lesson in time-boxed spikes; capture
  bundle/start/RSS/JS/a11y evidence; accept ADR-005.
- Acceptance: fixture-labelled preview cannot complete; 14-hour/per-candidate kill rule; all
  surviving must-passes; weighted score/tie rule; no copied proprietary content; reproducible
  candidate artifacts retained through I5-05.
- Verify: `make learn-preview LESSON=promotion-trust`; `make web-spike-scorecard-check`; candidate
  unit/a11y/Playwright commands recorded in the scorecard.

### I5-03 — Version lesson, lab, progress and evidence contracts

- Labels: `risk:high`, `security:S3`, `tdd`, `shared-core`, `api`.
- Depends on: I5-01, ADR-005 evidence from I5-02.
- Phase: 3.
- TDD: failing schema/ref/state/tamper/migration fixtures first; implement JSON Schemas, OpenAPI,
  state machine and evidence canonicalization; add backward-reader tests.
- Acceptance: complete contract from `lesson-lab-contract.md`; operation matrix covers every
  claimed taxonomy operation; one completion authority/reconciliation protocol; prerequisite
  probes/hint ladder; no AsyncAPI without a channel; promotion-trust manifest validates.
- Verify: `make learning-contracts-check api-contracts-check evidence-contracts-check`.

### I5-04 — Build isolated privileged local runner

- Labels: `risk:high`, `security:S3`, `tdd`, `backend`.
- Depends on: I5-01, I5-03.
- Phase: 4.
- TDD: interpreter/import/startup-hook/argv/path-TOCTOU/env/quota/output/descendant/base-write/
  browser-request/cross-entrypoint-race/crash/idempotency negatives first; implement runner; full
  data-contract regression.
- Acceptance: private transport with Host/Origin/CSRF protections, pinned entrypoints and OS
  containment, typed commands, shared mutation fencing, all-11 atomic local release pointer,
  read-only base, no ambient credentials/network or Terraform apply, auditable state; otherwise
  runner remains disabled.
- Verify:

```bash
make runner-test
make runner-security-test
make runner-race-test
make data-contracts-check
```

### I5-05 — Deliver runnable promotion-trust portal slice

- Labels: `risk:high`, `security:S3`, `tdd`, `frontend`, `accessibility`, `vertical-slice`.
- Depends on: I5-02, I5-03, I5-04.
- Phase: 5.
- TDD: component/state/a11y/real-browser journey tests first; implement portal modular monolith and
  BFF; integrate actual runner/data products; run manual AT/visual review.
- Acceptance: business question→grain-honest four-mart context→decision→reset→verified evidence
  bundle→evidence; one crash-safe completion authority; Docker unavailable; no cloud credential;
  static/reduced-motion path; external-tool unavailable states.
- Verify:

```bash
make portal-test portal-a11y
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
make portal-visual-review
make learn-status
make learn-down
```

### I5-06 — Publish architecture curriculum, templates and fitness functions

- Labels: `risk:high`, `security:S3`, `tdd`, `architecture`, `curriculum`.
- Depends on: I5-03 and passing, merged I5-05 real journey; no portal-source overlap.
- Phase: 6.
- TDD: broken-reference/prerequisite/view/ADR/pattern-without-failure fixtures first.
- Acceptance: foundation→mid graph, templates, read-only preservation of I5-01 local views,
  expansion renders/text, requirement/ADR/test traceability, pattern admission rules, and one
  executable architecture failure-reset-verify-evidence lab.
- Verify: `make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check`.

### I5-07 — Add data-pipeline guided labs without changing golden semantics

- Labels: `risk:high`, `security:S3`, `tdd`, `data-platform`, `recovery`.
- Depends on: I5-01, I5-03, I5-04 and passing, merged I5-05 real journey.
- Phase: 7.
- TDD: current warning/mart/lineage/publish/catalog behavior first; add labs and fail-loud seams;
  regression/equivalence after.
- Acceptance: labs for deterministic ingest/model/quality, orchestration, metric weighting,
  eleven-asset atomic curated release, Iceberg commit/recovery, namespace-safe exact OpenMetadata
  reconciliation; every service/pattern has a failure.
- Verify: `make data-labs-e2e lake-fault-test metadata-reconcile-test data-contracts-check`.

### I5-08 — Enforce local profiles and resource budgets

- Labels: `risk:high`, `security:S3`, `tdd`, `performance`, `compose`.
- Depends on: I5-05, I5-07.
- Phase: 8.
- TDD: invalid profile combinations and measurement schema first; implement admission/telemetry;
  cold/warm profile matrix.
- Acceptance: Docker-free core remains green; each admitted heavy profile fits owner-approved,
  normalized repeated thresholds; all-three denied; guarded co-run measured; teardown clean.
- Verify: `make compose-check compose-security-check profile-budget-check recovery-test`.

### I5-09 — Decide AWS state, cost, persistence and readiness

- Labels: `risk:high`, `security:S3`, `tdd`, `decision-gate`, `aws`, `finops`, `recovery`.
- Depends on: I5-01, I5-06. Does not block local issues.
- Phase: 9.
- TDD: incomplete state/cost/TBC matrices fail schema tests; cost golden cases first.
- Acceptance: state/key/config authority matrix; ClickHouse/catalog/metadata/search options;
  topology/plan-reconcilable current-source BOM; enforcing CostGuard; apply TBCs explicit; no
  false zero-cost/scale-to-zero claim.
- Verify: `make state-matrix-check cost-model-check aws-decision-check`.

### I5-10 — Build non-applying Terraform platform modules

- Labels: `risk:high`, `security:S3`, `tdd`, `terraform`, `no-apply`.
- Depends on: I5-09 accepted design interfaces.
- Phase: 10.
- TDD: policy/mocked tests for network/IAM/state/schedule/persistence/wrong-account first; build
  modules; run static/offline/mocked checks.
- Acceptance: networking, IAM, state backend, every admitted P9 persistence/key/backup row, ECS
  capacity, office workflow, observability/budget/teardown outputs, and exact saved-plan envelope;
  no default/apply path and no learner ingress before I5-14.
- Verify: `make terraform-check terraform-validate-offline terraform-test-mocked`; real
  `make terraform-plan-aws` remains credential/account/role gated and is not apply authorization.

### I5-11 — Prove AWS ClickHouse/Superset/OpenMetadata/S3-Iceberg adapters

- Labels: `risk:high`, `security:S3`, `tdd`, `aws`, `data-platform`, `persistence`, `no-apply`.
- Depends on: adapter work after I5-07/I5-09; composition waits for exact I5-10 and I5-11 outputs;
  never edits Terraform-owned paths.
- Phase: 11.
- TDD: local contract fixtures and incompatibility cases first; adapter lifecycle/equivalence;
  recovery readiness tests.
- Acceptance: validated catalog choice; ClickHouse role evidence; Superset/OpenMetadata state and
  restore contract; exact descriptor/module office lifecycle composition; versioned divergences;
  offline mocks not deployability; no cloud resource created by default.
- Verify: `make aws-adapters-contract engine-equivalence metadata-contracts-check aws-composition-check`;
  separately authorized validation-environment restore drills later.

### I5-12 — Optional governed AI admission and learning add-on

- Labels: `risk:high`, `security:S3`, `tdd`, `ai`, `optional`, `cost`.
- Depends on: I5-07 for local-single-actor-read-only admission; I5-09/I5-10/I5-11 composition and
  I5-14 for hosted-agentcore admission.
- Phase: 12.
- TDD: ACL/prompt-tool injection/citation/redaction/approval/replay/crash/cost evals first.
- Acceptance: profile-specific admission JSON; exact approval digest; one durable workflow/
  approval/idempotency authority; local core unchanged. Passing admission creates no runtime;
  implementation needs a separate human-authorized follow-up.
- Verify: `make ai-admission-check`; optional credential-gated `make ai-evals`.

### I5-13 — Produce clean-checkout release, recovery and rollback evidence

- Labels: `risk:high`, `security:S3`, `tdd`, `release`, `evidence`.
- Depends on: I5-01..I5-08 for local release; includes merged non-applying AWS checks when present.
- Phase: 13.
- TDD: release manifest schema and stale/forged evidence failures first; aggregate checks; run from
  clean checkout twice; review docs/rollback.
- Acceptance: all gates pass, tested-tree/attestation/merge-tag provenance is non-recursive,
  reserved root manifest/user paths are unchanged, browser/manual evidence retained, rollback
  rehearsed, runtime artifacts ignored, no product contract drift.
- Verify: `make release-evidence`, `git diff --check`, clean status, plan-defined evidence
  manifest.

### I5-14 — Hosted multi-user identity and tenant evolution (later)

- Labels: `risk:high`, `security:S3`, `tdd`, `identity`, `hosted`.
- Depends on: local release I5-13 and separate product decision.
- Expected files/behavior: own `platform/identity/hosted/**`, hosted authz/isolation tests and
  `mk/issue-5/i5-14.mk`; add IdP/session/tenant/object authorization, per-lab workspace quotas,
  instructor/operator roles, deletion/retention and cross-user denial without changing the local
  single-actor contract. Any OpenAPI or portal adapter edit uses a serialized lease and exact
  released seam. Not required for the first local release.
- TDD: write cross-user object-enumeration, role downgrade/expiry, CSRF/session fixation,
  quota/race, retention/deletion and evidence-isolation failures first; implement the hosted
  adapters and policy; rerun local runner/portal/evidence and tenant blast-radius suites after.
- Acceptance: no learner-reachable AWS ingress or hosted-agentcore claim exists before this issue
  merges; all tenant/object/role denials are non-enumerating and audit-redacted; local mode and
  evidence readers remain backward compatible; `security:S3` threat disposition and manual human
  pre-merge approval are retained.
- Migration/rollback: additive hosted adapters and schema version only; feature remains off by
  default, old local readers remain valid, and rollback disables hosted ingress/revokes sessions
  without deleting local evidence or tenant data outside an approved retention runbook.
- Evidence/STOP: emit schema-valid results below
  `.artifacts/evidence/hosted-identity/<run-id>/`; stop while the hosted-product decision, IdP,
  retention/deletion values, key authority, account/environment or separate ingress/apply
  authorization is TBC. Blocks all learner-reachable AWS ingress and every hosted-agentcore claim.
- Verify: `make hosted-authz-test hosted-isolation-test`; rerun `make runner-security-test
  portal-e2e evidence-contracts-check` for the shared trust-boundary blast radius.

## Per-Issue Acceptance Template

Every follow-up issue body must include:

1. Expected files/behavior and explicit out-of-scope.
2. Tests-before characterization and failure fixture.
3. Implementation/refactor steps with exclusive ownership.
4. Tests-after plus blast-radius regression commands.
5. Security/resource/accessibility/recovery evidence as applicable.
6. Migration and rollback from exact input SHA.
7. Machine-readable evidence path and schema version.
8. STOP/TBC conditions and who may clear them.
9. Confirmation that product code, cloud apply, merge, and issue-state transitions remain outside
   the issue unless explicitly authorized.
10. Changed-path deny-list result for root `release-manifest.json`, `docs/code-standards.md`, raw
    discovery history, ignored runtime fixtures, and contracts owned by another active lease.
