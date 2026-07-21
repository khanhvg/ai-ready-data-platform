from __future__ import annotations

import pathlib
import unittest

from scripts.learning_contracts.check import _validate_schema_instance


ROOT = pathlib.Path(__file__).resolve().parents[3]


class PromotionTrustManifestTests(unittest.TestCase):
    def test_manifest_matches_closed_schema(self) -> None:
        self.assertIsNone(_validate_schema_instance(
            ROOT / "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
            ROOT / "learning/manifests/promotion-trust-v1.json",
        ))


if __name__ == "__main__":
    unittest.main()
