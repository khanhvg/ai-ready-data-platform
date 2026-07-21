#!/usr/bin/env python3
"""Construct the shared, bounded fitness-result-v1 pass envelope."""
from __future__ import annotations
import datetime, hashlib
from typing import Any

LOCK_SHA="f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"
def passed(*,command_id:str,tested_tree_sha:str,projection_sha256:str,started_at:datetime.datetime,duration_ms:int,requested:dict[str,Any]|None=None,artifacts:list[dict[str,Any]]|None=None,locators:dict[str,str|None]|None=None,toolchain:dict[str,str]|None=None)->dict[str,Any]:
    finished=started_at+datetime.timedelta(milliseconds=duration_ms)
    return {"schemaVersion":"fitness-result-v1","commandId":command_id,"owner":"I5-01","requested":requested or {},"status":"pass","failureCode":None,"remediation":None,"testedTreeSha":tested_tree_sha,"toolchain":toolchain or {"python":"3.12"},"lockSha256":LOCK_SHA,"startedAt":started_at.isoformat().replace("+00:00","Z"),"finishedAt":finished.isoformat().replace("+00:00","Z"),"durationMs":duration_ms,"rawLocator":(locators or {}).get("raw"),"projectionLocator":(locators or {}).get("projection"),"envelopeLocator":(locators or {}).get("envelope"),"projectionSha256":projection_sha256,"artifacts":artifacts or []}
