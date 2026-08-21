# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/credentials/ebay.py
# Author      : Richalbert
# Created     : 2026-08-16
# Last Update : 
# Version     : 0.1
# Description : La classe EbayCredentieals qui recoit les IDs eBay
# License     : MIT
#==============================================================================

from dataclasses import dataclass

@dataclass
class EbayCredentials:
    client_id: str
    client_secret: str