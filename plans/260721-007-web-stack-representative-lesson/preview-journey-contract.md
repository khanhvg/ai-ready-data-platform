# Preview Journey Contract

## Outcome and Authority

The first runnable issue #7 artifact is a project-owned, framework-neutral, interactive/static
review surface for the promotion-trust lesson. It is useful before a stack decision and remains
runnable after no-winner. It is not the I5-05 product, does not execute a lab, and cannot complete
a lesson.

The exact visible label is permanent:

> SYNTHETIC LEARN-PREVIEW — UNSCORED — CANNOT COMPLETE

It appears at the page entry, state/evidence rail, verify/evidence result, and every evidence
view/export. Hiding or shortening it fails `WEB-PREVIEW-001`.

## Decision Question

For a Retail Operations Director supported by a Data Product Owner:

> Can we trust a promotion decision when fulfillment delays, returns/refunds, and controlled
> data-quality failures may distort the headline?

The bounded answer is `insufficient evidence`. The lesson teaches why the current evidence cannot
support causal promotion attribution; it does not manufacture a campaign-grain product.

## Entry Prerequisite Probes

The probes are unscored, non-blocking, and used only to choose explanation depth:

1. Grain: identify the fields defining a row in two sample mart summaries.
2. Weighted measure: choose displayed numerator/denominator reasoning rather than an
   average-of-averages.
3. Failure class: distinguish an intentionally failing analytical assertion from a missing or
   mismatched fixture.

Skipping or answering incorrectly never lowers a hidden score or traps navigation. Probe state is
local/transient and cannot alter verifier output, evidence truth, or completion.

## Deterministic Hint Ladder

Every consequential prompt offers:

1. `orient`: point to the grain/status/measure and restate the decision.
2. `connect`: expose the numerator/denominator, weighting, failure, or limitation relationship.
3. `explain`: show worked reasoning and limitation; allow retry or review-mode continuation.

Viewing a hint may be recorded but never counts as pass/fail or completion.

## Ten Acts

| Act | Learner purpose | Static/no-JS content | Progressive/reversible enhancement | Forbidden authority |
|---|---|---|---|---|
| 1. Frame | Name stakeholder, concern, capability/value stream, decision and success threshold | Heading, question, threshold/limitations and probes | Probe feedback selects hint depth | No grade/completion |
| 2. Inspect context | Understand the local system and promotion-evaluation sequence | Project-owned diagram plus structured text/table equivalent | Explicit disclose/collapse with focus return | No copied reference layout/source |
| 3. Simulate pipeline | Understand generator→load→dbt→export prerequisites | Ordered command-shaped explanation labelled simulation | Explicit replay control changes only preview status | No subprocess/runner/mutation |
| 4. Observe controlled failure | See the naive promotion headline fail the bounded assertion | Controlled failure code, symptom, why intentional, next action | Named action commits diagnosis step | Environmental failure cannot substitute |
| 5. Diagnose evidence | Inspect grains, filters, measures, lineage, limitations | Four separate semantic cards/tables | Independent disclosure; no linking/filtering across cards | No cross-grain join/causality |
| 6. Compare alternatives | Choose an evidence-bounded decision | Alternatives include `insufficient evidence` and missing-data explanation | Ephemeral choice + hints; explicit commit | Cannot accept a product/ADR decision |
| 7. Reset | Learn safe recovery and base/golden preservation | Reset scope/oracle and synthetic integrity explanation | Idempotent reset, count increments, same baseline digest | No repository/data mutation |
| 8. Inspect typed remediation | See a lesson-owned schema-shaped configuration | Escaped project-owned code/data example | Reversible field explanation, not editing shared config | No write/API/runtime MDX |
| 9. Verify and review evidence | Understand query/metric/quality/evidence checks | Fixture-only assertion/evidence table and exact label | Explicit verify/replay/evidence controls | Verify never completes |
| 10. Reflect | Explain trade-offs and local→hosted/AWS evolution | Prompt, consequences, further reading, no cloud prerequisite | Local draft/reveal only | Reflection/time never completes/cloud-calls |

## Four Grain-Honest Evidence Cards

| Card | Exact grain | Must disclose | Supports | Cannot establish |
|---|---|---|---|---|
| Promotion headline | `promo_name, channel` | completed-order/time filters; order count; gross/discount/net numerators; weighted AOV and discount ratio | Headline promotion/channel performance under stated filters | Carrier, region, return, or DQ causality for a promotion |
| Fulfillment context | `carrier, region` | shipment denominator; on-time numerator/rate; in-transit exclusion; delivered lead-time rule | Separate operational delivery context | A promotion caused a delay |
| Returns/refunds context | `return_reason, category, region` | return count; refund numerator/denominator; weighted refund; category-selection limitation | Separate returns/refunds context | A promotion caused a return/refund |
| Global DQ context | global `scenario, count` | controlled scenario ID/type, count, affected global scope | Separate platform quality warning context | A global DQ event belongs to a promotion |

Cards may align visually by evidence type only. No combined row, shared filter, join line, Sankey
edge, causal arrow, copy, state field, export relationship, or verifier assertion may connect an
operational/return/DQ fact to a promotion. The conclusion states the missing future data needed:
an additive common order/promotion/time grain under separate authority.

The invariant requires `WEB-CONTRACT-002`, `WEB-CONTRACT-003`, `WEB-TRUST-001`, and
`WEB-TRUST-002` plus semantic DOM, normalized screenshots, verifier JSON, forbidden-attribution
scan, and reviewer attestation.

## Preview State and Navigation

Allowed states only:

```text
not-started
exploring
controlled-failure-shown
diagnosing
reset-demonstrated
fixture-verified
evidence-reviewed
reflection-open
```

`completed` is absent from source schemas, DOM state, URL, storage, events, evidence, and export.

State fields include stable preview attempt ID, fixture kind/digest, current/committed act,
declared transient draft policy, hint level, failure class, reset count, fixture-verify status,
evidence-review status, and last explicit action. Browser state is an untrusted projection.

Rules:

- Named controls or native links commit. URL/history records committed act.
- Back/forward/reload restore the last committed act. Transient text is explicitly restored as a
  draft or discarded; it is never silently committed.
- Scroll, intersection observers, animation end, hover, elapsed time, card visitation, and focus
  movement never commit or verify.
- Reset clears transient state, returns the exact synthetic baseline digest, increments a visible
  counter, and explains no repository/data asset was touched. Duplicate reset is idempotent.
- Fixture kind/digest change invalidates state. URL/storage tampering resets safely and cannot
  author verifier/evidence truth.
- Evidence rail shows act, fixture kind/digest abbreviation, failure class, last committed action,
  reset/verify state, evidence count, and the permanent label. At narrow/200% it becomes an in-flow
  summary landmark and never covers focus/content.

## Failure Contract

| Class | Codes | Copy/recovery/progression |
|---|---|---|
| Controlled analytical | `PROMOTION_HEADLINE_INSUFFICIENT` | Explain intended assertion failure; diagnose grains/measures/limitations; may progress only to diagnosis |
| Environmental | `FIXTURE_UNAVAILABLE`, `FIXTURE_DIGEST_MISMATCH`, `STATIC_ASSET_UNAVAILABLE` | Identify broken input/environment, stop attempt, repair/restart with digest; never become the lesson challenge |
| Unexpected product | `PREVIEW_UNEXPECTED` | Preserve safe trace, stop, fix product; no progression |
| Future authorization, compatibility only | `SESSION_ORIGIN_REJECTED`, `CSRF_REJECTED` | Document future portal/BFF behavior; not emitted/implemented by issue #7 |

Copy, icon/text cue, semantic status/error relationship, evidence, safe next action, and progression
must differ by class. Color is never the only distinction.

## Verify, Evidence, Export, Reflection

- Verify validates the synthetic fixture projection and four-grain invariant. It does not call a
  runner, mutate state outside the preview, or mark completion.
- Evidence displays deterministic IDs, synthetic fixture digest, source mart, assertion result,
  normalized fixture timestamps, and safe relative locators.
- Export contains safe synthetic values only and starts with the permanent label. It excludes
  absolute paths, environment, credentials, headers/cookies, personal data, executable content,
  or score/winner fields.
- Reflection can be drafted, reset, and revisited. It never changes verifier/evidence/completion.

## Accessibility and Static Contract

- Use native landmarks, headings, links/buttons, disclosure semantics, tables, status/error
  relationships, visible focus, skip link, and non-color state labels.
- Source order is the narrative order. All facts/limitations/evidence/failure explanations and a
  linear previous/next path exist in HTML before JavaScript.
- JavaScript-off mode may omit rich manipulation but not the facts, decision, labels, limitations,
  or understandable review sequence.
- `prefers-reduced-motion: reduce` removes nonessential motion; static states/text exist before and
  after animation. No auto-scroll or focus theft.
- At 200%/narrow view, no two-dimensional narrative scrolling; cards/rail reflow; focused controls
  remain visible.
- Automated semantic/axe/emulation tests are necessary, while manual keyboard, named screen
  reader, 200%, reduced-motion, and no-JS review are mandatory Gate C evidence.

## Security and Non-Copy Constraints

- Only trusted project-owned content is compiled at build time. Synthetic/real fixture values are
  escaped data or schema-rejected; no runtime MDX/eval/raw HTML/remote import.
- Network allow-list is own static assets and an optional same-origin read-only replay in
  candidates. No external fonts/CDN/analytics/service worker/runner/cloud/mutation.
- Project wording, diagrams, components, spacing, colors, timing, interaction, and source are
  independently authored. The reference supplies principles only.
- The non-copy inventory records each principle, project expression, source/license, and reviewer
  result. Any derivative prose/asset/layout/style/source is removed and rebuilt before publication.

## Acceptance and Rollback

The preview is reviewable only when all applicable common WEB tests, non-copy review, protected
path checks, and safe lifecycle pass. Fresh manual browser evidence is still required for
decision-grade candidate acceptance. On failure, remove unsafe enhancement, flatten to the
semantic static document, clear only scoped preview state, retain evidence, and never manufacture
completion or a framework decision.
