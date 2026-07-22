"""Exact eleven-asset release validation."""
from __future__ import annotations
import json, pathlib
ASSETS=("mart_daily_revenue","mart_top_products","mart_customer_cohorts","mart_fulfillment_performance","mart_returns_analysis","mart_promotion_effectiveness","mart_channel_geography","mart_inventory_health","mart_web_funnel_conversion","mart_supplier_purchasing","mart_data_quality")


def validate(workspace: pathlib.Path) -> list[dict[str,object]]:
    export=workspace/"serving/export"
    observed=sorted(p.stem for p in export.glob("*.parquet"))
    if observed != sorted(ASSETS) or len(list(export.iterdir())) != 11:
        raise RuntimeError("RUNNER_RELEASE_ASSET_SET_INVALID")
    rows=[]
    for asset in ASSETS:
        p=export/f"{asset}.parquet"
        if not p.is_file() or p.is_symlink() or p.stat().st_nlink!=1: raise RuntimeError("RUNNER_RELEASE_ASSET_INVALID")
        rows.append({"assetId":asset,"size":p.stat().st_size})
    return rows
