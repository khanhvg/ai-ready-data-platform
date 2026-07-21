"""Fitness-result-v2 scaffold."""

from __future__ import annotations

import pathlib
from typing import Any

from .schema import LearningContractError


def verify_fitness(value: dict[str, Any], *, root: pathlib.Path) -> None:
    del value, root
    raise LearningContractError("LEARNING_FITNESS_NOT_IMPLEMENTED")
