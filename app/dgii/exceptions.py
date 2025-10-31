"""Custom exceptions for DGII integrations."""
from __future__ import annotations


class DGIIError(Exception):
    """Base DGII exception."""


class DGIIAuthError(DGIIError):
    """Raised when authentication with DGII fails permanently."""


class DGIISignError(DGIIError):
    """Raised when XML signing fails."""


class DGIIReceiptError(DGIIError):
    """Raised when the DGII reception service returns an error."""


class DGIIRetryableError(DGIIError):
    """Indicates that the operation can be retried (e.g. transient HTTP issues)."""
