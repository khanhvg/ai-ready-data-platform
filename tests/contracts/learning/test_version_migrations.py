"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-MIGRATION-UNKNOWN-150",
    "I8-MIGRATION-LOSS-151",
    "I8-MIGRATION-CYCLE-152",
    "I8-MIGRATION-COLLISION-153",
    "I8-MIGRATION-BACKWARD-159",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
