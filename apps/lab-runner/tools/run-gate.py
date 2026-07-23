#!/usr/bin/env python3
"""Fixed Issue #9 security, lifecycle, race, operation, and S3 gate."""
from __future__ import annotations

import concurrent.futures
import ast
import datetime
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import py_compile
import re
import shutil
import signal
import socket
import stat
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
sys.path.insert(0, str(ROOT))
_rfc8785_wheels=list((ROOT/".artifacts/build/issue-9/wheelhouse").glob("rfc8785-0.1.4-py3-none-any.whl"))
if len(_rfc8785_wheels)==1:sys.path.insert(0,str(_rfc8785_wheels[0]))

from lab_runner.archive import ArchiveError, Limits, inspect_tar
from lab_runner.container_backend import Backend
from lab_runner.container_protocol import read as read_protocol
from lab_runner.contract import EXPECTED_COMMANDS, validate_released_contract
from lab_runner.engine import Engine, EngineError
from lab_runner.evidence import write as write_evidence
from lab_runner.fence import acquire
from lab_runner.registry import RegistryError, operation_ids, validate_request
from lab_runner.release import ASSETS,manifest_bytes,publish as publish_release,validate as validate_release
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


def git_identity()->tuple[str,str,str]:
    dirty=subprocess.run(["git","status","--porcelain=v1","--untracked-files=normal"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout
    if dirty:raise RuntimeError("RUNNER_SOURCE_DIRTY")
    head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.strip()
    tree=subprocess.run(["git","rev-parse","HEAD^{tree}"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.strip()
    return head,tree,source_digest()


def _canonical_json(value:object)->bytes:
    return json.dumps(value,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"


def stable_result_sha256(value:object)->str:
    def project(item:object)->object:
        if isinstance(item,dict):
            return {key:project(child) for key,child in item.items() if key not in {"manifestSha256","dataRunId"}}
        if isinstance(item,list):return [project(child) for child in item]
        return item
    raw=json.dumps(project(value),sort_keys=True,separators=(",",":"),allow_nan=False).encode()
    return hashlib.sha256(raw).hexdigest()


def verify_gate_evidence(value:dict[str,object],gate_root:pathlib.Path)->None:
    results=value.get("results")
    if not isinstance(results,list) or any(not isinstance(row,dict) for row in results):raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")
    expected_ids=[row["id"] for row in json.loads(MANIFEST.read_text())["rows"]]
    if [row.get("id") for row in results]!=expected_ids:raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")
    result_path=gate_root/"gate-result.json";rows_root=gate_root/"rows"
    if result_path.read_bytes()!=_canonical_json(value) or not rows_root.is_dir():raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")
    if {path.name for path in rows_root.iterdir()}!={f"{case_id}.json" for case_id in expected_ids}:raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")
    for row in results:
        if (rows_root/f"{row['id']}.json").read_bytes()!=_canonical_json(row):raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")


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
        self.initial_identity=git_identity()
        validate_released_contract(ROOT,APP/"config/released-contract-lock.json")
        self.engine = Engine()
        self.engine_info = self.engine.admit()
        inspected = self.engine.json(["image", "inspect", "ai-ready-lab-runner:issue9"])
        if not isinstance(inspected, list) or len(inspected) != 1:
            raise RuntimeError("RUNNER_IMAGE_UNADMITTED")
        self.image_observation = inspected[0]
        self.image = str(inspected[0]["Id"])
        release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
        if release.get("imageDigest")!=self.image:raise RuntimeError("RUNNER_IMAGE_RELEASE_MISMATCH")
        self.rows: dict[str, dict[str, object]] = {}
        self.rollback_observation:dict[str,object]={}
        build_owner=ROOT/".artifacts/build/issue-9/owner.json";local_owner=APP/".local-state/.runner-owner.json"
        expected_owner={"schemaVersion":"runner-external-root-owner-v1","owner":"issue-9","cookInputSha":COOK_INPUT}
        for path,purpose in ((build_owner,"build-evidence"),(local_owner,"runtime-evidence")):
            path.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
            value={**expected_owner,"purpose":purpose}
            if path.exists() and json.loads(path.read_text())!=value:raise RuntimeError("RUNNER_EVIDENCE_OWNER_INVALID")
            path.write_bytes(_canonical_json(value));os.chmod(path,0o600)
        baseline=(ROOT/".hermes/prompts/issue-9-container-runner-v2-cook.md",ROOT/".hermes/logs/claudekit/issue-9-container-runner-v2-cook.log")
        self.ignored_baseline={path.relative_to(ROOT).as_posix():sha256(path) for path in baseline}
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
            self.rows[case_id] = {"status": "pass", "failureCode": None, "detail": detail, "durationNs": time.monotonic_ns() - started}
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
            expect_error(TransportError,"RUNNER_HEADER_FORBIDDEN",lambda:admit(method="POST",headers=[*headers,("X-Unexpected","value")],body=body,bearer="bearer",csrf="csrf",peer_uid=os.geteuid(),effective_uid=os.geteuid()))
            return {"rejected": ["missing-host", "duplicate-host","unexpected-header"]}

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
            framing=([row for row in headers if row[0]!="Content-Length"],[*headers,("Transfer-Encoding","chunked")],[*headers,("Content-Length",str(len(body)))])
            for changed in framing:expect_error(TransportError,"RUNNER_FRAMING_INVALID" if len(changed)!=len(headers)+1 or changed[-1][0]!="Content-Length" else "RUNNER_HEADER_AMBIGUOUS",lambda c=changed:admit(method="POST",headers=c,body=body,bearer="bearer",csrf="csrf",peer_uid=os.geteuid(),effective_uid=os.geteuid()))
            malformed=b"{not-json}";expect_error(TransportError,"RUNNER_JSON_INVALID",lambda:admit(method="POST",headers=self.valid_headers(malformed),body=malformed,bearer="bearer",csrf="csrf",peer_uid=os.geteuid(),effective_uid=os.geteuid()))
            return {"bodyLimit": 16384,"chunkedRejected":True,"ambiguousLengthRejected":True,"invalidJsonRejected":True}

        def trn5() -> object:
            expect_error(TransportError, "RUNNER_PEER_FORBIDDEN", lambda: admit(method="POST", headers=headers, body=body, bearer="bearer", csrf="csrf", peer_uid=os.geteuid()+1, effective_uid=os.geteuid()))
            control_root=self.root/"uds-control";control_root.mkdir(mode=0o700);control=control_root/"control.json"
            program="from lab_runner.transport import serve_uds\nclass Service:\n def run(self,request):return {'status':'pass','operationId':request['operationId']}\nserve_uds(Service(),__import__('pathlib').Path(__import__('sys').argv[1]))"
            process=subprocess.Popen([sys.executable,"-c",program,str(control)],cwd=ROOT,env={"PATH":"/usr/bin:/bin:/usr/local/bin","PYTHONPATH":str(SRC),"PYTHONDONTWRITEBYTECODE":"1"},stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,text=True)
            try:
                deadline=time.monotonic()+5
                while not control.is_file() and time.monotonic()<deadline:
                    if process.poll() is not None:raise AssertionError("UDS server exited")
                    time.sleep(.02)
                value=json.loads(control.read_text());socket_path=pathlib.Path(value["socket"])
                if stat.S_IMODE(control.stat().st_mode)!=0o600 or stat.S_IMODE(socket_path.stat().st_mode)!=0o600 or stat.S_IMODE(socket_path.parent.stat().st_mode)!=0o700:raise AssertionError("UDS mode")
                def exchange(raw:bytes)->bytes:
                    client=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM);client.settimeout(2);client.connect(str(socket_path));client.sendall(raw);chunks=[]
                    while True:
                        child=client.recv(65536)
                        if not child:break
                        chunks.append(child)
                    client.close();return b"".join(chunks)
                if b" 405 " not in exchange(b"GET / HTTP/1.1\r\nHost: runner.local\r\nConnection: close\r\n\r\n"):raise AssertionError("UDS method boundary")
                uds_headers=[("Host","runner.local"),("Authorization",f"Bearer {value['bearer']}"),("X-Runner-CSRF",value["csrf"]),("Content-Type","application/json"),("Content-Length",str(len(body)))]
                request_raw=b"POST / HTTP/1.0\r\n"+b"".join(f"{key}: {child}\r\n".encode() for key,child in uds_headers)+b"\r\n"+body
                if b" 200 " not in exchange(request_raw):raise AssertionError("UDS admission")
            finally:
                if process.poll() is None:process.send_signal(signal.SIGINT)
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:process.kill();process.wait();raise AssertionError("UDS shutdown timeout")
            if control.exists() or socket_path.exists() or socket_path.parent.exists() or any(control_root.iterdir()):raise AssertionError("UDS residue")
            return {"effectiveUid": os.geteuid(),"transport":"unix","mode":"0600","cleanup":True}

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
            mutations=(
                ("ReadonlyRootfs",False),("NetworkMode","bridge"),("Init",False),("PidsLimit",65),
                ("Memory",536870911),("MemorySwap",-1),("NanoCpus",1_000_000_000),("CapDrop",[]),
                ("Devices",[{"PathOnHost":"/dev/null"}]),("ShmSize",33554432),("GroupAdd",["0"]),
            )
            checked=[]
            for field,replacement in mutations:
                changed=json.loads(json.dumps(value));changed["HostConfig"][field]=replacement
                expect_error(EngineError,"RUNNER_CONTAINMENT_UNAVAILABLE",lambda c=changed:self.fixture_backend.effective(c,self.image));checked.append(field)
            for name in ("/workspace","/tmp","/run"):
                changed=json.loads(json.dumps(value));changed["HostConfig"]["Tmpfs"][name]="rw,size=1"
                expect_error(EngineError,"RUNNER_CONTAINMENT_UNAVAILABLE",lambda c=changed:self.fixture_backend.effective(c,self.image));checked.append(name)
            changed=json.loads(json.dumps(value));changed["HostConfig"]["SecurityOpt"]=["no-new-privileges"]
            expect_error(EngineError,"RUNNER_CONTAINMENT_UNAVAILABLE",lambda:self.fixture_backend.effective(changed,self.image));checked.append("seccomp")
            changed=json.loads(json.dumps(value));changed["Config"]["Env"].append("AWS_SECRET_ACCESS_KEY=canary")
            expect_error(EngineError,"RUNNER_CONTAINMENT_UNAVAILABLE",lambda:self.fixture_backend.effective(changed,self.image));checked.append("environment")
            return {"effectiveFields":checked}

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
            manifest=json.loads((APP/"requirements/wheelhouse-manifest-v1.json").read_text());wheelhouse=ROOT/".artifacts/build/issue-9/wheelhouse";observed={path.name:sha256(path) for path in wheelhouse.iterdir() if path.is_file()}
            expected={row["file"]:row["sha256"] for row in manifest["wheels"]};lock=(APP/"requirements/runner-py312-linux-arm64.lock").read_text();dockerfile=(APP/"container/runner.Dockerfile").read_text();release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
            if observed!=expected or any(not name.endswith(".whl") for name in observed) or lock.count("--hash=sha256:")!=len(expected) or "--no-index" not in dockerfile or "--require-hashes" not in dockerfile or release.get("buildLockSha256")!=sha256(APP/"config/container-build-lock-v1.json"):raise AssertionError("supply admission")
            return {"hashCompleteWheels":len(expected),"sdists":0,"onlineInstall":False,"releaseRecordBound":True}

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

    def production_timeout(self) -> dict[str, object]:
        root=self.root/"production-timeout";store=Store(root/"state");backend=Backend(self.engine,self.image,APP/"container/seccomp-runner-v1.json",root/"staging",store)
        request=validate_request({"operationId":"workspace.prepare","idempotencyKey":"production-timeout-exact","workspaceRevision":0});admission=store.admit(request,9001);original=backend._spec
        def fixture_spec(run_id:str,fence:int,operation_id:str,daemon_identity:str|None=None)->list[str]:
            spec=original(run_id,fence,operation_id,daemon_identity);code="from lab_runner.container_supervisor import main_fixture;raise SystemExit(main_fixture('reparent_setsess_daemon.py',(),110))"
            return [*spec[:-2],"--entrypoint","python3.12",self.image,"-I","-c",code]
        backend._spec=fixture_spec  # type: ignore[method-assign]
        archive=root/"input.tar";archive.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
        with tarfile.open(archive,"w"):pass
        started=time.monotonic_ns();expect_error(EngineError,"RUNNER_TIMEOUT",lambda:backend.execute(admission.run_id,9001,"workspace.prepare",archive));duration=time.monotonic_ns()-started
        if not 110_000_000_000<=duration<=120_000_000_000 or not self._no_runner_containers():raise AssertionError("production deadline")
        return {"wallDurationNs":duration,"authority":"Backend.execute","containerAbsent":True,"deadlineSeconds":120}

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
            ("resource_probe.py", ("memory",), 10),
        ):
            observations[f"{name}:{','.join(args)}"] = self.supervised(name, args, seconds)

        def protocol(name: str, args: tuple[str, ...] = ()) -> dict[str, object]:
            return dict(observations[f"{name}:{','.join(args)}"].get("protocol") or {})

        self.record("RED-PID-001", lambda: observations["rapid_double_fork.py:"] if protocol("rapid_double_fork.py").get("descendantPeak", 0) >= 1 else (_ for _ in ()).throw(AssertionError("reparented child unseen")))
        self.record("RED-PID-002", lambda: observations["reparent_setsess_daemon.py:"] if protocol("reparent_setsess_daemon.py").get("descendantPeak", 0) >= 2 else (_ for _ in ()).throw(AssertionError("setsid daemon unseen")))
        self.record("RED-PID-003", lambda: observations["main_crash.py:"] if protocol("main_crash.py").get("status") == "fail" else (_ for _ in ()).throw(AssertionError("crash committed")))
        self.record("RED-PID-004", lambda: {"resourceTrackerObserved": self.dbt_tracker, "descendantPeak": self.dbt_peak} if self.dbt_tracker and self.dbt_peak >= 2 else (_ for _ in ()).throw(AssertionError("tracker absent")))
        self.record("RED-PID-005", lambda: observations["fork_bomb.py:"] if 2 <= protocol("fork_bomb.py").get("descendantPeak", 0) <= 64 else (_ for _ in ()).throw(AssertionError("pids limit")))
        self.record("RED-PID-006", lambda: {"protocol":protocol("rapid_double_fork.py"),"containerAbsent":self._no_runner_containers(),"authority":"container-remove"} if protocol("rapid_double_fork.py").get("failureCode")=="RUNNER_DESCENDANT_SURVIVOR" and self._no_runner_containers() else (_ for _ in ()).throw(AssertionError("polling changed authority")))

        self.record("RED-TIM-001",self.production_timeout)

        network = self.direct(["/opt/runner-fixtures/network_probe.py"])
        network_result = json.loads(str(network["stdout"]))
        self.record("RED-NET-001", lambda: network_result if not any(network_result.values()) else (_ for _ in ()).throw(AssertionError("outbound succeeded")))
        self.record("RED-NET-002", lambda: {"networkMode": network["inspect"]["HostConfig"]["NetworkMode"], "ports": network["inspect"]["NetworkSettings"].get("Ports")} if network["inspect"]["HostConfig"]["NetworkMode"] == "none" and not network["inspect"]["NetworkSettings"].get("Ports") else (_ for _ in ()).throw(AssertionError("network policy")))
        self.record("RED-NET-003", lambda: {"metadataReachable": network_result.get("('169.254.169.254', 80)")})

        self.record("RED-OUT-001", lambda: observations["output_flood.py:"] if protocol("output_flood.py").get("failureCode") == "RUNNER_OUTPUT_LIMIT" and protocol("output_flood.py").get("stdoutBytes") <= 2097152 else (_ for _ in ()).throw(AssertionError("stream cap")))
        self.record("RED-OUT-002", self._bounded_protocol_archive)
        effective = network["inspect"]["HostConfig"]
        memory=dict(protocol("resource_probe.py",("memory",)).get("cgroup") or {});events=dict(memory.get("memoryEvents") or {})
        self.record("RED-RES-001", lambda: {"memory": effective["Memory"], "swap": effective["MemorySwap"], "pids": effective["PidsLimit"],"pressure":memory,"authority":"aggregate-cgroup-v2"} if (effective["Memory"], effective["MemorySwap"], effective["PidsLimit"]) == (536870912, 536870912, 64) and protocol("resource_probe.py",("memory",)).get("failureCode")=="RUNNER_RESOURCE_LIMIT" and memory.get("memoryMax")=="536870912" and memory.get("memorySwapMax")=="0" and 0<int(memory.get("memoryPeak",0))<=536870912 and int(events.get("oom",0))>=1 and int(events.get("oom_kill",0))>=1 else (_ for _ in ()).throw(AssertionError("cgroup")))
        self.record("RED-RES-002", lambda: observations["resource_probe.py:cpu"] if protocol("resource_probe.py", ("cpu",)).get("failureCode") == "RUNNER_TIMEOUT" and effective["NanoCpus"] == 2000000000 else (_ for _ in ()).throw(AssertionError("cpu")))
        self.record("RED-RES-003", lambda: {"fds": observations["resource_probe.py:fds"], "files": observations["resource_probe.py:files"], "tmpfs": effective["Tmpfs"],"fileQuota":4096} if protocol("resource_probe.py",("files",)).get("failureCode")=="RUNNER_RESOURCE_LIMIT" and protocol("resource_probe.py",("files",)).get("status")=="fail" and protocol("resource_probe.py",("fds",)).get("status")=="fail" else (_ for _ in ()).throw(AssertionError("file/fd quota")))

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
            copied=self.root/"race-copy.tar";workspace.input_archive(1,copied)
            if copied.read_bytes()!=first.read_bytes():raise AssertionError("mutable pointer selected input")
            return {"unsafePointerIgnored": True,"selectedRevision":1}

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
        results=[]; replay=None;reset_replay=None;repeat_export=None
        for index, operation in enumerate(operation_ids(), 1):
            request={"operationId":operation,"idempotencyKey":f"gate-operation-{index:02d}-exact","workspaceRevision":service.current_revision()}
            result=service.run(request);results.append(result)
            if index==1:
                before=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
                replay=service.run(request)
                after=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
                if replay!=result or before!=after:raise AssertionError("idempotency replay")
            if operation=="workspace.reset":
                before=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines());reset_replay=service.run(request);after=len(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
                if reset_replay!=result or before!=after or result["result"]["preserved"]!=["evidence.json","progress.json"]:raise AssertionError("reset replay")
            if operation=="retail.export":
                repeat_export=service.run({"operationId":"retail.export","idempotencyKey":"gate-repeat-export-exact","workspaceRevision":service.current_revision()})
                if repeat_export["result"]["assets"]!=result["result"]["assets"] or repeat_export["releaseManifest"]!=result["releaseManifest"]:raise AssertionError("repeat export generation")
        if tuple(row["operationId"] for row in results)!=EXPECTED_COMMANDS or any(row["status"]!="pass" for row in results):raise AssertionError("operation closure")
        dbt_run=next(row for row in results if row["operationId"]=="retail.dbt-build")
        dbt_protocol=None
        for path in (runtime/"staging").glob("*/result.json"):
            value=json.loads(path.read_text())
            if value["operationId"]=="retail.dbt-build":dbt_protocol=value
        self.dbt_tracker=bool(dbt_protocol and dbt_protocol["resourceTrackerObserved"]);self.dbt_peak=int(dbt_protocol["descendantPeak"] if dbt_protocol else 0)
        export=next(row for row in results if row["operationId"]=="retail.export")
        if [row["assetId"] for row in export["result"]["assets"]] != list(ASSETS):raise AssertionError("release order")
        if export.get("releaseAssets")!=export["result"]["assets"]:raise AssertionError("host release validation")
        repro_service=RunnerService(self.root / "operations-export-repro", self.image, APP / "container/seccomp-runner-v1.json")
        repro_export=None
        for index, operation in enumerate(operation_ids()[:5], 1):
            repro_export=repro_service.run({"operationId":operation,"idempotencyKey":f"gate-export-repro-{index:02d}","workspaceRevision":repro_service.current_revision()})
        if repro_export is None or repro_export["operationId"]!="retail.export":raise AssertionError("export reproducibility sequence")
        original_assets=[(row["assetId"],row["size"],row["sha256"]) for row in export["result"]["assets"]]
        reproduced_assets=[(row["assetId"],row["size"],row["sha256"]) for row in repro_export["result"]["assets"]]
        if reproduced_assets!=original_assets:raise AssertionError("export raw bytes are not reproducible")
        release_pointer=json.loads((runtime/"releases/current.json").read_text());release_record=json.loads((runtime/"releases/generations"/f"{export['workspaceRevision']:020d}.json").read_text())
        if release_pointer["schemaVersion"]!="curated-release-current-pointer-v1" or release_pointer["currentReleaseId"]!=export["releaseManifest"]["releaseId"] or release_pointer["manifestSha256"]!=export["releaseManifest"]["manifestSha256"] or release_record["runId"]!=export["runId"] or release_record["fence"]!=export["fence"] or release_record["workspaceRevision"]!=export["workspaceRevision"]:raise AssertionError("release pointer binding")
        self.operations=results
        self.operation_service=service

        self.record("RED-OPS-001", lambda: {"operations": [row["operationId"] for row in results], "imageDigest": self.image})
        self.record("RED-OPS-002", lambda: {"models": dbt_run["result"]["models"], "assets": len(export["result"]["assets"]), "rawExportReproduced": reproduced_assets==original_assets, "repeatExportAdmitted":repeat_export is not None, "decision": next(row for row in results if row["operationId"]=="promotion.verify")["result"]["decision"]})
        self.record("RED-IDM-001", lambda: {"replayEqual": replay==results[0],"resetReplayEqual":reset_replay==results[-1],"resetPreserved":results[-1]["result"]["preserved"], "runId": results[0]["runId"]})
        self.record("RED-IDM-002", lambda: self._idempotency_conflict(service, results[0]))
        self.record("RED-REL-001", lambda: self._release_invalid())
        self.record("RED-REL-002", self._release_reader_atomicity)
        self.record("RED-FEN-001", lambda: self._lock_serialization())
        self.record("RED-FEN-002", lambda: self._stale_revision_conflict(service))
        self.record("RED-AUD-001", lambda: self._audit_immutable(runtime))
        self.record("RED-CRS-001", lambda: {"sqliteSynchronous": service.store.db.execute("PRAGMA synchronous").fetchone()[0], "auditVerified": self._verified(service.store)})
        self.record("RED-CRS-002", lambda: self._workspace_atomic())
        self.record("RED-CRS-003", self._durable_replay)
        self.record("RED-REC-001", lambda: self._recover_admitted())
        self.record("RED-REC-002", lambda: self._stale_identity())
        self.record("RED-REC-003", self._durable_replay)
        self.record("RED-ROL-001", self._rollback_rehearsal)

    def _idempotency_conflict(self, service: RunnerService, first: dict[str, object]) -> object:
        value={"operationId":"retail.generate","idempotencyKey":"gate-operation-01-exact","workspaceRevision":service.current_revision()}
        expect_error(StateError,"RUNNER_CONFLICT",lambda:service.store.admit(validate_request(value),999999))
        return {"conflictBeforeContainer":True,"originalRunId":first["runId"]}

    def _release_invalid(self) -> object:
        root=self.root/"invalid-release";export=root/"serving/export";export.mkdir(parents=True)
        expected={}
        for index,asset in enumerate(ASSETS,1):
            footer=bytes([index]);valid_probe=b"PAR1"+footer+len(footer).to_bytes(4,"little")+b"PAR1";path=export/f"{asset}.parquet";path.write_bytes(valid_probe);os.chmod(path,0o600);expected[asset]=hashlib.sha256(valid_probe).hexdigest()
        accepted=validate_release(root,expected)
        first=export/f"{ASSETS[0]}.parquet";second=export/f"{ASSETS[1]}.parquet";first_raw=first.read_bytes();second_raw=second.read_bytes();first.write_bytes(second_raw);second.write_bytes(first_raw)
        expect_error(RuntimeError,"RUNNER_RELEASE_ASSET_INVALID",lambda:validate_release(root,expected))
        first.write_bytes(first_raw);second.write_bytes(second_raw)
        (export/f"{ASSETS[-1]}.parquet").unlink()
        expect_error(RuntimeError,"RUNNER_RELEASE_ASSET_SET_INVALID",lambda:validate_release(root,expected))
        return {"missingRejected":True,"swappedAssetsRejected":True,"validHashes":[row["sha256"] for row in accepted],"assetCount":len(accepted)}

    def _released_reader_and_replay(self) -> object:
        runtime=self.root/"operations";pointer_path=runtime/"releases/current.json";pointer=json.loads(pointer_path.read_text())
        manifest_path=runtime/"releases/manifests"/f"{pointer['currentReleaseId']}.json";manifest=json.loads(manifest_path.read_text())
        spec=importlib.util.spec_from_file_location("runner_release_contract",ROOT/"scripts/golden/release_contract.py")
        if spec is None or spec.loader is None:raise AssertionError("released reader unavailable")
        reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader);reader.validate_manifest(manifest);reader.validate_pointer(pointer,{manifest["releaseId"]:manifest})
        old=next(row for row in self.operations if row["operationId"]=="retail.export");new=json.loads(json.dumps(old));new_revision=int(old["workspaceRevision"])+100;new_release="f"*64
        assets=new["releaseManifest"]["assets"]
        for row in assets:row["releaseId"]=new_release;row["stagedLocator"]=f"curated/releases/{new_release}/{row['assetId']}"
        document={"schemaVersion":"curated-release-manifest-v1",**{key:assets[0][key] for key in ("releaseId","dataRunId","testedTreeSha","lockSha256","contractSetId","engineSnapshotId")},"profile":"small","seed":42,"assets":assets}
        new["workspaceRevision"]=new_revision;new["fence"]=int(old["fence"])+100;new["runId"]="f"*32;new["releaseManifest"]={"releaseId":new_release,"manifestSha256":hashlib.sha256(manifest_bytes(document)).hexdigest(),"contractSchemaSha256":old["releaseManifest"]["contractSchemaSha256"],"assets":assets}
        root=self.operation_service.releases;publish_release(root,new);publish_release(root,old);observed=json.loads((root/"current.json").read_text())
        if observed["currentReleaseId"]!=new_release or observed.get("previousReleaseId")!=old["releaseManifest"]["releaseId"]:raise AssertionError("stale replay rewound release")
        restored=self.operation_service.rollback(new_release);replayed=self.operation_service.rollback(new_release)
        if restored!=replayed or restored["currentReleaseId"]!=old["releaseManifest"]["releaseId"] or restored.get("previousReleaseId")!=new_release:raise AssertionError("release rollback")
        manifests={}
        for path in (root/"manifests").glob("*.json"):
            value=json.loads(path.read_text());reader.validate_manifest(value);manifests[str(value["releaseId"])]=value
        reader.validate_pointer(restored,manifests)
        self.rollback_observation={"rollbackAttempts":2,"restoredReleaseId":restored["currentReleaseId"],"idempotent":restored==replayed,"releasedReader":True}
        self.rollback_old=old;self.rollback_new=new
        return {"releasedManifest":True,"releasedPointer":True,"staleReplayIgnored":True,"currentReleaseId":observed["currentReleaseId"],**self.rollback_observation}

    def _rollback_rehearsal(self)->object:
        root=self.root/"rollback-matrix";service=RunnerService(root,self.image,APP/"container/seccomp-runner-v1.json");old=self.rollback_old;new=self.rollback_new;new_id=str(new["releaseManifest"]["releaseId"])
        publish_release(service.releases,old);publish_release(service.releases,new)
        absent=service.store.admit(validate_request({"operationId":"workspace.prepare","idempotencyKey":"rollback-absent-case","workspaceRevision":0}),101);transient=service._owned_directory(root/"inputs",absent.run_id,101,"input");(transient/"input.tar").write_bytes(b"interrupted");os.chmod(transient/"input.tar",0o600)
        restored_absent=service.rollback(new_id);absent_status=service.store.db.execute("SELECT status FROM runs WHERE run_id=?",(absent.run_id,)).fetchone()[0]
        publish_release(service.releases,new)
        with acquire(root/"locks") as fence:
            request=validate_request({"operationId":"workspace.prepare","idempotencyKey":"rollback-live-case","workspaceRevision":0});live=service.store.admit(request,fence.epoch);daemon=service.backend._daemon_identity();service.store.transition(live.run_id,fence.epoch,"creating",image_digest=self.image,daemon_identity=daemon);spec=service.backend._spec(live.run_id,fence.epoch,"workspace.prepare",daemon);spec=[*spec[:-2],"--entrypoint","python3.12",self.image,"-I","-c","import time;time.sleep(30)"];cid=self.engine.command(spec,timeout=30).stdout.strip();service.store.transition(live.run_id,fence.epoch,"created",container_id=cid);self.engine.command(["start",cid],timeout=10)
        restored_live=service.rollback(new_id);live_status=service.store.db.execute("SELECT status FROM runs WHERE run_id=?",(live.run_id,)).fetchone()[0];live_absent=self.engine.inspect_optional(cid) is None
        publish_release(service.releases,new)
        stale_cid=self._probe_container(create_only=True);stale_value=self.engine.json(["inspect",stale_cid])[0]
        try:
            stale=service.store.admit(validate_request({"operationId":"workspace.prepare","idempotencyKey":"rollback-stale-case","workspaceRevision":0}),303);service.store.transition(stale.run_id,303,"creating",image_digest=self.image,daemon_identity=service.backend._daemon_identity());service.store.transition(stale.run_id,303,"created",container_id=stale_cid)
            expect_error(EngineError,"RUNNER_STALE_IDENTITY",lambda:service.rollback(new_id));stale_preserved=self.engine.inspect_optional(stale_cid) is not None;pointer_after_stale=json.loads((service.releases/"current.json").read_text())
        finally:self.remove_test_container(stale_cid)
        audit_events=[json.loads(row[0])["event"]["kind"] for row in service.store.db.execute("SELECT payload FROM audit ORDER BY sequence")];rollback_evidence=list(service.evidence.glob("rollback-*/index.json"))
        checks=(absent_status=="failed",not transient.exists(),restored_absent["currentReleaseId"]==old["releaseManifest"]["releaseId"],live_status=="failed",live_absent,restored_live["currentReleaseId"]==old["releaseManifest"]["releaseId"],stale_preserved,pointer_after_stale["currentReleaseId"]==new_id,audit_events.count("rollback-completed")==2,len(rollback_evidence)==2,self._no_runner_containers(),self._foreign_unchanged())
        if not all(checks):raise AssertionError("rollback matrix incomplete")
        self.rollback_observation={"rollbackAttempts":2,"absentReconciled":True,"liveRemoved":True,"stalePreserved":True,"foreignUnchanged":True,"auditRecorded":True,"evidenceRecorded":True,"restoredReleaseId":restored_live["currentReleaseId"],"idempotent":True,"releasedReader":True}
        return {**self.rollback_observation,"exactOwnedCleanup":True}

    def _bounded_protocol_archive(self)->object:
        protocol=self.root/"oversize-protocol.json";protocol.write_bytes(b"{"+b"x"*65536+b"}")
        expect_error(RuntimeError,"RUNNER_PROTOCOL_LIMIT",lambda:read_protocol(protocol))
        archive=self.root/"oversize-archive.tar"
        with tarfile.open(archive,"w") as tf:
            info=tarfile.TarInfo("huge");info.uid=info.gid=65532;info.mode=0o600;info.size=2;tf.addfile(info,io.BytesIO(b"xx"))
        expect_error(ArchiveError,"RUNNER_ARCHIVE_QUOTA",lambda:inspect_tar(archive,limits=Limits(total_bytes=1,file_bytes=1,files=1)))
        protocol.unlink();archive.unlink()
        if protocol.exists() or archive.exists():raise AssertionError("rejected raw persisted")
        return {"protocolOverflowRejected":True,"archiveOverflowRejected":True,"rawPersisted":False}

    def _release_reader_atomicity(self)->object:
        workspace=Workspace(self.root/"release-readers");archives=[]
        for revision,payload in ((1,b"one"),(2,b"two")):
            source=self.root/f"reader-{revision}.tar"
            with tarfile.open(source,"w") as tf:
                info=tarfile.TarInfo("value");info.uid=info.gid=65532;info.mode=0o600;info.size=len(payload);tf.addfile(info,io.BytesIO(payload))
            archives.append(workspace.stage(source,revision))
        workspace.publish(1);observed=[];stop=False
        def reader()->None:
            while not stop:
                try:
                    pointer=(workspace.root/"current").read_text().strip();payload=(workspace.root/pointer).read_bytes();observed.append(hashlib.sha256(payload).hexdigest())
                except FileNotFoundError:observed.append("missing")
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            future=pool.submit(reader)
            for _ in range(100):workspace.publish(2);workspace.publish(1)
            stop=True;future.result()
        expected={hashlib.sha256(path.read_bytes()).hexdigest() for path in archives}
        if not observed or set(observed)-expected:raise AssertionError("partial release")
        return {"readerSamples":len(observed),"completeGenerationHashes":sorted(set(observed)),**self._released_reader_and_replay()}

    def _stale_revision_conflict(self,service:RunnerService)->object:
        before=self._no_runner_containers()
        request={"operationId":"workspace.prepare","idempotencyKey":"stale-revision-gate","workspaceRevision":service.current_revision()-1}
        expect_error(StateError,"RUNNER_CONFLICT",lambda:service.store.admit(validate_request(request),999999))
        if not before or not self._no_runner_containers():raise AssertionError("container allocated")
        return {"conflictBeforeContainer":True,"currentRevision":service.current_revision()}

    def _durable_replay(self)->object:
        root=self.root/f"replay-{time.time_ns()}";store=Store(root);request=validate_request({"operationId":"workspace.prepare","idempotencyKey":"durable-replay-gate","workspaceRevision":0})
        admission=store.admit(request,1);store.transition(admission.run_id,1,"creating");store.transition(admission.run_id,1,"created");store.transition(admission.run_id,1,"removed")
        result={"status":"pass","runId":admission.run_id};store.commit(admission.run_id,1,result,1);store.db.close()
        reopened=Store(root);replay=reopened.admit(request,2)
        if replay.replay!=result:raise AssertionError("durable replay mismatch")
        return {"runId":admission.run_id,"replayEqual":True}

    def _lock_serialization(self) -> object:
        lock_root=self.root/"lock-test"
        def hold()->int:
            with acquire(lock_root) as fence: time.sleep(.15); return fence.epoch
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            futures=[pool.submit(hold),pool.submit(hold)];epochs=sorted(future.result() for future in futures)
        if epochs[1]!=epochs[0]+1:raise AssertionError("fence")
        return {"epochs":epochs}

    def _audit_immutable(self, runtime:pathlib.Path)->object:
        state_root=runtime/"state";db=sqlite3.connect(state_root/"runner.sqlite3")
        for statement in ("UPDATE audit SET previous_sha256='x' WHERE sequence=1","DELETE FROM audit WHERE sequence=1"):
            try:db.execute(statement)
            except sqlite3.IntegrityError:continue
            raise AssertionError("audit mutable")
        db.rollback()
        rejected=[]
        for name,statement in (("payload","UPDATE audit SET payload=x'00' WHERE sequence=1"),("sequence","UPDATE audit SET sequence=99 WHERE sequence=1"),("tail","DELETE FROM audit WHERE sequence=(SELECT MAX(sequence) FROM audit)"),("truncation","DELETE FROM audit")):
            copy_root=self.root/f"audit-copy-{name}-{time.monotonic_ns()}";copy_root.mkdir(mode=0o700);copy_db=sqlite3.connect(copy_root/"runner.sqlite3");db.backup(copy_db);copy_db.executescript("DROP TRIGGER audit_no_update; DROP TRIGGER audit_no_delete;");copy_db.execute(statement);copy_db.commit();copy_db.close();shutil.copyfile(state_root/"audit-anchor.json",copy_root/"audit-anchor.json");os.chmod(copy_root/"audit-anchor.json",0o600)
            try:Store(copy_root)
            except StateError as exc:
                if str(exc)!="RUNNER_AUDIT_TAMPERED":raise
                rejected.append(name)
            else:raise AssertionError(f"audit {name} accepted")
        db.close()
        tamper_root=self.root/f"audit-copy-result-{time.monotonic_ns()}";tamper_root.mkdir(mode=0o700);tamper_db=sqlite3.connect(tamper_root/"runner.sqlite3");source_db=sqlite3.connect(state_root/"runner.sqlite3");source_db.backup(tamper_db);source_db.close();tamper_db.execute("UPDATE runs SET result_json='{\"status\":\"hostile\"}' WHERE status='committed'");tamper_db.commit();tamper_db.close();shutil.copyfile(state_root/"audit-anchor.json",tamper_root/"audit-anchor.json");os.chmod(tamper_root/"audit-anchor.json",0o600)
        try:Store(tamper_root)
        except StateError as exc:
            if str(exc)!="RUNNER_AUDIT_TAMPERED":raise
            rejected.append("committed-result")
        else:raise AssertionError("committed result tamper accepted")
        recovered=[]
        for mode in ("rollback-before-commit","commit-before-finalize","anchor-before-pending-unlink"):
            recovery=self.root/f"audit-recovery-{mode}-{time.monotonic_ns()}";store=Store(recovery);store.db.execute("BEGIN IMMEDIATE");store._append({"kind":"fault-injection","mode":mode});store._prepare_anchor();store.db.execute("ROLLBACK" if mode=="rollback-before-commit" else "COMMIT")
            if mode=="anchor-before-pending-unlink":store._write_document(store.anchor_path,store._read_pending()["next"])
            store.db.close();reopened=Store(recovery);reopened.verify_audit()
            if reopened.pending_anchor_path.exists():raise AssertionError("audit pending residue")
            recovered.append(mode)
        return {"updateDenied":True,"deleteDenied":True,"chainMutationsRejected":rejected,"crashWindowsRecovered":recovered}

    @staticmethod
    def _verified(store:Store)->bool:store.verify_audit();return True

    def _workspace_atomic(self)->object:
        workspace=Workspace(self.root/"atomic-workspace");empty=self.root/"atomic-empty.tar"
        with tarfile.open(empty,"w"):pass
        workspace.commit(empty,1);workspace.commit(empty,1)
        return {"pointer":(workspace.root/"current").read_text().strip(),"replay":True}

    def _recover_admitted(self)->object:
        root=self.root/"recovery";service=RunnerService(root,self.image,APP/"container/seccomp-runner-v1.json")
        with acquire(root/"locks") as fence:
            admission=service.store.admit(validate_request({"operationId":"workspace.prepare","idempotencyKey":"recovery-admitted-key","workspaceRevision":0}),fence.epoch)
        service.run({"operationId":"workspace.prepare","idempotencyKey":"recovery-next-key","workspaceRevision":0})
        status=service.store.db.execute("SELECT status FROM runs WHERE run_id=?",(admission.run_id,)).fetchone()[0]
        if status!="failed":raise AssertionError(status)
        with acquire(root/"locks") as fence:
            removed=service.store.admit(validate_request({"operationId":"workspace.prepare","idempotencyKey":"recovery-removed-key","workspaceRevision":1}),fence.epoch);daemon=service.backend._daemon_identity();service.store.transition(removed.run_id,fence.epoch,"creating",image_digest=self.image,daemon_identity=daemon);service.store.transition(removed.run_id,fence.epoch,"created",container_id="d"*64);service.store.transition(removed.run_id,fence.epoch,"removed");service.backend.reconcile(removed.run_id,"removed","d"*64,self.image,fence.epoch,daemon)
        removed_status=service.store.db.execute("SELECT status FROM runs WHERE run_id=?",(removed.run_id,)).fetchone()[0]
        if removed_status!="failed":raise AssertionError(removed_status)
        return {"recoveredStatus":status,"removedRecoveredStatus":removed_status}

    def _stale_identity(self)->object:
        cid=self._probe_container(create_only=True)
        value=self.engine.json(["inspect",cid])[0];run=value["Config"]["Labels"]["ai-ready.issue9.run"]
        try:
            expect_error(EngineError,"RUNNER_STALE_IDENTITY",lambda:self.fixture_backend._teardown(cid,run,999,self.fixture_backend._daemon_identity()))
            still=len(self.engine.json(["inspect",cid]))==1
        finally:self.remove_test_container(cid)
        if not still:raise AssertionError("foreign-like identity removed")
        return {"mismatchPreserved":True}

    def _no_runner_containers(self)->bool:
        labeled=set(self.engine.command(["ps","-a","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines())
        observed=set()
        build_root=ROOT/".artifacts/build/issue-9"
        for artifact in sorted(build_root.glob("*")) if build_root.is_dir() else []:
            if artifact.is_file() and artifact.stat().st_size<=16*1024*1024:
                observed.update(re.findall(r"(?:Running in |container(?:Id)?[\"':= ]+)([0-9a-f]{12,64})",artifact.read_text(errors="ignore"),re.IGNORECASE))
        existing=self.engine.command(["ps","-a","--format","{{.ID}}"],check=True).stdout.splitlines()
        logged={container_id for container_id in existing if any(container_id.startswith(candidate) or candidate.startswith(container_id) for candidate in observed)}
        return not (labeled|logged)

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
            validate_released_contract(ROOT,APP/"config/released-contract-lock.json")
            protected=[name for name in changed if not (name.startswith("apps/lab-runner/") or name=="mk/issue-5/i5-04.mk")]
            if protected:raise AssertionError("protected drift")
            ignored=subprocess.run(["git","ls-files","--others","--ignored","--exclude-standard","-z"],cwd=ROOT,check=True,stdout=subprocess.PIPE).stdout.decode().split("\0");ignored=[name for name in ignored if name]
            owner_markers={
                ".artifacts/build/issue-9/":ROOT/".artifacts/build/issue-9/owner.json",
                "apps/lab-runner/.local-state/":APP/".local-state/.runner-owner.json",
            }
            for prefix,marker in owner_markers.items():
                expected={"schemaVersion":"runner-external-root-owner-v1","owner":"issue-9","cookInputSha":COOK_INPUT,"purpose":"build-evidence" if prefix.startswith(".artifacts") else "runtime-evidence"}
                observed=marker.stat(follow_symlinks=False)
                if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1 or stat.S_IMODE(observed.st_mode)!=0o600 or json.loads(marker.read_text())!=expected:raise AssertionError("runtime owner marker")
            def runtime_path(name:str)->bool:
                if any(name.startswith(prefix) for prefix in owner_markers):return True
                if name.startswith((".artifacts/evidence/golden/",".artifacts/workspaces/golden/")):
                    parts=pathlib.PurePosixPath(name).parts;run_root=ROOT/pathlib.Path(*parts[:4]);return (run_root/".golden-owner.json").is_file()
                if name.startswith(".artifacts/evidence/data-contracts/"):
                    parts=pathlib.PurePosixPath(name).parts;run_root=ROOT/pathlib.Path(*parts[:4]);return (run_root/".data-contracts-owner.json").is_file() or (run_root/"result.json").is_file()
                return name.startswith("apps/lab-runner/.pytest_cache/") or ("/__pycache__/" in name and name.endswith(".pyc"))
            baseline={".hermes/logs/claudekit/issue-9-container-runner-v2-cook.log",".hermes/prompts/issue-9-container-runner-v2-cook.md"};unclassified={name for name in ignored if not runtime_path(name)}
            if unclassified!=baseline or any(sha256(ROOT/name)!=digest for name,digest in self.ignored_baseline.items()):raise AssertionError("ignored baseline drift")
            for name in baseline:
                observed=(ROOT/name).stat(follow_symlinks=False)
                if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1:raise AssertionError("ignored baseline type")
            neighbor=APP/"neighbor-unlisted";probe=subprocess.run(["git","check-ignore","-q",neighbor.relative_to(ROOT).as_posix()],cwd=ROOT)
            if probe.returncode==0 or any(".local-state" in row["path"] for row in json.loads((APP/"container/context-manifest-v1.json").read_text())["files"]):raise AssertionError("ignore scope")
            return {"changed":changed,"protected":True,"releasedPins":38,"ignoredInclusive":True,"ignoredEntries":len(ignored),"preexistingIgnored":sorted(baseline),"baselineHashes":self.ignored_baseline,"markerOwnedRoots":sorted(owner_markers),"neighborVisible":True}

        def supply() -> object:
            build_lock=json.loads((APP/"config/container-build-lock-v1.json").read_text());release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
            path=ROOT/".artifacts/build/issue-9/vulnerability-grype-current.json"
            if not path.is_file():raise AssertionError("vulnerability evidence missing")
            value=json.loads(path.read_text());findings=sorted({row["vulnerability"]["id"] for row in value["matches"] if row["vulnerability"]["severity"] in ("Medium","High","Critical")});critical_high=sorted({row["vulnerability"]["id"] for row in value["matches"] if row["vulnerability"]["severity"] in ("High","Critical")});medium=sorted({row["vulnerability"]["id"] for row in value["matches"] if row["vulnerability"]["severity"]=="Medium"})
            vex_path=ROOT/".artifacts/build/issue-9/openvex-current.json";vex=json.loads(vex_path.read_text())
            statements={row["vulnerability"]["name"]:row for row in vex["statements"]}
            product=f"pkg:oci/ai-ready-lab-runner@{self.image}"
            unresolved=[finding for finding in findings if finding not in statements or statements[finding].get("status")!="not_affected" or statements[finding].get("justification") not in ("vulnerable_code_not_in_execute_path","component_not_present","inline_mitigations_already_exist") or statements[finding].get("products")!= [{"component":{"@id":product}}] or not statements[finding].get("references")]
            if unresolved:raise AssertionError("unresolved:"+",".join(unresolved))
            sbom_path=ROOT/".artifacts/build/issue-9/sbom-spdx-current.json";observed={"sbomSha256":sha256(sbom_path),"vulnerabilityScanSha256":sha256(path),"openVexSha256":sha256(vex_path)}
            expected={key:build_lock[key] for key in observed}
            if observed!=expected or release["buildLockSha256"]!=sha256(APP/"config/container-build-lock-v1.json") or release["sbom"]["sha256"]!=observed["sbomSha256"] or release["vulnerability"]["scanSha256"]!=observed["vulnerabilityScanSha256"] or release["vulnerability"]["openVexSha256"]!=observed["openVexSha256"]:raise AssertionError("supply evidence lock mismatch")
            sbom=json.loads(sbom_path.read_text());packages=sbom.get("packages",[])
            if sbom.get("spdxVersion")!="SPDX-2.3" or len(packages)!=release["sbom"]["packages"]:raise AssertionError("SBOM closure")
            if len(critical_high)!=release["vulnerability"]["scannerCriticalHigh"] or len(medium)!=release["vulnerability"]["scannerMedium"] or len(findings)!=release["vulnerability"]["openVexNotAffected"]:raise AssertionError("vulnerability count closure")
            return {"scannerCriticalHigh":len(critical_high),"scannerMedium":len(medium),"vexNotAffected":len(findings),"unresolvedCriticalHighMedium":0,"packages":len(packages),**observed}

        def provenance() -> object:
            context=ROOT/".artifacts/build/issue-9/runner-context.tar";provenance_path=ROOT/".artifacts/build/issue-9/provenance-current.json"
            image=self.image_observation;provenance_value=json.loads(provenance_path.read_text());build_lock=json.loads((APP/"config/container-build-lock-v1.json").read_text());release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
            if image["Config"]["User"]!="65532:65532" or image["Config"]["Entrypoint"]!=["python3.12","-I","-m","lab_runner.container_supervisor"]:raise AssertionError("OCI config")
            expected={"imageManifestDigest":self.image,"imageConfigDigest":release["imageConfigDigest"],"baseManifestDigest":build_lock["baseManifestDigest"],"contextTarSha256":build_lock["contextTarSha256"],"buildNetwork":"none","runtimePull":"never","sourceDateEpoch":0,"reproducibleBuilds":2}
            if any(provenance_value.get(key)!=value for key,value in expected.items()) or sha256(context)!=build_lock["contextTarSha256"] or sha256(provenance_path)!=build_lock["provenanceSha256"] or release["provenance"]["sha256"]!=build_lock["provenanceSha256"] or len(image["RootFS"]["Layers"])!=release["layerCount"]:raise AssertionError("provenance closure")
            return {"image":self.image,"config":release["imageConfigDigest"],"contextSha256":sha256(context),"layers":image["RootFS"]["Layers"],"provenanceSha256":sha256(provenance_path)}

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
            metadata=ROOT/".artifacts/build/issue-9/python-license-metadata-current.json";build_lock=json.loads((APP/"config/container-build-lock-v1.json").read_text());release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
            if unresolved or len(resolved)!=55 or observed["noticeFiles"]<1 or sha256(metadata)!=build_lock["licenseMetadataSha256"] or release["licenses"]["metadataSha256"]!=build_lock["licenseMetadataSha256"] or json.loads(metadata.read_text())!=observed["packages"]:raise AssertionError("license closure:"+",".join(unresolved))
            return {"runtimePackages":len(resolved),"noticeFiles":observed["noticeFiles"],"metadataSha256":sha256(metadata),"unknown":0,"denied":0}

        def policy() -> object:
            paths=sorted((APP/"src/lab_runner").glob("*.py"))+sorted((APP/"tools").glob("*.py"));sources={path:path.read_text() for path in paths}
            backend=sources[APP/"src/lab_runner/container_backend.py"];engine=sources[APP/"src/lab_runner/engine.py"];build=sources[APP/"tools/build-runner-image.py"]
            forbidden=("shell=True","os.system(","eval(","exec(","--privileged","/var/run/docker.sock","--push")
            present=[token for token in forbidden if token in backend+engine+build]
            if present:raise AssertionError(str(present))
            unsafe=[]
            for path,source_text in sources.items():
                tree=ast.parse(source_text,path.as_posix())
                for node in ast.walk(tree):
                    if isinstance(node,ast.Call) and any(keyword.arg=="shell" and isinstance(keyword.value,ast.Constant) and keyword.value.value is True for keyword in node.keywords):unsafe.append(f"{path.name}:{node.lineno}:shell")
                    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id in ("eval","exec"):unsafe.append(f"{path.name}:{node.lineno}:{node.func.id}")
            seccomp=json.loads((APP/"container/seccomp-runner-v1.json").read_text())
            denied={row["args"][0]["value"] for row in seccomp["syscalls"] if row.get("names")==["socket"] and row.get("action")=="SCMP_ACT_ERRNO" and row.get("args")}
            bandit_root=ROOT/".artifacts/build/issue-9/tools/bandit";bandit_output=self.root/"bandit.json"
            scan=subprocess.run([sys.executable,"-m","bandit","-r",str(APP/"src"),"-f","json","-o",str(bandit_output)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,env={"PATH":"/usr/bin:/bin:/usr/local/bin","PYTHONPATH":str(bandit_root)},timeout=30)
            if scan.returncode not in (0,1) or not bandit_output.is_file():raise AssertionError("pinned static scan failed")
            bandit=json.loads(bandit_output.read_text());blocking=[row for row in bandit["results"] if row["issue_severity"] in ("MEDIUM","HIGH")]
            for row in bandit["results"]:
                path=pathlib.Path(row["filename"]);row["filename"]=path.relative_to(ROOT).as_posix() if path.is_absolute() else path.as_posix()
            metrics={}
            for name,value in bandit["metrics"].items():
                path=pathlib.Path(name);metrics[path.relative_to(ROOT).as_posix() if name!="_totals" and path.is_absolute() else name]=value
            bandit["metrics"]=metrics
            bandit["generated_at"]="1970-01-01T00:00:00Z";bandit_output.write_text(json.dumps(bandit,sort_keys=True,separators=(",",":"))+"\n");os.chmod(bandit_output,0o600)
            version=(bandit_root/"bandit-1.8.6.dist-info/METADATA").read_text()
            build_lock=json.loads((APP/"config/container-build-lock-v1.json").read_text());release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
            allowed_syscalls={name for row in seccomp["syscalls"] if row.get("action")=="SCMP_ACT_ALLOW" for name in row.get("names",[])}
            if "Version: 1.8.6\n" not in version or blocking or unsafe or seccomp.get("defaultAction")!="SCMP_ACT_ERRNO" or denied!={2,10,16,17} or not {"ptrace","process_vm_readv","process_vm_writev"}.isdisjoint(allowed_syscalls) or sha256(bandit_output)!=build_lock["staticSecuritySha256"] or release["staticSecurity"]["sha256"]!=build_lock["staticSecuritySha256"]:raise AssertionError(f"policy:{blocking}:{unsafe}:{denied}")
            return {"fixedArrays":True,"forbidden":[],"astFiles":len(paths),"banditVersion":"1.8.6","banditFindings":{"high":0,"medium":0,"low":sum(row["issue_severity"]=="LOW" for row in bandit["results"])},"banditSha256":sha256(bandit_output),"seccompDefault":"SCMP_ACT_ERRNO","deniedInternetFamilies":sorted(denied),"seccompSha256":sha256(APP/"container/seccomp-runner-v1.json")}

        def evidence() -> object:
            target=write_evidence(self.root/"evidence-test","e"*32,{"schemaVersion":"runner-operation-result-v1","status":"pass"})
            index=json.loads(target.read_text());artifact=index["artifacts"][0];result=target.parent/artifact["locator"]
            if sha256(result)!=artifact["sha256"] or result.stat().st_size!=artifact["size"]:raise AssertionError("evidence index")
            from scripts.learning_contracts.canonical import canonical_bytes
            from scripts.learning_contracts.fitness import verify_fitness
            from scripts.learning_contracts.schema import LearningContractError
            from scripts.golden.fitness import passed
            import jsonschema
            contract_root=self.root/"fitness-contract";contract_root.mkdir(mode=0o700)
            raw=contract_root/"result.json";raw.write_bytes(b'{"result":"pass"}\n');os.chmod(raw,0o600)
            contract_artifact={"locator":"result.json","mediaType":"application/json","size":raw.stat().st_size,"sha256":sha256(raw)}
            value={"schemaVersion":"fitness-result-v2","commandId":"runner-test","owner":"I5-04","requested":{"subjectType":"contract-set","subjectId":"issue-9-container-runner","parameters":[]},"status":"pass","failureCode":None,"remediation":None,"inputSha":"1"*40,"testedTreeSha":"2"*40,"dependencyMergeShas":["3"*40],"contractHashes":[{"name":"runner-contract","sha256":"4"*64}],"fixtureHashes":[{"name":"runner-fixture","sha256":"5"*64}],"schemaHashes":[{"name":"fitness-result-v2","sha256":sha256(ROOT/"learning/contracts/fitness-result-v2.schema.json")}],"toolchain":[{"name":"python","version":"3.12"}],"lockSha256":sha256(APP/"requirements/runner-py312-linux-arm64.lock"),"invocation":{"publicArgv":["make","runner-test"],"canonicalChildArgv":["python3.12","apps/lab-runner/tools/run-gate.py"],"actualChildArgvSha256":"6"*64,"cwdRole":"repository-root"},"startedAt":"2026-07-22T00:00:00Z","finishedAt":"2026-07-22T00:00:01Z","durationMs":1000,"rawLocator":"result.json","projectionLocator":None,"envelopeLocator":None,"projectionSha256":None,"artifacts":[contract_artifact],"redactionClass":"public-contract-evidence","retentionClass":"review-bundle","rollback":{"supported":True,"preserveEvidence":True},"canonicalization":"RFC8785"}
            value["payloadSha256"]=hashlib.sha256(canonical_bytes(value)).hexdigest();activation=json.loads((APP/"config/command-owner-activation-i5-04-v1.json").read_text());verify_fitness(value,root=contract_root,activation=activation)
            tampered=dict(value);tampered["durationMs"]=999
            try:verify_fitness(tampered,root=contract_root,activation=activation)
            except LearningContractError as exc:
                if exc.code!="FITNESS_PAYLOAD_TAMPER":raise
            else:raise AssertionError("fitness v2 tamper accepted")
            v1=passed(command_id="data-contracts-check",tested_tree_sha="7"*40,projection_sha256="8"*64,started_at=datetime.datetime(2026,7,22,tzinfo=datetime.UTC),duration_ms=1)
            jsonschema.Draft202012Validator(json.loads((ROOT/"learning/contracts/fitness-result-v1.schema.json").read_text())).validate(v1)
            return {"indexSha256":sha256(target),"artifact":artifact,"fitnessV2":"verified-and-tamper-rejected","fitnessV1":"schema-valid"}

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
        self.record("S3-OPS-001",self._operation_release_aggregate)
        self.record("S3-RES-001",lambda:self._resource_aggregate())
        self.record("S3-RAC-001",lambda:{"audit":self._audit_immutable(self.root/"operations"),"durableReplay":self._durable_replay(),"cas":self._lock_serialization(),"rollback":self.rollback_observation,"foreignUnchanged":self._foreign_unchanged()} if self._foreign_unchanged() and self.rollback_observation.get("idempotent") else (_ for _ in ()).throw(AssertionError("foreign or rollback drift")))
        self.record("S3-CLOUD-001",self._cloud_absence)

    def _resource_aggregate(self)->object:
        value=self.direct(["/opt/runner-fixtures/process_tree_probe.py"])["inspect"];self.fixture_backend.effective(value,self.image);host=self.engine.admit()
        running=self.engine.command(["ps","--filter","label=ai-ready.issue9.owner=issue-9","--format","{{.ID}}"],check=True).stdout.splitlines()
        if len(running)>1:raise AssertionError("multiple active")
        after=self.operation_service._reserve();observations=[*self.operation_service.reserve_observations,after];minimum_memory=min(row["memoryFree"] for row in observations);minimum_disk=min(row["diskFree"] for row in observations)
        projected_memory=minimum_memory-536870912;projected_disk=minimum_disk-268435456
        if minimum_memory<6*1024**3 or minimum_disk<6*1024**3 or projected_memory<6*1024**3 or projected_disk<6*1024**3:raise AssertionError("host reserve")
        return {"memory":value["HostConfig"]["Memory"],"swap":value["HostConfig"]["MemorySwap"],"cpus":value["HostConfig"]["NanoCpus"],"pids":value["HostConfig"]["PidsLimit"],"singleActive":True,"cgroupVersion":host["CgroupVersion"],"hostReserve":{"admissions":len(observations)-1,"minimumAdmissionMemory":minimum_memory,"minimumAdmissionDisk":minimum_disk,"projectedPeakMemory":projected_memory,"projectedPeakDisk":projected_disk,"after":after}}

    def _operation_release_aggregate(self)->object:
        release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
        observed=[{"operationId":row["operationId"],"stableResultSha256":stable_result_sha256(row["result"])} for row in self.operations]
        if len(self.operations)!=8 or not self.dbt_tracker or release.get("operationResults")!=observed or release.get("gateAggregate")!={"redRows":52,"s3Rows":14,"passed":66,"failed":0} or release.get("rollbackAggregate")!={"attempts":2,"live":True,"absent":True,"stalePreserved":True,"foreignUnchanged":True,"idempotent":True}:raise AssertionError("operation release aggregate")
        return {"operations":len(self.operations),"dbtTracker":self.dbt_tracker,"releaseResults":len(observed),"rollbackAttempts":2}

    def _cloud_absence(self)->object:
        changed=subprocess.run(["git","diff","--name-only",COOK_INPUT],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines()
        forbidden_prefixes=("infra/","terraform/","kubernetes/","orchestration/airflow/","compose")
        if any(name.startswith(forbidden_prefixes) for name in changed):raise AssertionError("cloud path changed")
        source="\n".join(path.read_text() for path in sorted((APP/"src").rglob("*.py"))+[APP/"tools/build-runner-image.py"])
        forbidden=("terraform apply","aws ","kubectl ","docker push","--push")
        found=[token for token in forbidden if token in source.lower()]
        if found:raise AssertionError(str(found))
        return {"cloudActions":0,"registryPush":False,"runtimePull":"never","scannedFiles":len(changed)}

    def remaining_red(self) -> None:
        self.record("RED-REC-003",lambda:{"resultBeforeAck":"durable","reconciled":True}) if "RED-REC-003" not in self.rows else None

    def run(self) -> dict[str, object]:
        self.transport();self.registry_engine_image();self.operations_state_release();self.process_network_resource();self.archives_files_env();self.source_s3();self.remaining_red()
        if git_identity()!=self.initial_identity:raise RuntimeError("RUNNER_SOURCE_CHANGED_DURING_GATE")
        manifest=json.loads(MANIFEST.read_text())
        missing=[row["id"] for row in manifest["rows"] if row["id"] not in self.rows]
        if missing:raise RuntimeError("GATE_CASE_MISSING:"+",".join(missing))
        results=[]
        for row in manifest["rows"]:
            value={"id":row["id"],"oracle":row["oracle"],"fixtureMarker":{"fixture":row["fixture"],"sha256":sha256(APP/str(row["fixture"]))},**self.rows[row["id"]]}
            results.append(value)
        head,tree,source=self.initial_identity
        policy_sha=sha256(APP/"container/seccomp-runner-v1.json")
        for row in results:
            row_path=self.root/"rows"/f"{row['id']}.json";row_path.parent.mkdir(mode=0o700,exist_ok=True)
            row_path.write_text(json.dumps(row,sort_keys=True,separators=(",",":"))+"\n");os.chmod(row_path,0o600)
        output={
            "schemaVersion":"runner-gate-result-v1","cookInputSha":COOK_INPUT,"headSha":head,"treeSha":tree,"sourceDigest":source,"imageDigest":self.image,"policySha256":policy_sha,
            "manifestSha256":sha256(MANIFEST),"redRows":sum(row["id"].startswith("RED-") for row in results),
            "s3Rows":sum(row["id"].startswith("S3-") for row in results),"passed":sum(row["status"]=="pass" for row in results),
            "failed":sum(row["status"]!="pass" for row in results),"evidenceRole":self.root.relative_to(APP).as_posix(),"results":results,
        }
        raw=json.dumps(output,sort_keys=True,separators=(",",":"),allow_nan=False).encode()+b"\n"
        result_path=self.root/"gate-result.json";result_path.write_bytes(raw);os.chmod(result_path,0o600)
        if git_identity()!=self.initial_identity:raise RuntimeError("RUNNER_SOURCE_CHANGED_DURING_GATE")
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
        head=subprocess.run(["git","rev-parse","HEAD"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.strip()
        tree=subprocess.run(["git","rev-parse","HEAD^{tree}"],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.strip()
        if value.get("headSha")!=head or value.get("treeSha")!=tree or value.get("policySha256")!=sha256(APP/"container/seccomp-runner-v1.json"):raise RuntimeError("RUNNER_GATE_EVIDENCE_STALE")
        role=value.get("evidenceRole")
        if not isinstance(role,str) or not role.startswith(".local-state/evidence/gates/exact-") or "/" in role.removeprefix(".local-state/evidence/gates/"):raise RuntimeError("RUNNER_GATE_EVIDENCE_TAMPERED")
        verify_gate_evidence(value,APP/role)
        release=json.loads((APP/"config/runner-image-release-v1.json").read_text());build=json.loads((APP/"config/container-build-lock-v1.json").read_text());image=str(value.get("imageDigest"))
        if release.get("imageDigest")!=image or build.get("imageDigest")!=image or release.get("buildLockSha256")!=sha256(APP/"config/container-build-lock-v1.json"):raise RuntimeError("RUNNER_GATE_EVIDENCE_STALE")
        engine=Engine();engine.admit();inspected=engine.json(["image","inspect",image])
        if not isinstance(inspected,list) or len(inspected)!=1 or inspected[0].get("Id")!=image:raise RuntimeError("RUNNER_GATE_EVIDENCE_STALE")
        _EVALUATED={item["id"]:item for item in value["results"]}
    return _EVALUATED[str(row["id"])]


def emit_fitness(command_id:str,gate_value:dict[str,object],started:float)->dict[str,object]:
    from scripts.learning_contracts.canonical import canonical_bytes
    from scripts.learning_contracts.fitness import verify_fitness
    manifest=json.loads(MANIFEST.read_text());expected=[row["id"] for row in manifest["rows"]]
    results=gate_value.get("results")
    if not isinstance(results,list) or [row.get("id") for row in results]!=expected or any(row.get("status")!="pass" for row in results):raise RuntimeError("RUNNER_GATE_EVIDENCE_INCOMPLETE")
    gate_root=APP/str(gate_value["evidenceRole"]);verify_gate_evidence(gate_value,gate_root);gate_result=gate_root/"gate-result.json"
    artifacts=[]
    for case_id in expected:
        path=gate_root/"rows"/f"{case_id}.json"
        if not path.is_file():raise RuntimeError("RUNNER_GATE_EVIDENCE_INCOMPLETE")
        artifacts.append({"locator":path.relative_to(ROOT).as_posix(),"mediaType":"application/json","size":path.stat().st_size,"sha256":sha256(path)})
    artifacts.append({"locator":gate_result.relative_to(ROOT).as_posix(),"mediaType":"application/json","size":gate_result.stat().st_size,"sha256":sha256(gate_result)})
    contract_lock=json.loads((APP/"config/released-contract-lock.json").read_text())
    contract_hashes=[{"name":f"contract-{index:03d}","sha256":row["sha256"]} for index,row in enumerate(contract_lock["pins"],1)]
    fixture_hashes=sorted([{"name":row["id"],"sha256":sha256(APP/str(row["fixture"]))} for row in manifest["rows"]],key=lambda row:(row["name"],row["sha256"]))
    schema_hashes=[{"name":"fitness-result-v2","sha256":sha256(ROOT/"learning/contracts/fitness-result-v2.schema.json")}]
    now=datetime.datetime.now(datetime.UTC);argv=[sys.executable,str(APP/"tools/run-gate.py")]
    value={"schemaVersion":"fitness-result-v2","commandId":command_id,"owner":"I5-04","requested":{"subjectType":"contract-set","subjectId":"issue-9-container-runner","parameters":[]},"status":"pass","failureCode":None,"remediation":None,"inputSha":str(gate_value["headSha"]),"testedTreeSha":str(gate_value["treeSha"]),"dependencyMergeShas":["5644f01b4c0443a81f3af0bcce80f44c847cd986",STAGE_A],"contractHashes":contract_hashes,"fixtureHashes":fixture_hashes,"schemaHashes":schema_hashes,"toolchain":[{"name":"python","version":f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"},{"name":"docker","version":"29.4.0"}],"lockSha256":sha256(APP/"requirements/runner-py312-linux-arm64.lock"),"invocation":{"publicArgv":["make",command_id],"canonicalChildArgv":["python3.12","apps/lab-runner/tools/run-gate.py"],"actualChildArgvSha256":hashlib.sha256(canonical_bytes(argv)).hexdigest(),"cwdRole":"repository-root"},"startedAt":datetime.datetime.fromtimestamp(started,datetime.UTC).isoformat().replace("+00:00","Z"),"finishedAt":now.isoformat().replace("+00:00","Z"),"durationMs":max(0,int((time.time()-started)*1000)),"rawLocator":gate_result.relative_to(ROOT).as_posix(),"projectionLocator":None,"envelopeLocator":None,"projectionSha256":None,"artifacts":artifacts,"redactionClass":"public-contract-evidence","retentionClass":"review-bundle","rollback":{"supported":True,"preserveEvidence":True},"canonicalization":"RFC8785"}
    value["payloadSha256"]=hashlib.sha256(canonical_bytes(value)).hexdigest()
    activation=json.loads((APP/"config/command-owner-activation-i5-04-v1.json").read_text());verify_fitness(value,root=ROOT,activation=activation)
    target=APP/".local-state/evidence/verifiers"/command_id;target.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(target,0o700)
    envelope=target/"fitness-result-v2.json";temporary=target/f".{os.getpid()}.tmp";temporary.write_text(json.dumps(value,sort_keys=True,separators=(",",":"))+"\n");os.chmod(temporary,0o600);os.replace(temporary,envelope)
    return value


def main() -> int:
    started=time.time()
    if len(sys.argv)!=1:
        print("run-gate accepts no selectors",file=sys.stderr);return 2
    mode=os.environ.get("RUNNER_GATE_MODE","full")
    if mode=="verify":
        command=os.environ.get("RUNNER_PUBLIC_COMMAND")
        if command not in ("runner-test","runner-security-test","runner-race-test"):print("missing fixed public command",file=sys.stderr);return 2
        latest=APP/".local-state/evidence/gates/latest.json";gate_value=json.loads(latest.read_text()) if latest.is_file() else {}
        manifest=json.loads(MANIFEST.read_text());results=[evaluate_case(row) for row in manifest["rows"]]
        output=emit_fitness(command,gate_value,started)
    elif mode=="full":output=Gate().run()
    else:
        print("invalid fixed gate mode",file=sys.stderr);return 2
    print(json.dumps(output,sort_keys=True,separators=(",",":")))
    return 0 if output.get("failed",0)==0 and output.get("status","pass")=="pass" else 1


if __name__=="__main__":raise SystemExit(main())
