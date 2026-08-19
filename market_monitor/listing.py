# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/listing.py
# Author      : Richalbert
# Created     : 2026-08-16
# Last Update : 
# Version     : 0.1
# Description : La classe Listing : represente une annonce trouvee
# License     : MIT
#==============================================================================

from dataclasses import dataclass


@dataclass
class Listing:
    title: str
    price: int
    url: str
    source: str
