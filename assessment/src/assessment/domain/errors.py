"""Typed failures at contract, storage, migration, and archive boundaries."""


class AssessmentError(Exception):
    """Base exception for the assessment package."""


class ContentValidationError(AssessmentError, ValueError):
    """A schema, authored document, or semantic contract is invalid."""


class InvalidPathError(AssessmentError, ValueError):
    """A path is not a safe relative POSIX key."""


class EngagementNotFoundError(AssessmentError, FileNotFoundError):
    """The requested engagement does not exist."""


class EngagementExistsError(AssessmentError, FileExistsError):
    """The requested engagement or import destination already exists."""


class ConcurrentWriteError(AssessmentError):
    """Another writer owns the engagement lock."""


class CompatibilityError(AssessmentError):
    """A document or archive uses an unsupported version."""


class ArchiveValidationError(AssessmentError, ValueError):
    """An archive or exported entry is unsafe or violates the v1 contract."""
