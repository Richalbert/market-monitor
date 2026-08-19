# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/search_query.py
# Author      : Richalbert
# Created     : 2026-08-18
# Last Update : 
# Version     : 0.1
# Description : La classe SearchQuery : decrit ce qu'on cherche
# License     : MIT
#==============================================================================

from dataclasses import dataclass


@dataclass
class SearchQuery:
    name: str
    query: str
