# =============================================================================
# Project     : Market Monitor
# File        : tests/test_listing.py
# Author      : Richalbert
# Created     : 2026-08-18
# Last Update :
# Version     : 0.1
# Description : Test TDD de la classe SearchQuery
# License     : MIT
# ==============================================================================

from market_monitor.search_query import SearchQuery


def test_search_query_basic_information():
    search = SearchQuery(
        name="Carte mere X570",
        query="MSI X570 UNIFY",
    )

    assert search.name == "Carte mere X570"
    assert search.query == "MSI X570 UNIFY"


# === Test 63 ======================================================
#
#   Comportement :
#   Une SearchQuery peut contenir ses propres termes
#   d'inclusion et d'exclusion.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une recherche eBay pour une carte mere X570.
#
#
#   LORSQUE / WHEN :
#
#       La recherche est configuree avec :
#
#           include_terms = ["X570", "B550"]
#           exclude_terms = ["broken", "for parts"]
#
#
#   ALORS / THEN :
#
#       SearchQuery doit conserver ces deux listes.
#
#
#   POURQUOI CE TEST ?
#
#       Les filtres ne sont pas des donnees globales.
#
#       Deux recherches differentes peuvent avoir des regles
#       differentes.
#
#       Les termes d'inclusion et d'exclusion appartiennent donc
#       naturellement a la configuration d'une recherche.
#
#
#   REGLE METIER INTRODUITE :
#
#       Une SearchQuery peut definir :
#
#           - les termes recherches par la source
#           - la categorie
#           - les termes d'inclusion locaux
#           - les termes d'exclusion locaux
#
# ------------------------------------------------------------------
def test_search_query_can_store_listing_filter_terms():

    # ------------------------------------------------------------------
    # ETANT DONNE - Les regles locales de cette recherche.
    # ------------------------------------------------------------------
    include_terms = [
        "X570",
        "B550",
    ]

    exclude_terms = [
        "broken",
        "for parts",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - La recherche est construite avec ces regles.
    # ------------------------------------------------------------------
    search = SearchQuery(
        name="Cartes meres X570",
        query="X570",
        include_terms=include_terms,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - SearchQuery conserve exactement cette configuration.
    # ------------------------------------------------------------------
    assert search.include_terms == ["X570", "B550"]
    assert search.exclude_terms == ["broken", "for parts"]
