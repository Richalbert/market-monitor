
# la classe RequestsHttpClient
#   -> utilise la bibliotheque requests
#   -> recupere Response
#   -> appelle .json()
#   -> retourne le dictionnaire
class RequestsHttpClient:
  
    def __init__(self, requests_module):
        self.requests_module = requests_module

    def post(self, url, headers=None, data=None):
        response = self.requests_module.post(
            url,
            headers=headers,
            data=data,
        )
        return response.json()