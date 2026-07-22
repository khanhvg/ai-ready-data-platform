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
plannerInputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
initialValidationInputSha: "24ff21db72e0d08d34b62c3280e76ab6329665eb"
goldenAuthoritySha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
dependencyIssue8ReleaseSha: ""
dependencyIssue9ReleaseSha: ""
dependencyIssue10MergeSha: ""
currentImplementationPaths: []
currentImplementationCommands: []
---

# I5-07 — Data-platform guided labs without golden semantic drift

## Tổng quan

Lập kế hoạch Vietnamese-first từ foundation đến mid cho các lab data-platform có thao tác thật,
lỗi có kiểm soát, xác minh, evidence và reset; output cuối không được là docs dump. Kế hoạch bảo
vệ tuyệt đối semantic golden của Issue #6 tại authority SHA
`24be3b34c6b0fcdbd07c5800dcab349054e34713`. Initial validation bắt đầu từ plan-only child
`24ff21db72e0d08d34b62c3280e76ab6329665eb`; không coi label/plan/branch mở của #8, #9 hoặc #10
là release có thể tiêu thụ.

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
- Chỉ đọc: contracts/data/views/fixtures/readers Issue #6 và toàn bộ golden semantics; released
  completion/evidence authority của #8, private runner authority của #9 và renderer/API authority
  của #10. Không copy schema, tạo parallel registry, duplicate truth hoặc invented adapter.
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
- Mỗi stage chỉ được handoff sau khi exact tested head chạy từ pristine detached checkout không có
  generated/runtime artifact ẩn; observability phải bind run/operation/fault/resource/result vào
  evidence đã redact; docs/release impact phải ghi `none` hoặc exact owner/path/gate, không tự sửa
  protected `release-manifest.json` hay `docs/code-standards.md`.

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
      Iceberg, OpenMetadata, evidence, exact six-view oracle và protected semantics.
- [ ] Pristine-checkout, observability và docs/release-impact gates có stable IDs và evidence.
- [ ] Human exact-head pre-merge approval bắt buộc; approval của SHA khác không chuyển tiếp.

## Companion artifacts

- [Dependency and authority register](./dependency-and-authority-register.md)
- [Requirements traceability](./requirements-traceability.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Protected baseline manifest](./protected-baseline-manifest.md)
- [Independent initial validation report](./validation/initial-validation-report.md)

## Open questions

None. Dependency outputs are unresolved gates, not planner assumptions.

## Validation Log

### Session 1 — 2026-07-22

**Trigger:** Fresh independent `$ck:plan validate` at exact plan head
`24ff21db72e0d08d34b62c3280e76ab6329665eb` against the user-supplied ten-part adversarial
contract.

**Questions asked:** 0. The exact user contract supplied all binding decisions; dependency
outputs remain unresolved gates rather than questions to guess.

### Verification Results

- **Tier:** Full — Fact Checker, Flow Tracer, Scope Auditor and Contract Verifier.
- **Claims checked:** 86.
- **Verified:** 86 | **Failed:** 0 | **Unverified:** 0 after bounded plan-only fixes.
- **Initial objective defect families fixed:** 7.
- **Report:** [Initial independent validation](./validation/initial-validation-report.md).

### Confirmed Decisions

- Planner/product input and immutable Issue #6 authority are
  `24be3b34c6b0fcdbd07c5800dcab349054e34713`; initial validation input is the separate plan-only
  child `24ff21db72e0d08d34b62c3280e76ab6329665eb`.
- Stage A/B/C dependency authority remains empty and fail-closed.
- No current schema/path/command/runner/renderer authority was inferred from future declarations.
- Stage A cannot claim runnable completion; Stage B cannot claim portal completion; Stage C alone
  may claim the real learner journey after exact merged #10 authority.
- Exact six-view semantics, special files, per-behavior TDD sequence and fresh exact-head
  implementation review are release blockers.

### Impact on Phases

- Phase 1: separated validation input from golden authority and added six-view characterization.
- Phase 2: added learner-action/expected-actual and no-docs-dump criteria.
- Phase 3: unchanged authority; its S3/TDD companion contracts were strengthened.
- Phase 4: unchanged authority and Stage C-only completion boundary.
- Phase 5: fresh implementation/security review now has stable ID `DL-REV-001`.

### Whole-Plan Consistency Sweep

- Files reread: `plan.md`, all five phase files and all six companion plan artifacts.
- Decision deltas checked: 7.
- Reconciled stale/implicit references: 19.
- Unresolved contradictions: 0.
- Recommendation: pass initial validation with fixes; do not cook. Move to plan audit, then run a
  fresh dependency-aware readiness audit that remains blocked until exact releases/lease exist.

## Readiness Audit Log

### Fresh dependency-aware audit — 2026-07-22

- Exact audit input: `975e7c93fbe2cbdb883ca8b28e1635cdd69f460c`.
- Verdict: `BLOCKED_DEPENDENCIES`; implementation authority remains `none`.
- Bounded plan fixes: added explicit pristine-checkout, observability and docs/release-impact
  trace/gates without resolving any dependency-derived field.
- Report: [Fresh readiness audit](./audit/readiness-audit-report.md).
- Next legal phase: wait for exact dependency releases/lease, then amend only the eligible stage
  and run fresh independent revalidation plus readiness audit.
