# Lesson and Lab Contract

## Purpose

One versioned contract drives authoring, portal rendering, runner authorization, verification,
evidence, accessibility, and remediation. Content must be project-owned and may borrow only
interaction principles—not prose, assets, layout, styles, or implementation—from the reference
site.

Planned sources:

- `learning/contracts/lesson.schema.json`
- `learning/contracts/lab.schema.json`
- `learning/contracts/lab-state.schema.json`
- `learning/contracts/evidence.schema.json`
- `learning/lessons/<lesson-id>/lesson.yaml`
- `learning/lessons/<lesson-id>/content.mdx`
- `learning/labs/<lab-id>/{starter,solution,verification}/`

## Required Lesson Fields

| Field | Required content | Validation |
|---|---|---|
| `id/version/title/summary` | Stable kebab ID and semver contract version | Schema + uniqueness |
| `level/competencies` | Foundation, junior, mid; competency IDs | IDs exist in curriculum graph |
| `outcome` | Observable learner capability | Non-empty; tied to completion evidence |
| `stakeholder` | Actor, concern, business decision | Traceability link required |
| `prerequisites` | Competency and environment/tool requirements | Acyclic graph; optional tools marked |
| `fr/nfr/asr` | Measurable functional and quality requirements | Threshold or explicit TBC/blocker |
| `architectureViews` | Minimum C4/dynamic/deployment sources needed | View IDs exist and render |
| `decision` | Question, alternatives, trade-offs, selected/default status | ADR link; unresolved state visible |
| `patterns` | Pattern plus failure/quality attribute it addresses | Reject unmotivated pattern |
| `narrativeSteps` | Reversible ordered acts; static equivalent | Unique IDs; no scroll-only completion |
| `lab` | Lab manifest ID | Referenced lab validates |
| `evidence` | Assertions and artifacts required for completion | Verifier IDs exist |
| `reflection` | Prompt tied to trade-off/outcome | Cannot set completion |
| `accessibility` | Keyboard, announcements, motion/static, text alternatives | Required checklist |
| `remediation` | Failure code to useful next action; solution reveal policy | Every expected failure mapped |

## Required Lab Fields

| Field | Required content |
|---|---|
| Identity | `id`, `version`, `lessonId`, `risk`, `profile` |
| Inputs | Typed parameters, enum/range/length limits, defaults; never shell fragments |
| Workspace | Template source, allowed relative paths, quota, cleanup/retention |
| Commands | IDs from the runner registry with typed args, timeout, CPU/memory/disk/network policy |
| Starter | Project-owned starting files and expected initial state |
| Controlled failure | Trigger, learner-visible symptom, expected evidence, safe boundary |
| State machine | Legal transitions, lock/idempotency behavior, crash recovery |
| Reset | Scope, atomicity, preserved progress/evidence, post-reset oracle |
| Verify | Ordered assertions, severity, failure codes, deterministic inputs |
| Solution | Versioned files/explanation, reveal prerequisites, separate from starter |
| Evidence | Required metadata/artifact hashes and retention class |
| Accessibility | Announced status, non-color cues, keyboard operation, reduced-motion/static path |
| Remediation | Failure code, likely cause, safe action, deeper diagnostic |

## First Representative Journey

### Outcome and stakeholder

- Stakeholder: Retail Operations Director, supported by Data Product Owner.
- Business question: **Can we trust a promotion decision when fulfillment delays,
  returns/refunds, and controlled data-quality failures distort headline performance?**
- Data products: existing promotion, fulfillment, returns, and data-quality marts.
- Learner outcome: trace a decision from concern to FR/NFR, architecture views, raw/model/metric
  contracts, a controlled failure, reset, verified data product, and tamper-evident evidence.

### Acts

1. Frame the decision, stakeholders, capability/value stream, and success threshold.
2. Inspect system context/container and promotion-evaluation dynamic view.
3. Run bounded deterministic generation/load/dbt/export through allow-listed commands.
4. Observe a deliberately naive campaign assessment that overweights headline revenue and fails
   required quality/operational assertions.
5. Trace controlled anomalies and model/lineage to the four existing marts.
6. Compare architecture/data-product alternatives and record a bounded decision.
7. Reset the failed workspace; prove the base repository and golden contracts are unchanged.
8. Apply the lesson-owned typed campaign-decision configuration in a fresh workspace.
9. Verify query/metric/quality rules and produce evidence; optionally replay from reset.
10. Reflect on trade-offs and hosted/AWS evolution without requiring cloud execution.

### Completion threshold

All critical verifier assertions pass, evidence hash validates, the required decision response is
recorded, and the learner can reach the result through the keyboard/static route. Remediation may
be used. Scroll position, time spent, solution file presence, or reflection text alone never
marks completion.

## State Machine

```text
not_started -> preparing -> ready -> running
running -> controlled_failure -> diagnosing
diagnosing -> running
running -> verifying -> verified -> evidenced -> completed
preparing|ready|running|controlled_failure|diagnosing|verifying -> reset_pending
reset_pending -> resetting -> ready
preparing|running|verifying|resetting -> failed
failed -> reset_pending | recovering
recovering -> ready | failed
```

Rules:

- One mutating operation per workspace lock.
- Every request has `operationId` and idempotency key.
- Duplicate in-flight key returns the same operation; conflicting reset/publish receives a typed
  conflict and never races.
- Evidence binds only the last committed verified run.
- Reset replaces the lab workspace atomically and preserves prior immutable evidence unless the
  learner explicitly invokes a separate, confirmed evidence-delete operation.
- From any interrupted state, resume reports the last committed transition and offers bounded
  recover/reset.

## Runner Command Contract

Initial registry:

| Command ID | Purpose | Allowed inputs | Side effects |
|---|---|---|---|
| `workspace.prepare` | Copy validated lesson assets into isolated workspace | lesson/lab version | Workspace only |
| `retail.generate` | Existing generator with bounded profile/seed/output | enum profile, bounded seed/rows | Workspace data |
| `retail.load` | Existing loader against workspace DuckDB | manifest/workspace refs | Workspace DB |
| `retail.dbt-build` | Selected existing dbt graph | selector from allow-list | Workspace DB/artifacts |
| `retail.export` | Existing curated Parquet exporter | fixed curated contract | Workspace exports |
| `promotion.configure` | Write the bounded campaign-decision configuration | enums, booleans and ranges from the lab schema | One allowed workspace file |
| `promotion.verify` | Run lesson verifier against four marts/evidence | run ID | Evidence staging |
| `workspace.reset` | Atomic recreate from starter | workspace/run ID | Workspace only |

`terraform apply`, arbitrary binaries, shell strings, user-controlled working directories,
network destinations, and raw environment injection are absent. Later command additions require
threat model, typed schema, tests, and owner approval.

## API Contract

Planned synchronous OpenAPI operations:

- `GET /v1/lessons`, `GET /v1/lessons/{lessonId}`
- `POST /v1/labs/{labId}/workspaces`
- `GET /v1/workspaces/{workspaceId}`
- `POST /v1/workspaces/{workspaceId}/operations`
- `GET /v1/operations/{operationId}`
- `POST /v1/workspaces/{workspaceId}/reset`
- `POST /v1/workspaces/{workspaceId}/verify`
- `GET /v1/evidence/{evidenceId}`

Every mutating operation requires idempotency/correlation headers and returns typed problem
details. The logical taxonomy is metadata:

- Experience: lesson/progress views.
- Process: start/reset/verify use cases.
- System: runner orchestration and data-product query.
- Backend: adapter operations.
- Technical: health/readiness/evidence integrity.

Initial physical service count remains portal + runner. Long-running local operations use bounded
HTTP polling or SSE documented in OpenAPI. AsyncAPI is added only if an actual broker/channel is
later introduced.

## Evidence Record

Required fields:

- `schemaVersion`, `evidenceId`, `lessonId/version`, `labId/version`
- actor mode/ID (local actor initially), workspace/run/operation IDs
- `inputGitSha`, official golden main SHA, lesson content hash, verifier version/hash
- environment/tool versions, OS/architecture, profile and sanitized parameters
- ordered state transitions and allow-listed command IDs
- assertions with IDs, expected/actual summaries, severity and result
- artifacts with media type, relative locator, size and SHA-256
- start/finish timestamps and duration
- redaction/retention class
- canonical payload SHA-256; later optional signer/key ID for hosted mode

Evidence must never contain tokens, full environment dumps, raw Terraform plans/state, PII
canaries, or absolute local paths. JSON Schema and canonicalization tests reject unknown
security-sensitive fields.

## Accessibility Contract

- All narrative, diagrams, code, controls, status, definitions, and evidence are reachable in a
  logical keyboard order.
- Dynamic state changes use appropriate live-region announcements without flooding.
- Diagrams have structured text/table equivalents and retain meaning at 200% zoom.
- Motion is optional; `prefers-reduced-motion` and static mode preserve every fact/control.
- Color is never the only state signal; focus is visible; targets and contrast meet WCAG 2.2 AA.
- Browser back/forward and reverse journey navigation do not corrupt progress.
- Automated axe/unit tests are necessary but manual keyboard and screen-reader review is a
  release gate.

## Remediation Contract

Every expected failure has:

- stable code, e.g. `DQ_DUPLICATE_ORDER`, `METRIC_REFUND_NOT_ACCOUNTED`,
  `RUNNER_WORKSPACE_CONFLICT`;
- what happened in learner language;
- whether it is controlled, environmental, or unexpected;
- evidence link and likely cause;
- one safe next action and optional deeper diagnosis;
- solution reveal eligibility;
- reset impact.

Unexpected infrastructure failures never masquerade as controlled lesson failures and never
advance progress.

## Contract Fitness Commands

Future tracked commands:

```bash
make learning-contracts-check
make api-contracts-check
make lesson-check LESSON=promotion-trust
make lesson-e2e LESSON=promotion-trust
make evidence-verify EVIDENCE=.artifacts/evidence/<id>/evidence.json
```

The implementation issue must make these commands discoverable through `make help` and record
their versions/results in evidence.
