from __future__ import annotations
import importlib.util
import hashlib
import pathlib
import tempfile
import unittest

APP = pathlib.Path(__file__).resolve()
while APP.name != "lab-runner":
    APP = APP.parent
spec = importlib.util.spec_from_file_location("runner_gate", APP / "tools/run-gate.py")
assert spec and spec.loader
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
ROWS = {row["id"]: row for row in __import__("json").loads((APP / "tests/red-manifest.json").read_text())["rows"]}


class RedPublicPathTest(unittest.TestCase):
    def test_seccomp_and_worker_memory_match_the_plan(self) -> None:
        import json
        profile=json.loads((APP/"container/seccomp-runner-v1.json").read_text())
        allowed={name for row in profile["syscalls"] if row.get("action")=="SCMP_ACT_ALLOW" for name in row.get("names",[])}
        self.assertTrue({"ptrace","process_vm_readv","process_vm_writev"}.isdisjoint(allowed))
        supervisor=(APP/"src/lab_runner/container_supervisor.py").read_text()
        self.assertIn("resource.RLIMIT_AS",supervisor)

    def test_image_fixes_allocator_and_native_worker_limits_before_python_start(self) -> None:
        dockerfile=(APP/"container/runner.Dockerfile").read_text()
        for setting in (
            "MALLOC_ARENA_MAX=1",
            "OMP_NUM_THREADS=1",
            "OPENBLAS_NUM_THREADS=1",
            "MKL_NUM_THREADS=1",
            "NUMEXPR_NUM_THREADS=1",
        ):
            with self.subTest(setting=setting):
                self.assertIn(setting,dockerfile)

    def test_release_record_binds_build_and_gate_aggregates(self) -> None:
        import hashlib,json
        release=json.loads((APP/"config/runner-image-release-v1.json").read_text())
        build=APP/"config/container-build-lock-v1.json"
        self.assertEqual(hashlib.sha256(build.read_bytes()).hexdigest(),release["buildLockSha256"])
        self.assertEqual(8,len(release["operationResults"]))
        self.assertEqual({"redRows":52,"s3Rows":14,"passed":66,"failed":0},release["gateAggregate"])
        self.assertEqual(2,release["rollbackAggregate"]["attempts"])

    def test_release_result_identity_retains_semantics_but_not_run_manifest_identity(self) -> None:
        first={"tables":18,"manifestSha256":"a"*64,"nested":{"dataRunId":"b"*64,"models":51}}
        replay={"tables":18,"manifestSha256":"c"*64,"nested":{"dataRunId":"d"*64,"models":51}}
        changed={"tables":17,"manifestSha256":"a"*64,"nested":{"dataRunId":"b"*64,"models":51}}
        self.assertEqual(gate.stable_result_sha256(first),gate.stable_result_sha256(replay))
        self.assertNotEqual(gate.stable_result_sha256(first),gate.stable_result_sha256(changed))

    def test_supply_lock_requires_every_selected_wheel_hash(self) -> None:
        expected={"selected.whl":"a"*64,"second.whl":"b"*64}
        lock="package==1 --hash=sha256:"+"a"*64+" --hash=sha256:"+"b"*64+" --hash=sha256:"+"c"*64
        self.assertTrue(gate.wheelhouse_lock_complete(expected,lock))
        self.assertFalse(gate.wheelhouse_lock_complete({**expected,"missing.whl":"d"*64},lock))

    def test_ignored_session_log_may_only_append_to_the_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path=pathlib.Path(temporary)/"session.log";path.write_bytes(b"baseline")
            baseline={"size":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()}
            path.write_bytes(b"baseline-appended")
            self.assertTrue(gate.append_only_file_matches(path,baseline))
            path.write_bytes(b"rewritten-appended")
            self.assertFalse(gate.append_only_file_matches(path,baseline))

    def test_memory_probe_uses_multiple_rlimit_bounded_workers_for_aggregate_cgroup(self) -> None:
        fixture=(APP/"tests/fixtures/resource_probe.py").read_text()
        supervisor=(APP/"src/lab_runner/container_supervisor.py").read_text()
        self.assertIn("os.fork()",fixture)
        self.assertIn('fixture==("resource_probe.py",("memory",)) and int(cgroup["memoryEvents"].get("oom_kill",0))>=1',supervisor)

    def test_write_lease_recognizes_exact_content_inherited_from_a_merge(self) -> None:
        inherited=gate.inherited_merge_blobs(gate.COOK_INPUT)
        path="apps/learning-portal/index.html"
        self.assertIn(path,inherited)
        self.assertEqual(gate._git_blob("HEAD",path),inherited[path])

    def test_named_behavior_passes_public_gate(self) -> None:
        for case_id in ["RED-ENV-001","RED-ENV-002","RED-RES-001"]:
            with self.subTest(case_id=case_id):
                result = gate.evaluate_case(ROWS[case_id])
                self.assertIn("fixtureMarker", result)
                self.assertEqual(result["status"], "pass", result["failureCode"])


if __name__ == "__main__":
    unittest.main()
