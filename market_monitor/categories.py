
# =============================================================================
# Project     : Market Monitor
# File        : market-monitor/categories.py
# Author      : Richalbert
# Created     : 2026-09-15
# Last Update : 
# Version     : 0.1
# Description : 
#             
# License     : MIT
#==============================================================================
from market_monitor.models.category import Category

# conversion d'une suggestion en Category
def parse_category_suggestion(suggestion):
    category = suggestion["category"]

    return Category(
        id=category["categoryId"],
        name=category["categoryName"],
    )

# conversion de plusieurs suggestions en une liste de Category
def parse_category_suggestions(suggestions):
    results = []

    for suggestion in suggestions:
        category = parse_category_suggestion(suggestion)
        results.append(category)

    return results

# reponse eBay -> list[Category]
def parse_taxonomy_response(response):
    suggestions = response["categorySuggestions"]

    return parse_category_suggestions(suggestions)