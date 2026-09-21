#
# taxonomy/ebay.py
#


from market_monitor.categories import parse_taxonomy_response


class EbayTaxonomy:

    def __init__(self, client):
        self.client = client

    def suggest_categories(self, query: str):
        response = self.client.get_category_suggestions(
            query=query,
        )

        return parse_taxonomy_response(response)


# === Test 52 ======================================================
#
#   Comportement :
#   EbayTaxonomy transmet correctement la requete de recherche
#   au client eBay.
#
#
#   ETANT DONNE / GIVEN :
#
#       Un client eBay espion.
#
#       Ce client n'effectue aucun appel reseau.
#
#       Il memorise simplement la valeur de query recue par :
#
#           get_category_suggestions()
#
#
#   ETANT DONNE :
#
#       Une recherche :
#
#           "X570 UNIFY"
#
#
#   LORSQUE / WHEN :
#
#       EbayTaxonomy.suggest_categories() est appelee avec
#       cette recherche.
#
#
#   ALORS / THEN :
#
#       EbayClient doit avoir recu exactement :
#
#           "X570 UNIFY"
#
#
#   POURQUOI CE TEST ?
#
#       Le test 51 verifie le resultat produit par EbayTaxonomy.
#
#       Le test 52 verifie maintenant la collaboration entre :
#
#           EbayTaxonomy
#               ↓
#           EbayClient
#
#       Nous voulons garantir que la requete de l'utilisateur
#       n'est ni modifiee ni perdue entre les deux couches.
#
# ------------------------------------------------------------------


class SpyEbayClient:

    def __init__(self):
        self.last_query = None

    def get_category_suggestions(self, query):

        # --------------------------------------------------------------
        # Le Spy memorise la requete recue.
        # --------------------------------------------------------------
        self.last_query = query

        # --------------------------------------------------------------
        # Il retourne ensuite une reponse Taxonomy valide afin que
        # EbayTaxonomy puisse terminer normalement son travail.
        # --------------------------------------------------------------
        return {
            "categorySuggestions": [],
            "categoryTreeId": "71",
            "categoryTreeVersion": "120",
        }


def test_ebay_taxonomy_transmits_query_to_client():

    # ------------------------------------------------------------------
    # ETANT DONNE - Un client eBay espion.
    # ------------------------------------------------------------------
    client = SpyEbayClient()

    # ------------------------------------------------------------------
    # ETANT DONNE - EbayTaxonomy utilisant ce client.
    # ------------------------------------------------------------------
    taxonomy = EbayTaxonomy(client)

    # ------------------------------------------------------------------
    # LORSQUE - Nous demandons les categories correspondant
    #           a "X570 UNIFY".
    # ------------------------------------------------------------------
    taxonomy.suggest_categories(
        query="X570 UNIFY",
    )

    # ------------------------------------------------------------------
    # ALORS - Le client eBay doit avoir recu exactement cette requete.
    # ------------------------------------------------------------------
    assert client.last_query == "X570 UNIFY"
