# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/tools.py
# Author      : Richalbert
# Created     : 2026-08-16
# Last Update : 
# Version     : 0.1
# Description : fonctions diverses utilisees
# License     : MIT
#==============================================================================

def convert_price(prix_du_site: str) -> int:
    """Convertit le prix d'un site en un entier"""

    # supprime les espaces et le symbole euro
    prix = (prix_du_site.replace(" ", "")
            .replace(" ", "")
            .replace("€", "")
    )

    # supprime la partie decimale si besoin
    if "," in prix:
        prix = prix.split(",")[0]

    # converti le prix en entier
    try:
        return int(prix)
    except ValueError:
        raise ValueError(f"Impossible de convertir {prix_du_site} en entier")

def convert_date():
    pass

def clean_url():
    pass

def parse_location():
    pass