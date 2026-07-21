"""Closed OpenAPI 3.2 project-profile validation."""
from __future__ import annotations

import json
from pathlib import Path

from .canonical import ContractError, parse_json
from .schema import ROOT, load_json, validate

OPENAPI_PATH = "contracts/openapi/learning-platform-v1.yaml"


def load_openapi(path: Path | None = None) -> dict[str, object]:
    import yaml

    source = path or ROOT / OPENAPI_PATH
    raw = source.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ContractError("OPENAPI_YAML_BOM_FORBIDDEN")
    try:
        text = raw.decode("utf-8", "strict")
        events = list(yaml.parse(text))
        node = yaml.compose(text)
    except (UnicodeError, yaml.YAMLError) as exc:
        raise ContractError("OPENAPI_YAML_INVALID") from exc
    if any(getattr(event, "anchor", None) for event in events):
        raise ContractError("OPENAPI_YAML_ALIAS_FORBIDDEN")
    def reject_duplicate_keys(current: object) -> None:
        if isinstance(current, yaml.MappingNode):
            observed: set[str] = set()
            for key, value in current.value:
                name = str(key.value)
                if name in observed:
                    raise ContractError("OPENAPI_YAML_DUPLICATE_KEY")
                observed.add(name)
                reject_duplicate_keys(value)
        elif isinstance(current, yaml.SequenceNode):
            for value in current.value:
                reject_duplicate_keys(value)
    reject_duplicate_keys(node)
    try:
        document = parse_json(raw)
    except ContractError as exc:
        if exc.code == "JSON_DUPLICATE_NAME":
            raise ContractError("OPENAPI_YAML_DUPLICATE_KEY") from exc
        raise ContractError("OPENAPI_YAML_NON_JSON") from exc
    if not isinstance(document, dict):
        raise ContractError("OPENAPI_PROFILE_INVALID")
    return document


def operation_set(document: dict[str, object]) -> set[tuple[str, str, str]]:
    result: set[tuple[str, str, str]] = set()
    for path, item in document["paths"].items():
        for method, operation in item.items():
            key = (method.upper(), path, operation["operationId"])
            if key in result:
                raise ContractError("OPERATION_DUPLICATE")
            result.add(key)
    return result


def check() -> dict[str, object]:
    document = load_openapi()
    validate(document, "contracts/openapi/learning-platform-openapi-profile-v1.schema.json")
    matrix = load_json("learning/contracts/operation-matrix-v1.json")
    expected = {(row["method"], row["path"], row["operationId"]) for row in matrix["operations"]}
    if operation_set(document) != expected:
        raise ContractError("OPENAPI_OPERATION_SET_MISMATCH")
    for row in matrix["operations"]:
        operation = document["paths"][row["path"]][row["method"].lower()]
        parameters = {parameter["name"] for parameter in operation.get("parameters", [])}
        if row["method"] == "POST" and parameters != {"Idempotency-Key", "X-Correlation-ID"}:
            raise ContractError("OPERATION_IDEMPOTENCY_MISSING")
        if operation.get("requestBody", {}).get("content", {}).get("application/json", {}).get("schema", {}).get("additionalProperties") is not False and row["method"] == "POST":
            raise ContractError("OPENAPI_REQUEST_CONTRACT_MISMATCH")
    if matrix["channels"] != []:
        raise ContractError("ASYNCAPI_WITHOUT_CHANNEL")
    return document
