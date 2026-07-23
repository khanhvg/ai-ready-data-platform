from __future__ import annotations

import unittest

from test_architecture_expansion import CASES, TRACEABILITY_FAMILIES, install_case_tests


class TraceSourceRelationBridgeAndTopologyMutations(unittest.TestCase):
    pass


install_case_tests(
    TraceSourceRelationBridgeAndTopologyMutations,
    [case for case in CASES if case["family"] in TRACEABILITY_FAMILIES],
)
