from __future__ import annotations
import ast, importlib.util, pathlib, subprocess, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
CURRENT={"venv","up","down","seed","load","health","dbt","dbt-docs","airflow","bi","catalog","lake-up","lake-publish","catalog-ingest","clean"}
ISSUE6={"help","golden-clean","data-contracts-check","evidence-contracts-check","migration-contracts-check","architecture-check","architecture-render"}
class MakeCompatibilityTests(unittest.TestCase):
    def test_current_targets_and_seven_recipes(self) -> None:
        makefile=(ROOT/"Makefile").read_text()
        snapshot=ROOT/"learning/contracts/make-input-contract-v1.json"
        if not snapshot.is_file(): self.fail("P7-RED-15-TARGET-COMPAT")
        names={line.split(":",1)[0] for line in makefile.splitlines() if line and not line.startswith(("\t",".","#","-")) and ":" in line and "=" not in line.split(":",1)[0]}
        if not CURRENT <= names: self.fail("P7-RED-15-TARGET-COMPAT")
    def test_seven_recipes_and_help(self) -> None:
        fragment=ROOT/"mk/issue-5/i5-01.mk"
        if not fragment.is_file(): self.fail("P7-RED-SEVEN-RECIPES\nP7-RED-HELP-AVAILABILITY")
        fragment_names={line.split(":",1)[0] for line in fragment.read_text().splitlines() if line and not line.startswith(("\t",".","#","-")) and ":" in line}
        self.assertEqual(ISSUE6,fragment_names)
        registry=__import__("json").loads((ROOT/"learning/contracts/command-owner-registry-v1.json").read_text())
        self.assertTrue(any(row["availability"]=="future-owner" for row in registry["commands"]))
    def test_airflow_explicit_private_paths_and_graph_callers(self) -> None:
        path=ROOT/"orchestration/airflow/callables/pipeline.py"; tree=ast.parse(path.read_text())
        functions={node.name:node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.AsyncFunctionDef))}
        expected={"seed":{"raw_dir"},"load_raw":{"raw_dir","duckdb_path"},"health_check":{"duckdb_path"},"dbt_build":{"dbt_profiles_dir","dbt_target_path","dbt_log_path"},"dbt_docs_generate":{"dbt_profiles_dir","dbt_target_path","dbt_log_path"},"export_marts_snapshot":{"duckdb_path","export_dir"}}
        missing=[]
        for name,parameters in expected.items(): missing.extend(sorted(parameters-{arg.arg for arg in functions[name].args.args}))
        if missing: self.fail("P7-RED-AIRFLOW-PRIVATE-PATHS\nP7-RED-AIRFLOW-GRAPH-CALLERS")
        dag=ROOT/"orchestration/airflow/dags/retail_batch_pipeline.py"; self.assertTrue(dag.is_file())
        spec=importlib.util.spec_from_file_location("airflow_pipeline",path); assert spec and spec.loader
        module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
        calls=[]; module._run=lambda command,cwd=None,extra_env=None: calls.append((command,cwd,extra_env)) or ""
        with tempfile.TemporaryDirectory() as temp:
            private=pathlib.Path(temp)
            module.seed(raw_dir=private/"raw"); module.load_raw(private/"raw",private/"warehouse.duckdb")
            module.dbt_build(private/"profiles",private/"build-target",private/"build-logs")
            module.dbt_docs_generate(private/"profiles",private/"docs-target",private/"docs-logs")
            module.export_marts_snapshot(private/"warehouse.duckdb",private/"export")
        flattened=" ".join(" ".join(str(part) for part in call[0]) for call in calls)
        for option in ("--out","--raw-dir","--duckdb-path","--export-dir"): self.assertIn(option,flattened)
        self.assertEqual(str(private/"profiles"),calls[2][2]["DBT_PROFILES_DIR"])
        self.assertEqual(str(private/"build-target"),calls[2][2]["DBT_TARGET_PATH"])
        self.assertEqual(str(private/"docs-logs"),calls[3][2]["DBT_LOG_PATH"])
if __name__=="__main__": unittest.main()
