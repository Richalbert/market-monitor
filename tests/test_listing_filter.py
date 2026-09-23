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


# === Test 57 ======================================================
#
#   Comportement :
#   La recherche des termes inclus dans le titre d'une annonce
#   est insensible aux majuscules et aux minuscules.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce dont le titre contient :
#
#           "X570"
#
#       en majuscules :
#
#           "MSI MEG X570 UNIFY AM4 ATX"
#
#       et un terme inclus ecrit en minuscules :
#
#           "x570"
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit etre consideree comme pertinente.
#
#
#   POURQUOI CE TEST ?
#
#       Pour la pertinence d'une annonce :
#
#           "X570"
#           "x570"
#
#       representent le meme terme.
#
#       La casse ne doit donc pas modifier le resultat
#       du filtrage.
#
#
#   REGLE METIER INTRODUITE :
#
#       La comparaison des include_terms avec le titre
#       est insensible a la casse.
#
# ------------------------------------------------------------------
def test_included_term_matching_is_case_insensitive():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce contenant "X570" en majuscules.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY AM4 ATX",
        price=149.99,
        url="https://www.ebay.fr/itm/123",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Le meme terme, mais ecrit en minuscules.
    # ------------------------------------------------------------------
    include_terms = [
        "x570",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        include_terms=include_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - La difference de casse ne doit pas provoquer de rejet.
    # ------------------------------------------------------------------
    assert relevant is True


# === Test 58 ======================================================
#
#   Comportement :
#   La recherche des termes exclus dans le titre d'une annonce
#   est insensible aux majuscules et aux minuscules.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce dont le titre contient :
#
#           "BROKEN"
#
#       en majuscules :
#
#           "MSI MEG X570 UNIFY BROKEN"
#
#       et un terme exclu ecrit en minuscules :
#
#           "broken"
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
#   POURQUOI CE TEST ?
#
#       Pour une exclusion :
#
#           "BROKEN"
#           "broken"
#
#       representent le meme terme.
#
#       La casse ne doit donc pas modifier le comportement
#       du filtre.
#
#
#   REGLE METIER PROTEGEE :
#
#       La comparaison des exclude_terms avec le titre
#       est insensible a la casse.
#
# ------------------------------------------------------------------
def test_excluded_term_matching_is_case_insensitive():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce contenant "BROKEN" en majuscules.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY BROKEN",
        price=99.99,
        url="https://www.ebay.fr/itm/789",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Le meme terme exclu, mais ecrit en minuscules.
    # ------------------------------------------------------------------
    exclude_terms = [
        "broken",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - La difference de casse ne doit pas empecher l'exclusion.
    # ------------------------------------------------------------------
    assert relevant is False


# === Test 59 ======================================================
#
#   Comportement :
#   Une liste include_terms vide ne doit pas rejeter une annonce.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY AM4 ATX"
#
#       et aucune regle d'inclusion supplementaire :
#
#           include_terms = []
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit rester pertinente.
#
#
#   POURQUOI CE TEST ?
#
#       include_terms n'est pas la requete de recherche.
#
#       La recherche a deja ete effectuee par eBay avec par exemple :
#
#           query = "X570 UNIFY"
#           category_id = "1244"
#
#       Une liste vide signifie simplement :
#
#           "aucun filtre positif supplementaire"
#
#       Elle doit donc avoir le meme effet que :
#
#           include_terms = None
#
#
#   REGLE METIER PROTEGEE :
#
#       None -> pas de filtre d'inclusion
#       []   -> pas de filtre d'inclusion
#
# ------------------------------------------------------------------
def test_empty_include_terms_does_not_reject_listing():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce valide.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY AM4 ATX",
        price=149.99,
        url="https://www.ebay.fr/itm/123",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Aucune regle positive supplementaire.
    # ------------------------------------------------------------------
    include_terms = []

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        include_terms=include_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - Une liste vide ne doit pas provoquer le rejet.
    # ------------------------------------------------------------------
    assert relevant is True


# === Test 60 ======================================================
#
#   Comportement :
#   Une liste exclude_terms vide ne doit pas rejeter une annonce.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY AM4 ATX"
#
#       et aucune regle d'exclusion :
#
#           exclude_terms = []
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit rester pertinente.
#
#
#   POURQUOI CE TEST ?
#
#       exclude_terms n'est pas la recherche elle-meme.
#
#       Une liste vide signifie simplement :
#
#           "aucun terme supplementaire a exclure"
#
#       Elle doit donc avoir le meme effet que :
#
#           exclude_terms = None
#
#
#   REGLE METIER PROTEGEE :
#
#       None -> aucune exclusion
#       []   -> aucune exclusion
#
# ------------------------------------------------------------------
def test_empty_exclude_terms_does_not_reject_listing():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce valide.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY AM4 ATX",
        price=149.99,
        url="https://www.ebay.fr/itm/123",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Aucune regle negative supplementaire.
    # ------------------------------------------------------------------
    exclude_terms = []

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - Une liste vide ne doit pas provoquer le rejet.
    # ------------------------------------------------------------------
    assert relevant is True


#
# === Test 61 ======================================================
#
#   Comportement :
#   Des termes d'exclusion qui ne correspondent pas au titre
#   ne doivent pas provoquer le rejet de l'annonce.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY AM4 ATX"
#
#       et plusieurs termes d'exclusion :
#
#           "broken"
#           "damaged"
#           "for parts"
#
#       dont aucun n'apparait dans le titre.
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit rester pertinente.
#
#
#   POURQUOI CE TEST ?
#
#       La presence de termes dans exclude_terms ne signifie pas
#       que toutes les annonces doivent etre rejetees.
#
#       Le rejet doit avoir lieu uniquement si au moins un terme
#       exclu correspond effectivement au titre.
#
#
#   REGLE METIER PROTEGEE :
#
#       Aucun terme exclu ne correspond
#           -> pas de veto
#           -> l'annonce continue normalement son evaluation.
#
# ------------------------------------------------------------------
def test_non_matching_exclude_terms_do_not_reject_listing():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce qui ne contient aucun terme interdit.
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY AM4 ATX",
        price=149.99,
        url="https://www.ebay.fr/itm/123",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Plusieurs termes d'exclusion sans correspondance.
    # ------------------------------------------------------------------
    exclude_terms = [
        "broken",
        "damaged",
        "for parts",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - Aucun veto n'a ete trouve.
    # ------------------------------------------------------------------
    assert relevant is True


# === Test 62 ======================================================
#
#   Comportement :
#   Si au moins un terme parmi plusieurs exclude_terms correspond
#   au titre, l'annonce doit etre rejetee.
#
#
#   ETANT DONNE / GIVEN :
#
#       Une annonce :
#
#           "MSI MEG X570 UNIFY DAMAGED"
#
#       et plusieurs termes d'exclusion :
#
#           "broken"
#           "damaged"
#           "for parts"
#
#       Le premier terme ne correspond pas.
#       Le deuxieme terme correspond.
#       Le troisieme n'a donc pas besoin de correspondre.
#
#
#   LORSQUE / WHEN :
#
#       MarketMonitor evalue la pertinence de cette annonce.
#
#
#   ALORS / THEN :
#
#       l'annonce doit etre rejetee.
#
#
#   POURQUOI CE TEST ?
#
#       exclude_terms fonctionne comme une liste de vetos.
#
#       Il n'est pas necessaire que tous les termes correspondent.
#
#       Une seule correspondance suffit :
#
#           broken    -> False
#           damaged   -> True
#           for parts -> peu importe
#
#       donc :
#
#           False OR True OR ...
#               -> True
#               -> veto
#               -> annonce rejetee
#
#
#   REGLE METIER PROTEGEE :
#
#       exclude_terms utilise une logique OU :
#
#       au moins un terme exclu correspond
#           -> annonce rejetee.
#
# ------------------------------------------------------------------
def test_one_matching_exclude_term_rejects_listing():

    # ------------------------------------------------------------------
    # ETANT DONNE - Une annonce contenant "DAMAGED".
    # ------------------------------------------------------------------
    listing = Listing(
        title="MSI MEG X570 UNIFY DAMAGED",
        price=99.99,
        url="https://www.ebay.fr/itm/789",
        source="ebay",
    )

    # ------------------------------------------------------------------
    # ETANT DONNE - Plusieurs exclusions dont seule l'une correspond.
    # ------------------------------------------------------------------
    exclude_terms = [
        "broken",
        "damaged",
        "for parts",
    ]

    # ------------------------------------------------------------------
    # LORSQUE - Le filtre evalue l'annonce.
    # ------------------------------------------------------------------
    relevant = is_relevant_listing(
        listing,
        exclude_terms=exclude_terms,
    )

    # ------------------------------------------------------------------
    # ALORS - Une seule correspondance suffit pour exercer le veto.
    # ------------------------------------------------------------------
    assert relevant is False
