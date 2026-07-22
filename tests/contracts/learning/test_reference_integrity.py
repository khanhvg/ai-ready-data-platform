from __future__ import annotations

import hashlib
import pathlib
import tempfile
import unittest

from scripts.learning_contracts.references import resolve_reference


class ReferenceIntegrityTests(unittest.TestCase):
    def test_local_reference_is_hash_bound(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            raw = b"reference\n"
            (root / "reference.txt").write_bytes(raw)
            self.assertEqual(raw, resolve_reference(root, "reference.txt", hashlib.sha256(raw).hexdigest()))


if __name__ == "__main__":
    unittest.main()
