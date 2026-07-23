---
phase: 2
title: Stage A Contract-Bound Foundation Labs
status: completed
priority: P1
dependencies:
  - 1
externalDependencies: []
effort: bounded 10-path Stage A cook
---

# Phase 2: Stage A Contract-Bound Foundation Labs

## Context links

- [Plan](./plan.md)
- [Requirements traceability](./requirements-traceability.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Master lesson/lab contract — historical planning input](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md)

## Overview

Từ exact Issue #8 release `5644f01b4c0443a81f3af0bcce80f44c847cd986`, tạo Vietnamese-first lab content và ứng viên verifier
không mutate cho deterministic ingest/model/quality và weighted metrics. Stage A chỉ chứng minh
contract/content candidate trên fixture/readers Issue #6 bất biến; không runner, pipeline mutation,
portal publication hoặc runnable-completion claim.

## Requirements

### Functional

- Foundation→junior route: grain/determinism → model layers/quality → weighted metric correctness.
- Mỗi lab có prerequisite, starter, task, controlled failure, hints, verify, evidence requirements,
  reset semantics, gated solution và reflection.
- Mỗi candidate phải dẫn tới một learner action và expected-vs-actual artifact kiểm chứng được;
  prose/links/scroll-only content không đủ và không được coi là hands-on completion.
- `small`, seed `42` và Issue #6 readers/fixtures là truth; controlled failure được tạo trong
  private copy, không sửa golden files.
- Weighted lab dùng real golden rows của một metric Issue #6 bắt buộc weighting (ví dụ
  fulfillment lead time hoặc supplier on-time) để chứng minh ratio/additive result khác invalid
  average-of-averages; đồng thời giữ nguyên các measure hiện hữu được contract ghi là intentionally
  unweighted. Không “sửa” mọi `AVG` và không dạy công thức bằng prose-only.
- Draft content cho orchestration/release/Iceberg/OpenMetadata chỉ được reference stable outcomes;
  không gắn command/registry/API chưa release.

### Non-functional

- Non-mutating verifier candidate chỉ đọc dependency contract + immutable fixtures/readers.
- Core serial, Docker-free, cloud-free, 16GB-safe.
- Stage A evidence chỉ là contract/static verification; không được dùng set progress/completion.

## Architecture

Content dùng ba exact Issue #12-owned directories dưới `learning/labs/data-platform/**`. Mỗi
`lab-v1.json` bind released `lab-v1`; `content.vi.md` bên cạnh là candidate content được
`verify_stage_a.py` kiểm tra bằng invariant I5-07 cục bộ, không tạo shared schema field. Verifier
đọc contract-valid content và Issue #6 projection, chỉ tạo temporary/run-owned evidence. Không tạo
runner/API/renderer wrapper hoặc completion/progress writer.

## Learning lab matrix

| Level | Outcome | Starter/task | Controlled failure | Verify/evidence | Reset/solution/reflection |
|---|---|---|---|---|---|
| Foundation | Nhận diện grain và deterministic input | Inspect `small`/42 manifest/projection và map raw grain | Same totals nhưng private copy đổi anomaly/hash | `DL-ING-001`; exact reader projection | Recreate private starter; reveal hash/grain explanation; reflect reproducibility limit |
| Junior | Trace model và quality | Map source→staging→intermediate→core→mart, classify warning | Treat controlled warning as error hoặc silently ignore | `DL-MOD-001`, `DL-DQ-001/002` | Reset mapping; progressive hint from warning ID→layer; reflect severity trade-off |
| Junior | Tính KPI đúng grain | Build numerator/denominator/weight table cho metric contractually weighted trên real golden result | Average subgroup averages; hoặc “fix” nhầm intentional unweighted metric | `DL-MET-001/002`; correct and invalid values both retained | Reset formula; reveal additive derivation only after evidence; reflect when unweighted AVG is intentional |

## Related code files

- Create: `learning/labs/data-platform/deterministic-ingest/lab-v1.json`.
- Create: `learning/labs/data-platform/deterministic-ingest/content.vi.md`.
- Create: `learning/labs/data-platform/model-quality/lab-v1.json`.
- Create: `learning/labs/data-platform/model-quality/content.vi.md`.
- Create: `learning/labs/data-platform/weighted-metrics/lab-v1.json`.
- Create: `learning/labs/data-platform/weighted-metrics/content.vi.md`.
- Create: `learning/labs/data-platform/verify_stage_a.py`.
- Create: `learning/labs/data-platform/tests/test_stage_a.py`.
- Create: `learning/labs/data-platform/command-owner-activation.stage-a.json`.
- Create: `mk/issue-5/i5-07.mk` with `lake-contracts-check` only.
- Preserve: all Issue #6 contracts/data/views/fixtures/readers and protected trees.
- Exact Stage A implementation path count: 10.

## Implementation steps

1. Create the cook branch from exact integration head
   `041d4ca866e927a331e159fdf8216838b481a595` (or freshly verified descendant), prove #8 ancestry,
   then assert all 10 consumed authority paths/hashes from the register. Do not implement from the
   stale plan-only branch tree.
2. Add RED contract cases by omitting/mutating one required field/remediation link in a private
   content copy; prove the released verifier reports the stable failing assertion.
3. Author Vietnamese-first prerequisite/starter/task/failure/hints/verify/evidence/reset/solution/
   reflection sections for the three lab outcomes.
4. Bind exact Issue #6 readers and fixture hashes read-only; reject copied/edited evidence as
   completion.
5. Add real-golden weighted metric exercise with one deliberately invalid learner formula.
6. Add only the reserved `lake-contracts-check` recipe and its owner-scoped activation document;
   leave all E2E/fault/metadata commands future/unimplemented.
7. Run the 12 command entries from the register, including detached clean-checkout smoke.
8. Use one Lane S delivery context: focused review with `Critical=0`, `Important=0`, fresh exact-head
   tests, PR/CI, merge and post-merge static contract smoke.
9. Mark outputs `candidate-not-runnable`; retain Stage B/C dependency blockers.

## Tests before

- Baseline characterization IDs pass unchanged.
- `DL-LAB-001` REDs are private document mutations against the released #8 validator.
- `DL-MET-001` RED is the real invalid learner computation, not a fake fixture or hardcoded error.

## Refactor

Share only contract-required Vietnamese lab structure/remediation helpers after three contents
prove duplication. Do not add a general framework, registry, API or renderer.

## Tests after

- Focused: unit discovery, verifier `check`, verifier `self-test`, direct-fragment and composed
  `lake-contracts-check`.
- Released blast radius: exact #8 primary/lesson/evidence commands, exact #6 data/migration
  commands, help and diff check.
- Clean smoke: exact Stage A head in a fresh detached worktree, no pre-existing generated/runtime
  evidence, direct-fragment `lake-contracts-check`.
- Functional safety: contract mutation matrix, links/prerequisites/remediation, stable
  ingest/model/DQ/metric IDs, evidence/tamper non-completion and protected hashes.

## Success criteria

- [ ] Three foundation/junior lab candidates satisfy full content contract.
- [ ] Mỗi candidate có learner action và expected-vs-actual contract rõ ràng; không phải docs
      dump hoặc completion-by-reading.
- [ ] Verifier candidate is non-mutating and Issue #6 remains byte/semantic identical.
- [ ] Invalid average-of-averages fails against real golden data with useful remediation.
- [ ] Output cannot be described as runnable or complete learner experience.
- [ ] Focused review has zero Critical/Important findings; fresh 12-command set, PR/CI and
      post-merge static smoke pass.

## Risk assessment

| Risk | Impact | Mitigation |
|---|---|---|
| Guessed #8 schema/IDs | Contract fork | No work before exact amendment; use released values verbatim |
| “Educational simplification” changes grain/warning truth | Golden semantic drift | Issue #6 reader oracle and `DL-PROT-001` |
| Content-only pass treated as runnable | False release | Explicit candidate state; no progress authority |
| Fake metric fixture hides weighting defect | Weak lab | Real golden rows and both correct/invalid result evidence |

## Security considerations

Treat content fields/paths/refs as untrusted. No raw SQL, shell, environment, credentials,
absolute path, link/special file, PII or browser action. Negative tests
`DL-SEC-001/002/003/004/006` run before handoff.

## Next steps

Stage B remains blocked until exact Issue #9 runner release and separately admitted narrow
data-contract/pipeline lease.
