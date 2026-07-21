from __future__ import annotations

import ast
import csv
import hashlib
import io
import os
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class GeneratorCharacterizationTests(unittest.TestCase):
    EXPECTED = {
        "regions.csv": (5, "aa53262dffa42af91d54bb08b210950b9006f1d5fa05539db65c7fdc56066446"),
        "stores.csv": (20, "9500b325ab38d24436f0e7527e5d196ede91a6c41900392a8cb926a38e6a4ccf"),
        "product_categories.csv": (8, "b2f3b1157635ad1204550adcf202db74925c25b5111b610ed6e20e293e826bf5"),
        "products.csv": (150, "69f6670f4fc776137b6eb66b4b811ee7bff56f60f258245712ca211107534c65"),
        "customers.csv": (201, "6bb1bd567be4cd43abca76ea7e35ce2be08f8307c583ad6de2b9a123d7aa2e45"),
        "promotions.csv": (6, "94beef9b03a4d6eaccc104a0240a52777e0422c1ef636b16f8206509fb8c6de3"),
        "suppliers.csv": (10, "7c7d478912cffa95e86f95d9af8d95cbc0dbdd8f9cf1d23df9f5f1b779658e6f"),
        "purchase_orders.csv": (69, "c0b710c062f6f8ba86b7ae4722213fcff260b13ba3d27aa6d31e4f67c7048f06"),
        "purchase_order_items.csv": (188, "92c606b32704ef407f6f25dc977c6365b02172c7bc7beea4f2d15a71bff8b209"),
        "orders.csv": (1001, "1fa72d45cbb8680903ae149d3fa99d2ffad6787a24acdd99b0d1783a66969cd1"),
        "order_items.csv": (2136, "17a56e72564952e3b0c81b021d7a31a00ca42810eb4601a06cc507728ef534c2"),
        "payments.csv": (1000, "c67719cfec3be7c8448f4a1906044a8a9db148c92bb03a21c40a8ff651aec069"),
        "returns_refunds.csv": (56, "bf1e736d5e2e5b67ca2cd24dee65df5c020b345e48afabc01ed5974dc8007b44"),
        "inventory_movements.csv": (295, "c0d8cc6ef721fea76fed7e8b81a3a981807615c85fa746a597e0b04c4118f2c4"),
        "reviews.csv": (125, "b07705ff914640663dbee87cf49f469d066fb0d6ebf66804cd58c0874f796ce6"),
        "shipments.csv": (870, "d73d88f0b0efac24e0f1fb40179de6718320bf2d16abcc7aa427f475fe191611"),
        "web_sessions.csv": (200, "4a642f3f93e6c05cdc10c32e186d170f242af627b828666f21b76be385be25e4"),
        "web_events.csv": (472, "7942455445d7915e644a64f8c27c5438a0824e3e8e9a83d7d5f103d5903fd693"),
    }

    def test_current_generator_has_exact_profile_and_output_seams(self) -> None:
        source = (ROOT / "data-generator/generate.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        self.assertIn('"small"', source)
        self.assertIn('"demo-large"', source)
        self.assertIn("--out", source)
        self.assertIn("generated_at", source)
        self.assertTrue(any(isinstance(node, ast.FunctionDef) for node in ast.walk(tree)))

    def test_retail_contract_is_required_before_publication(self) -> None:
        path = ROOT / "contracts/data/retail-golden-v1.json"
        self.assertTrue(path.is_file(), "P1-RED-RETAIL-CONTRACT-MISSING")

    def test_private_runtime_csv_bytes_when_supplied(self) -> None:
        locator = os.environ.get("GOLDEN_RAW_DIR")
        if locator is None:
            return
        raw_dir = pathlib.Path(locator)
        self.assertEqual(set(self.EXPECTED), {path.name for path in raw_dir.glob("*.csv")})
        for name, (row_count, digest) in self.EXPECTED.items():
            data = (raw_dir / name).read_bytes()
            self.assertEqual(digest, hashlib.sha256(data).hexdigest(), name)
            rows = sum(1 for _ in csv.reader(io.StringIO(data.decode("utf-8")))) - 1
            self.assertEqual(row_count, rows, name)
        self.assertEqual(6812, sum(value[0] for value in self.EXPECTED.values()))


if __name__ == "__main__":
    unittest.main()
