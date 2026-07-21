---
phase: 2
title: "Stage A Contract-Bound Foundation Labs"
status: pending
priority: P1
dependencies: [1]
externalDependencies: [issue-8-released-contracts]
effort: "unresolved until exact Stage A amendment"
---

# Phase 2: Stage A Contract-Bound Foundation Labs

## Context links

- [Plan](./plan.md)
- [Requirements traceability](./requirements-traceability.md)
- [Test and evidence strategy](./test-and-evidence-strategy.md)
- [Risk and S3 threat model](./risk-and-threat-model.md)
- [Master lesson/lab contract — historical planning input](../260721-005-enterprise-learning-sandbox/lesson-lab-contract.md)

## Overview

Sau exact released Issue #8 contracts, tạo Vietnamese-first lab content và ứng viên verifier
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

Content path dùng template
`learning/labs/data-platform/<stable-lab-id-from-issue-8-contract>/**`. Verifier root và exact
entrypoint lấy nguyên văn từ #8 amendment. Verifier đọc contract-valid content và Issue #6
projection; output chỉ tới private planner/test workspace defined by released contract. Không tạo
runner/API/renderer wrapper.

## Learning lab matrix

| Level | Outcome | Starter/task | Controlled failure | Verify/evidence | Reset/solution/reflection |
|---|---|---|---|---|---|
| Foundation | Nhận diện grain và deterministic input | Inspect `small`/42 manifest/projection và map raw grain | Same totals nhưng private copy đổi anomaly/hash | `DL-ING-001`; exact reader projection | Recreate private starter; reveal hash/grain explanation; reflect reproducibility limit |
| Junior | Trace model và quality | Map source→staging→intermediate→core→mart, classify warning | Treat controlled warning as error hoặc silently ignore | `DL-MOD-001`, `DL-DQ-001/002` | Reset mapping; progressive hint from warning ID→layer; reflect severity trade-off |
| Junior | Tính KPI đúng grain | Build numerator/denominator/weight table cho metric contractually weighted trên real golden result | Average subgroup averages; hoặc “fix” nhầm intentional unweighted metric | `DL-MET-001/002`; correct and invalid values both retained | Reset formula; reveal additive derivation only after evidence; reflect when unweighted AVG is intentional |

## Related code files

- Create after amendment: dependency-derived lab content paths under authorized
  `learning/labs/data-platform/**`.
- Create after amendment: dependency-derived non-mutating verifier paths.
- Preserve: all Issue #6 contracts/data/views/fixtures/readers and protected trees.
- Exact current Stage A implementation path list: empty.

## Implementation steps

1. Amend exact #8 release SHA, contract schemas, stable field names, validator command and
   verifier destination; revalidate independently and pass readiness.
2. Add RED contract cases by omitting/mutating one required field/remediation link in a private
   content copy; prove the released verifier reports the stable failing assertion.
3. Author Vietnamese-first prerequisite/starter/task/failure/hints/verify/evidence/reset/solution/
   reflection sections for the three lab outcomes.
4. Bind exact Issue #6 readers and fixture hashes read-only; reject copied/edited evidence as
   completion.
5. Add real-golden weighted metric exercise with one deliberately invalid learner formula.
6. Run contract/content/verifier tests plus exact #6/#8 blast radius and protected hashes.
7. Mark outputs `candidate-not-runnable`; retain Stage B/C dependency blockers.

## Tests before

- Baseline characterization IDs pass unchanged.
- `DL-LAB-001` REDs are private document mutations against the released #8 validator.
- `DL-MET-001` RED is the real invalid learner computation, not a fake fixture or hardcoded error.

## Refactor

Share only contract-required Vietnamese lab structure/remediation helpers after three contents
prove duplication. Do not add a general framework, registry, API or renderer.

## Tests after

- Contract mutation matrix, links, prerequisites and remediation mapping.
- Stable ingest/model/DQ/metric IDs.
- Evidence/tamper checks that cannot advance completion.
- Exact released #6/#8 blast radius and protected hashes.

## Success criteria

- [ ] Three foundation/junior lab candidates satisfy full content contract.
- [ ] Mỗi candidate có learner action và expected-vs-actual contract rõ ràng; không phải docs
      dump hoặc completion-by-reading.
- [ ] Verifier candidate is non-mutating and Issue #6 remains byte/semantic identical.
- [ ] Invalid average-of-averages fails against real golden data with useful remediation.
- [ ] Output cannot be described as runnable or complete learner experience.

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
