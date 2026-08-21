# =============================================================================
# Project     : Market Monitor
# File        : tests/clients/ebay.py
# Author      : Richalbert
# Created     : 2026-08-21
# Last Update : 
# Version     : 0.1
# Description : 
#             
# License     : MIT
#==============================================================================

from market_monitor.credentials.ebay import EbayCredentials


class EbayClient(EbayCredentials):
    
    def __init__(self, credentials: EbayCredentials):
        self.credentials = credentials
