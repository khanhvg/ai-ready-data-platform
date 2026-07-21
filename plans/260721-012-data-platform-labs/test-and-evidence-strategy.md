# Test and Evidence Strategy

## TDD ordering

1. **Characterization GREEN:** run released Issue #6 readers against exact input without mutation.
2. **Behavior-specific RED:** create a real controlled condition in a private run/service
   namespace and assert the missing verifier/fail-loud/recovery behavior. Capture actual failure,
   not an echoed expected code.
3. **Minimum GREEN:** implement only the admitted content/verifier/seam needed for that ID.
4. **Refactor:** remove duplication while stable IDs and behavior remain green.
5. **Regression:** stage-local suite + exact released dependency blast radius + protected hashes.

Unconditional `fail`, a test that passes because a file is merely absent, fake rows/services,
ignored/skipped/xfail fixtures or assertions, mock-only catalog/object behavior, expected-code
echo and in-place mutation of golden fixtures are invalid RED evidence. Missing
dependency/tool/service là gate hoặc typed environmental failure, không phải behavior RED và
không được dùng thay cho actual failing behavior.

Mỗi stable behavior ID phải giữ một sequence riêng theo exact tested tree: characterization
expected/actual → RED expected/actual với đúng một controlled condition → minimum GREEN
expected/actual → refactor/regression expected/actual. Không được batch nhiều behavior vào một RED,
viết GREEN trước rồi dựng lại RED, hoặc chỉ lưu expected code mà thiếu actual state/value/effect.

## Characterization anchors before any RED

| ID | Current truth at input SHA | Mutation policy |
|---|---|---|
| `DL-CHAR-ING` | `small`/42, 18 CSVs, 6,812 rows, exact Issue #6 file/manifest projection hashes | Read-only |
| `DL-CHAR-MOD` | 18 sources; 18 staging, 6 intermediate, 16 core, 11 marts; 51 models | Read-only |
| `DL-CHAR-DQ` | 141 generic tests; 179 pass, 7 warn, 0 fail, 186 total; nine configured warn IDs | Read-only |
| `DL-CHAR-MET` | Exact Rill sources/dimensions/expressions and weighted/unweighted distinctions | Read-only |
| `DL-CHAR-ARCH` | Exact six architecture IDs and manifest audience/concern/scope; source closure, six SVG/text pairs and render-manifest hashes | Read-only |
| `DL-CHAR-REL` | Ordered exact 11-set; manifest/current-pointer pure contract; publisher remains sequential drop/create | Read-only |
| `DL-CHAR-ICE` | Current local publisher/read-back behavior is a gap, not atomic/conflict/orphan proof | Read-only |
| `DL-CHAR-OM` | Current catalog verifier checks non-zero populations/count context, not exact reconcile | Read-only |
| `DL-CHAR-FIX` | Exact fixture/contract SHA-256 in protected baseline manifest | Read-only |

## Stable behavior IDs and RED design

| Stable ID | RED condition on real state | Required GREEN oracle |
|---|---|---|
| `DL-ING-001` | Private `small`/42 rerun differs in file/row/content projection | Exact Issue #6 projection equality twice |
| `DL-MOD-001` | Learner starter references wrong layer/grain while real graph reader supplies truth | Names exact source→staging→intermediate→core→mart path and grain |
| `DL-DQ-001` | Learner treats controlled warn as error | Verifier distinguishes controlled warn/environment failure and retains progress incomplete |
| `DL-DQ-002` | Private mutation changes warn identity/severity/status | Golden reader emits semantic mismatch; protected files untouched |
| `DL-ORCH-001` | Same admitted operation replayed during/after retry | Exactly one committed effect; duplicate maps to same outcome |
| `DL-ORCH-002` | Real bounded operation exceeds deadline | Typed timeout, child tree stopped, no delayed mutation |
| `DL-ORCH-003` | Concurrent requests exceed released limit or race reset/publish | Bounded queue/rejection/conflict; one legal writer |
| `DL-ORCH-004` | Browser attempts direct privileged command or bypasses released registry | Denied before process start; authorized runner route only |
| `DL-MET-001` | Starter computes unweighted average of subgroup averages for an Issue #6 metric that contractually requires weighting | Ratio/additive weighted result matches contract and differs from invalid result |
| `DL-MET-002` | Numerator/denominator/weight/grain/source changed, or an intentionally unweighted Issue #6 measure is incorrectly “fixed” | Stable assertion names exact semantic mismatch and preserves current Rill contract |
| `DL-REL-001` | 10/12/duplicate/mixed-generation manifest | Exact 11-set validator rejects |
| `DL-REL-002` | Reader polls during pointer transition | Every observation is old complete or new complete/hash-valid |
| `DL-REL-003` | Crash after each asset/manifest/pointer boundary | Prior remains current or new complete; no false success/mixed set |
| `DL-ICE-001` | Real local commit/read-back has missing/wrong snapshot or asset identity | Exact snapshot, 11 assets and manifest hashes match |
| `DL-ICE-002` | Two real attempts commit from same base snapshot | One wins; stale writer conflicts or serialized gate prevents overlap |
| `DL-ICE-003` | Crash leaves run-owned orphan plus foreign sentinel | Run orphan recovered/removed; foreign object survives |
| `DL-OM-001` | Managed namespace and prefix-collision neighbor coexist | Exact namespace/FQN selection; neighbor untouched |
| `DL-OM-002` | Desired owner/tag/lineage changes, then reconcile twice | Exact create/update/delete policy; second run no-op/idempotent |
| `DL-OM-003` | Stale managed entity plus unmanaged sentinel | Only stale exact managed entity removed |
| `DL-OM-004` | Crash mid-reconcile | Replay completes same target or rollback restores prior exact set |
| `DL-LAB-001` | One required lab element/remediation mapping removed from private content copy | Released #8 contract/verifier rejects stable field gap |
| `DL-LAB-002` | Hint/solution/reflection/evidence file presence used to force completion | Completion remains false until fresh live verification passes |
| `DL-EVD-001` | Two serial equivalent runs | Deterministic semantic evidence projection; allowed runtime drift isolated |
| `DL-EVD-002` | Artifact/hash/index/dependency/tree/content/verifier binding changed or replayed | Typed integrity/replay failure; completion unchanged |
| `DL-PROT-001` | Protected Git object or semantic projection differs | Exact mismatch and STOP before publication |
| `DL-ARCH-001` | Six-view ID/set/order, audience/concern/scope, source, SVG/text or render-manifest semantics drift | Issue #6 architecture reader names exact mismatch; no golden view/source/render mutation |
| `DL-PAT-001` | Pattern/service has no named failure/evidence row | Content contract rejects pattern theater |
| `DL-OPT-001` | Optional service absent/starting/error | Honest status/remediation; affected verify cannot pass |

## Gate, security and publication IDs

| Stable ID | Oracle |
|---|---|
| `DL-DEP-008` | Exact released #8 SHA/artifacts exist, ancestry holds and Stage A amendment paths/commands match release |
| `DL-DEP-009` | Exact released #9 SHA/runner artifacts exist, ancestry holds and Stage B bindings match release |
| `DL-DEP-010` | Exact passing merged #10 SHA/renderer/API/E2E artifacts exist and ancestry holds |
| `DL-LEASE-001` | Serialized lease names exact owner, paths, input SHA and active/non-overlap window |
| `DL-SEC-001` | Traversal/absolute/encoded path/ref rejected before file/process/service mutation |
| `DL-SEC-002` | Symlink/hardlink/swap, FIFO/socket/device/other non-regular file and foreign source/destination rejected before read/write; protected tree unchanged |
| `DL-SEC-003` | SQL/template/shell metacharacter input cannot change fixed query/target/argv authority |
| `DL-SEC-004` | Credential/private-path/PII canary absent from retained content/log/evidence |
| `DL-SEC-005` | Cleanup/reconcile deletes only exact run-owned object/entity set; foreign sentinels survive |
| `DL-SEC-006` | Evidence artifact/index/canonical hash mutation and replay produce typed non-completion |
| `DL-SEC-007` | Browser direct privileged execution/bypass is denied before local side effect |
| `DL-EVD-003` | Hint/solution/reflection/time/scroll/file presence alone cannot mark completion |
| `DL-RES-001` | Serial core lane remains within admitted 16GB/resource bounds without Docker/cloud |
| `DL-MIG-001` | Additive N/N-1 readers dual-read, atomic switch and prior-state rollback pass |
| `DL-PUB-001` | Only fresh Stage C real journey + live valid evidence can set completion |
| `DL-PUB-002` | Reload/back-forward/reset/replay/accessibility paths preserve legal state/evidence authority |
| `DL-REV-001` | Fresh independent implementation/security review binds exact 40-hex head and has zero unresolved Critical/High |
| `DL-HUM-001` | Human approval record names exact independently reviewed 40-hex head |
| `DL-SCOPE-001` | Changed-command/path scan finds no AWS/Terraform apply/resource or destructive repo action |

## Evidence bundle requirements

Evidence root remains `.artifacts/evidence/data-labs/<run-id>/` after released contracts confirm
the exact locator. Until that amendment, no current evidence path/producer is authorized.

Required semantic fields, mapped to exact #8 schema names only after release:

- stable lab/lesson/content/verifier/assertion IDs and versions;
- input/tested-tree SHA plus exact #6/#8/#9/#10 dependency SHAs;
- contract, registry, fixture and protected-tree hashes;
- sanitized parameters (`small`, `42` where required), tool/service versions and topology;
- ordered operation/state transitions, fault boundary and actual result;
- per-behavior characterization/RED/GREEN/refactor-regression sequence; assertion expected/actual
  state/value/effect summaries, result, failure class and remediation;
- artifact media type, relative locator, byte size and SHA-256;
- release/manifest/pointer/snapshot/catalog/namespace identities when applicable;
- cleanup/rollback result, redaction/retention class and evidence index hash.

Evidence never stores token, full env, raw PII/customer/order rows, absolute host path, private URL
or learner raw SQL. Local hashes prove integrity only, not publisher authenticity.

## Test tiers

| Tier | Runtime | Mandatory outcome |
|---|---|---|
| Core contract/content | Serial, Docker-free | Required; foundation labs and protected semantics pass |
| Runner/pipeline | Released #9 local runtime | Required for Stage B; no browser claim |
| Iceberg/OpenMetadata real service | Verified local object store/catalog/service | Required before service-backed labs publish; unavailable may only be `not-run-optional` |
| Portal real journey | Passing merged #10 renderer/API/browser path | Required for Stage C completion claim |
| Human | Exact reviewed head | Required before merge |

## Final regression

```bash
make data-labs-e2e lake-fault-test metadata-reconcile-test data-contracts-check
```

Append, do not guess, exact blast-radius commands from released #6/#8/#9/#10 amendment. Execute
serially on 16GB. Required failure, protected drift, unverified optional-service claim or stale
human approval blocks merge.
