"""Fresh-container execution with exact identity fencing and teardown."""
from __future__ import annotations
import json, os, pathlib, subprocess, time
from dataclasses import dataclass
from .archive import inspect_tar
from .container_protocol import read as read_protocol
from .engine import Engine,EngineError
from .registry import resolve
from .state import Store

IMAGE_LABEL="ai-ready.issue9.image"
OWNER_LABEL="ai-ready.issue9.owner"
RUN_LABEL="ai-ready.issue9.run"
FENCE_LABEL="ai-ready.issue9.fence"


@dataclass(frozen=True,slots=True)
class Outcome:
    protocol:dict[str,object]
    output_archive:pathlib.Path
    inspect:dict[str,object]
    container_id:str


class Backend:
    def __init__(self,engine:Engine,image_digest:str,seccomp:pathlib.Path,staging:pathlib.Path,store:Store):
        self.engine=engine;self.image=image_digest;self.seccomp=seccomp.resolve();self.staging=staging;self.store=store
        staging.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(staging,0o700)

    def _spec(self,run_id:str,fence:int,operation_id:str)->list[str]:
        resolve(operation_id)
        return ["create","--pull","never","--name",f"ai-ready-runner-{run_id}",
        "--label",f"{OWNER_LABEL}=issue-9","--label",f"{RUN_LABEL}={run_id}","--label",f"{FENCE_LABEL}={fence}","--label",f"{IMAGE_LABEL}={self.image}",
        "--init","--network","none","--read-only","--user","65532:65532","--cap-drop","ALL",
        "--security-opt","no-new-privileges:true","--security-opt",f"seccomp={self.seccomp}",
        "--pids-limit","64","--memory","536870912","--memory-swap","536870912","--cpus","2",
        "--tmpfs","/workspace:rw,nosuid,nodev,size=268435456,uid=65532,gid=65532,mode=0700",
        "--tmpfs","/tmp:rw,nosuid,nodev,size=67108864,uid=65532,gid=65532,mode=0700",
        "--tmpfs","/run:rw,nosuid,nodev,size=16777216,uid=65532,gid=65532,mode=0700",
        "--shm-size","16777216",self.image,operation_id]

    def _inspect(self,cid:str)->dict[str,object]:
        value=self.engine.json(["inspect",cid])
        if not isinstance(value,list) or len(value)!=1: raise EngineError("RUNNER_STALE_IDENTITY")
        return value[0]

    def _identity(self,value:dict[str,object],run_id:str,fence:int)->bool:
        config=value.get("Config",{});labels=config.get("Labels",{}) if isinstance(config,dict) else {}
        return labels.get(OWNER_LABEL)=="issue-9" and labels.get(RUN_LABEL)==run_id and labels.get(FENCE_LABEL)==str(fence) and labels.get(IMAGE_LABEL)==self.image and config.get("Image")==self.image

    @staticmethod
    def effective(value:dict[str,object],image_digest:str)->None:
        c=value["Config"];h=value["HostConfig"];network=value.get("NetworkSettings",{})
        tmp=h.get("Tmpfs") or {}
        checks=[
          c.get("User")=="65532:65532",h.get("ReadonlyRootfs") is True,h.get("NetworkMode")=="none",
          h.get("PidMode") in ("","private"),h.get("IpcMode") in ("private",""),h.get("Init") is True,
          h.get("Privileged") is False,h.get("PidsLimit")==64,h.get("Memory")==536870912,
          h.get("MemorySwap")==536870912,h.get("NanoCpus")==2_000_000_000,
          h.get("CapDrop")==["ALL"],not h.get("Devices"),not h.get("DeviceRequests"),
          not h.get("PortBindings"),not c.get("ExposedPorts"),c.get("Image")==image_digest,
          set(tmp)=={"/workspace","/tmp","/run"},
          all(m.get("Type")!="bind" for m in value.get("Mounts",[])),
          any(str(x).startswith("no-new-privileges") for x in h.get("SecurityOpt",[])),
        ]
        if not all(checks): raise EngineError("RUNNER_CONTAINMENT_UNAVAILABLE")

    def _copy_retry(self,source:pathlib.Path,destination:str)->None:
        for _ in range(50):
            try: self.engine.command(["cp",str(source),destination],timeout=5);return
            except EngineError: time.sleep(.05)
        raise EngineError("RUNNER_INPUT_INVALID")

    def execute(self,run_id:str,fence:int,operation_id:str,input_archive:pathlib.Path)->Outcome:
        self.engine.admit();work=self.staging/run_id;work.mkdir(mode=0o700)
        marker=work/"input.ready";marker.write_bytes(b"ready\n");os.chmod(marker,0o600)
        cid="";inspected={}
        try:
            cid=self.engine.command(self._spec(run_id,fence,operation_id),timeout=30).stdout.strip()
            if len(cid)<12: raise EngineError("RUNNER_CONTAINER_LOST")
            self.store.transition(run_id,fence,"created",container_id=cid,image_digest=self.image)
            inspected=self._inspect(cid)
            if not self._identity(inspected,run_id,fence): raise EngineError("RUNNER_STALE_IDENTITY")
            self.effective(inspected,self.image)
            self.engine.command(["start",cid]);self.store.transition(run_id,fence,"started-awaiting-input")
            self._copy_retry(input_archive,f"{cid}:/run/runner/input.tar")
            self._copy_retry(marker,f"{cid}:/run/runner/input.ready")
            self.store.transition(run_id,fence,"executing")
            try: wait=self.engine.command(["wait",cid],timeout=115)
            except EngineError:
                self._teardown(cid,run_id,fence);raise EngineError("RUNNER_TIMEOUT")
            result_path=work/"result.json"
            self.engine.command(["cp",f"{cid}:/run/runner/result.json",str(result_path)])
            protocol=read_protocol(result_path)
            output=work/"output.tar"
            if protocol["status"]=="pass":
                self.engine.command(["cp",f"{cid}:/run/runner/output.tar",str(output)])
                inspect_tar(output)
            else: raise EngineError(str(protocol.get("failureCode") or "RUNNER_OPERATION_FAILED"))
            final_inspect=self._inspect(cid)
            self._teardown(cid,run_id,fence)
            return Outcome(protocol,output,final_inspect,cid)
        except Exception:
            if cid:
                try:self._teardown(cid,run_id,fence)
                except EngineError: pass
            raise

    def _teardown(self,cid:str,run_id:str,fence:int)->None:
        try:value=self._inspect(cid)
        except EngineError:
            self.store.transition(run_id,fence,"removed");return
        if not self._identity(value,run_id,fence): raise EngineError("RUNNER_STALE_IDENTITY")
        state=value.get("State",{})
        if state.get("Running"):
            try:self.engine.command(["stop","--time","5",cid],timeout=7)
            except EngineError:
                self.engine.command(["kill","--signal","KILL",cid],timeout=5)
        try:self.engine.command(["wait",cid],timeout=5)
        except EngineError:pass
        self.engine.command(["rm","--force",cid],timeout=10)
        try:self._inspect(cid)
        except EngineError:self.store.transition(run_id,fence,"removed");return
        raise EngineError("RUNNER_CONTAINER_RESIDUE")
