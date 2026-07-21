"""Issue #8 learning-contract tests and behavior-path helpers."""

from __future__ import annotations

import json
import pathlib
import unittest
from typing import Any

from scripts.learning_contracts.check import evaluate


FIXTURES = pathlib.Path(__file__).resolve().parents[2] / "fixtures" / "learning" / "contracts"


def fixture(relative: str) -> Any:
    raw = (FIXTURES / relative).read_bytes()
    if relative.endswith(".yaml"):
        return raw
    try:
        value = json.loads(raw)
    except (UnicodeDecodeError, json.JSONDecodeError):
        return raw
    if isinstance(value, dict) and set(value) == {"encodedHex"}:
        return bytes.fromhex(value["encodedHex"])
    if isinstance(value, dict) and set(value) == {"encodedJson"}:
        return value["encodedJson"].encode("utf-8")
    if relative.startswith("invalid/canonicalization/"):
        return raw
    return value


def assert_invalid(test: unittest.TestCase, test_id: str, domain: str, value: Any, expected: str) -> None:
    actual = evaluate(domain, value).code
    test.assertEqual(actual, expected, f"{test_id} expected={expected} actual={actual}")
