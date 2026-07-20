# Local and AWS Architecture View Source Plan

## Principle

Use the minimum view that answers a stakeholder concern. Source lives in Structurizr DSL;
rendered images are derived. No forced code-level view and no decorative duplicate diagrams.
Dynamic views exist only where order, retry, approval, reset or recovery changes the outcome.

## Planned Source Layout

```text
architecture/
  structurizr/
    workspace.dsl
    model/
      people-and-systems.dsl
      learning-platform.dsl
      data-platform.dsl
      aws-platform.dsl
      optional-ai.dsl
    views/
      landscape-and-context.dsl
      local-containers.dsl
      local-runner-components.dsl
      local-deployment.dsl
      local-dynamics.dsl
      aws-containers.dsl
      aws-deployment.dsl
      aws-dynamics.dsl
      optional-ai.dsl
    styles.dsl
    view-manifest.yaml
  rendered/
    <view-id>.svg
    <view-id>.txt
```

`optional-ai.dsl` is excluded from the default workspace until admission; stable placeholder
IDs may exist in the registry, but no active container/module is implied.

## Local Views

| ID | C4/view | Audience / concern | Required elements |
|---|---|---|---|
| C4-L0 | System landscape/capability | Product owner: business outcome/capabilities and external tools | Learner, instructor/operator evolution, learning platform, retail platform, optional AWS/identity |
| C4-L1 | System context | Learner/security/maintainer: trust and ownership | Browser, platform, data tools, hosted identity future, evidence boundary |
| C4-L2-LOCAL | Container | Developer/learner: actual local processes | Portal modular monolith, isolated runner, progress/evidence repository, data adapters, Rill/Airflow/Iceberg/OpenMetadata |
| C4-L3-RUNNER | Component | Security/reviewer: privileged execution | BFF client, transport auth, policy chain, command registry, workspace manager, state/idempotency, verifier/evidence |
| DEP-LOCAL | Deployment | Learner/operator: 16 GiB runtime/trust | Browser/host, loopback/Unix socket, read-only base, workspace/evidence, mutually exclusive Compose profiles |
| DYN-JOURNEY | Dynamic | Learner/product/security: complete first journey | Load lesson, start, run, controlled failure, diagnose, reset, verify, evidence, completion |
| DYN-PUBLISH | Dynamic | Data/operator: partial failure and recovery | dbt/export, object write, catalog commit, ingest, verify, retry/resume/rollback |

Local view exclusions:

- No separate Experience/Process/System/Backend/Technical services; show these as API operation
  ownership annotations.
- No AI container or AWS dependency in the core view.
- External tool UI internals are not modeled.

## AWS Views

| ID | C4/view | Audience / concern | Required elements |
|---|---|---|---|
| C4-L2-AWS | Container | Architecture/security/operations: stateless vs stateful ownership | Ingress, portal/BFF, runner/jobs, ClickHouse, Superset, OpenMetadata, S3/Iceberg catalog, DB/search, evidence/state, schedule workflow |
| DEP-AWS | Deployment | Network/IAM/FinOps: topology and residual cost | Route 53/cert/TLS/LB, VPC/AZ/subnets/routes/egress choice/SG/endpoints, ECS/EC2 ASG/capacity provider, state stores, logs/KMS/secrets/state |
| DYN-OFFICE | Dynamic | Operations/learner: usable office hours | Scheduled open, capacity, registrations, migrations/restore/hydration, health/equivalence, ready; close, block/drain/checkpoint/backup/verify, task/EC2 zero, residual inventory |
| DYN-RESTORE | Dynamic | Reliability/data owner: empty-environment recovery | Restore/register S3/Iceberg catalog, hydrate/restore ClickHouse, restore Superset/OpenMetadata/evidence, rebuild search, equivalence, readiness/RTO/RPO |

TBC values appear explicitly in annotations:

- region default `ap-southeast-1`;
- schedule default weekdays 08:00-18:00 `Asia/Ho_Chi_Minh`;
- monthly budget, retention by data class, cold-start/readiness SLO, production RTO/RPO,
  account/environment and named apply approver `TBC — blocks aws-apply`;
- managed/self-hosted metadata/search and ClickHouse final role remain decision links.

Do not label the AWS deployment “scale to zero” without an adjacent residual-state/cost note.
DEP-AWS must also show the S3/Terraform-state boundary: public-access block, TLS-only, SSE-KMS,
versioning/lockfile, least-privilege role/prefix, retention/lifecycle/restore, account/region/plan
SHA and the human security/apply gates. A diagram never implies those controls are deployed.

## Optional AI Views

Only after Phase 12 admission:

| ID | View | Concern |
|---|---|---|
| C4-L3-AI | Component | ACL policy, retrieval/provenance/eval, graph/workflow, tools/approval, AgentCore adapter, durable state |
| DYN-AI | Dynamic | Retrieve→authorize→cite/evaluate and later approve→tool→retry/reconcile |

The view must show AgentCore Runtime session state as ephemeral and identify the durable
workflow/idempotency/approval owner.

## View Manifest Contract

Each entry in `view-manifest.yaml` contains:

- stable `viewId`, type and source include;
- audience, stakeholder concern and scope;
- related requirement/ASR/ADR/lesson/finding IDs;
- source/tool version;
- expected elements/relationships;
- rendered SVG and structured text alternative paths;
- source/output SHA-256;
- last review evidence and status.

Fitness checks reject missing concerns, orphan elements, stale outputs, missing text alternatives
or a lesson referencing an undeclared view.

## Render and Validation Commands

Future tracked/discoverable commands:

```bash
make architecture-check
make architecture-render
make architecture-visual-review
```

`make architecture-check`:

- runs a pinned Structurizr CLI `validate` against `workspace.dsl`;
- validates the manifest/schema/required view IDs and relation/element references;
- checks every view has audience/concern/traceability/text output;
- checks optional AI views are excluded while admission is false;
- checks logical API taxonomy does not create five physical containers.

`make architecture-render`:

- exports every active view with the pinned CLI;
- generates deterministic SVG plus structured text/table alternatives;
- records source/tool/output hashes in a render manifest;
- fails on stale committed/generated portal assets.

`make architecture-visual-review`:

- renders views in the portal at desktop/mobile/200% and reduced-motion/static modes;
- stores review screenshots/evidence;
- requires a human readability check for labels, legend, contrast and sequence numbering.

Implementation pins the exact CLI/image digest after a compatibility spike. The wrapper commands
remain the stable contract even if vendor CLI syntax changes.

## Acceptance and Rollback

- All required local views validate/render before the first journey release.
- AWS sources may validate with TBC annotations before apply; no diagram is evidence that
  infrastructure exists.
- View IDs remain stable across layout/style changes; intentional rename uses a mapping and link
  migration.
- Rollback restores prior DSL/manifest; rendered assets regenerate. No hand-edited image becomes
  authoritative.
