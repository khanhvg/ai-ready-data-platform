# Dependency and Authority Register

## Mục đích

Ngăn plan suy diễn path, command, schema, registry, API, renderer hoặc SHA từ issue/branch chưa
release. Chỉ amendment sau release mới được điền các trường rỗng dưới đây.

## Immutable planner input

| Field | Value | Gate |
|---|---|---|
| Repository input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Exact local HEAD và integration tracking input |
| Issue #6 | Closed, `shipped`; merge SHA bằng repository input | Read-only golden authority |
| Issue #8 | Open; chưa có released learning-contract handoff | Stage A blocked |
| Issue #9 | Open; chưa có released runner handoff | Stage B blocked |
| Issue #10 | Open; chưa có passing merged real-journey handoff | Stage C blocked |
| Owner fan-out | Issue #5 comment `5036142770` | Planning parallel được phép; dependency bypass bị cấm |

## Resolution record — intentionally empty

| Stage | Exact dependency SHA | Exact consumed contract/registry/API/renderer paths | Exact dependency blast-radius commands | Exact Issue #12 implementation paths | Readiness |
|---|---|---|---|---|---|
| A — #8 contracts | `` | `` | `` | `` | `blocked-unreleased-dependency` |
| B — #9 runner + lease | `` | `` | `` | `` | `blocked-unreleased-dependency-and-lease` |
| C — #10 merged journey | `` | `` | `` | `` | `blocked-unmerged-dependency` |

Static placeholder check phải chứng minh các ô resolution trên rỗng; không thay bằng `TBD`, branch
head, plan commit, label hoặc guessed path.

## Dependency-derived path templates

Templates chỉ mô tả cách amendment lấy giá trị từ release thật; chúng không cấp authority hiện tại.

| Scope | Template | Resolver |
|---|---|---|
| Lab content | `learning/labs/data-platform/<stable-lab-id-from-issue-8-contract>/**` | Exact #8 contract release |
| Verifier | `<verifier-root-from-issue-8-release>/data-platform/<stable-lab-id>/**` | Exact #8 contract release |
| Runner binding | `<runner-registry-path-from-issue-9-release>` + released command IDs | Exact #9 runner release |
| Data/pipeline seam | `<exact-path-listed-in-serialized-lease>` | Human/owner lease record |
| Portal publication | `<renderer-and-route-paths-from-issue-10-release>` | Passing merged #10 handoff |
| Blast radius | `<exact-command-list-published-by-dependency-release>` | #6/#8/#9/#10 handoff comments/artifacts |

Fixed issue-owned destination `mk/issue-5/i5-07.mk` is authorized by Issue #12 but cannot receive
recipes until Stage B command IDs and ownership are amended. Root `Makefile` stays protected.

## Amendment protocol per stage

1. Fetch live remote read-only; require issue release state and exact 40-hex handoff SHA.
2. Prove SHA is an ancestor of the intended implementation input and that released artifacts
   exist at that SHA.
3. Record SHA, tree/blob hashes, exact consumed paths, exact blast-radius commands and declared
   compatibility/migration requirements.
4. Recompute [protected baseline](./protected-baseline-manifest.md); STOP on unexpected drift.
5. Obtain any serialized shared-contract/data/pipeline lease with exact paths and expiry/owner.
6. Run a fresh independent plan revalidation, then fresh readiness audit. Planner/cook identity
   cannot validate itself.
7. Cook only the amended stage. Later stages remain blocked and their fields remain empty.

## STOP conditions

- Branch/label/plan commit substituted for released dependency SHA.
- Any dependency path or command guessed before release.
- #8 contract, #9 runner, #10 journey or serialized lease mismatch.
- Concurrent shared-contract/pipeline writer.
- Protected path/tree drift without separately approved seam.
- Dirty/wrong base, unresolved merge ancestry or non-exact human approval.
