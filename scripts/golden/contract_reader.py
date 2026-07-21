#!/usr/bin/env python3
"""Closed semantic contract reader used by mutation and third-reader checks."""
from __future__ import annotations
import json, pathlib
from typing import Any

class ContractError(ValueError): pass
def read_closed(path:pathlib.Path,required:tuple[str,...])->dict[str,Any]:
    value=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value,dict) or tuple(value)!=required: raise ContractError("CONTRACT_FIELD_SET_MISMATCH")
    return value
