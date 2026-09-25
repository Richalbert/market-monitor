# =============================================================================
# Project     : Market Monitor
# File        : market-monitor/sources/ebay.py
# Author      : Richalbert
# Created     : 2026-08-19
# Last Update :
# Version     : 0.1
# Description :
#
# License     : MIT
# ==============================================================================


from market_monitor.sources.base import Source

from market_monitor.search_query import SearchQuery

from market_monitor.models.listing import Listing

from market_monitor.filters import is_relevant_listing


class EbaySource(Source):

    def __init__(self, client):
        self.client = client

    def search(self, search: SearchQuery) -> list[Listing]:

        if search.category is not None:
            response = self.client.search(
                search.query,
                category_id=search.category.id,
            )
        else:
            response = self.client.search(search.query)

        items = response.get("itemSummaries", [])

        # ---------------------------------------------------
        # listings contient toutes les annoncees transformes
        # depuis la reponse eBay
        # ---------------------------------------------------
        listings = parse_items(items)

        # ---------------------------------------------------
        # results contient uniquement celles qui ont passe
        # notre filtre
        # ---------------------------------------------------
        results = []

        # print("exclude_terms =", search.exclude_terms)

        for listing in listings:

            if is_relevant_listing(
                listing,
                include_terms=search.include_terms,
                exclude_terms=search.exclude_terms,
            ):
                results.append(listing)

        return results


def parse_item(item: dict) -> Listing:
    return Listing(
        title=item["title"],
        price=float(item["price"]["value"]),
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
