# Threat Model and Security

## S3 Disposition

I5-05 crosses an S3 boundary because an untrusted browser can request actions that eventually
reach a privileged local runner and evidence/progress authority. The portal must keep the browser
outside the runner trust boundary and prove negative cases before enabling Stage B. “Localhost”
alone is not authentication.

## Assets and Adversaries

Protected assets:

- repository base and Issue #6 contracts/fixtures;
- runner launch credential, private transport, registry, workspace journal, and process boundary;
- portal session/CSRF state and completion database;
- evidence bytes, index, canonical digest, retention metadata, and prior evidence;
- local home/cloud credentials, environment, private paths, process output, and network;
- dependency/package lock and exact released contract identities.

In-scope adversaries/failures:

- malicious same-browser/cross-origin page, DNS rebinding, forged Host/Origin/CSRF request;
- learner-controlled lesson field, error text, evidence metadata, artifact, ID, or URL;
- local process probing loopback ports;
- replay/double-click/reload/back/forward, stale state, operation race, crash/ENOSPC;
- dependency/contract drift, malicious package, credential/private-path leakage;
- accidental cleanup/rollback across worktree or evidence boundaries.

Out of scope but stated residual risk: the owner of the same local OS account can replace portal,
runner, database, verifier, and evidence and recompute an unkeyed digest. Hosted multi-user
identity and external signing remain I5-14; I5-05 makes no non-repudiation claim.

## Trust Boundaries

| Boundary | Allowed | Denied |
|---|---|---|
| Browser → portal documents | loopback GET, safe static content | private locators/credentials |
| Browser → BFF | exact same-origin #8 operations and typed bodies | wildcard CORS, generic proxy, arbitrary path/URL/SQL/command |
| BFF → runner | exact #9 client/transport/registry, server-held runner credential | browser-provided runner URL/token/argv/path/env |
| Portal → completion store | exact #8 transitions/transaction | client-authored completion or reflection-derived completion |
| Runner/evidence → BFF | verified bounded schemas/handles | raw HTML, special files, path traversal, unbounded output |
| Cleanup → runtime | marker-verified I5-05 namespace | evidence, repository, home, other worktrees/processes |

## STRIDE and Negative Test Matrix

| ID | Threat | Control | Required negative |
|---|---|---|---|
| PTP-S3-01 | Spoof portal/runner session | launch-scoped high entropy; portal and runner credentials distinct; HttpOnly SameSite session | absent/expired/replayed/wrong launch session denied |
| PTP-S3-02 | DNS rebinding/Host spoof | bind loopback; exact runtime Host allow-list; no hostname suffix matching | foreign Host, rebinding host, public interface denied |
| PTP-S3-03 | CSRF/cross-origin mutation | exact Origin, `Sec-Fetch-Site`, server-bound CSRF header, no wildcard CORS | missing/foreign/null Origin, missing/wrong CSRF denied |
| PTP-S3-04 | Browser-direct runner | runner address/credential server-only; private transport; CSP `connect-src 'self'` | browser request/credential disclosure tests fail closed |
| PTP-S3-05 | Command/path/SQL injection | exact released operation and registry enums; closed schemas | shell metacharacter, extra field, path, URL, SQL, unknown command denied |
| PTP-S3-06 | XSS in content/error/evidence | released validation, React text escaping, no raw HTML, strict CSP | script/event/URL/HTML payload rendered inert |
| PTP-S3-07 | Artifact traversal/type confusion | opaque ID, #9 verified immutable handle, regular-file/media/size/digest allow-list | `..`, symlink/special file, wrong media/size/digest denied |
| PTP-S3-08 | Completion tampering | fresh runner result + evidence + #8 transaction, no browser storage authority | forged URL/storage/result/evidence/reflection cannot complete |
| PTP-S3-09 | Replay/race | idempotency/correlation, one in-flight mutation, runner journal/reconciliation | duplicate/reset-vs-verify/crash retry returns one outcome |
| PTP-S3-10 | Sensitive output | bounded structured errors/log redaction; no raw env/path/credential | canary/private path/output flood never reaches UI/evidence |
| PTP-S3-11 | Dependency drift/supply chain | exact #7 lock, `npm ci`, integrity lock, audit and package scripts review | lock/package mismatch or High/Critical audit fails |
| PTP-S3-12 | Cleanup overreach | namespace marker, PID start identity/process group, evidence retention | stale/reused PID, foreign process/path, symlinked root denied |
| PTP-S3-13 | Contract downgrade | exact #8/#9 release SHA/version/digest; closed registry | unknown/rollback/draft version denied |
| PTP-S3-14 | Optional/cloud credential use | sanitized environment; no cloud SDK/endpoint/action; scan evidence | AWS/model credential canary absent from child/UI/log |

## HTTP Security Contract

The BFF binds a runtime-selected loopback port and prints one canonical URL. It accepts only exact
`Host` values for the chosen `127.0.0.1`/`::1` endpoint and exact same-origin requests. No
`0.0.0.0` bind, wildcard/reflective CORS, stable secret in URL, or trust of `X-Forwarded-*`.

Mutating operations require:

- valid launch-scoped portal session cookie with `HttpOnly; SameSite=Strict; Path=/`;
- server-issued CSRF token bound to that session and supplied in the released header;
- exact `Origin` and `Sec-Fetch-Site: same-origin`;
- released content type, bounded body, closed schema, correlation and idempotency fields;
- no cross-origin redirects.

Local plain HTTP cannot honestly provide a `Secure` cookie. The portal documents this localhost
limitation, never uses a `__Host-` prefix falsely, and keeps the runner credential out of the
browser. Hosted TLS/cookie semantics are out of scope.

Baseline production/static response policy:

```text
Content-Security-Policy:
  default-src 'self';
  script-src 'self';
  style-src 'self';
  img-src 'self' data:;
  connect-src 'self';
  object-src 'none';
  base-uri 'none';
  frame-ancestors 'none';
  form-action 'self';
  manifest-src 'self';
  worker-src 'none'
Referrer-Policy: no-referrer
X-Content-Type-Options: nosniff
Cross-Origin-Opener-Policy: same-origin
Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
Cache-Control: no-store
```

Do not add `unsafe-inline`/`unsafe-eval` to make Vite output work. Development-only Vite behavior
does not define release CSP; the built portal and tests use the strict policy. Static page styles
are external same-origin assets or nonce-free compiled CSS.

## XSS and Rendering Rules

- Validate released content before rendering and map it into a closed safe view model.
- React interpolates text; `dangerouslySetInnerHTML`, raw MDX/HTML execution, runtime eval,
  untrusted URL schemes, and artifact inline preview are forbidden.
- Links allow only declared same-origin paths or server-approved external `https` targets with
  visible host, `rel="noopener noreferrer"`, and no completion effect.
- Problem details map stable released codes to local components. Do not render server stack/log
  fragments or unknown fields.
- Static fallback uses escaped deterministic templates and the same validated model.
- Evidence artifacts download as attachments; the portal never sniffs or executes their content.

## Storage and Evidence Security

- Portal SQLite is mode-restricted and located in an I5-05 namespaced runtime root.
- Use one transaction for evidence-index/completion commit exactly as #8 specifies.
- Validate schema/registry/canonicalization, artifact hash graph, tested tree, dependency SHAs,
  fixture/contract/verifier hashes, redaction and retention before completion.
- Preserve prior evidence across reset, crash, retry, learn-down, failed migration, and rollback.
- Evidence locators are evidence-root relative, normalized, no `..`, symlink, absolute/private
  component, device/special file, or credential-bearing URL.
- Evidence writes/downloads are bounded and fail on size/digest/media mismatch.
- A local SHA-256 is called corruption detection only.

## Environment and Credential Boundary

Portal/BFF needs no AWS, Terraform, model, OpenMetadata, Rill, Airflow, MinIO, Lakekeeper, Docker,
or cloud credential. It passes only the minimum released configuration to the runner client and
never forwards ambient environment. Tests inject canaries for common cloud/model token names and
private paths and require zero propagation to browser, logs, child process, SQLite, or evidence.

No endpoint or command may call AWS/cloud/Terraform, install packages at runtime, fetch external
content, or invoke optional heavy profiles. Dependency installation is a separate locked
developer step; the real journey runs network-disabled after install if the released runner
contract supports that test.

## S3 Scans and Gates

Future Stage A/B gates include:

- exact changed-path allow-list and protected-path hashes;
- `npm ci` against the exact committed app lock and production build;
- `npm audit --audit-level=high` with zero High/Critical findings;
- dependency lifecycle-script/license/source review required by the #7 handoff;
- high-confidence AWS/key/token/private-key/credential and absolute-private-path scan;
- bundled source-map/runtime config scan for runner URL/credential/private path;
- Host/Origin/CSRF/CORS/CSP/XSS/storage/attachment negative tests;
- runner conformance/security/race tests from the exact #9 handoff in Stage B;
- final `git diff --check` and untracked/staged evidence exclusion.

Ordinary prose words such as “token” or “credential” are not themselves findings. Scans report
high-confidence assignments/signatures/canary values and inspect matches before blocking.

## Retention, Cleanup, and Rollback

- Evidence root: `.artifacts/evidence/local-journey/{run-id}/` using
  `fitness-result-v1` until an exact compatible #8 successor is released and pinned.
- Retain tests-before failure evidence, dependency manifests, journey result, browser trace,
  screenshots, axe output, download digest, cleanup/rollback result, redaction class, and human
  UAT/approval records through review/release policy.
- `learn-down` stops only the recorded I5-05 process group after PID/start-identity verification,
  revokes launch/CSRF/runner client secrets, requests runner-owned workspace cleanup through the
  exact API, and proves no owned process remains.
- It never deletes committed evidence, the completion DB under active retention, Issue #6 fixture,
  repository files, other worktrees, optional-profile volumes, or unrelated user state.
- Rollback disables Stage B first and serves Stage A static fallback. A full I5-05 code rollback
  removes only `apps/learning-portal/**` and `mk/issue-5/i5-05.mk` at an exact reviewed Git
  rollback point; retained evidence remains.

## Residual Production UAT

One named human at the exact reviewed head performs a bounded keyboard/visual review and, when
available, a representative screen-reader check before production release. This is residual UAT,
not a broad OS/browser matrix, not automated native OS control, and not proof of full WCAG or
screen-reader conformance. A missing/failing required human exact-head pre-merge approval blocks
merge.
