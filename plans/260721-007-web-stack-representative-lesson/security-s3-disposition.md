# Security S3 Disposition

## Disposition

`security:S3` is applicable. Issue #7 does not implement a privileged runner, but it creates
browser bundles, compiles trusted content, consumes a future tracked data fixture, installs three
dependency trees, records browser/process evidence, and defines a future BFF-compatible seam.
These are real code/content/supply-chain/evidence boundaries. A textual “not applicable” would be
invalid.

Issue #7 authority remains deliberately weaker than I5-04/I5-05:

- no subprocess, Docker socket, host mount, repository/data mutation, private runner route, cloud
  SDK/endpoint, credential, cookie/session, CSRF token, CORS exception, or completion service;
- only safe synthetic preview and later sanitized read-only issue #6 fixture consumption;
- future BFF protections are compatibility requirements, not implementation permission.

## Data and Asset Classification

| Asset | Classification | Allowed in browser/tracked evidence | Prohibited |
|---|---|---|---|
| Synthetic preview fixture | Public synthetic | Yes, with permanent unscored/non-completing label | Secret/PII/host path/real-score claim |
| Issue #6 promotion fixture | Public sanitized real evidence after merge | Only declared projection/fields with digest and schema | Raw source data, ignored fixture, unreviewed field |
| Project MDX/content | Trusted project source, executable at build | Compiled output/source under review | Remote, learner/fixture-authored, runtime evaluation |
| Browser bundles/assets | Public | Content-addressed output after bundle scan | Credential/private URL/env/source-map leak |
| Raw run evidence | Internal review artifact until sanitized | Hash-indexed canonical artifact root | Tokens, cookies, headers, env dumps, absolute paths, PII |
| Retained scorecard/evidence | Public sanitized | Relative locators, hashes, measurements, screenshots/traces after review | Secret-shaped canary, personal path, unsafe HTML/source |

## Threat Actors and Trust Boundaries

- A hostile local web page probes loopback origins, predictable ports, wildcard CORS/Host logic,
  browser storage, and source maps.
- A malicious or malformed fixture injects HTML/JSX/script/URL/oversized/secret-shaped data.
- A compromised/transitive npm package executes lifecycle code or alters build/test evidence.
- A learner tampers with URL/storage/DOM/clock/attempt IDs to forge verification/completion.
- A contributor accidentally publishes paths, headers, cookies, environment, copied content, or
  contaminated/mixed-fixture evidence.
- Time pressure weakens CSP, lock review, manual accessibility, must-pass, or provenance.

## Risk and Control Matrix

| Boundary/risk | Preventive control | Negative test/evidence | Failure/rollback | Residual risk |
|---|---|---|---|---|
| Browser credential/private endpoint | Client logical type has no credential/runner URL; empty privilege inventory; no public secret env | `WEB-API-001`; bundle/source/storage/network scan; secret canaries | Remove route/env/type; regenerate bundle; eliminate candidate | Public bundle metadata still reveals framework/version; accepted and recorded |
| Cross-origin/rebinding assumption | Preview exposes no mutation/runner; bind loopback; no wildcard CORS; exact static/read-only routes | Cross-origin/Host-shaped requests; route inventory; CSP/network trace | Remove permissive route/config; keep static preview | Future portal remains responsible for real auth/Origin controls |
| Runtime/untrusted MDX or HTML | Only project-owned build-time MDX; fixture values escaped/schema-validated; no raw HTML/eval/remote import | JSX/script/closing-tag/URL/frontmatter/oversize fixtures; DOM/network/build scan | Remove unsafe renderer/content; regenerate/eliminate | Trusted maintainer source can execute at build; protected by review/locks |
| Public env/source map leakage | Exact env allow-list is empty for secrets/private URLs; inspect built source maps and strings | `VITE_*`, `NEXT_PUBLIC_*`, source-map/absolute-path/secret scans | Purge/regenerate; rotate any real exposed secret; eliminate if cap | Heuristic scans can miss novel secret shapes; manual review remains |
| CSP weakening | Candidate documents exact CSP; no wildcard, remote script, `unsafe-eval`, or script `data:`; render-mode impact recorded | Header/meta/browser violation checks and asset/network inventory | Restore strict CSP or eliminate; mode drift invalidates evidence | Next/static constraints may force no-winner rather than a downgrade |
| Browser state forgery | State bound to fixture/mode/test digest; browser never authors verifier/evidence/completion; preview has no completed | URL/storage/DOM/time/tab/digest tamper E2E | Clear scoped state; restart; remove client-authoritative field | Local same-user can edit preview files; no security/completion claim is made |
| Dependency lifecycle/provenance | Independent exact locks; inspect lifecycle scripts; clean install; advisory/provenance/license record; no silent auto-fix | Lock/manifest mismatch, unexpected install script, advisory/license/provenance evidence | Remove dependency/version or eliminate; regenerate all evidence after lock change | Registry/provenance availability can block; cap/no-winner is accepted |
| Evidence privacy/integrity | Schema allow-list, relative locators, sanitized commands/environment, immutable hashes, redaction review | Absolute path/header/cookie/token/PII/unsafe-field canaries; artifact hash verification | Quarantine raw artifact; regenerate sanitized evidence; remove score | Unkeyed local SHA proves consistency/corruption only, not authorship |
| False fixture/score authority | Permanent preview label; Barrier B merge/digests; score schema rejects synthetic/mixed/killed | `WEB-PREVIEW-001`, barrier and scoring negative tests | Remove scores/winner/ADR decision; retain labelled preview | Human may misread screenshots out of context; visible watermark/metadata retained |
| False cross-grain claim | Four-card schema and forbidden relationship/copy rules | Four WEB grain/trust IDs, DOM/schema/visual/reviewer evidence | Delete composite and every dependent score/claim | Coincidental labels/counts remain cognitively tempting; copy states limitation |
| Non-copy/legal integrity | Project-owned expression; source/license/principle inventory; manual source/visual review | `WEB-NONCOPY-001`, attestation, asset/license inventory | Remove derivative work and rebuild | Similar broad interaction principles may remain; reviewer documents rationale |

## Supply-Chain Procedure

The common Gate 0/Gate A harness is dependency-free: it has no package manifest, lockfile,
installation, lifecycle script, or browser dependency. Its supply-chain gate proves those items
are absent and uses only the already-frozen host Node/Python/Make tools. For each independent
candidate, only after a later readiness audit authorizes candidate work:

1. Validate exact manifest/lock agreement and lock hash.
2. Inspect lock metadata and declared lifecycle scripts before approved script execution.
3. Use clean `npm ci`; retain exact registry/package/provenance/advisory/license evidence.
4. Do not use `npm audit fix`, broad upgrades, or dependency substitution as an unreviewed gate
   workaround. Any lock change invalidates build/browser/measurement evidence.
5. Reject missing required metadata/tool as `fail`; an external registry outage may pause the
   timer only with evidence.
6. Scan installed/build output and source maps for canaries/private endpoints/absolute paths.

The procedure evaluates risk; it does not promise all advisories have a patch. An unacceptably
exploitable dependency eliminates the candidate inside the same cap.

## Evidence Security

Canonical evidence uses `fitness-result-v1` and an allow-listed schema. Record OS/tool versions,
not full environment dumps. Store only safe command arguments and relative paths. Browser traces
must be reviewed for URLs, headers, cookies, storage, source, and local paths before entering
`spikes/web/evidence/retained/**` or tracked scorecards.

The SHA-256/artifact index is corruption and consistency evidence inside a local single-actor
threat model. It does not prove non-repudiation. A tracked scorecard records `testedTreeSha`; the
containing attestation commit is external and cannot self-reference recursively.

## Future BFF Compatibility Without Privilege

The common `LabClient` stops at a same-origin, OpenAPI-compatible interface. It contains no
transport credential, direct runner locator, raw shell/SQL, or browser authority. Candidate tests
must not contradict the later contract:

- exact loopback Host and Origin allow-lists;
- no wildcard CORS;
- high-entropy launch secret exchanged server-side for HttpOnly/SameSite session;
- CSRF protection for every mutation;
- DNS-rebinding/cross-origin negative tests;
- preferably a private Unix-domain-socket runner boundary;
- typed idempotent operations and server-authoritative verification/completion.

Issue #7 does not implement a session, CSRF, Host/Origin auth, Unix socket, runner, or mutation.
Adding a toy privileged path to score a candidate is a must-pass failure.

## S3 Acceptance

- All relevant negative tests and evidence rows above are present for the preview and every scored
  candidate.
- Browser route/bundle/storage/network inventory is empty of privilege and secrets.
- Content is trusted/build-time only; fixture hostility tests pass.
- Locks/lifecycle/provenance/advisory/license/CSP dispositions are complete.
- Evidence is sanitized/hash-indexed and the local threat-model claim is honest.
- Future BFF seam is compatible without implementing or weakening privilege controls.
- Changed-path/protected-hash/credential/non-copy checks pass.

Any failure blocks preview publication when exploitable and always blocks scoring/ADR/portal
handoff. Rollback returns to the static neutral preview, removes unsafe candidate execution and
numeric decision fields, retains evidence, and changes no shared/protected file.
