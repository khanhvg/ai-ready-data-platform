"""Strict reader and Draft 2020-12 validation scaffold."""

from __future__ import annotations

import pathlib
from typing import Any


class LearningContractError(ValueError):
    """A fail-closed learning-contract refusal with a stable code."""

    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def read_document(path: pathlib.Path, *, family: str | None = None) -> Any:
    del path, family
    raise LearningContractError("LEARNING_READER_NOT_IMPLEMENTED")


def validate_document(value: Any, *, family: str) -> None:
    del value, family
    raise LearningContractError("LEARNING_VALIDATOR_NOT_IMPLEMENTED")
