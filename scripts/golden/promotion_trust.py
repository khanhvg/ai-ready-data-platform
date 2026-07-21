#!/usr/bin/env python3
"""Promotion evidence grain validator with an explicit no-attribution boundary."""
from __future__ import annotations
import pathlib, re
from typing import Any
import yaml

ROOT=pathlib.Path(__file__).resolve().parents[2]
EXPECTED=(
 ("mart_promotion_effectiveness", ("promo_name","channel")),
 ("mart_fulfillment_performance", ("carrier","region_name")),
 ("mart_returns_analysis", ("reason","category_name","region_name")),
 ("mart_data_quality", ("scenario",)),
)
FORBIDDEN_KEYS={"score","adr","customer_id","customerId","order_id","orderId","attestationCommitSha","mergeOrTagSha"}
class PromotionError(ValueError): pass
def load_contract() -> dict[str, Any]: return yaml.safe_load((ROOT/"contracts/data/promotion-trust-v1.yaml").read_text())
def validate_contract(value: dict[str, Any]) -> None:
    observed=tuple((item.get("sourceId"),tuple(item.get("grain",()))) for item in value.get("sources",()))
    if observed != EXPECTED: raise PromotionError("PROMOTION_GRAIN_MISMATCH")
    if value.get("decision") != "insufficient-evidence" or value.get("reason") != "no-common-grain":
        raise PromotionError("PROMOTION_HEADLINE_INSUFFICIENT")
    text=str(value).lower()
    if "caused" in text or "attributed to" in text: raise PromotionError("PROMOTION_ATTRIBUTION_FORBIDDEN")
def _walk(value: Any):
    if isinstance(value,dict):
        for key, child in value.items(): yield key, child; yield from _walk(child)
    elif isinstance(value,list):
        for child in value: yield from _walk(child)
def validate_fixture_candidate(value: dict[str, Any]) -> None:
    for key, child in _walk(value):
        if key in FORBIDDEN_KEYS or re.search(r"(?i)(password|secret|private.?key|token)", key):
            raise PromotionError("PROMOTION_FIXTURE_FORBIDDEN")
        if isinstance(child,str) and (child.startswith("/") or re.search(r"https?://[^/@]+:[^/@]+@",child)):
            raise PromotionError("PROMOTION_FIXTURE_FORBIDDEN")
