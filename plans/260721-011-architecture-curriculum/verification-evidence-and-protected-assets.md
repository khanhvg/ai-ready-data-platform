# Verification, Evidence, and Protected Assets

## Verification Boundary

This planner runs plan/static/link/dependency/protected-hash checks only. It does not run the
future curriculum, architecture renderer, lab, portal, native GUI, manual browser matrix, cloud,
or Terraform gates.

Future practical acceptance, after exact stage authority, remains:

```bash
make curriculum-check architecture-check architecture-render architecture-lab-e2e traceability-check
```

No target is currently authorized for Issue #11 implementation. Existing Issue #6
`architecture-check` and `architecture-render` are read-only public contracts; a later amendment
must prove how they cover expansion without redefining or modifying their owner code.

## Planner-Only Check Set

| Check | Expected result |
|---|---|
| Branch/input/fresh remote | Required branch; clean input `24be3b34c6b0fcdbd07c5800dcab349054e34713` before plan writes |
| Live Issue #11 | OPEN; exact body; `triaged` before output transition; risk high/TDD/S3/architecture/curriculum |
| Dependencies | #8 not released; #10 not passing/merged; both implementation authorities empty |
| `ck plan status` | Seven pending phases, valid frontmatter/dependency DAG |
| Markdown structure | One H1 per file; required sections; no empty placeholders |
| Local links/anchors | All repo-relative plan links and anchors resolve |
| Authority scan | `implementationFileAllowList: []`, `implementationCommandAllowList: []`; no future SHA/route/renderer/schema path |
| Protected assets | Exact Issue #6 SHA-256 and Git blob identities unchanged |
| Staged scope | Only `plans/260721-011-architecture-curriculum/**` |
| Formatting | `git diff --cached --check` passes |
| S3 scan | No secret/private-key/private-path/credential-bearing URL/runtime artifact |

## Protected Issue #6 Source Closure

Baseline at planner input `24be3b34c6b0fcdbd07c5800dcab349054e34713`:

| Path | SHA-256 |
|---|---|
| `architecture/likec4/specification.c4` | `96eeff0c7df9c04c0b3ca0e66aa0e53a05ba61bb3a3c95ec447f58a276643a32` |
| `architecture/likec4/model/people-and-systems.c4` | `aaaca720b921db63526449147aa9c3ec67b7eb8dd70a301fd9f855e41e096d32` |
| `architecture/likec4/model/learning-platform.c4` | `33a224d2c6ae9e6e294b170741bb4184b6f6df2ef17956164354f1ed6abac9e3` |
| `architecture/likec4/model/data-platform.c4` | `cba2985a8d60646a5e2a801eb9d08595d1081487efd6aa576c909fdd5249650d` |
| `architecture/likec4/model/local-deployment.c4` | `58e6fbc72e3ea41b826057a60f096f50a42b75550f1d35e0378edee59f0006ad` |
| `architecture/likec4/view-manifest.yaml` | `1659c51389718f2799581550ab17fd31c4dd30639723d5b443ac088944178169` |

All source-closure bytes remain read-only. An additions-only lease may add exact new sources/rows
only after authority; it may not normalize or reserialize the protected files.

## Protected Six Views and Renders

| View | Source SHA-256 | SVG SHA-256 | Text SHA-256 |
|---|---|---|---|
| `C4-L0` | `7fbe895e119e0f93ebfd68b671f051a29556936158bf9d4517ed316a1c5d8240` | `2d41f7e064c832a6b09a3715dfd4a0c8f9a3fe4c4789cac5ac8f3fd746e4b965` | `e76a7da77a76fb0db70ba52d611c0c29343e5da2b6be2ed2a4231b8c4136fc2a` |
| `C4-L1` | `8c843198efcccb5fe91788b9715c495d42a28454b2083e678ceeb5f00d9bb30d` | `59075f6e6a4041953137fe988c9e309090228742cc3beb5d114ed4b4f113f33d` | `6720223e2c09f2f346ad7fde6e600c72f75685332851caa495bda61ce4046d65` |
| `C4-L2-LOCAL` | `a763d2820af704bc3986ab986df49d32f3acf76f29deb8022041857478578b5c` | `cdda1e25b0f735d5c0d54d88f18fa7ee51f39d24b8acdeaa97f5df0271232736` | `03cbe8c843b52c20a4c4602dcd9dd7b1b54b4a3030ef07d1284ee24ba6b10b7c` |
| `C4-L3-RUNNER` | `d7fa6a0869343b2db2e61543d2cdc4f00547ccd41e3a4073da6df3f9dbb82bb2` | `65125df61b15955ab7ac1bae7ba9eb8d0679670cbac4afb586713f07b7691bfc` | `4406e3dfcb88d9b37e59843cf7e06fd8564845e11f7fb2c515a59136c9ac110a` |
| `DEP-LOCAL` | `65b1490fbacb24b0809a524ae0ca22d9aa8db51ea155a36cd756759ccb9f4b83` | `ece5a0bba7230cef7f69a9da8535fee2a06523bba0883d30b507684b8c028a0b` | `7d0b2395ccfa329c2d4ff2349c328384117fc2878ccfadec7460795ebbcbb3d0` |
| `DYN-JOURNEY` | `3681b76fcb2cee1a8b40f437b9015288cd1ce15c72c0250e98165716ea7104af` | `4c64440ff0040df7d75f148931b6758b4790fbab55e53af62ff735f08d3b3598` | `f55c05126387b5eb8a3ce20a9dd45bb0cd5fb33c9fc20aae75eff4a83db36a0b` |

`architecture/rendered/render-manifest.json` SHA-256:
`7934c00f9f7bd772f0f2eec4730332b6b6a8b5907f2d7547673fbef9718a04e6`.

The later lease must also preserve the six manifest rows’ ordered ID/key/type/audience/concern/
scope semantics and the original six Git blob IDs. A whole-file manifest/render-manifest change
is allowed only if the lease explicitly owns additions and a semantic projection proves each
protected row/result unchanged.

## Deterministic Static and Semantic Render Tests

After an exact expansion seam exists, tests must cover:

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
9. **No broad visual matrix:** deterministic source/text/semantic assertions are required; fixed
   human readability review is a later release gate, not native GUI automation.

## Future Test Layers

| Layer | Stage A | Stage B |
|---|---|---|
| Static/schema | Curriculum/templates/refs/prerequisites/ADRs/patterns/views | Rerun against final content |
| Render/semantic | Expansion determinism/text/overlap/protected hashes | Published asset-to-render identity |
| Contract | Exact #8 validators/registries/evidence binding | Exact #8 completion and exact #10 renderer consumer |
| Integration | None claimed | Content discovery/render + lab lifecycle through released seams |
| Failure/recovery | Negative fixtures; no runtime reset claim | Controlled failure, hint, reset, process/retry/tamper/unavailable cases |
| Accessibility | Vietnamese/static semantic structure and text alternatives | Released renderer keyboard/static/no-JS/status/evidence behavior |
| Security | Content/render/secret/path/cloud-action scans | Browser/BFF/evidence/workspace negatives from exact releases |
| UAT | Content-owner review only; not completion evidence | Foundation, junior, mid challenge path and human readability review |

## Evidence Contract

Evidence root is fixed by Issue #11:

```text
.artifacts/evidence/architecture-curriculum/<run-id>/
```

The exact file layout is not invented here; it must come from the released Issue #8 binding in a
later amendment. The evidence bundle must nevertheless prove these logical records:

| Record | Required content |
|---|---|
| Authority | Stage, exact input, branch/worktree, local/tracking/live equality, dependency release SHAs/hashes, lease |
| RED | Failing fixture/assertion IDs and failure reasons before implementation |
| Commands | Exact command line, owner, tool/lock versions, start/end/status/resource/output bounds |
| Contracts | Every consumed #8/#10/view schema/registry/renderer/fixture path, version, SHA-256 |
| Renders | Source/projection/tool/SVG/text hashes, deterministic pair result, protected-six result |
| Traceability | Requirement/module/view/ADR/pattern/test/evidence reciprocal coverage |
| Runtime Stage B | Controlled failure, hints used, reset commit, verifier assertions, evidence/completion authority |
| Security | Negative results, secret/private-path scan, redaction class, residual risks |
| Cleanup/rollback | Owned bytes removed/restored, evidence preserved, protected/unrelated pre/post hashes |
| Provenance | `inputGitSha`, `testedTreeSha`, optional later attestation commit, external merge/approval identity |
| Index | Closed ordered inventory of every required result/artifact locator, media type, size and SHA-256; reject missing, duplicate, orphaned, stale, or unindexed bytes |

The current Issue #6 `fitness-result-v1` command envelope and the future Issue #8 learning/
evidence schema are separate authorities. The amendment must record the exact released #8 path,
version and SHA-256 plus an owner-authorized compatibility mapping to the Issue #11 command-result
requirement. The current repository copy and the proposed unreleased Issue #8 version are not
fallbacks.

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

1. Capture exact pre-stage tracked/ignored/protected manifests.
2. Allocate only an amendment-authorized Issue #11 mutable root with owner marker.
3. On success/failure, stop only recorded Issue #11 process groups and validate no descendants.
4. Delete only verified temporary workspace/render staging bytes; retain committed evidence.
5. Roll back new Issue #11 tracked candidates as one coherent set. For a shared additions-only
   manifest, restore the prior exact file while proving protected rows/outputs never changed.
6. Rerun protected hashes/blob IDs, contract/renderer dependency hashes, staged allow-list, S3
   scan, and clean-status check.
7. Any ambiguity, foreign byte, missing evidence, or protected drift fails rollback and blocks
   merge. No broad `make clean`, recursive workspace delete, reset/rebase, or worktree removal.

## Human Exact-Head Pre-Merge Gate

For each future staged release:

- independent implementation review at exact tested head;
- repository-authorized human approval naming exact 40-hex head and stage;
- all required results passing at that head after fresh dependency/lease check;
- local HEAD = tracking = fresh-live; clean worktree; exact staged diff;
- no synthetic approval from issue labels, automation, score, or this plan.

## Unresolved Questions

None. Exact evidence filenames/fields and renderer integration tests wait for released contracts.
