from __future__ import annotations

import unittest

from scripts.learning_contracts.check import _verify_release_hashes, validate_public_value


class CommandAndReleaseTests(unittest.TestCase):
    def test_release_hashes_are_closed(self) -> None:
        self.assertIsNone(_verify_release_hashes())

    def test_public_lesson_value_is_data(self) -> None:
        self.assertEqual("promotion-trust", validate_public_value("LESSON", "promotion-trust"))


if __name__ == "__main__":
    unittest.main()
