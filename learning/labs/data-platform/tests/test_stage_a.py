from __future__ import annotations

import copy
import importlib.util
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[4]
MODULE_PATH = ROOT / "learning/labs/data-platform/verify_stage_a.py"
SPEC = importlib.util.spec_from_file_location("verify_stage_a", MODULE_PATH)
assert SPEC and SPEC.loader
VERIFY = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY)


class StageAContractTests(unittest.TestCase):
    def test_repository_contract_passes(self) -> None:
        result = VERIFY.verify_repository(ROOT)
        self.assertEqual("candidate-not-runnable", result["claim"])
        self.assertEqual(3, result["labs"])

    def test_released_authority_hashes_are_pinned(self) -> None:
        VERIFY.verify_hashes(ROOT, VERIFY.AUTHORITY_HASHES, "RELEASED_AUTHORITY_DRIFT")

    def test_golden_files_are_protected(self) -> None:
        VERIFY.verify_hashes(ROOT, VERIFY.PROTECTED_HASHES, "PROTECTED_GOLDEN_DRIFT")

    def test_all_descriptors_validate_against_released_lab_v1(self) -> None:
        for lab_id in VERIFY.LAB_IDS:
            with self.subTest(lab_id=lab_id):
                value = VERIFY.read_json(ROOT / f"learning/labs/data-platform/{lab_id}/lab-v1.json")
                VERIFY.verify_descriptor(lab_id, value, ROOT)

    def test_content_pairing_and_full_lifecycle(self) -> None:
        for lab_id in VERIFY.LAB_IDS:
            with self.subTest(lab_id=lab_id):
                text = (ROOT / f"learning/labs/data-platform/{lab_id}/content.vi.md").read_text()
                VERIFY.verify_content(lab_id, text)

    def test_missing_lifecycle_is_rejected(self) -> None:
        path = ROOT / "learning/labs/data-platform/deterministic-ingest/content.vi.md"
        text = path.read_text().replace("## Reset", "## Khôi phục")
        with self.assertRaisesRegex(VERIFY.StageAError, "^LAB_LIFECYCLE_MISSING$"):
            VERIFY.verify_content("deterministic-ingest", text)

    def test_bad_metric_grain_and_average_are_rejected(self) -> None:
        path = ROOT / "learning/labs/data-platform/weighted-metrics/content.vi.md"
        text = path.read_text()
        for mutation in (
            text.replace("(carrier, region_name)", "(order_id)"),
            text.replace("5.456625", "5.34"),
        ):
            with self.subTest():
                with self.assertRaisesRegex(VERIFY.StageAError, "^METRIC_GRAIN_OR_AVERAGE_INVALID$"):
                    VERIFY.verify_content("weighted-metrics", mutation)

    def test_unsafe_content_is_rejected(self) -> None:
        path = ROOT / "learning/labs/data-platform/deterministic-ingest/content.vi.md"
        text = path.read_text()
        cases = {
            "BROAD_MUTATION_CONTENT": "\nrm -rf workspace\n",
            "UNSAFE_PATH_CONTENT": "\n`/Users/example/evidence`\n",
            "UNSAFE_LINK_CONTENT": "\n[x](https://private.example)\n",
            "PRIVATE_OR_SECRET_CONTENT": "\n" + "gh" + "p_" + "x" * 30 + "\n",
        }
        for code, suffix in cases.items():
            with self.subTest(code=code):
                with self.assertRaisesRegex(VERIFY.StageAError, f"^{code}$"):
                    VERIFY.verify_content("deterministic-ingest", text + suffix)

    def test_path_traversal_in_descriptor_is_rejected(self) -> None:
        path = ROOT / "learning/labs/data-platform/deterministic-ingest/lab-v1.json"
        value = copy.deepcopy(VERIFY.read_json(path))
        value["workspace"]["allowedPaths"] = ["../golden"]
        with self.assertRaisesRegex(VERIFY.StageAError, "^LAB_SCHEMA_INVALID$"):
            VERIFY.verify_descriptor("deterministic-ingest", value, ROOT)

    def test_activation_enables_only_static_lake_contract_check(self) -> None:
        path = ROOT / "learning/labs/data-platform/command-owner-activation.stage-a.json"
        value = VERIFY.read_json(path)
        VERIFY.verify_activation(value, ROOT)
        self.assertEqual(["lake-contracts-check"], [item["commandId"] for item in value["commands"]])

    def test_weighted_projection_uses_real_golden_rows(self) -> None:
        weighted, invalid, weight = VERIFY.weighted_projection(ROOT)
        self.assertEqual("5.456625", str(weighted))
        self.assertEqual("5.34", str(invalid))
        self.assertEqual(800, weight)

    def test_run_owned_evidence_reset_cleans_only_its_run(self) -> None:
        VERIFY.verify_run_owned_reset()

    def test_self_test_covers_negative_matrix(self) -> None:
        result = VERIFY.self_test(ROOT)
        self.assertGreaterEqual(result["negativeCases"], 11)
        self.assertEqual("pass", result["cleanup"])


if __name__ == "__main__":
    unittest.main()
