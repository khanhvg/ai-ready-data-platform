from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from learning.curriculum.tools import normalize_request
from learning.curriculum.tools.check_curriculum import run

FIXTURE = Path("tests/fixtures/learning/curriculum/invalid-cases-v1.json")


def _replace(document, replacements):
    value = copy.deepcopy(document)
    for locator, replacement in replacements.items():
        target = value
        parts = locator.split(".")
        for part in parts[:-1]:
            target = target[int(part)] if isinstance(target, list) else target[part]
        last = parts[-1]
        if isinstance(target, list):
            target[int(last)] = replacement
        else:
            target[last] = replacement
    return value


class CurriculumContractTest(unittest.TestCase):
    def test_valid_controls_and_named_mutations(self):
        families = json.loads(FIXTURE.read_text())["families"]
        selected = [item for item in families if item["entrypoint"] == "I11-EP-CURRICULUM"]
        self.assertEqual(10, len(selected))
        for family in selected:
            with self.subTest(family=family["id"], control=True):
                result = run(normalize_request(family["validControl"]))
                self.assertTrue(result.reached)
                self.assertEqual((), result.codes)
            for mutation in family["mutations"]:
                with self.subTest(family=family["id"], mutation=mutation["mutationId"]):
                    request = _replace(family["validControl"], mutation["replace"])
                    result = run(normalize_request(request))
                    self.assertTrue(result.reached)
                    self.assertIn(mutation["expectedCode"], result.codes)
