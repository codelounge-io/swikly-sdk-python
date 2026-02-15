from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional


class SwiklyError(Exception):
    """Base error for the Swikly SDK."""


@dataclass
class SwiklyAPIError(SwiklyError):
    status_code: int
    message: str
    code: Optional[str] = None
    context: Any = None
    errors: Any = None
    request_id: Optional[str] = None
    raw: Any = None

    def __str__(self) -> str:
        parts = [f"Swikly API error {self.status_code}: {self.message}"]
        if self.code:
            parts.append(f"code={self.code}")
        if self.request_id:
            parts.append(f"request_id={self.request_id}")
        return " | ".join(parts)


class SwiklyAuthError(SwiklyAPIError):
    """401/403."""


class SwiklyNotFoundError(SwiklyAPIError):
    """404."""


class SwiklyRateLimitError(SwiklyAPIError):
    """429."""

    retry_after: Optional[int] = None


class SwiklyValidationError(SwiklyAPIError):
    """422 with field errors."""
