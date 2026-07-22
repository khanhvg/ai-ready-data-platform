# Verification, Evidence, and Protected Assets

## Verification Boundary

The post-review author correction, fresh independent validation, and current readiness audit run
plan/static/link/dependency/protected-hash and installed-tool availability checks only. Readiness
passes for one whole Stage A cook after exact derived-input handoff; no new curriculum or expansion
implementation, lab, portal, native GUI, cloud, or Terraform gate ran.

Whole-product practical acceptance remains:

```bash
make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check
```

The exact Stage A command subset is in the
[Stage A amendment](./stage-a-release-amendment.md). Existing Issue #6 `architecture-check` and
`architecture-render` are read-only regression contracts; the isolated I5-06 adapter validates
five expansions separately without redefining owner code. `architecture-lab-e2e` and
the portal `architecture-visual-review` remain unavailable and cannot be reported pass. The five
new SVGs still have mandatory exact Stage A static visual machine gates and a bounded independent
human inspection at fitted widths 1440/1024.

## Planner-Only Check Set

| Check | Expected result |
|---|---|
| Branch/input/fresh remote | Author correction began at clean `1c62b68159ffc48cc2f063c137cb9072d8ed741f`; independent validation began with required branch and clean local/upstream/fresh-live equality at `788ea45331a34e34b0d330e568a39ee6c6566e63` |
| Live Issue #11 | Readiness input is OPEN with `ready for plan audit`; a passing readiness output moves only that label to `ready to cook`; risk high/TDD/S3/architecture/curriculum remain |
| Dependencies | #8 Stage A contracts remain pinned at `fecf6bb8…`; PR #28 is pristine-released at `5644f01b…`, non-overlapping and unconsumed by Issue #11; #10 not released and Stage B empty |
| `ck plan status` | Seven pending phases, valid frontmatter/dependency DAG |
| Markdown structure | One H1 per file; required sections; no empty placeholders |
| Local links/anchors | All repo-relative plan links and anchors resolve |
| Authority scan | Proposed exact 50 Stage A create paths, exact 16 commands and exact 7/5/38 chronology; Stage B lists empty; future implementation SHAs are explicit null blockers |
| Protected assets | Exact 33/33 Issue #6 SHA-256 and Git blob identities unchanged |
| Staged scope | Only `plans/260721-011-architecture-curriculum/**` |
| Formatting | `git diff --cached --check` passes |
| S3 scan | No secret/private-key/private-path/credential-bearing URL/runtime artifact |

## Protected Issue #6 Source Closure

Baseline remains identical at Stage A authority `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`,
clean v3 base `c07c9a080be7be88447aac497bdf0a2b5fddd020`, and current integration release
`5644f01b4c0443a81f3af0bcce80f44c847cd986`:

| Path | Git blob | SHA-256 |
|---|---|---|
| `architecture/likec4/specification.c4` | `1ceb46f11997750f49cef37382317bb908fc4fe1` | `96eeff0c7df9c04c0b3ca0e66aa0e53a05ba61bb3a3c95ec447f58a276643a32` |
| `architecture/likec4/model/people-and-systems.c4` | `7d1aa50047a510e82ddbbf793852b055f66d99e3` | `aaaca720b921db63526449147aa9c3ec67b7eb8dd70a301fd9f855e41e096d32` |
| `architecture/likec4/model/learning-platform.c4` | `9ba34a3ab49fba8d384f583dcb3988522bde72fb` | `33a224d2c6ae9e6e294b170741bb4184b6f6df2ef17956164354f1ed6abac9e3` |
| `architecture/likec4/model/data-platform.c4` | `8ef9d101579e15afabe4d85dbbb77e93a1d5399c` | `cba2985a8d60646a5e2a801eb9d08595d1081487efd6aa576c909fdd5249650d` |
| `architecture/likec4/model/local-deployment.c4` | `552e1af0dddb219f5c8fa0d7542678caf6ea1025` | `58e6fbc72e3ea41b826057a60f096f50a42b75550f1d35e0378edee59f0006ad` |
| `architecture/likec4/view-manifest.yaml` | `ff8f59a76440561d0de17a08b3d79fc580d2e043` | `1659c51389718f2799581550ab17fd31c4dd30639723d5b443ac088944178169` |

All source-closure bytes remain read-only. The readiness-authorized Stage A lease, after the exact
derived-input preflight, adds exact sources/rows only beneath the separate extension root; it may
not normalize, reserialize, or append the protected files.

## Protected Six Views and Renders

| View | Source blob / SHA-256 | SVG blob / SHA-256 | Text blob / SHA-256 |
|---|---|---|---|
| `C4-L0` | `bfea25cfd558b24e4c414cc72bfd89a37e400fe7` / `7fbe895e119e0f93ebfd68b671f051a29556936158bf9d4517ed316a1c5d8240` | `be91d0fc040f80f963cf7537b64e6aa2415a99c5` / `2d41f7e064c832a6b09a3715dfd4a0c8f9a3fe4c4789cac5ac8f3fd746e4b965` | `71ae460b0bab7bbd57315322cc5d3c80077f6ddd` / `e76a7da77a76fb0db70ba52d611c0c29343e5da2b6be2ed2a4231b8c4136fc2a` |
| `C4-L1` | `1bf7dcdd53850f64fd7010061d3466d1d4cfa7b2` / `8c843198efcccb5fe91788b9715c495d42a28454b2083e678ceeb5f00d9bb30d` | `0cdd574f8715a13f81e52aeaab2860b3fde4a946` / `59075f6e6a4041953137fe988c9e309090228742cc3beb5d114ed4b4f113f33d` | `f58c2e2938c9e320f56e40c43eaacdf5bab53615` / `6720223e2c09f2f346ad7fde6e600c72f75685332851caa495bda61ce4046d65` |
| `C4-L2-LOCAL` | `bfa8ea1346eaa0d967ce9536a5265b97bb611c21` / `a763d2820af704bc3986ab986df49d32f3acf76f29deb8022041857478578b5c` | `6640cfcc8a9a21f6ba84b0754c869dbbad467605` / `cdda1e25b0f735d5c0d54d88f18fa7ee51f39d24b8acdeaa97f5df0271232736` | `846a8fbe9f651cf0a8e725cf33a335bfb8c5e52b` / `03cbe8c843b52c20a4c4602dcd9dd7b1b54b4a3030ef07d1284ee24ba6b10b7c` |
| `C4-L3-RUNNER` | `abaaab3cea21a715f79e03ee38b25308c94f28e2` / `d7fa6a0869343b2db2e61543d2cdc4f00547ccd41e3a4073da6df3f9dbb82bb2` | `2a208518f2d6322d82c06eba299f2f9bae7002cc` / `65125df61b15955ab7ac1bae7ba9eb8d0679670cbac4afb586713f07b7691bfc` | `19f8302f9400bc562a19bc1d747f7db775f4cd73` / `4406e3dfcb88d9b37e59843cf7e06fd8564845e11f7fb2c515a59136c9ac110a` |
| `DEP-LOCAL` | `739ecbf21c320db256b32ef11d654e306e7ba1da` / `65b1490fbacb24b0809a524ae0ca22d9aa8db51ea155a36cd756759ccb9f4b83` | `8281d59a5e14676e2c0f22c46477dbbbf777f2b3` / `ece5a0bba7230cef7f69a9da8535fee2a06523bba0883d30b507684b8c028a0b` | `91f29582a751db05cfebb1b166bdd7b0c2e4c11e` / `7d0b2395ccfa329c2d4ff2349c328384117fc2878ccfadec7460795ebbcbb3d0` |
| `DYN-JOURNEY` | `49b04c042468151ff8ff76200853d870f27c2926` / `3681b76fcb2cee1a8b40f437b9015288cd1ce15c72c0250e98165716ea7104af` | `f4982f2cdd7a3b238d0ea7e78fa5eb786d3bcdc0` / `4c64440ff0040df7d75f148931b6758b4790fbab55e53af62ff735f08d3b3598` | `e76852f2e3f5326ba0b915c22ee0604ca087dd29` / `f55c05126387b5eb8a3ce20a9dd45bb0cd5fb33c9fc20aae75eff4a83db36a0b` |

`architecture/rendered/render-manifest.json` Git blob is
`c116d89ab5d1768894fce101e2eb1d1b9896e97c`; SHA-256 is
`7934c00f9f7bd772f0f2eec4730332b6b6a8b5907f2d7547673fbef9718a04e6`.

The Stage A lease preserves the six manifest rows’ ordered ID/key/type/audience/concern/
scope semantics and all original blobs. It does not permit any whole-file base manifest or
render-manifest change; extension manifests remain separate.

## Complete 33-Identity Gate

The 25 assets above (six source-closure files, six view sources, six SVGs, six text alternatives,
and one render manifest) plus the eight exact tool/lock/Make identities enumerated in the
[amendment](./stage-a-release-amendment.md#protected-tool-identities) form the protected set.
Sorted path/blob/content-hash inventory count must be exactly `33`; the independently reproduced
v2 review aggregate identity SHA-256 is
`0c6d42c8fb828ac5f47368c7c754233899929abc70c31ed853a18ecf9279f8f4`. The future v3 preflight,
every Stage A public command, rollback, and final handoff recompute all 33 from the clean base and
require byte/blob equality. The aggregate is supporting closure, never a substitute for the 33
individual comparisons.

## Deterministic Static and Semantic Render Tests

Stage A expansion tests must cover:

1. **Source validity:** format/reference/type/scope rules; required audience/concern/trace IDs.
2. **View-set partition:** protected six exactly unchanged; expansion IDs/keys/paths unique and
   exactly equal the authorized expansion set.
3. **Two-run determinism:** new isolated roots/caches; byte-identical normalized expansion SVG,
   text, and render-manifest semantic rows.
4. **Text semantics:** derived from computed model; ordered dynamic steps/deployment hierarchy;
   UTF-8/NFC/LF; one newline; no SVG scraping.
5. **Mutation sensitivity:** change each element/relation/order/technology/limitation/TBC class and
   require semantic/text/freshness hash change.
6. **Overlap:** no duplicate external/internal IDs, source/output locators, element identities,
   relationship tuples, or contradictory shared-boundary semantics.
7. **Freshness:** source closure, manifest row, tool lock, renderer/normalizer, projection, SVG,
   and text hashes agree; stale output fails.
8. **Safety:** no script, event handler, external image/URL, `foreignObject`, credential, account
   endpoint, absolute/private path, or hidden apply claim.
9. **Language/numbering:** Vietnamese-first title/primary labels; renderer is the sole ordinal
   source; text alternative contains exactly one matching order.
10. **Fitted readability:** exact 1440/1024 fit scales, 18/14/12 px font minima, aspect <=2.4:1,
    4.5:1 normal-text and 3:1 large/non-text contrast.
11. **Geometry:** computed painted/text bounding boxes prove no peer overlap, clipping, off-canvas
    content or relation endpoint; exact containment/outer padding thresholds apply.
12. **Independent inspection:** fresh reviewer records per-view readability, language, ordering,
    overlap, clipping and off-canvas disposition at both widths. This narrow static review is not
    the blocked portal/browser visual command.

## Stage Test Layers

| Layer | Stage A | Stage B |
|---|---|---|
| Static/schema | Curriculum/templates/refs/prerequisites/ADRs/patterns/views | Rerun against final content |
| Render/semantic | Expansion determinism/text/overlap/protected hashes | Published asset-to-render identity |
| Contract | Exact #8 validators/registries/evidence binding | Exact #8 completion and exact #10 renderer consumer |
| Integration | None claimed | Content discovery/render + lab lifecycle through released seams |
| Failure/recovery | Negative fixtures; no runtime reset claim | Controlled failure, hint, reset, process/retry/tamper/unavailable cases |
| Accessibility | Exact Vietnamese-first/numbering/fit/font/contrast/geometry/text-parity machine checks plus bounded independent static review | Released renderer keyboard/static/no-JS/status/evidence behavior |
| Security | Content/render/secret/path/cloud-action scans | Browser/BFF/evidence/workspace negatives from exact releases |
| UAT | Content-owner review only; not completion evidence | Foundation, junior, mid challenge path and human readability review |

## Evidence Contract

Stage A retained evidence root is fixed by the amendment:

```text
.claude/evidence/issue-11-stage-a/<run-id>/
```

The released `.gitignore` already ignores `/.claude/`; no ignore-file change is allowed. An
auditor-approved external mode-0700 app-state root may substitute with the same symbolic root ID.
Nonignored `.artifacts/**` is forbidden. The run-owned layout uses private modes, closed
`index.json` + `index.sha256`, and `fitness-result-v1` command envelopes. The evidence bundle must
prove these logical records:

| Record | Required content |
|---|---|
| Authority | Stage, exact input, branch/worktree, local/tracking/live equality, dependency release SHAs/hashes, lease |
| RED | Plan input, seven-path scaffold commit, direct-child five-path tests commit, RED tree, exact four `I11-EP-*` reach/preconditions, valid-control results, mutation IDs, absent exact-code assertions, first semantic commit |
| Commands | Exact command line, owner, tool/lock versions, start/end/status plus elapsed/RSS/process/output/file/PGID/TERM/KILL/wait measurements |
| Contracts | Every consumed #8/#10/view schema/registry/renderer/fixture path, version, SHA-256 |
| Renders | Source/projection/tool/SVG/text hashes, deterministic pair, exact visual metrics/inspection, protected-six result |
| Traceability | Requirement/module/template-instance/view/dynamic relation/deployment topology/bridge/ADR/pattern/test/evidence reciprocal coverage |
| Runtime Stage B | Controlled failure, hints used, reset commit, verifier assertions, evidence/completion authority |
| Security | Negative results, secret/private-path scan, redaction class, residual risks |
| Cleanup/rollback | Owned bytes removed/restored, ignored/private evidence preserved, zero-byte nonignored porcelain, ignored-inclusive ownership delta, protected/unrelated pre/post hashes |
| Provenance | `inputGitSha`, `testedTreeSha`, optional later attestation commit, external merge/approval identity |
| Index | Closed ordered inventory of every payload/owner locator, media type, size and SHA-256; detached index hash; reject missing, duplicate, orphaned, stale, traversal, extra, or unindexed bytes without recursive self-hash |

## Exact Process and Resource Verification

- `run-focused-tests` owns one PGID and one 120000 ms deadline.
- `verify-expansions` owns one 180000 ms deadline spanning both sequential locked installs, both
  renders, and all validation; per-child timeouts cannot substitute.
- Every external command starts a new session/process group; only one is active; maximum 16 live
  group processes; aggregate RSS <=1610612736 bytes.
- Combined output <=1048576 bytes; failure excerpt <=16384 bytes plus full hash; staging <=4096
  files; each tool root <=1 GiB; both roots plus staging <=2.5 GiB; per-command evidence <=4 MiB.
- On timeout/breach/abort: TERM owned PGID, wait 5000 ms, KILL survivors, wait/reap leader, prove
  zero descendants. Missing/ambiguous PGID is fail and never authorizes a signal.
- Evidence records elapsed ms, sampling count, peak aggregate RSS, maximum process count, output
  bytes/hash, file count/bytes, PGID and TERM/KILL/wait outcome. Tests force every breach class.

The existing I5-06 `fitness-result-v1` command envelope and released Issue #8 learning evidence
are separate authorities. Stage A emits only the former. Released `fitness-result-v2` declares
`emissionFallback: null`; it and progress/completion/learner-evidence schemas are read-only
negative boundaries, never fallbacks.

Allowed result states are inherited from the accepted master contract: `pass`, `fail`,
`blocked-tbc`, `not-run-optional`. A required missing tool, contract, renderer, or check is `fail`.
Stage A’s unavailable `architecture-lab-e2e` is not a Stage A pass and cannot appear in the Stage A
command allow-list.

## Evidence Hashing and Provenance

- SHA-256 for all file bytes; released #8 canonicalization for structured payloads.
- Evidence references exact command output hashes rather than embedding unbounded/raw logs.
- Tracked evidence never claims its own containing commit. Distinguish input, tested tree,
  attestation commit, and external merge/approval.
- Never overwrite a previous run. Failure and rollback evidence remain immutable.
- No secrets, private paths, raw environment, cloud IDs, full plans/state, or user/private data.

## Cleanup and Rollback Verification

1. Capture exact pre-stage tracked, nonignored-untracked, ignored-inclusive, device/inode, byte and
   protected manifests.
2. Allocate only the exact ignored app-owned or approved external Issue #11 root with mode-0700
   owner marker; retained files are mode 0600 and contain no absolute/private locator.
3. On success/failure, stop only recorded Issue #11 process groups and validate no descendants.
4. Delete only verified temporary workspace/render staging bytes; retain ignored/external
   evidence under the closed index.
5. Roll back the exact 50 new Issue #11 tracked candidates as one coherent set. Remove only the
   separate extension manifests/assets while proving protected rows/outputs never changed.
6. Rerun protected hashes/blob IDs, contract/renderer dependency hashes, staged allow-list and S3
   scan. Require exit 0 **and zero stdout bytes** from
   `git status --porcelain=v1 --untracked-files=all`; then parse NUL-terminated
   `git status --porcelain=v1 --ignored --untracked-files=all -z` and classify every ignored entry
   as pre-existing unchanged or exact retained-owned evidence.
7. Any ambiguity, foreign byte, missing evidence, or protected drift fails rollback and blocks
   merge. No broad `make clean`, recursive workspace delete, reset/rebase/rewrite, worktree
   removal, or merge other than the pre-cook exact integration reconciliation.

## Human Exact-Head Pre-Merge Gate

For each future staged release:

- independent implementation review at exact tested head;
- repository-authorized human approval naming exact 40-hex head and stage;
- all required results passing at that head after fresh dependency/lease check;
- local HEAD = tracking = fresh-live; clean worktree; exact staged diff;
- no synthetic approval from issue labels, automation, score, or this plan.

## Unresolved Questions

None for Stage A. Portal renderer integration tests wait for an exact Issue #10 release and remain
Stage B blockers.
