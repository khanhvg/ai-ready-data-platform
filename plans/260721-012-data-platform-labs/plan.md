---
title: "I5-07 — Data-platform guided labs without golden semantic drift"
description: "Kế hoạch TDD theo ba stage cho guided labs data-platform, khóa chặt Issue #6 và chỉ tích hợp khi #8, #9, #10 có release SHA chính xác."
status: pending
priority: P1
issue: 12
branch: "plan/issue-12-data-labs"
tags: [issue-5, i5-07, data-platform, tdd, security-s3, recovery, labs]
blockedBy: []
blocks: []
created: "2026-07-22"
createdBy: "ck:plan"
source: skill
planningMode: "deep-tdd-planner-only"
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
dependencyIssue8ReleaseSha: ""
dependencyIssue9ReleaseSha: ""
dependencyIssue10MergeSha: ""
currentImplementationPaths: []
currentImplementationCommands: []
---

# I5-07 — Data-platform guided labs without golden semantic drift

## Tổng quan

Lập kế hoạch Vietnamese-first từ foundation đến mid cho các lab data-platform có thao tác thật,
lỗi có kiểm soát, xác minh, evidence và reset. Kế hoạch bảo vệ tuyệt đối semantic golden của
Issue #6 tại input SHA `24be3b34c6b0fcdbd07c5800dcab349054e34713`; không coi label/plan/branch mở
của #8, #9 hoặc #10 là release có thể tiêu thụ.

Đây là artifact **planner-only**. Không lab, verifier, pipeline seam, registry, API, renderer,
Make target hay portal integration nào được triển khai hoặc xác nhận runnable trong phase này.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Dependency Amendment and Immutable Characterization](./phase-01-dependency-amendment-and-immutable-characterization.md) | Pending |
| 2 | [Stage A Contract-Bound Foundation Labs](./phase-02-stage-a-contract-bound-foundation-labs.md) | Pending |
| 3 | [Stage B Local Runner and Data Fault Exercises](./phase-03-stage-b-local-runner-and-data-fault-exercises.md) | Pending |
| 4 | [Stage C Portal Publication and Real Journey](./phase-04-stage-c-portal-publication-and-real-journey.md) | Pending |
| 5 | [Release Evidence Recovery and Human Handoff](./phase-05-release-evidence-recovery-and-human-handoff.md) | Pending |

## Stage gates

| Stage | Dependency bắt buộc | Phạm vi sớm nhất | Claim tối đa |
|---|---|---|---|
| A | Exact released Issue #8 learning contracts | Nội dung lab + ứng viên verifier không mutate; chỉ đọc fixture/reader Issue #6 | Contract-bound candidate; không runnable |
| B | Exact released Issue #9 runner + lease data-contract/pipeline riêng, hẹp, được ghi nhận | Local runner/pipeline exercises, fault/recovery seams | Local exercise evidence; không browser/portal completion |
| C | Passing merged Issue #10 real journey/renderer | Publication, renderer/API integration và real-journey E2E | Stage duy nhất được claim complete learner experience |

Mỗi stage cần amendment mới ghi exact SHA, dependency paths/commands, compatibility evidence,
independent revalidation và readiness trước cook. Resolution fields hiện tại phải tiếp tục rỗng
cho đến amendment đó; xem [dependency and authority register](./dependency-and-authority-register.md).

## Phạm vi học tập

1. `small`, seed `42`: deterministic ingest, model, quality, grain và truth bất biến.
2. Airflow local operators: retry, idempotency, timeout, backpressure; browser không có quyền
   thực thi đặc quyền.
3. Weighted/additive metric đúng và controlled failure average-of-averages sai.
4. Atomic curated release đúng 11 assets: manifest/hash/pointer all-or-none và crash recovery.
5. Iceberg commit/snapshot/conflict/orphan recovery trên semantics object store/catalog cục bộ đã
   được compatibility-test thật.
6. OpenMetadata reconciliation theo namespace/FQN chính xác: create/update/delete policy
   idempotent, không prefix collision, không broad delete.
7. Mọi service/pattern phải trỏ tới failure, quality attribute và evidence cụ thể; không pattern
   theater.

Mỗi lab bắt buộc có: prerequisite checks, starter, task, controlled failure, progressive hints,
verify, immutable evidence, reset, gated solution và reflection. Reflection/hint/solution không
được tự nâng completion.

## Ranh giới authority

- Được ghi sau gate phù hợp: `learning/labs/data-platform/**`, data-lab verifiers theo path do
  released contracts quy định, lease data-contract/pipeline đã serialize, và
  `mk/issue-5/i5-07.mk`.
- Chỉ đọc: contracts/data/views/fixtures/readers Issue #6 và toàn bộ golden semantics.
- Bảo vệ: root `Makefile`, `release-manifest.json`, `docs/code-standards.md`, shared contracts,
  architecture views, portal, runner và pipeline ngoài lease chính xác.
- Không AWS/Terraform apply/destroy, cloud resource, destructive migration, PR hoặc merge.

## TDD và release contract

- Characterization hiện tại phải pass trước mutation: generator/warnings/marts/lineage/Rill,
  curated assets, publisher gap, catalog behavior và fixture hashes.
- Mỗi thay đổi bắt đầu bằng RED gắn hành vi cụ thể; cấm unconditional RED, expected-code echo,
  fake fixture hoặc mock thay cho object store/catalog thật.
- Regression IDs và evidence contract nằm trong
  [test and evidence strategy](./test-and-evidence-strategy.md).
- Additive migration, reader cũ, atomic rollback và cleanup chỉ run-owned bytes là bắt buộc; xem
  [data architecture and recovery](./data-architecture-and-recovery.md).

## Final verify contract

Sau khi mọi dependency release được amendment và Stage C hoàn tất:

```bash
make data-labs-e2e lake-fault-test metadata-reconcile-test data-contracts-check
```

Phải chạy thêm blast radius chính xác do released #6/#8/#9/#10 công bố. Core chạy serial trên
16GB, không yêu cầu Docker/cloud. Service tùy chọn vắng mặt phải trả trạng thái trung thực và
không được dùng để claim lab service-backed đã pass.

## Acceptance

- [ ] Trace requirements/risk/threat/data architecture/test/evidence/recovery không có lỗ hổng.
- [ ] Ba dependency SHA, current implementation paths và current implementation commands vẫn rỗng
      trong planner output.
- [ ] Stage A/B/C có STOP, independent revalidation và readiness gate riêng.
- [ ] Stable test IDs bao phủ ingest/model/quality, orchestration, metrics, 11-asset atomicity,
      Iceberg, OpenMetadata, evidence và protected semantics.
- [ ] Human exact-head pre-merge approval bắt buộc; approval của SHA khác không chuyển tiếp.

## Companion artifacts

- [Dependency and authority register](./dependency-and-authority-register.md)
- [Requirements traceability](./requirements-traceability.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Protected baseline manifest](./protected-baseline-manifest.md)

## Open questions

None. Dependency outputs are unresolved gates, not planner assumptions.
