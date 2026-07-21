from __future__ import annotations

import unittest


class PublicSurfaceScaffoldTests(unittest.TestCase):
    def test_i8_v3_scaffold_public_surface_001(self) -> None:
        """I8-V3-SCAFFOLD-PUBLIC-SURFACE-001."""
        from scripts.learning_contracts import check

        self.assertTrue(callable(check.main))


if __name__ == "__main__":
    unittest.main()
