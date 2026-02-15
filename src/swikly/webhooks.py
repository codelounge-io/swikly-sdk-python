from __future__ import annotations

import hmac
import hashlib
import time
from typing import Optional, Tuple


class InvalidSignatureHeader(ValueError):
    pass


def _parse_signature_header(signature_header: str) -> Tuple[str, str]:
    # Format: t=1739352941,sha256=<hex>
    parts = [p.strip() for p in signature_header.split(",") if p.strip()]
    values = {}
    for part in parts:
        if "=" not in part:
            continue
        k, v = part.split("=", 1)
        values[k.strip()] = v.strip()
    ts = values.get("t")
    sig = values.get("sha256")
    if not ts or not sig:
        raise InvalidSignatureHeader("Invalid Swikly-Signature header")
    return ts, sig


def verify_swikly_signature(
    *,
    secret: str,
    signature_header: str,
    raw_body: bytes,
    tolerance_seconds: int = 10 * 60,
    now: Optional[int] = None,
) -> bool:
    ts_str, provided = _parse_signature_header(signature_header)
    try:
        ts = int(ts_str)
    except ValueError as e:
        raise InvalidSignatureHeader("Invalid timestamp in Swikly-Signature header") from e

    now_ts = int(now if now is not None else time.time())
    if abs(now_ts - ts) > tolerance_seconds:
        return False

    signed_payload = (ts_str + ".").encode("utf-8") + raw_body
    expected = hmac.new(secret.encode("utf-8"), signed_payload, hashlib.sha256).hexdigest()

    # constant-time compare
    return hmac.compare_digest(expected, provided)
