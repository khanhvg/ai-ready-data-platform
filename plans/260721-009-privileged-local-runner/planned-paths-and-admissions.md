# Issue #9 Exact Planned Paths and Admission Gates

## Authority

This file expands every brace/glob shorthand used elsewhere in the plan. It is the exact future
tracked-path allow-list for Issue #9. A path not listed here requires a new independently validated
plan/readiness decision. This is planning only: none of the future-create paths exists at validation
input `de66ad3da6a4f6ed49059e547689462f8269bca5`, and none may be created before the exact released
Issue #8 Stage A SHA and fresh readiness authority exist.

## Exact Future Create Paths

### Package, policy, runtime and service

- `apps/lab-runner/pyproject.toml`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.in`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.lock`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.metadata.json`
- `apps/lab-runner/config/runtime-policy-v1.toml`
- `apps/lab-runner/config/released-contract-lock.json`
- `apps/lab-runner/src/lab_runner/__init__.py`
- `apps/lab-runner/src/lab_runner/__main__.py`
- `apps/lab-runner/src/lab_runner/contract.py`
- `apps/lab-runner/src/lab_runner/registry.py`
- `apps/lab-runner/src/lab_runner/transport.py`
- `apps/lab-runner/src/lab_runner/containment.py`
- `apps/lab-runner/src/lab_runner/launcher.py`
- `apps/lab-runner/src/lab_runner/workspace.py`
- `apps/lab-runner/src/lab_runner/fence.py`
- `apps/lab-runner/src/lab_runner/process.py`
- `apps/lab-runner/src/lab_runner/state.py`
- `apps/lab-runner/src/lab_runner/release.py`
- `apps/lab-runner/src/lab_runner/evidence.py`
- `apps/lab-runner/src/lab_runner/service.py`
- `apps/lab-runner/tools/run-gate.py`
- `apps/lab-runner/README.md`
- `mk/issue-5/i5-04.mk`

### Characterization and bounded fixtures

- `apps/lab-runner/tests/characterization/test_current_entrypoints.py`
- `apps/lab-runner/tests/characterization/test_expert_namespace.py`
- `apps/lab-runner/tests/fixtures/argv_probe.py`
- `apps/lab-runner/tests/fixtures/import_probe.py`
- `apps/lab-runner/tests/fixtures/startup_probe.py`
- `apps/lab-runner/tests/fixtures/process_tree_probe.py`
- `apps/lab-runner/tests/fixtures/path_race_probe.py`
- `apps/lab-runner/tests/fixtures/network_probe.py`
- `apps/lab-runner/tests/fixtures/resource_probe.py`
- `apps/lab-runner/tests/fixtures/output_probe.py`
- `apps/lab-runner/tests/fixtures/browser-requests.json`
- `apps/lab-runner/tests/fixtures/fault-points.json`
- `apps/lab-runner/tests/fixtures/fixture-manifest.json`
- `apps/lab-runner/tests/red-manifest.json`

### Unit, security, race and integration tests

- `apps/lab-runner/tests/unit/test_released_contract_lock.py`
- `apps/lab-runner/tests/unit/test_generated_types.py`
- `apps/lab-runner/tests/unit/test_transport_policy.py`
- `apps/lab-runner/tests/unit/test_runtime_policy.py`
- `apps/lab-runner/tests/unit/test_workspace_policy.py`
- `apps/lab-runner/tests/unit/test_state_machine.py`
- `apps/lab-runner/tests/unit/test_release_policy.py`
- `apps/lab-runner/tests/unit/test_evidence_policy.py`
- `apps/lab-runner/tests/unit/test_fence.py`
- `apps/lab-runner/tests/unit/test_state.py`
- `apps/lab-runner/tests/unit/test_idempotency.py`
- `apps/lab-runner/tests/unit/test_audit.py`
- `apps/lab-runner/tests/unit/test_release.py`
- `apps/lab-runner/tests/security/test_interpreter_import.py`
- `apps/lab-runner/tests/security/test_argv_registry.py`
- `apps/lab-runner/tests/security/test_path_toctou.py`
- `apps/lab-runner/tests/security/test_environment_network.py`
- `apps/lab-runner/tests/security/test_quotas_output_descendants.py`
- `apps/lab-runner/tests/security/test_base_immutability.py`
- `apps/lab-runner/tests/security/test_browser_transport.py`
- `apps/lab-runner/tests/race/test_fencing.py`
- `apps/lab-runner/tests/race/test_cross_entrypoint.py`
- `apps/lab-runner/tests/race/test_release_atomicity.py`
- `apps/lab-runner/tests/race/test_crash_recovery.py`
- `apps/lab-runner/tests/race/test_idempotency.py`
- `apps/lab-runner/tests/integration/test_bounded_pipeline.py`
- `apps/lab-runner/tests/integration/test_evidence_manifest.py`
- `apps/lab-runner/tests/integration/test_rollback.py`
- `apps/lab-runner/tests/integration/test_full_runner_flow.py`

## Conditional Generated Binding Admission

No generated binding path is pre-authorized by a guessed contract. If and only if the released
Issue #8 Stage A handoff mandates generation, Phase 2 must record the exact generator command,
input schemas/hashes, output file list and output hashes in `released-contract-lock.json` before
any file is created below `apps/lab-runner/src/lab_runner/generated/`. A wildcard directory is not
write authority. Any output not named by that released deterministic procedure is refused and
requires revalidation.

## Exact Existing Modify Path

- `orchestration/airflow/callables/pipeline.py` — only the characterized pre-`_run` refusal for
  explicit runner-reserved learner paths. Default signatures, expert paths, command lists, env
  behavior, DAG import/order and every other callable remain unchanged.

No other tracked existing path may be modified.

## Exact Existing Read-Only Inputs

- `data-generator/generate.py`
- `ingestion/load_raw.py`
- `orchestration/airflow/callables/pipeline.py` before the admitted guard change
- `transform/dbt/dbt_project.yml`
- `transform/dbt/profiles.yml`
- `serving/export_marts_snapshot.py`
- `lake/curated_assets.json`
- `contracts/data/curated-release-manifest.schema.json`
- `scripts/golden/workspace.py`
- `scripts/golden/process.py`
- `scripts/golden/release_contract.py`
- `mk/issue-5/i5-01.mk`
- `learning/contracts/command-owner-registry-v1.json`
- `learning/contracts/schema-version-registry.json`
- `learning/contracts/fitness-result-v1.schema.json`
- Exact additional Issue #8 contract paths only after its owner-published released Stage A handoff
  binds their paths, versions and hashes.

Shared-contract inputs remain read-only. In particular, no Issue #9 change may write
`learning/contracts/`, `contracts/`, `scripts/golden/`, another `mk/issue-5/` fragment, root
`Makefile`, another issue plan, portal/framework paths, Docker/Compose, Terraform or cloud paths.

## Exact Future Verification Commands

Run from the repository root at the exact implementation tested tree:

```bash
make runner-test
make runner-security-test
make runner-race-test
make data-contracts-check
```

Current admission at validation input:

| Command | Current proof | Future admission |
|---|---|---|
| `make runner-test` | Intentionally absent; registry row is I5-04 `future-owner` | Issue #8 released registry activation plus exact `mk/issue-5/i5-04.mk` recipe |
| `make runner-security-test` | Intentionally absent; registry row is I5-04 `future-owner` | Same release gate; includes every stable RED family and S3 matrix row |
| `make runner-race-test` | Intentionally absent; registry row is I5-04 `future-owner` | Same release gate; deterministic barriers, no timing-only correctness |
| `make data-contracts-check` | Exists in `mk/issue-5/i5-01.mk` and is included by root `Makefile` | Remains read-only and unchanged |

## Host and Tool Admission

| Capability | Validation observation | Future cook rule |
|---|---|---|
| Host | macOS `26.5.1` build `25F80`, Darwin arm64, `17179869184` bytes physical memory | Exact match required; any drift disables readiness pending re-attestation |
| Python | `python3.12` is `3.12.3`; isolated mode, `LOCAL_PEERCRED`, `O_NOFOLLOW`, `O_DIRECTORY`, `RLIMIT_AS`, `RLIMIT_RSS` are exposed | Pin absolute runtime identity/hash and prove real entrypoint imports under `-I` |
| Seatbelt | `/usr/bin/sandbox-exec` exists | Existence is insufficient; functional network/base-write/workspace/import/cleanup probe must pass |
| Descendant control | Process group, PID/start identity and polling primitives exist; complete rapid reparent/`setsid` proof is not yet admitted | Phase 1 must prove a non-poll-only Darwin mechanism or STOP before RED/product cook |
| Bandit | Not present in the validation shell | Must be pinned and hash-complete in the app lock; missing is gate failure |
| pip-audit | Not present in the validation shell | Must be pinned and hash-complete in the app lock; missing is gate failure |
| pytest | Present in the validation shell | Global presence grants no authority; future gates use only the pinned app lock |

## Runtime-Only Paths

Runtime state may exist only under `.artifacts/workspaces/runner/`; evidence may exist only under
`.artifacts/evidence/runner/`. Public inputs never select a raw root or path. Ownership markers,
descriptor identities, private modes, live fence epochs and the rollback rules in
`verification-evidence-and-rollback.md` govern every create/remove/quarantine operation.

## Unresolved Questions

None for plan validation. The exact Issue #8 released Stage A SHA, released contract path set and
conditional generated binding list remain explicit external readiness blockers, not placeholders
that Issue #9 may fill.
