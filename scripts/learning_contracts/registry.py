"""Composition of the immutable Issue #6 registry and Issue #8 overlay."""
from __future__ import annotations

from .canonical import ContractError
from .schema import ROOT, load_json, sha256, validate

BASE_PATH = "learning/contracts/schema-version-registry.json"
BASE_SHA = "8e18588f63b5d99c0b60a229758575e8badf0f055bfcb4f89908f9fa2684a57e"


def compose() -> dict[str, object]:
    overlay = load_json("learning/contracts/learning-contract-version-registry-v1.json")
    validate(overlay, "learning/contracts/learning-contract-version-registry-v1.schema.json")
    if sha256(ROOT / BASE_PATH) != BASE_SHA or overlay["baseRegistry"] != {"path": BASE_PATH, "sha256": BASE_SHA}:
        raise ContractError("BASE_REGISTRY_HASH_MISMATCH")
    base = load_json(BASE_PATH)
    base_rows = base.get("families", [])
    base_families = {
        row["family"] if isinstance(row, dict) else str(row)
        for row in base_rows
    }
    owned: dict[str, object] = {}
    schema_ids: set[str] = set()
    for family in overlay["ownedFamilies"]:
        name = family["family"]
        if name in base_families or name in owned:
            raise ContractError("SCHEMA_FAMILY_COLLISION")
        for version in family["versions"]:
            path = ROOT / version["schemaPath"]
            if sha256(path) != version["sha256"]:
                raise ContractError("REF_SCHEMA_HASH_MISMATCH")
            schema = load_json(version["schemaPath"])
            if schema["$id"] != version["schemaId"] or schema["$id"] in schema_ids:
                raise ContractError("SCHEMA_FAMILY_COLLISION")
            schema_ids.add(schema["$id"])
        owned[name] = family
    extension = overlay["familyExtensions"][0]
    if extension["family"] != "fitness-result" or extension["addedReadableVersions"] != ["v2"]:
        raise ContractError("SCHEMA_VERSION_UNREADABLE")
    return {"base": base, "owned": owned, "extension": extension}
