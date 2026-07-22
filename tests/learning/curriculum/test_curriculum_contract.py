from __future__ import annotations

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[3]
INPUT_SHA = "c07c9a080be7be88447aac497bdf0a2b5fddd020"
RELEASE_SHA = "fecf6bb8e5dfa7cc69f9766f72ac6f5b9301dad9"
FIXTURE = ROOT / "tests/fixtures/learning/curriculum/invalid-cases-v1.json"


def _allowlist() -> tuple[str, ...]:
    amendment = (ROOT / "plans/260721-011-architecture-curriculum/stage-a-release-amendment.md").read_text()
    body = amendment.split("## Exact Stage A Tracked Write Allowlist", 1)[1]
    block = body.split("```text", 1)[1].split("```", 1)[0]
    return tuple(line.strip() for line in block.splitlines() if line.strip())


BEHAVIOR_PATHS = tuple(path for path in _allowlist() if not path.startswith("tests/"))


def require_stage_a_behavior() -> None:
    """Fail RED only after immutable dependencies are proven available."""
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    subprocess.run(["git", "cat-file", "-e", f"{RELEASE_SHA}^{{commit}}"], cwd=ROOT, check=True)
    for required in (
        "python3.12",
        "node",
        "npm",
    ):
        if shutil.which(required) is None:
            raise AssertionError(f"I11_REQUIRED_TOOL_MISSING:{required}")
    for relative in (
        "scripts/learning_contracts/runtime.py",
        "scripts/golden/architecture_pipeline.py",
        "learning/contracts/operation-matrix-v1.json",
    ):
        if not (ROOT / relative).is_file():
            raise AssertionError(f"I11_RELEASED_PRECONDITION_MISSING:{relative}")
    missing = [path for path in BEHAVIOR_PATHS if not (ROOT / path).is_file()]
    if missing:
        marker = "I11_PRECONDITION_BEHAVIOR_ABSENT"
        raise AssertionError(f"{marker}:head={head}:missing={len(missing)}:first={missing[0]}")


def cases(validator: str) -> list[dict[str, object]]:
    value = json.loads(FIXTURE.read_text())
    return [case for case in value["cases"] if case["validator"] == validator]


def candidate_root() -> tempfile.TemporaryDirectory[str]:
    holder = tempfile.TemporaryDirectory(prefix="i11-candidate-")
    destination = pathlib.Path(holder.name)
    shutil.copytree(ROOT / "learning", destination / "learning")
    shutil.copytree(ROOT / "architecture", destination / "architecture")
    return holder


def apply_mutation(base: pathlib.Path, mutation: dict[str, object]) -> None:
    target = base / str(mutation["target"])
    kind = mutation["kind"]
    if kind in {"json-set", "json-remove"}:
        value = json.loads(target.read_text())
        parts = [part.replace("~1", "/").replace("~0", "~") for part in str(mutation["pointer"]).split("/")[1:]]
        parent = value
        for part in parts[:-1]:
            parent = parent[int(part)] if isinstance(parent, list) else parent[part]
        leaf = parts[-1]
        if kind == "json-remove":
            if isinstance(parent, list):
                parent.pop(int(leaf))
            else:
                parent.pop(leaf)
        else:
            replacement = mutation.get("value")
            if "valueRepeat" in mutation:
                repeat = mutation["valueRepeat"]
                replacement = str(repeat["text"]) * int(repeat["count"])
            if isinstance(parent, list):
                parent[int(leaf)] = replacement
            else:
                parent[leaf] = replacement
        target.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    elif kind in {"text-set", "render-source-set"}:
        text = target.read_text()
        needle = str(mutation["needle"])
        if needle not in text:
            raise AssertionError(f"I11_FIXTURE_PRECONDITION_MISSING:{needle}")
        target.write_text(text.replace(needle, str(mutation["value"]), 1))
    else:
        raise AssertionError(f"I11_FIXTURE_KIND_UNKNOWN:{kind}")


def run_public(module: str, root: pathlib.Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", module, "--root", str(root), *arguments],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
    )


class CurriculumContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        require_stage_a_behavior()

    def test_public_curriculum_validator_accepts_all_real_files(self) -> None:
        result = run_public("learning.curriculum.tools.check_curriculum", ROOT, "--no-evidence", "--json")
        self.assertEqual(result.returncode, 0, result.stdout)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["moduleCount"], 20)
        self.assertEqual(summary["templateCount"], 12)
        self.assertEqual(summary["validatedFileCount"], 18)

    def test_curriculum_invalid_cases_reach_public_validator(self) -> None:
        for case in cases("curriculum"):
            with self.subTest(case=case["id"]), candidate_root() as temporary:
                root = pathlib.Path(temporary)
                apply_mutation(root, case["mutation"])
                result = run_public("learning.curriculum.tools.check_curriculum", root, "--no-evidence")
                self.assertNotEqual(result.returncode, 0, result.stdout)
                self.assertIn(str(case["expectedCode"]), result.stdout)


if __name__ == "__main__":
    unittest.main()
