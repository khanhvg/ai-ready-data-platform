"""Exact manifest-backed eleven-asset release admission and pointer publication."""
from __future__ import annotations
import hashlib, json, os, pathlib, shutil, stat
import jsonschema
ASSETS=("mart_daily_revenue","mart_top_products","mart_customer_cohorts","mart_fulfillment_performance","mart_returns_analysis","mart_promotion_effectiveness","mart_channel_geography","mart_inventory_health","mart_web_funnel_conversion","mart_supplier_purchasing","mart_data_quality")
INTEGRATION="5644f01b4c0443a81f3af0bcce80f44c847cd986"


def _sha(path:pathlib.Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_bytes(document:dict[str,object])->bytes:
    return json.dumps(document,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False).encode()


def _schema()->tuple[dict[str,object],str]:
    container=pathlib.Path("/opt/project/contracts/data/curated-release-manifest.schema.json")
    if container.is_file():path=container
    else:
        app=pathlib.Path(__file__).resolve().parents[2];root=app.parents[1];lock=json.loads((app/"container/context-manifest-v1.json").read_text());pin=next(row for row in lock["files"] if row["path"]=="project/contracts/data/curated-release-manifest.schema.json");path=root/"contracts/data/curated-release-manifest.schema.json"
        if _sha(path)!=pin["sha256"]:raise RuntimeError("RUNNER_RELEASE_CONTRACT_INVALID")
    raw=path.read_bytes();return json.loads(raw),hashlib.sha256(raw).hexdigest()


def contract_schema_sha256()->str:return _schema()[1]


def _golden()->dict[str,object]:
    container=pathlib.Path("/opt/project/contracts/data/retail-golden-v1.json")
    path=container if container.is_file() else pathlib.Path(__file__).resolve().parents[4]/"contracts/data/retail-golden-v1.json"
    return json.loads(path.read_text())


def _footer(raw:bytes)->str:
    if len(raw)<12 or not raw.startswith(b"PAR1") or not raw.endswith(b"PAR1"):raise RuntimeError("RUNNER_RELEASE_ASSET_INVALID")
    length=int.from_bytes(raw[-8:-4],"little")
    if length<=0 or length>len(raw)-12:raise RuntimeError("RUNNER_RELEASE_ASSET_INVALID")
    return hashlib.sha256(raw[-8-length:-8]).hexdigest()


def validate_assets(workspace:pathlib.Path)->list[dict[str,object]]:
    export=workspace/"serving/export"
    if not export.is_dir() or sorted(p.stem for p in export.glob("*.parquet"))!=sorted(ASSETS) or len(list(export.iterdir()))!=11:raise RuntimeError("RUNNER_RELEASE_ASSET_SET_INVALID")
    rows=[]
    for asset in ASSETS:
        path=export/f"{asset}.parquet";observed=path.stat(follow_symlinks=False)
        if not stat.S_ISREG(observed.st_mode) or path.is_symlink() or observed.st_nlink!=1 or stat.S_IMODE(observed.st_mode) not in (0o600,0o644):raise RuntimeError("RUNNER_RELEASE_ASSET_INVALID")
        raw=path.read_bytes();rows.append({"assetId":asset,"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"schemaSha256":_footer(raw)})
    return rows


def create_manifest(workspace:pathlib.Path,semantic:list[dict[str,object]])->dict[str,object]:
    assets=validate_assets(workspace);semantic_by_id={str(row["assetId"]):row for row in semantic}
    if list(semantic_by_id)!=list(ASSETS):raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
    schema,_=_schema();golden=_golden();data_run=_sha(workspace/"data/raw/manifest.json");engine="duckdb-1.5.4";lock=str(golden["inputIdentity"]["pythonLockSha256"])
    release_id=hashlib.sha256(json.dumps({"assets":assets,"semantic":semantic},sort_keys=True,separators=(",",":")).encode()).hexdigest()
    release=workspace/"curated/releases"/release_id;release.mkdir(mode=0o700,parents=True)
    rows=[]
    for row in assets:
        asset=str(row["assetId"]);source=workspace/"serving/export"/f"{asset}.parquet";target=release/asset;shutil.copyfile(source,target);os.chmod(target,0o600)
        rows.append({"assetId":asset,"releaseId":release_id,"dataRunId":data_run,"testedTreeSha":INTEGRATION,"lockSha256":lock,"contractSetId":"golden-contract-set-v1","engineSnapshotId":engine,"logicalFqn":f"retail_duckdb.retail.main_marts.{asset}","physicalFqn":f"retail_iceberg.default.retail.{asset}","schemaSha256":row["schemaSha256"],"contentSha256":str(semantic_by_id[asset]["contentSha256"]),"rowCount":int(semantic_by_id[asset]["rowCount"]),"stagedLocator":f"curated/releases/{release_id}/{asset}"})
    document={"schemaVersion":"curated-release-manifest-v1","releaseId":release_id,"dataRunId":data_run,"testedTreeSha":INTEGRATION,"lockSha256":lock,"contractSetId":"golden-contract-set-v1","engineSnapshotId":engine,"profile":"small","seed":42,"assets":rows}
    jsonschema.Draft202012Validator(schema).validate(document)
    manifest=release/"manifest.json";manifest.write_bytes(manifest_bytes(document));os.chmod(manifest,0o600)
    return validate_manifest(workspace)


def validate_manifest(workspace:pathlib.Path)->dict[str,object]:
    schema,_=_schema();root=workspace/"curated/releases";manifests=list(root.glob("*/manifest.json")) if root.is_dir() else []
    if len(manifests)!=1:raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
    manifest=manifests[0];document=json.loads(manifest.read_text())
    try:jsonschema.Draft202012Validator(schema).validate(document)
    except jsonschema.ValidationError as exc:raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID") from exc
    release_id=str(document["releaseId"]);release=root/release_id
    if manifest.parent!=release or {p.name for p in release.iterdir()}!={"manifest.json",*ASSETS} or [row["assetId"] for row in document["assets"]]!=list(ASSETS):raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
    raw_assets={row["assetId"]:row for row in validate_assets(workspace)}
    expected={row["martId"]:row for row in _golden()["marts"]}
    for row in document["assets"]:
        asset=str(row["assetId"]);path=workspace/str(row["stagedLocator"]);observed=path.stat(follow_symlinks=False);raw=path.read_bytes()
        semantic=expected[asset]
        if not stat.S_ISREG(observed.st_mode) or observed.st_nlink!=1 or stat.S_IMODE(observed.st_mode)!=0o600 or hashlib.sha256(raw).hexdigest()!=raw_assets[asset]["sha256"] or _footer(raw)!=row["schemaSha256"] or row["contentSha256"]!=semantic["contentSha256"] or row["rowCount"]!=semantic["rowCount"]:raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
        for field in ("releaseId","dataRunId","testedTreeSha","lockSha256","contractSetId","engineSnapshotId"):
            if row[field]!=document[field]:raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
        if row["logicalFqn"]!=f"retail_duckdb.retail.main_marts.{asset}" or row["physicalFqn"]!=f"retail_iceberg.default.retail.{asset}" or row["stagedLocator"]!=f"curated/releases/{release_id}/{asset}":raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
    if manifest.read_bytes()!=manifest_bytes(document):raise RuntimeError("RUNNER_RELEASE_MANIFEST_INVALID")
    return document


def validate(workspace:pathlib.Path)->list[dict[str,object]]:
    if (workspace/"curated/releases").exists():validate_manifest(workspace)
    return [{key:row[key] for key in ("assetId","size","sha256")} for row in validate_assets(workspace)]


def publish(root:pathlib.Path,result:dict[str,object])->pathlib.Path:
    release=dict(result.get("releaseManifest") or {});release_id=str(release.get("releaseId") or "");revision=result.get("workspaceRevision");run_id=result.get("runId");fence=result.get("fence")
    if len(release_id)!=64 or type(revision) is not int or not isinstance(run_id,str) or type(fence) is not int:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    schema,schema_sha=_schema()
    if release.get("contractSchemaSha256")!=schema_sha:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    assets=release.get("assets")
    if not isinstance(assets,list) or len(assets)!=11:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    first=dict(assets[0]);document={"schemaVersion":"curated-release-manifest-v1",**{key:first[key] for key in ("releaseId","dataRunId","testedTreeSha","lockSha256","contractSetId","engineSnapshotId")},"profile":"small","seed":42,"assets":assets}
    try:jsonschema.Draft202012Validator(schema).validate(document)
    except jsonschema.ValidationError as exc:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID") from exc
    raw_manifest=manifest_bytes(document)
    if hashlib.sha256(raw_manifest).hexdigest()!=release.get("manifestSha256"):raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    root.mkdir(mode=0o700,parents=True,exist_ok=True);os.chmod(root,0o700);generations=root/"generations";generations.mkdir(mode=0o700,exist_ok=True);manifests=root/"manifests";manifests.mkdir(mode=0o700,exist_ok=True)
    manifest=manifests/f"{release_id}.json"
    if manifest.exists() and manifest.read_bytes()!=raw_manifest:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    if not manifest.exists():
        temporary=manifests/f".{release_id}.{os.getpid()}.tmp";temporary.write_bytes(raw_manifest);os.chmod(temporary,0o600);fd=os.open(temporary,os.O_RDONLY);os.fsync(fd);os.close(fd);os.replace(temporary,manifest);fd=os.open(manifests,os.O_RDONLY);os.fsync(fd);os.close(fd)
    record={"schemaVersion":"runner-release-record-v1","releaseId":release_id,"runId":run_id,"fence":fence,"workspaceRevision":revision,"manifestSha256":release["manifestSha256"]};raw=json.dumps(record,sort_keys=True,separators=(",",":")).encode()+b"\n";generation=generations/f"{revision:020d}.json"
    if generation.exists() and generation.read_bytes()!=raw:raise RuntimeError("RUNNER_RELEASE_POINTER_INVALID")
    if not generation.exists():
        temporary=generations/f".{revision}.{os.getpid()}.tmp";temporary.write_bytes(raw);os.chmod(temporary,0o600);fd=os.open(temporary,os.O_RDONLY);os.fsync(fd);os.close(fd);os.replace(temporary,generation);fd=os.open(generations,os.O_RDONLY);os.fsync(fd);os.close(fd)
    revisions=sorted(int(path.stem) for path in generations.glob("*.json"))
    if revision<revisions[-1]:return generation
    pointer_path=root/"current.json";previous=None
    if pointer_path.is_file():
        current=json.loads(pointer_path.read_text())
        if revision==revisions[-1] and current.get("currentReleaseId")==release_id and current.get("manifestSha256")==release["manifestSha256"]:return generation
        previous=current.get("currentReleaseId")
    pointer={"schemaVersion":"curated-release-current-pointer-v1","currentReleaseId":release_id,"manifestSha256":release["manifestSha256"]}
    if isinstance(previous,str) and previous!=release_id:pointer["previousReleaseId"]=previous
    pointer_schema=dict(schema);pointer_schema["$ref"]="#/$defs/CuratedReleaseCurrentPointerV1";jsonschema.Draft202012Validator(pointer_schema).validate(pointer)
    pointer_raw=manifest_bytes(pointer);temporary=root/f".current.{os.getpid()}.tmp";temporary.write_bytes(pointer_raw);os.chmod(temporary,0o600);fd=os.open(temporary,os.O_RDONLY);os.fsync(fd);os.close(fd);os.replace(temporary,pointer_path);fd=os.open(root,os.O_RDONLY);os.fsync(fd);os.close(fd);return generation
