from __future__ import annotations

import unittest

from tests.contracts.learning import assert_invalid


class RuntimeDependencyBehaviorTest(unittest.TestCase):
    def test_unadmitted_import(self) -> None:
        assert_invalid(self, "I8-DEPS-IMPORT-181", "dependency", {"imports": ["requests"]}, "DEPENDENCY_IMPORT_UNADMITTED")

    def test_manifest_drift(self) -> None:
        assert_invalid(self, "I8-DEPS-MANIFEST-182", "dependency", {"lockSha256": "changed"}, "DEPENDENCY_MANIFEST_DRIFT")

    def test_advisory_disposition(self) -> None:
        assert_invalid(self, "I8-DEPS-ADVISORY-183", "dependency", {"inheritedAdvisoryDisposition": None}, "DEPENDENCY_ADVISORY_UNRESOLVED")
