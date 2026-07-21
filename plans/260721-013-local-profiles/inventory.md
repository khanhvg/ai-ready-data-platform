---
title: "Issue #13 Repository and Compose Inventory"
status: planning-baseline
inputSha: "24be3b34c6b0fcdbd07c5800dcab349054e34713"
created: "2026-07-22"
---

# Issue #13 Repository and Compose Inventory

## Immutable Planning Context

| Item | Observed value |
|---|---|
| Worktree | Issue #13 dedicated worktree only |
| Branch | `plan/issue-13-local-profiles` |
| Local HEAD | `24be3b34c6b0fcdbd07c5800dcab349054e34713` |
| Live integration ref | `origin/integration/issue-5-local-learning` at the same SHA |
| Issue #13 | Open; `triaged`; `risk:high`, `tdd`, `security:S3`, `performance`, `compose` |
| Issue #10 dependency | Open; plan-review state only; no passing merged journey SHA |
| Issue #12 dependency | Open; plan-review state only; no released/admitted lab SHA |
| Issue #13 remote branch at inventory time | Absent |
| `docs/code-standards.md` | Absent and protected as an absence invariant |

Remote plan branches for Issues #10 and #12 are not dependency completion. They supply no merge,
release, image, lab, or admission authority. No other worktree was read or changed.

These rows are immutable planner-baseline observations at `24be3b3`, not claims about the later
validation checkout. Independent validation starts from planner output `a23a0b77ac06dd6635f3b6a250432783cb9e2e04`;
the now-existing Issue #13 plan branch is expected and grants no implementation authority.

## Authority Ledger at Planning Input

Every `EMPTY` value is a hard implementation stop, not a placeholder to fill by guesswork.

| Authority | Current value | Required before |
|---|---|---|
| Passing merged Issue #10 journey SHA | `EMPTY` | Stage A |
| Released Issue #12 lab/release SHA | `EMPTY` | Stage A |
| Admitted P7 lab manifest/allowlist SHA | `EMPTY` | Stage A |
| Portal image index/platform digest | `EMPTY` | Stage A Compose mapping |
| Runner image index/platform digest | `EMPTY` | Stage A Compose mapping |
| Released command authority for I5-08 | `EMPTY` | Stage A GREEN/evidence claim |
| Released completion/evidence authority | `EMPTY` | Stage A evidence emission |
| Owner-approved exact service allowlist SHA | `EMPTY` | Stage A |
| Stage A tested/output head | `EMPTY` | Stage B |
| Admitted engine identity/allocation | `EMPTY` | Stage B |
| Admitted image digest/SBOM/signature set | `EMPTY` | Stage B |
| Admitted measurement toolchain SHA | `EMPTY` | Stage B |

`learning/contracts/command-owner-registry-v1.json` reserves the four I5-08 names, but all four
rows are `availability: future-owner` with `failureRule: not-runnable`; this is naming metadata,
not executable command authority. `fitness-result-v1` is currently owner-fixed to `I5-01`, so
I5-08 must consume the later released owner-compatible completion/evidence contract. This issue
must not silently edit the protected shared registry/schema to work around the mismatch.

## Profile Namespace Inventory

The word `profile` currently has separate contracts. Admission must never confuse them.

| Namespace | Actual values | Meaning |
|---|---|---|
| Dataset scale | `small`, `medium`, `large`, `demo-large` | Generator row-count/scale choice |
| Docker-free runtime | `core` | Host Python, DuckDB, dbt, export; not a Compose profile |
| Compose heavy groups | `orchestration`, `lake`, `governance` | Opt-in container service groups |
| Future master-plan term | `learning` | Planned only; no current service/image contract |

Dataset contracts at input:

| Scale | Customers | Products | Stores | Suppliers | Web sessions | Orders | Approx. rows |
|---|---:|---:|---:|---:|---:|---:|---:|
| `small` | 200 | 150 | 20 | 10 | 200 | 1,000 | ~6,800 |
| `medium` | 2,000 | 500 | 50 | 25 | 3,000 | 15,000 | ~91,000 |
| `large` | 20,000 | 2,000 | 150 | 80 | 45,000 | 150,000 | ~945,000 |
| `demo-large` | 20,000 | 2,000 | 150 | 100 | 40,000 | 90,000 | ~620,000 |

`small`/`42` is also the current golden contract. Resource admission cannot rename, overload, or
alter dataset scale, row/anomaly, mart, lineage, Rill, Airflow, Iceberg, or catalog semantics.

## Docker-Free Core Commands

Static `make -n health dbt bi` inspection found no Docker, cloud, socket, sudo, or privileged
command in these recipes:

| Target | Shipped behavior |
|---|---|
| `make health` | Open `warehouse/retail.duckdb` read-only and require a nonempty `raw` schema |
| `make dbt` | Build the existing dbt project through the local venv |
| `make bi` | Export DuckDB marts to local Parquet; print optional host Rill instructions |

`dbt` and `bi` may create/install the existing local venv through their prerequisite. They still
must not require Docker. `health` assumes the prior documented seed/load/venv journey.

## Compose Profiles, Services, and Configured Memory

Observed with Docker Compose v5.1.2 static rendering only; no engine or container was started.

| Group | Actual services | Current memory sum | Current CPU sum | Current PID caps |
|---|---|---:|---|---|
| `orchestration` | `airflow` | 4 GiB | Missing | Missing |
| `lake` | `minio`, `minio-init`, `lakekeeper-db`, `lakekeeper-migrate`, `lakekeeper` | 3.25 GiB | Missing | Missing |
| `governance` | `openmetadata-db`, `openmetadata-search`, `openmetadata-server` | 4 GiB | Missing | Missing |
| Guarded current pair | `lake+governance` | 7.25 GiB | Missing | Missing |
| Denied all-three set | `orchestration+lake+governance` | 11.25 GiB | Missing | Missing |

## Service Inventory

`*` means the current published port defaults to every host interface. Tag strings are observed
configuration, not admitted immutable image authority.

| Service | Group | Image/build | Memory | Port(s) | Writable volume/mount | Health/dependency |
|---|---|---|---:|---|---|---|
| `airflow` | orchestration | local build, `retail-airflow:local` | 4 GiB | `*:8080` | repo root RW; `airflow-home` | HTTP health; none |
| `minio` | lake | `minio/minio:RELEASE.2025-09-07T16-13-09Z` | 1 GiB | `*:9000`, `*:9001` | `minio-data` | `mc ready`; none |
| `minio-init` | lake | `minio/minio:RELEASE.2025-09-07T16-13-09Z` | 256 MiB | none | none | one-shot; waits for healthy `minio` |
| `lakekeeper-db` | lake | `postgres:16-alpine` | 512 MiB | none | `lakekeeper-db-data` | `pg_isready`; none |
| `lakekeeper-migrate` | lake | `quay.io/lakekeeper/catalog:v0.13.1` | 512 MiB | none | none | one-shot; waits for healthy DB |
| `lakekeeper` | lake | `quay.io/lakekeeper/catalog:v0.13.1` | 1 GiB | `*:8181` | none | binary health; DB+migration closure |
| `openmetadata-db` | governance | `mysql:8.3` | 1 GiB | none | `openmetadata-db-data` | `mysqladmin ping`; none |
| `openmetadata-search` | governance | `docker.elastic.co/elasticsearch/elasticsearch:8.11.4` | 1 GiB | none | `openmetadata-es-data` | cluster HTTP health; none |
| `openmetadata-server` | governance | `docker.getcollate.io/openmetadata/server:1.6.5` | 2 GiB | `*:8585` | none | version endpoint; DB+search closure |

Named top-level volumes are `airflow-home`, `minio-data`, `lakekeeper-db-data`,
`openmetadata-db-data`, and `openmetadata-es-data`. Compose project scoping applies to named
volumes, but fixed current `container_name` values and fixed host ports create global collision
risk. The Airflow root bind is writable; DAG/callable binds are read-only. No Docker socket is
mounted.

## Health and Dependency Closure

Seven long-running services have healthchecks. `minio-init` and `lakekeeper-migrate` are bounded
one-shot dependencies but have no explicit completion timeout. Healthchecks contain interval,
timeout, and retries; some contain `start_period`. The admission contract must calculate a hard
service deadline and reject a missing/zero timeout for both long-running and one-shot services.

Current same-group closure:

- `lakekeeper` expands to `lakekeeper-db` and `lakekeeper-migrate`; migration expands to DB.
- `minio-init` expands to `minio`.
- `openmetadata-server` expands to DB and search.
- No cross-profile dependency appears in Compose. Host-side `catalog-ingest` deliberately starts
  `lake+governance`, stops orchestration first, and leaves governance running afterward.

Supported admission must resolve transitive closure, compare it to the exact group service set,
and reject any undeclared extra—even if Compose would otherwise activate it automatically.

## Existing Guard and Teardown Behavior

- `make up PROFILE=core` is Docker-free; other values pass directly to Compose.
- `make airflow` starts orchestration directly.
- `make lake-up` and `make catalog` inspect fixed container names to prevent their pair.
- `make catalog-ingest` is the only documented `lake+governance` exception; it stops Airflow,
  waits on two fixed names, and tears down lake only.
- `make down` invokes all three profiles; named volumes remain.
- `make clean` removes host-generated pipeline/venv files, not named Docker volumes.

These are characterization facts, not sufficient admission. Direct profile selection currently
has no canonical validation for empty, duplicate, unknown, all-three, over-budget, malicious env,
dependency expansion, port/volume ownership, or foreign teardown.

## Current Static Security and Resource Gaps

- No `cpus`, `pids_limit`, per-service log rotation, disk ceiling, or admission timeout contract.
- Published ports are not loopback-bound.
- No explicit capability drop, `no-new-privileges`, read-only root, privilege/socket rule, or
  explicit network exposure policy.
- Image tags have no recorded index/platform digest, SBOM, signature/provenance decision, or
  offline `--pull never` enforcement.
- Local-only default credentials occur in Compose; runtime evidence must never retain values.
- Fixed container names/ports can collide with another worktree or foreign Compose project.
- Existing `down` commands are not tied to an immutable run ownership manifest.

## Protected Planning Hashes

SHA-256 values at the immutable input:

| Path/set | SHA-256 |
|---|---|
| `README.md` | `c9c0e9fb8a85b9f63b47f3e0a1717715d2e74af54a5f6db3edcfde070783c171` |
| `Makefile` | `12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458` |
| `docker-compose.yml` | `21fd1a8ce32c1e7a4868062f6313531c7a4e979a80fc553e48f27b8a15daa2b9` |
| `.env.example` | `7d80465a90a3cb2a0ba965180078a98f190b0088ec53c63d5ccbb7f682499e1b` |
| Root `release-manifest.json` | `f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539` |
| Audited Phase 8 source | `fc2181b901b1cc25c338c30e3a578bd87fe75e5ce8cda63e93a0bc87a7636d21` |
| Implementation graph | `4d4d6807396889ac4337e9280a3d0819350af82b71905dc08e3d6fb1f6c52731` |
| Command owner registry | `a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80` |
| `fitness-result-v1` schema | `a104ad6330bcfc22bda0fb661fef96f067c09153da7dc2f306103e5f93a4ab6d` |
| Schema version registry | `8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e` |
| Curated release schema | `dcad3a4c04f44e207a26f985702db6926d4c85545d85ef5481faf036dded4e33` |
| All 307 tracked input files except the new Issue #13 plan directory | `bf5ac7969dc039d19051cff5c3d8bad84102887451eb9409082b8ecaa65ae5b4` |

The aggregate is the SHA-256 of newline-terminated, bytewise-sorted
`SHA-256<two spaces>repo-relative-path` lines for `git ls-tree -r --name-only` at the shipped
baseline. It reproduces from both baseline blobs and the unchanged validation checkout. It is a
planning scope guard, not a future implementation baseline: Phase 1 must recompute hashes at the
exact dependency-amended implementation input. During planning or validation, any diff outside
`plans/260721-013-local-profiles/**` is a hard failure.

## Future Writable Allowlist

Only after Stage A entry gates:

| Action | Exact path boundary |
|---|---|
| Modify | `docker-compose.yml` |
| Create | `config/profiles/local-profiles.yaml` |
| Create | `scripts/profiles/admit.py`, `scripts/profiles/measure.py`, `scripts/profiles/teardown.py` |
| Create | `tests/profiles/**`, `tests/compose/**` |
| Create | `mk/issue-5/i5-08.mk` |
| Modify if proven necessary | `.env.example`, `README.md`, `docs/demo-runbook.md` |

Root `Makefile` already includes `mk/issue-5/*.mk` and remains protected. Shared contracts,
command/evidence registries, architecture views, portal, runner, labs, migrations, golden code and
semantics, root release manifest, code standards, and unrelated Compose/docs remain read-only.
Any required path outside the table stops implementation and requires an exact owner-approved
allowlist/dependency amendment plus independent revalidation/readiness.
