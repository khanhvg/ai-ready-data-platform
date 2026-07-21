# Scenario Report

## Execution summary

- Skill: `$ck:scenario --iterations 15`
- Mode: pre-plan discovery saturation loop; no implementation mutations.
- Input: `f9a87d0ebdb72c014a6f8c6eaae865dad4d2188c`.
- Iterations: 15 exactly.
- Coverage: all 12 core dimensions, followed by three cross-dimensional variants.
- Findings: 12 New, 3 Variant; 8 Critical, 7 High; 0 Medium/Low discarded.
- Machine-readable log: `scenario-results.tsv`.

All findings are retained because each can cause silent semantic corruption, unauthorized publication, evidence disclosure, irreversible workspace damage, or an invalid cross-issue handoff. The owner columns deliberately assign later-issue responsibilities without widening I5-01.

## Saturation progress

### Iterations 1–5

Five new scenarios established the publication persona, adversarial path, hash/read timing, resource-bound, and release-transition failure surfaces. The dominant pattern was that “deterministic” cannot be evaluated separately from workspace authority and atomic state transitions.

### Iterations 6–10

Five additional new scenarios covered ambient dependency drift, lifecycle artifact overwrite, integrity/authenticity confusion, semantic mutation hidden by aggregate counts, and Make registry collision. No overlap was collapsed because each requires a different acceptance oracle and owner boundary.

### Iterations 11–15

Three final core dimensions added tracked-evidence disclosure and grain-invented business logic. The last three iterations intentionally combined earlier dimensions: partial-release coherence, pre-merge identity timing, and backward-reader rollback. New issue rate fell from 100% in the first ten iterations to 40% in the last five, with three meaningful variants; further discovery would mostly elaborate implementation tests rather than change planner decisions.

## Four-step failure paths

Each retained scenario was exercised as a minimum four-step path rather than a one-line edge case:

1. **SC-01:** issue #7 locates a provisional fixture → treats local tested-tree identity as publication identity → runs the scoring gates → publishes a score/ADR before merge.
2. **SC-02:** caller supplies an escaping/symlinked path → harness performs a lexical or stale check → write/cleanup follows the changed target → user-owned bytes are overwritten/deleted.
3. **SC-03:** producer validates a path → attacker/concurrent process replaces it → producer reopens and hashes/publishes by path → manifest certifies different bytes from those validated.
4. **SC-04:** fresh host starts unlocked network bootstrap → resolver/download/log growth exceeds a bound → parent times out without killing descendants → partial environment/evidence is later mistaken for reusable state.
5. **SC-05:** publisher stages only part of 11 assets → process dies around pointer update → reader follows an incomplete/mixed release → recovery drops or overwrites the last good generation.
6. **SC-06:** harness reuses ambient env/stale venv → shadowed module or resolver drift changes execution → Git input remains the same → evidence falsely attributes the result solely to that input SHA.
7. **SC-07:** dbt build produces warning-rich results → docs generation replaces `run_results.json` → collector reads only the later artifact → golden projection omits or mislabels build warnings.
8. **SC-08:** publisher hashes canonical bytes → hostile actor replaces bytes and recomputes unkeyed hashes → verifier checks internal consistency only → UI/docs label the artifact signed/authentic.
9. **SC-09:** semantic field/edge/expression mutates → totals/nonzero checks remain stable → coarse oracle passes → later consumer receives behavior outside the frozen contract.
10. **SC-10:** issue fragment/root help duplicates a target → Make chooses/combines an unintended recipe → another owner's lifecycle changes → registry still appears discoverable but no longer authoritative.
11. **SC-11:** command output/environment includes sensitive locator/value → raw bundle is copied directly into tracked fixture → hash/commit makes it durable → remote publication exposes it.
12. **SC-12:** consumer joins promotion aggregates to unrelated fulfillment/returns/DQ grains → many-to-many multiplication or narrative inference occurs → fixture records an apparent effect → lesson teaches unsupported campaign causality.
13. **SC-13:** each asset entry validates independently → entries from two runs share compatible schemas → open-ended manifest accepts the mixed set → current pointer exposes a syntactically valid but incoherent release.
14. **SC-14:** producer records tested tree or attestation commit → reviewer interprets it as merged identity → scoring starts while merge can still change → published result cannot be tied to the final remote fixture.
15. **SC-15:** writer promotes evidence v2 → old schema/reader is removed → regression triggers rollback/re-audit → retained v1 evidence is no longer machine-verifiable.

## Complete Critical/High scenario register

| ID | Sev. | Scenario | Owner | Acceptance evidence | Mitigation and rollback | Dependency | Local-cook STOP condition |
|---|---|---|---|---|---|---|---|
| SC-01 | High | Provisional fixture scorer | I5-01 producer; I5-02/#7 scorer | Common tests may consume an explicitly provisional fixture, but scoring/ADR checks require an authorized tracked artifact, matching hashes, and externally observed merge SHA. | Label preview unscored; invalidate/remove any premature score and re-run only after merge handoff. | F-05 path authority; #6 merge | STOP if I5-01 emits a score/ADR or represents #7 scoring as ready before merge. |
| SC-02 | Critical | Workspace path escape | I5-01 golden workspace; I5-04 generalized runner | Negative tests for absolute path, `..`, symlink component/swap, foreign destination, and protected-path preservation. | Resolve beneath private owned root, no-follow/reject links, exclusive temp creation, scoped deletion. Preserve failure workspace; roll back only scoped pointer/output. | Workspace/run-ID contract | STOP on broad delete, user-selected unresolved path, symlink following, or any protected/unrelated file drift. |
| SC-03 | Critical | Hash/read TOCTOU swap | I5-01 | Mutation process attempts replacement during validation/hash/publish; final manifest hash matches atomically installed immutable bytes or operation fails. | Hash an opened immutable/private descriptor or stage privately then atomic rename; reject post-hash mutation. Retain failed stage and prior pointer. | Filesystem atomicity policy | STOP if code separately checks a path then reopens mutable bytes without identity verification/atomic containment. |
| SC-04 | High | No-cache bootstrap exhaustion | I5-01 | Empty-cache test records per-step time/output/disk bounds; timeout kills descendants; failure bundle is bounded and redacted. | Complete hashed/binary lock, explicit timeout/output cap, disk preflight, deterministic cleanup of owned temp only. Retry with the same lock; prior evidence remains valid. | D-01 lock, D-07 runtime | STOP on unbounded network installer, unbounded log capture, or timeout that leaves children/workspace authority unknown. |
| SC-05 | Critical | Interrupted release switch | I5-01 schema; I5-07 implementation | Crash injection at stage/validate/temp-pointer/rename/reconcile boundaries; readers see either prior complete release or new complete release, never partial. | Immutable staged generation and atomic one-file pointer switch; roll pointer back to prior complete manifest. Never drop prior generation during switch. | I5-07 lease and engine capability | STOP if I5-01 implements publisher logic or schema lacks exact set/generation/rollback identities. |
| SC-06 | High | Ambient environment drift | I5-01 harness; I5-04 broader runner | Two clean runs use allow-listed environment, exact lock/interpreter, fixed locale/timezone, sanitized paths, and no credentials; fingerprints match. | Fresh locked environment, reject unexpected PYTHONPATH/credential inputs, record allowed environment contract. Restore previous lock on regression. | D-01; narrow Airflow path seam | STOP if stale `.venv`, ambient modules/credentials, locale/timezone, or resolver output can change a passing result. |
| SC-07 | Critical | Build evidence overwritten by docs | I5-01 | Test proves dbt build `run_results.json` is captured and hashed before docs; build warning/test IDs remain present in the deterministic projection. | Copy to private immutable stage immediately after build; name by command/artifact type. Fall back to last raw bundle/reader if projection migration fails. | dbt command order; evidence schema | STOP if docs can overwrite the only build evidence or canonicalization cannot distinguish command lifecycle. |
| SC-08 | High | Checksum mislabeled as signature | I5-01 integrity semantics; I5-14 hosted authenticity | Schema/docs distinguish `sha256` integrity from signing; no hosted/trusted-publisher claim; hostile replacement fixture demonstrates limitation. | Use unkeyed hashes locally, record provenance layers, defer actual signature/identity verification to I5-14. Retract overclaim and reissue evidence metadata. | D-05 provenance | STOP if fields/docs use “signed”, “authentic”, or equivalent without a verified signer/trust root. |
| SC-09 | Critical | Semantic drift hidden by totals | I5-01 | Mutation suite independently changes CSV byte, anomaly, dbt edge/test ID, mart schema/value, Rill expression, Airflow edge, curated asset, Iceberg/OM ID; every mutation fails its named assertion. | Hash exact bytes where stable and typed canonical projections where container/runtime fields vary. Roll back contract registry or producer together. | Full characterization envelope | STOP if acceptance relies only on total rows, total models, nonzero reads, or one aggregate hash without itemized diagnostics. |
| SC-10 | High | Make registry ownership collision | I5-01 root seam; later issue fragment owners | Parse exactly 54 unique owner/target entries; issue #6 defines only seven; current 15 target behavior remains; synthetic collision fails. | One root include/help seam and disjoint fragments. Revert include plus I5-01 fragment atomically. | Master registry at input | STOP on duplicate recipe, later-owner target, unapproved root edit, or existing-target semantic drift. |
| SC-11 | Critical | Tracked evidence disclosure | I5-01 | High-confidence credential scan plus schema deny-list/redaction tests over exact staged publication set; no secrets, private URLs, home paths, raw IDs, or runtime identifiers. | Allow-list fixture/evidence fields, sanitize before hashing/publication, fail closed. Remove/revoke leaked material and invalidate artifact; do not rewrite Git history without separate authority. | Publication policy and scanner | STOP on any credential-like value, private locator, raw PII-like row, or unbounded stdout/stderr in tracked output. |
| SC-12 | Critical | Invented promotion attribution | I5-01 contract; I5-07 any future additive data product | Grain metadata and negative SQL/assertion fixtures reject cross-grain causal/campaign joins; fixture exposes only independent aggregate assertions. | Keep promotion, fulfillment, returns, and DQ results separate. Version/invalidate overclaimed contract; add governed product later if approved. | Current marts and #7 lesson | STOP on causal language, campaign-carrier/return/DQ attribution, or fields absent from current governed grains. |
| SC-13 | Critical | Mixed-generation current pointer | I5-01 schema; I5-07 implementation | Negative manifests with one asset from another run, duplicate/extra/missing asset, or different contract hash fail; concurrent reader sees one generation. | Common release/data-run/input/contract identity for exactly 11 assets; validate before atomic switch. Roll pointer back to prior manifest. | SC-05; curated asset registry | STOP if schema permits per-asset generation drift or an unordered/open-ended asset set. |
| SC-14 | High | Score published before merge identity | I5-01 handoff; I5-02/#7 | Three provenance layers are distinct; scorecard requires merge/tag SHA observed from remote and artifact/tested-tree hashes that match authorized fixture. | Treat tested tree/attestation commits as non-merge identities; retract and recompute early score after merge. | SC-01; D-05 | STOP if any self-containing or pre-merge SHA is accepted as the merged fixture identity. |
| SC-15 | High | Rollback cannot read evidence v1 | I5-01 schema/version registry | Retained v1 fixtures validate with current reader; migration compatibility and rollback tests pass; schema hashes remain addressable. | Keep old schemas/readers and immutable evidence; switch current writer/pointer back without deletion. | D-04 version policy | STOP if writer promotion deletes v1 schema/reader, mutates retained evidence, or has no downgrade path. |

## Cross-scenario invariants for the planner

1. **One owned workspace:** all writes, cleanup, and evidence staging are beneath a validated, exclusive run root.
2. **One immutable input:** Git tree identity, lock/tool identity, profile/seed, and dirty-base decision are explicit and non-volatile.
3. **Raw plus projection:** raw artifacts diagnose; versioned canonical projections decide determinism.
4. **Semantic mutation coverage:** exact itemized contracts detect drift hidden by totals.
5. **Atomic publication:** complete immutable generation first, one pointer switch second, prior generation retained.
6. **Separated trust claims:** checksum integrity, Git provenance, and hosted authenticity are different controls.
7. **Grain honesty:** current marts support aggregate comparison, not causal campaign attribution.
8. **Disjoint ownership:** I5-01 schema/seams/fixture only; later publishers, runner, scoring, and signing stay with their issues.

## Composite coverage score

Using the skill rubric:

- Scenarios: `15 * 10 = 150`
- Edge conditions captured across scenario descriptions/acceptance variants: `36 * 15 = 540`
- Dimensions covered: `12 / 12 * 30 = 30`
- Unique actors/roles: I5-01 producer, I5-02 scorer, I5-04 runner owner, I5-06 view lease holder, I5-07 publisher, I5-14 signer, and external reviewer/reader: `7 * 5 = 35`
- Critical-or-High findings: `15 * 3 = 45`

**Composite coverage score: 800.**

## Scenario verdict

**SATURATED FOR PRE-PLAN DISCOVERY.** The 15 iterations cover all required dimensions and converge on the same three immediate planner gates identified by prediction: fixture-path authority, hashed dependency baseline, and supported deterministic architecture rendering. Scenario evidence supports `GO_TO_PLANNER`; every SC-01 through SC-15 STOP remains binding on local cook.
