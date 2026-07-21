from __future__ import annotations

import importlib.util
import pathlib
import os
import time
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_process():
    path = ROOT / "scripts/golden/process.py"
    if not path.is_file():
        raise AssertionError("P3-RED-TIMEOUT-DESCENDANT")
    spec = importlib.util.spec_from_file_location("golden_process", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProcessSecurityTests(unittest.TestCase):
    def test_timeout_terminates_owned_process_group(self) -> None:
        process = load_process()
        with tempfile.TemporaryDirectory() as temp:
            pid_file=pathlib.Path(temp)/"grandchild.pid"
            code="import signal,subprocess,sys,time; p=subprocess.Popen([sys.executable,'-c','import signal,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); time.sleep(30)']); open(sys.argv[1],'w').write(str(p.pid)); time.sleep(30)"
            with self.assertRaisesRegex(process.ProcessError, "PROCESS_TIMEOUT"):
                process.run_bounded(
                    [sys.executable, "-c", code, str(pid_file)],
                    cwd=pathlib.Path(temp),
                    env={"PATH": str(pathlib.Path(sys.executable).parent)},
                    timeout_seconds=0.1,
                )
            grandchild=int(pid_file.read_text())
            deadline=time.monotonic()+2
            while time.monotonic()<deadline:
                try: os.kill(grandchild,0)
                except ProcessLookupError: break
                time.sleep(0.02)
            else: self.fail("owned timeout descendant remained")


if __name__ == "__main__":
    unittest.main()
