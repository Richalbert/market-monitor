#
# tests/test_ebay_workflow.py
#


# === Test 53 ======================================================
#
#   Comportement :
#   Une categorie proposee par eBay Taxonomy peut etre selectionnee
#   puis utilisee pour effectuer une recherche Browse.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une recherche utilisateur :
#
#           "X570 UNIFY"
#
#       eBay Taxonomy propose deux categories :
#
#           170080 -> "Cartes mère: plaques arrière"
#           1244   -> "Cartes mères"
#
#
#   ETANT DONNE :
#
#       L'utilisateur choisit :
#
#           1244 -> "Cartes mères"
#
#
#   LORSQUE / WHEN :
#
#       cette categorie est stockee dans SearchQuery
#       puis que EbaySource execute la recherche.
#
#
#   ALORS / THEN :
#
#       le client eBay doit recevoir :
#
#           query       = "X570 UNIFY"
#           category_id = "1244"
#
#       et EbaySource doit retourner des objets Listing.
#
#
#   POURQUOI CE TEST ?
#
#       Les tests precedents ont valide chaque brique separement :
#
#           EbayTaxonomy
#           Category
#           SearchQuery
#           EbaySource
#           EbayClient
#
#       Ce test verifie maintenant que ces briques peuvent etre
#       enchainees dans le workflow reel de MarketMonitor.
#
# ------------------------------------------------------------------


from market_monitor.taxonomy.ebay import EbayTaxonomy
from market_monitor.search_query import SearchQuery
from market_monitor.sources.ebay import EbaySource
from market_monitor.models.listing import Listing


class FakeEbayClient:

    def __init__(self):
        self.last_query = None
        self.last_category_id = None

    # ------------------------------------------------------------------
    # Simule la reponse de l'API Taxonomy.
    # ------------------------------------------------------------------
    def get_category_suggestions(self, query):

        return {
            "categorySuggestions": [
                {
                    "category": {
                        "categoryId": "170080",
                        "categoryName": "Cartes mère: plaques arrière",
                    }
                },
                {
                    "category": {
                        "categoryId": "1244",
                        "categoryName": "Cartes mères",
                    }
                },
            ],
            "categoryTreeId": "71",
            "categoryTreeVersion": "120",
        }

    # ------------------------------------------------------------------
    # Simule ensuite la recherche Browse.
    #
    # Cette methode joue aussi le role d'espion :
    # elle memorise query et category_id.
    # ------------------------------------------------------------------
    def search(self, query, category_id=None):

        self.last_query = query
        self.last_category_id = category_id

        return {
            "itemSummaries": [
                {
                    "title": "MSI MEG X570 UNIFY",
                    "price": {
                        "value": "149.99",
                        "currency": "EUR",
                    },
                    "itemWebUrl": "https://www.ebay.fr/itm/123",
                }
            ]
        }


def test_ebay_category_selection_is_used_for_search():

    # ------------------------------------------------------------------
    # ETANT DONNE - Un faux client eBay capable de simuler
    #               Taxonomy puis Browse.
    # ------------------------------------------------------------------
    client = FakeEbayClient()

    # ------------------------------------------------------------------
    # ETANT DONNE - Le service Taxonomy utilisant ce client.
    # ------------------------------------------------------------------
    taxonomy = EbayTaxonomy(client)

    # ------------------------------------------------------------------
    # LORSQUE - Nous demandons les categories correspondant
    #           a "X570 UNIFY".
    # ------------------------------------------------------------------
    categories = taxonomy.suggest_categories(
        query="X570 UNIFY",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - L'utilisateur choisit la categorie "Cartes mères".
    #
    # Dans notre reponse fictive, il s'agit de la deuxieme suggestion.
    # ------------------------------------------------------------------
    selected_category = categories[1]

    # ------------------------------------------------------------------
    # ETANT DONNE - Cette categorie est memorisee dans SearchQuery.
    # ------------------------------------------------------------------
    search = SearchQuery(
        name="Carte mere X570",
        query="X570 UNIFY",
        category=selected_category,
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Une source eBay utilisant le meme client.
    # ------------------------------------------------------------------
    source = EbaySource(client)

    # ------------------------------------------------------------------
    # LORSQUE - La recherche est executee.
    # ------------------------------------------------------------------
    listings = source.search(search)

    # ------------------------------------------------------------------
    # ALORS - Nous avons bien choisi la categorie "Cartes mères".
    # ------------------------------------------------------------------
    assert selected_category.id == "1244"
    assert selected_category.name == "Cartes mères"

    # ------------------------------------------------------------------
    # ALORS - EbaySource a transmis la bonne recherche au client.
    # ------------------------------------------------------------------
    assert client.last_query == "X570 UNIFY"

    # ------------------------------------------------------------------
    # ALORS - La categorie choisie a traverse le workflow jusqu'au
    #         client eBay.
    # ------------------------------------------------------------------
    assert client.last_category_id == "1244"

    # ------------------------------------------------------------------
    # ALORS - Le resultat Browse a bien ete transforme en Listing.
    # ------------------------------------------------------------------
    assert len(listings) == 1
    assert isinstance(listings[0], Listing)
    assert listings[0].title == "MSI MEG X570 UNIFY"
