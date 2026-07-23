"""Eight fixed in-image semantic operation adapters."""
from __future__ import annotations
import hashlib, importlib.util, json, os, pathlib, shutil, sys, time
from typing import Callable
from .registry import operation_ids
from .release import ASSETS, contract_schema_sha256, create_manifest, manifest_bytes, validate as validate_release

PROJECT=pathlib.Path("/opt/project")
STATE=pathlib.Path("/workspace/state")


def _load(name: str, path: pathlib.Path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError("RUNNER_BAKED_MODULE_MISSING")
    module=importlib.util.module_from_spec(spec)
    previous=sys.modules.get(name)
    sys.modules[name]=module
    try:
        spec.loader.exec_module(module)
    except BaseException:
        if previous is None:
            sys.modules.pop(name,None)
        else:
            sys.modules[name]=previous
        raise
    return module


def _base() -> None:
    STATE.mkdir(mode=0o700,parents=True,exist_ok=True)


def workspace_prepare() -> dict[str,object]:
    _base()
    marker={"schemaVersion":"runner-workspace-v1","profile":"small","seed":42,"state":"ready"}
    (STATE/"workspace.json").write_text(json.dumps(marker,sort_keys=True,separators=(",",":"))+"\n")
    return {"state":"ready","profile":"small","seed":42}


def retail_generate() -> dict[str,object]:
    _base(); raw=STATE/"data/raw"; raw.mkdir(parents=True,exist_ok=True)
    old=sys.argv
    try:
        sys.argv=["generate.py","--profile","small","--seed","42","--out",str(raw)]
        _load("runner_generator",PROJECT/"data-generator/generate.py").main()
    finally: sys.argv=old
    manifest=json.loads((raw/"manifest.json").read_text())
    if manifest.get("profile")!="small" or manifest.get("seed")!=42 or len(manifest.get("tables",{}))!=18:
        raise RuntimeError("RUNNER_GENERATOR_SEMANTICS_INVALID")
    return {"tables":18,"totalRows":sum(int(v["row_count"]) for v in manifest["tables"].values()),"manifestSha256":hashlib.sha256((raw/"manifest.json").read_bytes()).hexdigest()}


def retail_load() -> dict[str,object]:
    _base(); raw=STATE/"data/raw"; warehouse=STATE/"warehouse/retail.duckdb"
    module=_load("runner_loader",PROJECT/"ingestion/load_raw.py")
    counts=module.load_raw(raw,warehouse)
    if len(counts)!=18 or sum(counts.values())<6000: raise RuntimeError("RUNNER_LOAD_SEMANTICS_INVALID")
    return {"tables":len(counts),"totalRows":sum(counts.values())}


def _dbt_profile(warehouse:pathlib.Path)->str:
    return "retail_pipeline:\n  target: dev\n  outputs:\n    dev:\n      type: duckdb\n      path: "+json.dumps(str(warehouse))+"\n      threads: 1\n"


def retail_dbt_build() -> dict[str,object]:
    _base(); warehouse=STATE/"warehouse/retail.duckdb"; profiles=STATE/"dbt-profiles"; profiles.mkdir(exist_ok=True)
    (profiles/"profiles.yml").write_text(_dbt_profile(warehouse))
    target=STATE/"target"; logs=STATE/"logs"
    from dbt.cli.main import dbtRunner
    args=["build","--project-dir",str(PROJECT/"transform/dbt"),"--profiles-dir",str(profiles),"--target-path",str(target),"--log-path",str(logs),"--no-use-colors"]
    result=dbtRunner().invoke(args)
    if not result.success: raise RuntimeError("RUNNER_DBT_BUILD_FAILED")
    manifest=json.loads((target/"manifest.json").read_text())
    models=sum(1 for node in manifest["nodes"].values() if node.get("resource_type")=="model")
    if models!=51: raise RuntimeError("RUNNER_DBT_SEMANTICS_INVALID")
    return {"models":models,"manifestSha256":hashlib.sha256((target/"manifest.json").read_bytes()).hexdigest(),"dbtRunner":"dbt.cli.main.dbtRunner"}


def retail_export() -> dict[str,object]:
    _base(); module=_load("runner_exporter",PROJECT/"serving/export_marts_snapshot.py")
    export_dir=STATE/"serving/export";counts=module.export_marts(STATE/"warehouse/retail.duckdb",export_dir)
    if list(counts)!=list(ASSETS): raise RuntimeError("RUNNER_EXPORT_ORDER_INVALID")
    golden_module=_load("runner_golden_worker",PROJECT/"scripts/golden/golden_worker.py")
    golden=json.loads((PROJECT/"contracts/data/retail-golden-v1.json").read_text());semantic=[]
    import duckdb
    connection=duckdb.connect(str(STATE/"warehouse/retail.duckdb"),read_only=True)
    try:
        connection.execute("SET threads=1")
        for mart in ASSETS:
            target=export_dir/f"{mart}.parquet";temporary=export_dir/f".{mart}.parquet.tmp"
            connection.table(f"main_marts.{mart}").order("ALL").write_parquet(str(temporary))
            os.chmod(temporary,0o600)
            with temporary.open("rb") as stream:os.fsync(stream.fileno())
            os.replace(temporary,target)
        directory_fd=os.open(export_dir,os.O_RDONLY|os.O_DIRECTORY)
        try:os.fsync(directory_fd)
        finally:os.close(directory_fd)
        for expected in golden["marts"]:
            mart=expected["martId"];cursor=connection.execute("select * from query_table(?) order by all",[f"main_marts.{mart}"]);rows=cursor.fetchall();columns=[entry[0] for entry in cursor.description]
            digest=hashlib.sha256(golden_module.mart_csv(columns,rows)).hexdigest()
            if (len(rows),digest)!=(expected["rowCount"],expected["contentSha256"]):raise RuntimeError("RUNNER_EXPORT_GOLDEN_MISMATCH")
            semantic.append({"assetId":mart,"rowCount":len(rows),"contentSha256":digest})
    finally:connection.close()
    assets=validate_release(STATE)
    manifest=create_manifest(STATE,semantic);manifest_raw=manifest_bytes(manifest)
    return {"assets":assets,"rowCounts":counts,"semanticAssets":semantic,"releaseManifest":{"releaseId":manifest["releaseId"],"manifestSha256":hashlib.sha256(manifest_raw).hexdigest(),"contractSchemaSha256":contract_schema_sha256(),"assets":manifest["assets"]}}


def promotion_configure() -> dict[str,object]:
    _base(); config={"schemaVersion":"promotion-runner-config-v1","controlledFailure":"headline-revenue-overweighted","expectedEvidence":["METRIC_REFUND_NOT_ACCOUNTED"]}
    (STATE/"promotion-config.json").write_text(json.dumps(config,sort_keys=True,separators=(",",":"))+"\n")
    (STATE/"progress.json").write_text(json.dumps({"schemaVersion":"runner-progress-v1","state":"running"},sort_keys=True,separators=(",",":"))+"\n")
    return {"configured":True,"controlledFailure":config["controlledFailure"]}


def promotion_verify() -> dict[str,object]:
    _base()
    if not (STATE/"promotion-config.json").is_file(): raise RuntimeError("RUNNER_PROMOTION_NOT_CONFIGURED")
    lab=json.loads((PROJECT/"learning/labs/promotion-trust/lab-v1.json").read_text())
    assertion=lab["verify"]["assertions"][0]
    if assertion != {"id":"four-independent-grains","severity":"critical","failureCode":"PROMOTION_COMMON_GRAIN_FORBIDDEN"}:
        raise RuntimeError("RUNNER_PROMOTION_CONTRACT_INVALID")
    assets=validate_release(STATE)
    verifier=_load("runner_promotion_trust",PROJECT/"scripts/golden/promotion_trust.py")
    contract=verifier.load_contract();verifier.validate_contract(contract)
    import duckdb
    grains=[]
    for source in contract["sources"]:
        asset=str(source["sourceId"]);expected=tuple(source["grain"])
        parquet=STATE/"serving/export"/f"{asset}.parquet"
        columns=tuple(row[0] for row in duckdb.connect(":memory:").execute("DESCRIBE SELECT * FROM read_parquet(?)",[str(parquet)]).fetchall())
        if any(key not in columns for key in expected):raise RuntimeError("RUNNER_PROMOTION_GRAIN_INVALID")
        grains.append(set(expected))
    common=set.intersection(*grains)
    if common:raise RuntimeError("PROMOTION_COMMON_GRAIN_FORBIDDEN")
    promotion_columns=grains[0];returns_columns=tuple(row[0] for row in duckdb.connect(":memory:").execute("DESCRIBE SELECT * FROM read_parquet(?)",[str(STATE/"serving/export/mart_returns_analysis.parquet")]).fetchall())
    controlled_failure="total_refund_amount" not in promotion_columns and "total_refund_amount" in returns_columns
    if not controlled_failure:raise RuntimeError("METRIC_REFUND_NOT_ACCOUNTED")
    result={"schemaVersion":"promotion-verification-v1","decision":contract["decision"],"reason":contract["reason"],"assertions":[{"id":"four-independent-grains","status":"pass","observedCommonKeys":[]},{"id":"METRIC_REFUND_NOT_ACCOUNTED","status":"pass","observed":"refund-metric-is-independent-returns-grain"}],"assetCount":len(assets),"contractSha256":hashlib.sha256((PROJECT/"contracts/data/promotion-trust-v1.yaml").read_bytes()).hexdigest()}
    (STATE/"promotion-verification.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
    (STATE/"evidence.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
    return result


def workspace_reset() -> dict[str,object]:
    preserved={}
    for name in ("progress.json","evidence.json"):
        p=STATE/name
        if p.is_file(): preserved[name]=p.read_bytes()
    for child in list(STATE.iterdir()) if STATE.exists() else []:
        if child.name in preserved: continue
        if child.is_dir(): shutil.rmtree(child)
        else: child.unlink()
    result=workspace_prepare()
    for name,data in preserved.items(): (STATE/name).write_bytes(data)
    return {**result,"preserved":sorted(preserved)}


_ADAPTERS:dict[str,Callable[[],dict[str,object]]]={
"workspace.prepare":workspace_prepare,"retail.generate":retail_generate,"retail.load":retail_load,
"retail.dbt-build":retail_dbt_build,"retail.export":retail_export,
"promotion.configure":promotion_configure,"promotion.verify":promotion_verify,"workspace.reset":workspace_reset,
}
assert tuple(_ADAPTERS)==operation_ids()


def execute(operation_id:str)->dict[str,object]:
    return _ADAPTERS[operation_id]()
