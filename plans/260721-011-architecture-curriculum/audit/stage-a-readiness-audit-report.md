# Issue #11 Stage A v4 Recovered Readiness Audit

## Verdict

**READY TO COOK for the whole Stage A v4 plan.** The exact audited input is clean commit
`68bfc6b53ced963997266dbc4960aff4a8ca52d4`. The final plan/readiness delta contains the eight
recovered plan files plus this tracked report. It changes no product, test, runtime, protected,
released, or dependency path.

The two bounded readiness corrections are valid and do not weaken any requirement:

1. the command controller now has an exact `env -i` environment and interpreter boundary; and
2. actual released-command `.artifacts` evidence/workspace byproducts now have closed
   full-directory copy, verification, ownership, retention, and exact-source cleanup rules.

No frozen count, create-only path, command shape, RED assertion, template/module/trace/render
contract, promotion result, Stage B boundary, or cook chronology changed. This verdict grants only
`stage-a-v4-whole-plan` cook authority. It is not product implementation, product evidence,
independent implementation review, approval, merge, release, runner, container, or cloud authority.
The containing output SHA is recorded externally after commit and push rather than self-referenced
here.

## Recovery Provenance and Runtime

The first fresh readiness session was Herdr/Codex thread
`019f8b7e-f873-7872-92e7-797b417234fa`, using Herdr `0.7.3`, Codex CLI `0.144.1`,
`gpt-5.6-sol`, and reasoning effort `xhigh`. Its ignored transcript
`.hermes/logs/claudekit/issue-11-stage-a-v4-readiness-audit.log` is 1,477,555 bytes with SHA-256
`b8d750773802b5875557306b41936bcdc55e27f16176d54f504670c70a0bc0ec`. It ended immediately after
the final bounded validator emitted only:

```text
audit/stage-a-readiness-audit-report.md:placeholder marker
threat-model-and-security.md:private-locator-like wording
```

The next record is `context compacted`; there is no semantic verdict, commit, push, issue comment,
or label transition in that transcript. Its ignored report draft never became authority.

This completion is a distinct fresh Herdr/Codex thread
`019f8cd8-7ca0-7753-ae05-a2175c6a31e7`, again using Herdr `0.7.3`, Codex CLI `0.144.1`,
`gpt-5.6-sol`, and reasoning effort `xhigh`. Its live ignored transcript is
`.hermes/logs/claudekit/issue-11-stage-a-v4-readiness-recovery.log`; because it continues through
publication, this tracked report does not claim a final transcript hash.

At takeover, the worktree matched the recovery contract exactly: eight modified files, 171
insertions, 46 deletions, all under this plan directory, with no product/test change. The
continuation inspected bounded hunks for every file, preserved the technical corrections, replaced
only stale status/provenance, fixed both scanner findings unambiguously, and reran the current
validation matrix.

CK is CLI `4.5.2` with kit `engineer@v2.20.0`. Current host feasibility is 16 GiB RAM, eight
logical CPUs, more than 24 GiB free disk, and file-descriptor ceiling 1,048,575. No container,
browser, native GUI, AWS, Terraform, provider, or cloud action was performed.

## Exact Input, Integration, and Writers

Before the recovered diff, all identities were equal:

| Identity | Exact value |
|---|---|
| Branch | `plan/issue-11-architecture-curriculum` |
| Local input | `68bfc6b53ced963997266dbc4960aff4a8ca52d4` |
| Configured upstream | `68bfc6b53ced963997266dbc4960aff4a8ca52d4` |
| Fresh live branch | `68bfc6b53ced963997266dbc4960aff4a8ca52d4` |
| Integration release/live branch | `5644f01b4c0443a81f3af0bcce80f44c847cd986` |
| Integration tree | `a38594d420fe7df2b30265a8a72bb5fad1698012` |

Integration is the exact merge base and ancestor. The ten post-integration commits are linear,
single-parent, and plan-only. The direct integration-to-input diff contains zero non-plan path.
Failed Issue #11 heads `0f765d36958a2b97f2b95ccb23e3830aa0dd685f`,
`482591de3838589ccc37177c71d9e87f6e01ca14`, and
`eebcce4a3ae8327b189297378456ea6293927654`, plus
`c07c9a080be7be88447aac497bdf0a2b5fddd020`, are not ancestors. Their worktrees remain immutable
failed history and had no active cwd holder.

Herdr/process inspection found no Issue #11 product writer. The only Issue #11 live process is
this plan/readiness completion. Concurrent Issue #9 runner and Issue #10 portal cooks use their own
worktrees and disjoint leases.

All 50 future paths are absent at integration and input. All 33 protected identities match
integration/input/working bytes by Git blob. All 21 released contracts match the descriptor
content SHA-256 and integration/input/working blobs; the descriptor blob is
`0a85119871f769a17dc464591bf0623524e9a97e` in all three states.

## Closed Catalogues and Ownership

Fresh machine parsing returned:

| Catalogue | Result |
|---|---:|
| Stage A tracked writes | 50 unique, create-only, all absent |
| Chronology | C1 `7`, direct-child C2 `5`, semantic complement `38` |
| Literal top-level commands | 16 unique |
| Repository RED | 22 families / 82 unique exact codes |
| Template registry | 12 exact active `1.0.0` IDs |
| Curriculum modules | 20 exact IDs and prerequisite vectors |
| Critical flows / conceptual bridges | 11 / 8 |
| Source-derived expansion views | 5 |
| Protected / released identities | 33 / 21 |
| OpenAPI operations / released AsyncAPI channels | 16 / 0 |

There is no modify, delete, or third tracked class. The 50 write paths, 33 protected paths, and 21
released contracts are pairwise disjoint.

Fresh lease sampling found:

- Issue #9 is open at `ready to cook`, plan head
  `308c736f8811ac9aeaf41ad5b27dea07d2e60b2e`, with an active runner cook. Its
  `apps/lab-runner/**` and `mk/issue-5/i5-04.mk` write lease overlaps none of Issue #11.
- Issue #10 is open at `ready to cook` only for static Stage A v3, plan head
  `8c77957ad3be84dc97e4633cdafd898ea9e431fa`, with an active portal RED checkpoint. Its exact 33
  `apps/learning-portal/**` / `i5-05.mk` paths overlap none.
- Issue #12 remains open at `ready for plan audit` with empty current implementation authority;
  its future `learning/labs/data-platform/**` / `i5-07.mk` write lease overlaps none.
- Issue #13 remains open at `ready for plan audit` with dependency-empty profile/Compose
  authority; its future profile paths and `i5-08.mk` overlap none.

Issue #12/#13 plan histories contain the released shared contracts as ancestry/read-only bytes,
not write authority. Exact Issue #11 write overlap is zero for every sampled lane.

## Repository-Level RED Cookability

The [normative amendment](../stage-a-release-amendment.md) closes real scaffold-first TDD:

1. C1 creates exactly seven semantics-free callable/router paths.
2. Direct-child C2 creates four complete tests plus one fixture, unchanged through first GREEN.
3. Complete mode-0700 repositories and initialized Git fixtures reach `check_repository()`,
   `_verify_repository()`, `_toolchain_verification()`, and `_repository_handoff()`, plus matching
   public CLI/Make routes.
4. Only after contemporaneous repository RED may C3+ add the 38 semantic paths.

Every one of the 82 mutations changes real file/schema/template/instance/trace/LikeC4/topology/
visible-render/process/resource/raw-evidence/index/mode/type/link/porcelain state. Resource cases
really spawn descendants, ignore TERM, allocate memory, flood output, and create files. The
harness strips expected codes, IDs, and assertion prose before invoking production.

Abstract Boolean/dictionary predicates, expected-code echo or fallback, fixture-ID dispatch,
hard-coded pass/fail, predicate-only checking, mocks, monkeypatches, skips, missing
tool/import/path failures, and test-only behavior are explicitly rejected. Exact source, tree,
fixture, tool, ancestry, raw output, result, resource, render, and cleanup evidence is mandatory.

## Literal Commands and Resource Admission

All 16 literal command lines are unique and pass Bash syntax. Current target, interpreter, lock,
module, and future-owner routing resolves without an undocumented path:

- command 2 is the sole admitted host `python3.12` venv creation;
- commands 3, 4, 9, 10, and 16 use exact `$I11_RUNTIME/venv/bin/python`;
- released Make commands preserve their frozen host launchers while admitting the same candidate;
- future commands bind only `learning.curriculum.tools.architecture_expansion` and `i5-06.mk`;
- caller Make, Python, proxy, loader, cloud, authentication, Node/npm, and tool overrides are
  absent under the exact `env -i` table.

The interrupted session’s real private replay used one mode-0700 parent/candidate, Python 3.12.3,
the full hash-locked install, `pip check`, released admission, and exact interpreter path. It took
26 seconds, installed about 220 MiB, and executed commands 1–5 plus 15; released routes 6–8 and
13–14 were dry-resolved, while future 9–12 and 16 correctly remained absent at input.

That replay exposed real command-registry evidence creation. Source inspection then closed all
command-registry, learning-contract, architecture workspace/check/render, and renderer-transient
layouts. Complete evidence directories must be copied and verified before nonce/purpose/path/
device/inode/manifest-bound source cleanup. Pre-existing bytes cannot be adopted or deleted; any
unlisted byproduct or residual byte fails handoff.

The plan ceilings remain feasible: focused tests 120 seconds; sequential bootstrap/two-render/
validation parent 180 seconds; 16 processes; 1.5 GiB aggregate RSS; 1 MiB command output; 4,096
staging files; 2.5 GiB tool plus staging bytes; 2 MiB final renders. Breach handling is owned-PGID
TERM, five-second wait, KILL survivors, wait/reap, and zero-descendant proof.

## Lifecycle, Governance, Render, and Evidence

- **Templates:** exactly 12 active rows; canonical hash; stable unique instance ID; exact
  registry/template/version/hash/compatibility reciprocity; monotonic successor, migration,
  rollback, readable predecessor, replacement, tombstone, and removal rules. Real duplicate,
  ID-drift, compatibility-drift, orphan, successor, and removal mutations are required.
- **Modules:** exactly 20 Vietnamese-first modules with module-specific starter, task, controlled
  failure, verify, evidence, reset, progressive hints, gated solution, trade-off reflection, and
  operations consequence. Learning signatures and meaningful bodies must be unique and
  progressively harder.
- **Flows/governance:** 11 ordered flows and eight conceptual-only bridges. `BR-GOVERNANCE-01`
  binds protected `learning.adapters -> retail` to
  `local.developer_host.adapters_instance -> local.developer_host.retail_instance`, with reciprocal
  `DYN-PUBLISH` and `DEP-AWS` identities. One-sided and both-wrong real mutations must fail; the
  physical `retail_iceberg` and logical `retail_duckdb` views remain separate.
- **Render:** all five views derive projection, DOT, raw Graphviz SVG, normalized visible SVG,
  fitted HTML, text, and manifest from locked LikeC4/DOT/WASM Graphviz only. Relation mutations
  must visibly change SVG/HTML/text and hashes. Two-run determinism, Vietnamese-first semantics,
  single numbering, parity, accessibility, and 1440/1024 fit are blocking.
- **Evidence:** bounded raw RED stdout/stderr remains retained and indexed, never replaced by a
  hash-only claim. Sanitized logs are separate and source-bound. Owner/privacy/media/count/size/
  mode/type/link/hash/index/resource/render/S3/byproduct/cleanup records are closed. Cook visual
  evidence is honest self-inspection with `independent=false`; future independent review is a
  separate immutable bundle.

Promotion remains exactly `decision=insufficient-evidence` and `reason=no-common-grain` against
the released schema. Stage A emits no runtime, reset, progress, completion, learner-evidence,
hosted, deployed, runner, container, or cloud claim.

## Stage B and Security Decision

Fresh Issue #10 state is not a renderer release. Its v3 plan is ready only to cook a static Stage A
portal. Rejected PR #29 remains open/unmerged at
`28a71ccc9028c61084a0aaed7fb1b426a62b6ba8`; no passing merged real journey or released renderer
exists. Therefore the exact Stage B implementation-file, command, dependency-SHA, and
portal-renderer arrays remain empty. Stage B is blocked independently of this Stage A verdict.

S3 rejects secrets, authentication material, host-private locators, caller environment dumps,
unsafe external/local references, unsafe SVG/HTML, account/resource IDs, executable cloud
commands, AWS/Terraform/provider actions, and stage/deployment claims. Evidence and temporary
state remain owner/mode/type/link/device/inode bounded. No product test, failed-history write,
feature-worktree write, container, runner, cloud, AWS, Terraform, PR, merge, approval, or release
action occurred.

## Final Validation Matrix

| Check | Result |
|---|---|
| `ck plan validate plan.md --strict --json` with CK 4.5.2 | PASS; `valid=true`, seven phases, zero issues |
| `ck plan status --json` with CK 4.5.2 | PASS; seven pending, zero in progress/completed |
| Markdown UTF-8/NFC/H1/local links/anchors | PASS; zero failures |
| Unresolved-marker and private-locator/secret scans | PASS; zero failures |
| Path/command/RED/template/module/flow/bridge/view catalogues | PASS; `50/16/22/82/12/20/11/8/5` |
| Template instance/compatibility and module lifecycle tokens | PASS |
| Render parity/freshness and evidence truth contract | PASS |
| Protected/released identity recomputation | PASS; `33/33`, `21/21` |
| Direct integration derivation and failed-head exclusion | PASS |
| Active ownership overlap | PASS; zero write overlap |
| S3 and resource feasibility | PASS |
| Stage B empty authority and Issue #10 release gate | PASS; blocked |
| `git diff --check` and plan/readiness-only scope | PASS |
| Whole-plan consistency | PASS |

The exact current CK commands were:

```text
ck plan validate plans/260721-011-architecture-curriculum/plan.md --strict --json
(cd plans/260721-011-architecture-curriculum && ck plan status --json)
```

## Handoff

After this report and the recovered plan corrections are committed and pushed, local HEAD,
configured upstream, remote-tracking, and fresh live branch must equal the external output SHA and
the worktree/index must be clean. Only then may Issue #11 move from `ready for plan audit` to
`ready to cook` for Stage A v4.

The next phase is `cook-issue11-stage-a-v4`. The cook must start from the exact pushed readiness
output and reproduce all preflight gates before any write. Fresh independent exact-head
implementation review and repository-authorized human approval remain later gates.

`READINESS_VERDICT=READY_TO_COOK`
`INPUT_SHA=68bfc6b53ced963997266dbc4960aff4a8ca52d4`
`RECOVERED_PLAN_FILES=8/8`
`INTEGRATION_RELEASE_SHA=5644f01b4c0443a81f3af0bcce80f44c847cd986`
`INTEGRATION_DERIVATION=pass`
`REPOSITORY_LEVEL_RED=pass`
`COMMANDS=16/16`
`TEMPLATE_LIFECYCLE=pass`
`VISIBLE_RENDER_PARITY=pass`
`MODULE_LIFECYCLE=20/20`
`GOVERNANCE_BRIDGE=pass`
`EVIDENCE_TRUTH=pass`
`STAGE_A_PATHS=50/50`
`PROTECTED_IDENTITIES=33/33`
`OWNERSHIP_OVERLAP=pass`
`S3=pass`
`RESOURCE_FEASIBILITY=pass`
`STAGE_B=blocked`
`COOK_SCOPE=stage-a-v4-whole-plan`
`CLOUD_ACTION=none`
`NEXT_PHASE=cook-issue11-stage-a-v4`
