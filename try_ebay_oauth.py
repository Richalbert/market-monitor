import os
import requests

from market_monitor.credentials.ebay import EbayCredentials
from market_monitor.clients.ebay import EbayClient
from market_monitor.http.requests_client import RequestsHttpClient


# ----------------------------------------------
# Recuperation des identifiants eBay Production
# ----------------------------------------------

credentials = EbayCredentials(
    client_id=os.environ["EBAY_PRODUCTION_CLIENT_ID"],
    client_secret=os.environ["EBAY_PRODUCTION_CLIENT_SECRET"],
)


# -----------------
# Client HTTP reel
# -----------------

http_client = RequestsHttpClient(requests)


# -----------------------
# Client eBay Production
# -----------------------

client = EbayClient(
    credentials=credentials,
    http_client=http_client,
    base_url="https://api.ebay.com",
)


# ----------------------------------------------------
# Suggestions de categories
#
# EbayClient effectue automatiquement :
#
#   1. l'obtention du token OAuth
#   2. la recherche du categoryTreeId de EBAY_FR
#   3. la recherche des suggestions Taxonomy
# ----------------------------------------------------

suggestions = client.get_category_suggestions(
    query="X570 UNIFY",
)

print("Suggestions :", suggestions)
