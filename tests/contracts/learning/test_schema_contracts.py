from __future__ import annotations

import hashlib
import os
import pathlib
import tempfile
import threading
import unittest
from unittest import mock

from scripts.learning_contracts import canonical, check, references, schema


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
                for locator in (
                    f"../{outside.name}",
                    "/etc/passwd",
                    "https://example.test/a",
                    "s3:bucket/key",
                    "nested\\payload",
                    "nested//payload",
                ):
                    with self.subTest(locator=locator):
                        self.assert_code(
                            "REFERENCE_PATH_INVALID",
                            references.resolve_reference,
                            base,
                            locator,
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
                nested = base / "nested"
                nested.mkdir()
                escaped = base.parent / f"{base.name}-escaped"
                escaped.mkdir()
                (escaped / "payload").write_bytes(b"escaped")
                os.symlink(escaped, nested / "redirect")
                self.assert_code(
                    "REFERENCE_SPECIAL_FILE",
                    references.resolve_reference,
                    base,
                    "nested/redirect/payload",
                    hashlib.sha256(b"escaped").hexdigest(),
                )
            finally:
                outside.unlink(missing_ok=True)
                if 'escaped' in locals():
                    (escaped / "payload").unlink(missing_ok=True)
                    escaped.rmdir()

    def test_six_high_h1_fixture_metadata_cannot_select_result(self) -> None:
        """A fixture can identify a case, but cannot inject its expected result."""
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "fixture.json"
            path.write_text(
                '{"completionSource":"evidence-presence","completed":true,'
                '"expectedCode":"COMPLETION_DUAL_TRUTH"}',
                encoding="utf-8",
            )
            self.assert_code(
                "FIXTURE_METADATA_INVALID",
                check.validate_invalid_fixture,
                path,
                "completion",
            )

    def test_review_h1_semantic_rows_use_strict_family_reader(self) -> None:
        original = check.read_document
        family_reads: list[str] = []

        def traced(path: pathlib.Path, *, family: str | None = None):
            if family is not None:
                family_reads.append(family)
            return original(path, family=family)

        representatives = {
            "completion": (
                "invalid/semantics/completion/evidence-presence-completes.json",
                "completion-reconciliation",
            ),
            "state": (
                "invalid/semantics/state/stale-version.json",
                "progress",
            ),
        }
        for target, (relative, required_family) in representatives.items():
            family_reads.clear()
            with mock.patch.object(check, "read_document", traced):
                self.assert_code(
                    {
                        "completion": "COMPLETION_DUAL_TRUTH",
                        "state": "PROGRESS_VERSION_CONFLICT",
                    }[target],
                    check.validate_invalid_fixture,
                    check.FIXTURE_ROOT / relative,
                    target,
                )
            self.assertIn(required_family, family_reads, target)

    def test_six_high_h5_intermediate_replacement_cannot_redirect_read(self) -> None:
        """A concurrent intermediate replacement must fail closed, never redirect bytes."""
        with tempfile.TemporaryDirectory() as temporary:
            base = pathlib.Path(temporary)
            inside = base / "nested"
            inside.mkdir()
            (inside / "payload.json").write_bytes(b"inside")
            held_inside = base / "held-inside"
            outside = base / "outside"
            outside.mkdir()
            (outside / "payload.json").write_bytes(b"outside")
            checked = threading.Event()
            replaced = threading.Event()
            original_lstat = pathlib.Path.lstat
            original_stat = os.stat

            def replace_component() -> None:
                if checked.wait(2):
                    inside.rename(held_inside)
                    os.symlink("outside", inside)
                    replaced.set()

            def synchronized_lstat(path: pathlib.Path):
                result = original_lstat(path)
                if path == inside and not checked.is_set():
                    checked.set()
                    self.assertTrue(replaced.wait(2))
                return result

            def synchronized_stat(path, *args, **kwargs):
                result = original_stat(path, *args, **kwargs)
                if path == "nested" and kwargs.get("dir_fd") is not None and not checked.is_set():
                    checked.set()
                    self.assertTrue(replaced.wait(2))
                return result

            racer = threading.Thread(target=replace_component)
            racer.start()
            try:
                with (
                    mock.patch.object(pathlib.Path, "lstat", synchronized_lstat),
                    mock.patch.object(os, "stat", synchronized_stat),
                ):
                    try:
                        raw = references.resolve_reference(
                            base,
                            "nested/payload.json",
                            hashlib.sha256(b"outside").hexdigest(),
                        )
                    except schema.LearningContractError as exc:
                        self.assertIn(exc.code, {"REFERENCE_SPECIAL_FILE", "REFERENCE_UNREADABLE"})
                    else:
                        self.assertNotEqual(b"outside", raw)
            finally:
                racer.join(2)
                if inside.is_symlink():
                    inside.unlink()
                if held_inside.exists():
                    held_inside.rename(inside)
            self.assertFalse(racer.is_alive())


if __name__ == "__main__":
    unittest.main()
