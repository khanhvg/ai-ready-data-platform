"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-STATE-ILLEGAL-120",
    "I8-STATE-STALE-121",
    "I8-IDEMPOTENCY-CONFLICT-122",
    "I8-IDEMPOTENCY-DUPLICATE-123",
    "I8-COMPLETION-FORGE-130",
    "I8-COMPLETION-DUAL-131",
    "I8-COMPLETION-PRESENCE-134",
    "I8-RECONCILE-ORPHAN-132",
    "I8-RECONCILE-TAMPER-133",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
