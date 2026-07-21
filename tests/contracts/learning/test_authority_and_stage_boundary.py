"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-AUTH-BASE-001",
    "I8-AUTH-LEASE-002",
    "I8-AUTH-PROTECTED-003",
    "I8-I6-FIXTURE-PIN-004",
    "I8-STAGEA-NO-I7-010",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
