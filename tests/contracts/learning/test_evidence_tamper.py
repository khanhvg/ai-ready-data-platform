from __future__ import annotations

import unittest

from scripts.learning_contracts.check import validate_invalid_corpus


class EvidenceTamperCorpusTests(unittest.TestCase):
    def test_all_indexed_tamper_vectors_report_actual_codes(self) -> None:
        rows = validate_invalid_corpus()
        evidence_rows = [row for row in rows if row["rowId"] in {f"invalid-{number:03d}" for number in range(16, 23)}]
        self.assertEqual(7, len(evidence_rows))
        self.assertTrue(all(row["actual"] == row["expected"] for row in evidence_rows))


if __name__ == "__main__":
    unittest.main()
