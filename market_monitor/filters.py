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
        if any(term.casefold() in listing.title.casefold() for term in exclude_terms):
            return False

    # --------------------------------------------------------------
    # Si aucun terme d'inclusion n'est fourni,
    # on ne rajoute aucune restriction positive.
    # --------------------------------------------------------------
    if not include_terms:
        return True

    # --------------------------------------------------------------
    # Si des termes d'inclusion sont fournis,
    # au moins un doit etre present dans le titre.
    #
    # any(...) implemente ici notre logique OU.
    # --------------------------------------------------------------
    return any(term.casefold() in listing.title.casefold() for term in include_terms)
