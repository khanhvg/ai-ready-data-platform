from __future__ import annotations

import pathlib
import json
import os
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]
DBT = ROOT / "transform/dbt"


class DbtCharacterizationTests(unittest.TestCase):
    def test_exact_model_layer_inventory(self) -> None:
        expected = {"staging": 18, "intermediate": 6, "core": 16, "marts": 11}
        actual = {
            layer: len(list((DBT / "models" / layer).glob("*.sql")))
            for layer in expected
        }
        self.assertEqual(expected, actual)
        self.assertEqual(51, sum(actual.values()))

    def test_exact_source_and_singular_test_inventory(self) -> None:
        source_text = (DBT / "models/staging/_sources.yml").read_text(encoding="utf-8")
        table_names = [
            line for line in source_text.splitlines() if line.startswith("      - name:")
        ]
        self.assertEqual(18, len(table_names))
        singular = sorted(path.name for path in (DBT / "tests").glob("*.sql"))
        self.assertEqual(["assert_non_negative_shipment_lead_time.sql"], singular)

    def test_build_capture_contract_is_required(self) -> None:
        schema = ROOT / "learning/contracts/golden-evidence-v1.schema.json"
        self.assertTrue(schema.is_file(), "P1-RED-EVIDENCE-SCHEMA-MISSING")

    def test_private_runtime_build_results_when_supplied(self) -> None:
        locator = os.environ.get("GOLDEN_DBT_BUILD_RESULTS")
        if locator is None:
            return
        results = json.loads(pathlib.Path(locator).read_text(encoding="utf-8"))["results"]
        statuses = [row["status"] for row in results]
        self.assertEqual(186, len(statuses))
        self.assertEqual(179, statuses.count("pass") + statuses.count("success"))
        self.assertEqual(7, statuses.count("warn"))
        self.assertEqual(0, statuses.count("error"))


if __name__ == "__main__":
    unittest.main()
