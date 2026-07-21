from __future__ import annotations

import unittest
from unittest import mock

from scripts.learning_contracts import runtime
from scripts.learning_contracts.runtime import resource_limits
from tests.contracts.learning import assert_invalid


class RuntimeDependencyBehaviorTest(unittest.TestCase):
    def test_unadmitted_import(self) -> None:
        assert_invalid(self, "I8-DEPS-IMPORT-181", "dependency", {"imports": ["requests"]}, "DEPENDENCY_IMPORT_UNADMITTED")

    def test_manifest_drift(self) -> None:
        assert_invalid(self, "I8-DEPS-MANIFEST-182", "dependency", {"lockSha256": "changed"}, "DEPENDENCY_MANIFEST_DRIFT")

    def test_advisory_disposition(self) -> None:
        assert_invalid(self, "I8-DEPS-ADVISORY-183", "dependency", {"inheritedAdvisoryDisposition": None}, "DEPENDENCY_ADVISORY_UNRESOLVED")

    def test_resource_ceilings_are_executable_policy(self) -> None:
        expected = {"learning-contracts-check": 120, "api-contracts-check": 60, "lesson-check": 60, "evidence-verify": 30, "streamBytes": 2 * 1024 * 1024, "runBytes": 256 * 1024 * 1024, "rssBytes": 2 * 1024 * 1024 * 1024}
        actual = resource_limits()
        self.assertEqual(actual, expected, f"I8-RESOURCE-POLICY expected={expected} actual={actual}")

    def test_resource_deadline_fails_closed(self) -> None:
        limits = {**resource_limits(), "api-contracts-check": 0}
        with mock.patch.object(runtime, "resource_limits", return_value=limits), self.assertRaisesRegex(SystemExit, "RESOURCE_TIME_LIMIT"):
            runtime.launch(["api-contracts-check"])

    def test_resource_output_fails_closed(self) -> None:
        limits = {**resource_limits(), "streamBytes": 1}
        with mock.patch.object(runtime, "resource_limits", return_value=limits), self.assertRaisesRegex(SystemExit, "RESOURCE_OUTPUT_LIMIT"):
            runtime.launch(["api-contracts-check"])

    def test_resource_rss_fails_closed(self) -> None:
        limits = {**resource_limits(), "rssBytes": 1}
        with mock.patch.object(runtime, "resource_limits", return_value=limits), self.assertRaisesRegex(SystemExit, "RESOURCE_RSS_LIMIT"):
            runtime.launch(["api-contracts-check"])
