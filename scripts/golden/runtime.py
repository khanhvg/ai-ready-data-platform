#!/usr/bin/env python3
"""Exact private CPython environment bootstrap shared by issue #6 commands."""
from __future__ import annotations
import os, pathlib, platform, signal, subprocess, tempfile, time

ROOT=pathlib.Path(__file__).resolve().parents[2]
LOCK=ROOT/"requirements/golden-py312-macos-arm64.lock"
class RuntimeErrorTyped(RuntimeError): pass

def require_platform() -> None:
    if platform.system()!="Darwin" or platform.machine()!="arm64": raise RuntimeErrorTyped("PYTHON_BASELINE_UNSUPPORTED")
    version=subprocess.check_output(["python3.12","-c","import platform; print(platform.python_version())"],text=True).strip()
    if not version.startswith("3.12."): raise RuntimeErrorTyped("PYTHON_BASELINE_UNSUPPORTED")

def clean_env(home:pathlib.Path,cache:pathlib.Path,venv:pathlib.Path)->dict[str,str]:
    return {"PATH":f"{venv/'bin'}:/usr/bin:/bin:/usr/sbin:/sbin","HOME":str(home),"TMPDIR":str(home/"tmp"),"TZ":"UTC","LC_ALL":"C.UTF-8","LANG":"C.UTF-8","PYTHONHASHSEED":"0","PYTHONDONTWRITEBYTECODE":"1","PIP_CONFIG_FILE":"/dev/null","PIP_CACHE_DIR":str(cache),"PIP_DISABLE_PIP_VERSION_CHECK":"1","PIP_NO_INPUT":"1"}

def run(command:list[str],*,cwd:pathlib.Path,env:dict[str,str],deadline:float,limit:int=2*1024*1024)->subprocess.CompletedProcess[bytes]:
    temp_root=pathlib.Path(env.get("TMPDIR", ""))
    if not temp_root.is_dir() or temp_root.is_symlink(): raise RuntimeErrorTyped("PROCESS_TEMP_INVALID")
    def terminate(process:subprocess.Popen[bytes])->None:
        pgid=process.pid
        try: os.killpg(pgid,signal.SIGTERM)
        except ProcessLookupError: return
        grace=time.monotonic()+5
        while time.monotonic()<grace:
            process.poll()
            try: os.killpg(pgid,0)
            except (ProcessLookupError,PermissionError): break
            time.sleep(0.05)
        try: os.killpg(pgid,signal.SIGKILL)
        except ProcessLookupError: pass
        try: process.wait(timeout=5)
        except subprocess.TimeoutExpired: raise RuntimeErrorTyped("PROCESS_CLEANUP_FAILED")
        cleanup=time.monotonic()+5
        while time.monotonic()<cleanup:
            try: os.killpg(pgid,0)
            except (ProcessLookupError,PermissionError): return
            time.sleep(0.05)
        raise RuntimeErrorTyped("PROCESS_CLEANUP_FAILED")
    with tempfile.TemporaryFile(dir=temp_root) as stdout_file, tempfile.TemporaryFile(dir=temp_root) as stderr_file:
        process=subprocess.Popen(command,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=stdout_file,stderr=stderr_file,start_new_session=True)
        while process.poll() is None:
            if time.monotonic()>=deadline:
                terminate(process); raise RuntimeErrorTyped("PROCESS_TIMEOUT")
            if os.fstat(stdout_file.fileno()).st_size>limit or os.fstat(stderr_file.fileno()).st_size>limit:
                terminate(process); raise RuntimeErrorTyped("PROCESS_OUTPUT_LIMIT")
            time.sleep(0.02)
        stdout_file.seek(0); stderr_file.seek(0); stdout=stdout_file.read(limit+1); stderr=stderr_file.read(limit+1)
    result=subprocess.CompletedProcess(command,process.returncode,stdout,stderr)
    if len(result.stdout)>limit or len(result.stderr)>limit: raise RuntimeErrorTyped("PROCESS_OUTPUT_LIMIT")
    if result.returncode: raise RuntimeErrorTyped(f"PROCESS_FAILED:{pathlib.Path(command[0]).name}:{result.returncode}\n"+result.stderr[-4096:].decode("utf-8","replace"))
    return result

def bootstrap(run_root:pathlib.Path,deadline:float)->tuple[pathlib.Path,dict[str,str]]:
    require_platform(); venv=run_root/"venv"; home=run_root/"home"; cache=run_root/"pip-cache"
    for path in (home,home/"tmp",cache): path.mkdir(mode=0o700,parents=True,exist_ok=False)
    base={"PATH":"/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin","HOME":str(home),"TMPDIR":str(home/"tmp"),"TZ":"UTC","LC_ALL":"C.UTF-8","LANG":"C.UTF-8","PYTHONHASHSEED":"0","PYTHONDONTWRITEBYTECODE":"1","PIP_CONFIG_FILE":"/dev/null","PIP_CACHE_DIR":str(cache),"PIP_DISABLE_PIP_VERSION_CHECK":"1","PIP_NO_INPUT":"1"}
    run(["python3.12","-m","venv",str(venv)],cwd=ROOT,env=base,deadline=deadline)
    env=clean_env(home,cache,venv)
    run([str(venv/"bin/python"),"-m","pip","install","--require-hashes","--only-binary=:all:","--no-deps","-r",str(LOCK)],cwd=ROOT,env=env,deadline=deadline)
    run([str(venv/"bin/python"),"-m","pip","check"],cwd=ROOT,env=env,deadline=deadline)
    run([str(venv/"bin/python"),"-c","import dbt,duckdb,faker,jsonschema,rfc8785,yaml"],cwd=ROOT,env=env,deadline=deadline)
    return venv,env
