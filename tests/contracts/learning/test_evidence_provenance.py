"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-EVIDENCE-REPLAY-149",
    "I8-EVIDENCE-PROVENANCE-143",
    "I8-EVIDENCE-RECURSIVE-144",
    "I8-SECRET-145",
    "I8-INJECTION-146",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
