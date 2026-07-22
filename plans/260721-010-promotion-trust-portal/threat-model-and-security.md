# Threat Model and Security

## S3 Disposition

Stage A crosses an S3 boundary because released content and local browser requests reach a
loopback process that reads built files. It deliberately removes the higher-risk browser → BFF →
runner boundary: no runner, API, mutation, completion authority, secret, or canonical user state
exists. All 14 S3 rows are exercised now; Stage B-only attacks pass through proven absence, not a
skip. Stage B must be re-threat-modelled after an exact Issue #9 release.

## Assets and Adversaries

Protected assets:

- repository, released #7/#8 bytes, Issue #6 fixtures/contracts, and protected manifest;
- exact package lock, closed build inventory, released descriptor registry/binding, and safe view model;
- loopback process ownership, child-held control capability/instance nonce, runtime marker, and
  evidence/review artifacts;
- local environment, home/cloud credentials, private paths/locators, PII, raw fixture records,
  process output, remote imports, and network;
- lesson truth: four independent grains, canonical decision, and non-completion claim.

In-scope adversaries/failures include DNS rebinding/foreign Host, traversal/ambiguous decoding,
malicious released-field mutations, XSS/URL payloads, dependency drift, output floods/special
files, browser storage or network leakage, stale/tampered lifecycle state, symlink/hardlink aliasing, cleanup
overreach, and false execution/evidence/completion claims.

The owner of the same local OS account can replace application/evidence bytes and recompute an
unkeyed digest. Stage A makes no publisher-authentication, non-repudiation, hosted, multi-user, or
full WCAG claim.

## Trust Boundaries

| Boundary | Allowed | Denied |
|---|---|---|
| Released tree → build | exact hash-bound #7 packages and validated #8 descriptor registry/shared binding | feature worktree, ignored copy, test-only descriptor, portal-local map/schema, unknown field/version/path/hash |
| Released content → view model | closed escaped safe fields | raw HTML/MDX, script, event, executable URL, raw fixture rows |
| Browser → static server | exact loopback Host, GET/HEAD, admitted route/file | body, mutation, API, proxy, upload, traversal, ambiguous route |
| Browser state | current read-only route/view | cookie, session, local/session storage, IndexedDB, cache, service worker |
| Portal → host/network | owned built files and process metadata | runner, command, SQL, path/URL fetch, Docker, cloud, credentials |
| Lifecycle control → child | owner-private control record plus child-held capability/nonce; child self-shutdown | PID signal, foreign endpoint/process, mutable PID authority |
| Cleanup → runtime root | nonce/marker/capability-contained owned state | repository, home, selected evidence, other worktrees/processes, aliases |

## STRIDE and Negative Test Matrix

| ID | Threat | Stage A control | Required negative |
|---|---|---|---|
| PTP-S3-01 | Spoofed session/authority | no session/cookie/credential or authenticated state exists | cookie/session/token cannot appear or grant capability |
| PTP-S3-02 | DNS rebinding/Host spoof | bind `127.0.0.1`; exact runtime Host allowlist | foreign/rebinding Host or public interface denied |
| PTP-S3-03 | CSRF/cross-origin mutation | no mutation route; GET/HEAD only; `form-action 'none'`; no CORS | POST/PUT/PATCH/DELETE/OPTIONS and cross-origin forms fail |
| PTP-S3-04 | Browser-direct runner | no runner module/address/token; `connect-src 'none'` | bundle/DOM/network contains no #9 capability or request |
| PTP-S3-05 | Command/path/URL/SQL injection | no input surface; closed route and file maps | metacharacter/path/URL/SQL/extra-field inputs never reach host action |
| PTP-S3-06 | XSS in content/error | released validation, text escaping, no raw HTML, strict CSP | script/event/URL/HTML payload inert or rejected in both renderers |
| PTP-S3-07 | File traversal/type confusion | closed regular-file build inventory; containment, media, size, alias checks | `..`, ambiguous decode, unlisted/change-after-inventory, symlink/hardlink/FIFO/device/socket denied |
| PTP-S3-08 | Completion/evidence tampering | no completion/progress/evidence authority or browser store | URL/DOM/storage/reflection cannot produce run/evidence/completion claim |
| PTP-S3-09 | Replay/race | navigation is read-only; lifecycle serialized and identity-bound | reload/double-click/back/forward causes no mutation; repeated stop is safe |
| PTP-S3-10 | Sensitive/unbounded/stale output | closed errors, raw/private and sanitized classes, exact closure/ceilings | canary/private path/flood/stale-head/hash/count/aggregate drift fails publication |
| PTP-S3-11 | Dependency drift/supply chain | exact #7 graph/integrity; frozen no-script install; audit | lock/package/integrity drift or High/Critical finding fails |
| PTP-S3-12 | Lifecycle/cleanup overreach | child-authenticated self-shutdown; namespace marker/nonce/containment | tampered PID/endpoint/capability, foreign sentinel/path, alias root rejected without signal |
| PTP-S3-13 | Contract downgrade | exact #8 release/hash/version/closed registry | unknown, rollback, draft, wrong hash/path/field fails before render |
| PTP-S3-14 | Cloud/optional credential use | sanitized inputs; no cloud SDK/endpoint/action/runner | AWS/model canary or optional/cloud call absent from child/UI/log/bundle |

## Static HTTP Security Contract

The built server binds only `127.0.0.1` on a runtime-selected port and prints one canonical URL.
It accepts exact Host values for that selected endpoint, GET and HEAD only, no body or transfer
encoding, request target at most 2048 bytes, and only the closed post-build path/media/size/hash
inventory. Non-zero/ambiguous length, chunking, body bytes, unlisted or changed content, and
decoding ambiguity fail before a file is opened. It does not trust
`X-Forwarded-*`, enable CORS, redirect across origins, perform content negotiation from user
input, list directories, or serve source maps.

Every successful production response has equivalent strict headers; the CSP is exactly:

```text
default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:;
connect-src 'none'; object-src 'none'; base-uri 'none'; frame-ancestors 'none';
form-action 'none'; worker-src 'none'
```

Also require `Referrer-Policy: no-referrer`, `X-Content-Type-Options: nosniff`,
`Cross-Origin-Opener-Policy: same-origin`, a restrictive `Permissions-Policy`, and
`Cache-Control: no-store`. No `unsafe-inline`, `unsafe-eval`, nonce exception, external origin,
manifest, websocket, or development-server relaxation is admitted. HTML bootstraps external
same-origin compiled assets only.

The separate random loopback lifecycle control listener is not a product API and is unreachable
without the child-held 256-bit capability and instance nonce. It accepts only bounded status and
shutdown messages. The child validates them in constant time and exits itself. Caller commands
never signal a PID from the mutable control record.

## XSS and Rendering Rules

- Run exact released validators before mapping a closed safe view model.
- Iterate the released shared binding directly; forbid portal-local alias/mapping tables, copied
  binding schemas, generated binding types, or fallback identifier rules.
- React interpolation and static templates escape every field consistently.
- Forbid `dangerouslySetInnerHTML`, raw HTML/MDX, runtime eval/code generation, inline handlers,
  executable/untrusted URLs, artifact previews, and unknown released fields.
- Links are closed same-origin navigation routes. Canonical external GitHub evidence links belong
  to planning/audit documents, not the Stage A product.
- Errors expose stable local codes and remediation only, never stacks, environment, absolute
  paths, raw validation bodies, or unknown fields.

## Browser, Environment, and Credential Boundary

Stage A uses no cookie, session, CSRF token, runner token/URL, browser storage, service worker,
cache, database, canonical progress, evidence bytes, raw logs, private locator, or ambient
environment field. Static navigation remains useful when offline after page load.

Browser admission is exact: Playwright `1.61.1`, `browserName: chromium`, `channel: chrome`, one
worker, zero retries, and one measured Chrome product/version/executable SHA-256 shared by RED and
GREEN. Bundled-browser fallback, alternate browser/channel, browser download, or identity drift
fails; absolute executable paths remain local-private.

No command or endpoint may invoke Issue #9, Docker, Rill, Airflow, Iceberg, OpenMetadata, MinIO,
Lakekeeper, AWS, Terraform, cloud/model services, package installation at runtime, arbitrary host
commands, or external content fetches. Dependency acquisition is the one locked developer step;
tests/build/runtime use no undeclared online fallback.

## Resource and Artifact Security

The exact amendment ceilings are mandatory:

- one portal Node process, one Playwright worker, loopback only;
- 300-second install, 180-second build, 120-second unit/Node, 15-second readiness,
  300-second Playwright, and 180-second audit ceilings;
- production: at most 128 regular files, 1 MiB each, 16 MiB aggregate, no source maps or special
  files/aliases;
- review: two viewports, at most eight named screenshots, one trace, one axe JSON, one no-JS
  inventory, one console/CSP/request/storage record, raw/sanitized RED/GREEN logs, and non-self
  inventory/index/selector closure;
- text logs at most 2 MiB, binary artifacts at most 16 MiB, Chromium trace at most 16 MiB
  compressed/64 MiB uncompressed/512 entries with sources excluded, current generation at most
  128 files and 64 MiB aggregate.

Every current payload has exact owner/mode/type/link/media/privacy/size/hash and source/tree/input/
dependency/tool binding. Missing enforcement, a failed manifest entry, recursive/self hash, stale
head, or unclassified ignored node is failure. Logs/artifacts never become learner execution or
completion evidence.

## S3 Scans and Gates

Stage A must pass:

- exact changed-path allowlist, released per-file identities, protected hashes, and root Make
  command ownership;
- frozen install, exact transitive lock comparison, production build, and `npm audit` with zero
  High/Critical;
- high-confidence secret/key/private-locator/PII/raw-record and cloud/runner/remote-import/
  source-map/bundle scans;
- Host/method/path/CSP/XSS/storage/network/output/special-file/alias negative tests;
- all PTP-S3-01..14 assertions, including Stage B-capability absence;
- exact process, time, file, byte, log, browser-artifact, current-generation hash/privacy/count/
  aggregate, lifecycle, interruption, and cleanup bounds;
- `git diff --check`, staged/untracked scope inspection, and generated-output exclusion.

Ordinary prose such as “token” is not a secret finding. Scanner results must identify an actual
assignment/signature/canary or be manually dispositioned.

## Retention, Cleanup, and Rollback

- Runtime root: `.artifacts/runtime/i5-05-stage-a/`; review root:
  `.artifacts/evidence/local-journey/`. Both are marker/nonce/containment bound and untracked;
  directories are owner-only and retained files are owner-only regular single-link nodes.
- Retain the one selected current generation containing source/tree-bound raw/sanitized RED/GREEN,
  dependency/build/unit/contract/S3/a11y/resource records, two-viewport screenshots, exactly one
  sources-excluded Chromium trace, axe/no-JS/console/CSP/request/storage reports, non-self closure,
  cleanup/rollback/interruption results, an author/cook-produced role record with independent and
  human approval false, and the unapproved checklist.
- Prior/stale/failed generations are explicitly negative history and cannot satisfy current
  evidence. Pending interrupted generations are never selected.
- `learn-down` authenticates to the child, asks it to self-shutdown, is safe twice, preserves
  selected/negative-history evidence, and proves no owned process remains; it never signals a PID.
- It never deletes repository content, the Issue #6 fixture, dependency bytes, other worktrees,
  home/private paths, other processes, optional-profile volumes, or review evidence.
- Rollback is an exact reviewed Git revert/removal of only the 33 Stage A additions. No release
  byte, contract, root file, fixture, or retained review artifact is mutated by cleanup.

## Residual Human Gate

One named human reviews keyboard flow, information hierarchy, focus visibility, error/status
copy, Vietnamese-first readability, narrow layout, no-JS equivalence, grain honesty, and absence
of false course/run/completion claims at the exact reviewed head. This is bounded residual UAT,
not native OS automation or full screen-reader/WCAG conformance. Human exact-head pre-merge
approval remains mandatory.
