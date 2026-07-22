from __future__ import annotations

import unittest

from scripts.learning_contracts.openapi import validate_shipped_openapi


class OpenApiContractTests(unittest.TestCase):
    def test_shipped_openapi_is_wired(self) -> None:
        self.assertIsNone(validate_shipped_openapi())


if __name__ == "__main__":
    unittest.main()
