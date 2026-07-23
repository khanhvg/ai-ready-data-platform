from __future__ import annotations

import unittest

from test_architecture_expansion import CASES, install_case_tests


CURRICULUM_FAMILIES = frozenset(
    {
        "I11-RED-REF-001",
        "I11-RED-PREQ-001",
        "I11-RED-VIEW-001",
        "I11-RED-ADR-001",
        "I11-RED-PATTERN-001",
        "I11-RED-API-001",
        "I11-RED-TEMPLATE-001",
        "I11-RED-CRITICAL-FLOW-001",
        "I11-RED-ASSESSMENT-001",
        "I11-RED-PROMOTION-001",
    }
)


class CurriculumSchemaTemplateAndLifecycleMutations(unittest.TestCase):
    pass


install_case_tests(
    CurriculumSchemaTemplateAndLifecycleMutations,
    [case for case in CASES if case["family"] in CURRICULUM_FAMILIES],
)
