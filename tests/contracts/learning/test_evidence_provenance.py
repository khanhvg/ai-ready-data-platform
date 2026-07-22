from __future__ import annotations

import copy
import hashlib
import pathlib
import tempfile
import unittest

from scripts.learning_contracts import evidence, fitness, registry
from scripts.learning_contracts.canonical import canonical_bytes
from scripts.learning_contracts.schema import LearningContractError


def artifact(root: pathlib.Path, name: str = "result.json") -> dict[str, object]:
    raw = b'{"result":"pass"}\n'
    (root / name).write_bytes(raw)
    return {"locator": name, "mediaType": "application/json", "size": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def learner_evidence(root: pathlib.Path) -> dict[str, object]:
    value: dict[str, object] = {
        "schemaVersion": "learning-evidence-v1",
        "evidenceId": "evidence-promotion-trust-1",
        "lesson": {"id": "promotion-trust", "version": "1.0.0"},
        "lab": {"id": "promotion-trust-v1", "version": "1.0.0"},
        "actor": {"subjectId": "learner-1", "authContextSha256": "1" * 64},
        "workspaceId": "workspace-1",
        "runId": "run-1",
        "operationId": "verifyWorkspace",
        "inputGitSha": "1" * 40,
        "officialGoldenMainSha": "2" * 40,
        "dependencyMergeShas": ["3" * 40],
        "contractHashes": [{"path": "learning/contracts/lesson-v1.schema.json", "sha256": "4" * 64}],
        "fixtureHashes": [{"path": "tests/fixtures/learning/contracts/valid/promotion-trust-v1.json", "sha256": "5" * 64}],
        "verifier": {"id": "learning-contracts-v1", "sha256": "6" * 64},
        "environment": {"python": "3.12.3", "platform": "darwin-arm64", "offline": True},
        "parameters": [],
        "transitions": [{"from": "in-progress", "to": "verified", "revision": 2}],
        "commands": [{"argv": ["make", "lesson-check", "LESSON=promotion-trust"], "rc": 0}],
        "assertions": [{"id": "four-independent-grains", "status": "pass"}],
        "artifacts": [artifact(root)],
        "timing": {"startedAt": "2026-07-22T00:00:00Z", "finishedAt": "2026-07-22T00:00:01Z", "durationMs": 1000},
        "redactionClass": "public-contract-evidence",
        "retentionClass": "review-bundle",
        "rollback": {"supported": True, "preserveEvidence": True},
    }
    value["integrity"] = {"algorithm": "sha-256+jcs", "payloadSha256": hashlib.sha256(canonical_bytes(value)).hexdigest()}
    return value


def fitness_result(root: pathlib.Path) -> dict[str, object]:
    value: dict[str, object] = {
        "schemaVersion": "fitness-result-v2",
        "commandId": "learning-contracts-check",
        "owner": "I5-03",
        "requested": {"subjectType": "contract-set", "subjectId": "issue-8-stage-a-v1", "parameters": []},
        "status": "pass",
        "failureCode": None,
        "remediation": None,
        "inputSha": "1" * 40,
        "testedTreeSha": "2" * 40,
        "dependencyMergeShas": ["3" * 40],
        "contractHashes": [{"name": "lesson-v1", "sha256": "4" * 64}],
        "fixtureHashes": [{"name": "promotion-trust", "sha256": "5" * 64}],
        "schemaHashes": [{"name": "fitness-result-v2", "sha256": "6" * 64}],
        "toolchain": [{"name": "python", "version": "3.12.3"}],
        "lockSha256": "7" * 64,
        "invocation": {"publicArgv": ["make", "learning-contracts-check"], "canonicalChildArgv": ["python", "-m", "scripts.learning_contracts.check", "check"], "actualChildArgvSha256": "8" * 64, "cwdRole": "repository-root"},
        "startedAt": "2026-07-22T00:00:00Z",
        "finishedAt": "2026-07-22T00:00:01Z",
        "durationMs": 1000,
        "rawLocator": "result.json",
        "projectionLocator": None,
        "envelopeLocator": None,
        "projectionSha256": None,
        "artifacts": [artifact(root)],
        "redactionClass": "public-contract-evidence",
        "retentionClass": "review-bundle",
        "rollback": {"supported": True, "preserveEvidence": True},
        "canonicalization": "RFC8785",
    }
    value["payloadSha256"] = hashlib.sha256(canonical_bytes(value)).hexdigest()
    return value


class EvidenceFitnessMigrationPromotionTests(unittest.TestCase):
    def assert_code(self, expected: str, call, *args, **kwargs) -> None:
        with self.assertRaises(LearningContractError) as caught:
            call(*args, **kwargs)
        self.assertEqual(expected, caught.exception.code)

    def test_i8_v3_evidence_schema_provenance_013(self) -> None:
        """I8-V3-EVIDENCE-SCHEMA-PROVENANCE-013."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            self.assertIsNone(evidence.verify_evidence(learner_evidence(root), root=root, seen_run_ids=set()))

    def test_i8_v3_evidence_tamper_replay_014(self) -> None:
        """I8-V3-EVIDENCE-TAMPER-REPLAY-014."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            value = learner_evidence(root)
            (root / "result.json").write_bytes(b"tampered")
            self.assert_code("EVIDENCE_ARTIFACT_TAMPER", evidence.verify_evidence, value, root=root, seen_run_ids=set())
            value = learner_evidence(root)
            self.assert_code("EVIDENCE_REPLAY", evidence.verify_evidence, value, root=root, seen_run_ids={"run-1"})

    def test_i8_v3_fitness_hash_binding_015(self) -> None:
        """I8-V3-FITNESS-HASH-BINDING-015."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            value = fitness_result(root)
            self.assertIsNone(fitness.verify_fitness(value, root=root))
            drifted = copy.deepcopy(value)
            drifted["sourceSha"] = "9" * 40
            self.assert_code("FITNESS_SCHEMA_INVALID", fitness.verify_fitness, drifted, root=root)
            future = fitness_result(root)
            future["owner"] = "I5-04"
            future["commandId"] = "future-contracts-check"
            future["payloadSha256"] = hashlib.sha256(canonical_bytes({key: child for key, child in future.items() if key != "payloadSha256"})).hexdigest()
            activation = {
                "schemaVersion": "command-owner-activation-v1",
                "owner": "I5-04",
                "commands": [{"commandId": "future-contracts-check", "availability": "implemented", "evidenceVersion": "fitness-result-v2"}],
            }
            self.assertIsNone(fitness.verify_fitness(future, root=root, activation=activation))

            nested = copy.deepcopy(value)
            nested["requested"]["parameters"] = [{"unexpected": True}]
            nested["payloadSha256"] = hashlib.sha256(canonical_bytes({key: child for key, child in nested.items() if key != "payloadSha256"})).hexdigest()
            self.assert_code("FITNESS_SCHEMA_INVALID", fitness.verify_fitness, nested, root=root)

    def test_i8_v3_migration_back_reader_016(self) -> None:
        """I8-V3-MIGRATION-BACK-READER-016."""
        old = {"schemaVersion": "private-v0", "id": "legacy-1", "status": "ready"}
        current = registry.migrate_document(old, "private-v1")
        self.assertEqual("private-v1", current["schemaVersion"])
        self.assertEqual(old, registry.migrate_document(current, "private-v0"))
        self.assert_code("MIGRATION_EDGE_UNREGISTERED", registry.migrate_document, old, "fitness-result-v2")

    def test_i8_v3_promotion_four_grains_017(self) -> None:
        """I8-V3-PROMOTION-FOUR-GRAINS-017."""
        result = fitness.evaluate_promotion([
            {"grain": "daily-revenue", "keys": ["date"]},
            {"grain": "promotion-effectiveness", "keys": ["promotion_id"]},
            {"grain": "returns", "keys": ["return_id"]},
            {"grain": "quality", "keys": ["test_id"]},
        ])
        self.assertEqual("insufficient-evidence/no-common-grain", result["decision"])
        self.assertEqual(4, result["independentGrainCount"])

    def test_i8_v3_manifest_index_complete_018(self) -> None:
        """I8-V3-MANIFEST-INDEX-COMPLETE-018."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            first = artifact(root, "first.json")
            second = artifact(root, "second.json")
            manifest = {"schemaVersion": "evidence-manifest-v1", "entries": [first, second]}
            self.assertIsNone(evidence.verify_manifest(manifest, root=root))
            self.assert_code(
                "MANIFEST_INCOMPLETE",
                evidence.verify_manifest,
                {"schemaVersion": "evidence-manifest-v1", "entries": [first]},
                root=root,
            )

    def test_six_high_h2_raw_log_binding_is_sanitized_and_exact(self) -> None:
        raw = "FAILED /Users/alice/work/repo/test.py /tmp/result file:///private/var/a"
        sanitized = evidence.sanitize_retained_text(raw)
        self.assertNotIn("/Users/", sanitized)
        self.assertNotIn("/tmp/", sanitized)
        self.assertNotIn("/private/", sanitized)
        self.assertIn("<WORKSPACE>", sanitized)
        records = [{"id": "H2-RED", "expected": "EXPECTED_TOKEN", "actual": "ACTUAL_TOKEN"}]
        evidence.verify_raw_log_bindings(records, "EXPECTED_TOKEN\nACTUAL_TOKEN\n")
        with self.assertRaises(LearningContractError):
            evidence.verify_raw_log_bindings(records, "EXPECTED_TOKEN\n")

    def test_final_repair_review_bundle_declared_integers_are_strict_json_integers(self) -> None:
        manifest = {
            "schemaVersion": "issue8-v3-final-repair-bundle-v1",
            "totalBytes": 10,
            "entries": [{"path": "primary.log", "sha256": "0" * 64, "size": 10}],
        }
        commands = [{"id": "primary", "log": "primary.log", "logSha256": "0" * 64, "rc": 0}]
        red_records = [{"id": "A", "log": "red.log", "logSha256": "1" * 64, "rc": 1}]
        review = {
            "scope": {
                "additions": 121, "modifications": 0, "deletions": 0,
                "allowlistDelta": 0, "stageBPaths": 0,
            },
            "resourceLimits": {
                "outputBytes": 10 * 1024 * 1024, "rssBytes": 512 * 1024 * 1024,
                "timeoutSeconds": 120,
            },
            "nonIntegerMetadata": {"ratio": 1.5, "scientificMeasurement": 1e-3},
        }
        self.assertIsNone(
            evidence.validate_review_bundle_integer_fields(
                manifest, commands=commands, red_records=red_records, review=review,
            )
        )
        integer_paths = [
            (manifest, "totalBytes"),
            (manifest["entries"][0], "size"),
            (commands[0], "rc"),
            (red_records[0], "rc"),
            *[(review["scope"], key) for key in review["scope"]],
            *[(review["resourceLimits"], key) for key in review["resourceLimits"]],
        ]
        for owner, key in integer_paths:
            original = owner[key]
            for invalid in (float(original), bool(original)):
                with self.subTest(key=key, invalid=repr(invalid)):
                    owner[key] = invalid
                    self.assert_code(
                        "REVIEW_BUNDLE_INTEGER_TYPE_INVALID",
                        evidence.validate_review_bundle_integer_fields,
                        manifest,
                        commands=commands,
                        red_records=red_records,
                        review=review,
                    )
            owner[key] = original


if __name__ == "__main__":
    unittest.main()
