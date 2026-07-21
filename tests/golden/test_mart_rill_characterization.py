from __future__ import annotations

import pathlib
import os
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
MART_IDS = [
    "mart_daily_revenue", "mart_top_products", "mart_customer_cohorts",
    "mart_fulfillment_performance", "mart_returns_analysis",
    "mart_promotion_effectiveness", "mart_channel_geography",
    "mart_inventory_health", "mart_web_funnel_conversion",
    "mart_supplier_purchasing", "mart_data_quality",
]


class MartRillCharacterizationTests(unittest.TestCase):
    ROW_COUNTS = [319, 149, 97, 25, 47, 7, 14, 149, 15, 10, 10]
    def test_exact_current_mart_and_rill_sets(self) -> None:
        dbt = sorted(path.stem for path in (ROOT / "transform/dbt/models/marts").glob("mart_*.sql"))
        models = sorted(path.stem for path in (ROOT / "serving/rill/models").glob("*.sql"))
        metrics = sorted(path.stem.removesuffix("_metrics") for path in (ROOT / "serving/rill/metrics").glob("*.yaml"))
        self.assertEqual(sorted(MART_IDS), dbt)
        self.assertEqual(sorted(MART_IDS), models)
        self.assertEqual(11, len(metrics))

    def test_weighted_and_unweighted_expressions_remain_distinct(self) -> None:
        fulfillment = (ROOT / "serving/rill/metrics/fulfillment_performance_metrics.yaml").read_text(encoding="utf-8")
        daily = (ROOT / "serving/rill/metrics/daily_revenue_metrics.yaml").read_text(encoding="utf-8")
        self.assertIn("shipment_count - in_transit_count", fulfillment)
        self.assertIn("AVG(avg_order_value)", daily)

    def test_private_runtime_mart_rows_when_supplied(self) -> None:
        locator = os.environ.get("GOLDEN_WAREHOUSE")
        if locator is None:
            return
        import duckdb
        connection = duckdb.connect(locator, read_only=True)
        try:
            actual = [connection.execute(f"select count(*) from main_marts.{name}").fetchone()[0] for name in MART_IDS]
        finally:
            connection.close()
        self.assertEqual(self.ROW_COUNTS, actual)


if __name__ == "__main__":
    unittest.main()
