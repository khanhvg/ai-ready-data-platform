"""PID-namespace supervisor and subreaper for one fixed semantic operation."""
from __future__ import annotations
import ctypes, json, os, pathlib, resource, signal, sys, tarfile, time
from .archive import extract_tar
from .container_protocol import write
from .operation_adapters import execute
from .registry import resolve

RUN=pathlib.Path("/run/runner"); WORKSPACE=pathlib.Path("/workspace")
STREAM_LIMIT=2*1024*1024


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


def _archive_output(path:pathlib.Path)->None:
    with tarfile.open(path,"w",format=tarfile.PAX_FORMAT) as tf:
        for p in sorted((WORKSPACE/"state").rglob("*")):
            arc=p.relative_to(WORKSPACE).as_posix()
            info=tf.gettarinfo(str(p),arc); info.uid=65532; info.gid=65532; info.uname=""; info.gname=""; info.mtime=0
            if info.isfile():
                with p.open("rb") as f: tf.addfile(info,f)
            else: tf.addfile(info)


def main(argv:list[str]|None=None)->int:
    args=sys.argv[1:] if argv is None else argv
    if len(args)!=1: return 64
    operation=resolve(args[0]).operation_id
    RUN.mkdir(mode=0o700,parents=True,exist_ok=True); _subreaper()
    deadline=time.monotonic()+15
    while not (RUN/"input.ready").is_file():
        if time.monotonic()>deadline:
            write(RUN/"result.json",{"schemaVersion":"runner-container-result-v1","operationId":operation,"status":"fail","result":None,"failureCode":"RUNNER_INPUT_TIMEOUT","stdoutBytes":0,"stderrBytes":0,"descendantPeak":0,"resourceTrackerObserved":False}); return 1
        time.sleep(.02)
    extract_tar(RUN/"input.tar",WORKSPACE/"state")
    out_fd=os.open(RUN/"stdout.bin",os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    err_fd=os.open(RUN/"stderr.bin",os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    pid=os.fork()
    if pid==0:
        try:
            os.setsid(); os.dup2(out_fd,1); os.dup2(err_fd,2); os.close(out_fd); os.close(err_fd)
            resource.setrlimit(resource.RLIMIT_AS,(536870912,536870912))
            resource.setrlimit(resource.RLIMIT_FSIZE,(134217728,134217728))
            resource.setrlimit(resource.RLIMIT_NOFILE,(256,256))
            result=execute(operation)
            (RUN/"worker-result.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
            os._exit(0)
        except BaseException as exc:
            print(f"{type(exc).__name__}:{exc}",file=sys.stderr,flush=True); os._exit(1)
    os.close(out_fd); os.close(err_fd)
    end=time.monotonic()+110; peak=0; tracker=False; rc=None; failure=None
    while rc is None:
        got,status=os.waitpid(pid,os.WNOHANG)
        if got: rc=os.waitstatus_to_exitcode(status); break
        observed,saw=_descendants(); peak=max(peak,observed); tracker=tracker or saw
        if (RUN/"stdout.bin").stat().st_size>STREAM_LIMIT or (RUN/"stderr.bin").stat().st_size>STREAM_LIMIT:
            failure="RUNNER_OUTPUT_LIMIT"; os.killpg(pid,signal.SIGTERM); time.sleep(.2); os.killpg(pid,signal.SIGKILL)
        if time.monotonic()>end:
            failure="RUNNER_TIMEOUT"; os.killpg(pid,signal.SIGTERM); time.sleep(5)
            try: os.killpg(pid,signal.SIGKILL)
            except ProcessLookupError: pass
        if failure:
            _,status=os.waitpid(pid,0); rc=os.waitstatus_to_exitcode(status); break
        time.sleep(.02)
    reap_end=time.monotonic()+2
    while time.monotonic()<reap_end:
        try:
            got,_=os.waitpid(-1,os.WNOHANG)
            if got==0: time.sleep(.02)
        except ChildProcessError: break
    stdout_size=min((RUN/"stdout.bin").stat().st_size,STREAM_LIMIT)
    stderr_size=min((RUN/"stderr.bin").stat().st_size,STREAM_LIMIT)
    if rc==0 and failure is None:
        result=json.loads((RUN/"worker-result.json").read_text()); _archive_output(RUN/"output.tar"); status="pass"
    else:
        result=None; status="fail"; failure=failure or "RUNNER_OPERATION_FAILED"
    write(RUN/"result.json",{"schemaVersion":"runner-container-result-v1","operationId":operation,"status":status,"result":result,"failureCode":failure,"stdoutBytes":stdout_size,"stderrBytes":stderr_size,"descendantPeak":peak,"resourceTrackerObserved":tracker})
    print(json.dumps({"operationId":operation,"status":status},sort_keys=True),flush=True)
    return 0 if status=="pass" else 1


if __name__=="__main__": raise SystemExit(main())
