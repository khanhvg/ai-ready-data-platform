# Isolated local lab runner

Issue #9 provides one owner-only host control plane and one fresh Linux/arm64
container per exact semantic operation. The accepted operation set is closed to
the eight zero-argument IDs in the released promotion-trust lab. Callers cannot
supply an executable, argv, environment, path, URL, SQL, image, package, plugin,
Docker option, or cloud option.

Build prerequisites are acquired once into the ignored
.artifacts/build/issue-9/wheelhouse role and verified against
requirements/wheelhouse-manifest-v1.json. Build the deterministic offline image:

    python3.12 apps/lab-runner/tools/build-runner-image.py --build

Run the full fixed gate and its bounded public verifiers:

    python3.12 apps/lab-runner/tools/run-gate.py
    make runner-test
    make runner-security-test
    make runner-race-test

Runtime state is owner-only under apps/lab-runner/.local-state. The launcher
uses only the effective-user-owned OrbStack Unix socket. Missing engine or any
unobservable containment field fails closed; there is no host semantic fallback.
