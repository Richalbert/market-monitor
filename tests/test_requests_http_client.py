from market_monitor.http.requests_client import RequestsHttpClient

class StubResponse:

    def json(self):
        return {"access_token": "fake-access-token"}

    def raise_for_status(self):
        pass


class SpyRequests:

    def __init__(self):
        self.last_url = None
        self.last_params = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        response = StubResponse()
        return response

    def get(self, url, headers=None, params=None):
        self.last_url = url
        self.last_params= params
        return StubResponse()



# === Test 20 ==================================================
#
#   Ce test aura pour fonction de verifier que
#   RequestsHttpClient.post(...) delegue bien l'appel a
#   requests.post(...)
#
#   cad on teste l'url mais pas ce que retourne le post()
#
# ---------------------------------------------------------------


def test_requests_http_client_calls_requests_post():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)
    client.post("https://example.com")

    assert requests_module.last_url == "https://example.com"



# === Test 21 ==================================================
# 
#   RequestsHttpClient.post() recoit une reponse HTTP
#   le test transforme cette reponse en dictionnaire JSON
#
# --------------------------------------------------------------


def test_requests_http_client_returns_json_data_on_post():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)
    result = client.post("https://example.com")

    assert result == {"access_token": "fake-access-token"}



# === Test 22 ==================================================
# 
# on veut pouvoir observer si raise_for_status() a ete appele
#
# Teste la verification du status HTTP lors d'une requete POST 
# avec RequestsHttpClient
#
# --------------------------------------------------------------

class SpyResponse:

    def __init__(self):
        self.raise_for_status_called = False

    def raise_for_status(self):
        self.raise_for_status_called = True

    def json(self):
        return {
            "access_token": "fake-access-token"
        } 


def test_requests_http_client_checks_http_status_on_post():

    response = SpyResponse()

    class SpyRequestsForStatusPost:
        def post(self, url, headers=None, data=None):
            return response

    requests_module = SpyRequestsForStatusPost()
    client = RequestsHttpClient(requests_module)

    client.post("https://example.com")

    assert response.raise_for_status_called is True


# === Test 23 =========================================
#
# Ce test verifie que RequestsHttpClient appelle bien 
# la methode get()
#
# -----------------------------------------------------

def test_requests_http_client_calls_requests_get():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)
    client.get("https://example.com")

    assert requests_module.last_url == "https://example.com"


# === Test 24 ===========================================
#
# Ce test verifie que RequestsHttpClient verifie le status
# de la reponse au GET
#
# -------------------------------------------------------

def test_requests_http_client_checks_http_status_on_get():

    response = SpyResponse()

    class SpyRequestsForStatusGet:
        def get(self, url, headers=None, params=None):
            return response

    requests_module = SpyRequestsForStatusGet()
    client = RequestsHttpClient(requests_module)

    client.get("https://example.com")

    assert response.raise_for_status_called is True



# === Test 25 ==========================================
# 
#   RequestsHttpClient.get() recoit une reponse HTTP
#   le test transforme cette reponse en dictionnaire JSON
#
# ------------------------------------------------------

def test_requests_http_client_returns_json_data_on_get():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)
    result = client.get("https://example.com")

    assert result == {"access_token": "fake-access-token"}


# === Test 26 ==========================================
# 
#   Test si RequestsHttpClient.get() transmet bien les 
#   paramètres GET à requests
#
# -------------------------------------------------------

def test_requests_http_client_transmits_get_params_to_requests():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)

    client.get(
        "https://example.com",
        params={"q": "X570 UNIFY"},
    )

    assert requests_module.last_params == {"q": "X570 UNIFY"}

# === Test 27 ==========================================
# 
#   Test si RequestsHttpClient.get() transmet bien les 
#   paramètres GET à requests
#
# -------------------------------------------------------