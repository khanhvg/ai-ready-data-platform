# Verification, Evidence, and UAT

## TDD Rule

Every behavior begins with a retained RED at pristine integration
`5644f01b4c0443a81f3af0bcce80f44c847cd986` or a tests-only descendant. RED must traverse the
real portal adapter, model, static/React render, router, server, or lifecycle path and fail because
the behavior is absent. Missing imports/tools, unconditional failure, snapshots of copied truth,
or reconstructed evidence are invalid.

Each RED record binds ID, exact pre-behavior source/tree, dependency identities, tests-only diff,
command/exit code, expected and actual failure, raw-log digest, and later GREEN at the reviewed
head without weakening the assertion.

RED starts in the fresh v2 worktree after the ordered plan-only cherry-picks. A detached clean
checkout at the same tree must also pass release verification, static generation, production
build, and public-route tests without branch-name or upstream assumptions. Every dependency and
fixture is resolved from a tracked cook-tree path whose Git blob/bytes/SHA-256 match the 85-path
catalogue. An ignored, untracked, generated, retained-worktree, environment-selected, or absolute
private-path artifact is never authority; substituting any such candidate is a named RED failure.

## Tests-Before Matrix

| ID | First real failing assertion | Stage |
|---|---|---|
| PTP-RED-A-001 | Wrong integration/#7/#8/tree/blob/byte/hash/version/operation/lock is admitted | A |
| PTP-RED-A-002 | Any protected Issue #6/release identity drifts without failure | A |
| PTP-RED-A-010 | Real server/static render lacks catalog/module/lesson/step shell or required facts | A |
| PTP-RED-A-011 | Cross-grain attribution or non-canonical decision renders | A |
| PTP-RED-A-012 | Stage A exposes run/reset/verify/progress/evidence/completion or runner request | A |
| PTP-RED-A-013 | Router back/forward/reload changes more than validated view state | A |
| PTP-RED-A-014 | Built no-JS route lacks facts, navigation, unavailable, or non-completion state | A |
| PTP-RED-A-015 | Runner unavailable is confused with controlled lesson failure | A |
| PTP-RED-A-016 | Vietnamese semantics, focus, 360px reflow, reduced motion, or live status fails | A |
| PTP-RED-A-020 | Released binding/provider admits invalid authority/path/hash/grain/key/alias/type/version/field/state | A |
| PTP-RED-A-021 | Static and React renderers disagree on fact IDs or escaping | A |
| PTP-RED-A-022 | Bundle/build contains #9, API mutation, storage, secret, cloud, or source map | A |
| PTP-RED-A-023 | Process/request/output/artifact/alias/special-file ceilings are not enforced | A |
| PTP-RED-A-024 | Status/cleanup can target foreign PID/path or remove retained review evidence | A |
| PTP-RED-S3-001..014 | Corresponding S3 negative does not fail closed, including absence assertions | A |
| PTP-RED-B-001..016 | Runner/journey/evidence/completion requirements | B, catalogued but not runnable |

Tests load exact tracked released files. No copied, synthetic on-disk, ignored, generated, or
framework-specific promotion data fixture is allowed. The SA-R11 seam test uses only empty sets,
the exact current released descriptor, and duplicate rejection; it must not invent #11/#12
content or identifiers.

## Practical Stage A Portfolio

| Layer | Exact focus | Bound |
|---|---|---|
| Release/contract | shared binding, 85 per-file identities, #8 public validators, registry, two lesson-read operation identities | exact released bytes |
| Unit | provider/catalog/safe model/router/static render/security | focused Node tests; no snapshot wall |
| Build | exact frozen Vite graph and deterministic static routes | production build, no source maps |
| Security | PTP-S3-01..14, CSP/Host/path/XSS/storage/network/bundle/supply chain | closed negative matrix |
| Accessibility | semantics, keyboard, focus, live status, reduced motion, overflow, axe | zero Critical/Serious |
| Browser | one Chromium journey at 1280x800 then 360x800 | one worker, zero retry |
| Static/no-JS | built parser plus JavaScript-disabled Chromium | same stable facts/routes |
| Lifecycle | start/status/down twice, stale PID, foreign path/process, output bounds | one owned process |
| Visual/UAT | fixed Stage A screenshots/trace/manifest/checklist | no native OS automation or approval claim |

There is no Next.js/Astro comparison, Firefox/WebKit matrix, VoiceOver/System Settings/native
browser control, performance contest, score/timer, exhaustive device grid, or automated
conformance claim.

## Exact Stage A Command Contract

Run only the exact allowlist in the amendment. The implementation gate sequence is:

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
```

Then prove the Stage B commands fail without runner action:

```bash
make lesson-e2e LESSON=promotion-trust
make local-journey-e2e
```

Both required negatives return non-zero `STAGE_B_DEPENDENCY_UNAVAILABLE`. `mk/issue-5/i5-05.mk`
owns the nine reserved I5-05 public targets and delegates only to locked portal scripts. It does
not edit root Make, invoke Docker/optional profiles/cloud, or expose a generic host command.

## Command Acceptance

| Command | Required Stage A result |
|---|---|
| release verifier and #8 checks | one exact-lock CPython 3.12.3 runtime is marker-admitted/cleaned; shared binding focused 11/11 and invalid 8/8, exact lesson/lab/manifest/registry, and 16 OpenAPI operations pass |
| frozen install/build/unit | exact lock graph, real adapter/router/render/security tests, deterministic bounded production output |
| `make portal-test portal-a11y` | focused unit/contract/security/build plus axe zero Critical/Serious |
| `make portal-e2e` | desktop+narrow, history/reload, no-JS, unavailable/non-completion, zero unexpected network/storage |
| `make portal-visual-review` | bounded named Stage A artifacts and unapproved checklist |
| `make learn` | start static server only and print canonical URL, runner unavailable, completion disabled |
| `make learn-status` | report owned PID/start identity/static readiness and Stage B blocked |
| `make learn-down` | stop only owned portal; idempotent twice; retain review evidence |
| Stage B negatives | typed non-zero dependency unavailable; no runner import/start/call |

No Stage A command emits fresh learner-run, progress, completion, or verified evidence. Test and
review records are implementation-review artifacts, not Issue #8 completion evidence.

## Release and Fixture Identity Tests

Before content tests, recompute:

- the exact #7/#8 commit ancestry/tree relationships and 921-entry final released tree listing;
- every one of the 85 admitted released paths' blobs, byte lengths, and SHA-256 from the cook tree;
- exact package/lock graph and tool versions;
- all seven protected Issue #6/release identities;
- root Make include and the nine I5-05 `future-owner/not-runnable` registry rows;
- the app activation's base-registry/final-fragment hashes, nine exact command IDs,
  `implemented` recipe availability, and `fitness-result-v2` output binding;
- absence of the 33 Stage A create paths in the pristine integration.

Mutation tests change one identity, path, byte, hash, version, operation, unknown field, or lock
edge at a time and require a stable fail-closed result before render.

The released public binding adapter must additionally execute its exact invalid inventory:

| Released invalid fixture | Required code |
|---|---|
| `absolute-path.json` | `BINDING_REFERENCE_FORBIDDEN` |
| `completion-authority-override.json` | `BINDING_AUTHORITY_FORBIDDEN` |
| `contract-key-drift.json` | `BINDING_STAGE_A_KEY_MISMATCH` |
| `dependency-hash-drift.json` | `BINDING_DEPENDENCY_HASH_MISMATCH` |
| `duplicate-target-key.json` | `BINDING_ALIAS_NOT_BIJECTIVE` |
| `fixture-key-drift.json` | `BINDING_FIXTURE_KEY_MISMATCH` |
| `grain-id-drift.json` | `BINDING_GRAIN_MISMATCH` |
| `raw-record-leak.json` | `BINDING_DATA_PAYLOAD_FORBIDDEN` |

In-memory released-adapter cases also cover missing/extra grain, lossy/cyclic alias,
unsupported version, wrong type, unknown field, contract/fixture substitution, descriptor race,
hardlink/symlink/FIFO, and authority-state mutation. Portal tests then prove those failures stop
the real adapter/build/public-route path; they do not recreate the Python predicates in JavaScript.

## Chromium Journey

Use the frozen Playwright/Chrome channel, one worker, no retry, locale `vi-VN`, timezone
`Asia/Ho_Chi_Minh`, reduced motion, fixed color scheme, and animations suppressed only for
capture. Bind the journey to fixture `promotion-trust-small-42-v1`, profile `small`, seed `42`,
manifest SHA-256 `0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341`, evidence SHA-256
`2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5`, binding ID
`promotion-trust-vite-binding-v1`, and binding SHA-256
`03d2aa6bd9fa178e6075865364a8ae8b83ce548c42b450d1858b451b45d0d1d0`. Run the same route
sequence at 1280x800 and 360x800:

1. open `/` and confirm Vietnamese-first shell, one vertical-slice module/lesson, and visible
   not-full-product wording;
2. navigate `/module` → `/lesson/promotion-trust` → the `frame`, `inspect`, `run`, `fail`,
   `trace`, `decide`, `reset`, `configure`, `verify`, and `reflect` step documents;
3. verify four independent grains, limitations, controlled-failure explanation, and canonical
   decision without causal attribution;
4. reach run/reset/verify explanation and confirm runner unavailable/no actionable control;
5. use back, forward, and reload; confirm only view state changes and zero mutation/network replay;
6. verify keyboard order/focus/live status/reduced motion/no overflow and axe zero Critical/Serious;
7. verify every route's exact machine-readable non-claim attributes: runner unavailable,
   execution/progress/completion disabled, reset not-run, fresh evidence false, static slice;
8. inspect console, CSP, requests, cookies, all Web Storage/IndexedDB/Cache APIs, and bundle
   exposure for zero prohibited state/capability.

No console/page/unhandled/CSP error is allowed. Automated checks do not claim full WCAG or
screen-reader conformance.

## No-JavaScript and Static Equivalence

A JavaScript-disabled Chromium context follows all 13 canonical catalog/module/lesson/step links.
A separate parser reads every generated route. Both must expose the same stable released facts,
navigation, grain limitations, `PROMOTION_HEADLINE_INSUFFICIENT` explanation,
`insufficient-evidence / no-common-grain`, runner-unavailable state, and non-completion warning.

Static and React output share one safe model and escaping rules. No required fact/control may
exist only behind JavaScript, animation, hover, external network, or scroll position.

## Runner-Unavailable Boundary

Prove by import graph, built bundle/string scan, request observation, process inventory, DOM,
storage inventory, and command negatives that Stage A:

- does not import/start/probe/call Issue #9 or any runner-compatible placeholder;
- exposes no runner address/token, command/argv/path/URL/SQL, mutation method, API proxy, or
  browser secret;
- does not create progress, completion, workspace, run, reset, verifier, evidence, or download
  state;
- keeps the released controlled-failure explanation distinct from environmental unavailability.

## Deterministic Visual Review

`make portal-visual-review` captures only these Stage A states at both viewports, within the
eight-screenshot ceiling: catalog/vertical-slice context, four-grain lesson context, canonical
decision, and runner-unavailable/no-completion static fallback. It also emits one trace, axe JSON,
no-JS inventory, console/CSP record, SHA-256 manifest, and `uat-checklist.md` under the bounded
review root.

The checklist asks one human to review hierarchy, Vietnamese-first labels, focus, status/error
copy, grain honesty, 360px readability, static parity, reduced motion, and absence of false
course/run/completion claims. Reviewer identity, exact head, date, result, and residual notes are
recorded separately; artifact generation never fabricates approval.

## Evidence, Cleanup, and Rollback

Retain RED/GREEN records, release/protected identity manifests, unit/contract/S3/a11y results,
build/output inventory, audit result, Chromium trace/screenshots, axe/no-JS/console/CSP records,
artifact hashes, lifecycle/cleanup/rollback results, independent reviews, bounded UAT, and human
exact-head approval through release policy.

Runtime and review roots, file/byte bounds, PID/start identity, marker/nonce containment, special
file/alias denial, and idempotent cleanup are exact in the amendment. Cleanup preserves review
artifacts and never touches repository/dependency/fixture/home/other-worktree/foreign-process
state. Rollback removes only the exact 33 Stage A additions at a reviewed Git point.

## Exact-Head Release Gate

Before a Stage A human merge:

- every exact command and TDD/S3 check above passes at one clean head;
- changed paths equal the 33-path create allowlist; no modify/delete or generated tracked output;
- release/protected hashes and command ownership match;
- `npm audit` has zero High/Critical and axe has zero Critical/Serious;
- two fresh independent exact-head reviews have zero unresolved Critical/High findings;
- one named human completes bounded visual/keyboard UAT and exact-head approval;
- local, upstream, and fresh PR head are equal; no cloud/AWS/Terraform action occurred.

Stage A readiness planning satisfies none of those implementation/release gates. Stage B remains
blocked and cannot be skipped, passed, or claimed by Stage A results.
