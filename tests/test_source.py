# =============================================================================
# Project     : Market Monitor
# File        : tests/test_listing.py
# Author      : Richalbert
# Created     : 2026-08-18
# Last Update : 
# Version     : 0.1
# Description : Test TDD d'une source fictive (FakeSource)
#               - Une source recoit une SearchQuerry et
#               - retourne une liste de Listing
# License     : MIT
#==============================================================================

import pytest

from market_monitor.sources.base import Source

from market_monitor.search_query import SearchQuery
from market_monitor.listing import Listing


#------------------------------------------------
# Une source possede une search(...)
# retourne une list[Listing]
#
# class FakeSource(Source)
#   -> FakeSource herite de Source
#------------------------------------------------
class FakeSource(Source):
    def search(self, search):
        return [
            Listing(
                title="MSI MEG X570 UNIFY",
                price=150,
                url="https://example.com/123",
                source="fake",
            )
        ]
    

#-----------------------------------------------
# Quand je donne une SearchQuery a une source,
# elle me retourne une liste de Listing.
#-----------------------------------------------
def test_source_returns_listings():
    search = SearchQuery(
        name="Carte mere X570",
        query="MSI X570 UNIFY",
    )

    source = FakeSource()

    results = source.search(search)

    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0], Listing)


# -------------------------------------------------------------------
# Source represente le concept general d'un markeplace
# On ne doit pas pouvoir creeer directement une Source
#
# Le test reussit si le code situe dans le bloc provoque un TypeError
#---------------------------------------------------------------------
def test_source_cannot_be_instantiated():
    with pytest.raises(TypeError):
        Source()

