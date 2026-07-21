"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-SCHEMA-CLOSED-100",
    "I8-SCHEMA-MISSING-101",
    "I8-SCHEMA-TYPE-102",
    "I8-CANON-DUPLICATE-103",
    "I8-CANON-NUMBER-104",
    "I8-CANON-SURROGATE-105",
    "I8-CANON-RANGE-106",
    "I8-CANON-UTF8-107",
    "I8-CANON-BOM-108",
    "I8-CANON-TRAILING-109",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
