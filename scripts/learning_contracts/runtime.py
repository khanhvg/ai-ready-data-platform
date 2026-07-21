"""Runtime, dependency, authority, and cleanup admission rules."""
from __future__ import annotations

from typing import Any

EXPECTED_LOCK_SHA = "f41c727b39f99106f95b7937b2811e8d27db89d1d5106e9f1d9effd4403143d2"
ADMITTED_IMPORTS = {"jsonschema", "rfc8785", "yaml"}
FORBIDDEN_READ_PREFIXES = ("spikes/web/", "portal/", "runner/", "contracts/adr/")


def authority_code(value: dict[str, Any]) -> str:
    identities = [value.get(name) for name in ("local", "tracking", "live")]
    if any(identities) and len(set(identities)) != 1:
        return "AUTHORITY_HEAD_MISMATCH"
    if "leaseOwners" in value and value["leaseOwners"] != ["I5-03"]:
        return "AUTHORITY_LEASE_REQUIRED"
    if value.get("protectedExpected") != value.get("protectedActual") and "protectedExpected" in value:
        return "PROTECTED_PATH_CHANGED"
    if value.get("fixtureManifestHash") != value.get("artifactHash") and "fixtureManifestHash" in value:
        return "FIXTURE_MANIFEST_ARTIFACT_MISMATCH"
    if any(str(path).startswith(FORBIDDEN_READ_PREFIXES) for path in value.get("reads", [])):
        return "STAGE_A_FRAMEWORK_DEPENDENCY"
    return "OK"


def dependency_code(value: dict[str, Any]) -> str:
    if any(name not in ADMITTED_IMPORTS for name in value.get("imports", [])):
        return "DEPENDENCY_IMPORT_UNADMITTED"
    if "lockSha256" in value and value["lockSha256"] != EXPECTED_LOCK_SHA:
        return "DEPENDENCY_MANIFEST_DRIFT"
    if "inheritedAdvisoryDisposition" in value and value["inheritedAdvisoryDisposition"] != "reviewed-inherited-no-delta":
        return "DEPENDENCY_ADVISORY_UNRESOLVED"
    return "OK"


def rollback_code(value: dict[str, Any]) -> str:
    if not value.get("owned") or value.get("marker") != "learning-contracts-v1" or value.get("links") != 1:
        return "ROLLBACK_SCOPE_UNOWNED"
    return "OK"
