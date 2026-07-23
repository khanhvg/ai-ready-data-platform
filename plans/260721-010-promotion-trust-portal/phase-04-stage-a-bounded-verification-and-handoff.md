---
phase: 4
title: "Stage A closed evidence and exact-head handoff"
status: completed
priority: P1
dependencies: [3]
effort: "L"
---

# Phase 4: Stage A closed evidence and exact-head handoff

## Overview

Complete the seven defensive requirements, run unchanged tests and all 18 commands at the final
head, and atomically publish one closed evidence generation with a real sources-excluded Chromium
trace. This phase can produce implementation-review readiness only—not plan/readiness authority,
merge approval, Issue completion, or Stage B authority.

## Context Links

- [Authenticated lifecycle and blocked result](./stage-a-release-amendment.md#authenticated-lifecycle-and-blocked-result)
- [Current-generation publication](./stage-a-release-amendment.md#current-generation-evidence-publication)
- [Chromium journey and trace](./verification-evidence-and-uat.md#chromium-journey-and-trace)
- [Security/resource bounds](./threat-model-and-security.md#resource-and-artifact-security)

## Requirements

### Defensive behavior

1. Authenticated child status/self-shutdown over a private loopback control listener; never signal
   a mutable recorded PID; tampered state cannot affect the foreign sentinel.
2. Both Stage B negatives emit schema-valid blocked `fitness-result-v2` on stderr, exit 2, leave
   stdout empty, and perform no runner/container/network action.
3. Two deterministic builds produce one closed path/media/size/hash inventory; the server serves
   only it and rejects Host/method/body/chunking/length/decoding/path mutations.
4. Exact Node/npm/Python/runtime-marker/lock/freeze/environment admission; sanitized child env;
   no scripts, fallback runtime/package manager, ambient credential, or undeclared network.
5. One released production descriptor registry plus test-only pure-function structure and
   production rejection/absence gates.
6. Exact process/time/file/byte/count/type/mode/owner/link/privacy/aggregate limits for build,
   logs, screenshots, trace, and full generation.
7. Complete PTP-RED-A and PTP-S3-01..14 valid-control/negative coverage with no skip.

### Evidence closure

- Generate current raw/sanitized GREEN logs for all 18 commands at the final tested head.
- Carry the contemporaneous RED logs forward by hash and verify they predate first semantics.
- Bind base/derived/scaffold/tests/RED/first-semantic/later-semantic/final commits and trees, all
  85 inputs, locks/tools, browser, command argv/exits, resource and S3 results.
- Bind exact Playwright/Chrome channel, Chrome `150.0.7871.181`, and executable SHA-256
  `b724a4c5603cfc8b9d9f27a5153c8a39e7133e53666ced7f2a8b03bf49484f85` identically across
  RED and GREEN; keep the executable path local-private.
- Capture exactly one successful real Chromium trace with mode on and sources false; inspect its
  archive/privacy/count/size and hash it into the closed inventory.
- Use non-self `inventory.json` → `generation-index.json` → atomic regular
  `current-generation.json` closure. Every current entry verifies.
- Classify stale/failed/prior generations as negative history; never use them as current evidence.
- Label current evidence as author/cook-generated with independent review and human approval false;
  later independent records bind the exact head/tree and generation index without rewriting it.
- Inject publication interruption and prove the selector exposes only a prior verified generation
  or none, never partial bytes.

## Related Code Files

Modify only already-created scaffold paths within the exact 33 set, chiefly lifecycle, server,
release verifier, review writer, Playwright config, package scripts, Make fragment, activation,
and security/render integration. Create no new tracked path. Modify no tests after Commit 2 unless
the plan's explicit fresh-tests-only/fresh-RED supersession rule is followed.

## Tests Before

Use the exact Phase 2 RED for lifecycle authentication, blocked schema, build/request policy,
runtime/lock/env admission, generic seam, artifacts/evidence, trace, cleanup/interruption, and all
S3 families. A stale v2 log or detached reconstruction cannot satisfy any row.

## Implementation Steps

1. Implement private authenticated control and child self-shutdown; prove no PID signal call.
2. Implement exact blocked v2 result generation/validation and no-action process/network gates.
3. Finalize deterministic build inventory, static request policy, runtime/lock/env admission, and
   exact activation/Make fragment hash binding.
4. Configure the single journey project with exact Chromium/Chrome-channel admission, trace mode
   on, sources false, one worker, zero retry, and same measured RED/GREEN browser identity; keep
   visual capture separate and produce at most eight named screenshots.
5. Implement pending-generation closure, non-self hashes, privacy/resource/S3 records, atomic
   selector, negative-history classification, and interruption recovery.
6. Commit the final behavior. Record actual final commit/tree; any later code change requires a
   complete new current GREEN generation.
7. Run all 18 commands, two builds, Chromium desktop/narrow/no-JS/axe, lifecycle/down twice,
   Stage B negatives, audit, S3/resource, cleanup/interruption, and rollback rehearsal.
8. Verify all current manifest entries, exact 33/18/85 closure, root Make composition/direct
   denial, #9/#11/#12/#13 non-overlap, secret/private-locator/PII/raw-record/source-map/
   remote-import/cloud scans, package-lock tracking, ignored-inclusive classification, diff check,
   and clean state.
9. Obtain two fresh independent final-head implementation reviews and named human exact-head UAT/
   approval before any later merge workflow. A later commit invalidates them.

## Success Criteria

- [ ] All seven defensive requirements are GREEN through unchanged tests.
- [ ] Raw/sanitized RED and GREEN logs are source/tree-bound and hash-valid.
- [ ] Exactly one compliant current Chromium trace exists; sources are absent.
- [ ] One current generation verifies completely; stale generations are negative history.
- [ ] Atomic interruption, cleanup twice, ignored classification, and rollback pass.
- [ ] Final product scope is 33/33, commands 18/18, released inputs 85/85, Stage B blocked.
- [ ] No cloud, container, AWS, Terraform, approval, merge, or full-product claim occurs.

## Risks and Rollback

| Risk | Mitigation |
|---|---|
| Mutable record kills foreign PID | No signal path; child-held capability and self-shutdown; foreign sentinel negative |
| Hash manifest is internally stale | Non-self three-layer closure plus second verifier before atomic selector rename |
| Successful test loses trace | Journey trace mode on, exactly-one inventory requirement, source/archive inspection |
| Interrupted publish becomes current | Pending sibling plus selector-written-last transaction and negative-history recovery |
| Rerun masks stale evidence | One selected generation per tested head; current source/tree equality mandatory |

Rollback uses authenticated child shutdown, removes only 33 created files and owned scratch, and
retains current/negative-history evidence. It never touches released bytes or failed PR #29.

## Next Steps

After later implementation and reviews, a separately authorized Git workflow may decide PR
publication. Phase 5 remains blocked until Issue #9 has an exact reviewed/merged/pristine release
and a new Stage B amendment passes independent validation/readiness.
