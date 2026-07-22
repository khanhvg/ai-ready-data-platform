---
phase: 5
title: "Recovery Security and Observability"
status: pending
priority: P1
dependencies: [4]
effort: "L"
---

# Phase 5: Recovery Security and Observability

## Context links

- [Threat matrix](./security-recovery-and-evidence.md#s3-threat-matrix)
- [Recovery scenarios](./requirements-and-risk-traceability.md#recovery-scenario-coverage)
- [Evidence layout](./security-recovery-and-evidence.md#evidence-layout)

## Overview

Close the persistence/DR, S3 security, readiness, observability, teardown and evidence contracts.
Use deterministic offline fault fixtures. Real AWS backup, restore, KMS, IAM, network or resource
tests remain separately authorized and cannot be simulated into a compatibility claim.

## Requirements

- Functional: FR-014..017/019/020.
- Non-functional: NFR-001/002/004..012/014.
- Cover every TH-001..TH-020 and DR scenario.
- Backup success is insufficient without consistency manifest, empty restore and semantic oracle.
- Preserve is default; destroy and break-glass require exact separately authorized envelopes.

## Architecture

```text
state dependency DAG + selected decisions + schedule state
  -> consistency groups / restore DAG / readiness oracles
  -> threat controls and fault injections
  -> observability projections and compact hash-indexed evidence
  -> preserve/destroy rollback decisions
```

Evidence finalization is atomic and content-addressed. It stores safe projections, not raw state,
plans, credentials, account/resource identifiers, PII or private paths.

## Related code files

- Current implementation allow-list: `[]`.
- Exact recovery/security/evidence model/test/ADR files: `TBC` in amendment.
- Candidate ownership envelope only: Issue #14 decision docs/models/tests and Make fragment.
- Shared evidence schemas and golden security helpers are read-only unless an explicit owner lease
  is separately approved.

## Tests before

- Key disabled/deletion/wrong-version; config/secret rotation mismatch.
- Partial/mixed consistency group and corrupt/truncated/foreign backup.
- Empty restore with missing catalog pointer, DB asset, search watermark, dashboard, projection or
  semantic equivalence.
- AZ/region failures with unsupported availability/failover claims.
- Duplicate/out-of-order/missed schedule events and crash at each state transition.
- Preserve/destroy/break-glass missing scope, wrong actor/expiry/SHA, replay and foreign resource.
- Evidence missing/extra/duplicate/tampered/replayed artifacts, recursive hash, sensitive canaries,
  unsafe locator/file type and partial atomic write.
- Observability missing a cost/retention/redaction dimension.

## Refactor

Reuse the canonical state IDs, option IDs and formula/unit registries. Do not create parallel
recovery or evidence schemas per service. Service-specific oracles plug into one bounded registry.

## Tests after

- Each consistency group restores/rebuilds in dependency order and runs exact semantic oracles.
- Observed RPO/RTO remain separate from owner objectives and fail when objectives are absent/missed.
- Every schedule transition is idempotent/reconcilable and cost-observable.
- All threats reject safely with bounded redacted evidence.
- Preserve/destroy and rollback cannot affect evidence, keys, foreign/unrelated state by default.

## Regression gate

```text
make state-matrix-check
make cost-model-check
make aws-decision-check
```

No live restore or cloud resource is part of these commands.

## Implementation steps

1. Write RED-C/RED-E recovery, teardown, observability and evidence fixtures.
2. Define consistency-group and restore-oracle registries from selected state rows.
3. Implement dependency-aware restore/rebuild/readiness evaluation.
4. Implement schedule crash/replay/reconciliation and CostGuard integration.
5. Implement strict preserve/destroy/break-glass policy evaluation without executing actions.
6. Implement safe observability projections and compact atomic evidence/hash indexing.
7. Run sensitive-data, path/link/process, tamper/replay and rollback adversarial suites.
8. Document residual risks and keep real compatibility/RPO/RTO outcomes `blocked-tbc`.

## Success criteria

- [ ] Every selected durable/derived state has a consistent backup or complete rebuild path.
- [ ] Restore oracles cover structural and semantic state before readiness.
- [ ] Key loss, corruption, AZ/region, catalog/metadata/search and schedule failures are explicit.
- [ ] Threat matrix passes with no unresolved Critical/High implementation finding.
- [ ] Evidence is compact, hash-indexed, private-safe and honest about offline scope.

## Risk assessment

Backups often restore bytes while applications remain unusable. Mitigation is cross-component
consistency groups and semantic readiness oracles. Rollback selects the previous complete
decryptable generation or local fallback; it never deletes the failed evidence or fabricates RTO.

## Security considerations

KMS key loss and destructive teardown are irreversible boundaries. Deny by default, separate
administration/use/deletion roles, and require dependency inventories and expiry-bound human
authority. SHA-256 evidence remains integrity-only.

## Next steps

Phase 6 proves every state/decision/cost/evidence row reconciles to exact released concerns and
future Terraform interface bindings without creating Terraform.
