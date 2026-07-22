---
type: local-container-platform-readiness-audit
issue: 9
date: "2026-07-22"
status: ready-to-cook
verdict: READY_TO_COOK
startHead: "4774c711208ef9cb7050b72c88106dffc7016f04"
releasedStageASha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
backend: "local-rootless-container-pid-namespace"
operationFeasibility: "8/8-planned"
cookScope: whole-plan
securityS3: PASS
resourceBudget: PASS
ownershipOverlap: PASS
cloudAction: none
containerAction: none
---

# Local Container Platform Readiness Audit — Issue #9

## Verdict

`READY_TO_COOK`; `COOK_SCOPE=whole-plan`; no unresolved owner choice.

The owner-authorized local Docker-compatible PID-namespace backend is fit for purpose and narrower
than weakening the proven 7/8 host strategy. The stopped engine is a fail-closed local
prerequisite. Because the Docker CLI and OrbStack app are installed, engine absence does not block
planning; cook may start the app only through the separately recorded local-side-effect gate and
must stop on admin or TCC interaction.

## Readiness Matrix

| Gate | Result | Cook consequence |
|---|---|---|
| One backend for all eight operations | PASS planned | Prove 8/8 for real; dbtRunner tracker stays in namespace |
| PID lifecycle authority | PASS specified | Init/subreaper plus cgroup and stop/KILL/wait/remove; polling evidence only |
| Container policy | PASS specified | Any ignored/unobservable field is RUNNER_CONTAINMENT_UNAVAILABLE |
| Host/API trust boundary | PASS | Owner UDS/random loopback, strict Host/Origin/bearer/CSRF; browser never Docker |
| Supply chain | PASS | Observe base/image digests; offline hashed wheels; SBOM/provenance/license/CVE closure; no push |
| Resource budget | PASS | One active runner, aggregate 512 MiB zero-swap, 2 CPUs, 64 PIDs, 6 GiB host reserves |
| TDD and adversarial catalog | PASS | Fixed no-argument 52-RED/14-S3 shard harness before production behavior |
| State/evidence/release | PASS | CAS, fences, idempotency, hash-chain audit, rollback, atomic eleven assets |
| Runtime state hygiene | PASS | App-owned exact ignore rule and ignored-baseline delta; root ignore unchanged |
| Issue #13 overlap | PASS | Issue #9 owns runner internals/i5-04; Issue #13 consumes release in profiles only |
| Engine discovery | PREREQUISITE | Docker 29.4.0 and OrbStack 2.2.1 present; engine stopped/socket absent |
| Cloud/container action during amendment | NONE | No AWS, Terraform, Kubernetes, image or container action |

## Ownership and Reuse

Issue #9 cook may write only `apps/lab-runner/**` and `mk/issue-5/i5-04.mk`. Root Make,
docker-compose.yml, profile/Compose files, Airflow, shared contracts, golden source, portal, cloud,
Terraform and Kubernetes paths remain denied. Issue #13 at plan head
`4a5ad724c94a606e0708064a536870f124ab8a2f` owns downstream profiles and may consume only the
released image identity and launcher; it cannot duplicate or modify runner internals.

The existing Airflow image/Compose stack is not reused as the runner base because its tag-only
base, online install, network/ports, credentials and writable repository mount conflict with the
runner boundary. Reuse is limited to exact read-only released semantic inputs, golden helpers and
the existing root Make wildcard.

## Whole-Plan Cook Gate

The six phases execute in order. Cook stops on a non-descendant or dirty input head, missing
engine/tool/digest, predicted digest, admin/TCC prompt, unclosed license or Critical/High advisory,
runtime pull/install, ignored containment field, container residue, resource/reserve breach,
operation result below 8/8, golden drift, evidence gap, ownership overlap or any unresolved
Critical/High review finding. No partial operation cook, host fallback or scope cut is authorized.

Only after real all-eight, adversarial, supply-chain, resource, rollback and exact-head review
evidence passes may cook write the measured runner image release record. A future implementation
head, image digest, PR, merge and human approval are deliberately not predicted or approved here.
