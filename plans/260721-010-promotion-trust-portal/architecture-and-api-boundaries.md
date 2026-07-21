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

## Exact Planned Implementation Paths

The future implementation may create/promote only the following product layout. The exact Issue
#7 handoff decides which listed Vite/TypeScript scaffolding files are copied unchanged versus
minimally adapted; a path mismatch at the handoff gate stops implementation.

```text
apps/learning-portal/
  package.json
  package-lock.json
  index.html
  vite.config.ts
  tsconfig.json
  playwright.config.ts
  scripts/verify-release-gates.mjs
  scripts/render-static-fallback.mjs
  src/client/main.tsx
  src/client/app/portal-app.tsx
  src/client/app/portal-router.ts
  src/client/app/route-state.ts
  src/client/components/error-summary.tsx
  src/client/components/status-region.tsx
  src/client/components/runner-unavailable.tsx
  src/client/features/promotion-trust/business-question.tsx
  src/client/features/promotion-trust/four-mart-context.tsx
  src/client/features/promotion-trust/controlled-failure.tsx
  src/client/features/promotion-trust/decision-panel.tsx
  src/client/features/promotion-trust/reset-panel.tsx
  src/client/features/promotion-trust/verified-evidence.tsx
  src/client/features/promotion-trust/evidence-download.tsx
  src/client/styles/portal.css
  src/server/main.ts
  src/server/config/runtime-config.ts
  src/server/contracts/released-contracts.ts
  src/server/contracts/release-bindings.generated.ts
  src/server/http/bff-router.ts
  src/server/http/http-security.ts
  src/server/runner/released-runner-client.ts
  src/server/state/completion-repository.ts
  src/server/state/reconciliation.ts
  src/server/evidence/evidence-service.ts
  src/shared/problem-details.ts
  src/shared/portal-view-models.ts
  src/static/promotion-trust-document.ts
  tests/unit/
  tests/contracts/
  tests/security/
  tests/accessibility/
  tests/e2e/
  tests/visual/
```

Also create `mk/issue-5/i5-05.mk`. Do not modify the root Makefile; Issue #6 already owns the
include/help seam. `package-lock.json` is staged by exact path if the repository ignore rule still
matches it; `.gitignore` is never edited.

The directories in the tree are boundaries, not permission to create every conceivable helper.
Keep files small and combine components when the released handoff makes a separate file
unnecessary. No implementation path outside this tree and the issue Make fragment is implied.

## Contract Binding Policy

`release-bindings.generated.ts` is created only after GA/GB pass. It records exact released
method/path/`operationId` values, schema/type imports, registry command IDs, version strings, and
source digests. It is regenerated deterministically from the released handoffs and compared in
tests. It must not contain:

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
| Completion/progress | Portal SQLite implementing exact Issue #8 authority | derived read-only state | transaction/reconciliation; browser never writes completion |

The accepted master authority already selects portal SQLite for completion/progress. Store it
under an untracked, namespaced I5-05 runtime root such as
`.artifacts/runtime/learning-portal/{worktree-namespace}/portal.sqlite3`. The exact compatible
Node driver is selected only from the released Node/package handoff and locked in the app lock.
If no compatible driver can meet the authority/recovery tests, readiness stops for a reviewed
decision; do not silently replace SQLite with browser storage or ad hoc JSON.

Never store a runner credential, CSRF token, canonical progress, completion, evidence bytes, raw
logs, or private locators in `localStorage`, `sessionStorage`, IndexedDB, URL query/fragment, or a
service-worker cache. Non-sensitive route step and an outstanding idempotency key may live only in
`history.state` so reload can reconcile without replaying a mutation.

## Routing, History, and Reset

Portal-owned document routes are:

- `/learn/promotion-trust` — interactive shell; Stage A is read-only.
- `/learn/promotion-trust/static` — generated semantic static/no-JavaScript equivalent.

The selected narrative step comes from the exact released lesson step ID in the URL query and is
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

`render-static-fallback.mjs` consumes the exact Issue #8 release through the same validator/view
model as the interactive route. It deterministically emits
`dist/learn/promotion-trust/static/index.html` and the `noscript` redirect/link in the built
entry document. The generated page contains the business question, four grains, calculations,
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
