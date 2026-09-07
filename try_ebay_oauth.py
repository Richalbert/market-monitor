import os
import requests

from market_monitor.credentials.ebay import EbayCredentials
from market_monitor.clients.ebay import EbayClient
from market_monitor.http.requests_client import RequestsHttpClient


credentials = EbayCredentials(
    client_id=os.environ["EBAY_CLIENT_ID"],
    client_secret=os.environ["EBAY_CLIENT_SECRET"],
)

http_client = RequestsHttpClient(requests)

client = EbayClient(
    credentials=credentials,
    http_client=http_client,
)

token = client.get_access_token()

print("Token recu :", bool(token))
print("Longueur du token :", len(token))

results = client.search(
    query="iphone",
    access_token=token,
)

print("Cles de la reponse :", results.keys())
print("Nombre de resultats :", results["total"])
