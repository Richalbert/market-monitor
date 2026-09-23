# est une annonce pertinente
def is_relevant_listing(
    listing,
    include_terms=None,
    exclude_terms=None,
):

    # --------------------------------------------------------------
    # L'ancienne regle reste valable :
    # une plaque I/O Shield n'est pas une annonce pertinente.
    # --------------------------------------------------------------
    if "I/O Shield" in listing.title:
        return False

    # --------------------------------------------------------------
    # Si une liste de termes exclus est fournie,
    # la presence d'un seul de ces termes suffit pour rejeter
    # l'annonce.
    # --------------------------------------------------------------
    if exclude_terms is not None:
        if any(term in listing.title for term in exclude_terms):
            return False

    # --------------------------------------------------------------
    # Si aucun terme d'inclusion n'est fourni,
    # on ne rajoute aucune restriction positive.
    # --------------------------------------------------------------
    if include_terms is None:
        return True

    # --------------------------------------------------------------
    # Si des termes d'inclusion sont fournis,
    # au moins un doit etre present dans le titre.
    #
    # any(...) implemente ici notre logique OU.
    # --------------------------------------------------------------
    return any(term in listing.title for term in include_terms)


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
#
#       car aucun des termes :
#
#           "X570"
#           "B550"
#
#       n'est present dans le titre.
#
#
#   REGLE METIER PROTEGEE :
#
#       include_terms fonctionne avec une logique OU :
#
#           X570 OU B550
#
#       mais au moins une condition doit etre vraie.
#
#       Si toutes sont fausses :
#
#           False OU False -> False
#
# ------------------------------------------------------------------
def test_listing_is_not_relevant_when_no_included_term_matches():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce dont le titre ne contient aucun
    #               des termes recherches.
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
    # ALORS - L'annonce doit etre rejetee car aucun terme ne correspond.
    # ------------------------------------------------------------------
    assert relevant is False
