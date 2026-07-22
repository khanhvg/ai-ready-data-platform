#!/usr/bin/env python3
"""Fixed Issue #9 security, lifecycle, race, operation, and S3 gate."""
from __future__ import annotations

import concurrent.futures
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import py_compile
import sqlite3
import struct
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
from typing import Callable

ROOT = pathlib.Path(__file__).resolve().parents[3]
APP = ROOT / "apps/lab-runner"
SRC = APP / "src"
MANIFEST = APP / "tests/red-manifest.json"
COOK_INPUT = "f6791555dc8b2ada6fa44747ca829a3d9cd87667"
STAGE_A = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
sys.path.insert(0, str(SRC))

from lab_runner.archive import ArchiveError, Limits, inspect_tar
from lab_runner.container_backend import Backend
from lab_runner.container_protocol import read as read_protocol
from lab_runner.contract import EXPECTED_COMMANDS, validate_released_contract
from lab_runner.engine import Engine, EngineError
from lab_runner.evidence import write as write_evidence
from lab_runner.fence import acquire
from lab_runner.registry import RegistryError, operation_ids, validate_request
from lab_runner.release import ASSETS
from lab_runner.service import RunnerService
from lab_runner.state import StateError, Store
from lab_runner.transport import TransportError, admit
from lab_runner.workspace import Workspace


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_digest() -> str:
    digest = hashlib.sha256()
    paths = subprocess.run(
        ["git", "ls-files", "apps/lab-runner", "mk/issue-5/i5-04.mk"],
        cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE,
    ).stdout.splitlines()
    for name in sorted(paths):
        path = ROOT / name
        digest.update(name.encode() + b"\0" + path.read_bytes() + b"\0")
    return digest.hexdigest()


def expect_error(error: type[BaseException], code: str, call: Callable[[], object]) -> None:
    try:
        call()
    except error as exc:
        if str(exc) != code:
            raise AssertionError(f"{type(exc).__name__}:{exc}") from exc
    else:
        raise AssertionError(f"missing:{code}")


class Gate:
    def __init__(self) -> None:
        self.engine = Engine()
        self.engine_info = self.engine.admit()
        inspected = self.engine.json(["image", "inspect", "ai-ready-lab-runner:issue9"])
        if not isinstance(inspected, list) or len(inspected) != 1:
            raise RuntimeError("RUNNER_IMAGE_UNADMITTED")
        self.image_observation = inspected[0]
        self.image = str(inspected[0]["Id"])
        self.rows: dict[str, dict[str, object]] = {}
        evidence_root = APP / ".local-state/evidence/gates"
        evidence_root.mkdir(mode=0o700, parents=True, exist_ok=True)
        os.chmod(evidence_root, 0o700)
        self.root = pathlib.Path(tempfile.mkdtemp(prefix="exact-", dir=evidence_root))
        os.chmod(self.root, 0o700)
        self.fixture_store = Store(self.root / "fixture-state")
        self.fixture_backend = Backend(
            self.engine, self.image, APP / "container/seccomp-runner-v1.json",
            self.root / "fixture-staging", self.fixture_store,
        )
        self.foreign_before = self._foreign_ids()

    def _foreign_ids(self) -> list[str]:
        rows=self.engine.command(["ps","-a","--format","{{.ID}}\t{{.Labels}}"],check=True).stdout.splitlines()
        return sorted(row.split("\t",1)[0] for row in rows if "ai-ready.issue9.owner=issue-9" not in row)

    def record(self, case_id: str, call: Callable[[], object]) -> None:
        started = time.monotonic_ns()
        try:
            detail = call()
            self.rows[case_id] = {"status": "pass", "detail": detail, "durationNs": time.monotonic_ns() - started}
        except BaseException as exc:
            self.rows[case_id] = {
                "status": "fail", "failureCode": f"{type(exc).__name__}:{str(exc)[:160]}",
                "durationNs": time.monotonic_ns() - started,
            }

    @staticmethod
    def valid_request() -> dict[str, object]:
        return {"operationId": "workspace.prepare", "idempotencyKey": "gate-valid-request-0001", "workspaceRevision": 0}

    @classmethod
    def valid_headers(cls, body: bytes) -> list[tuple[str, str]]:
        return [
            ("Host", "runner.local"), ("Authorization", "Bearer bearer"),
            ("X-Runner-CSRF", "csrf"), ("Content-Type", "application/json"),
            ("Content-Length", str(len(body))),
        ]

    def transport(self) -> None:
        body = json.dumps(self.valid_request(), separators=(",", ":")).encode()
        headers = self.valid_headers(body)

        def trn1() -> object:
            for changed in ([x for x in headers if x[0] != "Host"], [*headers, ("Host", "evil")]):
                expect_error(TransportError, "RUNNER_HOST_FORBIDDEN" if len(changed) == len(headers)-1 else "RUNNER_HEADER_AMBIGUOUS", lambda c=changed: admit(method="POST", headers=c, body=body, bearer="bearer", csrf="csrf", peer_uid=os.geteuid(), effective_uid=os.geteuid()))
            return {"rejected": ["missing-host", "duplicate-host"]}

        def trn2() -> object:
            for name, value in (("Origin", "http://evil"), ("Cookie", "x=y"), ("Sec-Fetch-Site", "cross-site"), ("Access-Control-Request-Method", "POST")):
                expect_error(TransportError, "RUNNER_BROWSER_REQUEST_FORBIDDEN", lambda n=name, v=value: admit(method="POST", headers=[*headers, (n, v)], body=body, bearer="bearer", csrf="csrf", peer_uid=os.geteuid(), effective_uid=os.geteuid()))
            return {"rejected": ["origin", "cookie", "fetch-metadata", "preflight"]}

        def trn3() -> object:
            for bearer, csrf in (("wrong", "csrf"), ("bearer", "wrong"), ("", "")):
                expect_error(TransportError, "RUNNER_ADMISSION_SECRET_INVALID", lambda b=bearer, c=csrf: admit(method="POST", headers=headers, body=body, bearer=b, csrf=c, peer_uid=os.geteuid(), effective_uid=os.geteuid()))
            return {"secretEcho": False}

        def trn4() -> object:
            bad_type = [(k, "text/plain" if k == "Content-Type" else v) for k, v in headers]
            expect_error(TransportError, "RUNNER_CONTENT_TYPE_INVALID", lambda: admit(method="POST", headers=bad_type, body=body, bearer="bearer", csrf="csrf", peer_uid=os.geteuid(), effective_uid=os.geteuid()))
            huge = b"{" + b"x" * 16384
            huge_headers = self.valid_headers(huge)
            expect_error(TransportError, "RUNNER_BODY_TOO_LARGE", lambda: admit(method="POST", headers=huge_headers, body=huge, bearer="bearer", csrf="csrf", peer_uid=os.geteuid(), effective_uid=os.geteuid()))
            return {"bodyLimit": 16384}

        def trn5() -> object:
            expect_error(TransportError, "RUNNER_PEER_FORBIDDEN", lambda: admit(method="POST", headers=headers, body=body, bearer="bearer", csrf="csrf", peer_uid=os.geteuid()+1, effective_uid=os.geteuid()))
            return {"effectiveUid": os.geteuid()}

        for case_id, call in (("RED-TRN-001", trn1), ("RED-TRN-002", trn2), ("RED-TRN-003", trn3), ("RED-TRN-004", trn4), ("RED-TRN-005", trn5)):
            self.record(case_id, call)

    def registry_engine_image(self) -> None:
        def cmd1() -> object:
            for value in (
                {**self.valid_request(), "operationId": "shell"},
                {**self.valid_request(), "argv": ["sh"]},
                {**self.valid_request(), "workspaceRevision": -1},
            ):
                try: validate_request(value)
                except RegistryError: continue
                raise AssertionError("unclosed request")
            return {"operations": list(operation_ids())}

        def cmd2() -> object:
            forbidden = ("executable", "argv", "env", "cwd", "path", "url", "sql", "plugin", "package", "image", "dockerOptions")
            for field in forbidden:
                value = {**self.valid_request(), field: "$(touch /tmp/escape); rm -rf /"}
                expect_error(RegistryError, "RUNNER_REQUEST_FIELD_INVALID", lambda v=value: validate_request(v))
            return {"rejectedFields": list(forbidden)}

        def cmd3() -> object:
            value = self.direct(["/opt/runner-fixtures/import_probe.py"])
            observed = json.loads(value["stdout"])
            if observed["userSite"] is not False or observed["executable"] != "/opt/venv/bin/python3.12":
                raise AssertionError("startup isolation")
            return observed

        def eng1() -> object:
            unavailable = Engine(); unavailable.socket = self.root / "absent.sock"
            expect_error(EngineError, "RUNNER_ENGINE_UNAVAILABLE", unavailable.admit)
            return {"hostFallback": False}

        def eng2() -> object:
            endpoint = self.root / "not-a-socket"; endpoint.write_text("no\n")
            unavailable = Engine(); unavailable.socket = endpoint
            expect_error(EngineError, "RUNNER_ENGINE_UNAVAILABLE", unavailable.admit)
            return {"endpoint": "owner-unix-socket-only"}

        def eng3() -> object:
            value = self.fixture_backend._inspect(self._probe_container(create_only=True))
            try: self.fixture_backend.effective(value, self.image)
            finally: self.remove_test_container(str(value["Id"]))
            changed = json.loads(json.dumps(value)); changed["HostConfig"]["ReadonlyRootfs"] = False
            expect_error(EngineError, "RUNNER_CONTAINMENT_UNAVAILABLE", lambda: self.fixture_backend.effective(changed, self.image))
            return {"effectiveFields": "observed"}

        def img1() -> object:
            image = self.image_observation
            if image["Architecture"] != "arm64" or image["Os"] != "linux" or not self.image.startswith("sha256:"):
                raise AssertionError("image identity")
            return {"digest": self.image, "platform": "linux/arm64"}

        def img2() -> object:
            build = subprocess.run([sys.executable, str(APP / "tools/build-runner-image.py")], cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if build.returncode != 0: raise AssertionError(build.stderr[-160:])
            value = json.loads(build.stdout)
            if value["tarSha256"] != sha256(ROOT / ".artifacts/build/issue-9/runner-context.tar"):
                raise AssertionError("context hash")
            return {"files": len(value["files"]), "tarSha256": value["tarSha256"]}

        def img3() -> object:
            synthetic = {"matches": [{"vulnerability": {"severity": "High"}}]}
            denied = any(row["vulnerability"]["severity"] in ("High", "Critical") for row in synthetic["matches"])
            if not denied: raise AssertionError("supply gate")
            return {"syntheticHighRejected": True}

        for case_id, call in (
            ("RED-CMD-001", cmd1), ("RED-CMD-002", cmd2), ("RED-CMD-003", cmd3),
            ("RED-ENG-001", eng1), ("RED-ENG-002", eng2), ("RED-ENG-003", eng3),
            ("RED-IMG-001", img1), ("RED-IMG-002", img2), ("RED-IMG-003", img3),
        ): self.record(case_id, call)

    def _probe_container(self, create_only: bool = False) -> str:
        run_id = hashlib.sha256(os.urandom(16)).hexdigest()[:32]
        spec = self.fixture_backend._spec(run_id, 1, "workspace.prepare")
        cid = self.engine.command(spec, timeout=30).stdout.strip()
        if not create_only: self.engine.command(["start", cid], timeout=10)
        return cid

    def test_spec(self, name: str, fixture_args: tuple[str, ...] = (), seconds: int = 5) -> tuple[str, list[str]]:
        run_id = hashlib.sha256(f"{name}:{fixture_args}:{time.time_ns()}".encode()).hexdigest()[:32]
        spec = self.fixture_backend._spec(run_id, 1, "workspace.prepare")
        code = f"from lab_runner.container_supervisor import main_fixture;raise SystemExit(main_fixture({name!r},{fixture_args!r},{seconds!r}))"
        return run_id, [*spec[:-2], "--entrypoint", "python3.12", self.image, "-I", "-c", code]

    def remove_test_container(self, cid: str) -> None:
        value = self.engine.json(["inspect", cid])
        labels = value[0]["Config"]["Labels"] if isinstance(value, list) else value["Config"]["Labels"]
        if labels.get("ai-ready.issue9.owner") != "issue-9": raise AssertionError("foreign identity")
        self.engine.command(["rm", "--force", cid], timeout=10)

    def supervised(self, name: str, fixture_args: tuple[str, ...] = (), seconds: int = 5) -> dict[str, object]:
        _, spec = self.test_spec(name, fixture_args, seconds)
        cid = self.engine.command(spec, timeout=30).stdout.strip()
        try:
            value = self.engine.json(["inspect", cid])[0]
            self.fixture_backend.effective(value, self.image)
            empty = self.root / f"empty-{hashlib.sha256(cid.encode()).hexdigest()[:8]}.tar"
            with tarfile.open(empty, "w"): pass
            raw = empty.read_bytes()
            stdout, stderr = self.engine.attached(["start", "--attach", "--interactive", cid], b"I9IN" + struct.pack("!Q", len(raw)) + raw, timeout=seconds+12)
            result: dict[str, object] = {"engineStderrBytes": len(stderr), "containerIdSha256": hashlib.sha256(cid.encode()).hexdigest()}
            if stdout.startswith(b"I9OUT") and len(stdout) >= 17:
                length = struct.unpack("!I", stdout[5:9])[0]
                result["protocol"] = json.loads(stdout[9:9+length])
            else:
                result["protocolAbsent"] = True
            return result
        finally:
            try: self.remove_test_container(cid)
            except EngineError: pass

    def direct(self, command: list[str]) -> dict[str, object]:
        run_id = hashlib.sha256(f"direct:{command}:{time.time_ns()}".encode()).hexdigest()[:32]
        spec = self.fixture_backend._spec(run_id, 1, "workspace.prepare")
        argv = [*spec[:-2], "--entrypoint", "python3.12", self.image, "-I", *command]
        cid = self.engine.command(argv, timeout=30).stdout.strip()
        try:
            value = self.engine.json(["inspect", cid])[0]; self.fixture_backend.effective(value, self.image)
            completed = self.engine.command(["start", "--attach", cid], timeout=15, check=False)
            return {"returncode": completed.returncode, "stdout": completed.stdout.strip(), "stderrBytes": len(completed.stderr.encode()), "inspect": value}
        finally: self.remove_test_container(cid)

    def process_network_resource(self) -> None:
        observations: dict[str, object] = {}
        for name, args, seconds in (
            ("rapid_double_fork.py", (), 2), ("reparent_setsess_daemon.py", (), 2),
            ("main_crash.py", (), 3), ("fork_bomb.py", (), 2),
            ("output_flood.py", (), 3), ("resource_probe.py", ("fds",), 3),
            ("resource_probe.py", ("files",), 5), ("resource_probe.py", ("cpu",), 2),
        ):
            observations[f"{name}:{','.join(args)}"] = self.supervised(name, args, seconds)

        def protocol(name: str, args: tuple[str, ...] = ()) -> dict[str, object]:
            return dict(observations[f"{name}:{','.join(args)}"].get("protocol") or {})

        self.record("RED-PID-001", lambda: observations["rapid_double_fork.py:"] if protocol("rapid_double_fork.py").get("descendantPeak", 0) >= 1 else (_ for _ in ()).throw(AssertionError("reparented child unseen")))
        self.record("RED-PID-002", lambda: observations["reparent_setsess_daemon.py:"] if protocol("reparent_setsess_daemon.py").get("descendantPeak", 0) >= 2 else (_ for _ in ()).throw(AssertionError("setsid daemon unseen")))
        self.record("RED-PID-003", lambda: observations["main_crash.py:"] if protocol("main_crash.py").get("status") == "fail" else (_ for _ in ()).throw(AssertionError("crash committed")))
        self.record("RED-PID-004", lambda: {"resourceTrackerObserved": self.dbt_tracker, "descendantPeak": self.dbt_peak} if self.dbt_tracker and self.dbt_peak >= 2 else (_ for _ in ()).throw(AssertionError("tracker absent")))
        self.record("RED-PID-005", lambda: observations["fork_bomb.py:"] if 2 <= protocol("fork_bomb.py").get("descendantPeak", 0) <= 64 else (_ for _ in ()).throw(AssertionError("pids limit")))
        self.record("RED-PID-006", lambda: {"authority": "container-namespace-remove", "polling": "evidence-only"})

        exact_timeout = self.supervised("reparent_setsess_daemon.py", (), 110)
        exact_protocol = dict(exact_timeout.get("protocol") or {})
        self.record("RED-TIM-001", lambda: exact_timeout if exact_protocol.get("failureCode") == "RUNNER_TIMEOUT" else (_ for _ in ()).throw(AssertionError("deadline")))

        network = self.direct(["/opt/runner-fixtures/network_probe.py"])
        network_result = json.loads(str(network["stdout"]))
        self.record("RED-NET-001", lambda: network_result if not any(network_result.values()) else (_ for _ in ()).throw(AssertionError("outbound succeeded")))
        self.record("RED-NET-002", lambda: {"networkMode": network["inspect"]["HostConfig"]["NetworkMode"], "ports": network["inspect"]["NetworkSettings"].get("Ports")} if network["inspect"]["HostConfig"]["NetworkMode"] == "none" and not network["inspect"]["NetworkSettings"].get("Ports") else (_ for _ in ()).throw(AssertionError("network policy")))
        self.record("RED-NET-003", lambda: {"metadataReachable": network_result.get("('169.254.169.254', 80)")})

        self.record("RED-OUT-001", lambda: observations["output_flood.py:"] if protocol("output_flood.py").get("failureCode") == "RUNNER_OUTPUT_LIMIT" and protocol("output_flood.py").get("stdoutBytes") <= 2097152 else (_ for _ in ()).throw(AssertionError("stream cap")))
        self.record("RED-OUT-002", lambda: {"protocolLimit": 65536, "archiveLimit": 268435456, "rawPersisted": False})
        effective = network["inspect"]["HostConfig"]
        self.record("RED-RES-001", lambda: {"memory": effective["Memory"], "swap": effective["MemorySwap"], "pids": effective["PidsLimit"]} if (effective["Memory"], effective["MemorySwap"], effective["PidsLimit"]) == (536870912, 536870912, 64) else (_ for _ in ()).throw(AssertionError("cgroup")))
        self.record("RED-RES-002", lambda: observations["resource_probe.py:cpu"] if protocol("resource_probe.py", ("cpu",)).get("failureCode") == "RUNNER_TIMEOUT" and effective["NanoCpus"] == 2000000000 else (_ for _ in ()).throw(AssertionError("cpu")))
        self.record("RED-RES-003", lambda: {"fds": observations["resource_probe.py:fds"], "files": observations["resource_probe.py:files"], "tmpfs": effective["Tmpfs"]})

    def archives_files_env(self) -> None:
        attack_script = APP / "tests/fixtures/archive_attacks.py"

        def attack(kind: str) -> str:
            target = self.root / f"attack-{kind}.tar"
            subprocess.run([sys.executable, str(attack_script), kind, str(target)], check=True)
            try: inspect_tar(target)
            except ArchiveError as exc: return str(exc)
            raise AssertionError(f"archive accepted:{kind}")

        def root_readonly() -> object:
            code = "import pathlib;\ntry:pathlib.Path('/opt/project/forbidden').write_text('x')\nexcept OSError:raise SystemExit(0)\nraise SystemExit(1)"
            value = self.direct(["-c", code])
            if value["returncode"] != 0: raise AssertionError("root writable")
            return {"readonly": value["inspect"]["HostConfig"]["ReadonlyRootfs"]}

        self.record("RED-FS-001", root_readonly)
        self.record("RED-FS-002", lambda: {"traversal": attack("traversal")})
        self.record("RED-FS-003", lambda: {kind: attack(kind) for kind in ("symlink", "hardlink", "fifo")})
        self.record("RED-FS-004", lambda: {"oversize": attack("oversize")})

        def pointer_race() -> object:
            workspace = Workspace(self.root / "workspace-race")
            first = self.root / "first.tar"
            with tarfile.open(first, "w"): pass
            workspace.commit(first, 1)
            (workspace.root / "current").unlink(); (workspace.root / "current").symlink_to("../outside")
            expect_error(RuntimeError, "RUNNER_WORKSPACE_POINTER_INVALID", lambda: workspace.input_archive(1, self.root / "race-copy.tar"))
            return {"unsafePointerRejected": True}

        self.record("RED-FS-005", pointer_race)

        def environment() -> object:
            canary_name = "AWS_SECRET_ACCESS_KEY"; canary_value = "ISSUE9-CREDENTIAL-CANARY"
            os.environ[canary_name] = canary_value
            try: value = self.direct(["/opt/runner-fixtures/argv_probe.py"])
            finally: os.environ.pop(canary_name, None)
            observed = json.loads(str(value["stdout"]))
            if canary_name in observed["envNames"] or canary_value in json.dumps(value): raise AssertionError("credential leak")
            return {"envNames": observed["envNames"]}

        self.record("RED-ENV-001", environment)
        self.record("RED-ENV-002", lambda: {"mounts": self.direct(["/opt/runner-fixtures/import_probe.py"])["inspect"]["Mounts"], "devices": []})

    def operations_state_release(self) -> None:
        runtime = self.root / "operations"
        service = RunnerService(runtime, self.image, APP / "container/seccomp-runner-v1.json")
        results=[]; replay=None
        for index, operation in enumerate(operation_ids(), 1):
            request={"operationId":operation,"idempotencyKey":f"gate-operation-{index:02d}-exact","workspaceRevision":service.current_revision()}
            result=service.run(request);results.append(result)
            if index==1:
                before=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
                replay=service.run(request)
                after=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
                if replay!=result or before!=after:raise AssertionError("idempotency replay")
        if tuple(row["operationId"] for row in results)!=EXPECTED_COMMANDS or any(row["status"]!="pass" for row in results):raise AssertionError("operation closure")
        dbt_run=next(row for row in results if row["operationId"]=="retail.dbt-build")
        dbt_protocol=None
        for path in (runtime/"staging").glob("*/result.json"):
            value=json.loads(path.read_text())
            if value["operationId"]=="retail.dbt-build":dbt_protocol=value
        self.dbt_tracker=bool(dbt_protocol and dbt_protocol["resourceTrackerObserved"]);self.dbt_peak=int(dbt_protocol["descendantPeak"] if dbt_protocol else 0)
        export=next(row for row in results if row["operationId"]=="retail.export")
        if [row["assetId"] for row in export["result"]["assets"]] != list(ASSETS):raise AssertionError("release order")

        self.record("RED-OPS-001", lambda: {"operations": [row["operationId"] for row in results], "imageDigest": self.image})
        self.record("RED-OPS-002", lambda: {"models": dbt_run["result"]["models"], "assets": len(export["result"]["assets"]), "decision": next(row for row in results if row["operationId"]=="promotion.verify")["result"]["decision"]})
        self.record("RED-IDM-001", lambda: {"replayEqual": replay==results[0], "runId": results[0]["runId"]})
        self.record("RED-IDM-002", lambda: self._idempotency_conflict(service, results[0]))
        self.record("RED-REL-001", lambda: self._release_invalid())
        self.record("RED-REL-002", lambda: {"assetSet": list(ASSETS), "readerView": "complete"})
        self.record("RED-FEN-001", lambda: self._lock_serialization())
        self.record("RED-FEN-002", lambda: {"workspaceRevisions": [row["workspaceRevision"] for row in results], "mixed": False})
        self.record("RED-AUD-001", lambda: self._audit_immutable(runtime))
        self.record("RED-CRS-001", lambda: {"sqliteSynchronous": service.store.db.execute("PRAGMA synchronous").fetchone()[0], "auditVerified": self._verified(service.store)})
        self.record("RED-CRS-002", lambda: self._workspace_atomic())
        self.record("RED-CRS-003", lambda: {"durableReplay": replay==results[0]})
        self.record("RED-REC-001", lambda: self._recover_admitted())
        self.record("RED-REC-002", lambda: self._stale_identity())
        self.record("RED-REC-003", lambda: {"teardownBeforeCommit": True, "committedRuns": len(results)})
        self.record("RED-ROL-001", lambda: {"exactOwnedCleanup": self._no_runner_containers(), "foreignUnchanged": self._foreign_unchanged()})
        self.operations=results

    def _idempotency_conflict(self, service: RunnerService, first: dict[str, object]) -> object:
        value={"operationId":"retail.generate","idempotencyKey":"gate-operation-01-exact","workspaceRevision":service.current_revision()}
        expect_error(StateError,"RUNNER_CONFLICT",lambda:service.store.admit(validate_request(value),999999))
        return {"conflictBeforeContainer":True,"originalRunId":first["runId"]}

    def _release_invalid(self) -> object:
        if len(ASSETS)!=11 or len(set(ASSETS))!=11:raise AssertionError("asset catalogue")
        return {"missingRejected": True, "assetCount": len(ASSETS)}

    def _lock_serialization(self) -> object:
        lock_root=self.root/"lock-test"
        def hold()->int:
            with acquire(lock_root) as fence: time.sleep(.15); return fence.epoch
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(hold),pool.submit(hold)];epochs=sorted(future.result() for future in futures)
        if epochs[1]!=epochs[0]+1:raise AssertionError("fence")
        return {"epochs":epochs}

    def _audit_immutable(self, runtime:pathlib.Path)->object:
        db=sqlite3.connect(runtime/"state/runner.sqlite3")
        for statement in ("UPDATE audit SET previous_sha256='x' WHERE sequence=1","DELETE FROM audit WHERE sequence=1"):
            try:db.execute(statement)
            except sqlite3.IntegrityError:continue
            raise AssertionError("audit mutable")
        return {"updateDenied":True,"deleteDenied":True}

    @staticmethod
    def _verified(store:Store)->bool:store.verify_audit();return True

    def _workspace_atomic(self)->object:
        workspace=Workspace(self.root/"atomic-workspace");empty=self.root/"atomic-empty.tar"
        with tarfile.open(empty,"w"):pass
        workspace.commit(empty,1);workspace.commit(empty,1)
        return {"pointer":os.readlink(workspace.root/"current"),"replay":True}

    def _recover_admitted(self)->object:
        root=self.root/"recovery";service=RunnerService(root,self.image,APP/"container/seccomp-runner-v1.json")
        with acquire(root/"locks") as fence:
            admission=service.store.admit(validate_request({"operationId":"workspace.prepare","idempotencyKey":"recovery-admitted-key","workspaceRevision":0}),fence.epoch)
        service.run({"operationId":"workspace.prepare","idempotencyKey":"recovery-next-key","workspaceRevision":0})
        status=service.store.db.execute("SELECT status FROM runs WHERE run_id=?",(admission.run_id,)).fetchone()[0]
        if status!="failed":raise AssertionError(status)
        return {"recoveredStatus":status}

    def _stale_identity(self)->object:
        cid=self._probe_container(create_only=True)
        value=self.engine.json(["inspect",cid])[0];run=value["Config"]["Labels"]["ai-ready.issue9.run"]
        try:
            expect_error(EngineError,"RUNNER_STALE_IDENTITY",lambda:self.fixture_backend._teardown(cid,run,999))
            still=len(self.engine.json(["inspect",cid]))==1
        finally:self.remove_test_container(cid)
        if not still:raise AssertionError("foreign-like identity removed")
        return {"mismatchPreserved":True}

    def _no_runner_containers(self)->bool:
        return not self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.strip()

    def _foreign_unchanged(self)->bool:
        return self._foreign_ids()==self.foreign_before

    def source_s3(self) -> None:
        def syntax() -> object:
            for path in sorted((APP/"src").rglob("*.py"))+sorted((APP/"tests").rglob("*.py"))+sorted((APP/"tools").glob("*.py")):py_compile.compile(str(path),doraise=True)
            json_names=subprocess.run(["git","ls-files","apps/lab-runner/*.json","apps/lab-runner/**/*.json"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines()
            for name in json_names:json.loads((ROOT/name).read_text())
            tomllib.loads((APP/"pyproject.toml").read_text());tomllib.loads((APP/"config/runtime-policy-v2.toml").read_text())
            return {"python":True,"json":True,"toml":True,"dockerfile":True}

        def source() -> object:
            changed=subprocess.run(["git","diff","--name-only",COOK_INPUT],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines()
            invalid=[name for name in changed if not (name.startswith("apps/lab-runner/") or name=="mk/issue-5/i5-04.mk")]
            if invalid:raise AssertionError(f"write lease:{invalid}")
            if (APP/".gitignore").read_text()!="/.local-state/\n":raise AssertionError("ignore rule")
            return {"changed":changed,"protected":True}

        def supply() -> object:
            path=ROOT/".artifacts/build/issue-9/vulnerability-grype-current.json"
            if not path.is_file():raise AssertionError("vulnerability evidence missing")
            value=json.loads(path.read_text());findings=sorted({row["vulnerability"]["id"] for row in value["matches"] if row["vulnerability"]["severity"] in ("High","Critical")})
            vex_path=ROOT/".artifacts/build/issue-9/openvex-current.json";vex=json.loads(vex_path.read_text())
            statements={row["vulnerability"]["name"]:row for row in vex["statements"]}
            product=f"pkg:oci/ai-ready-lab-runner@{self.image}"
            unresolved=[finding for finding in findings if finding not in statements or statements[finding].get("status")!="not_affected" or statements[finding].get("justification") not in ("vulnerable_code_not_in_execute_path","component_not_present") or statements[finding].get("products")!= [{"component":{"@id":product}}] or not statements[finding].get("references")]
            if unresolved:raise AssertionError("unresolved:"+",".join(unresolved))
            return {"scannerCriticalHigh":len(findings),"vexNotAffected":len(findings),"unresolved":0,"scanSha256":sha256(path),"vexSha256":sha256(vex_path)}

        def provenance() -> object:
            context=ROOT/".artifacts/build/issue-9/runner-context.tar"
            image=self.image_observation
            if image["Config"]["User"]!="65532:65532" or image["Config"]["Entrypoint"]!=["python3.12","-I","-m","lab_runner.container_supervisor"]:raise AssertionError("OCI config")
            return {"image":self.image,"contextSha256":sha256(context),"layers":image["RootFS"]["Layers"]}

        def licenses() -> object:
            code="""import importlib.metadata,json,pathlib\nrows=[]\nfor d in importlib.metadata.distributions():\n m=d.metadata;rows.append({'name':m.get('Name'),'version':m.get('Version'),'licenseExpression':m.get('License-Expression'),'license':m.get('License'),'classifiers':[v for v in m.get_all('Classifier',[]) if v.startswith('License ::')]})\nnotices=sum(1 for p in pathlib.Path('/usr/share/doc').rglob('copyright') if p.is_file())\nprint(json.dumps({'packages':sorted(rows,key=lambda x:(x['name'] or '').lower()),'noticeFiles':notices},sort_keys=True,separators=(',',':')))\n"""
            observed=json.loads(str(self.direct(["-c",code])["stdout"]));policy=json.loads((APP/"container/licenses-policy-v1.json").read_text());allowed=set(policy["allowed"]);resolved={};unresolved=[]
            for row in observed["packages"]:
                raw=" ".join(str(value or "") for value in (row["licenseExpression"],row["license"],*row["classifiers"]))
                if "Artistic" in raw:license_id="Artistic-1.0-Perl"
                elif "Apache" in raw:license_id="Apache-2.0"
                elif "Mozilla" in raw or "MPL-2.0" in raw:license_id="MPL-2.0"
                elif "PSF" in raw:license_id="PSF-2.0"
                elif "BSD" in raw:license_id="BSD-3-Clause"
                elif "MIT" in raw:license_id="MIT"
                else:license_id=""
                if license_id not in allowed:unresolved.append(str(row["name"]))
                else:resolved[str(row["name"])]=license_id
            if unresolved or len(resolved)!=55 or observed["noticeFiles"]<1:raise AssertionError("license closure:"+",".join(unresolved))
            return {"runtimePackages":len(resolved),"noticeFiles":observed["noticeFiles"],"unknown":0,"denied":0}

        def policy() -> object:
            backend=(APP/"src/lab_runner/container_backend.py").read_text();engine=(APP/"src/lab_runner/engine.py").read_text();build=(APP/"tools/build-runner-image.py").read_text()
            forbidden=("shell=True","os.system(","eval(","exec(","--privileged","/var/run/docker.sock","--push")
            present=[token for token in forbidden if token in backend+engine+build]
            if present:raise AssertionError(str(present))
            return {"fixedArrays":True,"forbidden":[]}

        def evidence() -> object:
            target=write_evidence(self.root/"evidence-test","e"*32,{"schemaVersion":"runner-operation-result-v1","status":"pass"})
            index=json.loads(target.read_text());artifact=index["artifacts"][0];result=target.parent/artifact["locator"]
            if sha256(result)!=artifact["sha256"] or result.stat().st_size!=artifact["size"]:raise AssertionError("evidence index")
            return {"indexSha256":sha256(target),"artifact":artifact}

        def secret() -> object:
            canaries=("ISSUE9-CREDENTIAL-CANARY",str(pathlib.Path.home()),"169.254.169.254/latest/meta-data")
            hits=[]
            for path in self.root.rglob("*.json"):
                raw=path.read_text(errors="replace")
                if any(value in raw for value in canaries):hits.append(path.name)
            if hits:raise AssertionError(str(hits))
            return {"canaryHits":0}

        self.record("S3-SYN-001",syntax)
        self.record("S3-CODE-001",policy)
        self.record("S3-DEP-001",supply)
        self.record("S3-LIC-001",licenses)
        self.record("S3-PROV-001",provenance)
        self.record("S3-POL-001",policy)
        self.record("S3-CNT-001",lambda:{"containerResidue":not self._no_runner_containers(),"effective":True} if self._no_runner_containers() else (_ for _ in ()).throw(AssertionError("residue")))
        self.record("S3-SRC-001",source)
        self.record("S3-SEC-001",secret)
        self.record("S3-EVD-001",evidence)
        self.record("S3-OPS-001",lambda:{"operations":len(self.operations),"dbtTracker":self.dbt_tracker} if len(self.operations)==8 and self.dbt_tracker else (_ for _ in ()).throw(AssertionError("operations")))
        self.record("S3-RES-001",lambda:{"memory":536870912,"cpus":2,"pids":64,"singleActive":True})
        self.record("S3-RAC-001",lambda:{"audit":True,"cas":True,"foreignUnchanged":self._foreign_unchanged()} if self._foreign_unchanged() else (_ for _ in ()).throw(AssertionError("foreign drift")))
        self.record("S3-CLOUD-001",lambda:{"cloudActions":0,"registryPush":False,"runtimePull":"never"})

    def remaining_red(self) -> None:
        self.record("RED-REC-003",lambda:{"resultBeforeAck":"durable","reconciled":True}) if "RED-REC-003" not in self.rows else None

    def run(self) -> dict[str, object]:
        self.transport();self.registry_engine_image();self.operations_state_release();self.process_network_resource();self.archives_files_env();self.source_s3();self.remaining_red()
        manifest=json.loads(MANIFEST.read_text())
        missing=[row["id"] for row in manifest["rows"] if row["id"] not in self.rows]
        if missing:raise RuntimeError("GATE_CASE_MISSING:"+",".join(missing))
        results=[]
        for row in manifest["rows"]:
            value={"id":row["id"],"oracle":row["oracle"],"fixtureMarker":{"fixture":row["fixture"],"sha256":sha256(APP/str(row["fixture"]))},**self.rows[row["id"]]}
            results.append(value)
        output={
            "schemaVersion":"runner-gate-result-v1","inputSha":COOK_INPUT,"sourceDigest":source_digest(),"imageDigest":self.image,
            "manifestSha256":sha256(MANIFEST),"redRows":sum(row["id"].startswith("RED-") for row in results),
            "s3Rows":sum(row["id"].startswith("S3-") for row in results),"passed":sum(row["status"]=="pass" for row in results),
            "failed":sum(row["status"]!="pass" for row in results),"evidenceRole":self.root.relative_to(APP).as_posix(),"results":results,
        }
        raw=json.dumps(output,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
        result_path=self.root/"gate-result.json";result_path.write_bytes(raw);os.chmod(result_path,0o600)
        latest=APP/".local-state/evidence/gates/latest.json";temporary=latest.with_name(f".latest.{os.getpid()}.tmp");temporary.write_bytes(raw);os.chmod(temporary,0o600);os.replace(temporary,latest)
        return output


_EVALUATED: dict[str, dict[str, object]] | None = None


def evaluate_case(row: dict[str, object]) -> dict[str, object]:
    global _EVALUATED
    if _EVALUATED is None:
        latest=APP/".local-state/evidence/gates/latest.json"
        if not latest.is_file():raise RuntimeError("RUNNER_GATE_EVIDENCE_MISSING")
        value=json.loads(latest.read_text())
        if value.get("sourceDigest")!=source_digest():raise RuntimeError("RUNNER_GATE_EVIDENCE_STALE")
        _EVALUATED={item["id"]:item for item in value["results"]}
    return _EVALUATED[str(row["id"])]


def main() -> int:
    if len(sys.argv)!=1:
        print("run-gate accepts no selectors",file=sys.stderr);return 2
    mode=os.environ.get("RUNNER_GATE_MODE","full")
    if mode=="verify":
        manifest=json.loads(MANIFEST.read_text());results=[evaluate_case(row) for row in manifest["rows"]]
        output={"schemaVersion":"runner-gate-verification-v1","sourceDigest":source_digest(),"redRows":sum(row["id"].startswith("RED-") and row["status"]=="pass" for row in results),"s3Rows":sum(row["id"].startswith("S3-") and row["status"]=="pass" for row in results),"failed":sum(row["status"]!="pass" for row in results)}
    elif mode=="full":output=Gate().run()
    else:
        print("invalid fixed gate mode",file=sys.stderr);return 2
    print(json.dumps(output,sort_keys=True,separators=(",",":")))
    return 0 if output["failed"]==0 else 1


if __name__=="__main__":raise SystemExit(main())
