from __future__ import annotations

import unittest

from test_architecture_expansion import CASES, install_case_tests


SECURITY_AND_BOUND_FAMILIES = frozenset(
    {
        "I11-RED-S3-001",
        "I11-RED-BOUND-001",
        "I11-RED-EVIDENCE-001",
        "I11-RED-RESOURCE-001",
        "I11-RED-CLEANUP-001",
    }
)


class SecurityProcessResourceEvidenceAndCleanupMutations(unittest.TestCase):
    pass


install_case_tests(
    SecurityProcessResourceEvidenceAndCleanupMutations,
    [case for case in CASES if case["family"] in SECURITY_AND_BOUND_FAMILIES],
)
