---
title: I5-07 — Data-platform guided labs without golden semantic drift
description: >-
  Stage A đã merge; Stage B đã resolve runner/lease nhưng bị chặn bởi
  reset-rerun recovery; Stage C chờ Issue #10 Stage B.
status: pending
priority: P1
issue: 12
branch: plan/issue-12-data-labs
tags:
  - issue-5
  - i5-07
  - data-platform
  - tdd
  - security-s3
  - recovery
  - labs
blockedBy: []
blocks: []
created: '2026-07-22'
createdBy: 'ck:plan'
source: skill
planningMode: deep-tdd-planner-only
deliveryLane: standard-lean
cookScope: none
plannerInputSha: 24be3b34c6b0fcdbd07c5800dcab349054e34713
initialValidationInputSha: 24ff21db72e0d08d34b62c3280e76ab6329665eb
goldenAuthoritySha: 24be3b34c6b0fcdbd07c5800dcab349054e34713
dependencyIssue8ReleaseSha: 5644f01b4c0443a81f3af0bcce80f44c847cd986
dependencyIssue9ReleaseSha: 671201f78024786a9f2eba5e9e5fce7c78b4443d
dependencyIssue9ReviewedHeadSha: 86a6c259ad384591777cf1d46f2f6c9ea6327361
dependencyIssue10StageAMergeSha: 041d4ca866e927a331e159fdf8216838b481a595
dependencyIssue10StageBMergeSha: ''
stageAImplementationBaseSha: 041d4ca866e927a331e159fdf8216838b481a595
stageAMergeSha: 8ffbd420aed8dee6f5b4b0fb6d3734e094200a87
stageAReviewedHeadSha: 941307931b29ef8c1a75b0f75afe480690fa8424
stageBImplementationBaseSha: 8ffbd420aed8dee6f5b4b0fb6d3734e094200a87
stageAPathCount: 10
stageACommandCount: 12
stageBPathCount: 12
stageBCommandCount: 16
runnerOperationCount: 8
stageAImplementationPaths:
  - learning/labs/data-platform/deterministic-ingest/lab-v1.json
  - learning/labs/data-platform/deterministic-ingest/content.vi.md
  - learning/labs/data-platform/model-quality/lab-v1.json
  - learning/labs/data-platform/model-quality/content.vi.md
  - learning/labs/data-platform/weighted-metrics/lab-v1.json
  - learning/labs/data-platform/weighted-metrics/content.vi.md
  - learning/labs/data-platform/verify_stage_a.py
  - learning/labs/data-platform/tests/test_stage_a.py
  - learning/labs/data-platform/command-owner-activation.stage-a.json
  - mk/issue-5/i5-07.mk
stageAImplementationCommands:
  - >-
    python3 -m unittest discover -s learning/labs/data-platform/tests -p
    'test_*.py'
  - python3 learning/labs/data-platform/verify_stage_a.py check
  - python3 learning/labs/data-platform/verify_stage_a.py self-test
  - make -f mk/issue-5/i5-07.mk lake-contracts-check
  - make lake-contracts-check
  - make learning-contracts-check api-contracts-check evidence-contracts-check
  - make lesson-check LESSON=promotion-trust
  - make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"
  - make data-contracts-check migration-contracts-check
  - make help
  - git diff --check
  - fresh detached-worktree Stage A focused smoke (exact block in Phase 2)
stageBImplementationPaths:
  - learning/labs/data-platform/deterministic-ingest/lab-v1.json
  - learning/labs/data-platform/deterministic-ingest/content.vi.md
  - learning/labs/data-platform/model-quality/lab-v1.json
  - learning/labs/data-platform/model-quality/content.vi.md
  - learning/labs/data-platform/weighted-metrics/lab-v1.json
  - learning/labs/data-platform/weighted-metrics/content.vi.md
  - learning/labs/data-platform/verify_stage_b.py
  - learning/labs/data-platform/tests/test_stage_b.py
  - learning/labs/data-platform/stage-b-operation-bindings.json
  - learning/labs/data-platform/tests/fixtures/stage-b-controlled-failures.json
  - learning/labs/data-platform/command-owner-activation.stage-b.json
  - mk/issue-5/i5-07.mk
---

# I5-07 — Data-platform guided labs without golden semantic drift

## Tổng quan

Lập kế hoạch Vietnamese-first từ foundation đến mid cho các lab data-platform có thao tác thật,
lỗi có kiểm soát, xác minh, evidence và reset; output cuối không được là docs dump. Kế hoạch bảo
vệ tuyệt đối semantic golden của Issue #6 tại authority SHA
`24be3b34c6b0fcdbd07c5800dcab349054e34713`. Initial validation bắt đầu từ plan-only child
`24ff21db72e0d08d34b62c3280e76ab6329665eb`; nó không coi label/plan/branch là release.

Stage A đã merge qua PR #33 tại `8ffbd420aed8dee6f5b4b0fb6d3734e094200a87` từ reviewed head
`941307931b29ef8c1a75b0f75afe480690fa8424`, đủ 10 paths và post-merge contract smoke. Issue #9
đã ship qua PR #32 tại `671201f78024786a9f2eba5e9e5fce7c78b4443d`, reviewed head
`86a6c259ad384591777cf1d46f2f6c9ea6327361`, với đúng tám operations. Fresh OrbStack consumer
smoke tại exact Stage B base `8ffbd420...` phát hiện blocker reset-rerun trong released host
release state; vì vậy amendment này giữ `COOK_SCOPE=none`. Stage C vẫn bị chặn bởi Issue #10
Stage B chưa merge.

## Phases

| Phase | Name | Status |
|-------|------|--------|
| 1 | [Dependency Amendment and Immutable Characterization](./phase-01-dependency-amendment-and-immutable-characterization.md) | Completed for Stage A; reopen for B/C |
| 2 | [Stage A Contract-Bound Foundation Labs](./phase-02-stage-a-contract-bound-foundation-labs.md) | Completed |
| 3 | [Stage B Local Runner and Data Fault Exercises](./phase-03-stage-b-local-runner-and-data-fault-exercises.md) | Pending |
| 4 | [Stage C Portal Publication and Real Journey](./phase-04-stage-c-portal-publication-and-real-journey.md) | Pending |
| 5 | [Release Evidence, Recovery, and PR Handoff](./phase-05-release-evidence-recovery-and-human-handoff.md) | Pending |

## Stage gates

| Stage | Dependency bắt buộc | Phạm vi sớm nhất | Claim tối đa |
|---|---|---|---|
| A | Issue #8 release `5644f01b4c0443a81f3af0bcce80f44c847cd986` | 10 exact paths trong register | Contract-bound candidate; không runnable |
| B | Runner merge `671201f...` + Issue #12 lease 12 paths + released I5-04 reset-rerun repair | Ba local data-fault labs; không shared data/pipeline write | Local exercise evidence; không browser/portal completion |
| C | Exact merged runner-backed Issue #10 Stage B | Publication, renderer/API integration và real-journey E2E | Stage duy nhất được claim complete learner experience |

Stage A đã merge. Stage B đã resolve runner SHA, 12-path local lease, eight-operation binding và
16 verification entries, nhưng không được cook trước I5-04 reset-rerun repair release. Stage C chỉ
được amend khi runner-backed Issue #10 Stage B đã merge. Không lặp per-stage red-team/security/
human ceremony trong critical path; xem
[dependency and authority register](./dependency-and-authority-register.md).

## Standard lean delivery path

Sau khi blocker release được pin, một delivery context duy nhất giữ vai trò implementer → focused
reviewer → fresh tester → PR/CI → merge/post-merge smoke. Reviewer phải còn
`0 Critical / 0 Important`; fresh tester chạy 16 Stage B command entries trên exact head. S3
functional negatives, golden immutability, reset/evidence và cloud prohibition vẫn là acceptance,
không phải audit lane riêng. Audit hiện tại không tạo PR hoặc merge.

## Phạm vi học tập

1. `small`, seed `42`: deterministic ingest, model, quality, grain và truth bất biến.
2. Fixed runner operations tái hiện ingest prerequisite, dbt model/quality và 11 Rill-compatible
   Parquet marts trong private workspace.
3. Weighted/additive metric đúng và controlled failure average-of-averages sai trên DuckDB đọc
   `mart_fulfillment_performance` private export.
4. Runner evidence index, reset, rerun/idempotency, timeout/resource classification và zero
   container residue được kiểm tra thật trên OrbStack.
5. Airflow, Iceberg và OpenMetadata là optional/blocked ở Stage B này vì tám released operations
   không cung cấp operation tương ứng; không sửa pipeline/governance để tạo bài học giả.
6. Mọi service/pattern phải trỏ tới failure, quality attribute và evidence cụ thể; không pattern
   theater.

Mỗi lab bắt buộc có: prerequisite checks, starter, task, controlled failure, progressive hints,
verify, immutable evidence, reset, gated solution và reflection. Reflection/hint/solution không
được tự nâng completion.

## Ranh giới authority

- Stage A đã merge đúng 10 paths; Stage B lease chỉ gồm 12 Issue #12-owned paths trong register:
  `learning/labs/data-platform/**` và `mk/issue-5/i5-07.mk`.
- Chỉ đọc: contracts/data/views/fixtures/readers Issue #6 và toàn bộ golden semantics; released
  completion/evidence authority của #8, private runner authority của #9 và renderer/API authority
  của #10. Không copy schema, tạo parallel registry, duplicate truth hoặc invented adapter.
- Bảo vệ: root `Makefile`, `release-manifest.json`, `docs/code-standards.md`, shared contracts,
  architecture views, Issue #10 portal, Issue #11 `learning/curriculum/**`, runner và pipeline.
  I5-04 repair lease là dependency riêng; Issue #12 không được dùng lease đó để sửa runner.
- Không AWS/Terraform apply/destroy, cloud resource hoặc destructive migration. PR/merge chỉ thuộc
  Standard delivery context sau cook/review/fresh tests và không được thực hiện bởi audit này.

## TDD và release contract

- Characterization hiện tại phải pass trước mutation: generator/warnings/marts/lineage/Rill,
  curated assets, publisher gap, catalog behavior và fixture hashes.
- Mỗi thay đổi bắt đầu bằng RED gắn hành vi cụ thể; cấm unconditional RED, expected-code echo,
  fake fixture hoặc mock thay cho object store/catalog thật.
- Regression IDs và evidence contract nằm trong
  [test and evidence strategy](./test-and-evidence-strategy.md).
- Additive migration, reader cũ, atomic rollback và cleanup chỉ run-owned bytes là bắt buộc; xem
  [data architecture and recovery](./data-architecture-and-recovery.md).
- Mỗi delivery stage chỉ được handoff sau khi exact tested head chạy từ pristine detached checkout không có
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
- [x] Issue #8 release, runner PR #32, Issue #12 Stage A PR #33, 12 Stage B paths, 16 Stage B
      commands và eight-operation binding đã resolve.
- [x] Stage B/C có exact dependency STOP riêng; current cook scope là `none`.
- [ ] Stable test IDs bao phủ ingest/model/quality, metrics, eight-operation recovery, evidence,
      exact six-view oracle và protected semantics; optional-service absence được báo trung thực.
- [ ] Pristine-checkout, observability và docs/release-impact gates có stable IDs và evidence.
- [ ] Standard focused review có `Critical=0`, `Important=0`; fresh tests, PR/CI và post-merge
      smoke pass trên đúng delivery head.

## Companion artifacts

- [Dependency and authority register](./dependency-and-authority-register.md)
- [Requirements traceability](./requirements-traceability.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Data architecture and recovery](./data-architecture-and-recovery.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Protected baseline manifest](./protected-baseline-manifest.md)
- [Independent initial validation report](./validation/initial-validation-report.md)

## Open questions

None. I5-04 repair release và Issue #10 Stage B là unresolved gates, không phải câu hỏi để planner
đoán.

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
- Historical next phase at that audit output was to wait for releases and repeat the old
  revalidation/readiness chain. The Lane S amendment below supersedes that active workflow.

### Standard-lane dependency amendment — 2026-07-23

- Audit input: `b697aa1f0791ed659dfc5ae748700ce8eae0cbd0`.
- Live integration head: `041d4ca866e927a331e159fdf8216838b481a595`.
- Issue #8 released by PR #28 at `5644f01b4c0443a81f3af0bcce80f44c847cd986`.
- Issue #10 static portal Stage A merged by PR #31 at
  `041d4ca866e927a331e159fdf8216838b481a595`; its post-merge browser smoke passed, but this does
  not satisfy the runner-backed Stage C dependency.
- Stage A implementation must branch from that exact integration head (or a fresh later descendant
  after rechecking dependency ancestry), not cook product files on this stale plan-only branch.
- Issue #9 remains open/unreleased; its SHA field is intentionally empty.
- Stage A disposition: `ready`, `COOK_SCOPE=stage-a-only`, 10 exact paths, 12 exact commands.
- Stage B disposition: `blocked-on-issue9` plus bounded lease.
- Stage C disposition: `blocked-on-issue10-stage-b`.
- Active workflow is Standard lean. Historical deep validation/readiness records above remain
  immutable provenance, not repeated per-stage ceremony.

### Standard-lane validation and consistency sweep

- Strict plan validation: pass, 5 phases, 0 errors, 0 warnings.
- Plan status: `in-progress`, Phase 1 complete, Stage A pending/ready, Stage B/C pending/blocked.
- Frontmatter contract: Issue #8/#10 Stage A SHAs exact; Issue #9/#10 Stage B fields empty;
  Stage A paths `10`, command entries `12`.
- Scope: 11 modified files, all Markdown under this plan directory; product paths unchanged.
- Local links: 47 checked across 14 plan Markdown artifacts, 0 broken.
- Files reread: `plan.md` and all five phase files; changed companion register, requirements,
  test strategy, risk model and protected baseline reconciled.
- Active-plan findings: `Critical=0`, `Important=0`; unresolved contradictions: 0.
- No new deep/high-assurance, red-team, security-only or human-approval audit was started.

### Standard-lane Stage B dependency/lease amendment — 2026-07-23

- Exact audit input: `876b5eaa79a48fc07e5d6a3a49a6152b20d39e53`.
- Runner release: PR #32 merge `671201f78024786a9f2eba5e9e5fce7c78b4443d`, reviewed head
  `86a6c259ad384591777cf1d46f2f6c9ea6327361`, eight operations and clean shipped smoke.
- Stage A: PR #33 merge/implementation base
  `8ffbd420aed8dee6f5b4b0fb6d3734e094200a87`, reviewed head
  `941307931b29ef8c1a75b0f75afe480690fa8424`, 10 paths and post-merge contract smoke PASS.
- Fresh detached OrbStack first cycle: three prerequisite failures classified by the runner as
  `RUNNER_OPERATION_FAILED`; all eight released operations then passed; timeout and memory probes
  returned `RUNNER_TIMEOUT` and `RUNNER_RESOURCE_LIMIT`; protected hashes and direct/root Stage A
  Make passed; no runner container remained.
- Blocking empirical result: after `workspace.reset`, a fresh second cycle passed
  `workspace.prepare`, `retail.generate`, `retail.load`, `retail.dbt-build`, then
  `retail.export` returned `RUNNER_RELEASE_POINTER_INVALID`. The export was already committed,
  left a staged evidence directory, and the next owner-CLI call crashed during recovery with the
  same code. This violates Stage B reset → rerun/idempotency and clean recovery acceptance.
- State/evidence inspection then proved 13 committed results and 13 valid published evidence
  indexes, including the second export whose caller received failure; this confirms a
  committed-but-client-failed boundary rather than an evidence-integrity failure.
- Exact local Stage B lease is recorded for 12 paths, but it does not authorize runner repair.
  I5-04 must release the bounded repair in the register before this plan can move to cook.
- Stage B disposition: `blocked`; `COOK_SCOPE=none`; `NEXT=fix-plan` after exact repair handoff.
- Stage C disposition: `blocked-on-issue10-stage-b`; Issue #10 has no merged Stage B authority.
- No product, runner, pipeline, golden, portal, curriculum or cloud mutation occurred.
