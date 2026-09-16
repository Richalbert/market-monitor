# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/models/category.py
# Author      : Richalbert
# Created     : 2026-08-16
# Last Update : 
# Version     : 0.1
# Description : La classe Category : represente la categorie a chercher la 
#               requete dedans
# License     : MIT
#==============================================================================

from dataclasses import dataclass


@dataclass
class Category:
    id: str
    name: str