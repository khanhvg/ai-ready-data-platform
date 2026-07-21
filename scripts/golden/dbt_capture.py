#!/usr/bin/env python3
"""Capture immutable dbt build files before the disjoint docs invocation."""

from __future__ import annotations

import hashlib
import os
import pathlib


class CaptureError(RuntimeError): pass


def hash_file(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def capture_build(source: pathlib.Path, destination: pathlib.Path) -> dict[str, str]:
    try:
        destination.mkdir(mode=0o700, parents=True, exist_ok=False)
    except FileExistsError as exc:
        raise CaptureError("DBT_RAW_CAPTURE_EXISTS") from exc
    hashes: dict[str, str] = {}
    for path in sorted(source.iterdir()):
        if path.is_symlink() or not path.is_file(): continue
        payload = path.read_bytes()
        target = destination / path.name
        fd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        try:
            os.write(fd, payload); os.fsync(fd)
        finally: os.close(fd)
        hashes[path.name] = hashlib.sha256(payload).hexdigest()
    if not hashes: raise CaptureError("DBT_RAW_CAPTURE_EMPTY")
    return hashes
