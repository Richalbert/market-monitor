# =============================================================================
# Project     : Market Monitor
# File        : tests/test_listing.py
# Author      : Richalbert
# Created     : 2026-08-18
# Last Update : 
# Version     : 0.1
# Description : Test TDD de la classe SearchQuery
# License     : MIT
#==============================================================================

from market_monitor.search_query import SearchQuery

def test_search_query_basic_information():
    search = SearchQuery(
        name="Carte mere X570",
        query="MSI X570 UNIFY",
    )

    assert search.name == "Carte mere X570"
    assert search.query == "MSI X570 UNIFY"


