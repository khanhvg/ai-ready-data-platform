from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class SchemaContractBehaviorTest(unittest.TestCase):
    def test_closed_object(self) -> None:
        assert_invalid(self, "I8-SCHEMA-CLOSED-100", "schema", fixture("invalid/schema/unknown-field.json"), "SCHEMA_UNKNOWN_PROPERTY")

    def test_required_property(self) -> None:
        assert_invalid(self, "I8-SCHEMA-MISSING-101", "schema", fixture("invalid/schema/missing-required.json"), "SCHEMA_REQUIRED_PROPERTY")

    def test_property_type(self) -> None:
        assert_invalid(self, "I8-SCHEMA-TYPE-102", "schema", fixture("invalid/schema/wrong-type.json"), "SCHEMA_TYPE_MISMATCH")

    def test_duplicate_name(self) -> None:
        assert_invalid(self, "I8-CANON-DUPLICATE-103", "canonical", fixture("invalid/canonicalization/duplicate-name.json"), "JSON_DUPLICATE_NAME")

    def test_non_ijson_numbers(self) -> None:
        for name in ("nan.json", "positive-infinity.json", "negative-infinity.json"):
            with self.subTest(name=name):
                assert_invalid(self, "I8-CANON-NUMBER-104", "canonical", fixture(f"invalid/canonicalization/{name}"), "JSON_NON_IJSON_NUMBER")

    def test_lone_surrogate(self) -> None:
        assert_invalid(self, "I8-CANON-SURROGATE-105", "canonical", fixture("invalid/canonicalization/lone-surrogate.json"), "JSON_LONE_SURROGATE")

    def test_unsafe_integer(self) -> None:
        assert_invalid(self, "I8-CANON-RANGE-106", "canonical", fixture("invalid/canonicalization/unsafe-integer.json"), "JSON_INTEGER_UNSAFE")

    def test_invalid_utf8(self) -> None:
        assert_invalid(self, "I8-CANON-UTF8-107", "canonical", fixture("invalid/canonicalization/invalid-utf8.json"), "JSON_UTF8_INVALID")

    def test_bom(self) -> None:
        assert_invalid(self, "I8-CANON-BOM-108", "canonical", fixture("invalid/canonicalization/bom.json"), "JSON_BOM_FORBIDDEN")

    def test_trailing_document(self) -> None:
        assert_invalid(self, "I8-CANON-TRAILING-109", "canonical", fixture("invalid/canonicalization/trailing-document.json"), "JSON_TRAILING_CONTENT")
