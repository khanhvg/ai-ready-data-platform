"""Bounded semantic tooling for the closed Stage A architecture curriculum."""

from .content_io import RepositoryLimits, RepositoryReport

STAGE_A_COUNTS = {"modules": 20, "templates": 12, "flows": 11, "bridges": 8, "views": 5}

__all__ = ["RepositoryLimits", "RepositoryReport", "STAGE_A_COUNTS"]
