# =============================================================================
# Project     : Market Monitor
# File        : tests/test_listing.py
# Author      : Richalbert
# Created     : 2026-08-16
# Last Update : 
# Version     : 0.1
# Description : Test TDD de la classe Listing
# License     : MIT
#==============================================================================

from market_monitor.listing import Listing

from market_monitor.tools import convert_price


def test_listing_store_basic_information():
    listing=Listing(
        title="MSI RTX 3080",
        price=350,
        url="https://example.com/annonce/123",
        source="leboncoin",
    )

    assert listing.title == "MSI RTX 3080"
    assert listing.price == 350
    assert listing.url == "https://example.com/annonce/123"
    assert listing.source == "leboncoin"


def test_prix_d_un_site():
    """recevoir un prix provenant d un site"""

    assert convert_price("350 €") == 350
    assert convert_price("1 250 €") == 1250
    assert convert_price("2,50 €") == 2