#!/usr/bin/env python3
"""Validate and display the exact issue #5 command ownership registry."""
from __future__ import annotations
import datetime, hashlib, json, os, pathlib, secrets, subprocess, sys, time
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent)); import fitness, source_state, workspace as workspace_core

ROOT=pathlib.Path(__file__).resolve().parents[2]
REGISTRY=ROOT/"learning/contracts/command-owner-registry-v1.json"
ISSUE6=("help","golden-clean","data-contracts-check","evidence-contracts-check","migration-contracts-check","architecture-check","architecture-render")
def main()->int:
    source=source_state.identity(); started_wall=datetime.datetime.now(datetime.timezone.utc); started=time.monotonic()
    value=json.loads(REGISTRY.read_text()); rows=value["commands"]
    if len(rows)!=54 or len({row["command"] for row in rows})!=54 or len({row["owner"] for row in rows})!=14: raise SystemExit("COMMAND_REGISTRY_INVALID")
    implemented=tuple(row["command"] for row in rows if row["availability"]=="implemented")
    if implemented!=ISSUE6: raise SystemExit("COMMAND_REGISTRY_OWNERSHIP_INVALID")
    make=(ROOT/"Makefile").read_text()+"\n"+(ROOT/"mk/issue-5/i5-01.mk").read_text()
    for row in rows:
        if row["availability"]=="future-owner" and f'\n{row["command"]}:' in "\n"+make: raise SystemExit("COMMAND_REGISTRY_FUTURE_RECIPE")
        print(f'{row["command"]:<34} {row["owner"]:<5} {row["availability"]}')
    run=secrets.token_hex(16); owner=workspace_core.allocate_family(("evidence","command-registry"),"command-registry",run); out=owner.path
    source_state.assert_unchanged(source)
    payload=fitness.passed(command_id="help",tested_tree_sha=source[0],projection_sha256=hashlib.sha256(REGISTRY.read_bytes()).hexdigest(),started_at=started_wall,duration_ms=round((time.monotonic()-started)*1000))
    (out/"result.json").write_text(json.dumps(payload,sort_keys=True,separators=(",",":"))+"\n"); os.chmod(out/"result.json",0o600)
    print(f"evidence=command-registry/{run}/result.json"); owner.close()
    return 0
if __name__=="__main__": raise SystemExit(main())
