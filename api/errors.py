"""
Custom exception classes for the VetDict analysis platform.

Provides explicit error types to disambiguate between:
  - Library/dependency unavailability (AnalysisUnavailableError)
  - Actual analysis failures (AnalysisError)
  - Data corruption or invalid input (DataCorruptionError)
"""


class AnalysisError(Exception):
    """Raised when an analysis operation fails due to a processing error.

    This is distinct from returning None for 'library not available' —
    AnalysisError means the library was present but the analysis itself
    failed (e.g. bad image data, numerical error, unexpected format).
    """


class AnalysisUnavailableError(AnalysisError):
    """Raised when a required library (OpenCV, PIL) is not installed.

    Callers should catch this to fall back to an alternative analysis
    engine or return a graceful 'unavailable' response.
    """


class DataCorruptionError(Exception):
    """Raised when stored data (JSON, DB records) is corrupt or unparseable.

    This replaces silent fallback-to-empty-dict patterns where data loss
    would otherwise go unnoticed.
    """
