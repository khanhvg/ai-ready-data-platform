# Requirements Traceability

## Quy ước

- `MUST`: release blocker.
- `OPTIONAL-REAL`: cần service thật để claim lab đó; thiếu service chỉ được
  `not-run-optional`, không được giả pass.
- Test IDs `DL-*` là stable behavior IDs của Issue #12. Released #8/#9/#10 amendment có thể map
  chúng sang schema/registry/API fields, nhưng không được đổi nghĩa.

## Business requirements

| ID | Business outcome | Stage/phase | Stable verification IDs | Evidence | Recovery / STOP |
|---|---|---|---|---|---|
| BUS-01 | Learner foundation→mid phải thao tác, gây lỗi có kiểm soát, sửa, verify và reset; output cuối không phải docs dump | A-C / P2-P5 | `DL-LAB-001`, `DL-PUB-001` | Learner action + exact expected/actual + real journey | Không publish/complete content chỉ đọc |
| BUS-02 | Nền tảng dạy đúng golden truth và không đổi business semantics để làm lab pass | All / P1-P5 | `DL-PROT-001`, `DL-ARCH-001`, `DL-MET-002` | Issue #6 semantic readers, protected objects, six-view oracle | STOP, revert Issue #12-owned change |
| BUS-03 | Lab cốt lõi dùng được trên máy 16GB không cloud; service tùy chọn phải trung thực | B-C / P3-P5 | `DL-RES-001`, `DL-OPT-001` | Serial resource report + typed availability | Stop optional profile; không claim affected completion |

## Functional and learning requirements

| ID | Requirement | Stage/phase | Stable verification IDs | Evidence | Recovery / STOP |
|---|---|---|---|---|---|
| REQ-DEP-01 | Không cook trước exact released #8 contracts | A / P1-P2 | `DL-DEP-008` | SHA, tree hashes, released path/command matrix | Để resolution rỗng; STOP |
| REQ-DEP-02 | Không chạy runner/pipeline trước exact released #9 + exact serialized lease | B / P1-P3 | `DL-DEP-009`, `DL-LEASE-001` | Runner release + lease owner/path/expiry | Không mutate; STOP |
| REQ-DEP-03 | Không portal/publication trước passing merged #10 | C / P1-P4 | `DL-DEP-010` | Merge ancestry + released renderer/API/blast radius | Không claim completion; STOP |
| REQ-LAB-01 | Vietnamese-first foundation→mid; prerequisite/starter/task/failure/hints/verify/evidence/reset/solution/reflection | A-C / P2-P4 | `DL-LAB-001` | Contract-valid content projection | Unpublish invalid lab version |
| REQ-LAB-02 | Hint, solution, reflection, time/scroll không thể set completion | C / P4 | `DL-LAB-002`, `DL-EVD-003` | Real-journey state transitions | Restore prior content; no completion |
| REQ-DATA-01 | Ingest `small`/42 giữ exact source/model/test/grain truth | A / P2 | `DL-ING-001`, `DL-MOD-001`, `DL-DQ-001` | Issue #6 reader output + lab evidence | Reset workspace; STOP on drift |
| REQ-DATA-02 | Controlled quality warnings không bị “fix”, ignore hoặc đổi severity | A / P2 | `DL-DQ-002` | Nine configured IDs, seven warn/two pass | Revert lab/config; protected semantics fail |
| REQ-ORCH-01 | Retry chỉ lặp operation an toàn; cùng idempotency key không nhân đôi effect | B / P3 | `DL-ORCH-001` | Operation/effect journal and hashes | Resume or rollback run-owned effect |
| REQ-ORCH-02 | Timeout chặn delayed success; process tree/resource/output bounded | B / P3 | `DL-ORCH-002` | Real process timing/termination evidence | Kill scoped process group; mark failed |
| REQ-ORCH-03 | Backpressure/concurrency giới hạn và conflict fail typed | B / P3 | `DL-ORCH-003` | Queue/concurrency/state transition trace | Reject new operation; preserve active run |
| REQ-ORCH-04 | Airflow local operator path; browser không trực tiếp chạy privileged action | B-C / P3-P4 | `DL-ORCH-004`, `DL-SEC-007` | Registry/API authority trace | Disable action; no browser fallback |
| REQ-MET-01 | Weighted/additive KPI đúng; invalid average-of-averages bị bắt trên real golden data | A / P2 | `DL-MET-001`, `DL-MET-002` | Numerator/denominator/weight/grain projection | Reset starter; preserve Rill expressions |
| REQ-REL-01 | Release gồm đúng 11 assets, một generation, manifest hash và atomic current pointer | B / P3 | `DL-REL-001`, `DL-REL-002` | Old/new reader observations + manifest/pointer hash | Pointer về prior complete release |
| REQ-REL-02 | Crash tại mọi boundary không lộ mixed release hoặc false success | B / P3 | `DL-REL-003` | Fault matrix, prior pointer, orphan set | Resume same key or quarantine run-owned staging |
| REQ-ICE-01 | Commit/snapshot/read-back dùng semantics object store/catalog cục bộ đã kiểm chứng thật | B / P3 | `DL-ICE-001` | Version/topology + committed snapshot evidence | Prior snapshot remains current |
| REQ-ICE-02 | Stale writer/conflict không overwrite winner | B / P3 | `DL-ICE-002` | Two real writers, catalog conflict result | Abort loser; bounded retry with same input |
| REQ-ICE-03 | Orphan detect/recover/delete chỉ run-owned bytes | B / P3 | `DL-ICE-003` | Ownership index + before/after object list | Quarantine; refuse unknown ownership |
| REQ-OM-01 | Exact namespace/FQN/managed-set reconcile; không prefix collision | B / P3 | `DL-OM-001` | Expected/actual exact set and collision entity | Refuse broad/prefix selection |
| REQ-OM-02 | Create/update/delete policy idempotent; unmanaged entity preserved | B / P3 | `DL-OM-002`, `DL-OM-003` | Two reconcile runs + protected sentinel | Roll back run-owned mutations only |
| REQ-OM-03 | Reconcile crash/rollback phục hồi exact prior managed set | B / P3 | `DL-OM-004` | Journal, prior/current exact hashes | Replay or restore prior manifest |
| REQ-PAT-01 | Service/pattern chỉ xuất hiện khi có named failure + quality attribute + evidence | A-C / P2-P4 | `DL-PAT-001` | Pattern admission table | Remove unmotivated content |
| REQ-PUB-01 | Chỉ Stage C có thể claim complete learner experience | C / P4 | `DL-PUB-001`, `DL-PUB-002` | Passing merged #10 E2E + real evidence | Unpublish/deep-link disable |

## Non-functional, security and operational requirements

| ID | Requirement | Phase | Verification | Evidence | Recovery / STOP |
|---|---|---|---|---|---|
| NFR-DET-01 | Same admitted input ⇒ deterministic verifier/evidence projection | P2-P5 | `DL-EVD-001` | Two serial run hashes | Preserve both; reject mismatch |
| NFR-RES-01 | Core serial profile chạy trong 16GB; không Docker/cloud requirement | P2-P5 | `DL-RES-001` | Tool/profile/resource report | Stop optional services; core remains usable |
| NFR-OPT-01 | Optional service unavailable/error không masquerade controlled failure/pass | P3-P5 | `DL-OPT-001` | Typed state/remediation | No completion for affected lab |
| NFR-SEC-01 | Typed untrusted input; path/ref/link/special-file containment trước read hoặc mutation | P2-P5 | `DL-SEC-001`, `DL-SEC-002` | Negative traversal/ref/link/FIFO/socket/device suite | Reject before file/process/object effect |
| NFR-SEC-02 | Fixed query/template authority; no raw SQL/template injection | P2-P5 | `DL-SEC-003` | Injection corpus + argv/query capture | Reject; no DB/catalog effect |
| NFR-SEC-03 | Credentials/private paths/PII không vào content/evidence/log | P2-P5 | `DL-SEC-004` | Canary/redaction/private-locator scan | Quarantine evidence; rotate if exposed |
| NFR-SEC-04 | Catalog/object/namespace cleanup exact và ownership-scoped | P3-P5 | `DL-SEC-005` | Foreign sentinel survives | Refuse cleanup; manual adjudication |
| NFR-SEC-05 | Evidence tamper/replay/tree mismatch bị phát hiện | P2-P5 | `DL-SEC-006`, `DL-EVD-002` | Canonical payload/index/artifact hashes | Preserve corrupted evidence; no completion |
| NFR-MIG-01 | Additive migration; N-1 readers/adapters còn đọc; switch atomic | P3-P5 | `DL-MIG-001` | Dual-read/rollback evidence | Switch prior pointer/reader |
| NFR-REP-01 | Chỉ plan artifacts trong planner commit; product/protected path unchanged | Planner / P1 | `DL-PROT-001` | Changed-path + protected hash scan | Abort planner push |
| NFR-ARCH-01 | Exact six Issue #6 architecture view IDs/manifest semantics/source/render pairs không đổi | P1-P5 | `DL-ARCH-001` | Read-only architecture projection + tree/render hashes | STOP on view/source/semantic/render drift |
| NFR-CLEAN-01 | Exact tested head phải reproduce từ pristine detached checkout không có generated/runtime evidence ẩn | P1/P5 | `DL-CLEAN-001` | Clean status, absent pre-existing artifacts, exact released setup/test commands and final hashes | STOP; bổ sung dependency amendment thay vì dùng local-state fallback |
| NFR-OBS-01 | Run/operation/fault/resource/remediation/result có redacted observable correlation và bind evidence index | P3-P5 | `DL-OBS-001` | Ordered state/resource projection + artifact hashes; credential/private-path scan | Không claim diagnosable/pass khi projection thiếu hoặc leak |
| NFR-DOC-01 | Docs/release impact phải là `none` hoặc exact owner/path/review gate; protected root files không implicit write | P1/P5 | `DL-DOC-001` | Impact matrix + changed-path/owner/lease evidence | STOP unowned docs/release change; handoff owner separately |
| NFR-REV-01 | Fresh independent implementation/security review tại exact head, zero unresolved Critical/High | P5 | `DL-REV-001` | Exact-head review artifact and findings | Head drift/finding ⇒ review invalid; STOP |
| NFR-HUM-01 | Human approval gắn exact reviewed head trước merge | P5 | `DL-HUM-001` | GitHub exact-head approval record | Head changed ⇒ approval invalid |
| NFR-NOCLOUD-01 | Không AWS/Terraform apply/resources/destructive repo action | All | `DL-SCOPE-001` | Command/diff/evidence scan | Immediate STOP |

## Failure-to-pattern admission map

| Named failure | Quality attribute | Pattern/technique allowed | Evidence required |
|---|---|---|---|
| Retry duplicates release effect | Idempotency/consistency | Idempotency key + state/journal only if #9 contract supports it | One effect across replay |
| Timeout produces delayed success | Bounded execution/correctness | Deadline + scoped process termination | No post-timeout mutation |
| Queue overwhelms laptop | Resource safety | Bounded concurrency/backpressure | Rejection/queue depth/resource trace |
| Average-of-averages corrupts KPI | Analytical correctness | Additive numerator/denominator + explicit grain | Correct vs invalid result on golden data |
| Crash exposes 3/11 assets | Atomic visibility/recovery | Immutable staging + manifest hash + one pointer switch | Readers observe old or complete new only |
| Stale Iceberg writer wins | Concurrency integrity | Catalog conflict/optimistic commit semantics as actually verified | Loser conflict and winner snapshot |
| Orphan object cleanup deletes foreign bytes | Ownership/safety | Run-owned index + exact allow-list | Foreign sentinel preserved |
| Prefix reconcile deletes neighbor namespace | Governance safety | Exact FQN/namespace/managed-set reconciliation | Collision namespace untouched |
| Evidence file edited/replayed | Integrity/provenance | Canonical hash/index + tested-tree binding | Tamper/replay typed failure |
| Generator/DuckDB/dbt/Rill or six-view truth drifts | Learning correctness/reproducibility | Immutable Issue #6 semantic readers + protected hashes | Exact input/model/test/grain/metric/view mismatch |
| Optional Iceberg/OpenMetadata service unavailable | Truthful availability | Typed environmental state, no fake controlled failure | `not-run-optional` and affected completion false |
| Portal/UI state tries to complete a lab | Completion integrity | Fresh released verifier/evidence authority only | UI action alone leaves completion false |

Any pattern without a row above or an amendment-backed new row fails `DL-PAT-001`.
