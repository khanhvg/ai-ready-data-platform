"""Host control-plane composition for one admitted semantic operation."""
from __future__ import annotations
import os, pathlib, subprocess, tempfile
from .archive import extract_tar
from .container_backend import Backend
from .engine import Engine,EngineError
from .evidence import discard as discard_evidence, publish as publish_evidence, reconcile as reconcile_evidence, stage as stage_evidence
from .fence import acquire
from .registry import validate_request
from .release import validate as validate_release
from .state import Store,StateError
from .workspace import Workspace


class RunnerError(RuntimeError):
    pass


class RunnerService:
    def __init__(self,root:pathlib.Path,image_digest:str,seccomp:pathlib.Path):
        self.root=root.resolve();self.root.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(self.root,0o700)
        self.store=Store(self.root/"state");self.workspace=Workspace(self.root/"workspaces"/"promotion-trust")
        self.engine=Engine();self.backend=Backend(self.engine,image_digest,seccomp,self.root/"staging",self.store)
        self.evidence=self.root/"evidence";self.evidence.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(self.evidence,0o700)
        self.workspace.reconcile(self.store.current_revision())
        for run_id,_ in self.store.committed():reconcile_evidence(self.evidence,run_id)

    def _reserve(self)->None:
        disk=os.statvfs(self.root)
        if disk.f_bavail*disk.f_frsize < 6*1024**3: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE")
        probe=subprocess.run(["/usr/bin/memory_pressure","-Q"],text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=5,check=True,env={"PATH":"/usr/bin:/bin"})
        line=next((x for x in probe.stdout.splitlines() if "free percentage" in x),"")
        try:percent=int(line.rsplit(" ",1)[1].rstrip("%"))
        except ValueError as exc: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE") from exc
        total=int(subprocess.run(["/usr/sbin/sysctl","-n","hw.memsize"],text=True,stdout=subprocess.PIPE,check=True,timeout=5,env={"PATH":"/usr/bin:/bin:/usr/sbin"}).stdout)
        if total*percent//100 < 6*1024**3: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE")

    def run(self,request_value:object)->dict[str,object]:
        request=validate_request(request_value)
        self._reserve()
        with acquire(self.root/"locks") as fence:
            self.workspace.reconcile(self.store.current_revision())
            for run_id,status,container_id,image_digest,run_fence,daemon_identity in self.store.incomplete():
                self.backend.reconcile(run_id,status,container_id,image_digest,run_fence,daemon_identity)
            admission=self.store.admit(request,fence.epoch)
            if admission.replay is not None:return admission.replay
            run_dir=self.root/"inputs"/admission.run_id;run_dir.mkdir(mode=0o700,parents=True,exist_ok=False)
            input_archive=run_dir/"input.tar";self.workspace.input_archive(int(request["workspaceRevision"]),input_archive)
            committed=False;staged_evidence=None
            try:
                outcome=self.backend.execute(admission.run_id,fence.epoch,str(request["operationId"]),input_archive)
                revision=int(request["workspaceRevision"])+1
                release_assets=None
                if request["operationId"]=="retail.export":
                    validation_root=self.root/"release-validation";validation_root.mkdir(mode=0o700,exist_ok=True);os.chmod(validation_root,0o700)
                    with tempfile.TemporaryDirectory(prefix=f"{admission.run_id}-",dir=validation_root) as temporary:
                        extracted=pathlib.Path(temporary);extract_tar(outcome.output_archive,extracted);release_assets=validate_release(extracted)
                self.workspace.stage(outcome.output_archive,revision)
                result={"schemaVersion":"runner-operation-result-v1","runId":admission.run_id,"operationId":request["operationId"],"workspaceRevision":revision,"status":"pass","result":outcome.protocol["result"],"containerIdSha256":__import__("hashlib").sha256(outcome.container_id.encode()).hexdigest()}
                if release_assets is not None:result["releaseAssets"]=release_assets
                staged_evidence=stage_evidence(self.evidence,admission.run_id,result)
                self.store.commit(admission.run_id,fence.epoch,result,revision)
                committed=True
                self.workspace.publish(revision)
                publish_evidence(self.evidence,admission.run_id,staged_evidence);staged_evidence=None
                return result
            except (EngineError,StateError,RuntimeError) as exc:
                if not committed and staged_evidence is not None and staged_evidence.exists():discard_evidence(staged_evidence)
                if not committed:
                    try:self.store.fail_if_safe(admission.run_id,fence.epoch)
                    except StateError:pass
                raise RunnerError(str(exc)) from exc

    def current_revision(self)->int:return self.store.current_revision()
