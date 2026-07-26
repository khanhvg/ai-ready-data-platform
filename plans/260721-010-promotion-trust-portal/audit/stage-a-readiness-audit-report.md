---
title: "Issue #10 Stage A post-binding release-readiness audit"
auditDate: "2026-07-22"
inputSha: "d79bcd0c3894c2b8477f1188faadc08f77480087"
integrationReleaseSha: "5644f01b4c0443a81f3af0bcce80f44c847cd986"
integrationTreeSha: "a38594d420fe7df2b30265a8a72bb5fad1698012"
bindingSha256: "03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0"
verdict: STAGE_A_READY
cookScope: stage-a-static-portal
stageB: blocked-on-issue9
cloudAction: none
---

# Issue #10 Stage A Post-Binding Release-Readiness Audit

## Verdict

`STAGE_A_READY` for one bounded static portal cook from final released integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986`. The exact authority is 33 create-only tracked paths,
18 command surfaces, and 85 consumed release paths. Stage B is `blocked-on-issue9`; its file,
command, dependency, transport, action, evidence, reset, progress, and completion authorities are
all `[]`.

This is planning/cook readiness only. It does not claim that the portal was implemented, built,
run, reset, evidenced, completed, reviewed, approved, merged, or released. The product claim is a
meaningful Vietnamese-first static Stage A portal slice, not the complete learning product.

## Frozen Input and Independence

| Check | Result |
|---|---|
| Required worktree/branch | Exact requested Issue #10 worktree on `plan/issue-10-promotion-portal` |
| Local HEAD at start | `d79bcd0c3894c2b8477f1188faadc08f77480087` |
| Configured upstream after fresh fetch | exact input |
| Remote-tracking branch after fresh fetch | exact input |
| Live GitHub branch head | exact input |
| Initial tracked/untracked/index state | clean |
| Auditor runtime | Herdr `audit-issue10-postbinding-readiness`; Codex `gpt-5.6-sol`; reasoning `xhigh` |
| Write authority | Issue #10 plan/readiness artifacts only |

No portal/test implementation, feature-worktree write, dependency-worktree write, merge,
approval, runner, browser, package install, container/engine, cloud, AWS, Terraform, or destructive
action occurred.

## Active Worktrees, Agents, and Writer Overlap

- This auditor was the only writer in the Issue #10 plan worktree.
- The old `feature/issue-10-portal-stage-a` worktree is clean at
  `515bd919da243dd9f30395d3deef02f7819cd0a1`, has no Herdr/Codex process in that worktree, and is
  ahead of/behind the now-advanced integration. It is preserved as non-authoritative pre-binding
  history; this audit does not rely on a no-product reconciliation of its commits.
- Issue #9 plan and cook worktrees were clean at
  `308c736f8811ac9aeaf41ad5b27dea07d2e60b2e` and
  `9eb31075aeb0e7b974ad15645460ab4987570f20`. Neither is a release.
- Herdr also exposed Issue #11 activity in its separate worktree and a completed Issue #8 release
  agent in the Issue #8 worktree. No active agent owned or changed an Issue #10 Stage A path.
- No integration branch worktree, shared-contract lease, root-Make writer, portal writer, or
  stopped-cook writer overlapped this plan audit.

`OWNERSHIP_OVERLAP=pass`.

## Final Remote Release Proof

| Authority | Exact result |
|---|---|
| Integration release M | `5644f01b4c0443a81f3af0bcce80f44c847cd986` |
| Ordered parents | `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`, `12e17427076fb31de85534bfbbbedca7e901e76c` |
| Released tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` |
| Tree inventory | 921 entries; listing SHA-256 `a6681b3e7ee932fbd29728bc3f649017e57e6980871a3de9def9cb3ac318d9fe` |
| Issue #8 | CLOSED/`shipped`; I5-03 shared-contract lease released |
| Handoff | Issue #10 comment `5047964988`; release records `5047954510`, `5047954805` |
| Issue #9 | OPEN; plan/cook provenance only; no reviewed/merged/pristine runner release |

The Issue #8 release reports a brand-new tracked-files-only pristine verification directly at
M/tree: focused binding `11/11`, invalid binding family `8/8`, full learning `67/67`, Stage A
invalid `65/65`, final public behaviors `4/4`, Vite `5/5`, API `16`, evidence `13/13`, data
`19/19`, migration `1/1`, protected/S3/resource/cleanup PASS. No repository checks are configured;
this audit does not turn their absence into a CI-success claim.

## Shared Binding and Dependency Closure

- Shared binding: `learning/bindings/vite/promotion-trust-v1.json`.
- Version/binding ID: `promotion-trust-vite-binding-v1`.
- Binding SHA-256: `03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0`.
- Binding schema SHA-256:
  `74035baee08b378e46421466333d6933d1bad820337acd1b80a633d236173a43`.
- Stage A contract-set SHA-256:
  `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`.
- Full consumed catalogue: 85 unique paths, with Git blob, byte length, and SHA-256 recomputed from
  M. The final tree changed three previously consumed bytes (`check.py`, `schema.py`, Issue #8
  Phase 5) and added 12 binding/schema/adapter/test/invalid-fixture paths.
- Seven Issue #6/protected identities, exact #7 Vite graph, Python lock, root Make include seam,
  and all nine I5-05 command reservations remain byte-exact.

The portal consumes the shared binding directly after released public validation. It creates no
portal-local binding, alias/mapping table, copied schema, generated binding type, default,
transform, canonicalizer, or invented module/identifier truth. The three non-identity mappings
remain exclusively in the released binding. `DEPENDENCY_BINDING=pass`.

## Stage A Scope Reconciliation

The historical scope was 34 creates and 18 commands. Removing
`apps/learning-portal/release-binding.stage-a.json` is the only product-path delta required by the
shared release. The new authority is exactly 33 creates, zero modifies, zero deletes, and the same
18 commands. Every one of the 33 paths is absent from M/tree.

The scope touches only a bounded subset of `apps/learning-portal/**` and
`mk/issue-5/i5-05.mk`. It does not overlap shared/Issue #7/Issue #8 source, root Make, data,
fixtures, runner, README/docs, CI, cloud, AWS, or Terraform paths. Generated `node_modules`,
`dist`, Playwright, runtime, log, screenshot, trace, and review files remain ignored run-owned
state with no authority.

`STAGE_A_SCOPE=33-create/0-modify/0-delete/18-commands/85-consumed-release-paths`.

## Meaningful Static Product Slice

Stage A provides exactly 13 canonical public documents: `/`, `/module`,
`/lesson/promotion-trust`, and ten routes for released narrative-step IDs. `/module` is a
presentation-only view and introduces no module identifier. The portal is Vietnamese-first,
keyboard/focus/overflow aware, desktop+narrow responsive, axe-gated, and complete without
JavaScript. Provider/catalog/router/static-render seams can accept later released #11/#12
identifiers without inventing their content now.

The portal renders the four independent grains through the released binding, keeps
`PROMOTION_HEADLINE_INSUFFICIENT` distinct from runner unavailability, and shows only
`insufficient-evidence / no-common-grain`. Every route visibly says the slice is not the complete
learning product and emits machine-readable non-claim attributes: runner unavailable, execution
disabled, reset not-run, fresh evidence false, progress disabled, completion disabled.

## TDD, Browser, and Build Closure

- RED begins at final M or a tests-only descendant in the fresh v2 worktree; a detached clean
  checkout at the same tree must also pass without branch/upstream assumptions.
- Released invalid fixtures traverse the real public binding adapter and exact eight failure
  codes. Additional real-adapter cases cover missing/extra grain, lossy/cyclic alias, version,
  type, unknown field, substitution, path, special-file, descriptor race, and authority state.
- Portal RED then traverses the real adapter, provider/catalog/router, static/React render,
  server/lifecycle, and exact public routes. Missing tools/imports and copied predicates are not
  valid RED.
- Ignored, generated, untracked, other-worktree, environment-selected, or absolute-path fixtures
  cannot satisfy dependency or RED authority.
- Production build runs twice with deterministic static output, no source maps, at most 128
  regular files, 1 MiB each and 16 MiB aggregate.
- One Chromium journey, one worker and zero retry covers 1280x800 and 360x800, exact fixture
  `promotion-trust-small-42-v1`/seed 42, all 13 routes, history/reload, keyboard/focus/overflow,
  reduced motion, axe zero Critical/Serious, JavaScript-disabled parity, CSP/console/network/
  storage absence, and machine-readable non-claims.
- Lifecycle and visual output retain exact process/time/file/byte/artifact ceilings, scoped
  cleanup twice, foreign-state preservation, and rollback of only 33 tracked additions.

`TDD=pass`; `VISUAL_ACCESSIBILITY=pass`; `RESOURCE_FEASIBILITY=pass` at planning readiness.

## Security:S3 and Stage B Boundary

All PTP-S3-01..14 controls remain mandatory. Stage A has one GET/HEAD-only loopback static
process, exact Host/path/CSP/XSS/type/size/alias bounds, no body/API/CORS/session/cookie/storage/
service-worker/network/credential surface, and no runner import/probe/start/call. It exposes no
raw command, argv, path, URL, SQL, shell, engine, host bridge, mutation, evidence, progress, or
completion path. `S3=pass` at planning readiness.

Stage B remains blocked on an exact reviewed, merged, pristine Issue #9 release compatible with
the pinned Issue #8 release. Current Issue #9 plan/cook heads are not adapters. No fake execution,
synthetic success/evidence, browser-to-host/engine command, local-shell fallback, reset,
verification, evidence, progress, or completion action is authorized. `STAGE_B=blocked-on-issue9`.

## Fresh Implementation Worktree Decision

Create a new `feature/issue-10-portal-stage-a-v2` branch/worktree directly from M after this output
is published. Cherry-pick the ordered Issue #10 plan-only commits `ad87c3f`, `e2bba33`, `4a36bab`,
and `d79bcd0`, followed by the published readiness commit identified in the Issue #10 handoff.
Prove the resulting plan-directory tree equals the published output and that no product path
changed before RED. Preserve the old stopped worktree without reset, rewrite, deletion, or reuse.

## Validation and Publication Gates

Prepublication validation passed:

- CK 4.5.2 strict JSON: `valid: true`, zero issues, seven phase links resolved. CK JSON status is
  correctly `pending`, with seven pending phases and zero implementation progress.
- All 52 Markdown links resolve; all 30 anchored links target existing headings across 17 plan
  Markdown files.
- No unresolved placeholder/future SHA occurs in current authority. The sole brace template is
  confined to the immutable Session 1 validation snapshot's deferred Stage B evidence example;
  it is not Stage A authority.
- The 85-row dependency catalogue has 85 unique paths, and every Git blob, byte length, and
  SHA-256 matches M. The seven protected rows also independently match M.
- The 33-row create allowlist is unique, equals the Phase 1–4 union, and every path is absent from
  M. The 18 unique command rows exactly equal the verification sequence. The released registry
  has nine exact I5-05 rows, all `future-owner`/`not-runnable`, bound to the future fragment and
  `fitness-result-v1` before cook activation.
- Catalogue closure is exact: 13 routes, seven non-claim attributes, 11 Stage A requirements, ten
  scenarios, 14 Stage A REDs, eight released invalid-binding cases with matching released codes,
  14 S3 controls, ten functional plus eight non-functional trace rows, and 12 risks.
- Visual, accessibility, deterministic fixture, no-JavaScript, evidence, cleanup, rollback, and
  process/time/file/byte ceilings agree across the amendment, threat model, verification plan,
  and Phase 4. Stage B remains an empty-authority fail-closed gate in every current phase.
- The working diff is 15 Issue #10 plan/readiness files and zero paths outside the plan directory;
  private-path and high-confidence secret scans are empty, and `git diff --check` passes.
- The whole-plan stale-term sweep found no current contradiction. References to the old base,
  34-path scope, and portal-local binding occur only as final-release ancestry or explicitly
  labelled historical/superseded facts.

Publication still requires this focused plan-only commit, push, and fresh local/upstream/live
equality before the Issue #10 comment and label transition; the issue handoff records those
post-commit facts because a commit cannot embed its own SHA.

On PASS, remove `ready for plan audit` and add `ready to cook` for Stage A only. Issue #10 remains
open and Stage B explicitly blocked. Any failed publication gate changes the verdict to BLOCKED
and preserves the current labels.
