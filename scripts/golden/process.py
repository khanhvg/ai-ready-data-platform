#!/usr/bin/env python3
"""Bounded, explicitly-owned child process execution."""

from __future__ import annotations

import hashlib
import os
import pathlib
import signal
import subprocess
import tempfile
import time


MAX_STREAM = 2 * 1024 * 1024


class ProcessError(RuntimeError):
    def __init__(self, code: str, *, stdout: bytes = b"", stderr: bytes = b""):
        super().__init__(code)
        self.code = code
        self.stdout = stdout
        self.stderr = stderr


def _bounded(stream: bytes) -> tuple[bytes, str, int]:
    digest = hashlib.sha256(stream).hexdigest()
    if len(stream) <= MAX_STREAM:
        return stream, digest, len(stream)
    retained = stream[: MAX_STREAM // 2] + b"\n<bounded-output-omitted>\n" + stream[-MAX_STREAM // 2 :]
    return retained, digest, len(stream)


def run_bounded(
    command: list[str],
    *,
    cwd: pathlib.Path,
    env: dict[str, str],
    timeout_seconds: float,
) -> dict[str, object]:
    if not command or timeout_seconds <= 0:
        raise ProcessError("PROCESS_ARGUMENT_INVALID")
    child_env = {str(key): str(value) for key, value in env.items()}
    child_env.pop("PYTHONPATH", None)
    started = time.monotonic()
    with tempfile.TemporaryFile(dir=cwd) as out_file, tempfile.TemporaryFile(dir=cwd) as err_file:
        process = subprocess.Popen(command,cwd=cwd,env=child_env,stdin=subprocess.DEVNULL,stdout=out_file,stderr=err_file,start_new_session=True)
        deadline=started+timeout_seconds; failure=None
        while process.poll() is None:
            if time.monotonic()>=deadline: failure="PROCESS_TIMEOUT"
            elif os.fstat(out_file.fileno()).st_size>MAX_STREAM or os.fstat(err_file.fileno()).st_size>MAX_STREAM: failure="PROCESS_OUTPUT_LIMIT"
            if failure:
                pgid=process.pid; os.killpg(pgid,signal.SIGTERM); grace=time.monotonic()+5
                while time.monotonic()<grace:
                    process.poll()
                    try: os.killpg(pgid,0)
                    except (ProcessLookupError,PermissionError): break
                    time.sleep(0.05)
                try: os.killpg(pgid,signal.SIGKILL)
                except ProcessLookupError: pass
                process.wait(timeout=5)
                cleanup=time.monotonic()+5
                while time.monotonic()<cleanup:
                    try: os.killpg(pgid,0)
                    except (ProcessLookupError,PermissionError): break
                    time.sleep(0.05)
                else: raise ProcessError("PROCESS_CLEANUP_FAILED")
                break
            time.sleep(0.01)
        out_file.seek(0); err_file.seek(0); stdout=out_file.read(MAX_STREAM+1); stderr=err_file.read(MAX_STREAM+1)
    if failure:
        bounded_out, _, _ = _bounded(stdout); bounded_err, _, _ = _bounded(stderr)
        raise ProcessError(failure,stdout=bounded_out,stderr=bounded_err)
    out, out_sha, out_bytes = _bounded(stdout)
    err, err_sha, err_bytes = _bounded(stderr)
    if out_bytes > MAX_STREAM or err_bytes > MAX_STREAM:
        raise ProcessError("PROCESS_OUTPUT_LIMIT", stdout=out, stderr=err)
    return {
        "returnCode": process.returncode,
        "durationMs": round((time.monotonic() - started) * 1000),
        "stdout": out,
        "stderr": err,
        "stdoutSha256": out_sha,
        "stderrSha256": err_sha,
        "stdoutBytes": out_bytes,
        "stderrBytes": err_bytes,
    }
