# Dependency and Release Gates

## Current Authority

The v4 plan is corrected but unvalidated. Implementation authority is `none`. Historical v1/v2/v3
validation and readiness reports remain immutable evidence for old SHAs and cannot authorize this
contract. The only next gate is fresh independent plan validation; a later fresh readiness audit
must bind its exact pushed result before any cook.

| Authority | Exact identity | Disposition |
|---|---|---|
| Authorized author input | `287dc08546f7013ca8c187b318e0a2f7cf832e55` | Required initial local/upstream/fresh-live equality |
| Current integration release | `5644f01b4c0443a81f3af0bcce80f44c847cd986` | Direct v4 base and required ancestor |
| Integration tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` | Non-plan byte authority |
| Issue #8 Stage A contract release | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | Read-only 21-contract authority inherited by integration |
| PR #30 review | [comment 5050486239](https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239) | Eight findings; prior v3 authority fails |
| v4 recovery | [comment 5050513064](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064) | Plan-only reconstruction from integration |
| Stage B dependency | Passing merged Issue #10 real journey and released renderer | Missing; Stage B blocked and empty |

`c07c9a080be7be88447aac497bdf0a2b5fddd020` and every failed v1/v2/v3 product/test/render/evidence
head are explicit non-authorities. They must not be ancestors, cherry-pick sources, copy sources,
fixture sources, or evidence sources for v4 implementation.

## Gate A1 — Direct Integration Derivation

The plan correction branch, independent validation commit, and readiness commit must be a linear
plan-only descendant of exact integration `5644f01b…`. The eventual exact readiness head is
`cookInput`. Before C1:

- local HEAD, upstream, newly fetched remote, and live GitHub branch equal `cookInput`;
- `git merge-base --is-ancestor 5644f01b… cookInput` succeeds;
- direct `5644f01b… -> cookInput` name-status contains only
  `plans/260721-011-architecture-curriculum/**`;
- all exact 50 future paths are absent;
- all 33 protected and 21 released identities equal integration per path/blob/bytes; and
- failed feature commits are not ancestors and no patch/byte provenance names them.

The [amendment derivation](./stage-a-release-amendment.md#integration-derivation-and-byte-equality)
defines the three closed ranges. A merge, no-ff reconciliation, alternate base, undocumented
conflict resolution, or product/test/evidence copy fails this gate.

## Gate A2 — Fresh Independent Plan Validation

Status is pending. A fresh xhigh validator must start from the exact pushed v4 output in a clean
checkout, prove local/upstream/fetch/live equality, re-read PR #30 and v4 authority, and validate
the whole plan rather than only the correction report. Required checks include:

- CK 4.5.2 strict plan validation and status;
- links, anchors, frontmatter, placeholders, unresolved/future SHA claims;
- direct integration ancestry and plan-only diff;
- exact 50/16/22/82/12/20/11/8/5 counts and catalogue closure;
- repository-level real-state RED and exact callable/CLI/Make routes;
- runtime root/interpreter/private-mode/closed-environment consistency;
- template lifecycle, visible parity, module progression, governance bridge, evidence truth;
- 33/33 protected and 21/21 released identities; and
- private-path/secret/S3/diff consistency.

The validator publishes a new plan-only report and exact-head attestation. It may return PASS or
BLOCKED/FAIL. The author report is input, never the independent verdict.

## Gate A3 — Fresh Readiness

Status is blocked on Gate A2 PASS. A different fresh reviewer binds the exact pushed validation
head, repeats live dependency/remote/diff/count/security checks, and decides whether one Stage A
cook may start. Readiness must not infer cook authority from a label, author comment, historical
report, or validation alone. Only a later explicit passing readiness output may fill
`stageAImplementationInputSha`.

## Gate A4 — Stage A Cook and Review

Status is blocked on Gate A3. The cook may follow only the exact 7-path scaffold, direct-child
5-path tests/fixture, real repository RED, and 38-path semantic complement chronology. It creates
exactly 50 product/test paths and no other tracked path. Cook visual evidence is self-inspection,
not independent review. After bounded handoff, a fresh implementation reviewer uses a detached
checkout of the exact pushed candidate and creates separate evidence. Repository-authorized human
exact-head approval remains required before a future merge; this plan grants neither action.

## Stage B Gate

```yaml
stageBStatus: blocked-on-passing-merged-issue-10-journey
stageBImplementationFileAllowList: []
stageBImplementationCommandAllowList: []
stageBDependencyReleaseShas: []
stageBPortalRendererPaths: []
```

Stage B cannot inherit Stage A validation/readiness/cook authority. It requires a passing merged
Issue #10 real journey and released renderer, then a new exact amendment, independent validation,
and readiness. Until then no portal, runner, executable lab, browser command, reset, progress,
completion, or learner-evidence claim is admitted.

## Hard Stops

Stop on remote inequality, wrong branch/base/tree, a non-plan derivation path, an existing one of
the 50 paths, protected/released drift, failed-feature ancestry or copied bytes, changed count,
missing tool, skipped check, secret/private-path issue, cloud/container/AWS/Terraform action,
feature-worktree write, merge, approval, or nonempty Stage B authority.
