# =============================================================================
# Project     : Market Monitor
# File        : tests/test_ebay_client.py
# Author      : Richalbert
# Created     : 2026-08-21
# Last Update : 
# Version     : 0.1
# Description : Test TDD du client eBay qui sera appartir des
#               IDs dans.env 
#               - de passer OAuth eBay Sandbox
#               - d'obtenir des acces_token et 
#               - d'utiliser Browse API 
# License     : MIT
#==========================================================

from market_monitor.credentials.ebay import EbayCredentials
from market_monitor.clients.ebay import EbayClient

# === Test 13 ======================================
#
#   EbayClient conserve ses credentials
#
# --------------------------------------------------

def test_ebay_client_stores_credentials():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    client = EbayClient(credentials)

    assert client.credentials == credentials



# === Test 14 =====================================
#
#   EbayClient recupere l'access_token
#
# EbayClient demande un token a un composant HTTP et 
# recupere l'access_token contenu dans la reponse
#
# Et le Stub simulera la reponse HTTP d'eBay
#
# EbayClient 
#   -> appelle un client HTTP fictif
#   -> recoit une reponse contenant access_token
#   -> retourne "fake-access-token"
# ---------------------------------------------------

class StubHttpClient:

    def post(self, url, headers=None, data=None):
        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }


def test_ebay_client_gets_access_token():

    # on fixe des IDs
    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    # on appelle le Stub
    http_client = StubHttpClient()

    # on fournit au client les IDs et la requete de connection
    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    # on recupere l'access_token
    token = client.get_access_token()

    # le contrat de ce test
    assert token == "fake-access-token"

# ==================================================


# === Test 15 =================================
#
#   EbayClient utilise le bon endpoint OAuth
# 
#   Test: le client eBay utilise la bonne URL OAuth Sandbox
#
# Stub evolue en Spy
#
# EbayClient
#   -> appelle le client HTTP
#   -> a la bonne URL OAuth Sandbox
# ---------------------------------------------

class SpyHttpClient:

    def __init__(self):
        self.last_url = None

    def post(self, url, headers=None, data=None):
        self.last_url = url

        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }


def test_ebay_client_uses_oauth_sandbox_url():
        
    # on fixe des IDs
    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )
    
    # on appelle le Spy
    http_client = SpyHttpClient()

    # on fournit au client les IDs et la requete de connection
    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    # on recupere l'access_token la reponse a la requete
    token = client.get_access_token()
        
    # le contrat de ce test
    assert http_client.last_url == (
        "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    )
    assert token == "fake-access-token"


# === Test 16 =======================================
#
#   EbayClient envoie le bon Content-Type
#
# ----------------------------------------------------

class SpyHttpClient:

    def __init__(self):
        self.last_url = None
        self.last_headers = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        self.last_headers=headers

        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }

def test_ebay_client_uses_form_urlencoded_content_type():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    http_client = SpyHttpClient()

    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    token = client.get_access_token()

    # le contrat de ce test
    assert http_client.last_headers["Content-Type"] == (
        "application/x-www-form-urlencoded"
    )




# === Test 17 ===========================================
#
#   EbayClient envoie Authorization Basic correctement
#
# --------------------------------------------------------

class SpyHttpClient:

    def __init__(self):
        self.last_url = None
        self.last_headers = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        self.last_headers=headers

        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }

def test_ebay_client_uses_basic_authorization():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    http_client = SpyHttpClient()

    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    token = client.get_access_token()

    """ 
        Pour eviter une erreur de calcul a la main, on demande a Python de realiser l'encodage 
    
            python -c 'import base64; \
            print(base64.b64encode(b"fake-client-id:fake-client-secret").decode())'
    """
    assert http_client.last_headers["Authorization"] == (
        "Basic ZmFrZS1jbGllbnQtaWQ6ZmFrZS1jbGllbnQtc2VjcmV0"
    )





# === Test 18 ============================================
#
#   EbayyClient envoie le body de la requete OAuth
#   en commencant par grant_type=client_credentials
#   puis le scope
#
# ---------------------------------------------------------

class SpyHttpClient:

    def __init__(self):
        self.last_url = None
        self.last_headers = None
        self.last_data = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        self.last_headers = headers
        self.last_data = data

        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }

def test_ebay_client_uses_client_credentials_grant_type():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    http_client = SpyHttpClient()

    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    token = client.get_access_token()

    # le contrat du test
    assert http_client.last_data["grant_type"] == "client_credentials"



# === Test 19 ==================================================
#
#   La logique du scope OAuth, decrit ce que l'appli a le droit
#   de faire avec le token obtenu
#
#   scope=https://api.ebay.com/oauth/api_scope
# --------------------------------------------------------------

class SpyHttpClient:

    def __init__(self):
        self.last_url = None
        self.last_headers = None
        self.last_data = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        self.last_headers = headers
        self.last_data = data

        return {
            "access_token": "fake-access-token",
            "expires_in": 7200,
            "token_type": "Application Access Token",
        }


def test_ebay_client_uses_api_scope():

    credentials = EbayCredentials(
        client_id="fake-client-id",
        client_secret="fake-client-secret",
    )

    http_client = SpyHttpClient()

    client = EbayClient(
        credentials=credentials,
        http_client=http_client,
    )

    token = client.get_access_token()




    # le contrat du test
    assert http_client.last_data["scope"] == (
        "https://api.ebay.com/oauth/api_scope"
    )