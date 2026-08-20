# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/sources/local.py
# Author      : Richalbert
# Created     : 2026-08-19
# Last Update : 
# Version     : 0.1
# Description : La classe LocalSource: 
#               - elle possede une petite liste d'annonces fictive, puis
#               - elle retourne celles qui correspondent a search.query
# License     : MIT
#==============================================================================

from market_monitor.sources.base import Source
from market_monitor.search_query import SearchQuery
from market_monitor.listing import Listing


class LocalSource(Source):

    def search(self, search: SearchQuery) -> list[Listing]:
        pass

#----------------------------
# 3 annonces fictives
#----------------------------
class LocalSource(Source):

    # LocalSource recoit une liste de Listing a sa creation
    def __init__(self, listings):
        self.listings = listings

    # Une source a une methode de recherche
    def search(self, search: SearchQuery) -> list[Listing]:

        results = []

        # on parcourt les annonces
        for listing in self.listings:
            
            # si ce qu on cherche est dans le titre de l'annonce
            if search.query.upper() in listing.title.upper():

                # alors on l'ajoute au resultat
                results.append(listing)

        return results




