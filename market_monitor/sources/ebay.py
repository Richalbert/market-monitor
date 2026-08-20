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

from market_monitor.sources.base import Source
from market_monitor.search_query import SearchQuery

from market_monitor.listing import Listing

class EbaySource(Source):
    
    # EbaySource recoit la reponse de sa requete au site au format
    # JSON qu elle conserve lors de l'initialisation de l'objet
    def __init__(self, client):
        self.client = client

    # Une source a une methode de recherche
    # qui a partir d'une requete SearchQuery.query 
    # fournit une liste de Listing
    def search(self, search: SearchQuery) -> list[Listing]:

        # la requete (notre recherche) est 
        search = search.query

        # les items dans la reponse du client (le stub) sont
        items = self.client.search(search)

        # le resultat du parse d'items qui transforme 
        # le dictionnaire JSON e liste d'objet Listing est
        results = parse_items(items)

        # et on retourne la liste de Listing
        return results




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