#!/usr/bin/env python3
"""Execute one exact small/42 pipeline inside a preallocated private runtime."""
from __future__ import annotations
import argparse, csv, datetime, hashlib, io, json, os, pathlib, shutil, subprocess, sys, time
from decimal import Decimal
from typing import Any
import duckdb, rfc8785
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import fitness, runtime

ROOT=pathlib.Path(__file__).resolve().parents[2]
EXPECTED_CSV={
"regions.csv":(5,"aa53262dffa42af91d54bb08b210950b9006f1d5fa05539db65c7fdc56066446"),"stores.csv":(20,"9500b325ab38d24436f0e7527e5d196ede91a6c41900392a8cb926a38e6a4ccf"),"product_categories.csv":(8,"b2f3b1157635ad1204550adcf202db74925c25b5111b610ed6e20e293e826bf5"),"products.csv":(150,"69f6670f4fc776137b6eb66b4b811ee7bff56f60f258245712ca211107534c65"),"customers.csv":(201,"6bb1bd567be4cd43abca76ea7e35ce2be08f8307c583ad6de2b9a123d7aa2e45"),"promotions.csv":(6,"94beef9b03a4d6eaccc104a0240a52777e0422c1ef636b16f8206509fb8c6de3"),"suppliers.csv":(10,"7c7d478912cffa95e86f95d9af8d95cbc0dbdd8f9cf1d23df9f5f1b779658e6f"),"purchase_orders.csv":(69,"c0b710c062f6f8ba86b7ae4722213fcff260b13ba3d27aa6d31e4f67c7048f06"),"purchase_order_items.csv":(188,"92c606b32704ef407f6f25dc977c6365b02172c7bc7beea4f2d15a71bff8b209"),"orders.csv":(1001,"1fa72d45cbb8680903ae149d3fa99d2ffad6787a24acdd99b0d1783a66969cd1"),"order_items.csv":(2136,"17a56e72564952e3b0c81b021d7a31a00ca42810eb4601a06cc507728ef534c2"),"payments.csv":(1000,"c67719cfec3be7c8448f4a1906044a8a9db148c92bb03a21c40a8ff651aec069"),"returns_refunds.csv":(56,"bf1e736d5e2e5b67ca2cd24dee65df5c020b345e48afabc01ed5974dc8007b44"),"inventory_movements.csv":(295,"c0d8cc6ef721fea76fed7e8b81a3a981807615c85fa746a597e0b04c4118f2c4"),"reviews.csv":(125,"b07705ff914640663dbee87cf49f469d066fb0d6ebf66804cd58c0874f796ce6"),"shipments.csv":(870,"d73d88f0b0efac24e0f1fb40179de6718320bf2d16abcc7aa427f475fe191611"),"web_sessions.csv":(200,"4a642f3f93e6c05cdc10c32e186d170f242af627b828666f21b76be385be25e4"),"web_events.csv":(472,"7942455445d7915e644a64f8c27c5438a0824e3e8e9a83d7d5f103d5903fd693")}
PROMOTION_SPECS=(
("mart_promotion_effectiveness",("promo_name","channel"),7,("gross_revenue","total_discount_amount","net_revenue","avg_order_value"),("discount_pct_of_gross",),"ratio-of-sums","no shared key with fulfillment, returns, or data-quality grains"),
("mart_fulfillment_performance",("carrier","region_name"),25,(),("on_time_pct","avg_lead_time_days"),"ratio-of-sums; lead time weighted by non-in-transit shipments","no shared key with promotion, returns, or data-quality grains"),
("mart_returns_analysis",("reason","category_name","region_name"),47,("total_refund_amount","avg_refund_amount"),(),"ratio-of-sums","no shared key with promotion, fulfillment, or data-quality grains"),
("mart_data_quality",("scenario",),10,(),(),"independent scenario count","aggregate diagnostic only; no cross-grain attribution"))
class WorkerError(RuntimeError): pass
def sha(data:bytes)->str:return hashlib.sha256(data).hexdigest()
def inventory(root:pathlib.Path)->list[dict[str,str]]:
    return [{"locator":path.relative_to(ROOT).as_posix(),"sha256":sha(path.read_bytes())} for path in sorted(root.rglob("*")) if path.is_file()]
def execute(command:list[str],cwd:pathlib.Path,env:dict[str,str],deadline:float)->tuple[bytes,bytes]:
    try: result=runtime.run(command,cwd=cwd,env=env,deadline=deadline)
    except runtime.RuntimeErrorTyped as exc: raise WorkerError(str(exc)) from exc
    return result.stdout,result.stderr
def json_safe(value:Any)->Any:
    if value is None or isinstance(value,(str,int,bool)): return value
    if isinstance(value,Decimal): return format(value,"f")
    if isinstance(value,float): return value
    if isinstance(value,(datetime.date,datetime.datetime)): return value.isoformat()
    return str(value)
def mart_csv(columns:list[str],rows:list[tuple[Any,...]])->bytes:
    buffer=io.StringIO(newline=""); writer=csv.writer(buffer,lineterminator="\n",quoting=csv.QUOTE_MINIMAL)
    writer.writerow(columns)
    for row in rows: writer.writerow(["" if value is None else (str(value).lower() if isinstance(value,bool) else str(value)) for value in row])
    return buffer.getvalue().encode()
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--run-root",type=pathlib.Path,required=True); parser.add_argument("--evidence-root",type=pathlib.Path,required=True); parser.add_argument("--tested-tree-sha",required=True); parser.add_argument("--budget",type=float,default=260); args=parser.parse_args()
    started_wall=datetime.datetime.now(datetime.timezone.utc); started=time.monotonic(); deadline=started+args.budget; run=args.run_root; evidence=args.evidence_root
    raw=run/"raw"; warehouse=run/"warehouse"/"retail.duckdb"; profiles=run/"profiles"; export=run/"export"
    for path in (raw,warehouse.parent,profiles,export,run/"dbt-build-target",run/"dbt-build-logs",run/"dbt-docs-target",run/"dbt-docs-logs"): path.mkdir(mode=0o700,parents=True,exist_ok=False)
    env=dict(os.environ); python=pathlib.Path(env["VIRTUAL_ENV"])/"bin/python"; dbt=pathlib.Path(env["VIRTUAL_ENV"])/"bin/dbt"
    execute([str(python),str(ROOT/"data-generator/generate.py"),"--profile","small","--seed","42","--out",str(raw)],ROOT,env,deadline)
    observed=[]
    for path in sorted(raw.glob("*.csv")):
        payload=path.read_bytes(); rows=max(0,payload.count(b"\n")-1); observed.append((path.name,rows,sha(payload)))
        if EXPECTED_CSV.get(path.name)!=(rows,sha(payload)): raise WorkerError("GOLDEN_INPUT_MISMATCH")
    if len(observed)!=18 or sum(row[1] for row in observed)!=6812: raise WorkerError("GOLDEN_INPUT_MISMATCH")
    execute([str(python),str(ROOT/"ingestion/load_raw.py"),"--raw-dir",str(raw),"--duckdb-path",str(warehouse)],ROOT,env,deadline)
    (profiles/"profiles.yml").write_text(f"retail_pipeline:\n  target: dev\n  outputs:\n    dev:\n      type: duckdb\n      path: '{warehouse}'\n      threads: 4\n")
    dbt_env={**env,"DBT_PROFILES_DIR":str(profiles),"DBT_TARGET_PATH":str(run/"dbt-build-target"),"DBT_LOG_PATH":str(run/"dbt-build-logs")}
    execute([str(dbt),"build"],ROOT/"transform/dbt",dbt_env,deadline)
    build_manifest=json.loads((run/"dbt-build-target/manifest.json").read_text()); build_results=json.loads((run/"dbt-build-target/run_results.json").read_text())
    dbt_env={**env,"DBT_PROFILES_DIR":str(profiles),"DBT_TARGET_PATH":str(run/"dbt-docs-target"),"DBT_LOG_PATH":str(run/"dbt-docs-logs")}
    execute([str(dbt),"docs","generate"],ROOT/"transform/dbt",dbt_env,deadline)
    execute([str(python),str(ROOT/"serving/export_marts_snapshot.py"),"--duckdb-path",str(warehouse),"--export-dir",str(export)],ROOT,env,deadline)
    statuses=[item["status"] for item in build_results["results"]]; passes=sum(status in {"pass","success"} for status in statuses); warns=statuses.count("warn"); fails=sum(status in {"error","fail","runtime error"} for status in statuses)
    if (passes,warns,fails,len(statuses))!=(179,7,0,186): raise WorkerError("DBT_RESULT_MISMATCH")
    resource_types=[node.get("resource_type") for node in build_manifest["nodes"].values()]
    if (resource_types.count("model"),resource_types.count("test"),len(build_manifest["sources"]))!=(51,141,18): raise WorkerError("DBT_GRAPH_MISMATCH")
    retail=json.loads((ROOT/"contracts/data/retail-golden-v1.json").read_text()); expected_marts={item["martId"]:(item["rowCount"],item["contentSha256"]) for item in retail["marts"]}
    con=duckdb.connect(str(warehouse),read_only=True); marts=[]; promotion=[]
    try:
        for item in retail["marts"]:
            mart=item["martId"]; schema_rows=con.execute(f"describe main_marts.{mart}").fetchall(); cursor=con.execute(f"select * from main_marts.{mart} order by all"); rows=cursor.fetchall(); columns=[entry[0] for entry in cursor.description]; digest=sha(mart_csv(columns,rows))
            if (len(rows),digest)!=expected_marts[mart]: raise WorkerError("MART_PROJECTION_MISMATCH")
            schema_projection=[{"columnName":row[0],"logicalType":row[1],"nullable":row[2]=="YES"} for row in schema_rows]
            null_positions=[[row_index,column_index] for row_index,row in enumerate(rows) for column_index,value in enumerate(row) if value is None]
            marts.append({"martId":mart,"rowCount":len(rows),"contentSha256":digest,"schemaSha256":sha(rfc8785.dumps(schema_projection)),"nullPositionsSha256":sha(rfc8785.dumps(null_positions))})
        for mart,grain,count,money,one_decimal,calculation,limitation in PROMOTION_SPECS:
            cursor=con.execute(f"select * from main_marts.{mart} order by all"); rows=cursor.fetchall(); columns=[entry[0] for entry in cursor.description]; records=[]
            for source_row in rows:
                record={key:json_safe(value) for key,value in zip(columns,source_row)}
                for key in money:
                    if record[key] is not None: record[key]=f"{float(record[key]):.2f}"
                for key in one_decimal:
                    if record[key] is not None: record[key]=f"{float(record[key]):.1f}"
                records.append(record)
            if len(records)!=count: raise WorkerError("PROMOTION_SOURCE_COUNT_MISMATCH")
            canonical=rfc8785.dumps(records)
            promotion.append({"sourceId":mart,"grain":list(grain),"order":list(grain),"filter":"full-input","calculation":calculation,"limitation":limitation,"rowCount":count,"sourceMartContentSha256":expected_marts[mart][1],"normalizedRecordsSha256":sha(canonical),"records":records})
    finally: con.close()
    promotion_bytes=rfc8785.dumps({"sources":promotion,"decision":"insufficient-evidence","reason":"no-common-grain"})
    curated=json.loads((ROOT/"lake/curated_assets.json").read_text())["assets"]
    curated_projection=[{"assetId":item["name"],"logicalFqn":f"retail_duckdb.retail.main_marts.{item['name']}","physicalFqn":f"retail_iceberg.default.retail.{item['name']}"} for item in curated]
    normative_marts=[{key:item[key] for key in ("martId","rowCount","contentSha256")} for item in marts]
    mart_summary=sha(rfc8785.dumps(normative_marts))
    if mart_summary!="4b8a16acd83064c374061a0f1eb4737e6b9fd6fe2fcaae3ec45a659dc684c84b": raise WorkerError("MART_SUMMARY_MISMATCH")
    projection={"schemaVersion":"golden-projection-v1","profile":"small","seed":42,"testedTreeSha":args.tested_tree_sha,"generator":{"fileCount":18,"totalRows":6812,"files":[{"file":name,"rowCount":rows,"csvSha256":digest} for name,rows,digest in observed]},"anomalies":{"generatorNullPromotionIds":1,"generatorInvalidStatuses":10,"martNullPromotionIds":879,"martInvalidStatuses":9},"dbt":{"modelCount":51,"genericTestCount":141,"sourceCount":18,"pass":passes,"warn":warns,"fail":fails,"total":len(statuses),"configuredWarningTests":9,"observedWarnings":7},"marts":marts,"martSummarySha256":mart_summary,"martExtendedSummarySha256":sha(rfc8785.dumps(marts)),"rill":{"files":inventory(ROOT/"serving/rill"),"modelCount":11,"metricsViewCount":11,"exploreCount":11},"airflow":{"dagSha256":sha((ROOT/"orchestration/airflow/dags/retail_batch_pipeline.py").read_bytes()),"defaultTaskIds":["seed","load_raw","health_check","dbt_build","dbt_docs_generate","export_marts_snapshot"],"defaultEdges":[["seed","load_raw"],["load_raw","health_check"],["health_check","dbt_build"],["dbt_build","dbt_docs_generate"],["dbt_docs_generate","export_marts_snapshot"]],"optionalTaskIds":["publish_iceberg","iceberg_read_back"],"optionalEdges":[["export_marts_snapshot","publish_iceberg"],["publish_iceberg","iceberg_read_back"]]},"curatedAssets":curated_projection,"metadataIdentities":{"files":inventory(ROOT/"governance/openmetadata"),"physicalService":"retail_iceberg","logicalService":"retail_duckdb","physicalEntityCount":11,"logicalMaterializedModelCount":45},"promotionTrust":{"sources":promotion,"decision":"insufficient-evidence","reason":"no-common-grain"},"promotionTrustSha256":sha(promotion_bytes),"dependencyFingerprints":{"pythonApplicationLockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2","pythonToolLockSha256":sha((ROOT/"requirements/golden-lock-tools.lock").read_bytes()),"pythonFreezeSha256":"cdb87ed71e0996f90041371cc25138afa02d78b134cbdc4afe9c25baa6649bba","architecturePackageSha256":sha((ROOT/"requirements/architecture/package.json").read_bytes()),"architectureLockSha256":sha((ROOT/"requirements/architecture/package-lock.json").read_bytes())},"contractFingerprints":{"schemaRegistrySha256":sha((ROOT/"learning/contracts/schema-version-registry.json").read_bytes()),"retailGoldenSha256":sha((ROOT/"contracts/data/retail-golden-v1.json").read_bytes()),"promotionTrustSha256":sha((ROOT/"contracts/data/promotion-trust-v1.yaml").read_bytes()),"curatedReleaseSha256":sha((ROOT/"contracts/data/curated-release-manifest.schema.json").read_bytes())},"architecture":{"sourceFiles":inventory(ROOT/"architecture/likec4"),"renderedFiles":inventory(ROOT/"architecture/rendered")},"architectureRenderManifestSha256":sha((ROOT/"architecture/rendered/render-manifest.json").read_bytes()),"pythonLockSha256":"f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"}
    projection_bytes=rfc8785.dumps(projection); projection_sha=sha(projection_bytes)
    now=datetime.datetime.now(datetime.timezone.utc); raw_index={"schemaVersion":"golden-raw-index-v1","run":{"runId":run.name,"startedAt":now.isoformat().replace("+00:00","Z"),"finishedAt":now.isoformat().replace("+00:00","Z"),"durationMs":round((time.monotonic()-started)*1000),"workspaceLocator":f"golden/{run.name}"},"semanticProjectionSha256":projection_sha,"pythonLockSha256":projection["pythonLockSha256"],"testedTreeSha":args.tested_tree_sha}
    payload={"testedTreeSha":args.tested_tree_sha,"profile":"small","seed":42,"lockSha256":projection["pythonLockSha256"],"toolchain":{"python":"3.12","dbt":"1.11.12","duckdb":"1.5.4"},"projection":{"sha256":projection_sha},"artifacts":[{"locator":"raw.json","sha256":sha(rfc8785.dumps(raw_index))},{"locator":"projection.json","sha256":projection_sha}]}
    envelope={"schemaVersion":"golden-evidence-envelope-v1","payload":payload,"integrity":{"canonicalization":"rfc8785-jcs-v1","algorithm":"sha-256","payloadSha256":sha(rfc8785.dumps(payload))}}
    for name,data in (("raw.json",rfc8785.dumps(raw_index)),("projection.json",projection_bytes),("envelope.json",rfc8785.dumps(envelope))):
        (evidence/name).write_bytes(data); os.chmod(evidence/name,0o600)
    duration_ms=raw_index["run"]["durationMs"]
    result=fitness.passed(command_id="golden-clean",tested_tree_sha=args.tested_tree_sha,projection_sha256=projection_sha,started_at=started_wall,duration_ms=duration_ms,requested={"profile":"small","seed":42},locators={"raw":"raw.json","projection":"projection.json","envelope":"envelope.json"},toolchain={"python":"3.12","dbt":"1.11.12","duckdb":"1.5.4"},artifacts=[{"locator":name,"sha256":sha((evidence/name).read_bytes())} for name in ("raw.json","projection.json","envelope.json")])
    (evidence/"result.json").write_text(json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(evidence/"result.json",0o600)
    print(json.dumps({"result":"pass","durationMs":duration_ms,"projectionSha256":projection_sha,"evidence":f"golden/{evidence.name}"},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
