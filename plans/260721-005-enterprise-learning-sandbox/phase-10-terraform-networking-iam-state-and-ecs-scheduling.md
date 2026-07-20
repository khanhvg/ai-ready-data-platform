---
phase: 10
title: "Terraform Networking IAM State and ECS Scheduling"
status: pending
priority: P1
dependencies: [9]
effort: "L"
---

# Phase 10: Terraform Networking IAM State and ECS Scheduling

<!-- Updated: Validation Session 1 - strengthened backend/S3 security and exact human apply gates. -->

## Overview

Build test-first Terraform modules for backend contract, network, IAM, ECS on EC2 capacity and
office-hours readiness/drain orchestration. Validate and produce non-applying plans only. No
backend bootstrap, account mutation or Terraform apply is authorized.

## Context Links

- Accepted/parameterized outputs from Phase 9
- AWS deployment and office-hours views
- Source register S07/S08/S17/S18
- PH-C09, PH-H07/H08 and SC-13/17

## Requirements

- Separate bootstrap-state configuration from workload stacks. Backend contract requires S3
  public-access block, `BucketOwnerEnforced`, an `aws:SecureTransport=false` deny, SSE-KMS,
  versioning, Terraform S3 backend `use_lockfile = true`, least-privilege key-prefix actions,
  logging/monitoring, retention/deletion and previous-version restore. DynamoDB locking is not a
  new dependency. Never VCS/local-state production or static credentials.
- Configurable two-AZ VPC, subnet/route/egress mode, security groups, DNS/TLS/ingress and endpoints
  without silently accepting NAT/public exposure cost.
- ECS cluster with new empty ASG capacity provider, replaceable EC2, task/service roles, logs and
  budgets/alarms. Durable state is not instance-local by implication.
- Office-hours workflow schedules demand but declares ready only after dependencies,
  migration/restore/hydration and portal/data/dashboard/catalog health checks.
- Close workflow blocks new labs, drains/checkpoints/backups, verifies recovery artifact, stops
  schedulers/services, drives tasks/ASG to zero and inventories residual resources.
- Wrong account/region/environment/SHA/role and placeholder secret/public ingress must fail.
- Before I5-14, any future validation environment is private operator-only; learner-reachable
  ingress is mechanically denied.
- Any future apply requires all six TBC groups resolved, Security approval of S3/IAM, and the
  named apply approver bound to the single-use saved-plan authorization envelope in the normative
  execution contract. This phase provides policy tests only and cannot clear that gate.
- No default target, CI workflow or documented command may call `apply` or `destroy`.
- Async/event services exist only if needed by the readiness workflow, not curriculum symmetry.

## Architecture

Likely modules:

```text
bootstrap-state-contract (files only, not applied)
network -> security/ingress/endpoints
iam -> ECS instance/task/plan/apply/readiness roles
ecs-capacity -> launch template/ASG/capacity provider/cluster
ecs-services -> replaceable portal/runner/jobs adapters
office-hours -> EventBridge Scheduler + observable state workflow
observability-budget -> logs/metrics/alarms/tags/residual inventory
persistence -> selected S3/catalog/metadata-db/search/portal-state/secrets/KMS/backup resources
```

Step Functions with minimal Lambda/ECS control tasks is the leading readiness implementation
because wait/retry/drain/checkpoint states require observable sequencing; reject it if Phase 9
shows a smaller construct satisfies the same tests.

## File Inventory

| Action | Planned path | Rough size | Test impact |
|---|---|---:|---|
| Create | `infra/aws/terraform/bootstrap-state/**` | 150-250 lines | Contract/mocks only |
| Create | `infra/aws/terraform/modules/{network,iam,ecs-capacity,ecs-services,office-hours,observability-budget,data-lake,catalog,metadata-db,search,portal-state,secrets,backup-recovery}/**` as admitted by P9 | 2,800-4,200 lines | Every accepted state row has a Terraform owner/test |
| Create | `infra/aws/terraform/environments/sandbox/**` | 500-800 lines | Composition/no secrets |
| Create | `infra/aws/terraform/tests/**.tftest.hcl` | 800-1,200 lines | Mock provider/plan assertions |
| Create | `infra/aws/policy/{terraform,iam,network,cost}/**` | 500-800 lines | Conftest/security |
| Create | `scripts/aws/{terraform-check,terraform-validate-offline,terraform-test-mocked}.sh` | 180-300 LOC | Clearly separated non-applying orchestration |
| Create/modify | `mk/issue-5/i5-10.mk`, `.gitignore`, docs | 80-150 lines | Safe targets/state/plan ignores via root include |

## Interface Checklist

- [ ] environment/account/region/input-SHA precondition
- [ ] backend bucket/key/KMS/lockfile variables with no secret values
- [ ] network egress mode and explicit cost/security output
- [ ] least-privilege role/policy documents and permissions boundaries
- [ ] office workflow inputs/state/readiness/drain/override outputs
- [ ] task/service health and residual-resource inventory contract
- [ ] outputs consumed by Phase 11 without circular state ownership
- [ ] every accepted P9 persistence/key/backup row maps to one module/resource or explicit
  rejected topology; no adapter-owned Terraform
- [ ] single-use saved-plan envelope binds plan/config/lock/vars/backend-state/identity/expiry

## Dependency Map

- Depends on Phase 9 decision schemas/interfaces; unresolved thresholds remain variables/apply
  preconditions.
- May run in parallel with Phase 11 after interface freeze.
- Apply remains blocked by owner TBCs and separate authorization.

## Test Scenario Matrix

| Priority | Scenario | Expected |
|---|---|---|
| Critical | Wrong account/region/workspace/SHA/role | Plan/precondition denial |
| Critical | Concurrent backend operation/approval replay | Lock/identity policy denial (mock; real later) |
| Critical | Saved plan or any bound input changes after approval | Authorization invalid; no replan/apply |
| Critical | Secret/static credential/state/plan committed | Security/secret check fails |
| High | Broad ingress/public runner/NAT hidden | Policy/cost check fails |
| High | Schedule sets count but health/hydration fails | Not ready; no learner admission |
| High | Close with active lab/failed backup | Drain waits/cancels close; override audited |
| High | EC2 zero but residual resources unreported | Inventory/cost test fails |
| High | Module gains apply/destroy default | Command-policy test fails |

## Tests Before

Write `terraform test` mock cases and policy fixtures for wrong identity, broad IAM/ingress,
missing encryption/version/lock, unsafe schedule and hidden residual cost. Assert there is no
apply target.

## Refactor

No existing Terraform exists. Keep modules small and compose through explicit outputs; do not
introduce a platform framework.

## Tests After

Run fmt/validate/tflint/security/policy and explicitly labelled mocked tests. Offline validation is
not a Terraform plan or provider-compatibility claim. Later real plan/lock/restore checks require
explicit credentials/account approval and still do not apply.

## Regression Gate

```bash
make terraform-check
make terraform-validate-offline
make terraform-test-mocked
make aws-decision-check
git diff --check
```

The optional `make terraform-plan-aws` command must verify account/role/environment and emit a
redacted plan; it is not run in this planning issue.

## Implementation Steps

1. Pin Terraform/provider/tool versions and write failing mock/policy tests.
2. Add state-backend contract/examples without creating the backend.
3. Implement network/egress and IAM modules with explicit preconditions.
4. Implement ECS EC2 capacity/services modules.
5. Implement office open/readiness and close/drain/checkpoint state workflow.
6. Add observability/budget/residual-inventory outputs and policies.
7. Run only static/offline/mock gates and document future real-plan/apply authority.

## Success Criteria

- [ ] All modules format/validate/lint/security/policy/mocked-test clean; evidence never labels a
  mocked result a real plan.
- [ ] Network/IAM/state/ECS schedule requirements are explicit and testable.
- [ ] Readiness/drain—not desired count alone—drives office availability.
- [ ] No apply/destroy or cloud creation occurs; unresolved owner gates block them mechanically.
- [ ] Phase 11 can consume stable outputs without assuming state topology.

## Risk, Security, and Rollback

Terraform plan/state can disclose secrets and wrong-account changes. Keep plans ignored/redacted,
roles separate and identity preconditions mandatory. Rollback removes un-applied modules; if a
future authorized environment exists, its separate runbook/state governs rollback.

## Next Steps

Feed outputs into Phase 11 adapter task definitions/config while retaining the no-apply boundary.
