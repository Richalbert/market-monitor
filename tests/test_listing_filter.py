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