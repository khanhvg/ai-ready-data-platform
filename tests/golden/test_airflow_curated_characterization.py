from __future__ import annotations

import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


class AirflowCuratedCharacterizationTests(unittest.TestCase):
    def test_current_dag_and_curated_assets_are_exact(self) -> None:
        dag = (ROOT / "orchestration/airflow/dags/retail_batch_pipeline.py").read_text(encoding="utf-8")
        for task_id in ("seed", "load_raw", "health_check", "dbt_build", "dbt_docs_generate", "export_marts_snapshot", "publish_iceberg", "iceberg_read_back"):
            self.assertIn(task_id, dag)
        assets = json.loads((ROOT / "lake/curated_assets.json").read_text(encoding="utf-8"))
        rows = assets.get("assets", assets) if isinstance(assets, dict) else assets
        self.assertEqual(11, len(rows))

    def test_public_command_surface_is_not_available_before_phase_seven(self) -> None:
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        fragment = ROOT / "mk/issue-5/i5-01.mk"
        self.assertIn("-include $(ISSUE_5_MAKE_FRAGMENTS)", makefile, "P1-RED-COMMANDS-MISSING")
        self.assertTrue(fragment.is_file(), "P1-RED-COMMANDS-MISSING")
        self.assertIn("golden-clean:", fragment.read_text(encoding="utf-8"), "P1-RED-COMMANDS-MISSING")

    def test_architecture_sources_are_not_available_before_phase_six(self) -> None:
        self.assertTrue((ROOT / "architecture/likec4/specification.c4").is_file(), "P1-RED-ARCH-SOURCES-MISSING")


if __name__ == "__main__":
    unittest.main()
