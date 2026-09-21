#
#   tests/test_ebay_taxonomy.py
#

from market_monitor.taxonomy.ebay import EbayTaxonomy


# === Test 51 ======================================================
#
#   Comportement :
#   EbayTaxonomy transforme les suggestions brutes de l'API eBay
#   en objets Category utilisables par MarketMonitor.
#
#
#   ETANT DONNE / GIVEN :
#
#       Un client eBay fictif qui, pour la recherche :
#
#           "X570 UNIFY"
#
#       retourne la reponse Taxonomy suivante :
#
#           170080 -> "Cartes mère: plaques arrière"
#           1244   -> "Cartes mères"
#
#
#   LORSQUE / WHEN :
#
#       EbayTaxonomy demande les categories correspondant
#       a la recherche "X570 UNIFY".
#
#
#   ALORS / THEN :
#
#       MarketMonitor doit obtenir deux objets Category :
#
#           Category(
#               id="170080",
#               name="Cartes mère: plaques arrière",
#           )
#
#           Category(
#               id="1244",
#               name="Cartes mères",
#           )
#
#
#   POURQUOI CE TEST ?
#
#       EbayClient travaille avec le format JSON propre a eBay.
#
#       Le reste de MarketMonitor doit travailler avec ses propres
#       objets metier, ici Category.
#
#       EbayTaxonomy constitue donc la frontiere entre ces deux mondes.
#
# ------------------------------------------------------------------


class StubEbayClient:

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


def test_ebay_taxonomy_returns_categories():

    # ------------------------------------------------------------------
    # ETANT DONNE - Un faux client eBay.
    #
    # Il ne contacte pas Internet.
    # Il retourne une reponse Taxonomy connue et controlee.
    # ------------------------------------------------------------------
    client = StubEbayClient()

    # ------------------------------------------------------------------
    # ETANT DONNE - Le composant EbayTaxonomy utilisant ce client.
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
    # ALORS - Deux categories doivent etre obtenues.
    # ------------------------------------------------------------------
    assert len(categories) == 2

    # ------------------------------------------------------------------
    # ALORS - La premiere suggestion eBay est correctement transformee.
    # ------------------------------------------------------------------
    assert categories[0].id == "170080"
    assert categories[0].name == "Cartes mère: plaques arrière"

    # ------------------------------------------------------------------
    # ALORS - La seconde suggestion eBay est correctement transformee.
    # ------------------------------------------------------------------
    assert categories[1].id == "1244"
    assert categories[1].name == "Cartes mères"
