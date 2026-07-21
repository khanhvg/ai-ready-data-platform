"""Issue #8 Stage A RED oracle shared by the contract test modules."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
INDEX = ROOT / "tests/fixtures/learning/contracts/fixture-index-v1.json"


def red_case(test_id: str) -> dict[str, object]:
    rows = json.loads(INDEX.read_text(encoding="utf-8"))["cases"]
    return next(row for row in rows if row["testId"] == test_id)


def assert_contract_behavior(testcase: object, test_id: str) -> None:
    case = red_case(test_id)
    for locator in case["paths"]:
        if locator != "generated-private":
            testcase.assertTrue(
                (ROOT / locator).is_file(),
                f"{test_id}: indexed negative fixture is missing",
            )
    from scripts.learning_contracts.check import evaluate_red_case

    testcase.assertEqual(
        evaluate_red_case(test_id),
        case["expectedCode"],
        f"{test_id}: frozen negative contract did not fail with its exact code",
    )
