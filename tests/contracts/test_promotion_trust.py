from __future__ import annotations
import importlib.util, pathlib, unittest, json, jsonschema
ROOT = pathlib.Path(__file__).resolve().parents[2]

class PromotionTrustTests(unittest.TestCase):
    def _load(self):
        contract = ROOT / "contracts/data/promotion-trust-v1.yaml"; module = ROOT / "scripts/golden/promotion_trust.py"
        if not contract.is_file() or not module.is_file(): raise AssertionError("P5-RED-FOUR-GRAINS\nP5-RED-INSUFFICIENT-EVIDENCE\nP5-RED-FIXTURE-DENYLIST")
        spec = importlib.util.spec_from_file_location("golden_promotion", module); assert spec and spec.loader
        loaded = importlib.util.module_from_spec(spec); spec.loader.exec_module(loaded); return loaded
    def test_four_independent_grains_and_decision(self) -> None:
        module = self._load(); value = module.load_contract()
        jsonschema.Draft202012Validator(json.loads((ROOT/"learning/contracts/promotion-trust-v1.schema.json").read_text())).validate(value)
        self.assertEqual(4, len(value["sources"])); self.assertEqual("insufficient-evidence", value["decision"])
        module.validate_contract(value)
    def test_fixture_fields_are_denylisted(self) -> None:
        module = self._load()
        for field in ("score", "adr", "customer_id", "attestationCommitSha", "mergeOrTagSha"):
            with self.subTest(field=field), self.assertRaisesRegex(module.PromotionError, "PROMOTION_FIXTURE_FORBIDDEN"):
                module.validate_fixture_candidate({field: "x"})

if __name__ == "__main__": unittest.main()
