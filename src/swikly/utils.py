from __future__ import annotations

import time
from typing import Any, Dict, Optional, Tuple

import httpx


def _default_base_url(environment: str) -> str:
    env = (environment or "").lower()
    if env in {"prod", "production", "live"}:
        return "https://api.v2.swikly.com/v1"
    if env in {"sandbox", "test", "testing"}:
        return "https://api.sandbox.swikly.com/v1"
    # Allow passing a full URL as environment for convenience
    if env.startswith("http://") or env.startswith("https://"):
        return environment
    raise ValueError("environment must be 'production', 'sandbox', or a base URL")


def _coerce_with_param(with_: Optional[list[str] | tuple[str, ...] | str]) -> Optional[str]:
    if with_ is None:
        return None
    if isinstance(with_, str):
        return with_
    return ",".join(with_)


def _parse_error_payload(data: Any) -> Tuple[Optional[str], str, Any, Any]:
    # Swikly examples:
    # {"code":"ERR_PARAMS","message":"...","errors":{...}}
    # {"message":"Too Many Attempts."}
    code = None
    message = "Unknown error"
    context = None
    errors = None
    if isinstance(data, dict):
        code = data.get("code")
        message = data.get("message") or message
        context = data.get("context")
        errors = data.get("errors")
    elif isinstance(data, str):
        message = data
    return code, message, context, errors


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


def _read_retry_after(headers: httpx.Headers) -> Optional[int]:
    ra = headers.get("Retry-After")
    if not ra:
        return None
    try:
        return int(ra)
    except ValueError:
        return None
