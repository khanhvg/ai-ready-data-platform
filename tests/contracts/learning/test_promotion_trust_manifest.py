from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class PromotionTrustBehaviorTest(unittest.TestCase):
    def test_no_hidden_common_grain(self) -> None:
        assert_invalid(self, "I8-PROMO-GRAIN-170", "promotion", fixture("invalid/promotion-trust/hidden-common-grain.json"), "PROMOTION_COMMON_GRAIN_FORBIDDEN")

    def test_limitation_required(self) -> None:
        assert_invalid(self, "I8-PROMO-LIMIT-171", "promotion", fixture("invalid/promotion-trust/missing-limitation.json"), "PROMOTION_LIMITATION_REQUIRED")

    def test_fixture_hash_binding(self) -> None:
        assert_invalid(self, "I8-PROMO-HASH-172", "promotion", fixture("invalid/promotion-trust/fixture-hash-drift.json"), "PROMOTION_FIXTURE_HASH_MISMATCH")
