from __future__ import annotations

import copy
import hashlib
import inspect
import json
import os
import pathlib
import stat
import subprocess
import tempfile
import unittest

from scripts.learning_contracts import check, schema


ROOT = pathlib.Path(__file__).resolve().parents[3]
COOK_INPUT_SHA = "cb44a71b1762f861bc63b6f13ce4f54142087b34"
STAGE_A_RELEASE_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
STAGE_A_MERGE_SHA = "5c2244c2c860234d0df49cf0a42ad950c6495717"
ISSUE_7_MERGE_SHA = "1806b6d515f2f7a2ace2be7077af84a745ff221f"
BINDING_SCHEMA = ROOT / "learning/contracts/promotion-trust-vite-binding-v1.schema.json"
BINDING = ROOT / "learning/bindings/vite/promotion-trust-v1.json"
INVALID_ROOT = ROOT / "tests/fixtures/learning/bindings/vite/invalid"

PINNED_INPUTS = {
    "learning/contracts/learning-contract-set-v1.json": "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638",
    "learning/manifests/promotion-trust-v1.json": "553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac",
    "tests/fixtures/learning/promotion-trust/evidence-v1.json": "2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5",
    "tests/fixtures/learning/promotion-trust/manifest.json": "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341",
    "docs/decisions/0005-web-stack.md": "6e26c48a027d226d8529fda939c07cca99e9f4e1d88cac12708deb98d6fe5eee",
    "spikes/web/candidates/vite/package.json": "c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871",
    "spikes/web/candidates/vite/package-lock.json": "96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c",
    "spikes/web/candidates/vite/src/lesson-contract.mjs": "32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9",
    "learning/contracts/completion-reconciliation-v1.json": "8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff",
}
INVALID_CASES = {
    "absolute-path.json": "BINDING_REFERENCE_FORBIDDEN",
    "completion-authority-override.json": "BINDING_AUTHORITY_FORBIDDEN",
    "contract-key-drift.json": "BINDING_STAGE_A_KEY_MISMATCH",
    "dependency-hash-drift.json": "BINDING_DEPENDENCY_HASH_MISMATCH",
    "duplicate-target-key.json": "BINDING_ALIAS_NOT_BIJECTIVE",
    "fixture-key-drift.json": "BINDING_FIXTURE_KEY_MISMATCH",
    "grain-id-drift.json": "BINDING_GRAIN_MISMATCH",
    "raw-record-leak.json": "BINDING_DATA_PAYLOAD_FORBIDDEN",
}
ALLOWLIST = {
    "learning/contracts/promotion-trust-vite-binding-v1.schema.json",
    "learning/bindings/vite/promotion-trust-v1.json",
    "scripts/learning_contracts/vite_binding.py",
    "scripts/learning_contracts/schema.py",
    "scripts/learning_contracts/check.py",
    "tests/contracts/learning/test_vite_consumer_binding.py",
    *(f"tests/fixtures/learning/bindings/vite/invalid/{name}" for name in INVALID_CASES),
}


class ViteConsumerBindingTests(unittest.TestCase):
    def assert_code(self, expected: str, call, *args, **kwargs) -> None:
        with self.assertRaises(schema.LearningContractError) as caught:
            call(*args, **kwargs)
        self.assertEqual(expected, caught.exception.code)

    def public_path_validator(self, path: pathlib.Path):
        info = path.lstat()
        if stat.S_ISREG(info.st_mode) and info.st_nlink == 1:
            parsed = schema.read_document(path)
            self.assertIsInstance(parsed, dict)
        validator = getattr(check, "validate_vite_binding_path", None)
        self.assertIsNotNone(validator, f"VITE_BINDING_REQUIRED: {path.name}")
        return validator(path)

    def public_document_validator(self, value: dict[str, object]):
        validator = getattr(check, "validate_vite_binding_document", None)
        self.assertIsNotNone(validator, "VITE_BINDING_REQUIRED: public document path")
        return validator(value)

    def load_binding(self) -> dict[str, object]:
        self.assertTrue(BINDING_SCHEMA.is_file(), "VITE_BINDING_REQUIRED: schema")
        self.assertTrue(BINDING.is_file(), "VITE_BINDING_REQUIRED: document")
        value = schema.read_document(BINDING, family="vite-binding")
        self.assertIsInstance(value, dict)
        return value

    def test_i8b_auth_001_commit_tree_authority_and_ancestry(self) -> None:
        self.assertEqual(COOK_INPUT_SHA, subprocess.check_output(
            ["git", "rev-parse", f"{COOK_INPUT_SHA}^{{commit}}"], cwd=ROOT, text=True
        ).strip())
        self.assertEqual(STAGE_A_RELEASE_SHA, subprocess.check_output(
            ["git", "rev-parse", f"{COOK_INPUT_SHA}^"], cwd=ROOT, text=True
        ).strip())
        for ancestor in (STAGE_A_MERGE_SHA, ISSUE_7_MERGE_SHA, COOK_INPUT_SHA):
            result = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, "HEAD"], cwd=ROOT)
            self.assertEqual(0, result.returncode, ancestor)
        self.assertEqual(40, len(subprocess.check_output(
            ["git", "rev-parse", "HEAD^{tree}"], cwd=ROOT, text=True
        ).strip()))

    def test_i8b_protected_002_pinned_and_contract_set_hashes(self) -> None:
        for relative, expected in PINNED_INPUTS.items():
            with self.subTest(path=relative):
                self.assertEqual(expected, hashlib.sha256((ROOT / relative).read_bytes()).hexdigest())
        contract_set = schema.read_document(ROOT / "learning/contracts/learning-contract-set-v1.json")
        self.assertEqual(21, len(contract_set["contracts"]))
        for row in contract_set["contracts"]:
            with self.subTest(contract=row["path"]):
                self.assertEqual(row["contentSha256"], hashlib.sha256(
                    (ROOT / row["path"]).read_bytes()
                ).hexdigest())

    def test_i8b_mismatch_010_released_identifier_gap_is_exact(self) -> None:
        manifest = schema.read_document(ROOT / "learning/manifests/promotion-trust-v1.json")
        evidence = schema.read_document(
            ROOT / "tests/fixtures/learning/promotion-trust/evidence-v1.json"
        )
        self.assertEqual([
            ("promotion", ["promo_name", "channel"]),
            ("fulfillment", ["carrier", "region"]),
            ("returns", ["reason", "category", "region"]),
            ("dq", ["scenario"]),
        ], [(row["grain"], row["keys"]) for row in manifest["sources"]])
        self.assertEqual([
            ["promo_name", "channel"],
            ["carrier", "region_name"],
            ["reason", "category_name", "region_name"],
            ["scenario"],
        ], [row["grain"] for row in evidence["sources"]])
        vite_source = schema.read_regular_bytes(
            ROOT / "spikes/web/candidates/vite/src/lesson-contract.mjs"
        ).decode()
        for token in (
            "id: 'data-quality'",
            "carrier × region_name",
            "reason × category_name × region_name",
        ):
            self.assertIn(token, vite_source)

    def test_i8b_binding_absent_011_aggregate_requires_fixed_binding(self) -> None:
        self.assertEqual({}, dict(inspect.signature(check.validate_all_contracts).parameters))
        rows = check.validate_all_contracts()
        self.assertEqual(65, len(rows))
        self.load_binding()
        shipped = getattr(check, "validate_shipped_vite_binding", None)
        self.assertIsNotNone(shipped, "VITE_BINDING_REQUIRED: aggregate public path")
        snapshot = shipped()
        self.assertEqual("promotion-trust-vite-binding-v1", snapshot.document["bindingId"])
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaises(TypeError):
                check.validate_all_contracts(binding_root=pathlib.Path(temporary))

    def test_i8b_alias_020_through_boundary_027_exact_invalid_inventory(self) -> None:
        actual = {path.name for path in INVALID_ROOT.iterdir() if path.suffix == ".json"}
        self.assertEqual(set(INVALID_CASES), actual, "BINDING_FIXTURE_INDEX_INCOMPLETE")

    def test_i8b_alias_020_through_boundary_027_public_validation_codes(self) -> None:
        for name, expected in INVALID_CASES.items():
            with self.subTest(path=name):
                self.assert_code(expected, self.public_path_validator, INVALID_ROOT / name)

    def test_i8b_valid_binding_is_closed_ordered_lossless_and_deterministic(self) -> None:
        value = self.load_binding()
        first = self.public_path_validator(BINDING)
        second = self.public_path_validator(BINDING)
        self.assertEqual(value, first.document)
        self.assertEqual(first, second)
        rows = first.document["grainBindings"]
        self.assertEqual([
            ("promotion", "promotion"), ("fulfillment", "fulfillment"),
            ("returns", "returns"), ("dq", "data-quality"),
        ], [(row["stageAGrain"], row["viteGrain"]) for row in rows])
        aliases = [
            alias for row in rows for alias in row["aliases"]
            if alias["kind"] == "identifier-alias"
        ]
        self.assertEqual([
            ("region", "region_name"), ("category", "category_name"),
            ("region", "region_name"),
        ], [(row["from"], row["to"]) for row in aliases])
        self.assertEqual(2, len({(row["from"], row["to"]) for row in aliases}))

    def test_i8b_fail_closed_mapping_version_type_and_unknown_field(self) -> None:
        base = self.load_binding()
        cases = []
        missing = copy.deepcopy(base); missing["grainBindings"].pop()
        cases.append((missing, "BINDING_GRAIN_MISMATCH"))
        extra = copy.deepcopy(base); extra["grainBindings"].append(copy.deepcopy(extra["grainBindings"][0]))
        cases.append((extra, "BINDING_GRAIN_MISMATCH"))
        renamed = copy.deepcopy(base); renamed["grainBindings"][0]["stageAGrain"] = "renamed"
        cases.append((renamed, "BINDING_GRAIN_MISMATCH"))
        lossy = copy.deepcopy(base); lossy["grainBindings"][1]["aliases"].pop()
        cases.append((lossy, "BINDING_ALIAS_NOT_BIJECTIVE"))
        cyclic = copy.deepcopy(base); cyclic["grainBindings"][1]["aliases"][1].update(
            {"from": "region_name", "to": "region"}
        )
        cases.append((cyclic, "BINDING_ALIAS_CYCLIC"))
        version = copy.deepcopy(base); version["schemaVersion"] = "promotion-trust-vite-binding-v2"
        cases.append((version, "BINDING_VERSION_UNSUPPORTED"))
        wrong_type = copy.deepcopy(base); wrong_type["grainBindings"] = "four"
        cases.append((wrong_type, "BINDING_SCHEMA_INVALID"))
        unknown = copy.deepcopy(base); unknown["extension"] = {}
        cases.append((unknown, "BINDING_SCHEMA_INVALID"))
        for value, expected in cases:
            with self.subTest(expected=expected):
                self.assert_code(expected, self.public_document_validator, value)

    def test_i8b_no_copy_030_and_projection_authority_boundary(self) -> None:
        base = self.load_binding()
        for key, payload, expected in (
            ("default", "unknown", "BINDING_CONTRACT_FORK_FORBIDDEN"),
            ("transform", "lowercase", "BINDING_CONTRACT_FORK_FORBIDDEN"),
            ("operations", [], "BINDING_CONTRACT_FORK_FORBIDDEN"),
            ("records", [], "BINDING_DATA_PAYLOAD_FORBIDDEN"),
            ("url", "https://example.invalid", "BINDING_REFERENCE_FORBIDDEN"),
        ):
            mutated = copy.deepcopy(base); mutated[key] = payload
            with self.subTest(key=key):
                self.assert_code(expected, self.public_document_validator, mutated)
        self.assertEqual({
            "browserRole": "projection-only",
            "serverValidationAuthority": "stage-a-learning-contracts",
            "completionAuthority": "learning-progress-authority-v1",
            "authorize": False, "mutate": False, "validate": False,
            "complete": False, "emitEvidence": False,
        }, base["trustBoundary"])

    def test_i8b_fixed_root_descriptor_snapshot_and_substitution_refusal(self) -> None:
        self.assertEqual({}, dict(inspect.signature(check.validate_all_contracts).parameters))
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            regular = root / "regular.json"
            regular.write_bytes(schema.read_regular_bytes(INVALID_ROOT / "dependency-hash-drift.json"))
            os.link(regular, root / "hardlink.json")
            os.symlink(regular, root / "symlink.json")
            fifo = root / "fifo.json"; os.mkfifo(fifo)
            self.assertTrue(stat.S_ISFIFO(fifo.lstat().st_mode))
            for name in ("hardlink.json", "symlink.json", "fifo.json"):
                with self.subTest(path=name):
                    self.assert_code(
                        "BINDING_DOCUMENT_SPECIAL_FILE",
                        self.public_path_validator,
                        root / name,
                    )
            self.assertTrue(BINDING.is_file(), "VITE_BINDING_REQUIRED: document")
            valid_raw = schema.read_regular_bytes(BINDING)
            race_path = root / "race.json"; race_path.write_bytes(valid_raw)
            snapshot = self.public_path_validator(race_path)
            race_path.write_bytes(schema.read_regular_bytes(
                INVALID_ROOT / "dependency-hash-drift.json"
            ))
            self.assertEqual(hashlib.sha256(valid_raw).hexdigest(), snapshot.hashes[
                "learning/bindings/vite/promotion-trust-v1.json"
            ])
            self.assertEqual("promotion-trust-vite-binding-v1", snapshot.document["bindingId"])

    def test_i8b_no_generated_types_031_and_changed_path_boundary(self) -> None:
        changed = set(subprocess.check_output(
            ["git", "diff", "--name-only", f"{COOK_INPUT_SHA}...HEAD"], cwd=ROOT, text=True
        ).splitlines())
        changed.update(subprocess.check_output(
            ["git", "ls-files", "--others", "--exclude-standard"], cwd=ROOT, text=True
        ).splitlines())
        self.assertTrue(changed <= ALLOWLIST, sorted(changed - ALLOWLIST))
        self.assertFalse(any(path.endswith((".ts", ".tsx", ".d.ts")) for path in changed))
        self.assertFalse(any(path.startswith(("apps/", "runner/")) for path in changed))


if __name__ == "__main__":
    unittest.main()
