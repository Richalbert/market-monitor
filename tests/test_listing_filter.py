from market_monitor.models.listing import Listing
from market_monitor.filters import is_relevant_listing


# === Test 34 ======================================================
#
#   Une annonce d'accessoire ne doit pas etre consideree pertinente
#
# ------------------------------------------------------------------
def test_listing_with_io_shield_is_not_relevant():

    listing = Listing(
        title="OEM I/O Shield For MSI MEG X570 UNIFY Motherboard Backplate IO",
        price=19.36,
        url="https://www.ebay.fr/itm/396052469502",
        source="ebay",
    )

    assert is_relevant_listing(listing) is False


# === Test 54 ======================================================
#
#   Comportement :
#   Une annonce est pertinente lorsqu'au moins un des termes
#   inclus apparait dans son titre.
#
#
#   CONTEXTE :
#
#       Le filtrage par categorie eBay constitue notre premier niveau
#       de selection.
#
#       Mais meme dans une categorie correcte, nous pouvons vouloir
#       affiner les resultats avec des termes presents dans le titre.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY AM4 ATX"
#
#       et une liste de termes inclus :
#
#           ["X570", "B550"]
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit etre consideree pertinente,
#
#       car au moins un terme de la liste :
#
#           "X570"
#
#       est present dans le titre.
#
#
#   REGLE METIER INTRODUITE :
#
#       include_terms utilise une logique OU :
#
#           terme 1 OU terme 2 OU terme 3 ...
#
#       Un seul terme correspondant suffit.
#
# ------------------------------------------------------------------
def test_listing_is_relevant_when_one_included_term_matches():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce appartenant au produit recherche.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY AM4 ATX",
        price=149.99,
        url="https://www.ebay.fr/itm/123",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Plusieurs termes acceptables.
    #
    # "X570" est present dans le titre.
    # "B550" ne l'est pas.
    #
    # Comme notre regle est "au moins un", le resultat attendu
    # reste True.
    # ------------------------------------------------------------------
    include_terms = [
        "X570",
        "B550",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce avec les termes inclus.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        include_terms=include_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - L'annonce est pertinente car "X570" correspond.
    # ------------------------------------------------------------------
    assert relevant is True


# === Test 55 ======================================================
#
#   Comportement :
#   Une annonce n'est pas pertinente lorsqu'aucun des termes
#   inclus n'apparait dans son titre.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "ASUS ROG STRIX Z790 HERO"
#
#       et une liste de termes inclus :
#
#           ["X570", "B550"]
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit etre consideree comme non pertinente,
#       car aucun terme inclus n'apparait dans le titre.
#
# ------------------------------------------------------------------
def test_listing_is_not_relevant_when_no_included_term_matches():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce sans aucun terme recherche.
    # ------------------------------------------------------------------
    listing = Listing(
        title="ASUS ROG STRIX Z790 HERO",
        price=299.99,
        url="https://www.ebay.fr/itm/456",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Les termes acceptables pour notre surveillance.
    # ------------------------------------------------------------------
    include_terms = [
        "X570",
        "B550",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        include_terms=include_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - Aucun terme ne correspond : l'annonce est rejetee.
    # ------------------------------------------------------------------
    assert relevant is False


# === Test 56 ======================================================
#
#   Comportement :
#   Une annonce contenant un terme exclu n'est pas pertinente,
#   meme si elle contient egalement un terme inclus.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY BROKEN"
#
#       avec :
#
#           include_terms = ["X570"]
#           exclude_terms = ["BROKEN"]
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit etre consideree comme non pertinente.
#
#
#   POURQUOI ?
#
#       "X570" correspond bien a un terme inclus :
#
#           include -> True
#
#       mais "BROKEN" correspond a un terme exclu :
#
#           exclude -> True
#
#       Une exclusion est prioritaire :
#
#           include=True + exclude=True
#                       ↓
#                     False
#
#
#   REGLE METIER INTRODUITE :
#
#       Si au moins un terme exclu apparait dans le titre,
#       l'annonce est rejetee.
#
# ------------------------------------------------------------------
def test_listing_is_not_relevant_when_excluded_term_matches():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce qui contient a la fois
    #               un terme souhaite et un terme interdit.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY BROKEN",
        price=99.99,
        url="https://www.ebay.fr/itm/789",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Un terme positif.
    # ------------------------------------------------------------------
    include_terms = [
        "X570",
    ]

    # ------------------------------------------------------------------
    # ETANT DONNE - Un terme qui doit provoquer le rejet.
    # ------------------------------------------------------------------
    exclude_terms = [
        "BROKEN",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce avec les deux regles.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        include_terms=include_terms,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - L'exclusion doit avoir priorite sur l'inclusion.
    # ------------------------------------------------------------------
    assert relevant is False
