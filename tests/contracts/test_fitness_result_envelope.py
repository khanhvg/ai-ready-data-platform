from __future__ import annotations

import importlib.util
import pathlib
import json
import unittest
import jsonschema


ROOT = pathlib.Path(__file__).resolve().parents[2]


class FitnessResultEnvelopeTests(unittest.TestCase):
    def test_pass_envelope_is_closed_and_schema_valid(self) -> None:
        path = ROOT / "scripts/golden/evidence.py"
        spec = importlib.util.spec_from_file_location("golden_evidence_shape", path); assert spec and spec.loader
        evidence = importlib.util.module_from_spec(spec); spec.loader.exec_module(evidence)
        value=evidence.fitness_envelope(fitness_id="data-contracts-check",result="pass",tested_tree_sha="0"*40,projection_sha256="1"*64)
        schema=json.loads((ROOT/"learning/contracts/fitness-result-v1.schema.json").read_text())
        jsonschema.Draft202012Validator(schema).validate(value)
    def test_sensitive_output_blocks_publication(self) -> None:
        path = ROOT / "scripts/golden/evidence.py"
        if not path.is_file():
            self.fail("P3-RED-SENSITIVE-OUTPUT")
        spec = importlib.util.spec_from_file_location("golden_evidence", path)
        assert spec and spec.loader
        evidence = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(evidence)
        for value in (
            "TOKEN=super-secret-canary",
            "https://user:password@example.invalid/private",
            "/" + "Users/private-person/project",
        ):
            with self.subTest(value=value):
                with self.assertRaisesRegex(evidence.EvidenceError, "EVIDENCE_SENSITIVE_CONTENT"):
                    evidence.assert_safe_text(value)


if __name__ == "__main__":
    unittest.main()
