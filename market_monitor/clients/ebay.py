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

    def get_access_token(self) -> str:

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
            f"{self.credentials.client_id}:" f"{self.credentials.client_secret}"
        )

        # Conversion str -> bytes
        credentials_bytes = client_credentials.encode()

        # Encodage Base64 : retourne des bytes
        credentials_base64_bytes = base64.b64encode(credentials_bytes)

        # Conversion bytes -> str
        credentials_base64 = credentials_base64_bytes.decode()

        # Construction de la valeur du header Authorization
        return f"Basic {credentials_base64}"

    def search(
        self,
        query: str,
        access_token: str | None = None,
        category_id: str | None = None,
    ):

        if access_token is None:
            access_token = self.get_access_token()

        params = {
            "q": query,
        }

        if category_id is not None:
            params["category_ids"] = category_id

        return self.http_client.get(
            f"{self.base_url}/buy/browse/v1/item_summary/search",
            headers={
                "Authorization": f"Bearer {access_token}",
                "X-EBAY-C-MARKETPLACE-ID": "EBAY_FR",
            },
            params=params,
        )

    def get_category_suggestions(
        self,
        query: str,
        category_tree_id: str | None = None,
        access_token: str | None = None,
    ):

        if access_token is None:
            access_token = self.get_access_token()

        if category_tree_id is None:
            category_tree_id = self.get_default_category_tree_id(
                marketplace_id="EBAY_FR",
                access_token=access_token,
            )

        url = (
            f"{self.base_url}/commerce/taxonomy/v1/"
            f"category_tree/{category_tree_id}/get_category_suggestions"
        )

        return self.http_client.get(
            url,
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params={
                "q": query,
            },
        )

    def get_default_category_tree_id(
        self,
        marketplace_id: str,
        access_token: str | None = None,
    ) -> str:

        if access_token is None:
            access_token = self.get_access_token()

        response = self.http_client.get(
            f"{self.base_url}/commerce/taxonomy/v1/" "get_default_category_tree_id",
            headers={
                "Authorization": f"Bearer {access_token}",
            },
            params={
                "marketplace_id": marketplace_id,
            },
        )

        return response["categoryTreeId"]
