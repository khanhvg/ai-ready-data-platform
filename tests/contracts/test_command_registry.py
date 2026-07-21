from __future__ import annotations
import json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[2]
ISSUE6=("help","golden-clean","data-contracts-check","evidence-contracts-check","migration-contracts-check","architecture-check","architecture-render")
class CommandRegistryTests(unittest.TestCase):
    def test_exact_54_owner_registry(self) -> None:
        path=ROOT/"learning/contracts/command-owner-registry-v1.json"
        if not path.is_file(): self.fail("P7-RED-54-OWNER-REGISTRY")
        commands=json.loads(path.read_text())["commands"]
        self.assertEqual(54,len(commands)); self.assertEqual(54,len({row["command"] for row in commands})); self.assertEqual(14,len({row["owner"] for row in commands}))
        self.assertEqual(ISSUE6,tuple(row["command"] for row in commands if row["owner"]=="I5-01"))
if __name__=="__main__": unittest.main()
