# Issue #9 Exact Planned Paths and Admission Gates

## Authority

This is the exhaustive tracked write allow-list for Issue #9 cook. All future-create paths are
absent at amendment head 4774c711208ef9cb7050b72c88106dffc7016f04. A path not listed requires a
new reviewed plan amendment. There is no conditional write outside this list.

## Exact Future Create Paths

### Package, launcher and state

- apps/lab-runner/.gitignore
- apps/lab-runner/pyproject.toml
- apps/lab-runner/requirements/runner-py312-linux-arm64.in
- apps/lab-runner/requirements/runner-py312-linux-arm64.lock
- apps/lab-runner/requirements/runner-py312-linux-arm64.metadata.json
- apps/lab-runner/requirements/wheelhouse-manifest-v1.json
- apps/lab-runner/config/runtime-policy-v2.toml
- apps/lab-runner/config/released-contract-lock.json
- apps/lab-runner/config/command-owner-activation-i5-04-v1.json
- apps/lab-runner/config/container-build-lock-v1.json
- apps/lab-runner/config/runner-image-release-v1.json
- apps/lab-runner/src/lab_runner/__init__.py
- apps/lab-runner/src/lab_runner/__main__.py
- apps/lab-runner/src/lab_runner/contract.py
- apps/lab-runner/src/lab_runner/registry.py
- apps/lab-runner/src/lab_runner/transport.py
- apps/lab-runner/src/lab_runner/engine.py
- apps/lab-runner/src/lab_runner/container_backend.py
- apps/lab-runner/src/lab_runner/container_protocol.py
- apps/lab-runner/src/lab_runner/container_supervisor.py
- apps/lab-runner/src/lab_runner/operation_adapters.py
- apps/lab-runner/src/lab_runner/archive.py
- apps/lab-runner/src/lab_runner/workspace.py
- apps/lab-runner/src/lab_runner/fence.py
- apps/lab-runner/src/lab_runner/state.py
- apps/lab-runner/src/lab_runner/audit.py
- apps/lab-runner/src/lab_runner/release.py
- apps/lab-runner/src/lab_runner/evidence.py
- apps/lab-runner/src/lab_runner/service.py
- apps/lab-runner/tools/build-runner-image.py
- apps/lab-runner/tools/run-gate.py
- apps/lab-runner/README.md
- mk/issue-5/i5-04.mk

### Exact container build and policy files

- apps/lab-runner/container/runner.Dockerfile
- apps/lab-runner/container/runner.Dockerfile.dockerignore
- apps/lab-runner/container/context-manifest-v1.json
- apps/lab-runner/container/seccomp-runner-v1.json
- apps/lab-runner/container/licenses-policy-v1.json

The Dockerfile path is apps/lab-runner/container/runner.Dockerfile. Its deterministic build-context
archive path is runtime-only .artifacts/build/issue-9/runner-context.tar, produced solely by
apps/lab-runner/tools/build-runner-image.py from context-manifest-v1.json. The adjacent
runner.Dockerfile.dockerignore denies every incidental directory entry. Docker may receive only
the normalized archive; the repository root is never a build context.

### Characterization and adversarial fixtures

- apps/lab-runner/tests/characterization/test_released_entrypoints.py
- apps/lab-runner/tests/characterization/test_expert_namespace.py
- apps/lab-runner/tests/fixtures/argv_probe.py
- apps/lab-runner/tests/fixtures/import_probe.py
- apps/lab-runner/tests/fixtures/process_tree_probe.py
- apps/lab-runner/tests/fixtures/rapid_double_fork.py
- apps/lab-runner/tests/fixtures/reparent_setsess_daemon.py
- apps/lab-runner/tests/fixtures/fork_bomb.py
- apps/lab-runner/tests/fixtures/main_crash.py
- apps/lab-runner/tests/fixtures/network_probe.py
- apps/lab-runner/tests/fixtures/resource_probe.py
- apps/lab-runner/tests/fixtures/output_flood.py
- apps/lab-runner/tests/fixtures/archive_attacks.py
- apps/lab-runner/tests/fixtures/browser-requests.json
- apps/lab-runner/tests/fixtures/fault-points.json
- apps/lab-runner/tests/fixtures/fixture-manifest.json
- apps/lab-runner/tests/red-manifest.json

### Unit, security, race and integration tests

- apps/lab-runner/tests/unit/test_released_contract_lock.py
- apps/lab-runner/tests/unit/test_transport_policy.py
- apps/lab-runner/tests/unit/test_runtime_policy.py
- apps/lab-runner/tests/unit/test_engine_admission.py
- apps/lab-runner/tests/unit/test_container_spec.py
- apps/lab-runner/tests/unit/test_container_protocol.py
- apps/lab-runner/tests/unit/test_archive_admission.py
- apps/lab-runner/tests/unit/test_workspace_policy.py
- apps/lab-runner/tests/unit/test_fence.py
- apps/lab-runner/tests/unit/test_state.py
- apps/lab-runner/tests/unit/test_idempotency.py
- apps/lab-runner/tests/unit/test_audit.py
- apps/lab-runner/tests/unit/test_release.py
- apps/lab-runner/tests/unit/test_evidence.py
- apps/lab-runner/tests/security/test_transport_boundary.py
- apps/lab-runner/tests/security/test_registry_and_environment.py
- apps/lab-runner/tests/security/test_container_effective_policy.py
- apps/lab-runner/tests/security/test_pid_namespace_lifecycle.py
- apps/lab-runner/tests/security/test_network_and_metadata_denial.py
- apps/lab-runner/tests/security/test_resource_limits.py
- apps/lab-runner/tests/security/test_archive_and_filesystem.py
- apps/lab-runner/tests/security/test_output_and_canary.py
- apps/lab-runner/tests/race/test_fencing.py
- apps/lab-runner/tests/race/test_container_reconciliation.py
- apps/lab-runner/tests/race/test_release_atomicity.py
- apps/lab-runner/tests/race/test_crash_recovery.py
- apps/lab-runner/tests/race/test_idempotency.py
- apps/lab-runner/tests/integration/test_all_eight_operations.py
- apps/lab-runner/tests/integration/test_dbt_resource_tracker.py
- apps/lab-runner/tests/integration/test_evidence_manifest.py
- apps/lab-runner/tests/integration/test_rollback.py
- apps/lab-runner/tests/integration/test_full_runner_flow.py

## Existing Modify Paths

None. Both admitted top-level scopes are absent at the amendment head and are created by cook. In
particular, no Airflow guard or profile integration is authorized.

## Exact Existing Read-Only Inputs

The deterministic context builder may copy only the files explicitly locked in
context-manifest-v1.json from these read-only families. Phase 2 expands the family to exact path and
SHA-256 rows before the build gate:

- data-generator/generate.py
- ingestion/load_raw.py
- transform/dbt/dbt_project.yml
- transform/dbt/profiles.yml
- transform/dbt/models/**
- transform/dbt/tests/**
- transform/dbt/macros/**
- serving/export_marts_snapshot.py
- lake/curated_assets.json
- contracts/data/retail-golden-v1.json
- contracts/data/curated-release-manifest.schema.json
- tests/fixtures/data/**
- scripts/golden/workspace.py
- scripts/golden/process.py
- scripts/golden/release_contract.py
- scripts/learning_contracts/**
- learning/contracts/**
- learning/labs/promotion-trust/lab-v1.json
- learning/lessons/promotion-trust/lesson-v1.json
- learning/manifests/promotion-trust-v1.json
- contracts/openapi/learning-platform-v1.yaml
- contracts/openapi/learning-platform-openapi-profile-v1.schema.json
- contracts/openapi/learning-platform-problem-details-v1.schema.json
- versions.md
- mk/issue-5/i5-01.mk
- mk/issue-5/i5-03.mk

All copied bytes must be present at and hash-equal to released Stage A
fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9. No wildcard itself grants build-context admission: the
generated manifest contains every individual path, mode, size and SHA-256 and rejects additions.

These existing paths are protected and may never be modified by Issue #9:

- root Makefile and docker-compose.yml
- every Compose/profile file
- orchestration/airflow/**
- learning/** and contracts/**
- scripts/golden/** and scripts/learning_contracts/**
- data-generator/**, ingestion/**, transform/**, serving/** and lake/**
- portals, cloud, Terraform and Kubernetes paths
- every mk/issue-5 fragment except new i5-04.mk
- every plan outside plans/260721-009-privileged-local-runner/**

Issue #13 may later modify its separately approved profile/Compose paths, but it may not create,
duplicate or modify apps/lab-runner/** or mk/issue-5/i5-04.mk.

## No Generated Binding Admission

Released Stage A has no generated-binding output authority. No generated package directory is
authorized. The runner consumes the exact released schema readers directly. Any proposed generated
binding needs a new exact output list and reviewed amendment.

## Exact Verification Sequence

Run the fixed complete shard harness from the repository root on the exact implementation tree:

    python3.12 apps/lab-runner/tools/run-gate.py

Then run all four public verifiers:

    make runner-test
    make runner-security-test
    make runner-race-test
    make data-contracts-check

i5-04.mk defines only runner-test, runner-security-test and runner-race-test. They verify the fresh
shard artifacts and emit fitness-result-v2 within 120000 ms. The existing root Make include
mechanism and I5-01 fitness-result-v1 data-contracts-check remain byte-identical.

## Engine and Tool Admission

| Capability | Amendment observation | Cook rule |
|---|---|---|
| Host | Darwin arm64, 16 GiB, 8 logical CPUs | Record drift; retain one-container/reserve policy |
| Docker client | 29.4.0 arm64, API 1.54 | Pin observed identity; never accept a remote endpoint |
| OrbStack | 2.2.1 installed, orbstack context selected | Separate side-effect gate may start app; admin/TCC stops |
| Engine | Stopped, user socket absent | RUNNER_ENGINE_UNAVAILABLE; no host fallback |
| Platform | linux/arm64 required | Reject emulation or wrong manifest platform |
| cgroup/seccomp/init | Not observable while stopped | Must be proven effective after gated engine start and before image tests |
| Security scanners | Not trusted from global environment | Fully pinned in the app lock or separately recorded tool lock |

## Runtime-Only Paths

Runtime may create only these marker-owned local roles:

- .artifacts/build/issue-9/** for the deterministic context, OCI output, SBOM, provenance and scans;
- apps/lab-runner/.local-state/workspaces/** for durable private workspace/CAS/audit state;
- apps/lab-runner/.local-state/evidence/** for bounded evidence.

The Issue #9-owned apps/lab-runner/.gitignore contains exactly `/.local-state/`. It does not ignore
source, tests, locks, build inputs or any root path. Cook proves both fixed state roles resolve to
that rule with `git check-ignore -v`, proves a neighboring unlisted file is visible to Git, and
proves the final default status has no ordinary untracked runtime artifact. The ignored-inclusive
status is compared to the Phase 1 exact baseline: its only new entries are the expected
marker-owned runtime roles, and every unrelated pre-existing ignored entry is unchanged. Root
.gitignore remains unchanged. The deterministic context allow-list rejects .local-state even
though Git ignores it.

Public requests cannot select any runtime path. Cleanup uses exact marker, nonce, device and inode
checks and never recursive broad targets. A broad removal of apps/lab-runner or .local-state is
forbidden.

## Open Questions

None. Actual base, image, implementation and release digests are deliberately cook-time measured
values. Engine absence is a fail-closed prerequisite with an explicit local-side-effect gate, not a
choice between backends.
