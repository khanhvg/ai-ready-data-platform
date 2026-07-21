"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-PROBE-MUTATION-167",
    "I8-HINT-ORDER-168",
    "I8-HINT-COMPLETION-169",
    "I8-PROBE-REQUIRED-176",
    "I8-PROBE-OPTIONAL-177",
    "I8-HINT-REVEAL-178",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
