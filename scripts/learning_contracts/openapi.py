"""Closed OpenAPI 3.2 profile and constrained YAML validation."""
from __future__ import annotations

from typing import Any

import yaml

VERSION_HEADER = "X-Learning-Contract-Version"
REQUEST_FIELDS = {
    "CreateWorkspaceRequest-v1": {"schemaVersion", "labVersion", "contractSetSha256", "parameters", "expectedProgressRevision"},
    "StartOperationRequest-v1": {"schemaVersion", "commandId", "arguments", "expectedWorkspaceRevision"},
    "ResetWorkspaceRequest-v1": {"schemaVersion", "expectedWorkspaceRevision", "preserveEvidence"},
    "VerifyWorkspaceRequest-v1": {"schemaVersion", "verifierId", "expectedWorkspaceRevision", "expectedProgressRevision"},
    "RegisteredQueryRequest-v1": {"schemaVersion", "workspaceId", "queryId", "parameters", "expectedWorkspaceRevision"},
}
RESPONSE_FIELDS = {
    "Workspace": {"schemaVersion", "workspaceId", "labId", "labVersion", "state", "revision", "activeOperationId", "links"},
}


class _Duplicate(ValueError):
    pass


class StrictLoader(yaml.SafeLoader):
    pass


def _mapping(loader: StrictLoader, node: yaml.MappingNode, deep: bool = False) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in result:
            raise _Duplicate
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


StrictLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)


def code(value: Any) -> str:
    if isinstance(value, bytes):
        try:
            list(yaml.load_all(value.decode("utf-8", "strict"), Loader=StrictLoader))
        except _Duplicate:
            return "OPENAPI_YAML_DUPLICATE_KEY"
        except (UnicodeError, yaml.YAMLError):
            return "OPENAPI_YAML_INVALID"
        return "OK"
    if "matrixOperationIds" in value and set(value["matrixOperationIds"]) != set(value.get("openapiOperationIds", [])):
        return "OPENAPI_OPERATION_SET_MISMATCH"
    if "authority" in value and value["authority"] is None:
        return "OPERATION_AUTHORITY_MISSING"
    if "idempotency" in value and value["idempotency"] is None:
        return "OPERATION_IDEMPOTENCY_MISSING"
    if any(field in {"rawSql", "command", "path", "url", "template"} for field in value.get("requestFields", [])):
        return "OPENAPI_RAW_QUERY_FORBIDDEN"
    reference = value.get("$ref")
    if isinstance(reference, str) and ("://" in reference or reference.startswith("/")):
        return "OPENAPI_REF_FORBIDDEN"
    if "responseHeaders" in value and VERSION_HEADER not in value["responseHeaders"]:
        return "OPENAPI_VERSION_NEGOTIATION_INCOMPLETE"
    if value.get("asyncapiArtifacts") and not value.get("channels"):
        return "ASYNCAPI_WITHOUT_CHANNEL"
    schema = value.get("schema")
    if schema in REQUEST_FIELDS and set(value.get("required", [])) != REQUEST_FIELDS[schema]:
        return "OPENAPI_REQUEST_CONTRACT_MISMATCH"
    if schema in RESPONSE_FIELDS and set(value.get("required", [])) != RESPONSE_FIELDS[schema]:
        return "OPENAPI_RESPONSE_CONTRACT_MISMATCH"
    if "errors" in value and len(value["errors"]) < 5:
        return "OPENAPI_ERROR_CONTRACT_MISMATCH"
    return "OK"
