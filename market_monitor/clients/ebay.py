# =============================================================================
# Project     : Market Monitor
# File        : market_monitor/clients/ebay.py
# Author      : Richalbert
# Created     : 2026-08-21
# Last Update : 
# Version     : 0.1
# Description : 
#             
# License     : MIT
# ==============================================================================

from market_monitor.credentials.ebay import EbayCredentials

import base64

class EbayClient:
    
    def __init__(
        self, 
        credentials: EbayCredentials,
        http_client=None,
        base_url="https://api.sandbox.ebay.com",
    ):
        self.credentials = credentials
        self.http_client = http_client
        self.base_url = base_url


    def get_access_token(self)-> str:

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self._build_authorization_header(),
        }

        data = {
            "grant_type": "client_credentials",
            "scope": "https://api.ebay.com/oauth/api_scope",
        }

        response = self.http_client.post(
            f"{self.base_url}/identity/v1/oauth2/token",
            headers=headers,
            data=data,
        )

        return response["access_token"]

    def _build_authorization_header(self) -> str:

        # Construction des identifiants client_id:client_secret
        client_credentials = (
            f"{self.credentials.client_id}:"
            f"{self.credentials.client_secret}"
        )

        # Conversion str -> bytes
        credentials_bytes = client_credentials.encode()

        # Encodage Base64 : retourne des bytes
        credentials_base64_bytes = base64.b64encode(credentials_bytes)

        # Conversion bytes -> str
        credentials_base64 = credentials_base64_bytes.decode()

        # Construction de la valeur du header Authorization
        return f"Basic {credentials_base64}"

    def search(self, query: str, access_token: str):
        return self.http_client.get(
            f"{self.base_url}/buy/browse/v1/item_summary/search",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-EBAY-C-MARKETPLACE-ID": "EBAY_FR",
            },
            params={"q": query},
        )
