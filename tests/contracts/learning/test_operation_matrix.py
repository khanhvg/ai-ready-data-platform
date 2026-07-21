from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid, fixture


class OperationMatrixBehaviorTest(unittest.TestCase):
    def test_duplicate_method_path(self) -> None:
        assert_invalid(self, "I8-OPERATION-DUPLICATE-154", "operation", fixture("invalid/operation/duplicate-method-path.json"), "OPERATION_DUPLICATE")

    def test_taxonomy(self) -> None:
        assert_invalid(self, "I8-OPERATION-TAXONOMY-155", "operation", fixture("invalid/operation/missing-taxonomy.json"), "OPERATION_TAXONOMY_INCOMPLETE")

    def test_neutral_role(self) -> None:
        assert_invalid(self, "I8-OPERATION-ROLE-156", "operation", fixture("invalid/operation/physical-module-role.json"), "OPERATION_ROLE_NOT_NEUTRAL")

    def test_authorization(self) -> None:
        assert_invalid(self, "I8-OPERATION-AUTHZ-157", "operation", fixture("invalid/operation/missing-authorization.json"), "OPERATION_AUTHORIZATION_INCOMPLETE")

    def test_evidence_rule(self) -> None:
        assert_invalid(self, "I8-OPERATION-EVIDENCE-158", "operation", fixture("invalid/operation/missing-evidence-rule.json"), "OPERATION_EVIDENCE_INCOMPLETE")
