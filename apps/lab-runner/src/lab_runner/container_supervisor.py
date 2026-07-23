"""PID-namespace supervisor and subreaper for one fixed semantic operation."""
from __future__ import annotations
import ctypes, hashlib, io, json, os, pathlib, resource, runpy, selectors, signal, struct, sys, tarfile, time
from .archive import extract_tar
from .container_protocol import write
from .operation_adapters import execute
from .registry import resolve

RUN=pathlib.Path("/run/runner"); WORKSPACE=pathlib.Path("/workspace"); OUTPUT=WORKSPACE/".runner-output.tar"
STREAM_LIMIT=2*1024*1024
FIXTURES={
    "argv_probe.py":(),"import_probe.py":(),"process_tree_probe.py":(),"rapid_double_fork.py":(),
    "reparent_setsess_daemon.py":(),"fork_bomb.py":(),"main_crash.py":(),"network_probe.py":(),
    "output_flood.py":(),"resource_probe.py":("memory","cpu","files","fds"),
}


def _workspace_file_count(root:pathlib.Path)->int:
    count=0
    for path in root.rglob("*"):
        if path.is_file():
            count+=1
            if count>4096:raise RuntimeError("RUNNER_RESOURCE_LIMIT")
    return count


def _subreaper()->None:
    if ctypes.CDLL(None,use_errno=True).prctl(36,1,0,0,0)!=0:
        raise OSError(ctypes.get_errno(),"PR_SET_CHILD_SUBREAPER")


def _descendants()->tuple[int,bool]:
    count=0; tracker=False
    for p in pathlib.Path("/proc").iterdir():
        if not p.name.isdigit() or int(p.name) in (1,os.getpid()): continue
        try:
            cmd=(p/"cmdline").read_bytes()
            count+=1; tracker=tracker or b"resource_tracker" in cmd
        except OSError: pass
    return count,tracker


def _descendant_pids()->list[int]:
    return [int(p.name) for p in pathlib.Path("/proc").iterdir() if p.name.isdigit() and int(p.name) not in (1,os.getpid())]


def _cgroup()->dict[str,object]:
    root=pathlib.Path("/sys/fs/cgroup");events=dict(line.split() for line in (root/"memory.events").read_text().splitlines())
    return {"memoryMax":(root/"memory.max").read_text().strip(),"memorySwapMax":(root/"memory.swap.max").read_text().strip(),"memoryPeak":int((root/"memory.peak").read_text()),"memoryEvents":{key:int(value) for key,value in events.items()}}


def _archive_output(path:pathlib.Path,state:pathlib.Path=WORKSPACE/"state")->None:
    rows=[]
    with tarfile.open(path,"w",format=tarfile.PAX_FORMAT) as tf:
        for p in sorted(state.rglob("*")):
            if p.relative_to(state).as_posix()==".runner-output-manifest.json":continue
            arc=p.relative_to(state).as_posix()
            info=tf.gettarinfo(str(p),arc); info.uid=65532; info.gid=65532; info.uname=""; info.gname=""; info.mtime=0
            if info.isfile():
                info.mode=0o600
                raw=p.read_bytes();tf.addfile(info,io.BytesIO(raw));rows.append({"path":arc,"type":"file","mode":384,"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()})
            elif info.isdir():
                info.mode=0o700;tf.addfile(info);rows.append({"path":arc,"type":"directory","mode":448,"size":0,"sha256":None})
            else:raise RuntimeError("RUNNER_OUTPUT_TYPE_INVALID")
        manifest=json.dumps({"schemaVersion":"runner-output-manifest-v1","entries":rows},sort_keys=True,separators=(",",":")).encode()+b"\n"
        info=tarfile.TarInfo(".runner-output-manifest.json");info.uid=info.gid=65532;info.mode=0o600;info.mtime=0;info.size=len(manifest)
        tf.addfile(info,io.BytesIO(manifest))


def _fixture(name:str,fixture_args:tuple[str,...])->dict[str,object]:
    allowed=FIXTURES.get(name)
    if allowed is None or (name=="resource_probe.py" and (len(fixture_args)!=1 or fixture_args[0] not in allowed)) or (name!="resource_probe.py" and fixture_args):
        raise RuntimeError("RUNNER_TEST_FIXTURE_INVALID")
    old_argv=sys.argv;old_guard=os.environ.get("RUNNER_ADVERSARIAL_CONTAINER")
    try:
        sys.argv=[name,*fixture_args];os.environ["RUNNER_ADVERSARIAL_CONTAINER"]="1"
        namespace=runpy.run_path(f"/opt/runner-fixtures/{name}",run_name="__main__")
    finally:
        sys.argv=old_argv
        if old_guard is None:os.environ.pop("RUNNER_ADVERSARIAL_CONTAINER",None)
        else:os.environ["RUNNER_ADVERSARIAL_CONTAINER"]=old_guard
    return {"fixture":name,"arguments":list(fixture_args),"observation":namespace.get("RESULT")}


def _main(operation:str,fixture:tuple[str,tuple[str,...]]|None=None,execute_seconds:int=110)->int:
    RUN.mkdir(mode=0o700,parents=True,exist_ok=True); _subreaper()
    header=sys.stdin.buffer.read(12)
    if len(header)!=12 or not header.startswith(b"I9IN"):return 65
    input_length=struct.unpack("!Q",header[4:])[0]
    if input_length>268435456:return 65
    input_raw=sys.stdin.buffer.read(input_length)
    if len(input_raw)!=input_length or sys.stdin.buffer.read(1):return 65
    (RUN/"input.tar").write_bytes(input_raw)
    extract_tar(RUN/"input.tar",WORKSPACE/"state")
    (WORKSPACE/"state/.runner-output-manifest.json").unlink(missing_ok=True)
    if fixture is None and operation=="retail.dbt-build":
        import dbt.cli.main, duckdb  # preload fixed native/runtime mappings before RLIMIT_AS
    out_read,out_write=os.pipe();err_read,err_write=os.pipe()
    pid=os.fork()
    if pid==0:
        try:
            os.close(out_read);os.close(err_read);os.setsid();os.dup2(out_write,1);os.dup2(err_write,2);os.close(out_write);os.close(err_write)
            resource.setrlimit(resource.RLIMIT_FSIZE,(134217728,134217728))
            resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
            resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
            result=_fixture(*fixture) if fixture is not None else execute(operation)
            (RUN/"worker-result.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
            os._exit(0)
        except BaseException as exc:
            print(f"{type(exc).__name__}:{exc}",file=sys.stderr,flush=True); os._exit(1)
    os.close(out_write);os.close(err_write)
    streams=selectors.DefaultSelector();streams.register(out_read,selectors.EVENT_READ,"stdout");streams.register(err_read,selectors.EVENT_READ,"stderr")
    sizes={"stdout":0,"stderr":0};stderr_preview=bytearray()
    def drain(wait:float)->None:
        for key,_ in streams.select(wait):
            try:data=os.read(key.fd,65536)
            except BlockingIOError:continue
            if data:
                sizes[str(key.data)]+=len(data)
                if key.data=="stderr" and len(stderr_preview)<131072:stderr_preview.extend(data[:131072-len(stderr_preview)])
            else:
                streams.unregister(key.fd);os.close(key.fd)
    end=time.monotonic()+execute_seconds; peak=0; tracker=False; rc=None; failure=None
    while rc is None:
        drain(.02)
        got,status=os.waitpid(pid,os.WNOHANG)
        if got: rc=os.waitstatus_to_exitcode(status); break
        observed,saw=_descendants(); peak=max(peak,observed); tracker=tracker or saw
        if sizes["stdout"]>STREAM_LIMIT or sizes["stderr"]>STREAM_LIMIT:
            failure="RUNNER_OUTPUT_LIMIT"
            try:os.killpg(pid,signal.SIGTERM)
            except ProcessLookupError:pass
            time.sleep(.2)
            try:os.killpg(pid,signal.SIGKILL)
            except ProcessLookupError:pass
        if time.monotonic()>end:
            failure="RUNNER_TIMEOUT"; os.killpg(pid,signal.SIGTERM); time.sleep(5)
            try: os.killpg(pid,signal.SIGKILL)
            except ProcessLookupError: pass
        if failure:
            _,status=os.waitpid(pid,0); rc=os.waitstatus_to_exitcode(status); break
    drain(0)
    if rc!=0 and stderr_preview:os.write(2,bytes(stderr_preview))
    cgroup=_cgroup()
    if fixture is not None and fixture==("resource_probe.py",("memory",)) and rc==-signal.SIGKILL and int(cgroup["memoryEvents"].get("oom_kill",0))>=1:failure="RUNNER_RESOURCE_LIMIT"
    reap_end=time.monotonic()+2
    while time.monotonic()<reap_end:
        observed,saw=_descendants();peak=max(peak,observed);tracker=tracker or saw
        try:
            got,_=os.waitpid(-1,os.WNOHANG)
            if got==0: time.sleep(.02)
        except ChildProcessError: break
    if rc==0 and failure is None:
        try:_workspace_file_count(WORKSPACE/"state")
        except RuntimeError as exc:failure=str(exc)
    survivors=_descendant_pids()
    if survivors:
        for child in survivors:
            try:os.kill(child,signal.SIGTERM)
            except ProcessLookupError:pass
        time.sleep(.2)
        for child in _descendant_pids():
            try:os.kill(child,signal.SIGKILL)
            except ProcessLookupError:pass
        while True:
            try:
                got,_=os.waitpid(-1,os.WNOHANG)
                if got==0:break
            except ChildProcessError:break
        failure=failure or "RUNNER_DESCENDANT_SURVIVOR"
    for key in list(streams.get_map().values()):
        try:streams.unregister(key.fd);os.close(key.fd)
        except OSError:pass
    streams.close();stdout_size=min(sizes["stdout"],STREAM_LIMIT);stderr_size=min(sizes["stderr"],STREAM_LIMIT)
    if rc==0 and failure is None and not _descendant_pids():
        result=json.loads((RUN/"worker-result.json").read_text()); _archive_output(OUTPUT); status="pass"
    else:
        result=None; status="fail"; failure=failure or "RUNNER_OPERATION_FAILED"
    write(RUN/"result.json",{"schemaVersion":"runner-container-result-v1","operationId":operation,"status":status,"result":result,"failureCode":failure,"stdoutBytes":stdout_size,"stderrBytes":stderr_size,"descendantPeak":peak,"resourceTrackerObserved":tracker,"cgroup":cgroup})
    protocol=(RUN/"result.json").read_bytes();archive=OUTPUT.read_bytes() if status=="pass" else b""
    sys.stdout.buffer.write(b"I9OUT"+struct.pack("!I",len(protocol))+protocol+struct.pack("!Q",len(archive))+archive);sys.stdout.buffer.flush()
    return 0 if status=="pass" else 1


def main_fixture(name:str,fixture_args:tuple[str,...]=(),execute_seconds:int=110)->int:
    if type(execute_seconds) is not int or not 1<=execute_seconds<=110:return 64
    return _main(f"fixture.{name}",(name,fixture_args),execute_seconds)


def main(argv:list[str]|None=None)->int:
    args=sys.argv[1:] if argv is None else argv
    if len(args)!=1:return 64
    return _main(resolve(args[0]).operation_id)


if __name__=="__main__": raise SystemExit(main())
