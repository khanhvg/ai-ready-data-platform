#!/usr/bin/env python3
"""Project-level C4 fitness and committed-output freshness checks."""
from __future__ import annotations
import hashlib, json, pathlib, platform, subprocess
from typing import Any
import yaml

ROOT=pathlib.Path(__file__).resolve().parents[2]
IDS=("C4-L0","C4-L1","C4-L2-LOCAL","C4-L3-RUNNER","DEP-LOCAL","DYN-JOURNEY")
KEYS=("index","c4_l1","c4_l2_local","c4_l3_runner","dep_local","dyn_journey")
class ArchitectureError(RuntimeError): pass

def check_tool_contract() -> None:
    if platform.system()!="Darwin" or platform.machine()!="arm64": raise ArchitectureError("ARCH_TOOL_MISSING")
    package=ROOT/"requirements/architecture/package.json"; lock=ROOT/"requirements/architecture/package-lock.json"
    if hashlib.sha256(package.read_bytes()).hexdigest()!="5cebd6d09ecef1334a492b871e388049392b6c0f6c9738873438b88958bd475d": raise ArchitectureError("ARCH_TOOL_LOCK_MISMATCH")
    if hashlib.sha256(lock.read_bytes()).hexdigest()!="7a56d803a47454023f40a04bcdb3b037f4ab2c2a05321292ad3b7f7225c2118c": raise ArchitectureError("ARCH_TOOL_LOCK_MISMATCH")
    if subprocess.check_output(["node","--version"],text=True).strip()!="v22.22.3" or subprocess.check_output(["npm","--version"],text=True).strip()!="10.9.8": raise ArchitectureError("ARCH_NODE_VERSION_MISMATCH")

def check_sources() -> None:
    manifest=yaml.safe_load((ROOT/"architecture/likec4/view-manifest.yaml").read_text())
    if tuple(row.get("id") for row in manifest.get("views",()))!=IDS or tuple(row.get("key") for row in manifest["views"])!=KEYS: raise ArchitectureError("ARCH_VIEW_SET_MISMATCH")
    required={"audience","concern","scope","type","id","key"}
    if any(set(row)<required for row in manifest["views"]): raise ArchitectureError("ARCH_C4_FITNESS_FAILED")
    sources=list((ROOT/"architecture/likec4/views").glob("*.c4"))
    if {path.stem for path in sources}!=set(IDS): raise ArchitectureError("ARCH_VIEW_SET_MISMATCH")
    model="\n".join(path.read_text() for path in (ROOT/"architecture/likec4").rglob("*.c4"))
    for term in ("Learner","Instructor and operator","Learning platform","Retail data platform","Command registry","Workspace manager","Verifier and evidence","Rill, Airflow, Iceberg, and OpenMetadata","Load","Complete"):
        if term not in model: raise ArchitectureError("ARCH_C4_FITNESS_FAILED")

def check_render_manifest() -> dict[str,Any]:
    path=ROOT/"architecture/rendered/render-manifest.json"
    value=json.loads(path.read_text())
    if tuple(row["id"] for row in value["views"])!=IDS: raise ArchitectureError("ARCH_VIEW_SET_MISMATCH")
    for row in value["views"]:
        for extension in ("svg","txt"):
            artifact=ROOT/"architecture/rendered"/f'{row["id"]}.{extension}'
            if hashlib.sha256(artifact.read_bytes()).hexdigest()!=row[f"{extension}Sha256"]: raise ArchitectureError("ARCH_OUTPUT_STALE")
    return value

def main() -> int:
    check_tool_contract(); check_sources(); check_render_manifest(); print("architecture-check: 6 views fresh"); return 0
if __name__=="__main__": raise SystemExit(main())
