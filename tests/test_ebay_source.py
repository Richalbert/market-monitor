# =============================================================================
# Project     : Market Monitor
# File        : tests/test_ebay_source.py
# Author      : Richalbert
# Created     : 2026-08-19
# Last Update :
# Version     : 0.1
# Description : Test TDD d'une source fictive venant de eBay
#               - Transformer la reponse eBay en un objet Listing
# License     : MIT
# ==============================================================================

from market_monitor.sources.ebay import (
    parse_item,
    parse_items,
    EbaySource,
)

from market_monitor.search_query import SearchQuery

from market_monitor.models.listing import Listing

from market_monitor.models.category import Category


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
    assert listing.price == 149.99
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


# ---------------------------------------------------------------
# le StubEbayClient joue le role d'eBay, sans jamais faire
# de connection internet, il retourne un fichier JSON comme le
# ferai une vrai requete HTTP vers eBay
# --------------------------------------------------------------
class StubEbayClient:

    def search(self, query):
        return [
            {
                "title": "MSI MEG X570 UNIFY",
                "price": {
                    "value": "149.99",
                    "currency": "EUR",
                },
                "itemWebUrl": "https://www.ebay.fr/itm/123",
            },
            {
                "title": "MSI X570 UNIFY + Ryzen",
                "price": {
                    "value": "220",
                    "currency": "EUR",
                },
                "itemWebUrl": "https://www.ebay.fr/itm/456",
            },
        ]


def test_ebay_source_search_returns_listings():

    # le client recoit la reponse du Stub eBay
    client = StubEbayClient()

    # on injecte la reponse du stub dans notre source
    source = EbaySource(client)

    # Voila notre recherche
    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
    )

    # et le resultat de notre recherche
    results = source.search(search)

    assert len(results) == 2
    assert isinstance(results[0], Listing)
    assert isinstance(results[1], Listing)


# === Test 33 ======================================================
#
#   Teste la precision monetaire
#
# ------------------------------------------------------------------
def test_parse_item_preserves_price_decimals():

    item = {
        "title": "OEM I/O Shield For MSI MEG X570 UNIFY Motherboard Backplate IO",
        "price": {
            "value": "19.36",
            "currency": "EUR",
        },
        "itemWebUrl": "https://www.ebay.fr/itm/396052469502",
    }

    listing = parse_item(item)

    assert listing.price == 19.36


# === Test 41 en style BDD ==========================================
#
#   Comportement :
#       EbaySource transmet au client eBay la categorie selectionnee
#       dans SearchQuery
#
#   ÉTANT DONNÉ
#       une SearchQuery "X570 UNIFY"
#       avec la catégorie "Cartes mères" / 1244
#
#   LORSQUE
#       EbaySource exécute cette recherche
#
#   ALORS
#       EbayClient reçoit :
#           query = "X570 UNIFY"
#           category_id = "1244"
#
# ------------------------------------------------------------------


class SpyEbayClient:

    def __init__(self):
        self.last_query = None
        self.last_category_id = None

    def search(self, query, category_id=None):
        self.last_query = query
        self.last_category_id = category_id

        return []


def test_ebay_source_transmits_selected_category():

    # ------------------------------------------------------------------
    # ETANT DONNE - Un client eBay espion qui enregistre les parametres
    #               de recherche recus
    # ------------------------------------------------------------------
    client = SpyEbayClient()

    # ------------------------------------------------------------------
    # ETANT DONNE - Une source eBay utilisant ce client espion
    # ------------------------------------------------------------------
    source = EbaySource(client)

    # ------------------------------------------------------------------
    # ETANT DONNE - Une categorie eBay choisie par l'utilisateur
    # ------------------------------------------------------------------
    category = Category(
        id="1244",
        name="Cartes mères",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Une recherche associee a cette categorie
    # ------------------------------------------------------------------
    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
        category=category,
    )

    # ------------------------------------------------------------------
    # LORSQUE - EbaySource execute la recherche
    # ------------------------------------------------------------------
    source.search(search)

    # ------------------------------------------------------------------
    # ALORS - Le client eBay recoit le texte recherche
    #         et l'identifiant de la categorie selectionnee
    # ------------------------------------------------------------------
    assert client.last_query == "X570 UNIFY"
    assert client.last_category_id == "1244"


# === Test 42 ======================================================
#
#   Comportement :
#       EbaySource doit pouvoir effectuer une recherche lorsqu'aucune
#       categorie eBay n'a ete selectionnee.
#
#       Ce test protege le comportement historique de MarketMonitor :
#       une SearchQuery peut contenir uniquement un texte de recherche.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une recherche :
#
#           query = "X570 UNIFY"
#
#       sans categorie :
#
#           category = None
#
#
#   LORSQUE / WHEN :
#
#       EbaySource execute cette recherche.
#
#
#   ALORS / THEN :
#
#       EbayClient doit recevoir :
#
#           query = "X570 UNIFY"
#
#       mais aucune categorie particuliere :
#
#           category_id = None
#
#
#   Ce comportement garantit que l'ajout des categories n'a pas
#   casse les anciennes recherches.
#
# ------------------------------------------------------------------
def test_ebay_source_search_without_selected_category():

    # ------------------------------------------------------------------
    # ETANT DONNE - Un client eBay espion.
    #
    #   Le Spy ne contacte pas eBay.
    #   Il enregistre simplement les informations que EbaySource
    #   lui transmet afin que nous puissions ensuite les verifier.
    # ------------------------------------------------------------------
    client = SpyEbayClient()

    # ------------------------------------------------------------------
    # ETANT DONNE - Une source eBay utilisant notre client espion.
    #
    #   EbaySource est la couche que nous testons ici.
    # ------------------------------------------------------------------
    source = EbaySource(client)

    # ------------------------------------------------------------------
    # ETANT DONNE - Une recherche sans categorie selectionnee.
    #
    #   Nous ne passons volontairement PAS :
    #
    #     category=...
    #
    #   Comme SearchQuery.category vaut None par defaut,
    #   cette recherche represente l'ancien fonctionnement
    #   de MarketMonitor.
    # ------------------------------------------------------------------
    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
    )

    # ------------------------------------------------------------------
    # LORSQUE - EbaySource execute cette recherche.
    #
    #   C'est l'ACTION du scenario BDD.
    # ------------------------------------------------------------------
    source.search(search)

    # ------------------------------------------------------------------
    # ALORS - Le texte de recherche doit etre transmis au client eBay.
    # ------------------------------------------------------------------
    assert client.last_query == "X570 UNIFY"

    # ------------------------------------------------------------------
    # ALORS - Aucune categorie ne doit avoir ete transmise.
    #
    #   Notre Spy initialise last_category_id a None.
    #   Si EbaySource n'envoie aucune categorie, cette valeur reste None.
    # ------------------------------------------------------------------
    assert client.last_category_id is None
