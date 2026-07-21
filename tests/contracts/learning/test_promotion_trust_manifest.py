from __future__ import annotations

import pathlib
import unittest

from scripts.learning_contracts.check import _validate_schema_instance
from scripts.learning_contracts import fitness, schema


ROOT = pathlib.Path(__file__).resolve().parents[3]


class PromotionTrustManifestTests(unittest.TestCase):
    def test_manifest_matches_closed_schema(self) -> None:
        self.assertIsNone(_validate_schema_instance(
            ROOT / "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
            ROOT / "learning/manifests/promotion-trust-v1.json",
        ))

    def test_review_h4_promotion_uses_resolved_structured_documents(self) -> None:
        manifest = schema.read_document(
            ROOT / "learning/manifests/promotion-trust-v1.json",
            family="promotion-manifest",
        )
        for key in ("lesson", "lab", "evidenceSchema", "dataContract", "fixture"):
            self.assertEqual({"path", "sha256"}, set(manifest[key]), key)
        for source in manifest["sources"]:
            self.assertEqual({"grain", "keys", "document"}, set(source))
            self.assertEqual({"path", "sha256"}, set(source["document"]))
        for limitation in manifest["limitations"]:
            self.assertEqual({"id", "statement"}, set(limitation))
        result = fitness.evaluate_promotion_document(
            ROOT / "learning/manifests/promotion-trust-v1.json",
            root=ROOT,
        )
        self.assertEqual(4, result["independentGrainCount"])
        self.assertEqual([], result["commonKeys"])


if __name__ == "__main__":
    unittest.main()
