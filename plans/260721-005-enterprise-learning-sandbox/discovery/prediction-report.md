# Prediction Report: Enterprise Architecture Learning Sandbox

## Method

Applied `ck:predict` to the complete issue #5 body and intake comment, the input repository at
`9bcacd7a44a33d298388dca2a8d2b398c6bb22a8`, issue #3, PR #4, historical verification evidence,
and the source register. Architect, Security, Performance, UX and Devil's Advocate assessments
were produced independently before conflicts were reconciled.

## Verdict: STOP

**STOP applies to implementation, destructive migration and cloud provisioning.** Discovery is
complete and may proceed to a fresh planner only if the planner treats the STOP conditions below
as blocking decisions/gates. The repository has a strong preservation baseline, but the proposal
does not yet own state, recovery, cost, trust boundaries or an immutable input baseline well
enough to authorize implementation.

## Independent Persona Assessments

### Architect

- **Position:** preserve and layer. Issue #3 already supplies a coherent data spine with explicit
  source, transform, serving, lake and governance seams. Add portal and AWS bounded contexts; do
  not rebuild the whole repository.
- **Critical concern:** “ECS on EC2 scales to zero” is a compute statement, not an architecture for
  ClickHouse data, Superset/OpenMetadata metadata, search indexes or the Iceberg catalog. Each
  owner, recovery path and RTO/RPO must be explicit.
- **Critical concern:** PR #4 is the actual base but remains unmerged and unprotected by CI.
- **High concern:** the issue lists a broad curriculum, many patterns and multiple agent
  frameworks without defining the smallest first journey or extraction criteria. A modular
  monolith portal plus lab-runner boundary is the safer starting point.
- **Recommendation:** freeze the golden SHA; treat S3/Iceberg as durable data truth; decide whether
  ClickHouse is durable or a rebuildable projection; isolate lesson content, lab execution,
  progress/evidence and integrations behind contracts.

### Security

- **Position:** core learning must remain credential-free and locally bound; AWS and agent labs
  need separate trust zones and identities.
- **Critical concern:** learner-triggered shell/dbt/Terraform/agent tools can become arbitrary code
  execution, credential theft, cross-learner data access or destructive cloud action if the portal
  passes untrusted parameters into the current Make/subprocess surface.
- **Critical concern:** governed RAG requires ACL propagation at retrieval and generation time,
  not just a catalog label; traces/citations can leak source content, tokens and PII.
- **Critical concern:** Terraform state and plans can contain secrets; “no apply during planning”
  is necessary but insufficient without isolated state, least privilege and environment gates.
- **High concern:** local Compose exposes several ports and development-only credentials; Airflow
  mounts the repository root read-write.
- **Recommendation:** define actors/resources/actions, tenant/workspace isolation, command
  allow-lists, localhost-only exposure, secret redaction, trace retention and human approval before
  tool side effects.

### Performance

- **Position:** profiles and the local core are a good foundation, but stack count must not become
  the curriculum's performance model.
- **Critical concern:** declared Compose `mem_limit` values are not a 16 GiB budget. Docker Desktop,
  the browser/portal, host tools and cold starts are unmeasured. Lake+governance already declares
  7.25 GiB before overhead.
- **High concern:** a disposable ClickHouse can make office-hours startup slow; a durable
  ClickHouse on replaceable EC2 can make recovery brittle. This is an explicit latency-versus-
  persistence decision.
- **High concern:** Superset, OpenMetadata and portal cold starts can leave scheduled services
  nominally “up” but unusable during a lesson. Readiness must be the schedule outcome.
- **High concern:** agents, retrying APIs and orchestration can amplify duplicate work and spend.
- **Recommendation:** measure per-profile RSS/CPU/disk/start time, bound data sizes and concurrency,
  make retries idempotent, and record cost/latency evidence for cold and warm paths.

### UX

- **Position:** the first vertical slice must be one complete hands-on journey, not a content shell
  or a dashboard of disconnected tools.
- **Critical concern:** a novice can misread a failing dependency, controlled fault or stale
  environment as their own failure. Every step needs prerequisites, current state, safe reset,
  verify evidence and a useful next action.
- **High concern:** external UIs (Rill, Airflow, OpenMetadata, Superset) fragment navigation and use
  different terminology. The portal needs deep links and a shared evidence vocabulary rather than
  attempting to clone all UIs.
- **High concern:** scroll-linked motion can harm keyboard, screen-reader and reduced-motion users;
  progress tied only to scroll is not learning progress.
- **High concern:** foundation/junior and mid-level learners need progressive disclosure, but the
  issue does not define personas, completion evidence or remediation paths.
- **Recommendation:** adopt the referenced site's reversible journey/evidence patterns, add real
  labs and durable progress, provide reduced-motion/static equivalents, and make reset/verify
  primary controls.

### Devil's Advocate

- **Position:** the issue risks becoming a technology museum. Most named patterns and services do
  not belong in the first implementation wave.
- **Critical concern:** the assumption that one sandbox should teach enterprise architecture,
  networking, application patterns, data platforms and agents may be false unless a single
  business narrative and competency dependency graph constrain it.
- **High concern:** replacing Rill locally with Superset merely for stack convergence increases
  laptop cost and discards verified assets; running both without distinct learning objectives is
  equally wasteful.
- **High concern:** “required AgentCore” can force credentials, spend and immature service coupling
  into a core path that expressly says AI is optional.
- **Recommendation:** deliver a thin portal over the preserved golden pipeline first. Admit each
  pattern/service only when a lesson has a failure it solves and evidence that verifies it.

## Agreements

All five personas align on these points:

1. A full repository rewrite is unjustified. Preserve the deterministic generator, dbt graph,
   Rill/Iceberg allow-list, Airflow flow and OpenMetadata adapters as golden assets.
2. PR #4's exact SHA must be made immutable or merged before implementation branches diverge.
3. The first vertical slice must complete one business journey from lesson to controlled failure,
   reset, verify and evidence on a 16 GiB laptop without AWS credentials.
4. Local and AWS deployments share learning contracts, not identical components or topology.
5. Every stateful component needs an owner, durable store, backup, restore test, RTO/RPO and
   scale-to-zero behavior.
6. AI/AgentCore remains an optional admission-gated add-on on governed data products.
7. Cost, security, accessibility and recovery are executable acceptance criteria, not prose.

## Conflicts and Resolutions

| Topic | Architect | Security | Performance | UX | Devil's Advocate | Resolution |
|---|---|---|---|---|---|---|
| Preserve vs rebuild | Layer on golden spine | Preserve verified boundaries; harden execution | Reuse measured local path | Preserve familiar data story | Rewrite adds risk without learner value | **Preserve + selective refactor.** New portal/AWS directories are greenfield; core behavior changes need characterization tests and rollback. |
| Local BI | Rill is a valid local adapter | Smaller exposed surface is preferable | Rill is already lighter/proven | One portal vocabulary matters more than one engine | Convergence is not a goal | **Keep Rill as default candidate.** Spike Superset locally only against measured learning value, RSS and reset time; Superset remains AWS requirement. |
| ClickHouse persistence | Make state ownership explicit | Backups and IAM boundaries required | Disposable rebuild may simplify scale-to-zero | Learners need predictable startup | A stateful singleton on ASG may be needless complexity | **Decision required.** Preferred input is disposable serving projection rebuilt from S3/Iceberg; reject until rebuild SLA and evidence pass. Durable alternative needs stable volume topology and restore test. |
| OpenMetadata/Superset state | Managed durable dependencies simplify compute replacement | Managed IAM/encryption/backup reduce risk | Managed services create idle cost | Faster reliable startup improves labs | Residual cost may defeat office-hours premise | **Human cost/recovery choice.** Price managed RDS/search versus self-hosted persistent dependencies; never claim full scale-to-zero while either incurs cost. |
| Web stack | Modular monolith first | Separate privileged lab-runner boundary | Prefer small static shell where possible | Needs rich state, MDX, a11y and E2E | Avoid framework-first planning | **Prototype gate.** Compare Astro+islands, Next.js runtime/static split, and React/Vite + separate API using one lesson contract and measured criteria. |
| AgentCore | Useful AWS deployment target | Strong identity/gateway/policy potential | Consumption spend and cold paths must be bounded | Valuable only after core journey works | Optional means it can be deferred | **Admission gate.** No AgentCore wave until governed retrieval, evaluation, OTel, approvals, idempotency, cost and credential-optional core are proven. |

## Critical Risks and STOP Conditions

| ID | Critical risk | STOP condition that must be resolved | Evidence needed to clear |
|---|---|---|---|
| C1 | Moving/unmerged golden baseline | PR #4 merge strategy or immutable input tag/SHA approved | Clean-checkout golden run at the accepted SHA; branch graph recorded in every implementation issue |
| C2 | Undefined AWS state/system of record | ClickHouse role plus state owner for Superset, OpenMetadata, search and Iceberg catalog approved | State matrix, failure-mode test, backup and restore demonstration, declared RTO/RPO |
| C3 | Misleading scale-to-zero/cost claim | Monthly budget, region, office hours and residual services approved | Priced bill of materials with compute-zero and active-hour scenarios; cost alarms and teardown test |
| C4 | Privileged lab execution boundary absent | Learner/workspace/authz/command/secret model approved | Threat model; negative authorization tests; isolated workspace reset; no arbitrary Terraform/shell path |
| C5 | Destructive or concurrent reset/publish corrupts state | Lab state machine and idempotency/locking contract approved | Race/fault tests proving reset, publish and verify recover without silent loss |
| C6 | RAG/agent leaks data or causes duplicate side effects | ACL/provenance/approval/idempotency and trace-redaction contracts approved | Cross-user retrieval denial, citation provenance, PII redaction, replay/recovery tests |
| C7 | No executable clean-checkout golden baseline | One bounded, credential-free command and evidence schema approved | Two clean reruns with exact hashes/counts and no reliance on ignored pre-existing files |
| C8 | Curriculum breadth has no invariant learner journey | First business narrative, personas and competency prerequisites approved | One accessible end-to-end lesson/lab satisfying the standard contract and deterministic verification |

## High Risks and Required Decisions

| ID | High risk | Required decision or mitigation |
|---|---|---|
| H1 | Local profile exceeds usable laptop budget | Define measured RSS/CPU/disk/start thresholds including Docker Desktop, portal and browser; enforce mutual exclusion. |
| H2 | Dependency/version drift | Lock environments; key rebuilds to lock hashes; run compatibility spikes for current OpenMetadata, Lakekeeper, Airflow, dbt, Rill/Superset and Iceberg clients. |
| H3 | Stale OpenMetadata entities after model removal | Add reconciliation or resettable per-lab catalog; test rename/delete and rollback. |
| H4 | Non-atomic Iceberg publish | Teach and test staged/snapshot-based publication or guarantee rebuild/rollback; fail loud on partial state. |
| H5 | Fragmented external-tool UX | Portal owns status/evidence/deep-link vocabulary; external tools remain specialized inspectors. |
| H6 | Scroll/animation excludes learners | Keyboard, screen reader, zoom, reduced-motion and static narrative equivalents are acceptance gates. |
| H7 | Scheduled service is not ready at office start | Schedule readiness workflow, not only desired counts; surface partial startup and recovery. |
| H8 | Terraform state/plan exposure | Remote encrypted versioned locked state; environment isolation; least privilege; redact plans; no implicit apply. |
| H9 | Agent retries create duplicate spend/actions | Budgets, timeouts, idempotency keys, approval boundaries and deterministic recovery scenarios. |
| H10 | Local placeholder auth leaks into AWS | Separate dev and cloud config schemas; reject placeholder values and public port exposure in AWS validation. |

## GO Conditions for the Fresh Planner

The planner may begin architecture/roadmap work when it explicitly carries C1-C8 as gates and
does not silently choose unresolved business trade-offs. Implementation remains STOP until:

- the exact golden base and migration rollback are approved;
- the AWS state/cost decision and ClickHouse role are approved;
- the privileged lab-runner and learner identity model are approved;
- the first journey, local budget and verification contract are approved;
- no Terraform apply, cloud resource creation or issue state change is implied by planning.

## Unresolved Human Decisions

1. PR #4 disposition and immutable baseline mechanism.
2. Monthly AWS residual-cost ceiling, target region, office-hours window and acceptable cold start.
3. ClickHouse as durable warehouse versus disposable serving projection.
4. Managed RDS/search/catalog costs versus self-managed persistence/recovery learning burden.
5. Learner identity model: single-user local only, multi-user hosted, or staged evolution.
6. First business narrative and the minimum competencies it must assess.
7. Web-stack prototype winner after measured comparison.
