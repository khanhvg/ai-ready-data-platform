from __future__ import annotations

import hashlib
import os
import pathlib
import tempfile
import unittest

from scripts.learning_contracts import canonical, references, schema


class SchemaReaderCanonicalReferenceTests(unittest.TestCase):
    def assert_code(self, expected: str, call, *args, **kwargs) -> None:
        with self.assertRaises(schema.LearningContractError) as caught:
            call(*args, **kwargs)
        self.assertEqual(expected, caught.exception.code)

    def test_i8_v3_schema_nested_closed_001(self) -> None:
        """I8-V3-SCHEMA-NESTED-CLOSED-001."""
        malformed = {
            "schemaVersion": "lesson-v1",
            "lessonId": "promotion-trust",
            "title": "Promotion trust",
            "objectives": [{"id": "objective-1", "text": 7, "extra": True}],
            "labRef": {"path": "learning/labs/promotion-trust/lab-v1.json", "sha256": "0" * 64},
        }
        self.assert_code("SCHEMA_INVALID", schema.validate_document, malformed, family="lesson")

    def test_i8_v3_reader_json_duplicate_002(self) -> None:
        """I8-V3-READER-JSON-DUPLICATE-002."""
        with tempfile.TemporaryDirectory() as root:
            path = pathlib.Path(root) / "duplicate.json"
            path.write_bytes(b'{"name":"first","name":"second"}')
            self.assert_code("JSON_DUPLICATE_NAME", schema.read_document, path)

    def test_i8_v3_reader_yaml_duplicate_003(self) -> None:
        """I8-V3-READER-YAML-DUPLICATE-003."""
        with tempfile.TemporaryDirectory() as root:
            path = pathlib.Path(root) / "duplicate.yaml"
            path.write_bytes(b"openapi: 3.2.0\nopenapi: 3.1.0\n")
            self.assert_code("YAML_DUPLICATE_NAME", schema.read_document, path)

    def test_i8_v3_canonical_ijson_jcs_004(self) -> None:
        """I8-V3-CANONICAL-IJSON-JCS-004."""
        self.assert_code("JSON_BOM_REFUSED", canonical.parse_json, b'\xef\xbb\xbf{"a":1}')
        self.assertEqual(b'{"a":0,"b":1}', canonical.canonical_bytes({"b": 1, "a": -0.0}))

    def test_i8_v3_reference_local_hash_005(self) -> None:
        """I8-V3-REFERENCE-LOCAL-HASH-005."""
        with tempfile.TemporaryDirectory() as root:
            base = pathlib.Path(root)
            payload = b'{"schemaVersion":"fixture-v1"}\n'
            (base / "fixture.json").write_bytes(payload)
            digest = hashlib.sha256(payload).hexdigest()
            self.assertEqual(payload, references.resolve_reference(base, "fixture.json", digest))
            self.assert_code(
                "REFERENCE_HASH_MISMATCH",
                references.resolve_reference,
                base,
                "fixture.json",
                "0" * 64,
            )

    def test_i8_v3_reference_escape_special_006(self) -> None:
        """I8-V3-REFERENCE-ESCAPE-SPECIAL-006."""
        with tempfile.TemporaryDirectory() as root:
            base = pathlib.Path(root)
            outside = base.parent / f"{base.name}-outside"
            outside.write_bytes(b"outside")
            try:
                self.assert_code(
                    "REFERENCE_PATH_INVALID",
                    references.resolve_reference,
                    base,
                    f"../{outside.name}",
                    hashlib.sha256(b"outside").hexdigest(),
                )
                target = base / "regular"
                target.write_bytes(b"content")
                os.link(target, base / "hardlink")
                self.assert_code(
                    "REFERENCE_SPECIAL_FILE",
                    references.resolve_reference,
                    base,
                    "hardlink",
                    hashlib.sha256(b"content").hexdigest(),
                )
            finally:
                outside.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
