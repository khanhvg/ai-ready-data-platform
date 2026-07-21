from __future__ import annotations

import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class HistoricalEvidenceReaderTests(unittest.TestCase):
    def test_historical_context_cannot_be_current_small_42(self) -> None:
        text = (ROOT / "docs/verification/GH-3-full-flow-evidence.md").read_text(encoding="utf-8")
        self.assertIn("2026-07-10", text)
        self.assertIn("620,340", text)
        self.assertIn("demo-large", text)
        self.assertNotIn("small/42 current golden attestation", text)


if __name__ == "__main__":
    unittest.main()
