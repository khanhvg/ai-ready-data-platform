from __future__ import annotations
import json, pathlib, unittest, jsonschema
ROOT = pathlib.Path(__file__).resolve().parents[2]

class RetailGoldenContractTests(unittest.TestCase):
    def test_exact_baseline_identity_and_distinctions(self) -> None:
        path = ROOT / "contracts/data/retail-golden-v1.json"
        if not path.is_file(): self.fail("P5-RED-RETAIL-CONTRACT")
        value = json.loads(path.read_text())
        jsonschema.Draft202012Validator(json.loads((ROOT/"learning/contracts/retail-golden-v1.schema.json").read_text())).validate(value)
        self.assertEqual((18, 6812), (value["generator"]["fileCount"], value["generator"]["totalRows"]))
        self.assertEqual((51, 141, 18), (value["dbt"]["modelCount"], value["dbt"]["genericTestCount"], value["dbt"]["sourceCount"]))
        self.assertEqual((179, 7, 0, 186), tuple(value["dbt"]["build"][key] for key in ("pass", "warn", "fail", "total")))
        self.assertEqual((9, 7), (value["dbt"]["configuredWarningTests"], value["dbt"]["observedWarnings"]))
        self.assertEqual((1, 10, 879, 9), tuple(value["anomalies"][key] for key in ("generatorNullPromotionIds", "generatorInvalidStatuses", "martNullPromotionIds", "martInvalidStatuses")))
        self.assertEqual(11, len(value["marts"]))

if __name__ == "__main__": unittest.main()
