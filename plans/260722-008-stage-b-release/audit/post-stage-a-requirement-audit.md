---
title: "Issue #8 post-Stage-A Stage B requirement and readiness audit"
status: completed
issue: 8
auditDate: "2026-07-22"
inputSha: "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
verdict: "STAGE_B_READY"
stageARelease: "pass"
sharedContractLease: "active"
planValidation: "pass"
s3: "pass"
cloudAction: "none"
plannerRoute: "Herdr"
plannerModel: "gpt-5.6-sol"
reasoningEffort: "xhigh"
---

# Issue #8 Post-Stage-A Stage B Requirement and Readiness Audit

## Verdict

`STAGE_B_READY`. Stage A remains a passing immutable release, but it is not by itself an exact
consumer handoff. One bounded Issue #8-owned Stage B binding is required before the shared-contract
lease can be released and Issue #10 can consume the promotion-trust grain identifiers without
inventing shared semantics.

The cook scope is exactly the three-phase plan in this package: one closed schema, one hash-bound
binding document, one pure reader, two existing validator/check integrations, one tests-first
module, and eight input-only invalid fixtures. It includes no Stage A rewrite, registry/set/
manifest/OpenAPI/Make change, generated TypeScript, portal, runner, data pipeline, package/lock,
cloud, AWS, or Terraform action.

## Fresh Authority Check

- Branch/input were exact and clean before plan edits:
  `plan/issue-8-stage-b-amendment` at
  `fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`.
- Fresh live `origin/integration/issue-5-local-learning` equaled the input.
- PR #22 is merged at `1806b6d515f2f7a2ace2be7077af84a745ff221f`; Issue #7 is
  CLOSED/shipped.
- PR #23 is merged at `5c2244c2c860234d0df49cf0a42ad950c6495717`; PR #25 is merged at
  the input. Both release merges are ancestors of the input.
- All 23 Issue #8 comments current at audit time were read. Stage A release evidence is
  [5043195549](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043195549);
  the concrete mismatch report is
  [5043335319](https://github.com/khanhvg/ai-ready-data-platform/issues/8#issuecomment-5043335319).
- Issue #8 remains OPEN and owns the serialized shared first-manifest/contract seam. Issue #9 owns
  runner behavior; Issue #10 owns portal/browser behavior but consumes shared contracts read-only.
- Herdr process provenance showed Codex `gpt-5.6-sol` with
  `model_reasoning_effort=xhigh`. CK ran in auto/hard plan mode; no `plan-to-cook` surface was
  exposed, so the equivalent strict plan/readiness workflow was used.

GitHub exposed no configured required-check list for PRs #22/#23/#25; this is recorded as absence,
not a passing CI assertion. Release evidence and remote merge identities are the applicable facts.

## Stage A Release Result

Stage A remains **pass**:

- public release: 56/56;
- invalid fixture corpus: 65/65;
- operation matrix: 16;
- final I5-03 checks: 4/4;
- inherited Issue #6: data 19/19, migration 1/1, evidence 13/13;
- published S3/resource/offline/cleanup/rollback: pass;
- contract set: 21/21 current content hashes pass; set byte SHA-256
  `92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638`.

No Stage A byte is invalidated or edited by the Stage B plan. The gap is at the cross-release
consumer seam that Stage A tests did not compare.

## Exact Incompatibility and Mapping Proof

| Grain | Stage A manifest | Issue #6 evidence / Issue #7 Vite | Required alias |
|---|---|---|---|
| promotion | `promotion`: `promo_name,channel` | `promotion`: `promo_name,channel` | none |
| fulfillment | `fulfillment`: `carrier,region` | `fulfillment`: `carrier,region_name` | `region → region_name` |
| returns | `returns`: `reason,category,region` | `returns`: `reason,category_name,region_name` | `category → category_name`; `region → region_name` |
| data quality | `dq`: `scenario` | Vite `data-quality`; evidence `scenario` | grain ID `dq → data-quality` |

Verified immutable identities:

- Stage A manifest SHA-256
  `553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac`;
- Issue #6 evidence SHA-256
  `2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5`;
- Issue #7 lesson contract SHA-256
  `32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9`;
- Issue #7 package/lock SHA-256
  `c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871` /
  `96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c`.

The released Issue #7 focused Node suite ran read-only and passed 5/5, confirming its Vite labels
and Issue #6 fixture keys at the pinned bytes. The mapping is mechanically bounded: match the
stable grain, retain equal identifiers, and alias the sole unmatched identifiers at the same
ordered positions. It changes no value, calculation, order, join, conclusion, or completion rule.

## Why This Is Issue #8 Stage B

- The master graph and Issue #8 body assign I5-03 the shared lesson/lab and first-manifest seam.
- Issue #10 may write only portal-owned paths and consumes released lesson contracts read-only. A
  portal-local `region → region_name` mapping would create unreviewed duplicate contract truth.
- Issue #7 released the exact source labels but explicitly no Issue #8+ product behavior; its Vite
  bytes are protected inputs, not a place to repair the shared seam.
- The previous BLOCKED comment correctly refused to invent files/tools inside the stale Phase 6.
  This fresh user-authorized planning task requires a new bounded plan when a real Stage B need is
  found and supplies its exact plan directory. The new plan is that required authority step; it
  does not claim implementation or a future release SHA.

## Minimum-Scope Readiness Result

The selected approach is ready because every material choice is fixed by released authority:

- exact input/dependency SHAs and source hashes exist;
- the alias set—two unique field rules applied in three row positions plus one grain-ID rule—is
  closed and empirically reproducible;
- exact create/modify/protected paths are named;
- stable real-path RED IDs and failure codes precede behavior;
- existing Python/Node/Make commands cover the seam with no new dependency or public command;
- Stage A/OpenAPI/registry/manifest/Make/downstream bytes are protected;
- browser/server/completion authority is explicit;
- additive v1/backward-reader, evidence, S3, resources, cleanup, rollback, independent review, and
  human exact-head merge gates are complete.

No unresolved product choice, placeholder, guessed path, package, command, mapping, or future SHA
remains in the cook scope.

## Validation and Hygiene

- strict `ck plan validate`: pass, three phases, zero errors/warnings;
- `ck plan status`: pending 0/3, correct for a cook-ready unimplemented plan;
- local Markdown links/anchors: pass;
- placeholders and unverified 40-hex identities: pass;
- exact plan-path and future implementation-path allow-lists: pass;
- protected Stage A/Issue #6/Issue #7 hashes and 21-entry contract-set closure: pass;
- S3 secret/private-path/cloud/destructive-command scan: pass;
- diff whitespace/staged-scope hygiene: pass;
- whole-plan requirements/phases/commands/hashes/ownership/trust/rollback/human-gate consistency:
  pass.

The audit validates planning readiness only. It performs no implementation test for nonexistent
Stage B bytes, creates no product/config/data output, and grants no PR merge or human approval.

## Lease and Next Gate

Shared-contract lease: **active**, exclusive to the bounded I5-03 Stage B cook. Use only
`plans/260722-008-stage-b-release/plan.md`. After implementation, fresh independent exact-head
review, repository checks, separate human approval, observed remote release SHA, and external
two-component handoff are mandatory before the lease is released.
