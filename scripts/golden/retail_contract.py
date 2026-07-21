#!/usr/bin/env python3
"""Semantic reader for the immutable retail golden contract."""
from __future__ import annotations
import json, pathlib
from typing import Any

ROOT=pathlib.Path(__file__).resolve().parents[2]
class RetailContractError(ValueError): pass
def read(path:pathlib.Path=ROOT/"contracts/data/retail-golden-v1.json")->dict[str,Any]:
    value=json.loads(path.read_text())
    if value.get("schemaVersion")!="retail-golden-v1" or len(value.get("marts",()))!=11: raise RetailContractError("RETAIL_GOLDEN_INVALID")
    ids=[item["martId"] for item in value["marts"]]
    if len(ids)!=len(set(ids)): raise RetailContractError("RETAIL_GOLDEN_DUPLICATE_ID")
    if (value["generator"]["fileCount"],value["generator"]["totalRows"])!=(18,6812): raise RetailContractError("GOLDEN_INPUT_MISMATCH")
    return value
