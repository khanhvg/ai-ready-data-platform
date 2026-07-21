"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-REF-MISSING-110",
    "I8-REF-CYCLE-111",
    "I8-REF-TRAVERSAL-112",
    "I8-REF-REMOTE-113",
    "I8-REF-HASH-114",
    "I8-REGISTRY-BASE-115",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
