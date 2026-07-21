from __future__ import annotations

import hashlib
import json
import os
import pathlib
import signal
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
            for locator in ("symlink", "hardlink"):
                with self.subTest(locator=locator):
                    self.assert_code("LOCATOR_SPECIAL_FILE", runtime.validate_evidence_locator, root, locator, hashlib.sha256(b"content").hexdigest())

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
            self.assert_code("CLEANUP_OWNERSHIP_MISMATCH", runtime.cleanup_owned, owned, wrong)
            runtime.cleanup_owned(owned, marker)
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
            self.assert_code("CLEANUP_ENTRY_UNSAFE", runtime.cleanup_owned, owned, marker)
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
            self.assert_code("CLEANUP_MANIFEST_OPEN", runtime.cleanup_owned, owned, marker)
            self.assertEqual(b"mutable", (owned / "mutable.tmp").read_bytes())
            self.assertEqual(b"foreign", (owned / "foreign.sentinel").read_bytes())
            (owned / "foreign.sentinel").unlink()
            runtime.cleanup_owned(owned, marker)
            runtime.cleanup_owned(owned, marker)
            self.assertFalse((owned / "mutable.tmp").exists())


if __name__ == "__main__":
    unittest.main()
