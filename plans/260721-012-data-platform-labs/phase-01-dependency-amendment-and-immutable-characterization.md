---
phase: 1
title: "Dependency Amendment and Immutable Characterization"
status: completed
priority: P1
dependencies: []
externalDependencies: []
effort: "Stage A gate complete; reopen only for B/C dependency handoff"
---

# Phase 1: Dependency Amendment and Immutable Characterization

## Context links

- [Plan](./plan.md)
- [Dependency and authority register](./dependency-and-authority-register.md)
- [Protected baseline manifest](./protected-baseline-manifest.md)
- [Issue #6 golden contract matrix](../260721-006-freeze-golden-baseline/golden-contract-matrix.md)
- [Master Phase 7](../260721-005-enterprise-learning-sandbox/phase-07-data-pipeline-guided-labs.md)

## Overview

Gate không triển khai. Standard-lane amendment này đã pin released Issue #8 và exact Stage A
path/command set. Future bounded amendment chỉ resolve Stage B hoặc C khi dependency tương ứng
release; plan/label/open branch không thay thế release.

## Requirements

### Functional

- Initial validator phải bắt đầu tại exact plan head
  `24ff21db72e0d08d34b62c3280e76ab6329665eb`; planner/product input và Issue #6 immutable
  authority riêng là `24be3b34c6b0fcdbd07c5800dcab349054e34713`.
- Record current truth read-only: warnings, marts, lineage, publish/catalog gaps, curated set và
  fixture/contract hashes.
- Stage A pins Issue #8 merge `5644f01b4c0443a81f3af0bcce80f44c847cd986`; Issue #10 static
  Stage A merge `041d4ca866e927a331e159fdf8216838b481a595` is reference-only.
- Stage B/C amendment phải điền exact 40-hex dependency SHA, exact released paths/commands,
  tree/blob hashes, compatibility, blast radius và lease khi áp dụng.
- Stage amendment phải khai báo pristine-checkout setup/test behavior, observability mapping và
  docs/release impact (`none` hoặc exact owner/path/gate) từ authority đã release.
- #9 runner và #10 runner-backed Stage B resolution fields giữ rỗng.

### Non-functional

- Không chạy generator/dbt/publisher/catalog hoặc optional service trong planner phase.
- Không sửa historical plans để “resolve” dependency metadata stale.
- Không lặp deep validation/red-team/readiness ceremony; Lane S dùng combined amendment này rồi
  focused review, fresh tests, PR/CI và post-merge smoke.

## Architecture

Dependency release là capability input. Mỗi amendment pin dependency snapshot rồi map stable
`DL-*` requirements sang contract/registry/API/renderer thật. Nếu map không đầy đủ, stage đó tiếp
tục blocked; không tạo adapter hay “equivalent” path trong lúc cook.

## Related code files

- Preserve: toàn bộ targets trong [protected baseline](./protected-baseline-manifest.md).
- Modify now: chỉ các plan artifacts trong directory này.
- Future exact implementation files: unresolved and intentionally empty.
- Future templates: xem [dependency register](./dependency-and-authority-register.md); templates
  không cấp current authority.

## Characterization checklist

- [ ] `DL-CHAR-ING`: Issue #6 generator profile/seed/file/row/hash projection.
- [ ] `DL-CHAR-MOD`: dbt source/layer/model/mart/grain truth.
- [ ] `DL-CHAR-DQ`: nine configured warnings, seven warn/two pass, zero errors.
- [ ] `DL-CHAR-MET`: exact Rill source/dimension/measure/weighting distinctions.
- [ ] `DL-CHAR-ARCH`: exact six architecture IDs, manifest audience/concern/scope semantics,
      source closure, rendered SVG/text pairs and deterministic render-manifest hashes.
- [ ] `DL-CHAR-REL`: exact 11-set + manifest/pointer contract; publisher gap retained.
- [ ] `DL-CHAR-ICE`: current service behavior not relabeled atomic/conflict/orphan proof.
- [ ] `DL-CHAR-OM`: count-oriented current check not relabeled exact reconciliation.
- [ ] `DL-CHAR-FIX`: fixture/contract/tree hashes match protected manifest.

## Implementation steps

1. At each future amendment, fetch live integration/dependency refs read-only and verify exact
   ancestry/release state.
2. Compare protected Git objects and semantic Issue #6 reader projections.
3. Fill only the amendment’s dependency stage row; Stage A is resolved and later-stage rows stay
   empty.
4. Record exact serialized lease for any shared contract/publisher/Airflow/OpenMetadata path.
5. Map released schema/registry/API/renderer fields to stable requirements without renaming
   behavior IDs.
6. Run one Standard-lane combined dependency/readiness amendment for the newly unblocked stage.
7. Reproduce the amended gate from a pristine detached checkout with no hidden generated/runtime
   evidence; fail if released setup/test commands or required cache assumptions are incomplete.
8. Produce an exact implementation-input SHA; only then may the stage enter cook.

## Tests before

Characterization is GREEN and read-only. A dependency mismatch is a gate failure, not a fabricated
RED. No product change starts in this phase.

## Tests after

Re-run ancestry, dependency existence, protected hash, path/command resolution and changed-path
checks after each amendment.

## Success criteria

- [x] Stage A records exact #8 SHA, 10 paths and 12 commands; #9 and #10 Stage B fields remain
      empty.
- [x] Stage A-base protected objects/hashes match Issue #6; the sole expected inventory delta is
      exact released #8 `learning/contracts/`, unchanged between #8 release and integration head.
- [x] Every blocked future stage owns an exact dependency handoff and combined Lane S amendment.
- [x] Every amended stage defines pristine-checkout, observability and docs/release-impact gates.
- [x] No guessed schema, registry, API, renderer, command or implementation path appears.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| “Ready to cook/audit” label mistaken as release | Consume unstable contract | Require issue release handoff + exact ancestor SHA + artifact hashes |
| Historical plan `pending` status mistaken as live dependency | Wrong cross-plan edits | GitHub release/merge evidence is authority; historical plan stays read-only |
| Dependency release drifts protected semantics | Golden regression | Semantic reader + tree/hash checks; separately admitted lease or STOP |
| Ceremony replaces evidence | Slow delivery without risk reduction | One Lane S context; retain functional S3/reset/evidence/cloud gates |

## Security considerations

Read-only GitHub/repository inspection only. No secrets, installs, service startup, cloud calls,
workspace cleanup, product mutation or broad branch operation.

## Next steps

Cook Phase 2 only with `COOK_SCOPE=stage-a-only`. Reopen this gate for Stage B only after exact
merged Issue #9 runner release plus bounded lease; Stage C waits for merged runner-backed Issue
#10 Stage B.
