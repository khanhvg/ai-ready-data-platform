"""Owner CLI; accepts only a closed semantic operation and idempotency key."""
from __future__ import annotations
import argparse,json,pathlib,sys
from .service import RunnerService,RunnerError
from .transport import serve_loopback


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(prog="lab-runner",allow_abbrev=False);sub=p.add_subparsers(dest="command",required=True)
    run=sub.add_parser("run",allow_abbrev=False);run.add_argument("operation",choices=__import__("lab_runner.registry",fromlist=["operation_ids"]).operation_ids());run.add_argument("--idempotency-key",required=True)
    sub.add_parser("serve",allow_abbrev=False)
    p.add_argument("--state-root",default="apps/lab-runner/.local-state",help=argparse.SUPPRESS)
    p.add_argument("--image-lock",default="apps/lab-runner/config/runner-image-release-v1.json",help=argparse.SUPPRESS)
    a=p.parse_args(argv)
    root=pathlib.Path.cwd();release=json.loads((root/a.image_lock).read_text())
    service=RunnerService(root/a.state_root,release["imageDigest"],root/"apps/lab-runner/container/seccomp-runner-v1.json")
    if a.command=="serve":
        serve_loopback(service,root/a.state_root/"control.json");return 0
    request={"operationId":a.operation,"idempotencyKey":a.idempotency_key,"workspaceRevision":service.current_revision()}
    try:result=service.run(request)
    except RunnerError as exc:
        print(json.dumps({"status":"fail","failureCode":str(exc)},sort_keys=True),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True,separators=(",",":")));return 0


if __name__=="__main__":raise SystemExit(main())
