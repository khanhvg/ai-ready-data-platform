#!/usr/bin/env python3
"""Create the exact normalized context and build the local arm64 image."""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, pwd, shutil, subprocess, tarfile

ROOT=pathlib.Path(__file__).resolve().parents[3]
APP=ROOT/"apps/lab-runner"
BUILD=ROOT/".artifacts/build/issue-9"
CONTEXT=BUILD/"context"
TAR=BUILD/"runner-context.tar"
STAGE_A="fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"


def sha(path:pathlib.Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()


def tracked(path:pathlib.Path)->None:
    subprocess.run(["git","ls-files","--error-unmatch",path.relative_to(ROOT).as_posix()],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)


def copy_file(source:pathlib.Path,target:pathlib.Path)->None:
    tracked(source)
    if source.is_symlink() or not source.is_file():raise SystemExit("CONTEXT_SOURCE_TYPE_INVALID")
    target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(source.read_bytes());os.chmod(target,0o644)


def files_in(family:str)->list[pathlib.Path]:
    names=subprocess.run(["git","ls-files",family],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines()
    return [ROOT/name for name in names]


def build_context()->dict[str,object]:
    if CONTEXT.exists():shutil.rmtree(CONTEXT)
    CONTEXT.mkdir(mode=0o700,parents=True)
    copy_file(APP/"container/runner.Dockerfile",CONTEXT/"Dockerfile")
    app_paths=[APP/"pyproject.toml",APP/"requirements/runner-py312-linux-arm64.lock",APP/"config/runtime-policy-v2.toml"]
    app_paths+=files_in("apps/lab-runner/src")+files_in("apps/lab-runner/tests/fixtures")
    for p in app_paths:copy_file(p,CONTEXT/"app"/p.relative_to(APP))
    families=["transform/dbt","scripts/golden","tests/fixtures/data"]
    project_paths=[ROOT/name for name in ("data-generator/generate.py","ingestion/load_raw.py","serving/export_marts_snapshot.py","lake/curated_assets.json","contracts/data/retail-golden-v1.json","contracts/data/promotion-trust-v1.yaml","contracts/data/curated-release-manifest.schema.json")]
    for family in families:project_paths+=files_in(family)
    for p in project_paths:copy_file(p,CONTEXT/"project"/p.relative_to(ROOT))
    stage_families=["scripts/learning_contracts","learning/contracts","learning/labs/promotion-trust","learning/lessons/promotion-trust","learning/manifests"]
    for family in stage_families:
        names=subprocess.run(["git","ls-tree","-r","--name-only",STAGE_A,"--",family],cwd=ROOT,text=True,check=True,stdout=subprocess.PIPE).stdout.splitlines()
        for name in names:
            raw=subprocess.run(["git","show",f"{STAGE_A}:{name}"],cwd=ROOT,check=True,stdout=subprocess.PIPE).stdout
            target=CONTEXT/"project"/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw);os.chmod(target,0o644)
    wheels=BUILD/"wheelhouse"; manifest=json.loads((APP/"requirements/wheelhouse-manifest-v1.json").read_text())
    expected={row["file"]:row["sha256"] for row in manifest["wheels"]}
    observed={}
    for p in sorted(wheels.iterdir()):
        if p.is_symlink() or not p.is_file():raise SystemExit("WHEELHOUSE_TYPE_INVALID")
        observed[p.name]=sha(p);target=CONTEXT/"wheelhouse"/p.name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes());os.chmod(target,0o644)
    if observed!=expected:raise SystemExit("WHEELHOUSE_HASH_MISMATCH")
    rows=[]
    for p in sorted(x for x in CONTEXT.rglob("*") if x.is_file()):
        rows.append({"path":p.relative_to(CONTEXT).as_posix(),"mode":"0644","size":p.stat().st_size,"sha256":sha(p)})
    declared=json.loads((APP/"container/context-manifest-v1.json").read_text())
    if declared.get("files") != rows or declared.get("fileCount") != len(rows):
        raise SystemExit("CONTEXT_MANIFEST_HASH_MISMATCH")
    with tarfile.open(TAR,"w",format=tarfile.GNU_FORMAT) as tf:
        for p in sorted(CONTEXT.rglob("*")):
            info=tf.gettarinfo(str(p),p.relative_to(CONTEXT).as_posix());info.uid=0;info.gid=0;info.uname="";info.gname="";info.mtime=0
            if info.isfile():
                with p.open("rb") as f:tf.addfile(info,f)
            else:tf.addfile(info)
    return {"schemaVersion":"runner-context-observation-v1","files":rows,"tarSha256":sha(TAR)}


def main()->int:
    parser=argparse.ArgumentParser(allow_abbrev=False);parser.add_argument("--build",action="store_true");a=parser.parse_args()
    observation=build_context();print(json.dumps(observation,sort_keys=True,separators=(",",":")))
    if a.build:
        home=pathlib.Path(pwd.getpwuid(os.geteuid()).pw_dir);config=BUILD/"buildx-config";config.mkdir(mode=0o700,exist_ok=True)
        with TAR.open("rb") as stream:
            subprocess.run([str(home/".docker/cli-plugins/docker-buildx"),"build","--output","type=docker","--provenance=false","--sbom=false","--platform","linux/arm64","--network","none","--pull=false","--build-arg","SOURCE_DATE_EPOCH=0","--tag","ai-ready-lab-runner:issue9","-"],stdin=stream,check=True,env={"PATH":"/usr/local/bin:/usr/bin:/bin","HOME":str(BUILD),"DOCKER_CONFIG":str(config),"BUILDX_CONFIG":str(config),"DOCKER_HOST":f"unix://{home}/.orbstack/run/docker.sock"})
    return 0


if __name__=="__main__":raise SystemExit(main())
