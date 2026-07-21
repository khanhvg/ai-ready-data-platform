from __future__ import annotations

import importlib.util
import hashlib
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]


class VersionMigrationTests(unittest.TestCase):
    def test_registry_has_explicit_current_and_private_lossless_migration(self) -> None:
        registry = ROOT / "learning/contracts/schema-version-registry.json"
        module = ROOT / "scripts/golden/schema_reader.py"
        if not registry.is_file() or not module.is_file(): self.fail("P4-RED-REGISTRY-MIGRATION")
        spec = importlib.util.spec_from_file_location("golden_schema_reader", module)
        assert spec and spec.loader
        reader = importlib.util.module_from_spec(spec); spec.loader.exec_module(reader)
        value = {"schemaVersion": "private-v0", "value": 7}
        migrated = reader.private_migrate(value, "private-v1")
        self.assertEqual(value, reader.private_migrate(migrated, "private-v0"))
        import rfc8785
        payload={"testedTreeSha":"0"*40}; envelope={"payload":payload,"integrity":{"payloadSha256":hashlib.sha256(rfc8785.dumps(payload)).hexdigest()}}
        reader.verify_envelope(envelope)
        envelope["payload"]["changed"]=True
        with self.assertRaisesRegex(reader.SchemaError,"ENVELOPE_PAYLOAD_HASH_MISMATCH"): reader.verify_envelope(envelope)
        registry=json.loads((ROOT/"learning/contracts/schema-version-registry.json").read_text()); families=registry["families"]
        self.assertEqual(len(families),len({row["family"] for row in families}))
        for family in families:
            readable={row["version"]:row for row in family["readableVersions"]}; self.assertIn(family["currentVersion"],readable)
            entry=readable[family["currentVersion"]]; self.assertEqual(entry["schemaSha256"],hashlib.sha256((ROOT/entry["schemaPath"]).read_bytes()).hexdigest())


if __name__ == "__main__": unittest.main()
