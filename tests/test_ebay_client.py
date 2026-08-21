# =============================================================================
# Project     : Market Monitor
# File        : tests/test_ebay_client.py
# Author      : Richalbert
# Created     : 2026-08-21
# Last Update : 
# Version     : 0.1
# Description : Test TDD du client eBay qui sera appartir des
#               IDs dans.env 
#               - de passer OAuth eBay Sandbox
#               - d'obtenir des acces_token et 
#               - d'utiliser Browse API 
# License     : MIT
#==========================================================

from market_monitor.credentials.ebay import EbayCredentials
from market_monitor.clients.ebay import EbayClient


def test_ebay_client_stores_credentials():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    client = EbayClient(credentials)

    assert client.credentials == credentials





