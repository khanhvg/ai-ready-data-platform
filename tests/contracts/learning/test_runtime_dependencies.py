from __future__ import annotations

import hashlib
import json
import os
import pathlib
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest

from scripts.learning_contracts import check, runtime
from scripts.learning_contracts.schema import LearningContractError


class S3CommandResourceCleanupTests(unittest.TestCase):
    def assert_code(self, expected: str, call, *args, **kwargs) -> None:
        with self.assertRaises(LearningContractError) as caught:
            call(*args, **kwargs)
        self.assertEqual(expected, caught.exception.code)

    def marker(self, path: pathlib.Path, entries: list[dict[str, str]]) -> dict[str, object]:
        info = path.lstat()
        return {
            "schemaVersion": "learning-owner-v1",
            "nonce": "a" * 64,
            "device": info.st_dev,
            "inode": info.st_ino,
            "closed": True,
            "entries": entries,
        }

    def write_marker(self, path: pathlib.Path, value: dict[str, object]) -> None:
        (path / ".learning-owner.json").write_text(json.dumps(value, sort_keys=True), encoding="utf-8")

    def test_i8_v3_s3_special_file_locator_019(self) -> None:
        """I8-V3-S3-SPECIAL-FILE-LOCATOR-019."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            fifo = root / "blocked"
            os.mkfifo(fifo)
            started = time.monotonic()
            self.assert_code("LOCATOR_SPECIAL_FILE", runtime.validate_evidence_locator, root, "blocked", "0" * 64)
            self.assertLess(time.monotonic() - started, 0.5)
            regular = root / "regular"
            regular.write_bytes(b"content")
            os.symlink(regular.name, root / "symlink")
            os.link(regular, root / "hardlink")
            endpoint = socket.socket(socket.AF_UNIX)
            try:
                endpoint.bind(str(root / "socket"))
                for locator in ("symlink", "hardlink", "socket"):
                    with self.subTest(locator=locator):
                        self.assert_code(
                            "LOCATOR_SPECIAL_FILE",
                            runtime.validate_evidence_locator,
                            root,
                            locator,
                            hashlib.sha256(b"content").hexdigest(),
                        )
            finally:
                endpoint.close()

    def test_i8_v3_public_command_injection_020(self) -> None:
        """I8-V3-PUBLIC-COMMAND-INJECTION-020."""
        with tempfile.TemporaryDirectory() as temporary:
            sentinel = pathlib.Path(temporary) / "injected"
            hostile = f"promotion-trust;touch {sentinel}"
            self.assert_code("PUBLIC_ARGUMENT_INVALID", check.main, ["check", "--lesson", hostile])
            self.assertFalse(sentinel.exists())

    def test_i8_v3_secret_private_pii_refusal_021(self) -> None:
        """I8-V3-SECRET-PRIVATE-PII-REFUSAL-021."""
        self.assertEqual("promotion-trust", check.validate_public_value("LESSON", "promotion-trust"))
        for value in ("/Users/private/evidence.json", "AKIAIOSFODNN7EXAMPLE", "learner@example.com", "$(touch injected)"):
            with self.subTest(value=value):
                self.assert_code("PUBLIC_ARGUMENT_INVALID", check.validate_public_value, "EVIDENCE", value)

    def test_i8_v3_resource_process_tree_022(self) -> None:
        """I8-V3-RESOURCE-PROCESS-TREE-022."""
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            output = runtime.run_bounded([sys.executable, "-c", "print('ok')"], cwd=root, timeout=2)
            self.assertEqual(b"ok\n", output)
            child_code = (
                "import pathlib,subprocess,sys,time;"
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);"
                "pathlib.Path('child.pid').write_text(str(p.pid));time.sleep(30)"
            )
            self.assert_code("PROCESS_TIMEOUT", runtime.run_bounded, [sys.executable, "-c", child_code], cwd=root, timeout=0.2)
            child_pid = int((root / "child.pid").read_text(encoding="utf-8"))
            with self.assertRaises(ProcessLookupError):
                os.kill(child_pid, 0)
            rss_code = "x=bytearray(32*1024*1024);print(len(x))"
            self.assert_code("PROCESS_RSS_LIMIT", runtime.run_bounded, [sys.executable, "-c", rss_code], cwd=root, timeout=2, max_rss_bytes=16 * 1024 * 1024)
            output_code = "import sys;sys.stdout.write('x' * 65537)"
            self.assert_code("PROCESS_OUTPUT_LIMIT", runtime.run_bounded, [sys.executable, "-c", output_code], cwd=root, timeout=2, output_limit=65536)
            lingering = (
                "import pathlib,subprocess,sys;"
                "p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)']);"
                "pathlib.Path('lingering.pid').write_text(str(p.pid))"
            )
            self.assert_code(
                "PROCESS_CLEANUP_FAILED", runtime.run_bounded,
                [sys.executable, "-c", lingering], cwd=root, timeout=2,
            )
            lingering_pid = int((root / "lingering.pid").read_text(encoding="utf-8"))
            with self.assertRaises(ProcessLookupError):
                os.kill(lingering_pid, 0)

    def test_six_high_h6_term_resistant_tree_and_foreign_process(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            foreign = subprocess.Popen([sys.executable, "-c", "import time;time.sleep(30)"])
            resistant = (
                "import os,pathlib,signal,subprocess,sys,time;"
                "signal.signal(signal.SIGTERM,signal.SIG_IGN);"
                "p=subprocess.Popen([sys.executable,'-c',"
                "'import signal,time;signal.signal(signal.SIGTERM,signal.SIG_IGN);time.sleep(30)']);"
                "pathlib.Path('resistant.pid').write_text(str(p.pid));time.sleep(30)"
            )
            try:
                self.assert_code(
                    "PROCESS_TIMEOUT", runtime.run_bounded,
                    [sys.executable, "-c", resistant], cwd=root, timeout=0.2,
                )
                owned_pid = int((root / "resistant.pid").read_text(encoding="utf-8"))
                with self.assertRaises(ProcessLookupError):
                    os.kill(owned_pid, 0)
                os.kill(foreign.pid, 0)
            finally:
                foreign.terminate()
                foreign.wait(timeout=3)

    def test_i8_v3_cleanup_owned_manifest_023(self) -> None:
        """I8-V3-CLEANUP-OWNED-MANIFEST-023."""
        with tempfile.TemporaryDirectory() as temporary:
            owned = pathlib.Path(temporary) / "owned"
            owned.mkdir()
            (owned / "mutable.tmp").write_bytes(b"mutable")
            (owned / "evidence.json").write_bytes(b"evidence")
            marker = self.marker(owned, [{"path": "mutable.tmp", "disposition": "mutable"}, {"path": "evidence.json", "disposition": "preserve"}])
            self.write_marker(owned, marker)
            wrong = dict(marker, nonce="b" * 64)
            self.assert_code("CLEANUP_OWNERSHIP_MISMATCH", runtime.cleanup_owned, owned, wrong, owned_root=owned.parent)
            runtime.cleanup_owned(owned, marker, owned_root=owned.parent)
            self.assertFalse((owned / "mutable.tmp").exists())
            self.assertEqual(b"evidence", (owned / "evidence.json").read_bytes())
            (owned / "first.tmp").write_bytes(b"first")
            (owned / "regular").write_bytes(b"regular")
            os.symlink("regular", owned / "unsafe")
            marker = self.marker(owned, [
                {"path": "evidence.json", "disposition": "preserve"},
                {"path": "first.tmp", "disposition": "mutable"},
                {"path": "regular", "disposition": "preserve"},
                {"path": "unsafe", "disposition": "mutable"},
            ])
            self.write_marker(owned, marker)
            self.assert_code("CLEANUP_ENTRY_UNSAFE", runtime.cleanup_owned, owned, marker, owned_root=owned.parent)
            self.assertEqual(b"first", (owned / "first.tmp").read_bytes())

    def test_i8_v3_rollback_foreign_preservation_024(self) -> None:
        """I8-V3-ROLLBACK-FOREIGN-PRESERVATION-024."""
        with tempfile.TemporaryDirectory() as temporary:
            owned = pathlib.Path(temporary) / "owned"
            owned.mkdir()
            (owned / "mutable.tmp").write_bytes(b"mutable")
            marker = self.marker(owned, [{"path": "mutable.tmp", "disposition": "mutable"}])
            self.write_marker(owned, marker)
            (owned / "foreign.sentinel").write_bytes(b"foreign")
            self.assert_code("CLEANUP_MANIFEST_OPEN", runtime.cleanup_owned, owned, marker, owned_root=owned.parent)
            self.assertEqual(b"mutable", (owned / "mutable.tmp").read_bytes())
            self.assertEqual(b"foreign", (owned / "foreign.sentinel").read_bytes())
            (owned / "foreign.sentinel").unlink()
            runtime.cleanup_owned(owned, marker, owned_root=owned.parent)
            runtime.cleanup_owned(owned, marker, owned_root=owned.parent)
            self.assertFalse((owned / "mutable.tmp").exists())

    def test_six_high_h6_runtime_admission_is_exact_and_unique(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            expected = {
                "schemaVersion": "learning-runtime-admission-v1",
                "interpreterSha256": "1" * 64,
                "toolSha256": "2" * 64,
                "lockSha256": "3" * 64,
                "planSha256": "4" * 64,
                "inputSha": "abcaa2de7247d99c642fcad1535c24870f08c79f",
            }
            self.assert_code("RUNTIME_ADMISSION_COUNT", runtime.select_admitted_runtime, root, expected)
            for name in ("first", "second"):
                candidate = root / name
                candidate.mkdir()
                (candidate / "runtime-admission.json").write_text(json.dumps(expected), encoding="utf-8")
            self.assert_code("RUNTIME_ADMISSION_COUNT", runtime.select_admitted_runtime, root, expected)

    def test_six_high_h6_runtime_admission_rejects_stale_and_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            candidate = root / "only"
            interpreter = candidate / "venv/bin/python"
            interpreter.parent.mkdir(parents=True)
            shutil.copy2(sys.executable, interpreter)
            expected = {
                "schemaVersion": "learning-runtime-admission-v1",
                "interpreterSha256": hashlib.sha256(interpreter.read_bytes()).hexdigest(),
                "toolSha256": "2" * 64,
                "lockSha256": "3" * 64,
                "planSha256": "4" * 64,
                "inputSha": "abcaa2de7247d99c642fcad1535c24870f08c79f",
            }
            marker = dict(expected)
            marker["inputSha"] = "0" * 40
            (candidate / "runtime-admission.json").write_text(json.dumps(marker), encoding="utf-8")
            self.assert_code("RUNTIME_ADMISSION_MISMATCH", runtime.select_admitted_runtime, root, expected)
            (candidate / "runtime-admission.json").write_text(json.dumps(expected), encoding="utf-8")
            interpreter.write_bytes(b"stale")
            self.assert_code("RUNTIME_INTERPRETER_MISMATCH", runtime.select_admitted_runtime, root, expected)

    def test_six_high_h6_public_make_targets_use_bounded_launcher(self) -> None:
        fragment = (pathlib.Path(__file__).resolve().parents[3] / "mk/issue-5/i5-03.mk").read_text(encoding="utf-8")
        self.assertNotIn("wildcard", fragment)
        self.assertNotIn("lastword", fragment)
        for target in ("learning-contracts-check", "lesson-check", "api-contracts-check", "evidence-verify"):
            recipe = fragment.split(f"{target}:", 1)[1].split("\n\n", 1)[0]
            self.assertIn("scripts.learning_contracts.runtime launch", recipe)
            self.assertNotIn("$(LEARNING_CONTRACTS_PY)", recipe)

    def test_six_high_h6_launcher_starts_with_stdlib_only(self) -> None:
        result = subprocess.run(
            [sys.executable, "-S", "-m", "scripts.learning_contracts.runtime", "--help"],
            cwd=pathlib.Path(__file__).resolve().parents[3],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout.decode("utf-8", "replace"))


if __name__ == "__main__":
    unittest.main()
