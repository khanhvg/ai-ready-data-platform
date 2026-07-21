#!/usr/bin/env python3
"""Finalize actual LikeC4 computed JSON + WASM Graphviz output as one six-view set."""
from __future__ import annotations
import argparse, hashlib, json, pathlib
import yaml
from architecture_render import IDS, normalize_svg

ROOT=pathlib.Path(__file__).resolve().parents[2]
def sha(data:bytes)->str: return hashlib.sha256(data).hexdigest()
def semantic_text(external:str,row:dict,view:dict)->bytes:
    lines=[f"ID: {external}",f"Title: {view['title']}",f"Type: {row['type']}",f"Audience: {row['audience']}",f"Concern: {row['concern']}",f"Scope: {row['scope']}","Owner: I5-01",f"Legend: C4 elements and labelled unidirectional relations",""]
    lines.append("Elements:")
    for node in sorted(view["nodes"],key=lambda item:item["id"]):
        description=(node.get("description") or {}).get("txt","")
        lines.append(f"- {node['id']} | {node.get('kind','element')} | {node['title']} | {description} | parent={node.get('parent') or 'none'}")
    lines.append(""); lines.append("Relations:")
    edges=view["edges"] if view.get("_type")=="dynamic" else sorted(view["edges"],key=lambda item:(item["source"],item["target"],item.get("label") or ""))
    for ordinal,edge in enumerate(edges,1):
        prefix=f"{ordinal}. " if view.get("_type")=="dynamic" else "- "
        technology=(edge.get("description") or {}).get("txt","")
        suffix=f" | {technology}" if technology else ""
        lines.append(f"{prefix}{edge['label']}: {edge['source']} -> {edge['target']}{suffix}")
    lines.extend(["","Limitations: descriptive architecture only; future context is not implemented or a runtime dependency."])
    return ("\n".join(lines)+"\n").encode()
def main()->int:
    parser=argparse.ArgumentParser(); parser.add_argument("--stage",type=pathlib.Path,required=True); parser.add_argument("--out",type=pathlib.Path,required=True); args=parser.parse_args()
    args.out.mkdir(mode=0o700,parents=True,exist_ok=False)
    model=json.loads((args.stage/"model.json").read_text()); manifest=yaml.safe_load((ROOT/"architecture/likec4/view-manifest.yaml").read_text())
    if tuple(model["views"]) != ("index","c4_l1","c4_l2_local","c4_l3_runner","dep_local","dyn_journey"): raise RuntimeError("ARCH_VIEW_SET_MISMATCH")
    rows=[]
    for row in manifest["views"]:
        external=row["id"]; view=model["views"][row["key"]]
        text=semantic_text(external,row,view)
        svg=normalize_svg((args.stage/"raw-svg"/f"{external}.raw.svg").read_text(),view["title"],f"{row['type']} view for {row['audience']}: {row['concern']}")
        (args.out/f"{external}.txt").write_bytes(text); (args.out/f"{external}.svg").write_bytes(svg)
        rows.append({"id":external,"key":row["key"],"type":row["type"],"svgBytes":len(svg),"svgSha256":sha(svg),"txtBytes":len(text),"txtSha256":sha(text)})
    closure=hashlib.sha256()
    for path in sorted((ROOT/"architecture/likec4").rglob("*")):
        if path.is_file(): closure.update(path.relative_to(ROOT).as_posix().encode()); closure.update(path.read_bytes())
    result={"schemaVersion":"architecture-render-manifest-v1","toolchain":{"node":"22.22.3","npm":"10.9.8","likec4":"1.59.1","wasmGraphviz":"1.22.2","graphviz":"15.0.0"},"sourceClosureSha256":closure.hexdigest(),"packageLockSha256":"7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c","views":rows,"reviewStatus":"fitness-validated","integrityClaim":"local-corruption-detection-not-authenticity"}
    (args.out/"render-manifest.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(f"architecture-finalize: {len(rows)} views")
    return 0
if __name__=="__main__": raise SystemExit(main())
