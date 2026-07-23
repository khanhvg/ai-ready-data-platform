# Dependency and Authority Register

## Mục đích

Ngăn plan suy diễn path, command, schema, registry, API, renderer hoặc SHA từ issue/branch chưa
release. Amendment Standard-lane này resolve Stage A; Stage B/C tiếp tục fail-closed.

## Immutable planner input

| Field | Value | Gate |
|---|---|---|
| Planner/product input | `24be3b34c6b0fcdbd07c5800dcab349054e34713` | Integration input trước planner-only commit; read-only product tree |
| Initial validation input | `24ff21db72e0d08d34b62c3280e76ab6329665eb` | Exact clean local/tracking/fresh-live plan head |
| Issue #6 | Closed, `shipped`; merge SHA bằng planner/product input | Read-only golden authority |
| Integration head | `041d4ca866e927a331e159fdf8216838b481a595`, tree `1ad11b31c45b282bd179f76054ad215484f81060` | Fresh remote head of `integration/issue-5-local-learning` |
| Issue #8 | Released by PR #28 at `5644f01b4c0443a81f3af0bcce80f44c847cd986`, tree `a38594d420fe7df2b30265a8a72bb5fad1698012` | Stage A dependency satisfied |
| Issue #9 | Open; no merged/released runner SHA | Stage B blocked; field must remain empty |
| Issue #10 Stage A | Static portal merged by PR #31 at `041d4ca866e927a331e159fdf8216838b481a595`; post-merge browser smoke passed | Reference-only; does not unblock Stage C |
| Issue #10 Stage B | Runner-backed journey not merged/released | Stage C blocked |
| Owner fan-out | Issue #5 comment `5036142770` | Planning parallel được phép; dependency bypass bị cấm |

## Resolution record

| Stage | Exact dependency SHA | Exact consumed contract/registry/API/renderer paths | Exact dependency blast-radius commands | Exact Issue #12 implementation paths | Readiness |
|---|---|---|---|---|---|
| A — #8 contracts | `5644f01b4c0443a81f3af0bcce80f44c847cd986` | Exact Stage A consumed paths below | 12 exact command entries below | 10 exact paths below | `ready-contract-bound-candidate` |
| B — #9 runner + lease | `` | `` | `` | `` | `blocked-on-issue9-release-and-bounded-lease` |
| C — #10 runner-backed Stage B | `` | `` | `` | `` | `blocked-on-issue10-stage-b` |

Stage A implementation base is integration head
`041d4ca866e927a331e159fdf8216838b481a595` (or a freshly verified descendant retaining both
dependency merges). The plan-only branch is the amendment publication vehicle, not a stale product
base for cook.

Static placeholder check phải chứng minh Stage B/C resolution vẫn rỗng; không thay bằng branch
head, plan commit, label hoặc guessed path.

## Stage A exact consumed authority

Read-only paths at Issue #8 release, all present in integration head:

1. `learning/contracts/lab-v1.schema.json`
2. `learning/contracts/learning-evidence-v1.schema.json`
3. `learning/contracts/completion-reconciliation-v1.json`
4. `learning/contracts/fitness-result-v2.schema.json`
5. `learning/contracts/command-owner-activation-v1.schema.json`
6. `learning/contracts/command-owner-registry-v1.json`
7. `learning/contracts/learning-contract-version-registry-v1.json`
8. `learning/contracts/learning-contract-set-v1.json`
9. `learning/contracts/operation-matrix-v1.json`
10. `mk/issue-5/i5-03.mk`

`command-owner-registry-v1.json` reserves `lake-contracts-check` for I5-07 and
`mk/issue-5/i5-07.mk`; Stage A may activate only that static contract check through an
I5-07-owned activation document. It must not activate runner-, fault-, metadata- or E2E claims.
The released base registry SHA-256 is
`a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80`.

Issue #10 static Stage A handoff paths verified read-only:

- `apps/learning-portal/scripts/verify-stage-a-release.mjs`
- `apps/learning-portal/src/contracts/released-learning-adapter.mjs`
- `apps/learning-portal/src/catalog/released-module-provider.mjs`
- `apps/learning-portal/src/render/static-document.mjs`
- `apps/learning-portal/src/routing/portal-router.mjs`
- `apps/learning-portal/tests/e2e/stage-a.spec.mjs`
- `mk/issue-5/i5-05.mk`

These paths prove only static catalog/render/browser behavior. Stage C fields stay empty until the
runner-backed Issue #10 Stage B handoff publishes its exact merge SHA, extension paths and commands.

## Stage A exact write set — 10 paths

1. `learning/labs/data-platform/deterministic-ingest/lab-v1.json`
2. `learning/labs/data-platform/deterministic-ingest/content.vi.md`
3. `learning/labs/data-platform/model-quality/lab-v1.json`
4. `learning/labs/data-platform/model-quality/content.vi.md`
5. `learning/labs/data-platform/weighted-metrics/lab-v1.json`
6. `learning/labs/data-platform/weighted-metrics/content.vi.md`
7. `learning/labs/data-platform/verify_stage_a.py`
8. `learning/labs/data-platform/tests/test_stage_a.py`
9. `learning/labs/data-platform/command-owner-activation.stage-a.json`
10. `mk/issue-5/i5-07.mk`

The three JSON descriptors bind released `lab-v1` fields. The three Markdown files are
Vietnamese-first content candidates paired only by the I5-07-owned verifier; this pairing does not
create a shared schema/registry field. The verifier and tests are non-mutating/read-only over
Issue #6 inputs. The activation document may mark only `lake-contracts-check` implemented with
`fitness-result-v2`. No lesson manifest, shared contract set, portal catalog, runner operation or
completion/progress authority is changed.

## Stage A exact verification commands — 12 entries

1. `python3 -m unittest discover -s learning/labs/data-platform/tests -p 'test_*.py'`
2. `python3 learning/labs/data-platform/verify_stage_a.py check`
3. `python3 learning/labs/data-platform/verify_stage_a.py self-test`
4. `make -f mk/issue-5/i5-07.mk lake-contracts-check`
5. `make lake-contracts-check`
6. `make learning-contracts-check api-contracts-check evidence-contracts-check`
7. `make lesson-check LESSON=promotion-trust`
8. `make evidence-verify EVIDENCE="$EVIDENCE_LOCATOR"`
9. `make data-contracts-check migration-contracts-check`
10. `make help`
11. `git diff --check`
12. Run the following clean-checkout smoke as one command block with `STAGE_A_HEAD` set to the
    exact reviewed head:

```bash
smoke_parent="$(mktemp -d)"
smoke_root="${smoke_parent}/checkout"
git worktree add --detach "$smoke_root" "$STAGE_A_HEAD"
make -C "$smoke_root" -f mk/issue-5/i5-07.mk lake-contracts-check
git worktree remove --force "$smoke_root"
rmdir "$smoke_parent"
```

The released #8 runtime admission variables and `EVIDENCE_LOCATOR` must come from the same fresh
run; missing runtime/evidence is failure. Commands run serially, cloud-free, with no retained
generated state required for the detached smoke.

## Dependency-derived path templates

Templates chỉ mô tả cách amendment lấy giá trị từ release thật; chúng không cấp authority hiện tại.

| Scope | Template | Resolver |
|---|---|---|
| Lab content | `learning/labs/data-platform/<stable-lab-id-from-issue-8-contract>/**` | Exact #8 contract release |
| Verifier | `<verifier-root-from-issue-8-release>/data-platform/<stable-lab-id>/**` | Exact #8 contract release |
| Runner binding | `<runner-registry-path-from-issue-9-release>` + released command IDs | Exact #9 runner release |
| Data/pipeline seam | `<exact-path-listed-in-serialized-lease>` | Human/owner lease record |
| Portal publication | `<renderer-and-route-paths-from-issue-10-stage-b-release>` | Passing merged runner-backed #10 Stage B handoff |
| Blast radius | `<exact-command-list-published-by-dependency-release>` | #6/#8/#9/#10 handoff comments/artifacts |

Fixed issue-owned destination `mk/issue-5/i5-07.mk` may receive only the Stage A
`lake-contracts-check` recipe. Remaining I5-07 recipes wait for their runner/service stages. Root
`Makefile` stays protected.

Released #8 completion/evidence schemas/readers are now Stage A read-only authority. #9 private
runner registry/API remains unavailable; #10 static renderer/routes are reference-only until its
runner-backed Stage B release. Issue #12 chỉ nối qua extension point được release và lease; cấm
copy schema, parallel registry, duplicate truth, invented compatibility adapter hoặc
browser-to-command fallback.

## Amendment protocol per stage

1. Fetch live remote read-only; require issue release state and exact 40-hex handoff SHA.
2. Prove SHA is an ancestor of the intended implementation input and that released artifacts
   exist at that SHA.
3. Record SHA, tree/blob hashes, exact consumed paths, exact blast-radius commands and declared
   compatibility/migration requirements.
4. Recompute [protected baseline](./protected-baseline-manifest.md); STOP on unexpected drift.
5. Obtain any serialized shared-contract/data/pipeline lease with exact paths and expiry/owner.
6. Run the Standard-lane combined dependency/readiness amendment once, then use focused review
   (`Critical=0`, `Important=0`), fresh tests, PR/CI and merge/post-merge smoke in one delivery
   context.
7. Prove the exact amended head from a pristine detached checkout with no pre-existing generated
   or runtime evidence; use only dependency-released setup/test commands and record any required
   cache/offline assumptions instead of relying on local machine state.
8. Record observability and docs/release impact as `none` or exact released schema/owner/path/gate;
   no implicit log format, docs writer or release-manifest mutation is authority.
9. Cook only the amended stage. Later stages remain blocked and their fields remain empty.

## Exact remaining blocker/handoff fields

| Stage | Required future handoff | Fields that must remain empty now |
|---|---|---|
| B | Merged Issue #9 runner release SHA, runner registry/workspace/evidence paths and commands; bounded lease with owner, exact paths, input SHA, start/expiry and non-overlap | `dependencyIssue9ReleaseSha`, Stage B paths/commands, lease record |
| C | Merged runner-backed Issue #10 Stage B SHA, renderer/API/route extension paths and real E2E commands | `dependencyIssue10StageBMergeSha`, Stage C paths/commands |

## STOP conditions

- Branch/label/plan commit substituted for released dependency SHA.
- Any dependency path or command guessed before release.
- #8 contract, #9 runner, #10 Stage B journey or serialized lease mismatch.
- Concurrent shared-contract/pipeline writer.
- Protected path/tree drift without separately approved seam.
- Dirty/wrong base, unresolved merge ancestry, unresolved Critical/Important review finding,
  failed fresh test/CI or failed post-merge smoke.
