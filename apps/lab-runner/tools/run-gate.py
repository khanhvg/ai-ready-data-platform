#!/usr/bin/env python3
"""Fixed no-selector Issue #9 shard harness.

The initial commit is an intentionally semantics-free RED scaffold.  It loads
every declared case, proves its fixture/precondition marker, then reports the
specific production policy that is not implemented yet.  Later implementation
commits replace ``evaluate_case`` with public runner invocations; the manifest
and expected oracles remain immutable.
"""
from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[3]
APP = ROOT / "apps/lab-runner"
MANIFEST = APP / "tests/red-manifest.json"


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate_case(row: dict[str, object]) -> dict[str, object]:
    fixture = APP / str(row["fixture"])
    if not fixture.is_file():
        raise RuntimeError(f"fixture missing before marker: {fixture.name}")
    marker = {"fixture": fixture.relative_to(APP).as_posix(), "sha256": sha256(fixture)}
    return {
        "id": row["id"],
        "status": "fail",
        "fixtureMarker": marker,
        "failureCode": f"BEHAVIOR_NOT_IMPLEMENTED:{row['oracle']}",
        "oracle": row["oracle"],
    }


def main() -> int:
    if len(sys.argv) != 1:
        print("run-gate accepts no selectors", file=sys.stderr)
        return 2
    started = time.monotonic_ns()
    manifest_raw = MANIFEST.read_bytes()
    manifest = json.loads(manifest_raw)
    ids = [row["id"] for row in manifest["rows"]]
    if len(ids) != 66 or len(ids) != len(set(ids)):
        raise RuntimeError("RED_S3_MANIFEST_CLOSURE")
    results = [evaluate_case(row) for row in manifest["rows"]]
    output = {
        "schemaVersion": "runner-red-provenance-v1",
        "inputSha": os.environ.get("COOK_INPUT_SHA", "f6791555dc8b2ada6fa44747ca829a3d9cd87667"),
        "manifestSha256": hashlib.sha256(manifest_raw).hexdigest(),
        "redRows": sum(str(row["id"]).startswith("RED-") for row in results),
        "s3Rows": sum(str(row["id"]).startswith("S3-") for row in results),
        "failedAsDesigned": sum(row["status"] == "fail" for row in results),
        "durationNs": time.monotonic_ns() - started,
        "results": results,
    }
    print(json.dumps(output, sort_keys=True, separators=(",", ":")))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
