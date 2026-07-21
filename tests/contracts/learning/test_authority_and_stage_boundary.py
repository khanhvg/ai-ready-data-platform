from __future__ import annotations

import unittest

from scripts.learning_contracts import engine_ready


class ScaffoldTest(unittest.TestCase):
    def test_scaffold_entrypoint_is_executable(self) -> None:
        self.assertIs(engine_ready(), True, "I8-SCAFFOLD-READY expected=True actual=False")


if __name__ == "__main__":
    unittest.main()
