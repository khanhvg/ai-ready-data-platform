"""Immutable released-contract admission."""
from __future__ import annotations
import hashlib, json, pathlib, subprocess
from typing import Any

STAGE_A_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
STAGE_A_TREE = "27fc3667ef37892dad5c3fbfd76769f65a0760be"
EXPECTED_COMMANDS = (
    "workspace.prepare", "retail.generate", "retail.load", "retail.dbt-build",
    "retail.export", "promotion.configure", "promotion.verify", "workspace.reset",
)


class ContractError(RuntimeError):
    pass


def _json(raw: bytes) -> Any:
    return json.loads(raw.decode("utf-8", "strict"))


def released_blob(root: pathlib.Path, path: str) -> bytes:
    try:
        return subprocess.run(
            ["git", "show", f"{STAGE_A_SHA}:{path}"], cwd=root, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            env={"PATH": "/usr/bin:/bin:/usr/local/bin"},
        ).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise ContractError("RUNNER_DEPENDENCY_NOT_RELEASED") from exc


def validate_released_contract(root: pathlib.Path, lock_path: pathlib.Path) -> dict[str, Any]:
    lock = _json(lock_path.read_bytes())
    if lock.get("releaseSha") != STAGE_A_SHA or lock.get("releaseTree") != STAGE_A_TREE:
        raise ContractError("RUNNER_DEPENDENCY_NOT_RELEASED")
    seen: set[str] = set()
    for row in lock.get("pins", []):
        path, expected = row.get("path"), row.get("sha256")
        if not isinstance(path, str) or path in seen or not isinstance(expected, str):
            raise ContractError("RUNNER_CONTRACT_LOCK_INVALID")
        seen.add(path)
        if hashlib.sha256(released_blob(root, path)).hexdigest() != expected:
            raise ContractError("RUNNER_CONTRACT_HASH_MISMATCH")
    if len(seen) != 38:
        raise ContractError("RUNNER_CONTRACT_LOCK_INVALID")
    lab = _json(released_blob(root, "learning/labs/promotion-trust/lab-v1.json"))
    commands = tuple(row["id"] for row in lab["commands"])
    if commands != EXPECTED_COMMANDS:
        raise ContractError("RUNNER_OPERATION_MATRIX_MISMATCH")
    for row in lab["commands"]:
        if row != {"id": row["id"], "arguments": [], "timeoutSeconds": 120, "memoryBytes": 536870912, "network": "denied"}:
            raise ContractError("RUNNER_OPERATION_MATRIX_MISMATCH")
    if lab["profile"] != {"id": "small-42", "seed": 42} or lab["workspace"]["quotaBytes"] != 268435456:
        raise ContractError("RUNNER_OPERATION_MATRIX_MISMATCH")
    return lab
