# swikly-sdk (unofficial)

Production-grade Python SDK for Swikly API v2 (sync + async), based on Swikly's OpenAPI spec.

## Install

```bash
pip install swikly-sdk
```

## Quickstart

```python
from swikly import SwiklyClient

client = SwiklyClient(
    token="YOUR_API_TOKEN",
    environment="sandbox",  # or "production"
    user_agent="YourProject/1.0",
)

accounts = client.accounts.list()
account_id = accounts.accounts[0].id

req = client.requests.create(
    account_id=account_id,
    description="My simple deposit request",
    language="fr",
    first_name="John",
    last_name="Doe",
    deposit={"startDate": "2026-06-10", "endDate": "2026-06-12", "amount": 12000},
)
print(req.request.link)
```

## Webhook signature verification

```python
from swikly.webhooks import verify_swikly_signature

ok = verify_swikly_signature(
    secret="ACCOUNT_SECRET",
    signature_header=headers["Swikly-Signature"],
    raw_body=request_raw_body_bytes,
    tolerance_seconds=10 * 60,
)
```

## Notes
- Swikly requires `Accept: application/json`.
- Swikly recommends setting a meaningful `User-Agent` (e.g. `YourProject/1`).
