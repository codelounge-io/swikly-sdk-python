from swikly import SwiklyClient

client = SwiklyClient(
    token="<<PAST_TOKEN>>",
    environment="sandbox",
    user_agent="SwiklySDK/1.0",
)

accounts = client.accounts.list()
account_id = accounts.accounts[0].id
print("Account ID:", account_id)
resp = client.requests.create(
    account_id=account_id,
    description="My simple deposit request",
    language="fr",
    first_name="John",
    last_name="Doe",
    deposit={"startDate": "2026-06-10", "endDate": "2026-06-12", "amount": 12000},
)

print("Checkout link:", resp.request.link)
