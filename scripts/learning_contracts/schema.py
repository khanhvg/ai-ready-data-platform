"""Descriptor-safe reader and closed Draft 2020-12 validation."""

from __future__ import annotations

import pathlib
import os
import stat
from typing import Any

import jsonschema
import yaml

from . import LearningContractError

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAX_DOCUMENT_BYTES = 2 * 1024 * 1024


class _UniqueYamlLoader(yaml.SafeLoader):
    pass


def _construct_mapping(loader: _UniqueYamlLoader, node: yaml.MappingNode, deep: bool = False) -> dict[Any, Any]:
    result: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise LearningContractError("YAML_DUPLICATE_NAME")
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


_UniqueYamlLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_mapping,
)


def read_regular_bytes(path: pathlib.Path) -> bytes:
    try:
        before = path.lstat()
    except OSError as exc:
        raise LearningContractError("DOCUMENT_UNREADABLE") from exc
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise LearningContractError("DOCUMENT_SPECIAL_FILE")
    flags = os.O_RDONLY | os.O_NONBLOCK | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise LearningContractError("DOCUMENT_SPECIAL_FILE") from exc
    try:
        after = os.fstat(descriptor)
        if (
            not stat.S_ISREG(after.st_mode)
            or after.st_nlink != 1
            or (before.st_dev, before.st_ino) != (after.st_dev, after.st_ino)
            or after.st_size > MAX_DOCUMENT_BYTES
        ):
            raise LearningContractError("DOCUMENT_SPECIAL_FILE")
        raw = os.read(descriptor, MAX_DOCUMENT_BYTES + 1)
        if len(raw) > MAX_DOCUMENT_BYTES:
            raise LearningContractError("DOCUMENT_TOO_LARGE")
        return raw
    finally:
        os.close(descriptor)


def read_document(path: pathlib.Path, *, family: str | None = None) -> Any:
    from .canonical import parse_json

    raw = read_regular_bytes(path)
    if path.suffix == ".json":
        value = parse_json(raw)
    elif path.suffix in {".yaml", ".yml"}:
        if raw.startswith(b"\xef\xbb\xbf"):
            raise LearningContractError("YAML_BOM_REFUSED")
        try:
            text = raw.decode("utf-8", "strict")
            documents = list(yaml.load_all(text, Loader=_UniqueYamlLoader))
        except LearningContractError:
            raise
        except (UnicodeDecodeError, yaml.YAMLError) as exc:
            raise LearningContractError("YAML_INVALID") from exc
        if len(documents) != 1 or documents[0] is None:
            raise LearningContractError("YAML_DOCUMENT_COUNT")
        value = documents[0]
    else:
        raise LearningContractError("DOCUMENT_EXTENSION_UNSUPPORTED")
    if family is not None:
        validate_document(value, family=family)
    return value


def validate_document(value: Any, *, family: str) -> None:
    schemas = {
        "lesson": ROOT / "learning/contracts/lesson-v1.schema.json",
        "lab": ROOT / "learning/contracts/lab-v1.schema.json",
        "progress": ROOT / "learning/contracts/progress-v1.schema.json",
        "learning-evidence": ROOT / "learning/contracts/learning-evidence-v1.schema.json",
        "fitness-result": ROOT / "learning/contracts/fitness-result-v2.schema.json",
        "completion-reconciliation": ROOT / "learning/contracts/completion-reconciliation-v1.schema.json",
        "operation-matrix": ROOT / "learning/contracts/operation-matrix-v1.schema.json",
        "promotion-manifest": ROOT / "learning/contracts/promotion-trust-learning-manifest-v1.schema.json",
        "version-registry": ROOT / "learning/contracts/learning-contract-version-registry-v1.schema.json",
        "command-activation": ROOT / "learning/contracts/command-owner-activation-v1.schema.json",
        "contract-set": ROOT / "learning/contracts/learning-contract-set-v1.schema.json",
        "vite-binding": ROOT / "learning/contracts/promotion-trust-vite-binding-v1.schema.json",
        "problem-details": ROOT / "contracts/openapi/learning-platform-problem-details-v1.schema.json",
    }
    path = schemas.get(family)
    if path is None:
        raise LearningContractError("SCHEMA_FAMILY_UNKNOWN")
    from .canonical import parse_json

    schema_value = parse_json(read_regular_bytes(path))
    try:
        jsonschema.Draft202012Validator.check_schema(schema_value)
        jsonschema.Draft202012Validator(schema_value).validate(value)
    except jsonschema.exceptions.SchemaError as exc:
        raise LearningContractError("SCHEMA_DOCUMENT_INVALID") from exc
    except jsonschema.exceptions.ValidationError as exc:
        raise LearningContractError("SCHEMA_INVALID") from exc


def validate_activation_semantics(value: dict[str, Any], *, root: pathlib.Path = ROOT) -> None:
    """Bind a command activation to the exact admitted base registry bytes."""
    validate_document(value, family="command-activation")
    base = value["baseRegistryPath"]
    actual = __import__("hashlib").sha256((root / base).read_bytes()).hexdigest()
    if value["baseRegistrySha256"] != actual:
        raise LearningContractError("COMMAND_ACTIVATION_BASE_MISMATCH")
