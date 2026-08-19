# =============================================================================
# Project     : Market Monitor
# File        : tests/sources/ebay.py
# Author      : Richalbert
# Created     : 2026-08-19
# Last Update : 
# Version     : 0.1
# Description : 
#             
# License     : MIT
#==============================================================================

from market_monitor.listing import Listing


def parse_item(item: dict) -> Listing:
    return Listing(
        title=item["title"],
        price=int(float(item["price"]["value"])),
        url=item["itemWebUrl"],
        source="ebay",
    )


def parse_items(items: list[dict]) -> list[Listing]:

    # on cree une liste vide d'objet Listing
    results = []

    # on parcourt les reponses eBay
    for item in items:

        # on transforme l'item JSON en objet Listing
        listing = parse_item(item)

        # on le rajoute a la liste
        results.append(listing)

    # on retourne la liste d'objets Listing
    return results