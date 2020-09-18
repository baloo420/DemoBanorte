import requests

class identity():
    """docstring for identity."""
    def __init__(self):
        pass

    def generateToken():
        url = "https://amer-api-partner67-test.apigee.net/identity/v1/token?grant_type=client_credentials"
        payload = {}
        headers = {
          'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA=='
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        return(response.text.encode('utf8'))
