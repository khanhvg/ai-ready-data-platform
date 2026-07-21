from __future__ import annotations

import importlib.util
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load():
    path = ROOT / "scripts/golden/canonical.py"
    if not path.is_file():
        raise AssertionError("P4-RED-DUPLICATE-NAME\nP4-RED-NON-IJSON\nP4-RED-JCS-VECTOR")
    spec = importlib.util.spec_from_file_location("golden_canonical", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CanonicalizationTests(unittest.TestCase):
    def test_duplicate_names_are_rejected_before_mapping(self) -> None:
        canonical = load()
        with self.assertRaisesRegex(canonical.CanonicalizationError, "JSON_DUPLICATE_NAME"):
            canonical.parse_json(b'{"a":1,"\\u0061":2}')

    def test_non_ijson_numbers_and_surrogates_are_rejected(self) -> None:
        canonical = load()
        for raw in (b'{"n":NaN}', b'{"n":Infinity}', b'{"n":-Infinity}', b'{"s":"\\uDEAD"}'):
            with self.subTest(raw=raw), self.assertRaises(canonical.CanonicalizationError):
                canonical.parse_json(raw)

    def test_jcs_vectors(self) -> None:
        canonical = load()
        self.assertEqual(b'{"n":0}', canonical.dumps({"n": -0.0}))
        composed = canonical.dumps({"s": "é"})
        decomposed = canonical.dumps({"s": "e\u0301"})
        self.assertNotEqual(composed, decomposed)


if __name__ == "__main__": unittest.main()
