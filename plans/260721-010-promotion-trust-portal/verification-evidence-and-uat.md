# Verification, Evidence, and UAT

## Scaffold-First TDD Rule

V3 uses the exact chronology in the
[recovery amendment](./stage-a-release-amendment.md#scaffold-first-commit-chronology): 22 callable
semantics-free scaffold paths, then all eight test paths, then contemporaneous RED, then semantic
commits. No product path exists before the scaffold commit. No test exists in that commit. No
semantic byte exists before the tests-only commit and its closed RED generation.

The scaffold must let real adapter, provider, catalog, router, static/React render, built server,
lifecycle, evidence writer, Make delegates, and real Chromium reach a bounded neutral document.
It contains no target lesson/routes/outcome, fixture ID, expected-value branch, forced error,
default catalog/step table, mock, skip, or final semantic copy. RED is valid only when a complete
assertion reaches that scaffold and reports one of the named absent-semantics classifications.

Every RED record binds the actual base, derived plan-only input, scaffold commit/tree, tests
commit/tree, 85-input aggregate, lock/tools, command argv/exit/duration, raw log SHA-256, sanitized
log SHA-256, expected invariant, and observed absent semantic. A later detached reproduction or
summary is diagnostic only and cannot replace contemporaneous RED.

## Complete Tests-Only Portfolio

Commit 2 creates all eight final test paths and changes no scaffold byte. Valid controls and
mutations are exact:

| Family | Valid control | One-change mutations and required oracle |
|---|---|---|
| Release/contract | Exact 85 released inputs at `5644f01…` | commit/tree/blob/byte/hash/path/version/family/field/operation/lock/freeze drift must fail before admission |
| Registry/generic seam | Exact released descriptor registry plus binding | branded in-memory `test-only-structure` exercises pure functions; production rejects it; duplicate/unhashed/draft/unknown descriptors fail |
| Content/grain | Released lesson/manifest/binding and 89 sanitized rows | fifth/missing/reordered grain, key/alias drift, causal wording, outcome drift, raw field, fresh-evidence claim fail |
| Router/render | Registry-derived current routes | malformed/overlong/ambiguous/traversal path, duplicate route, order mutation, escaping payload, static/React fact drift fail |
| Build/server | Closed valid regular-file build inventory and loopback GET/HEAD | extra/unlisted file, content change, media/size mismatch, executable, symlink/hardlink/FIFO/socket/device, Host/method/body/chunked/length/decoding mutation fail |
| Lifecycle | One test-owned scaffold child and authentic private control record | tampered endpoint/nonce/capability, owner/mode/type/link/containment drift, stale record, benign foreign-process sentinel fail without any PID signal |
| Blocked result | Released `fitness-result-v2` schema and exact Stage B invocation | missing/extra field, `unavailable` status, wrong code/exit/stream, empty bindings/artifacts, bad argv/payload hash, any runner action fail |
| Evidence | One fresh private pending generation with valid payloads | missing/extra/duplicate entry, stale log, hash/count/size/aggregate/privacy/type/link/source/tree/tool drift, recursive hash, interrupted publish, second/missing trace fail |
| Browser/a11y | Real Chrome channel, current released registry, two fixed viewports | missing Vietnamese semantics, focus/order/live region, overflow, reduced motion, axe, no-JS, request/storage/console/CSP invariant fail |
| S3 | PTP-S3-01..14 valid absence/control cases | one exact canary per row must fail closed; no row passes by skip or predicate copy |

Mutations use in-memory clones or private `mkdtemp` roots created from the valid control. They are
never tracked, shipped, selected by environment, admitted by production, or used as a fallback.
The exact released invalid binding fixtures remain read-only controls and must produce their
released eight codes through the real public validator and portal adapter.

## RED Families and Commands

The normative family/classification matrix is in the
[amendment](./stage-a-release-amendment.md#exact-red-families-classifications-and-commands). The
tests-only head runs every command in the 18-command allowlist. Acquisition and released
validators may be successful setup controls. Every behavior-bearing unit/build/public/Chromium
path must fail at a named absent semantic after reaching the scaffold. The RED recorder rejects:

- import/tool/path-not-found failures;
- unconditional throw, `assert false`, deliberate non-zero, expected echo, or hard-coded answer;
- mock/skip/xfail/todo/only/focus or predicate-only reimplementation of production admission;
- snapshots copied from released truth without traversing the real path;
- ignored/untracked/other-worktree/absolute-path fixture fallback;
- logs generated after the matching semantic commit.

`make learn`, status, and down traverse real scaffold lifecycle state. The scaffold child
self-expires safely; public commands report semantic readiness absent and produce current logs.
The two Stage B commands are non-zero both before and after implementation, but RED remains until
their stderr objects validate as exact blocked `fitness-result-v2` with zero runner action.

## Exact Stage A Command Contract

No additional command shape is authorized:

```bash
node apps/learning-portal/scripts/verify-stage-a-release.mjs
make learning-contracts-check
make lesson-check LESSON=promotion-trust
make api-contracts-check
npm --prefix apps/learning-portal ci --ignore-scripts --no-audit --no-fund
npm --prefix apps/learning-portal run test:unit
npm --prefix apps/learning-portal run build
npm --prefix apps/learning-portal run test:stage-a -- --workers=1 --retries=0
npm --prefix apps/learning-portal run test:visual -- --workers=1 --retries=0
npm --prefix apps/learning-portal audit --audit-level=high --json
make portal-test portal-a11y
make portal-e2e
make portal-visual-review
make learn LESSON=promotion-trust
make learn-status
make learn-down
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
```

The root Makefile remains byte-identical and supplies only the sorted fragment include seam.
`mk/issue-5/i5-05.mk` owns the nine reserved commands and delegates fixed argv to portal scripts.
Direct fragment execution, arbitrary variables/argv, generic host commands, and root edits fail.

## Command Acceptance

| Command group | Final required result |
|---|---|
| Release verifier and three released checks | Exact runtime/lock/environment admitted; 85 inputs, public binding, lesson/lab/manifest/registry, and 16 OpenAPI operations verify |
| Frozen install/unit/build/audit | Exact graph; unchanged complete tests; two byte-identical builds; closed inventory; zero High/Critical |
| Public test/a11y/e2e | Real delegates pass current descriptor, desktop/narrow, keyboard/focus/overflow, axe, no-JS, request/storage/network/console/CSP gates |
| Public visual review | One fresh atomic generation with hash-valid artifacts and exactly one sources-excluded Chromium trace; checklist unapproved |
| Learn/status/down | Static portal only; authenticated child status/self-shutdown; down twice safe; evidence retained |
| Two Stage B negatives | stderr one-line schema-valid blocked `fitness-result-v2`; exit 2; stdout empty; no runner/container/network action |

## Production Registry and Metamorphic Proof

Production constructs one `ReleasedPortalDescriptorRegistry` from the exact released contract-set
root and shared binding after released validation. Catalog, app, router, static-route generation,
static rendering, and React rendering consume only that object. Tests prove:

1. the current released descriptor derives exactly `/`, `/module`, one released lesson route, and
   its ten ordered released step routes;
2. route count equals two presentation roots plus each admitted lesson and its steps; order and
   uniqueness are deterministic;
3. a branded test-only structural descriptor can be renamed, reordered, added, or removed in pure
   functions with local predictable effects;
4. production admission rejects that brand with `PORTAL_DESCRIPTOR_AUTHORITY_FORBIDDEN`;
5. build/runtime inventories and string scans contain no test-only tokens;
6. unknown, duplicate, unhashed, wrong-family/version/path/field, draft, or future descriptors fail
   before catalog creation;
7. no `defaultCatalog`, `STEP_IDS`, promotion switch, copied route list, or duplicated alias map
   exists.

This proves generic structure without pretending a future release exists. #11/#12 later enter
only through a reviewed integration release that adds hash-bound recognized-family entries and a
later exact-SHA amendment; the production code gains no content-ID switch.

## Released Product Truth

The real final Chromium/no-JS journey derives and visits the current 13 documents:

```text
/
/module
/lesson/promotion-trust
/lesson/promotion-trust/step/frame
/lesson/promotion-trust/step/inspect
/lesson/promotion-trust/step/run
/lesson/promotion-trust/step/fail
/lesson/promotion-trust/step/trace
/lesson/promotion-trust/step/decide
/lesson/promotion-trust/step/reset
/lesson/promotion-trust/step/configure
/lesson/promotion-trust/step/verify
/lesson/promotion-trust/step/reflect
```

The route list above is acceptance truth derived from the released lesson, never a production
table. `/module` is presentation-only. Every route is Vietnamese-first, visibly identifies Stage
A as a static slice rather than the full product, presents four independent grains without causal
join, and shows only `insufficient-evidence/no-common-grain`. Run/reset/verify are explanation
only. Runner, execution, reset, fresh evidence, progress, and completion remain unavailable,
disabled, not-run, false, disabled, and disabled respectively.

## Chromium Journey and Trace

One Playwright test, one Chrome channel, one worker, and zero retries perform the entire journey.
Locale is `vi-VN`; timezone is `Asia/Ho_Chi_Minh`; color scheme and reduced motion are fixed. The
same test uses `1280x800`, then `360x800`, and creates a JavaScript-disabled context for static
parity.

The test covers catalog → module → lesson → every released step, direct links, reload,
back/forward, unknown routes, keyboard order, visible focus, live status, reduced motion, no
horizontal overflow, axe zero Critical/Serious, no-JS parity, exact non-claim attributes, zero
unexpected request/storage/cookie/cache/service-worker state, and zero console/page/CSP error.
It distinguishes the released controlled-failure explanation from environmental runner
unavailability.

Playwright trace configuration is an object with mode `on`, screenshots/snapshots enabled,
attachments enabled, and sources disabled for the single journey project. The visual project
omits trace recording. The completed journey must retain exactly one trace archive. The official
Playwright Test API documents the object mode and `sources` control:
https://playwright.dev/docs/api/class-testoptions#test-options-trace.

Trace admission verifies regular single-link type, exact owner/private mode, SHA-256, compressed
and uncompressed bounds, archive count, safe relative entries, no source-resource entries, and
privacy canaries. A missing, second, oversized, source-bearing, stale-head, or unindexed trace is
failure.

## Authenticated Lifecycle Verification

The public process record is not kill authority. Tests start a benign foreign sentinel and then
mutate PID/start fields, endpoint, nonce, capability, owner, mode, type, link count, and path.
`learn-status`/down must not call `kill` or signal any recorded PID. They authenticate over the
private loopback control listener; only the child can close its listeners and exit. Tampering
fails closed while the sentinel remains alive. Valid down proves authenticated response, listener
closure, child exit, no owned descendant, retained evidence, and safe second down.

## Blocked `fitness-result-v2` Verification

For each Stage B command, parse stderr as one JSON object, validate it with the exact released
schema, independently recompute RFC 8785 payload SHA-256, verify all named hashes/artifacts and
actual argv, require `status: fail` plus `STAGE_B_DEPENDENCY_UNAVAILABLE`, require exit 2 and empty
stdout, and inspect process/network/import records for no runner, container, Docker, cloud, or
optional-profile action. Mutation tests cover every required field and conditional.

## One Current Evidence Generation

The exact publication protocol is normative in
[Current-Generation Evidence Publication](./stage-a-release-amendment.md#current-generation-evidence-publication).
The current generation must contain:

- raw and sanitized RED logs from the tests-only head and raw/sanitized GREEN logs from the final
  tested head for all 18 command rows;
- actual commit/tree roles for base, derived plan-only input, scaffold, tests/RED, first semantic,
  later semantics, and final head;
- 85-input/protected/runtime/lock/tool/command/build inventories;
- current resource, all-14-S3, lifecycle, blocked-result, cleanup, interruption, and rollback
  records;
- exact browser/axe/no-JS/console/CSP/request/storage records, at most eight fixed screenshots,
  and exactly one compliant Chromium trace;
- `inventory.json`, `generation-index.json`, and an atomically published regular
  `current-generation.json` selector with non-self hash closure.

Every retained current manifest entry must verify. Negative history has a separate outer manifest
whose entries also all verify; an old invalid manifest is inert payload with its failure recorded,
never nested authority. A stale prior generation is not a current fallback. An interrupted pending
directory is never selectable. Raw logs may remain local-private but must reject secret/credential
canaries; sanitized logs also remove private paths and unstable ports. File count, aggregate bytes,
every individual size/hash/type/mode/owner/link, privacy class, and source/tree/input/dependency/
tool binding are exact, not summaries.

## Cleanup, Rollback, and Ignored Classification

Cleanup closes handles, uses authenticated child self-shutdown, removes only owner-validated
runtime/dependency/build/test scratch, and preserves current evidence plus classified negative
history. It runs twice. Recovery after injected interruption proves the selector still names the
previous verified generation or no generation, never a partial publication.

An ignored-inclusive walk and Git classification account for every node: tracked product,
expected ignored dependency cache, build/test scratch to remove, runtime to remove, selected
current evidence, or negative history. Unknown untracked/ignored content, tracked generated
output, special files, aliases, private paths, or unclassified bytes fail.

Rollback removes only the exact 33 create-only tracked paths and owned scratch while retaining
evidence. It never modifies released inputs, failed PR #29, another worktree, home, containers,
cloud, AWS, or Terraform.

## Exact-Head Gate

Before any Stage A merge:

- final diff is exact 33 creates; commands are 18/18; released inputs are 85/85;
- tests-only blobs remain bound; all GREEN and current evidence match the final head/tree;
- one trace, all current manifest entries, resource/S3/cleanup/rollback, build inventory, blocked
  results, secret/private-path and ignored-inclusive scans pass;
- two fresh independent final-head implementation reviews have zero unresolved Critical/High;
- one named human completes bounded keyboard/visual UAT and exact-head approval;
- local, upstream, and fresh PR head match.

This corrected plan satisfies none of those implementation gates. Fresh independent plan
validation and fresh readiness audit must occur before v3 cook. Stage B remains blocked on Issue
#9 and Issue #10 stays open.
