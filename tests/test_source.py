# =============================================================================
# Project     : Market Monitor
# File        : tests/test_source.py
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
from market_monitor.sources.local import LocalSource

from market_monitor.search_query import SearchQuery
from market_monitor.listing import Listing


#-------------------------------------------------------
# Une source possede une search(...)
# retourne une list[Listing]
#
# class FakeSource(Source)
#   -> FakeSource herite de Source
#
# annotation de type:
#   -> la methode recoit notre propre type SearchQuery et
#   -> retourne une liste de nos propres objets Listing
#--------------------------------------------------------
class FakeSource(Source):
    def search(self, search: SearchQuery) -> list[Listing]:
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

#----------------------------------------------------
# recherche dans la source local une annonce precise
#----------------------------------------------------
def test_local_source_returns_matching_listings():

    # 3 annonces fictives
    listings = [
        Listing(
            title="MSI MEG X570 UNIFY",
            price=150,
            url="https://example.com/1",
            source="local",
        ),
        Listing(
            title="ASUS B550 Gaming",
            price=90,
            url="https://example.com/2",
            source="local",
        ),
        Listing(
            title="MSI X570 UNIFY + Ryzen",
            price=220,
            url="https://example.com/3",
            source="local",
        ),
    ]

    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
    )

    source = LocalSource(listings)
    results = source.search(search)

    assert len(results) == 2
    assert results[0].title == "MSI MEG X570 UNIFY"
    assert results[1].title == "MSI X570 UNIFY + Ryzen"


def test_local_source_search_is_case_insensitive():

    # 3 annonces fictives
    listings = [
        Listing(
            title="MSI MEG X570 UNIFY",
            price=150,
            url="https://example.com/1",
            source="local",
        ),
        Listing(
            title="ASUS B550 Gaming",
            price=90,
            url="https://example.com/2",
            source="local",
        ),
        Listing(
            title="MSI X570 UNIFY + Ryzen",
            price=220,
            url="https://example.com/3",
            source="local",
        ),
    ]

    search = SearchQuery(
        name="Carte mere X570",
        query="x570 unify",
    )

    source = LocalSource(listings)
    results = source.search(search)

    assert len(results) == 2
    assert results[0].title == "MSI MEG X570 UNIFY"
    assert results[1].title == "MSI X570 UNIFY + Ryzen"

#-------------------------------------------------
# LocalSource recoit les annonces
# et effetue l recherche sur celle ci
#--------------------------------------------------
def test_local_source_accepts_listings():

    # 2 annonces fictives
    listings = [
        Listing(
            title="MSI Meg x570 Unify",
            price=150,
            url="https://example.com/1",
            source="local",
        ),
        Listing(
            title="ASUS B550 Gaming",
            price=90,
            url="https://example.com/2",
            source="local",
        ),
    ]

    # les annonces sont passees a la Source Locale
    source = LocalSource(listings)

    # on recherche cette query
    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
    )

    results = source.search(search)

    assert len(results) == 1
    assert results[0].title == "MSI Meg x570 Unify"
