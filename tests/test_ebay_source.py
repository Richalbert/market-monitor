# =============================================================================
# Project     : Market Monitor
# File        : tests/test_ebay_source.py.py
# Author      : Richalbert
# Created     : 2026-08-19
# Last Update : 
# Version     : 0.1
# Description : Test TDD d'une source fictive venant de eBay
#               - Transformer la reponse eBay en un objet Listing
# License     : MIT
#==============================================================================

from market_monitor.sources.ebay import parse_item
from market_monitor.sources.ebay import parse_items

from market_monitor.listing import Listing

def test_parse_item():

    # Soit le JSON suivant correspondant a une reponse eBay

    item = {
        "title": "MSI MEG X570 UNIFY",
        "price": {
            "value": "149.99",
            "currency": "EUR",
        },
        "itemWebUrl": "https://www.ebay.fr/itm/123",
    }

    # Que nous voulons transformer en objet Listing

    listing = parse_item(item)

    # verification a travers les tests

    assert listing.title == "MSI MEG X570 UNIFY"
    assert listing.price == 149
    assert listing.url == "https://www.ebay.fr/itm/123"
    assert listing.source == "ebay"


def test_parse_items():

    # Soit 2 resultats dans notre reponse eBay

    item1 = {
        "title": "MSI MEG X570 UNIFY",
        "price": {
            "value": "149.99",
            "currency": "EUR",
        },
        "itemWebUrl": "https://www.ebay.fr/itm/123",
    }

    item2 = {
        "title": "ASUS B550 Gaming",
        "price": {
            "value": "90",
            "currency": "EUR",
        },
        "itemWebUrl": "https://www.ebay.fr/itm/456",
    }

    items = [item1, item2]

    # Que l'on souhaite transformer en 2 objets Listing

    listings = parse_items(items)

    # Verification a travers les tests suivants
    # parse_items() doit retourner 2 objets 
    # les objets doivent etre de type Listing

    assert len(listings) == 2
    assert isinstance(listings[0], Listing)
    assert isinstance(listings[1], Listing)
