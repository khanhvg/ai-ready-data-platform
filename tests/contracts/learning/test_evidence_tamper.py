"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-TAMPER-PAYLOAD-140",
    "I8-TAMPER-ARTIFACT-141",
    "I8-LOCATOR-TRAVERSAL-142",
    "I8-LOCATOR-PRIVATE-147",
    "I8-TAMPER-VERIFIER-148",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
