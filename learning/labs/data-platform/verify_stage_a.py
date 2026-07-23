#!/usr/bin/env python3
"""Bounded, read-only verification for Issue #12 Stage A lab candidates."""
from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from typing import Any

from jsonschema import Draft202012Validator


ROOT = pathlib.Path(__file__).resolve().parents[3]
LAB_ROOT = ROOT / "learning/labs/data-platform"
ISSUE_6_SHA = "24be3b34c6b0fcdbd07c5800dcab349054e34713"
ISSUE_8_SHA = "5644f01b4c0443a81f3af0bcce80f44c847cd986"
LAB_IDS = ("deterministic-ingest", "model-quality", "weighted-metrics")

AUTHORITY_HASHES = {
    "learning/contracts/lab-v1.schema.json": "891c41100a28548e603ca1714aeaf5be2d541cd1780ab2ef72e3ef0740c6c16d",
    "learning/contracts/learning-evidence-v1.schema.json": "52a68529b72ecb7f24c59ebe52e16e4ee5f21660164b1d20570827b18be3fe47",
    "learning/contracts/completion-reconciliation-v1.json": "8fd50ced7a068c81f9868c23842ce680a46aba94a211bb932afef2beecc2d9ff",
    "learning/contracts/fitness-result-v2.schema.json": "d53f9b7b68b9f313bf0b9259fe5042bfb8cdbca0001570c18cd937de4971d6c6",
    "learning/contracts/command-owner-activation-v1.schema.json": "8fe337b7646fddc2dff4d1fc30e4a9120d0edec3f7eb293e8ead0e5d82f7a1f0",
    "learning/contracts/command-owner-registry-v1.json": "a94ac86bda0b70643edef9f144a59d8753d91f963b83d22cd510adbc31970e80",
    "learning/contracts/learning-contract-version-registry-v1.json": "a34c907e8870e89a182a180250a284f1a3c2ab3b6f1c4217c087cbc57775f9cb",
    "learning/contracts/learning-contract-set-v1.json": "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638",
    "learning/contracts/operation-matrix-v1.json": "ffabcc11ca3943e3e520cd7b98c535032be439b1e2d1b920fe9ee17806180b1e",
    "mk/issue-5/i5-03.mk": "566acfb4956eafca4d91cf5efdc7f4205198a60cc5b988249975a614ff742576",
}

PROTECTED_HASHES = {
    "Makefile": "12926b16a797fded79b0b11b00147887258721f145c79e66472f44c5f0228458",
    "release-manifest.json": "f9037b5d946d14f7b1b9c020939f1a44961011f2ad933db9f2b69054abbf9539",
    "contracts/data/retail-golden-v1.json": "f303282e3b524e1273e702c9b8b24b500aaa01afdd3c3b623ac997afba8840cc",
    "contracts/data/promotion-trust-v1.yaml": "c30e1938aae6eeffa2adf0c0b3bdee15f7f877d769cce09e171d43dc2f153cfe",
    "contracts/data/curated-release-manifest.schema.json": "dcad3a4c04f44e207a26f985702db6926d4c85545d85ef5481faf036dded4e33",
    "tests/fixtures/learning/promotion-trust/evidence-v1.json": "2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5",
    "tests/fixtures/learning/promotion-trust/manifest.json": "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341",
}

PROTECTED_OBJECTS = {
    "Makefile": "e1a4332a9645ccbd37bec4be1f70372241e16b7b",
    "release-manifest.json": "b27d231c5ee6d48fd7932b06807ef6a9a2220e21",
    "learning/contracts": "042d88ccf9cafe2c7f746e725f1cd34a158f14f2",
    "contracts/data": "ed56fef97ce114250b37a68e092bc1b26d708921",
    "tests/fixtures/learning/promotion-trust": "7b2389765373f09971784f6b3f0b6569dc16d08f",
    "architecture": "cd020fce1d525dd6fe414d5db28748911b7cf300",
    "transform/dbt": "28932692fc20e079eecbe7ab1c9f93b2a94a8bbf",
    "serving/rill": "27bda8a14222cae083d480275453659adb85b3ff",
    "lake/curated_assets.json": "fc4b04aca3d4941d06658f27c58d078299301200",
    "lake/publish_iceberg.py": "f929090963f94e0847231558271d176f3c8b714c",
    "governance/openmetadata": "47583e22c4702f0de0608482c60649e99cc7e6d4",
    "orchestration/airflow": "1cff31770c4d98b7591b1d077064194b7b902675",
}

REQUIRED_HEADINGS = (
    "## Trạng thái",
    "## Điều kiện tiên quyết",
    "## Bộ khởi đầu",
    "## Nhiệm vụ",
    "## Lỗi có kiểm soát",
    "## Gợi ý 1",
    "## Gợi ý 2",
    "## Gợi ý 3",
    "## Xác minh",
    "## Evidence bất biến",
    "## Reset",
    "## Lời giải có khóa",
    "## Liên kết khắc phục",
    "## Phản tư đánh đổi",
)


class StageAError(RuntimeError):
    """Stable failure code for Stage A checks."""


def fail(code: str) -> None:
    raise StageAError(code)


def sha256(path: pathlib.Path) -> str:
    if not path.is_file() or path.is_symlink():
        fail("UNSAFE_OR_MISSING_FILE")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: pathlib.Path) -> dict[str, Any]:
    if not path.is_file() or path.is_symlink():
        fail("UNSAFE_OR_MISSING_FILE")
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise StageAError("JSON_INVALID") from exc
    if not isinstance(value, dict):
        fail("JSON_OBJECT_REQUIRED")
    return value


def read_text(path: pathlib.Path) -> str:
    if not path.is_file() or path.is_symlink():
        fail("UNSAFE_OR_MISSING_FILE")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise StageAError("TEXT_INVALID") from exc


def verify_hashes(root: pathlib.Path, expected: dict[str, str], code: str) -> None:
    for relative, digest in expected.items():
        if sha256(root / relative) != digest:
            fail(code)


def git_output(root: pathlib.Path, *arguments: str) -> str:
    try:
        result = subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise StageAError("GIT_IDENTITY_INVALID") from exc
    return result.stdout.strip()


def verify_git_authority(root: pathlib.Path) -> None:
    for dependency in (ISSUE_6_SHA, ISSUE_8_SHA):
        try:
            subprocess.run(
                ["git", "merge-base", "--is-ancestor", dependency, "HEAD"],
                cwd=root,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, subprocess.CalledProcessError) as exc:
            raise StageAError("DEPENDENCY_ANCESTRY_INVALID") from exc
    for relative, expected in PROTECTED_OBJECTS.items():
        if git_output(root, "rev-parse", f"HEAD:{relative}") != expected:
            fail("PROTECTED_GIT_OBJECT_DRIFT")
    protected = tuple(PROTECTED_OBJECTS)
    status = git_output(root, "status", "--porcelain", "--untracked-files=all", "--", *protected)
    if status:
        fail("PROTECTED_WORKTREE_DRIFT")


def validate_schema(instance: dict[str, Any], schema_path: pathlib.Path, code: str) -> None:
    schema = read_json(schema_path)
    errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda item: list(item.path))
    if errors:
        fail(code)


def verify_released_registry(root: pathlib.Path) -> None:
    registry = read_json(root / "learning/contracts/learning-contract-version-registry-v1.json")
    lab = next((item for item in registry.get("ownedFamilies", []) if item.get("family") == "lab"), None)
    activation = next(
        (item for item in registry.get("ownedFamilies", []) if item.get("family") == "command-owner-activation"),
        None,
    )
    extensions = registry.get("familyExtensions", [])
    fitness = next((item for item in extensions if item.get("family") == "fitness-result"), None)
    if (
        not lab
        or lab.get("currentVersion") != "lab-v1"
        or lab.get("schema", {}).get("sha256") != AUTHORITY_HASHES["learning/contracts/lab-v1.schema.json"]
        or not activation
        or activation.get("currentVersion") != "command-owner-activation-v1"
        or not fitness
        or "fitness-result-v2"
        not in {item.get("version") for item in fitness.get("addedReadableVersions", [])}
    ):
        fail("RELEASED_CONTRACT_REGISTRY_DRIFT")


def verify_descriptor(lab_id: str, value: dict[str, Any], root: pathlib.Path = ROOT) -> None:
    validate_schema(value, root / "learning/contracts/lab-v1.schema.json", "LAB_SCHEMA_INVALID")
    if value.get("id") != f"data-platform-{lab_id}-v1":
        fail("LAB_CONTENT_PAIR_MISMATCH")
    if value.get("profile") != {"id": "small", "seed": 42}:
        fail("LAB_PROFILE_DRIFT")
    if value.get("risk") != {
        "class": "bounded-local",
        "network": "denied",
        "privilege": "unprivileged",
    }:
        fail("LAB_RISK_BOUNDARY_INVALID")
    transitions = [(item.get("from"), item.get("to")) for item in value["stateMachine"]["transitions"]]
    expected = [
        ("not-started", "preparing"),
        ("preparing", "ready"),
        ("ready", "running"),
        ("running", "verified"),
        ("verified", "evidenced"),
        ("evidenced", "completed"),
    ]
    if transitions != expected:
        fail("LAB_LIFECYCLE_MISSING")
    if not all(item.get("id", "").startswith("candidate.") for item in value["commands"]):
        fail("RUNNER_AUTHORITY_FORBIDDEN")
    if value["reset"] != {
        "scope": "workspace",
        "atomic": True,
        "preserveProgress": True,
        "preserveEvidence": True,
        "postResetState": "ready",
    }:
        fail("LAB_RESET_INVALID")
    if value["solution"].get("revealAfterHints") != 3 or not value["solution"].get("separateFromStarter"):
        fail("LAB_SOLUTION_GATE_INVALID")
    evidence_metadata = set(value["evidence"].get("requiredMetadata", []))
    if not {"operationId", "contractHashes", "fixtureHashes", "expectedActual"} <= evidence_metadata:
        fail("LAB_EVIDENCE_METADATA_MISSING")
    failure_codes = set(value["controlledFailure"]["expectedEvidence"])
    remediation_codes = {item["failureCode"] for item in value["remediation"]}
    assertion_codes = {item["failureCode"] for item in value["verify"]["assertions"]}
    if not failure_codes <= remediation_codes or assertion_codes != remediation_codes:
        fail("LAB_REMEDIATION_MISSING")


def scan_untrusted_text(text: str) -> None:
    checks = {
        "UNSAFE_PATH_CONTENT": (r"(?:^|[\s`'\"])(?:/Users/|/home/|/tmp/|file://|\.\./)",),
        "UNSAFE_LINK_CONTENT": (r"https?://", r"\[[^\]]+\]\((?!#[^)]+\))"),
        "BROAD_MUTATION_CONTENT": (
            r"\brm\s+-rf\b",
            r"\bgit\s+clean\b",
            r"\bgit\s+reset\s+--hard\b",
            r"\bfind\s+\.\s+.*-delete\b",
        ),
        "PRIVATE_OR_SECRET_CONTENT": (
            r"\bAKIA[0-9A-Z]{16}\b",
            r"\bgh[pousr]_[A-Za-z0-9]{20,}\b",
            r"\b(?:password|token|secret)\s*[:=]\s*\S+",
            r"\b(?:BEGIN\s+(?:RSA|OPENSSH|EC)\s+PRIVATE\s+KEY)\b",
        ),
    }
    for code, patterns in checks.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE | re.MULTILINE) for pattern in patterns):
            fail(code)


def verify_content(lab_id: str, text: str) -> None:
    scan_untrusted_text(text)
    if any(heading not in text for heading in REQUIRED_HEADINGS):
        fail("LAB_LIFECYCLE_MISSING")
    if text.count("candidate-not-runnable") != 1:
        fail("RUNNABLE_COMPLETION_CLAIM")
    if not all(marker in text for marker in ("**Hành động:**", "**Kỳ vọng:**", "**Thực tế:**")):
        fail("EXPECTED_ACTUAL_MISSING")
    if text.index("## Lời giải có khóa") < text.index("## Gợi ý 3"):
        fail("LAB_SOLUTION_GATE_INVALID")
    required = {
        "deterministic-ingest": (
            "small",
            "42",
            "18 CSV",
            "6.812",
            "60ce82ce297acec1e3c047466f4b068baed5dc1875964832cb6cda3d4f91e9d6",
            "GOLDEN_INPUT_MISMATCH",
            "workspace-only",
        ),
        "model-quality": (
            "source -> staging -> intermediate -> core -> mart",
            "51 model",
            "141 generic test",
            "179 pass",
            "7 warn",
            "0 fail",
            "Chín test",
            "QUALITY_SEVERITY_DRIFT",
        ),
        "weighted-metrics": (
            "(carrier, region_name)",
            "25 dòng",
            "shipment_count - in_transit_count",
            "tổng weight là 800",
            "5.456625",
            "5.34",
            "AVERAGE_OF_AVERAGES_INVALID",
            "AVG(avg_order_value)",
        ),
    }
    if any(marker not in text for marker in required[lab_id]):
        code = "METRIC_GRAIN_OR_AVERAGE_INVALID" if lab_id == "weighted-metrics" else "LAB_SEMANTIC_ANCHOR_MISSING"
        fail(code)


def verify_activation(value: dict[str, Any], root: pathlib.Path = ROOT) -> None:
    validate_schema(
        value,
        root / "learning/contracts/command-owner-activation-v1.schema.json",
        "ACTIVATION_SCHEMA_INVALID",
    )
    expected = {
        "commandId": "lake-contracts-check",
        "availability": "implemented-static-contract",
        "evidenceVersion": "fitness-result-v2",
    }
    if (
        value.get("baseRegistryPath") != "learning/contracts/command-owner-registry-v1.json"
        or value.get("baseRegistrySha256")
        != AUTHORITY_HASHES["learning/contracts/command-owner-registry-v1.json"]
        or value.get("owner") != "I5-07"
        or value.get("fragment", {}).get("path") != "mk/issue-5/i5-07.mk"
        or value.get("fragment", {}).get("sha256") != sha256(root / "mk/issue-5/i5-07.mk")
        or value.get("commands") != [expected]
    ):
        fail("ACTIVATION_SCOPE_INVALID")


def verify_make_fragment(root: pathlib.Path = ROOT) -> None:
    text = read_text(root / "mk/issue-5/i5-07.mk")
    if text.count("lake-contracts-check:") != 1:
        fail("MAKE_TARGET_INVALID")
    forbidden = ("data-labs-e2e", "lake-fault-test", "metadata-contracts-check", "metadata-reconcile-test")
    if any(item in text for item in forbidden):
        fail("ACTIVATION_SCOPE_INVALID")
    if "verify_stage_a.py check" not in text or "env -u PYTHONPATH" not in text:
        fail("MAKE_TARGET_INVALID")


def weighted_projection(root: pathlib.Path = ROOT) -> tuple[Decimal, Decimal, int]:
    fixture = read_json(root / "tests/fixtures/learning/promotion-trust/evidence-v1.json")
    source = next(
        (item for item in fixture.get("sources", []) if item.get("sourceId") == "mart_fulfillment_performance"),
        None,
    )
    if (
        not source
        or source.get("grain") != ["carrier", "region_name"]
        or source.get("rowCount") != 25
        or source.get("sourceMartContentSha256")
        != "8c0114d1ab48b4fb42009aba3df192988bf917004461d0c0dd0155d0283dce60"
    ):
        fail("METRIC_GRAIN_OR_AVERAGE_INVALID")
    rows = source["records"]
    weights = [row["shipment_count"] - row["in_transit_count"] for row in rows]
    weighted = sum(Decimal(row["avg_lead_time_days"]) * weight for row, weight in zip(rows, weights))
    weighted /= sum(weights)
    invalid = sum(Decimal(row["avg_lead_time_days"]) for row in rows) / len(rows)
    if (weighted, invalid, sum(weights)) != (Decimal("5.456625"), Decimal("5.34"), 800):
        fail("METRIC_GRAIN_OR_AVERAGE_INVALID")
    fulfillment = read_text(root / "serving/rill/metrics/fulfillment_performance_metrics.yaml")
    daily = read_text(root / "serving/rill/metrics/daily_revenue_metrics.yaml")
    if (
        "SUM(avg_lead_time_days * (shipment_count - in_transit_count))" not in fulfillment
        or "AVG(avg_order_value)" not in daily
    ):
        fail("METRIC_SEMANTIC_DRIFT")
    return weighted, invalid, sum(weights)


def verify_run_owned_reset() -> None:
    with tempfile.TemporaryDirectory(prefix="stage-a-owned-") as parent_name:
        parent = pathlib.Path(parent_name)
        foreign = parent / "foreign-sentinel"
        foreign.write_text("preserve", encoding="utf-8")
        run = parent / "run-001"
        run.mkdir(mode=0o700)
        marker = run / ".stage-a-owner.json"
        marker.write_text('{"runId":"run-001","owner":"I5-07"}\n', encoding="utf-8")
        evidence = run / "evidence"
        evidence.mkdir(mode=0o700)
        (evidence / "result.json").write_text(
            '{"assertionId":"DL-EVD-001","expected":"pass","actual":"pass"}\n',
            encoding="utf-8",
        )
        marker_value = read_json(marker)
        if marker_value != {"runId": "run-001", "owner": "I5-07"}:
            fail("RUN_OWNERSHIP_INVALID")
        shutil.rmtree(run)
        if run.exists() or foreign.read_text(encoding="utf-8") != "preserve":
            fail("RESET_SCOPE_INVALID")


def verify_repository(root: pathlib.Path = ROOT) -> dict[str, Any]:
    verify_git_authority(root)
    verify_hashes(root, AUTHORITY_HASHES, "RELEASED_AUTHORITY_DRIFT")
    verify_hashes(root, PROTECTED_HASHES, "PROTECTED_GOLDEN_DRIFT")
    if (root / "docs/code-standards.md").exists():
        fail("PROTECTED_ABSENCE_DRIFT")
    verify_released_registry(root)
    schema = root / "learning/contracts/lab-v1.schema.json"
    if sha256(schema) != AUTHORITY_HASHES["learning/contracts/lab-v1.schema.json"]:
        fail("RELEASED_AUTHORITY_DRIFT")
    for lab_id in LAB_IDS:
        descriptor_path = root / f"learning/labs/data-platform/{lab_id}/lab-v1.json"
        content_path = root / f"learning/labs/data-platform/{lab_id}/content.vi.md"
        descriptor = read_json(descriptor_path)
        verify_descriptor(lab_id, descriptor, root)
        verify_content(lab_id, read_text(content_path))
    activation = read_json(root / "learning/labs/data-platform/command-owner-activation.stage-a.json")
    verify_activation(activation, root)
    verify_make_fragment(root)
    weighted, invalid, weight = weighted_projection(root)
    verify_run_owned_reset()
    return {
        "status": "pass",
        "claim": "candidate-not-runnable",
        "labs": len(LAB_IDS),
        "dependencies": [ISSUE_6_SHA, ISSUE_8_SHA],
        "weighted": str(weighted),
        "invalidAverage": str(invalid),
        "weight": weight,
    }


def expect_failure(code: str, action: Any) -> None:
    try:
        action()
    except StageAError as exc:
        if str(exc) != code:
            raise StageAError(f"SELF_TEST_EXPECTED_{code}_GOT_{exc}") from exc
    else:
        fail(f"SELF_TEST_DID_NOT_FAIL_{code}")


def self_test(root: pathlib.Path = ROOT) -> dict[str, Any]:
    ingest = read_text(root / "learning/labs/data-platform/deterministic-ingest/content.vi.md")
    model = read_text(root / "learning/labs/data-platform/model-quality/content.vi.md")
    metric = read_text(root / "learning/labs/data-platform/weighted-metrics/content.vi.md")
    descriptor = read_json(root / "learning/labs/data-platform/deterministic-ingest/lab-v1.json")
    activation = read_json(root / "learning/labs/data-platform/command-owner-activation.stage-a.json")
    cases: list[tuple[str, Any]] = [
        (
            "LAB_LIFECYCLE_MISSING",
            lambda: verify_content("deterministic-ingest", ingest.replace("## Reset", "## Khôi phục")),
        ),
        (
            "LAB_SEMANTIC_ANCHOR_MISSING",
            lambda: verify_content("model-quality", model.replace("179 pass", "178 pass")),
        ),
        (
            "METRIC_GRAIN_OR_AVERAGE_INVALID",
            lambda: verify_content("weighted-metrics", metric.replace("(carrier, region_name)", "(order_id)")),
        ),
        (
            "METRIC_GRAIN_OR_AVERAGE_INVALID",
            lambda: verify_content("weighted-metrics", metric.replace("5.456625", "5.34")),
        ),
        ("BROAD_MUTATION_CONTENT", lambda: verify_content("deterministic-ingest", ingest + "\nrm -rf workspace\n")),
        ("UNSAFE_PATH_CONTENT", lambda: verify_content("deterministic-ingest", ingest + "\n`/Users/example/evidence`\n")),
        ("UNSAFE_LINK_CONTENT", lambda: verify_content("deterministic-ingest", ingest + "\n[x](https://private.example)\n")),
        (
            "PRIVATE_OR_SECRET_CONTENT",
            lambda: verify_content("deterministic-ingest", ingest + "\n" + "gh" + "p_" + "x" * 30 + "\n"),
        ),
    ]
    missing_transition = copy.deepcopy(descriptor)
    missing_transition["stateMachine"]["transitions"].pop()
    cases.append(
        ("LAB_LIFECYCLE_MISSING", lambda: verify_descriptor("deterministic-ingest", missing_transition, root))
    )
    unsafe_descriptor = copy.deepcopy(descriptor)
    unsafe_descriptor["workspace"]["allowedPaths"] = ["../golden"]
    cases.append(("LAB_SCHEMA_INVALID", lambda: verify_descriptor("deterministic-ingest", unsafe_descriptor, root)))
    broad_activation = copy.deepcopy(activation)
    broad_activation["commands"].append(
        {
            "commandId": "lake-fault-test",
            "availability": "implemented",
            "evidenceVersion": "fitness-result-v2",
        }
    )
    cases.append(("ACTIVATION_SCOPE_INVALID", lambda: verify_activation(broad_activation, root)))
    with tempfile.TemporaryDirectory(prefix="stage-a-drift-") as drift_name:
        drift_root = pathlib.Path(drift_name)
        (drift_root / "authority.txt").write_text("drift", encoding="utf-8")
        expect_failure(
            "RELEASED_AUTHORITY_DRIFT",
            lambda: verify_hashes(
                drift_root,
                {"authority.txt": hashlib.sha256(b"released").hexdigest()},
                "RELEASED_AUTHORITY_DRIFT",
            ),
        )
    for code, action in cases:
        expect_failure(code, action)
    verify_run_owned_reset()
    return {"status": "pass", "negativeCases": len(cases) + 1, "cleanup": "pass"}


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"check", "self-test"}:
        print("usage: verify_stage_a.py {check|self-test}", file=sys.stderr)
        return 2
    try:
        result = verify_repository() if argv[1] == "check" else self_test()
    except StageAError as exc:
        print(f"stage-a: fail code={exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
