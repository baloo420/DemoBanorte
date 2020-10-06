<<<<<<< HEAD
import requests
import json
import datetime
from demobanorte.Apps.apicall.models import ParametrosUser

def identity():
    print("Entreaqui")
    #TokenApp = GenerateAccessTokenApigee()
    #LinkRedirect = CreateAccountAccesConsent(TokenApp)

def GenerateAccessTokenApigee():
    url = "https://amer-api-partner67-test.apigee.net/identity/v1/token?grant_type=client_credentials"
    payload = {}
    headers = {
      'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA=='
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    prueba = response.json()
    TokenApp = prueba['access_token']
    return(TokenApp)

def CreateAccountAccesConsent(TokenApp):

    url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1"

    payload = "{\n    \"Data\": {\n        \"TransactionToDateTime\": \"2020-09-18T17:00:49-05:00\",\n        \"ExpirationDateTime\": \"2020-10-03T17:00:49-05:00\",\n        \"Permissions\": [\n            \"ReadAccountsBasic\",\n            \"ReadAccountsDetail\",\n            \"ReadBalances\",\n            \"ReadTransactionsBasic\",\n            \"ReadTransactionsDebits\",\n            \"ReadTransactionsDetail\"\n        ],\n        \"TransactionFromDateTime\": \"2020-09-18T17:00:49-05:00\"\n    }\n}"
    headers = {
      'Authorization': 'Bearer '+TokenApp,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    prueba = response.json()
    return(prueba)
=======
import requests
import json
import datetime
from demobanorte.Apps.apicall.models import ParametrosUser

def identity():
    print("Entreaqui")
    #TokenApp = GenerateAccessTokenApigee()
    #LinkRedirect = CreateAccountAccesConsent(TokenApp)

def GenerateAccessTokenApigee():
    url = "https://amer-api-partner67-test.apigee.net/identity/v1/token?grant_type=client_credentials"
    payload = {}
    headers = {
      'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA=='
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    prueba = response.json()
    TokenApp = prueba['access_token']
    return(TokenApp)

def CreateAccountAccesConsent(TokenApp):

    url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1"

    payload = "{\n    \"Data\": {\n        \"TransactionToDateTime\": \"2020-09-18T17:00:49-05:00\",\n        \"ExpirationDateTime\": \"2020-10-03T17:00:49-05:00\",\n        \"Permissions\": [\n            \"ReadAccountsBasic\",\n            \"ReadAccountsDetail\",\n            \"ReadBalances\",\n            \"ReadTransactionsBasic\",\n            \"ReadTransactionsDebits\",\n            \"ReadTransactionsDetail\"\n        ],\n        \"TransactionFromDateTime\": \"2020-09-18T17:00:49-05:00\"\n    }\n}"
    headers = {
      'Authorization': 'Bearer '+TokenApp,
      'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    prueba = response.json()
    return(prueba)
>>>>>>> 5a28afeafdb6503d5350fa1d8071ad7d096d13aa
