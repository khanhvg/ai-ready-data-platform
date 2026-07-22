# Phase 4 — Implement and Prove the Container Runner Core

## Objective

Turn transport, registry, build, Engine admission, private PID namespace, resource and all-eight
operation RED families green without moving semantic work to the host.

## Ordered Steps

1. Implement strict released contract loading and the exact eight-command registry. Map each enum
   to one fixed in-image adapter; reject all unknown fields and caller-controlled execution data.
2. Implement owner-only UDS and bounded random-loopback fallback with exact Host, empty Origin,
   bearer, mutation CSRF, content-type, Fetch Metadata, framing and body-limit admission.
3. Implement the minimal local Unix Engine client. Ignore ambient Docker/proxy/registry state,
   validate socket type/owner and return RUNNER_ENGINE_UNAVAILABLE on stopped/missing engine.
4. Implement deterministic build context creation and the Dockerfile-specific ignore. Build from
   the measured base digest and offline hashed wheelhouse, with no build network after acquisition,
   and export local OCI metadata. Do not push.
5. Capture the actual linux/arm64 image manifest/config digest, Dockerfile/context hashes, SBOM,
   provenance, license and vulnerability evidence in container-build-lock-v1. Rebuild once and
   explain or stop on non-reproducible identity.
6. Implement the exact create specification: digest plus pull-never, UID:GID 65532:65532,
   read-only root, exact private workspace/tmp/run/shm roles, network none, no ports, private
   PID/IPC, init, cap-drop ALL,
   no-new-privileges, custom seccomp, no added host devices/device requests or privileged mode,
   pids 64, aggregate memory 536870912 bytes and zero swap,
   2 CPUs and closed environment.
7. Implement durable container identity before start and exact archive input copy. The repository,
   Docker socket, source, home, credentials and arbitrary host paths are never mounted.
8. Implement PID 1 init plus supervisor subreaper, fixed protocol, per-worker limits, output caps
   and 110-second execution plus TERM/KILL/wait/remove budget.
9. Implement real adapters for all eight operations from the baked released inputs. Use pinned
   dbtRunner and retain its multiprocessing tracker only inside the namespace/cgroup.
10. Implement hostile output archive validation before extraction: exact path/type/link/owner/
    mode/count/size/hash and declared asset closure.
11. Always converge the exact recorded container through stop, KILL when needed, wait and remove.
    Treat polling/inventory only as evidence.
12. Run effective-state and adversarial tests. Any ignored runtime flag, namespace/port/mount/
    process/container residue or 7/8 result stops the phase.

## All-Eight Feasibility Gate

Run each exact command against the actual locked image digest with profile small and seed 42. No
stub/fake/mocked operation is accepted. Compare outputs and golden behavior to the released expert
paths. retail.dbt-build evidence must show pinned dbtRunner origin, real model/test execution,
resource-tracker PID inside the private namespace, then zero survivors after removal.

## Security Acceptance

- Rapid double-fork/reparent/setsid/daemon and main-crash fixtures cannot survive removal.
- Fork bomb is bounded by effective pids limit; timeout follows TERM then KILL and completes by
  120 seconds.
- Network/DNS/listener/metadata probes fail and zero ports exist.
- Root/base is read-only; private tmpfs/input/output roles and archive checks hold under races.
- Canary/output/resource tests prove closed env and all kernel/resource bounds.
- Image has no Docker client/socket need, runtime installer or credentials.

## Exit Criteria

- Transport/registry/engine/container/operation RED families are green against the actual digest.
- Operation feasibility is measured 8/8.
- container-build-lock-v1 contains only observed values and complete supply-chain evidence.
- Durable CAS/release commit remains disabled until Phase 5.

## Rollback

Disable admission, converge only exact owner-recorded containers to removed, retain OCI/build/SBOM
evidence, and remove only marker-owned build/workspace staging. Do not prune Docker globally, remove
unowned images/containers or alter engine state without a separate gate.
