import pytest
from swikly.webhooks import verify_swikly_signature

def test_verify_signature_roundtrip():
    secret = "abc"
    raw = b'{"event":"requestSecured","request":{"id":"x"}}'
    # Construct header
    ts = 1739352941
    import hmac, hashlib
    signed = (str(ts) + ".").encode() + raw
    sig = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    header = f"t={ts},sha256={sig}"
    assert verify_swikly_signature(secret=secret, signature_header=header, raw_body=raw, tolerance_seconds=10**9, now=ts)
