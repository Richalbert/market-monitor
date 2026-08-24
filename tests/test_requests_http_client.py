from market_monitor.http.requests_client import RequestsHttpClient

class StubResponse:

    def json(self):
        return {"access_token": "fake-access-token"}


class SpyRequests:

    def __init__(self):
        self.last_url = None

    def post(self, url, headers=None, data=None):
        self.last_url = url
        response = StubResponse()
        return response



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


def test_requests_http_client_returns_json_data():

    requests_module = SpyRequests()
    client = RequestsHttpClient(requests_module)
    result = client.post("https://example.com")

    assert result == {"access_token": "fake-access-token"}