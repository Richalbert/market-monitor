import os
import requests

from market_monitor.credentials.ebay import EbayCredentials
from market_monitor.clients.ebay import EbayClient
from market_monitor.http.requests_client import RequestsHttpClient


credentials = EbayCredentials(
    client_id=os.environ["EBAY_PRODUCTION_CLIENT_ID"],
    client_secret=os.environ["EBAY_PRODUCTION_CLIENT_SECRET"],
)

http_client = RequestsHttpClient(requests)

client = EbayClient(
    credentials=credentials,
    http_client=http_client,
    base_url="https://api.ebay.com",
)

token = client.get_access_token()

print("Token recu :", bool(token))
print("Longueur du token :", len(token))

results = client.search(
    query="X570 UNIFY",
    access_token=token,
)

print("Cles de la reponse :", results.keys())
print("Nombre de resultats :", results["total"])

items = results.get("itemSummaries")

if items:
    item = items[0]

    print("ID :", item.get("itemId"))
    print("Titre :", item.get("title"))
    print("Prix :", item.get("price"))
    print("Etat :", item.get("condition"))
    print("URL :", item.get("itemWebUrl"))
    print("Marketplace :", item.get("listingMarketplaceId"))

    for item in items:
        print(item.get("title"), "-", item.get("price"))