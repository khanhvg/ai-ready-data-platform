from __future__ import annotations

import datetime
import argparse
import hashlib
import json
import math
import os
import pathlib
import re
import resource
import stat
import subprocess
import sys
import time
import unicodedata
from typing import Any


ROOT = pathlib.Path(__file__).resolve().parents[3]
MAX_JSON_BYTES = 256 * 1024
MAX_DEPTH = 16
MAX_ARRAY_ITEMS = 256
MAX_STRING_BYTES = 8 * 1024
MAX_SAFE_INTEGER = 2**53 - 1
PRIVATE_PATH = re.compile(r"(?i)(?:/Users/|/home/|file://|\\\\Users\\)")


class ContentError(ValueError):
    """Stable fail-closed curriculum content error."""


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: pathlib.Path) -> str:
    return sha256_bytes(path.read_bytes())


def _pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in items:
        if key in result:
            raise ContentError("CURRICULUM_DUPLICATE_KEY")
        result[key] = value
    return result


def _walk(value: Any, depth: int = 0) -> None:
    if depth > MAX_DEPTH:
        raise ContentError("CURRICULUM_BOUNDS_INVALID")
    if isinstance(value, str):
        if len(value.encode()) > MAX_STRING_BYTES or unicodedata.normalize("NFC", value) != value:
            raise ContentError("CURRICULUM_BOUNDS_INVALID")
    elif isinstance(value, list):
        if len(value) > MAX_ARRAY_ITEMS:
            raise ContentError("CURRICULUM_BOUNDS_INVALID")
        for item in value:
            _walk(item, depth + 1)
    elif isinstance(value, dict):
        for key, item in value.items():
            _walk(key, depth + 1)
            _walk(item, depth + 1)
    elif isinstance(value, float):
        if not math.isfinite(value):
            raise ContentError("CURRICULUM_NUMBER_INVALID")
    elif isinstance(value, int) and not isinstance(value, bool) and abs(value) > MAX_SAFE_INTEGER:
        raise ContentError("CURRICULUM_NUMBER_INVALID")


def load_json(path: pathlib.Path) -> Any:
    try:
        info = path.lstat()
    except OSError as exc:
        raise ContentError("CURRICULUM_FILE_INVALID") from exc
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or info.st_nlink != 1:
        raise ContentError("CURRICULUM_FILE_INVALID")
    if stat.S_IMODE(info.st_mode) != 0o644 or info.st_size > MAX_JSON_BYTES:
        raise ContentError("CURRICULUM_BOUNDS_INVALID")
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise ContentError("CURRICULUM_ENCODING_INVALID")
    try:
        text = raw.decode("utf-8")
        if unicodedata.normalize("NFC", text) != text:
            raise ContentError("CURRICULUM_ENCODING_INVALID")
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_constant=lambda _value: (_ for _ in ()).throw(ContentError("CURRICULUM_NUMBER_INVALID")),
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContentError("CURRICULUM_JSON_INVALID") from exc
    _walk(value)
    return value


def git_identity(root: pathlib.Path = ROOT) -> tuple[str, str]:
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    tree = subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=root, text=True).strip()
    return head, tree


def verify_evidence(directory: pathlib.Path) -> dict[str, Any]:
    try:
        info = directory.lstat()
    except OSError as exc:
        raise ContentError("EVIDENCE_INDEX_INVALID") from exc
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise ContentError("EVIDENCE_INDEX_INVALID")
    def evidence_json(path: pathlib.Path) -> Any:
        item_info = path.lstat()
        if not stat.S_ISREG(item_info.st_mode) or stat.S_ISLNK(item_info.st_mode) or item_info.st_nlink != 1 or stat.S_IMODE(item_info.st_mode) != 0o600 or item_info.st_size > MAX_JSON_BYTES:
            raise ContentError("EVIDENCE_INDEX_INVALID")
        raw_value = path.read_bytes()
        if b"\r" in raw_value or not raw_value.endswith(b"\n"):
            raise ContentError("EVIDENCE_INDEX_INVALID")
        try:
            parsed = json.loads(raw_value, object_pairs_hook=_pairs, parse_constant=lambda _value: (_ for _ in ()).throw(ContentError("EVIDENCE_INDEX_INVALID")))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ContentError("EVIDENCE_INDEX_INVALID") from exc
        _walk(parsed)
        return parsed

    index = evidence_json(directory / "index.json")
    if set(index) != {"schemaVersion", "closed", "selfHashPolicy", "entries"}:
        raise ContentError("EVIDENCE_INDEX_INVALID")
    if index["schemaVersion"] != "architecture-evidence-index-v1" or index["closed"] is not True:
        raise ContentError("EVIDENCE_INDEX_INVALID")
    if index["selfHashPolicy"] != "index-excluded-to-avoid-recursion":
        raise ContentError("EVIDENCE_INDEX_INVALID")
    locators = [row.get("locator") for row in index["entries"]]
    if len(locators) != len(set(locators)) or any(not isinstance(item, str) or "/" in item or item in {"", ".", "..", "index.json"} for item in locators):
        raise ContentError("EVIDENCE_INDEX_INVALID")
    actual = {item.name for item in directory.iterdir() if item.is_file() and item.name != "index.json"}
    if actual != set(locators):
        raise ContentError("EVIDENCE_INDEX_INVALID")
    for row in index["entries"]:
        if set(row) != {"locator", "mediaType", "bytes", "sha256"}:
            raise ContentError("EVIDENCE_INDEX_INVALID")
        item = directory / row["locator"]
        raw = item.read_bytes()
        if len(raw) != row["bytes"] or sha256_bytes(raw) != row["sha256"]:
            raise ContentError("EVIDENCE_INDEX_INVALID")
        if PRIVATE_PATH.search(raw.decode("utf-8", "replace")):
            raise ContentError("EVIDENCE_INDEX_INVALID")
    return {"entryCount": len(locators), "closed": True}


def emit_evidence(command: str, projection: dict[str, Any], started_at: datetime.datetime, started: float) -> pathlib.Path:
    sys.path.insert(0, str(ROOT / "scripts/golden"))
    import fitness
    import workspace

    head, tree = git_identity()
    run_id = hashlib.sha256(f"{command}:{head}:{time.time_ns()}".encode()).hexdigest()[:32]
    owner = workspace.allocate_family(("evidence", command), command, run_id)
    directory = owner.path
    try:
        marker = json.loads((directory / ".golden-owner.json").read_text())
        marker_public = {key: marker[key] for key in ("schemaVersion", "runId", "purpose")}
        (directory / "owner.json").write_bytes(canonical_bytes(marker_public))
        inventory = {
            "schemaVersion": "architecture-run-inventory-v1",
            "inputSha": "c07c9a080be7be88447aac497bdf0a2b5fddd020",
            "testOnlyHead": "9ecd8069791446c4a35a392773ed7cac525a2ec3",
            "implementationHead": head,
            "testedTreeSha": tree,
            "releasedStageASha": "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9",
            "contractSetSha256": "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638",
            "pythonLockSha256": "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2",
            "protectedIdentityCount": 33,
            "moduleCount": projection.get("moduleCount"),
            "templateCount": projection.get("templateCount"),
            "traceNodeCount": projection.get("nodeCount"),
            "traceEdgeCount": projection.get("edgeCount"),
            "viewCount": projection.get("viewCount"),
            "stage": "A-static-only",
            "stageB": "blocked-on-issue10",
            "cloudAction": "none",
        }
        projection_record = {"schemaVersion": "architecture-curriculum-projection-v1", "commandId": command, "projection": projection}
        duration_ms = round((time.monotonic() - started) * 1000)
        resources_record = {
            "schemaVersion": "architecture-resource-measurement-v1",
            "durationMs": duration_ms,
            "maxRssBytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            "stdoutLimitBytes": 1024 * 1024,
            "evidenceLimitBytes": 4 * 1024 * 1024,
        }
        for name, value in (
            ("inventory.json", inventory),
            ("projection.json", projection_record),
            ("resources.json", resources_record),
        ):
            (directory / name).write_bytes(canonical_bytes(value))
        projection_sha = sha256_file(directory / "projection.json")
        result = fitness.passed(
            command_id=command,
            tested_tree_sha=tree,
            projection_sha256=projection_sha,
            started_at=started_at,
            duration_ms=duration_ms,
            toolchain={"python": "3.12", "jsonschema": "4.26.0", "pyyaml": "6.0.3"},
            locators={"projection": "projection.json"},
            artifacts=[{"locator": "projection.json", "sha256": projection_sha}],
        )
        result["owner"] = "I5-06"
        result["inputGitSha"] = inventory["inputSha"]
        result["testOnlyHead"] = inventory["testOnlyHead"]
        result["stage"] = inventory["stage"]
        result["cloudAction"] = "none"
        result["cleanupRollback"] = "controller-gate-pending"
        (directory / "result.json").write_bytes(canonical_bytes(result))
        entries = []
        for item in sorted(directory.iterdir()):
            if item.name == "index.json":
                continue
            raw = item.read_bytes()
            entries.append({"locator": item.name, "mediaType": "application/json", "bytes": len(raw), "sha256": sha256_bytes(raw)})
            os.chmod(item, 0o600)
        index = {
            "schemaVersion": "architecture-evidence-index-v1",
            "closed": True,
            "selfHashPolicy": "index-excluded-to-avoid-recursion",
            "entries": entries,
        }
        (directory / "index.json").write_bytes(canonical_bytes(index))
        os.chmod(directory / "index.json", 0o600)
        verify_evidence(directory)
        owner.close()
        return directory.relative_to(ROOT)
    finally:
        owner.close()


def launch_admitted(command: str) -> int:
    """Run a fixed curriculum command with the sole released admitted runtime."""
    from scripts.learning_contracts import LearningContractError
    from scripts.learning_contracts import runtime

    modules = {
        "curriculum": "learning.curriculum.tools.check_curriculum",
        "traceability": "learning.curriculum.tools.check_traceability",
    }
    if command not in modules:
        raise ContentError("CURRICULUM_COMMAND_INVALID")
    runtime_root = ROOT / ".artifacts/workspaces/golden"
    markers = runtime._admission_markers(runtime_root)
    if len(markers) != 1:
        raise ContentError("RUNTIME_ADMISSION_COUNT")
    marker = load_json_evidence_marker(markers[0])
    interpreter_hash = marker.get("interpreterSha256")
    if not isinstance(interpreter_hash, str):
        raise ContentError("RUNTIME_ADMISSION_MISMATCH")
    expected = runtime.expected_runtime_identity(interpreter_hash)
    interpreter = runtime.select_admitted_runtime(runtime_root, expected)
    try:
        output = runtime.run_bounded(
            [str(interpreter), "-m", modules[command]],
            cwd=ROOT,
            timeout=60,
            output_limit=1024 * 1024,
            max_rss_bytes=512 * 1024 * 1024,
        )
    except LearningContractError as exc:
        raise ContentError(exc.code) from exc
    os.write(sys.stdout.fileno(), output)
    return 0


def load_json_evidence_marker(path: pathlib.Path) -> dict[str, Any]:
    try:
        info = path.lstat()
        raw = path.read_bytes()
    except OSError as exc:
        raise ContentError("RUNTIME_ADMISSION_MISMATCH") from exc
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) or info.st_nlink != 1 or stat.S_IMODE(info.st_mode) != 0o600 or len(raw) > MAX_JSON_BYTES:
        raise ContentError("RUNTIME_ADMISSION_MISMATCH")
    try:
        value = json.loads(raw, object_pairs_hook=_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ContentError("RUNTIME_ADMISSION_MISMATCH") from exc
    if not isinstance(value, dict):
        raise ContentError("RUNTIME_ADMISSION_MISMATCH")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=("launch",))
    parser.add_argument("command", choices=("curriculum", "traceability"))
    args = parser.parse_args(argv)
    try:
        return launch_admitted(args.command)
    except (ContentError, OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
