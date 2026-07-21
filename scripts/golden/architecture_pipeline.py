#!/usr/bin/env python3
"""Pinned Node bootstrap and two-install deterministic architecture verification."""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, platform, secrets, shutil, subprocess, sys, tarfile, time, urllib.request
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import fitness, runtime, source_state, workspace as workspace_core

ROOT=pathlib.Path(__file__).resolve().parents[2]
ARCHIVE="node-v22.22.3-darwin-arm64.tar.xz"; ARCHIVE_SHA="753c1629e168cc788ccc46ab61e0b35549fce08c07f82fcd3bb0d41f7fb01e7b"
class ArchitecturePipelineError(RuntimeError): pass
def run(command:list[str],cwd:pathlib.Path,env:dict[str,str],deadline:float)->subprocess.CompletedProcess[bytes]:
    try: return runtime.run(command,cwd=cwd,env=env,deadline=deadline)
    except runtime.RuntimeErrorTyped as exc: raise ArchitecturePipelineError(str(exc)) from exc
def safe_extract(archive:pathlib.Path,destination:pathlib.Path)->None:
    def contained(parts:tuple[str,...])->bool:
        stack=[]
        for part in parts:
            if part in {"","."}: continue
            if part=="..":
                if not stack: return False
                stack.pop()
            else: stack.append(part)
        return True
    with tarfile.open(archive,"r:xz") as bundle:
        for member in bundle.getmembers():
            pure=pathlib.PurePosixPath(member.name)
            if pure.is_absolute() or ".." in pure.parts: raise ArchitecturePipelineError("ARCH_TOOL_ARCHIVE_UNSAFE")
            if member.issym() or member.islnk():
                target=pathlib.PurePosixPath(member.linkname)
                resolved=pure.parent.joinpath(target)
                if target.is_absolute() or not contained(resolved.parts): raise ArchitecturePipelineError("ARCH_TOOL_ARCHIVE_UNSAFE")
        bundle.extractall(destination,filter="data")
def install(tool_root:pathlib.Path,node_root:pathlib.Path,deadline:float)->dict[str,str]:
    shutil.copyfile(ROOT/"requirements/architecture/package.json",tool_root/"package.json"); shutil.copyfile(ROOT/"requirements/architecture/package-lock.json",tool_root/"package-lock.json")
    env={"PATH":f"{node_root/'bin'}:/usr/bin:/bin:/usr/sbin:/sbin","HOME":str(tool_root/"home"),"TMPDIR":str(tool_root/"tmp"),"TZ":"UTC","LC_ALL":"C.UTF-8","LANG":"C.UTF-8","npm_config_cache":str(tool_root/"npm-cache"),"npm_config_audit":"false","npm_config_fund":"false","npm_config_ignore_scripts":"true"}
    for name in ("home","tmp","npm-cache"): (tool_root/name).mkdir(mode=0o700)
    if run([str(node_root/"bin/node"),"--version"],tool_root,env,deadline).stdout.strip()!=b"v22.22.3": raise ArchitecturePipelineError("ARCH_NODE_VERSION_MISMATCH")
    if run([str(node_root/"bin/npm"),"--version"],tool_root,env,deadline).stdout.strip()!=b"10.9.8": raise ArchitecturePipelineError("ARCH_NODE_VERSION_MISMATCH")
    run([str(node_root/"bin/npm"),"ci","--ignore-scripts","--no-audit","--no-fund"],tool_root,env,deadline)
    return env
def produce(tool:pathlib.Path,node:pathlib.Path,env:dict[str,str],stage:pathlib.Path,deadline:float)->pathlib.Path:
    like=tool/"node_modules/.bin/likec4"; model=stage/"model.json"; dot=stage/"dot"; dot.mkdir(mode=0o700)
    run([str(like),"format","--check",str(ROOT/"architecture/likec4")],ROOT,env,deadline)
    validation=run([str(like),"validate","--json",str(ROOT/"architecture/likec4")],ROOT,env,deadline)
    if b'"valid": true' not in validation.stdout: raise ArchitecturePipelineError("ARCH_SOURCE_INVALID")
    run([str(like),"export","json","--skip-layout","--pretty","-o",str(model),str(ROOT/"architecture/likec4")],ROOT,env,deadline)
    run([str(like),"gen","dot","-o",str(dot),str(ROOT/"architecture/likec4")],ROOT,env,deadline)
    shutil.copyfile(ROOT/"scripts/golden/architecture-render.mjs",tool/"architecture-render.mjs")
    raw=stage/"raw-svg"; run([str(node/"bin/node"),str(tool/"architecture-render.mjs"),str(dot),str(raw)],tool,env,deadline)
    final=stage/"final"; run([sys.executable,str(ROOT/"scripts/golden/architecture_finalize.py"),"--stage",str(stage),"--out",str(final)],ROOT,{**env,"PATH":f"{pathlib.Path(sys.executable).parent}:{env['PATH']}"},deadline)
    return final
def digest_tree(path:pathlib.Path)->str:
    digest=hashlib.sha256()
    for item in sorted(path.iterdir()): digest.update(item.name.encode()); digest.update(item.read_bytes())
    return digest.hexdigest()
def publish_complete(source:pathlib.Path,expected_sha:str,run_id:str)->None:
    architecture=ROOT/"architecture"; current=architecture/"rendered"; stage=architecture/f".rendered-stage-{run_id}"; backup=architecture/f".rendered-backup-{run_id}"
    if stage.exists() or backup.exists(): raise ArchitecturePipelineError("ARCH_RENDER_FAILED")
    shutil.copytree(source,stage)
    if digest_tree(stage)!=expected_sha: raise ArchitecturePipelineError("ARCH_RENDER_FAILED")
    os.rename(current,backup)
    try:
        os.rename(stage,current)
        directory_fd=os.open(architecture,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW)
        try: os.fsync(directory_fd)
        finally: os.close(directory_fd)
        if digest_tree(current)!=expected_sha: raise ArchitecturePipelineError("ARCH_RENDER_FAILED")
    except BaseException:
        if not current.exists(): os.rename(backup,current)
        raise
    shutil.rmtree(backup)
def main()->int:
    if len(sys.argv)!=2 or sys.argv[1] not in {"check","render"}: raise SystemExit("ARCH_COMMAND_INVALID")
    if platform.system()!="Darwin" or platform.machine()!="arm64": raise ArchitecturePipelineError("ARCH_TOOL_MISSING")
    source=source_state.identity(); started_wall=datetime.datetime.now(datetime.timezone.utc); started=time.monotonic(); deadline=started+120; run_id=secrets.token_hex(16)
    old=os.umask(0o077)
    workspace_owner=evidence_owner=None
    try:
        workspace_owner=workspace_core.allocate_family(("workspaces","golden"),f"architecture-{sys.argv[1]}",run_id)
        evidence_owner=workspace_core.allocate_family(("evidence",f"architecture-{sys.argv[1]}"),f"architecture-{sys.argv[1]}",run_id)
        workspace=workspace_owner.path; evidence=evidence_owner.path
        archive=workspace/ARCHIVE
        with urllib.request.urlopen(f"https://nodejs.org/download/release/v22.22.3/{ARCHIVE}",timeout=30) as response, archive.open("wb") as target: shutil.copyfileobj(response,target)
        if hashlib.sha256(archive.read_bytes()).hexdigest()!=ARCHIVE_SHA: raise ArchitecturePipelineError("ARCH_TOOL_LOCK_MISMATCH")
        extraction=workspace/"node"; extraction.mkdir(mode=0o700); safe_extract(archive,extraction); node=extraction/"node-v22.22.3-darwin-arm64"
        finals=[]
        for label in ("a","b"):
            tool=workspace/f"tool-{label}"; stage=workspace/f"stage-{label}"; tool.mkdir(mode=0o700); stage.mkdir(mode=0o700)
            env=install(tool,node,deadline); finals.append(produce(tool,node,env,stage,deadline))
        first=digest_tree(finals[0]); second=digest_tree(finals[1]); committed=digest_tree(ROOT/"architecture/rendered")
        if first!=second: raise ArchitecturePipelineError("ARCH_OUTPUT_NONDETERMINISTIC")
        if first!=committed:
            if sys.argv[1]!="render": raise ArchitecturePipelineError("ARCH_OUTPUT_STALE")
            publish_complete(finals[0],first,run_id); committed=digest_tree(ROOT/"architecture/rendered")
        if committed!=first: raise ArchitecturePipelineError("ARCH_OUTPUT_STALE")
        source_state.assert_unchanged(source); tested=source[0]; result=fitness.passed(command_id=f"architecture-{sys.argv[1]}",tested_tree_sha=tested,projection_sha256=first,started_at=started_wall,duration_ms=round((time.monotonic()-started)*1000),toolchain={"node":"22.22.3","npm":"10.9.8","likec4":"1.59.1","wasmGraphviz":"1.22.2","graphviz":"15.0.0"})
        (evidence/"result.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"result.json",0o600)
        print(f"architecture-{sys.argv[1]}: pass installs=2 renders=2 tree={first} evidence=architecture-{sys.argv[1]}/{run_id}/result.json"); workspace_owner.close(); evidence_owner.close(); workspace_owner=evidence_owner=None; return 0
    finally:
        if workspace_owner is not None: workspace_owner.close()
        if evidence_owner is not None: evidence_owner.close()
        os.umask(old)
if __name__=="__main__": raise SystemExit(main())
