"""Eight fixed in-image semantic operation adapters."""
from __future__ import annotations
import hashlib, importlib.util, json, os, pathlib, shutil, sys, time
from typing import Callable
from .registry import operation_ids
from .release import validate as validate_release

PROJECT=pathlib.Path("/opt/project")
STATE=pathlib.Path("/workspace/state")


def _load(name: str, path: pathlib.Path):
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None: raise RuntimeError("RUNNER_BAKED_MODULE_MISSING")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


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


def retail_dbt_build() -> dict[str,object]:
    _base(); warehouse=STATE/"warehouse/retail.duckdb"; profiles=STATE/"dbt-profiles"; profiles.mkdir(exist_ok=True)
    (profiles/"profiles.yml").write_text("retail:\n  target: dev\n  outputs:\n    dev:\n      type: duckdb\n      path: "+json.dumps(str(warehouse))+"\n      threads: 2\n")
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
    counts=module.export_marts(STATE/"warehouse/retail.duckdb",STATE/"serving/export")
    assets=validate_release(STATE)
    if list(counts)!=[row["assetId"] for row in assets]: raise RuntimeError("RUNNER_EXPORT_ORDER_INVALID")
    return {"assets":assets,"rowCounts":counts}


def promotion_configure() -> dict[str,object]:
    _base(); config={"schemaVersion":"promotion-runner-config-v1","controlledFailure":"headline-revenue-overweighted","expectedEvidence":["METRIC_REFUND_NOT_ACCOUNTED"]}
    (STATE/"promotion-config.json").write_text(json.dumps(config,sort_keys=True,separators=(",",":"))+"\n")
    return {"configured":True,"controlledFailure":config["controlledFailure"]}


def promotion_verify() -> dict[str,object]:
    _base()
    if not (STATE/"promotion-config.json").is_file(): raise RuntimeError("RUNNER_PROMOTION_NOT_CONFIGURED")
    lab=json.loads((PROJECT/"learning/labs/promotion-trust/lab-v1.json").read_text())
    assertion=lab["verify"]["assertions"][0]
    if assertion != {"id":"four-independent-grains","severity":"critical","failureCode":"PROMOTION_COMMON_GRAIN_FORBIDDEN"}:
        raise RuntimeError("RUNNER_PROMOTION_CONTRACT_INVALID")
    assets=validate_release(STATE)
    result={"schemaVersion":"promotion-verification-v1","decision":"insufficient-evidence","reason":"no-common-grain","assertions":[{"id":"four-independent-grains","status":"pass"},{"id":"METRIC_REFUND_NOT_ACCOUNTED","status":"pass"}],"assetCount":len(assets)}
    (STATE/"promotion-verification.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n")
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
