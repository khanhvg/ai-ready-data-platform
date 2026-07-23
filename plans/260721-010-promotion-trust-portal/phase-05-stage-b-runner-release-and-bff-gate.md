---
phase: 5
title: "Stage B runner release and BFF gate"
status: completed
priority: P1
dependencies: [4]
effort: "S"
---

# Phase 5: Stage B Runner Release and BFF Gate

## Overview

Dependency and boundary discovery is complete. PR #31 shipped Stage A and PR #32 shipped the
runner. This phase records the exact compatibility decision used by Phase 6; it performs no
product write.

## Verified Dependencies

- Portal merge: `041d4ca866e927a331e159fdf8216838b481a595`.
- Portal reviewed head: `473f54c2e0879d3037cbed25b2e7a3f0626d558d`.
- Runner/integration release: `671201f78024786a9f2eba5e9e5fce7c78b4443d`.
- Runner reviewed head: `86a6c259ad384591777cf1d46f2f6c9ea6327361`.
- Runner release gate: 66/66 = 52 RED + 14 S3.
- Implementation base: exact integration `671201f…`.

## Contract Finding

Issue #9 publishes an owner CLI and private UDS/loopback transport implementation. It does not
publish the general learning-platform HTTP API for portal use. The safe minimal adapter is
therefore:

1. one portal-owned loopback BFF;
2. one server-only fixed action → released operation map;
3. one serialized owner-CLI subprocess at a time;
4. one pending-call reconciliation path over released immutable runner evidence;
5. one released progress/completion authority and one learning-evidence projection.

The browser receives neither the runner socket/control record nor runner bearer/CSRF values. It
cannot submit operation IDs, commands, argv, environment, paths, URLs, SQL, images, packages,
plugins, Docker options, or cloud options.

## Shared-Core Decision

No shared-core change is authorized. Phase 6 reads the released lab, lesson, progress,
completion, and evidence contracts and invokes their existing validation/semantic functions. If
the pinned runtime cannot import those existing functions, cook stops and reports that exact
narrow dependency. It must not copy their logic into a second authority.

## Success Criteria

- [x] Stage A merge and post-merge smoke verified.
- [x] Runner release/review/integration identities verified.
- [x] Actual released CLI/registry/state/evidence/reset semantics inspected.
- [x] No absent runner API assumed.
- [x] Exact Stage B write set, commands, operations, adapter, journey, and rollback recorded.
- [x] Phase 6 is unblocked for the bounded Stage B scope.

## Next Steps

Cook only Phase 6 from exact integration `671201f78024786a9f2eba5e9e5fce7c78b4443d`.
