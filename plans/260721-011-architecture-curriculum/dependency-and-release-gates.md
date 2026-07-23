# Dependency and Release Gates

## Current Authority

The v4 plan passed fresh independent validation and a separate fresh readiness audit. Readiness
added only bounded plan-level controller-environment and released-byproduct cleanup closure; the
frozen product scope did not change. Historical v1/v2/v3 validation and readiness reports remain
immutable evidence for old SHAs and cannot authorize this contract. The exact pushed readiness
output is the only Stage A v4 cook input and is attested externally after push.

| Authority | Exact identity | Disposition |
|---|---|---|
| Authorized author input | `287dc08546f7013ca8c187b318e0a2f7cf832e55` | Required initial local/upstream/fresh-live equality |
| Current integration release | `5644f01b4c0443a81f3af0bcce80f44c847cd986` | Direct v4 base and required ancestor |
| Integration tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` | Non-plan byte authority |
| Issue #8 Stage A contract release | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9` | Read-only 21-contract authority inherited by integration |
| PR #30 review | [comment 5050486239](https://github.com/khanhvg/ai-ready-data-platform/pull/30#issuecomment-5050486239) | Eight findings; prior v3 authority fails |
| v4 recovery | [comment 5050513064](https://github.com/khanhvg/ai-ready-data-platform/issues/11#issuecomment-5050513064) | Plan-only reconstruction from integration |
| Fresh v4 validation input | `dfd8e4c7704de5e1392d1028f5a25757a3e77166` | Independently validated; containing output is attested after push |
| Fresh v4 validation report | [validation/260723-stage-a-v4-independent-validation-report.md](./validation/260723-stage-a-v4-independent-validation-report.md) | PASS with one bounded plan-only fix; not readiness |
| Fresh v4 readiness input | `68bfc6b53ced963997266dbc4960aff4a8ca52d4` | Exact clean local/upstream/live validation head |
| Fresh v4 readiness report | [audit/stage-a-readiness-audit-report.md](./audit/stage-a-readiness-audit-report.md) | `READY_TO_COOK`; recovered audit plus fresh completion, with exact containing output attested externally |
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

Status is PASS with one bounded plan-only fix. The fresh xhigh validator started from exact clean
input `dfd8e4c7704de5e1392d1028f5a25757a3e77166`, proved local/upstream/fetch/live equality,
re-read PR #30 and v4 authority, and validated the whole plan rather than only the correction
report. Reproduced checks include:

- CK 4.5.2 strict plan validation and status;
- links, anchors, frontmatter, placeholders, unresolved/future SHA claims;
- direct integration ancestry and plan-only diff;
- exact 50/16/22/82/12/20/11/8/5 counts and catalogue closure;
- repository-level real-state RED and exact callable/CLI/Make routes;
- runtime root/interpreter/private-mode/closed-environment consistency;
- template lifecycle, visible parity, module progression, governance bridge, evidence truth;
- 33/33 protected and 21/21 released identities; and
- private-path/secret/S3/diff consistency.

The independent result is the
[Stage A v4 validation report](./validation/260723-stage-a-v4-independent-validation-report.md).
Its containing output identity is attested externally after push to avoid a self-referential SHA.
The author report was input, never the independent verdict.

## Gate A3 — Fresh Readiness

Status is PASS. A role-separated fresh reviewer bound exact pushed validation head
`68bfc6b53ced963997266dbc4960aff4a8ca52d4`, literal-admitted the 16-command runtime, and closed two
bounded plan-only gaps: the exact `env -i` controller table and actual released `.artifacts`
byproduct copy/cleanup layouts. After that session ended at context compaction without a semantic
verdict, a fresh xhigh completion session preserved and reviewed all eight edits and repeated the
live dependency/remote/diff/count/security/whole-plan matrix. The tracked readiness report and its
externally attested containing output are the authority; neither interrupted transcript is.

## Gate A4 — Stage A Cook and Review

Status is authorized but not started. The cook may follow only the exact 7-path scaffold, direct-child
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
