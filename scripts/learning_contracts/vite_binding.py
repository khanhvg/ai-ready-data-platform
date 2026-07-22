"""Read-only validation for the promotion-trust Vite identifier binding."""

from __future__ import annotations

import pathlib
import re
from typing import Any

from . import LearningContractError
from .canonical import parse_json
from .references import resolve_reference
from .schema import ROOT, read_document, validate_document


BINDING_PATH = ROOT / "learning/bindings/vite/promotion-trust-v1.json"
BINDING_SCHEMA_PATH = ROOT / "learning/contracts/promotion-trust-vite-binding-v1.schema.json"

_EXPECTED_RELEASE_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
_EXPECTED_ISSUE_7_SHA = "1806b6d515f2f7a2ace2be7077af84a745ff221f"
_EXPECTED_REFERENCES = {
    ("stageA", "contractSet"): (
        "learning/contracts/learning-contract-set-v1.json",
        "92aaf9a573f5d23b5bf5d8d7db1e68150d4b0944f0e6ab6e651b1a3d34408638",
    ),
    ("stageA", "promotionManifest"): (
        "learning/manifests/promotion-trust-v1.json",
        "553b97ed5dc44b77564ae50b1a2211205cbd1a759f3578e5e4dfcefef99044ac",
    ),
    ("issue7", "adr"): (
        "docs/decisions/0005-web-stack.md",
        "6e26c48a027d226d8529fda939c07cca99e9f4e1d88cac12708deb98d6fe5eee",
    ),
    ("issue7", "package"): (
        "spikes/web/candidates/vite/package.json",
        "c80eab653ba83702e37dc41d19f18408714863bbb4c5e4d5d7e2da66a7f1b871",
    ),
    ("issue7", "lock"): (
        "spikes/web/candidates/vite/package-lock.json",
        "96feead881be424d4c0d8d4629d7da0312722a3d7c945d08ed071542ea5d443c",
    ),
    ("issue7", "lessonContract"): (
        "spikes/web/candidates/vite/src/lesson-contract.mjs",
        "32b19a5f2e25bd805f340917071c7935a70ae27397b366ca34f1a89054fc35d9",
    ),
    ("fixture", "evidence"): (
        "tests/fixtures/learning/promotion-trust/evidence-v1.json",
        "2f4d90228fa2ea8859a8db630ff587b6cebdc10a0bf6b7db25e46c3dc27181d5",
    ),
    ("fixture", "manifest"): (
        "tests/fixtures/learning/promotion-trust/manifest.json",
        "0a1dcd4023648f52009bfd4dc5d529c00ce66f42cd0e725732b972b0b78df341",
    ),
}
_EXPECTED_GRAINS = (
    ("promotion", "promotion"),
    ("fulfillment", "fulfillment"),
    ("returns", "returns"),
    ("dq", "data-quality"),
)
_EXPECTED_STAGE_A_KEYS = (
    ("promo_name", "channel"),
    ("carrier", "region"),
    ("reason", "category", "region"),
    ("scenario",),
)
_EXPECTED_VITE_KEYS = (
    ("promo_name", "channel"),
    ("carrier", "region_name"),
    ("reason", "category_name", "region_name"),
    ("scenario",),
)
_EXPECTED_TRUST_BOUNDARY = {
    "browserRole": "projection-only",
    "serverValidationAuthority": "stage-a-learning-contracts",
    "completionAuthority": "learning-progress-authority-v1",
    "authorize": False,
    "mutate": False,
    "validate": False,
    "complete": False,
    "emitEvidence": False,
}
_DATA_KEYS = frozenset({"data", "payload", "rawRecord", "rawRecords", "record", "records", "rows", "values"})
_FORK_KEYS = frozenset({
    "aggregation", "aggregations", "attribution", "default", "defaults", "join", "joins",
    "operations", "relationships", "schemaFields", "transform", "transforms",
})
_EXECUTABLE_KEYS = frozenset({
    "authPolicy", "command", "commands", "credential", "credentials", "expression", "template",
    "token", "uri", "url",
})


def _scan_forbidden(value: Any) -> None:
    if isinstance(value, dict):
        keys = set(value)
        if keys & _DATA_KEYS:
            raise LearningContractError("BINDING_DATA_PAYLOAD_FORBIDDEN")
        if keys & _FORK_KEYS:
            raise LearningContractError("BINDING_CONTRACT_FORK_FORBIDDEN")
        if keys & _EXECUTABLE_KEYS:
            raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
        for child in value.values():
            _scan_forbidden(child)
    elif isinstance(value, list):
        for child in value:
            _scan_forbidden(child)


def _is_safe_relative_path(value: object) -> bool:
    if not isinstance(value, str) or not value or len(value) > 256 or "\\" in value or "\x00" in value or ":" in value:
        return False
    parts = value.split("/")
    path = pathlib.PurePosixPath(value)
    return not path.is_absolute() and all(part not in {"", ".", ".."} for part in parts)


def _scan_reference_paths(value: Any) -> None:
    if isinstance(value, dict):
        if "path" in value and not _is_safe_relative_path(value["path"]):
            raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
        for child in value.values():
            _scan_reference_paths(child)
    elif isinstance(value, list):
        for child in value:
            _scan_reference_paths(child)


def _resolved_inputs(value: dict[str, Any], root: pathlib.Path) -> dict[tuple[str, str], bytes]:
    if value["stageA"]["releaseSha"] != _EXPECTED_RELEASE_SHA or value["issue7"]["mergeSha"] != _EXPECTED_ISSUE_7_SHA:
        raise LearningContractError("BINDING_DEPENDENCY_HASH_MISMATCH")
    resolved: dict[tuple[str, str], bytes] = {}
    for address, expected in _EXPECTED_REFERENCES.items():
        parent, name = address
        reference = value[parent][name]
        locator = reference["path"]
        declared_hash = reference["sha256"]
        if not _is_safe_relative_path(locator):
            raise LearningContractError("BINDING_REFERENCE_FORBIDDEN")
        if (locator, declared_hash) != expected:
            raise LearningContractError("BINDING_DEPENDENCY_HASH_MISMATCH")
        try:
            resolved[address] = resolve_reference(root, locator, declared_hash)
        except LearningContractError as exc:
            if exc.code in {"REFERENCE_PATH_INVALID", "REFERENCE_SPECIAL_FILE", "REFERENCE_UNREADABLE"}:
                raise LearningContractError("BINDING_REFERENCE_FORBIDDEN") from exc
            if exc.code == "REFERENCE_HASH_MISMATCH":
                raise LearningContractError("BINDING_DEPENDENCY_HASH_MISMATCH") from exc
            raise
    return resolved


def _vite_projection(source: bytes) -> tuple[tuple[str, tuple[str, ...]], ...]:
    try:
        text = source.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise LearningContractError("BINDING_VITE_SOURCE_INVALID") from exc
    rows = re.findall(r"id:\s*'([^']+)'\s*,\s*value:\s*'([^']+)'", text)
    projection = tuple((grain, tuple(key.strip() for key in keys.split("×"))) for grain, keys in rows)
    if len(projection) != 4:
        raise LearningContractError("BINDING_VITE_SOURCE_INVALID")
    return projection


def _has_alias_cycle(rows: list[dict[str, Any]]) -> bool:
    graph: dict[str, set[str]] = {}
    for row in rows:
        for alias in row.get("aliases", []):
            if isinstance(alias, dict) and alias.get("kind") == "identifier-alias":
                source, target = alias.get("from"), alias.get("to")
                if isinstance(source, str) and isinstance(target, str) and source != target:
                    graph.setdefault(source, set()).add(target)
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for child in graph.get(node, set()):
            if visit(child):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(visit(node) for node in graph)


def validate_vite_binding_document(value: Any, *, root: pathlib.Path = ROOT) -> dict[str, Any]:
    """Validate one binding without transforming or returning fixture records."""
    if not isinstance(value, dict):
        raise LearningContractError("BINDING_SCHEMA_INVALID")
    _scan_forbidden(value)
    _scan_reference_paths(value)
    if value.get("schemaVersion") != "promotion-trust-vite-binding-v1" or value.get("bindingId") != "promotion-trust-vite-binding-v1":
        raise LearningContractError("BINDING_VERSION_UNSUPPORTED")
    candidate_rows = value.get("grainBindings")
    if isinstance(candidate_rows, list) and len(candidate_rows) != 4:
        raise LearningContractError("BINDING_GRAIN_MISMATCH")
    try:
        validate_document(value, family="vite-binding")
    except LearningContractError as exc:
        if exc.code in {"SCHEMA_INVALID", "SCHEMA_DOCUMENT_INVALID"}:
            raise LearningContractError("BINDING_SCHEMA_INVALID") from exc
        raise

    resolved = _resolved_inputs(value, root)
    rows = value["grainBindings"]
    observed_grains = tuple((row["stageAGrain"], row["viteGrain"]) for row in rows)
    if observed_grains != _EXPECTED_GRAINS:
        raise LearningContractError("BINDING_GRAIN_MISMATCH")

    manifest = parse_json(resolved[("stageA", "promotionManifest")])
    evidence = parse_json(resolved[("fixture", "evidence")])
    if not isinstance(manifest, dict) or not isinstance(evidence, dict):
        raise LearningContractError("BINDING_DEPENDENCY_DOCUMENT_INVALID")
    manifest_rows = manifest.get("sources")
    evidence_rows = evidence.get("sources")
    if not isinstance(manifest_rows, list) or not isinstance(evidence_rows, list) or len(manifest_rows) != 4 or len(evidence_rows) != 4:
        raise LearningContractError("BINDING_DEPENDENCY_DOCUMENT_INVALID")
    stage_a_projection = tuple((row.get("grain"), tuple(row.get("keys", ()))) for row in manifest_rows)
    if stage_a_projection != tuple((grain, keys) for (grain, _), keys in zip(_EXPECTED_GRAINS, _EXPECTED_STAGE_A_KEYS)):
        raise LearningContractError("BINDING_STAGE_A_KEY_MISMATCH")
    if tuple(tuple(row["stageAKeys"]) for row in rows) != _EXPECTED_STAGE_A_KEYS:
        raise LearningContractError("BINDING_STAGE_A_KEY_MISMATCH")

    if _has_alias_cycle(rows):
        raise LearningContractError("BINDING_ALIAS_CYCLIC")
    for row in rows:
        aliases = row["aliases"]
        sources = [alias["from"] for alias in aliases]
        targets = [alias["to"] for alias in aliases]
        if len(aliases) != len(row["stageAKeys"]) or len(set(sources)) != len(sources) or len(set(targets)) != len(targets):
            raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")

    fixture_projection = tuple(tuple(row.get("grain", ())) for row in evidence_rows)
    fixture_order = tuple(tuple(row.get("order", ())) for row in evidence_rows)
    declared_vite_keys = tuple(tuple(row["viteKeys"]) for row in rows)
    if declared_vite_keys != _EXPECTED_VITE_KEYS or fixture_projection != _EXPECTED_VITE_KEYS or fixture_order != _EXPECTED_VITE_KEYS:
        raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")
    for row in rows:
        aliases = row["aliases"]
        sources = [alias["from"] for alias in aliases]
        targets = [alias["to"] for alias in aliases]
        if sources != row["stageAKeys"] or targets != row["viteKeys"]:
            raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
        for source, target, alias in zip(row["stageAKeys"], row["viteKeys"], aliases):
            expected_kind = "identity" if source == target else "identifier-alias"
            if alias != {"from": source, "to": target, "kind": expected_kind}:
                raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
    for source, keys in zip(evidence_rows, _EXPECTED_VITE_KEYS):
        records = source.get("records")
        if not isinstance(records, list) or not records or any(
            not isinstance(record, dict) or any(key not in record for key in keys) for record in records
        ):
            raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")

    vite_projection = _vite_projection(resolved[("issue7", "lessonContract")])
    if tuple(grain for grain, _ in vite_projection) != tuple(vite for _, vite in _EXPECTED_GRAINS):
        raise LearningContractError("BINDING_GRAIN_MISMATCH")
    if tuple(keys for _, keys in vite_projection) != _EXPECTED_VITE_KEYS:
        raise LearningContractError("BINDING_FIXTURE_KEY_MISMATCH")

    non_identity = [alias for row in rows for alias in row["aliases"] if alias["kind"] == "identifier-alias"]
    if len(non_identity) != 3 or {(row["from"], row["to"]) for row in non_identity} != {
        ("region", "region_name"), ("category", "category_name"),
    }:
        raise LearningContractError("BINDING_ALIAS_NOT_BIJECTIVE")
    if value["decision"] != manifest.get("decision") or value["decision"] != "insufficient-evidence/no-common-grain":
        raise LearningContractError("BINDING_DECISION_MISMATCH")
    if value["trustBoundary"] != _EXPECTED_TRUST_BOUNDARY:
        raise LearningContractError("BINDING_AUTHORITY_FORBIDDEN")
    return value


def validate_vite_binding_path(path: pathlib.Path = BINDING_PATH, *, root: pathlib.Path = ROOT) -> dict[str, Any]:
    try:
        value = read_document(path)
    except LearningContractError as exc:
        if exc.code in {"DOCUMENT_SPECIAL_FILE", "DOCUMENT_UNREADABLE"}:
            raise LearningContractError("BINDING_DOCUMENT_SPECIAL_FILE") from exc
        raise
    return validate_vite_binding_document(value, root=root)


def validate_shipped_vite_binding(*, root: pathlib.Path = ROOT) -> dict[str, Any]:
    schema_path = root / BINDING_SCHEMA_PATH.relative_to(ROOT)
    binding_path = root / BINDING_PATH.relative_to(ROOT)
    if not schema_path.is_file() or not binding_path.is_file():
        raise LearningContractError("VITE_BINDING_REQUIRED")
    return validate_vite_binding_path(binding_path, root=root)
