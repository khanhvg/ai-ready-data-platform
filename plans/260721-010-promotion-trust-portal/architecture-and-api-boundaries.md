# Architecture and API Boundaries

## Decision

Use one host-local Vite + React application with an in-process Node BFF and one separately
released private runner process. This is a modular monolith at the portal boundary, not a
distributed framework. It introduces no broker, worker fleet, service mesh, service worker,
cloud service, container requirement, or second product database.

```text
Browser
  | same-origin documents + released Issue #8 browser API only
  v
Learning portal process
  |- Vite-built React client
  |- static/no-JavaScript lesson renderer
  |- same-origin BFF/security filter
  |- released contract bindings and completion repository
  '- server-only released Issue #9 runner adapter
        | private transport + server-held runner credential
        v
     Issue #9 runner
        |- command registry / workspace journal / verifier
        '- immutable evidence and existing local data-product entrypoints
```

The browser never receives runner transport location, runner launch credential, command argv,
filesystem locator, arbitrary query capability, or direct artifact path.

## Stage Separation

| Concern | Stage A | Stage B |
|---|---|---|
| Framework | Exact merged Issue #7 Vite/React handoff | Same exact accepted foundation |
| Content/contracts | Exact released Issue #8 Stage A | Same release or explicit compatible successor |
| Runner | No import/call; capability is unavailable | Exact released Issue #9 server-only client/API |
| Completion | Disabled; no row/event can be written | One Issue #8 authority and reconciliation protocol |
| Evidence | Labelled Issue #6 baseline reference only | Fresh runner evidence + integrity/download |
| Claim | Readable static lesson shell | Complete local journey |

## Ownership Ceiling and Deferred File Resolution

The issue-level ownership ceiling is `apps/learning-portal/**` (including portal tests),
`mk/issue-5/i5-05.mk`, and Issue #10 plan/evidence artifacts. The root Makefile already provides
the `mk/issue-5/*.mk` include seam and must not change. Shared contracts, dependency source,
fixtures, root configuration, CI, cloud, AWS, and Terraform remain read-only or denied.

Repository `README.md` and `docs/**` are also outside the I5-05 product-write ceiling. A later
implementation review records documentation/release impact, but any required change is a separate
owner-authorized serialized handoff rather than an expansion of this portal stage.

This validated plan does not select a product tree before the dependencies exist:

| Stage | Authorized create/modify/delete paths now | Authorized implementation commands now | Consumable dependency SHAs now |
|---|---|---|---|
| A | `[]` | `[]` | `[]` |
| B | `[]` | `[]` | `[]` |

After exact released handoffs exist, a later amendment must derive the smallest concrete file and
command allow-lists from the merged #7 promotion map and released #8/#9 consumption surfaces.
That amendment must pin real 40-hex identities, receive independent revalidation and
stage-specific readiness, and stay inside the ownership ceiling. A candidate path mentioned in
historical planning is not authority.

## Contract Binding Policy

An app-owned release-binding artifact may be authorized only by the later exact-SHA amendment. It
records exact released method/path/`operationId` values, schema/type imports, registry command
IDs, version strings, and source digests. It must be generated deterministically from the
released handoffs and compared in tests. It must not contain:

- a route or command copied from draft #8/#9 plans;
- an I5-05-owned replacement schema or state machine;
- permissive parsing or unknown-field stripping;
- a browser-visible runner transport or credential;
- a local fallback version when a released version is unavailable.

The accepted master plan names candidate operations, but Issue #8 owns the final browser-facing
OpenAPI and operation matrix and Issue #9 owns the final private API/registry. Because neither is
released at this planner input, this plan deliberately does not freeze literal API URLs. At Gate
A/B the generator binds their exact released method/path pairs. Absence or difference is a STOP,
not an invitation to invent an adapter contract.

## Release-Time Semantic Closure

The later amendment must bind behavior as well as names, without inventing field/status literals:

- **Version negotiation:** pin the exact #8/#9 supported and rejected version sets and their
  compatibility matrix; an absent, unknown, draft, stale, or downgrade version fails closed.
- **Single completion authority:** use only #8's released CAS/expected-revision rule and one
  atomic completion/evidence transaction; the browser, reflection, route, runner, and evidence
  index are never competing completion writers.
- **Idempotency and response loss:** pin the released request-key scope, retention, committed
  replay, in-flight duplicate, conflict, and expiry semantics. A retry with the same identity
  reconciles one result; it never starts a second mutation.
- **Crash/restart:** pin the exact committed/in-flight/orphan recovery rules for portal and runner
  crashes, including when quarantine is mandatory and when a safe retry is allowed.
- **Reset:** pin #9's exact reset operation and #8's corresponding CAS/progress transition; reset
  preserves prior immutable evidence, proves the released fresh-ready oracle, and never completes.
- **Errors and unavailable states:** pin released problem/status classes and remediation for
  absent, starting, not-ready, crashed, containment-unavailable, conflict, invalid evidence, and
  controlled lesson failure. Environmental states never advance progress.
- **Evidence:** pin verified-handle identity, bounded byte/size/media/digest checks, and #8's
  completion predicate. Metadata, bytes, or hash disagreement blocks download and completion.

If either release omits one of these semantics, the corresponding stage remains disabled and the
owner issue must supply it; I5-05 does not create a local compatibility contract.

## Runtime Loading Boundary

Stage A startup resolves only the exact merged #7 runtime and exact released #8 read-only
interfaces. It must not import, bundle, probe, or configure Issue #9 code. In Stage B, the private
runner client and optional-tool adapters remain server-only and are loaded after the exact released
capability/readiness gate; absence or incompatibility leaves the Stage A static route operational.
No eager optional import may break offline/static startup or leak runner transport into the browser
bundle.

## Logical Operation Boundary

Only these logical capabilities may cross the browser/BFF boundary, each using the exact Issue #8
released operation:

| Capability | Stage | Browser input | BFF responsibility | Authority |
|---|---|---|---|---|
| lesson read | A/B | fixed released lesson ID | load/validate safe projection | #8 lesson release |
| progress/completion read | A disabled/B enabled | current local actor/lesson | read canonical state | #8 completion protocol |
| runner/tool status | A unavailable/B live | none | reduce released status, no transport detail | #9 status |
| workspace start | B | released typed manifest inputs | validate, attach idempotency/correlation, call runner | #9 journal |
| operation submit/status | B | released action/argument IDs only | map exact allow-list; never argv/path/SQL | #9 registry |
| reset | B | workspace identity + idempotency | call exact reset; reconcile last committed state | #9 journal |
| verify | B | released run/workspace identity | request fresh verifier result | #9 verifier |
| evidence read/download | B | opaque evidence ID | verify authority/digest, stream bounded immutable handle | #8/#9 evidence |
| completion commit | B, server only | none directly | atomic canonical commit after all predicates pass | #8 authority |

Every request and response is validated at the BFF. Unknown fields, versions, actions, states,
identifiers, media types, or problem codes fail closed. The BFF does not expose generic proxy,
filesystem, URL fetch, raw SQL, shell, environment, path, upload, or arbitrary download
operations.

## State and Storage Authority

| State | Durable authority | Client representation | Crash/reload rule |
|---|---|---|---|
| Lesson/version | Exact Issue #8 release files | immutable view model | reload from BFF/static build |
| Read-only route/step | URL + `history.state` | selected view only | back/forward changes view, never operation |
| Portal session/CSRF | BFF launch session | HttpOnly cookie + in-memory response token | rotate on restart; never runner credential |
| Workspace/operation/idempotency | Issue #9 runner journal | opaque IDs/status | retry queries/returns committed operation |
| Verification | Fresh Issue #9 verifier result | read-only summary | stale/uncommitted result cannot complete |
| Evidence bytes | Issue #9 immutable verified handle | metadata/link only | digest/handle disagreement blocks |
| Completion/progress | One server-side implementation of the exact released Issue #8 authority | derived read-only state | released CAS/transaction/reconciliation; browser never writes completion |

The accepted master authority permits local server-side persistence, but Issue #8 owns the exact
completion/CAS/reconciliation contract and its released binding. The later amendment must pin the
storage path/driver only if the #7/#8 handoffs make them concrete. If no compatible local binding
meets the authority/recovery tests, readiness stops for a reviewed decision; do not silently
replace the authority with browser storage, ad hoc JSON, or a second progress truth.

Never store a runner credential, CSRF token, canonical progress, completion, evidence bytes, raw
logs, or private locators in `localStorage`, `sessionStorage`, IndexedDB, URL query/fragment, or a
service-worker cache. Non-sensitive route step and an outstanding idempotency key may live only in
`history.state` so reload can reconcile without replaying a mutation.

## Routing, History, and Reset

Exact route literals are deferred to the released #8 browser contract and the later amendment;
none is authorized now. The interactive and static/no-JavaScript routes must remain same-origin
and deterministic. The selected narrative step comes from the exact released lesson step ID and is
validated against the release; no canonical progress or operation state is encoded in the URL.
Read-only step changes use `pushState`. Status refresh and mutation completion use
`replaceState`. `popstate` changes only the visible read-only step and fetches canonical state; it
never repeats a POST.

For reset:

1. Create one cryptographically random idempotency key and store it in the current history entry
   before the request.
2. Disable duplicate activation and share the in-flight promise.
3. Send the exact Issue #8 mutation to the BFF; the BFF calls the exact Issue #9 reset operation.
4. On timeout/reload, query/retry with the same key and reconcile the runner's committed result.
5. Only after the released ready-state oracle passes may the BFF update canonical progress.
6. Preserve earlier immutable evidence; reset never deletes it and never completes the lesson.

## Static and No-JavaScript Path

The static renderer authorized by the later amendment must consume the exact Issue #8 release
through the same validator/view model as the interactive route. It deterministically emits the
released static route and a no-JavaScript link/fallback. The generated page contains the business question, four grains, calculations,
limitations, controlled-versus-environmental explanation, exact
`insufficient-evidence / no-common-grain` outcome, reset explanation, baseline-fixture label,
runner-unavailable state, and no completion control.

There is no hand-maintained second lesson, copied raw fixture, ignored fixture, or separate fact
source. Contract/content hash changes regenerate both modes and equivalence tests compare stable
IDs/text facts. Static fallback remains useful when runner or JavaScript is unavailable but does
not claim a run occurred.

## Exact Journey Data Flow

1. Render the Retail Operations business question from the released lesson.
2. Show promotion, fulfillment, returns, and data-quality marts as four independent grains.
3. Stage B starts an isolated workspace using only the released typed operation.
4. The released runner produces the controlled `PROMOTION_HEADLINE_INSUFFICIENT` failure.
5. The UI distinguishes this expected lesson failure from environmental/runner failure.
6. Record the exact canonical decision `insufficient-evidence` / `no-common-grain`.
7. Reset idempotently and prove base/golden hashes remain unchanged.
8. Run the released verification operation against the fresh workspace.
9. Validate committed evidence schema, canonical digest, artifacts, dependency/fixture/tested-tree
   identities, and completion predicates.
10. Commit completion once through the Issue #8 authority, display metadata, and provide a
    bounded integrity-checked download.

Stage A renders/explains steps 1, 2, 4, 5, 6, and 7 from released static content but executes none
of steps 3 or 7..10.

## Evidence Display and Download

Display only released safe fields: evidence/run/lesson/lab IDs and versions, decision/reason,
assertion results, tested tree, dependency release SHAs, fixture/contract/verifier hashes,
artifact media type/size/SHA-256, status, redaction/retention class, and honest local-integrity
language. Never display absolute paths, raw environment, credentials, private runner URL,
unbounded logs, raw customer/order identifiers, or HTML from an artifact.

The BFF accepts only an opaque evidence/artifact ID present in the canonical index, requests the
exact immutable verified handle from #9, confirms metadata/digest before exposure, and streams the
bounded regular bytes with `Content-Disposition: attachment`, `X-Content-Type-Options: nosniff`,
`Cache-Control: no-store`, exact length, digest, and ETag. Handle/digest/size/media-type drift
blocks the response and completion. The browser UI displays the expected digest; automated tests
hash the downloaded bytes. Local SHA-256 is corruption detection, not publisher authentication or
non-repudiation.

## Offline and Unavailable Behavior

- No service worker or offline mutation queue.
- Network loss after page load keeps validated narrative visible, disables mutation, announces
  offline status once, and offers explicit retry.
- Runner absent/starting/not-ready/crashed is an environmental state, not the controlled failure.
- Required local tool absence blocks before mutation with released remediation.
- Rill, Airflow, Iceberg, OpenMetadata, Docker, cloud, and AWS remain optional/unstarted and are
  never queried by the core journey.
- Stage A is the durable fallback if Stage B containment or runner readiness fails.

## Performance Shape

Run one portal/BFF process, one released runner process, and the existing bounded local
DuckDB/core entrypoints. Poll only while an operation is active with released bounds; no
background refresh storm, broker, container stack, or eager evidence buffering. Stream bounded
artifacts and lazy-render large evidence tables. This respects the 16 GiB design envelope without
inventing a numeric performance/resource release threshold owned by Issue #8.
