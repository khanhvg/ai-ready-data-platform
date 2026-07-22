"""Minimal fixed Docker CLI adapter bound to OrbStack's owner socket."""
from __future__ import annotations
import json, os, pathlib, pwd, socket, stat, subprocess
from typing import Sequence


class EngineError(RuntimeError):
    pass


class Engine:
    def __init__(self) -> None:
        home=pathlib.Path(pwd.getpwuid(os.geteuid()).pw_dir)
        self.socket=home/".orbstack/run/docker.sock"
        self.docker=pathlib.Path("/usr/local/bin/docker")

    def _env(self)->dict[str,str]:
        return {"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":"/var/empty","DOCKER_CONFIG":"/var/empty"}

    def argv(self,args:Sequence[str])->list[str]:
        return [str(self.docker),"--host",f"unix://{self.socket}",*args]

    def admit(self)->dict[str,object]:
        try: st=os.lstat(self.socket)
        except FileNotFoundError as exc: raise EngineError("RUNNER_ENGINE_UNAVAILABLE") from exc
        if not stat.S_ISSOCK(st.st_mode) or st.st_uid!=os.geteuid() or self.socket.is_symlink():
            raise EngineError("RUNNER_ENGINE_UNAVAILABLE")
        value=self.json(["info","--format","{{json .}}"])
        required=("MemoryLimit","SwapLimit","CpuCfsQuota","PidsLimit")
        if value.get("OSType")!="linux" or value.get("Architecture") not in ("aarch64","arm64") or value.get("CgroupVersion")!="2" or any(value.get(k) is not True for k in required):
            raise EngineError("RUNNER_CONTAINMENT_UNAVAILABLE")
        security=value.get("SecurityOptions",[])
        if not any(str(x).startswith("name=seccomp") for x in security) or not value.get("InitBinary"):
            raise EngineError("RUNNER_CONTAINMENT_UNAVAILABLE")
        return value

    def command(self,args:Sequence[str],*,timeout:float=30,check:bool=True)->subprocess.CompletedProcess[str]:
        argv=self.argv(args)
        try:
            return subprocess.run(argv,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout,check=check,env=self._env())
        except (OSError,subprocess.TimeoutExpired,subprocess.CalledProcessError) as exc:
            detail=getattr(exc,"stderr","")
            raise EngineError("RUNNER_ENGINE_OPERATION_FAILED") from exc

    def attached(self,args:Sequence[str],payload:bytes,*,timeout:float)->tuple[bytes,bytes]:
        process=subprocess.Popen(self.argv(args),stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=self._env())
        try:stdout,stderr=process.communicate(payload,timeout=timeout)
        except subprocess.TimeoutExpired as exc:
            process.kill();process.communicate();raise EngineError("RUNNER_TIMEOUT") from exc
        if process.returncode not in (0,1):raise EngineError("RUNNER_ENGINE_OPERATION_FAILED")
        return stdout,stderr

    def json(self,args:Sequence[str],*,timeout:float=30)->dict[str,object]:
        try: return json.loads(self.command(args,timeout=timeout).stdout)
        except json.JSONDecodeError as exc: raise EngineError("RUNNER_ENGINE_PROTOCOL_INVALID") from exc

    def inspect_optional(self, container_id: str) -> dict[str, object] | None:
        completed = self.command(["inspect", container_id], timeout=30, check=False)
        if completed.returncode == 0:
            try:
                value = json.loads(completed.stdout)
            except json.JSONDecodeError as exc:
                raise EngineError("RUNNER_ENGINE_PROTOCOL_INVALID") from exc
            if not isinstance(value, list) or len(value) != 1 or not isinstance(value[0], dict):
                raise EngineError("RUNNER_ENGINE_PROTOCOL_INVALID")
            return value[0]
        missing = f"no such object: {container_id}".lower()
        if completed.returncode == 1 and missing in completed.stderr.strip().lower():
            return None
        raise EngineError("RUNNER_ENGINE_OPERATION_FAILED")
