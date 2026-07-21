"""Stage A RED contract assertions; frozen before production behavior."""
import unittest

from tests.contracts.learning import assert_contract_behavior

TEST_IDS = [
    "I8-OPENAPI-MATRIX-160",
    "I8-OPENAPI-AUTH-161",
    "I8-OPENAPI-IDEMPOTENCY-162",
    "I8-OPENAPI-RAW-163",
    "I8-OPENAPI-REF-164",
    "I8-OPENAPI-VERSION-165",
    "I8-ASYNCAPI-166",
    "I8-OPENAPI-REQUEST-173",
    "I8-OPENAPI-RESPONSE-174",
    "I8-OPENAPI-ERROR-175",
    "I8-OPENAPI-YAML-179",
]


class ContractRedTest(unittest.TestCase):
    pass


def _red(test_id: str):
    def test(self: unittest.TestCase) -> None:
        assert_contract_behavior(self, test_id)
    return test


for _test_id in TEST_IDS:
    setattr(ContractRedTest, "test_" + _test_id.lower().replace("-", "_"), _red(_test_id))
