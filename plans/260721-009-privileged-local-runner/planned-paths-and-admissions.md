# Issue #9 Exact Planned Paths and Admission Gates

## Authority

This file expands every brace/glob shorthand used elsewhere in the plan. It is the exact future
tracked-path allow-list for Issue #9. A path not listed here requires a new independently validated
plan/readiness decision. This is planning only: none of the future-create paths exists at amendment
input `5cea5ce248b49ff8741af1b1e65f8ac2eb64698f`. The current validation/readiness audit authorizes
the whole ordered plan, subject to every phase-local RED, containment, evidence, and review gate.

## Exact Future Create Paths

### Package, policy, runtime and service

- `apps/lab-runner/pyproject.toml`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.in`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.lock`
- `apps/lab-runner/requirements/runner-py312-macos-arm64.metadata.json`
- `apps/lab-runner/config/runtime-policy-v1.toml`
- `apps/lab-runner/config/released-contract-lock.json`
- `apps/lab-runner/config/command-owner-activation-i5-04-v1.json`
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

## No Generated Binding Admission

Released Stage A contains no generated-binding command, output list, output hashes, or generator
path. Therefore no file below `apps/lab-runner/src/lab_runner/generated/` and no generated-type
test is authorized. The runner consumes the exact released schemas/readers directly. Any future
proposal to generate bindings requires a new exact released authority and fresh validation; a
wildcard directory never grants write authority.

The released generic activation seam is compatible. The only admitted I5-04 instance is
`apps/lab-runner/config/command-owner-activation-i5-04-v1.json`. Its base-registry hash is the
released pin; its fragment and instance hashes are computed from actual future bytes and locked
then. It is not copied to or registered in any shared-contract path.

## Exact Existing Conditional Modify Path

- `orchestration/airflow/callables/pipeline.py` — only the characterized pre-`_run` refusal for
  explicit runner-reserved learner paths. Default signatures, expert paths, command lists, env
  behavior, DAG import/order and every other callable remain unchanged. If Phase 1 proves the
  refusal is unnecessary, this file remains byte-identical.

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

The following read-only inputs exist in exact Stage A Git tree
`fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9`; the future implementation head must contain those
exact bytes by ancestry before any Issue #9 write:

- `versions.md`
- `learning/contracts/learning-contract-set-v1.json`
- `learning/contracts/learning-contract-set-v1.schema.json`
- `learning/contracts/learning-contract-version-registry-v1.json`
- `learning/contracts/learning-contract-version-registry-v1.schema.json`
- `learning/contracts/canonicalization-v1.json`
- `learning/contracts/make-input-contract-v1.json`
- `learning/contracts/command-owner-activation-v1.schema.json`
- `learning/contracts/command-owner-activation-i5-03-v1.json`
- `learning/contracts/operation-matrix-v1.json`
- `learning/contracts/operation-matrix-v1.schema.json`
- `learning/contracts/completion-reconciliation-v1.json`
- `learning/contracts/completion-reconciliation-v1.schema.json`
- `learning/contracts/fitness-result-v2.schema.json`
- `learning/contracts/learning-evidence-v1.schema.json`
- `learning/contracts/lab-v1.schema.json`
- `learning/contracts/lesson-v1.schema.json`
- `learning/contracts/progress-v1.schema.json`
- `learning/contracts/promotion-trust-learning-manifest-v1.schema.json`
- `learning/labs/promotion-trust/lab-v1.json`
- `learning/lessons/promotion-trust/lesson-v1.json`
- `learning/manifests/promotion-trust-v1.json`
- `contracts/openapi/learning-platform-v1.yaml`
- `contracts/openapi/learning-platform-openapi-profile-v1.schema.json`
- `contracts/openapi/learning-platform-problem-details-v1.schema.json`
- `scripts/learning_contracts/schema.py`
- `scripts/learning_contracts/registry.py`
- `scripts/learning_contracts/openapi.py`
- `scripts/learning_contracts/state.py`
- `scripts/learning_contracts/completion.py`
- `scripts/learning_contracts/check.py`
- `scripts/learning_contracts/fitness.py`
- `scripts/learning_contracts/evidence.py`
- `scripts/learning_contracts/canonical.py`
- `mk/issue-5/i5-03.mk`

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

Released admission at Stage A SHA:

| Command | Current proof | Future admission |
|---|---|---|
| `make runner-test` | Recipe absent; exact base row is I5-04 `future-owner`, `runner-test`, S3 | Exact I5-04 fragment plus the admitted activation instance selecting `fitness-result-v2` |
| `make runner-security-test` | Recipe absent; exact base row is I5-04 `future-owner`, `runner-security`, S3 | Same activation gate; includes every stable RED family and S3 matrix row |
| `make runner-race-test` | Recipe absent; exact base row is I5-04 `future-owner`, `runner-race`, S3 | Same activation gate; deterministic barriers, no timing-only correctness |
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

None for readiness. The activation path is exact, the private request ceiling is 16,384 bytes,
and generated output is denied. Actual future file/head hashes are measured after the bytes exist;
they are not placeholders or authority to predict a SHA.
