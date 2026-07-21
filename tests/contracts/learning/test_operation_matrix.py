"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-OPERATION-DUPLICATE-154",
    "I8-OPERATION-TAXONOMY-155",
    "I8-OPERATION-ROLE-156",
    "I8-OPERATION-AUTHZ-157",
    "I8-OPERATION-EVIDENCE-158",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
