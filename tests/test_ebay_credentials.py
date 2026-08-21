# =============================================================================
# Project     : Market Monitor
# File        : tests/test_ebay_credentials.py
# Author      : Richalbert
# Created     : 2026-08-21
# Last Update : 
# Version     : 0.1
# Description : Test TDD de la lecture des IDs depuis .env
# License     : MIT
#==========================================================

from market_monitor.credentials.ebay import EbayCredentials


def test_ebay_credentials_store_ids():
    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    assert credentials.client_id == "fake-client-id"
    assert credentials.client_secret == "fake-client-secret"