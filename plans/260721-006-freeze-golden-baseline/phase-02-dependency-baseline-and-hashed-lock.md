---
phase: 2
title: "Dependency baseline and hashed lock"
status: pending
effort: "1.0-1.5 implementation days"
dependsOn: [1]
---

# Phase 2: Dependency baseline and hashed lock

## Overview

Publish the exact CPython-3.12/darwin-arm64 wheel-only hash lock selected in [dependency-lock-decision.md](./dependency-lock-decision.md). Prove two independent installs and full runs; never let `golden-clean` resolve or rewrite versions.

## Requirements

- Direct roots and exact 55-package graph, compiler/tool hashes, proposed lock SHA `6552bc…`, normalized environment SHA `e0b9ba…`.
- Exact platform policy; unsupported interpreter/platform fails before network.
- Empty cache/home/venv/data per run; `PIP_CONFIG_FILE=/dev/null`; wheel-only, `--require-hashes`, `--no-deps`.
- A newer resolvable version is irrelevant and must not alter the accepted graph.

## File inventory

| Action | Planned path | Purpose |
|---|---|---|
| Create | `requirements/golden-py312-macos-arm64.{in,lock,metadata.json}` | root pins, complete hashes and identity |
| Create | `requirements/golden-lock-tools.{in,lock}` | fully hashed eight-wheel pip/pip-tools compiler bootstrap |
| Create | `tests/golden/test_dependency_lock.py` | malformed/drift/platform/install assertions |
| Create | `scripts/golden/dependency-lock.py` or equivalent scoped module | read/verify/bootstrap only; never update at runtime |

## Dependency map

- Depends on phase 1 anchors and immutable requirements metadata.
- Blocks the trusted producer in phases 3–5 and formal two-run gate in phase 8.
- Does not edit existing three direct requirement files solely to make the golden lane work.

## Test scenario matrix

| Scenario | Expected |
|---|---|
| Missing hash/unpinned/VCS/path/sdist/index override | lock parser fails before install |
| dbt-core 1.12.0 or adapter 1.24.5 selected | `DEPENDENCY_LOCK_DRIFT` |
| CPython 3.11/3.13, PyPy, x86 emulation/Linux lock reuse | `PYTHON_BASELINE_UNSUPPORTED` |
| Ambient pip config/cache/system-site package | ignored or typed failure; never part of result |
| Two independent archives/caches/venvs | same lock/environment/full semantic projection |
| Missing binary wheel | `LOCK_BINARY_UNAVAILABLE`; no source build |

## Interface checklist

- [ ] `verify_lock(path, metadata, platform) -> exact package/hash inventory`.
- [ ] Runtime path is read-only; compile/update path is distinct and review-only.
- [ ] Compiler itself is bootstrapped from the exact eight-wheel tool lock fingerprint `ece1d206…`; CPython 3.12 bundled pip is the declared local trust anchor.
- [ ] Evidence records patch/build/platform but policy key is CPython 3.12 darwin-arm64.
- [ ] Install cannot use ambient config/index, cache, system site or dependencies outside lock.

## Tests Before

1. Add parser mutations for every forbidden requirement form and candidate fingerprint drift.
2. Add preflight tests for implementation/version/platform/emulation.
3. Run an unlocked current install in private state only to prove it can choose dbt-core 1.12.0; retain as expected failure evidence, never golden.
4. Add two full-run tests expecting the selected lock and environment hashes; fail because tracked locks/bootstrap are absent.

## Implementation

Generate locks once with the exact reviewed compiler command. Assert final path-sensitive byte fingerprint. Implement read-only verification and private empty-cache bootstrap with explicit environment/time/output limits. Run `pip check`, exact package-set comparison, dbt version and full phase-1 characterization.

## Refactor

Separate lock parsing, platform preflight, process execution and evidence projection. Runtime verifier must not import the compiler/update code path.

## Tests After

- Two independent no-cache/no-shared-state full runs match all phase-1 anchors.
- Corrupt one hash/package/version/tool identity at a time and prove failure before data generation.
- Verify no worktree requirement outside owned lock paths changes.

## Regression Gate

- Final lock fingerprint is exact at its repository path.
- Package graph and `pip freeze --all` semantic set match the selected decision.
- 1.12 comparator remains contextual migration evidence, not selected baseline.
- F-06, SC-04 and SC-06 are closed by retained evidence.

## Success criteria

- [ ] Complete wheel hashes and compiler identity are tracked.
- [ ] Two empty-cache full runs agree exactly.
- [ ] No resolver can select a newer version during golden execution.
- [ ] Rollback to the prior lock set is rehearsed from fresh state.
