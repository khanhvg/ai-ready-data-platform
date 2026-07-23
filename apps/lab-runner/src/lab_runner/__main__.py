"""Owner CLI; accepts only a closed semantic operation and idempotency key."""
from __future__ import annotations
import argparse,hashlib,json,pathlib,sys
from .contract import EXPECTED_COMMANDS, validate_released_contract
from .service import RunnerService,RunnerError
from .transport import serve_uds


def main(argv:list[str]|None=None)->int:
    p=argparse.ArgumentParser(prog="lab-runner",allow_abbrev=False);sub=p.add_subparsers(dest="command",required=True)
    run=sub.add_parser("run",allow_abbrev=False);run.add_argument("operation",choices=__import__("lab_runner.registry",fromlist=["operation_ids"]).operation_ids());run.add_argument("--idempotency-key",required=True)
    sub.add_parser("serve",allow_abbrev=False)
    a=p.parse_args(argv)
    app=pathlib.Path(__file__).resolve().parents[2];root=app.parents[1];config=app/"config"
    release_path=config/"runner-image-release-v1.json";build_path=config/"container-build-lock-v1.json";seccomp=app/"container/seccomp-runner-v1.json"
    release=json.loads(release_path.read_text());build=json.loads(build_path.read_text())
    validate_released_contract(root,config/"released-contract-lock.json")
    expected=(
        release.get("schemaVersion")=="runner-image-release-v1",release.get("platform")=="linux/arm64",
        release.get("user")=="65532:65532",release.get("workdir")=="/workspace",
        release.get("entrypoint")==["python3.12","-I","-m","lab_runner.container_supervisor"],
        tuple(release.get("operations") or ())==EXPECTED_COMMANDS,
        release.get("imageDigest")==build.get("imageDigest")==release.get("imageManifestDigest")==build.get("imageManifestDigest"),
        release.get("imageConfigDigest")==build.get("imageConfigDigest"),
        release.get("seccompSha256")==build.get("seccompSha256")==hashlib.sha256(seccomp.read_bytes()).hexdigest(),
        release.get("buildLockSha256")==hashlib.sha256(build_path.read_bytes()).hexdigest(),
        isinstance(release.get("operationResults"),list) and len(release["operationResults"])==8,
        release.get("gateAggregate")=={"redRows":52,"s3Rows":14,"passed":66,"failed":0},
        (release.get("rollbackAggregate") or {}).get("attempts")==2,
    )
    if not all(expected) or not str(release.get("imageDigest","")).startswith("sha256:"):
        raise SystemExit("RUNNER_IMAGE_RELEASE_INVALID")
    service=RunnerService(app/".local-state",release["imageDigest"],seccomp)
    if a.command=="serve":
        serve_uds(service,root/a.state_root/"control.json");return 0
    request={"operationId":a.operation,"idempotencyKey":a.idempotency_key,"workspaceRevision":service.current_revision()}
    try:result=service.run(request)
    except RunnerError as exc:
        print(json.dumps({"status":"fail","failureCode":str(exc)},sort_keys=True),file=sys.stderr);return 1
    print(json.dumps(result,sort_keys=True,separators=(",",":")));return 0


if __name__=="__main__":raise SystemExit(main())
