"""Host control-plane composition for one admitted semantic operation."""
from __future__ import annotations
import json, os, pathlib, stat, subprocess, tempfile
from .archive import extract_tar
from .container_backend import Backend
from .engine import Engine,EngineError
from .evidence import discard as discard_evidence, publish as publish_evidence, reconcile as reconcile_evidence, stage as stage_evidence, verify as verify_evidence, write as write_evidence
from .fence import acquire
from .registry import validate_request
from .release import contract_schema_sha256, manifest_bytes, publish as publish_release, rollback as rollback_release, validate as validate_release, validate_manifest
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
        self.releases=self.root/"releases"
        for run_id,result in self.store.committed():
            reconcile_evidence(self.evidence,run_id,result)
            if result.get("operationId")=="retail.export":publish_release(self.releases,result)

    def _reserve(self)->None:
        disk=os.statvfs(self.root)
        if disk.f_bavail*disk.f_frsize < 6*1024**3: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE")
        probe=subprocess.run(["/usr/bin/memory_pressure","-Q"],text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL,timeout=5,check=True,env={"PATH":"/usr/bin:/bin"})
        line=next((x for x in probe.stdout.splitlines() if "free percentage" in x),"")
        try:percent=int(line.rsplit(" ",1)[1].rstrip("%"))
        except ValueError as exc: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE") from exc
        total=int(subprocess.run(["/usr/sbin/sysctl","-n","hw.memsize"],text=True,stdout=subprocess.PIPE,check=True,timeout=5,env={"PATH":"/usr/bin:/bin:/usr/sbin"}).stdout)
        if total*percent//100 < 6*1024**3: raise RunnerError("RUNNER_RESOURCE_UNAVAILABLE")

    @staticmethod
    def _owned_directory(base:pathlib.Path,run_id:str,fence:int,purpose:str)->pathlib.Path:
        base.mkdir(mode=0o700,parents=True,exist_ok=True);path=base/run_id;path.mkdir(mode=0o700,exist_ok=False);observed=path.stat(follow_symlinks=False);owner={"schemaVersion":"runner-transient-owner-v1","runId":run_id,"fence":fence,"purpose":purpose,"device":observed.st_dev,"inode":observed.st_ino};marker=path/".runner-owner.json";marker.write_text(json.dumps(owner,sort_keys=True,separators=(",",":"))+"\n");os.chmod(marker,0o600);return path

    @staticmethod
    def _cleanup_owned(base:pathlib.Path,run_id:str,fence:int,purpose:str,allowed:set[str])->bool:
        path=base/run_id
        if not path.exists():return False
        observed=path.stat(follow_symlinks=False);marker=path/".runner-owner.json"
        try:owner=json.loads(marker.read_text())
        except (OSError,json.JSONDecodeError) as exc:raise RunnerError("RUNNER_TRANSIENT_IDENTITY_INVALID") from exc
        expected={"schemaVersion":"runner-transient-owner-v1","runId":run_id,"fence":fence,"purpose":purpose,"device":observed.st_dev,"inode":observed.st_ino}
        if path.is_symlink() or not stat.S_ISDIR(observed.st_mode) or stat.S_IMODE(observed.st_mode)!=0o700 or owner!=expected or {child.name for child in path.iterdir()}-({".runner-owner.json"}|allowed):raise RunnerError("RUNNER_TRANSIENT_IDENTITY_INVALID")
        for child in path.iterdir():
            child_state=child.stat(follow_symlinks=False)
            if not stat.S_ISREG(child_state.st_mode) or child.is_symlink() or child_state.st_nlink!=1:raise RunnerError("RUNNER_TRANSIENT_IDENTITY_INVALID")
        for child in path.iterdir():child.unlink()
        path.rmdir();fd=os.open(base,os.O_RDONLY);os.fsync(fd);os.close(fd);return True

    def run(self,request_value:object)->dict[str,object]:
        request=validate_request(request_value)
        self._reserve()
        with acquire(self.root/"locks") as fence:
            self.workspace.reconcile(self.store.current_revision())
            for run_id,status,container_id,image_digest,run_fence,daemon_identity in self.store.incomplete():
                self.backend.reconcile(run_id,status,container_id,image_digest,run_fence,daemon_identity)
            admission=self.store.admit(request,fence.epoch)
            if admission.replay is not None:
                self.workspace.reconcile(self.store.current_revision());reconcile_evidence(self.evidence,admission.run_id,admission.replay)
                if admission.replay.get("operationId")=="retail.export":publish_release(self.releases,admission.replay)
                return admission.replay
            run_dir=self._owned_directory(self.root/"inputs",admission.run_id,fence.epoch,"input")
            input_archive=run_dir/"input.tar";self.workspace.input_archive(int(request["workspaceRevision"]),input_archive)
            committed=False;staged_evidence=None
            try:
                outcome=self.backend.execute(admission.run_id,fence.epoch,str(request["operationId"]),input_archive)
                revision=int(request["workspaceRevision"])+1
                release_assets=None;release_manifest=None
                if request["operationId"]=="retail.export":
                    validation_root=self.root/"release-validation";validation_root.mkdir(mode=0o700,exist_ok=True);os.chmod(validation_root,0o700)
                    with tempfile.TemporaryDirectory(prefix=f"{admission.run_id}-",dir=validation_root) as temporary:
                        extracted=pathlib.Path(temporary)/"workspace";extract_tar(outcome.output_archive,extracted);release_assets=validate_release(extracted);manifest=validate_manifest(extracted)
                        protocol_manifest=dict(outcome.protocol["result"].get("releaseManifest") or {});manifest_raw=manifest_bytes(manifest);release_manifest={"releaseId":manifest["releaseId"],"manifestSha256":__import__("hashlib").sha256(manifest_raw).hexdigest(),"contractSchemaSha256":contract_schema_sha256(),"assets":manifest["assets"]}
                        if protocol_manifest!=release_manifest or release_assets!=outcome.protocol["result"].get("assets"):raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
                self.workspace.stage(outcome.output_archive,revision)
                result={"schemaVersion":"runner-operation-result-v1","runId":admission.run_id,"operationId":request["operationId"],"workspaceRevision":revision,"fence":fence.epoch,"status":"pass","result":outcome.protocol["result"],"containerIdSha256":__import__("hashlib").sha256(outcome.container_id.encode()).hexdigest()}
                if release_assets is not None:result["releaseAssets"]=release_assets
                if release_manifest is not None:result["releaseManifest"]=release_manifest
                staged_evidence=stage_evidence(self.evidence,admission.run_id,result)
                self.store.commit(admission.run_id,fence.epoch,result,revision)
                committed=True
                self.workspace.publish(revision)
                if release_manifest is not None:publish_release(self.releases,result)
                publish_evidence(self.evidence,admission.run_id,staged_evidence,result);staged_evidence=None
                return result
            except (EngineError,StateError,RuntimeError) as exc:
                if not committed and staged_evidence is not None and staged_evidence.exists():discard_evidence(staged_evidence)
                if not committed:
                    try:self.store.fail_if_safe(admission.run_id,fence.epoch)
                    except StateError:pass
                raise RunnerError(str(exc)) from exc

    def current_revision(self)->int:return self.store.current_revision()

    def rollback(self,expected_current_release_id:str)->dict[str,object]:
        with acquire(self.root/"locks"):
            incomplete=self.store.incomplete();cleaned=[]
            for run_id,status,container_id,image_digest,run_fence,daemon_identity in incomplete:
                self.backend.reconcile(run_id,status,container_id,image_digest,run_fence,daemon_identity)
                if self._cleanup_owned(self.root/"inputs",run_id,run_fence,"input",{"input.tar"}):cleaned.append(f"inputs/{run_id}")
                if self._cleanup_owned(self.root/"staging",run_id,run_fence,"staging",{"input.ready","result.json","output.tar"}):cleaned.append(f"staging/{run_id}")
            self.workspace.reconcile(self.store.current_revision())
            for run_id,result in self.store.committed():reconcile_evidence(self.evidence,run_id,result)
            self.store.record_event({"kind":"rollback-started","expectedCurrentReleaseId":expected_current_release_id})
            pointer=rollback_release(self.releases,expected_current_release_id)
            self.store.record_event({"kind":"rollback-completed","expectedCurrentReleaseId":expected_current_release_id,"restoredReleaseId":pointer["currentReleaseId"],"manifestSha256":pointer["manifestSha256"],"cleaned":cleaned})
            evidence={"schemaVersion":"runner-rollback-result-v1","status":"pass","expectedCurrentReleaseId":expected_current_release_id,"restoredReleaseId":pointer["currentReleaseId"],"manifestSha256":pointer["manifestSha256"],"cleaned":cleaned,"preserved":["audit","evidence","immutable-releases"]};rollback_id="rollback-"+__import__("hashlib").sha256(json.dumps(evidence,sort_keys=True,separators=(",",":")).encode()).hexdigest()[:32]
            if (self.evidence/rollback_id).is_dir():verify_evidence(self.evidence,rollback_id,evidence)
            else:write_evidence(self.evidence,rollback_id,evidence)
            return pointer
