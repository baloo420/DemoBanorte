<<<<<<< HEAD
import requests
import json
import datetime
from demobanorte.Apps.apicall.models import cuentasUsuario
from django.http import HttpResponse
from django.contrib.auth.models import User
from demobanorte.Apps.apicall.models import DetallesCuenta, DetalleConsent, DetalleTransaccion, procesocta
#####Flujo inicial
def logincnbv(code, state):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    client_id = 'z104dwltrg5e2cteoskjy5j2f20w0pte5cex3k0z'
    client_secret = '3syhvkffzxwtbc32rupxxraupx0iflwjsa4qf5u5'
# Se obtiene el Access Token para las operaciones
    url = "https://oauth2.ofpilot.com/hydra-public/oauth2/token"

    payload = 'grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https%3A//127.0.0.1%3A8000/redirect/'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'oauth2_authentication_csrf=MTYwMTkzMDQ2N3xEdi1CQkFFQ180SUFBUkFCRUFBQVB2LUNBQUVHYzNSeWFXNW5EQVlBQkdOemNtWUdjM1J5YVc1bkRDSUFJRGRqTmpFMFlUSmxZVGRtWXpRME0yTTVNREEwTXpFMFlUVmhaakV4WXpGbXyYQXMOqEMA7vX-n-hOsUszVLGKwsXzu6iBDnYDTWHGvg=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    #print(response.text.encode('utf8'))
    respuesta = response.json()
    Access_Token = respuesta['access_token']
    id_token = respuesta['id_token']
    refresh_token = respuesta['refresh_token']
    scope = respuesta['scope']
#En esta parte obtenemos las cuentas del usuario
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+Access_Token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    for Informacion in pruebaload["Data"]["Account"]:
        Nocuenta = Informacion['AccountId']
        Nickname = Informacion['Nickname']
        Currency = Informacion['Currency']
        Status = Informacion['Status']
        institucion = Informacion['Servicer']['Identification']
        r = cuentasUsuario(
        cuenta_numero = Nocuenta,
        cuenta_user = Cliente_id,
        cuenta_institucion = institucion,
        cuenta_nickname = Nickname,
        cuenta_currency = Currency,
        cuenta_status = Status,
        cuenta_id_token = id_token,
        cuenta_scope = scope
        )
        r.save()
    s = procesocta(
    proceso_user = Cliente_id,
    proceso_token = Access_Token,
    proceso_refresh_token = refresh_token,
    proceso_inst_inf = 'CNBV',
    proceso_cod_inst = institucion
    )
    s.save()

def getSaldo(cuenta, cod_institucion):
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cod_institucion, proceso_inst_inf='CNBV')
    token = DatosProceso.proceso_token
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta+"/balances"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        for Informacion in pruebaload["Data"]["Balance"]:
            Monto = Informacion["Amount"]['amount']
        return(Monto)
    else:
        return('NoOK')

def DetalleCuenta(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='CNBV')
    token = DatosProceso.proceso_token

    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta

    payload  = {}
    headers = {
      'Authorization': 'Bearer '+token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    RegistrosCta = []
    for entry in pruebaload["Data"]["Account"]:
        RegistrosCta.append(DetallesCuenta(entry['AccountId'], entry['Status'], entry['StatusUpdateDateTime'], entry['Currency'], entry['AccountType'], entry['AccountSubType'], entry['AccountIndicator'], entry['OnboardingType'], entry['Nickname'], entry['OpeningDate'], entry['Servicer']['SchemeName'], entry['Servicer']['Identification']))
    return(RegistrosCta)

def DetalleConsentimiento(cuenta):
######Obtiene el acces consents
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='CNBV')
    token = DatosProceso.proceso_token

    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents"

    payload = "{  \"Data\":{    \"TransactionToDateTime\":\"2020-10-23T06:44:05.618Z\",    \"ExpirationDateTime\":\"2021-10-23T06:44:05.618Z\",    \"Permissions\":[\"ReadAccountsBasic\",\"ReadAccountsDetail\",\"ReadBalances\",\"ReadTransactionsBasic\",\"ReadTransactionsDebits\",\"ReadTransactionsDetail\"],    \"TransactionFromDateTime\":\"2020-10-23T06:44:05.618Z\"  }}"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+token,
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    respuesta = response.json()
    Data = respuesta['Data']
    Consent = Data['ConsentId']
####se obtiene el detalle

    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents/"+Consent

    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+token,
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)

    DetallesCon = []
    DetallesCon.append(DetalleConsent(pruebaload["Data"]['CreationDateTime'], pruebaload["Data"]['ExpirationDateTime'], pruebaload["Data"]['ConsentId'], pruebaload["Data"]['Status'],pruebaload["Data"]['Permissions']))
    return(DetallesCon)

def DevTransacciones(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='CNBV')
    token = DatosProceso.proceso_token

    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta+"/transactions"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    Transaccionesdeta = []
    for entry in pruebaload["Data"]["Transaction"]:
        Transaccionesdeta.append(DetalleTransaccion(entry['TransactionId'], entry['Status'], entry['BookingDateTime'], entry['TransactionInformation'], entry['Amount']['Amount'], entry['Amount']['Currency']))
    return(Transaccionesdeta)

def EliminaConsent(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='CNBV')
    token = DatosProceso.proceso_token

    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents/"+consentid

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("DELETE", url, headers=headers, data = payload)
    
    for entry in cuentaUsuario:
        entry.delete()

def refrescarToken(client_user):
    client_id = 'z104dwltrg5e2cteoskjy5j2f20w0pte5cex3k0z'
    client_secret = '3syhvkffzxwtbc32rupxxraupx0iflwjsa4qf5u5'
    TokenAActualizar = procesocta.objects.all().filter(proceso_user=client_user, proceso_inst_inf='CNBV')
    for entry in TokenAActualizar:
        tokenRefresh = entry.proceso_refresh_token
        url = "https://oauth2.ofpilot.com/hydra-public/oauth2/token"

        payload = 'grant_type=refresh_token&refresh_token='+tokenRefresh+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https%3A//127.0.0.1%3A8000/redirect/'
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': 'oauth2_authentication_csrf=MTYwMTkzMDQ2N3xEdi1CQkFFQ180SUFBUkFCRUFBQVB2LUNBQUVHYzNSeWFXNW5EQVlBQkdOemNtWUdjM1J5YVc1bkRDSUFJRGRqTmpFMFlUSmxZVGRtWXpRME0yTTVNREEwTXpFMFlUVmhaakV4WXpGbXyYQXMOqEMA7vX-n-hOsUszVLGKwsXzu6iBDnYDTWHGvg=='
        }
        response = requests.request("POST", url, headers=headers, data = payload)

        respuesta = response.json()
        Access_Token = respuesta['access_token']
        id_token = respuesta['id_token']
        refresh_token = respuesta['refresh_token']
        entry.proceso_token = Access_Token
        entry.proceso_refresh_token = refresh_token
        entry.save()
=======
import requests
import json
import datetime
from demobanorte.Apps.apicall.models import cuentasUsuario
from django.http import HttpResponse
from django.contrib.auth.models import User
from demobanorte.Apps.apicall.models import DetallesCuenta, DetalleConsent, DetalleTransaccion
#####Flujo inicial
def logincnbv(code, state):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    client_id = 'z104dwltrg5e2cteoskjy5j2f20w0pte5cex3k0z'
    client_secret = '3syhvkffzxwtbc32rupxxraupx0iflwjsa4qf5u5'
# Se obtiene el Access Token para las operaciones
    url = "https://oauth2.ofpilot.com/hydra-public/oauth2/token"

    payload = 'grant_type=authorization_code&code='+code+'&client_id='+client_id+'&client_secret='+client_secret+'&redirect_uri=https%3A//127.0.0.1%3A8000/redirect/'
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'oauth2_authentication_csrf=MTYwMTkzMDQ2N3xEdi1CQkFFQ180SUFBUkFCRUFBQVB2LUNBQUVHYzNSeWFXNW5EQVlBQkdOemNtWUdjM1J5YVc1bkRDSUFJRGRqTmpFMFlUSmxZVGRtWXpRME0yTTVNREEwTXpFMFlUVmhaakV4WXpGbXyYQXMOqEMA7vX-n-hOsUszVLGKwsXzu6iBDnYDTWHGvg=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    #print(response.text.encode('utf8'))
    respuesta = response.json()
    Access_Token = respuesta['access_token']
    id_token = respuesta['id_token']
    refresh_token = respuesta['refresh_token']
    scope = respuesta['scope']
    print('Authorization: Bearer '+Access_Token+',')
#En esta parte obtenemos las cuentas del usuario
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+Access_Token,
      'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    for Informacion in pruebaload["Data"]["Account"]:
        Nocuenta = Informacion['AccountId']
        Nickname = Informacion['Nickname']
        Currency = Informacion['Currency']
        Status = Informacion['Status']
        institucion = Informacion['Servicer']['Identification']
        r = cuentasUsuario(
        cuenta_numero = Nocuenta,
        cuenta_user = Cliente_id,
        cuenta_token = Access_Token,
        cuenta_institucion = institucion,
        cuenta_nickname = Nickname,
        cuenta_currency = Currency,
        cuenta_status = Status,
        cuenta_Refresh_token = refresh_token,
        cuenta_id_token = id_token,
        cuenta_scope = scope
        )
        r.save()

def comisionNacional(usuario,password,institucion):
    TokenApp = directlogin(usuario,password)
    CreaAccesConsent(TokenApp,institucion,usuario)
#####Obtiene el token para poder realizar las solicitudes
def directlogin(usuario,password):
  url = "https://apisandbox.ofpilot.com/my/logins/direct"

  payload = {}
  headers = {
    'Content-Type': 'application/json  ',
    'Authorization': 'DirectLogin username='+usuario+',password='+password+',consumer_key=gu3fslufxhkwogpnks0r1mzlhuqi053yoimhjcvb',
    'Cookie': 'JSESSIONID=dku1uxd4wixj1bkqsb9pir52g'
  }

  response = requests.request("POST", url, headers=headers, data = payload)
  respuesta = response.json()
  Token = respuesta['token']
  return(Token)
def CreaAccesConsent(TokenApp,institucion,usuario):
######Crea el acces consents
  url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents"

  payload = "{  \"Data\":{    \"BankId\": \""+institucion+"\",    \"TransactionToDateTime\":\"2020-10-23T06:44:05.618Z\",    \"ExpirationDateTime\":\"2021-10-23T06:44:05.618Z\",    \"Permissions\":[\"ReadAccountsBasic\",\"ReadAccountsDetail\",\"ReadBalances\",\"ReadTransactionsBasic\",\"ReadTransactionsDebits\",\"ReadTransactionsDetail\"],    \"TransactionFromDateTime\":\"2020-10-23T06:44:05.618Z\"  }}"
  headers = {
  'Content-Type': 'application/json',
  'Authorization': 'DirectLogin token='+TokenApp+','
  'Cookie: JSESSIONID=1es187pzxfjqpmqg2gj6bged6'
  }

  response = requests.request("POST", url, headers=headers, data = payload)
  respuesta = response.json()
  Data = respuesta['Data']
  Consent = Data['ConsentId']
  Fecha = Data['TransactionFromDateTime']
  temp = len(Fecha)
  Fecha = Fecha[:temp - 5]
#####Se obtienen las cuentas del cliente
  url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts"
  payload = {}
  headers = {
  'Authorization': 'DirectLogin token='+TokenApp+','
  'Cookie: JSESSIONID=2ahkldeku5k0d3t6d29l7nt2'
  }

  response = requests.request("GET", url, headers=headers, data = payload)
  pruebaload = json.loads(response.text)
  cliente = User.objects.get()
  Cliente_id = cliente.username
  for Informacion in pruebaload["Data"]["Account"]:
    Nocuenta = Informacion['AccountId']
    Nickname = Informacion['Nickname']
    Currency = Informacion['Currency']
    Status = Informacion['Status']
    r = cuentasUsuario(
    cuenta_numero = Nocuenta,
    cuenta_user = usuario,
    cuenta_token = TokenApp,
    cuenta_institucion = institucion,
    cuenta_fecha_lim = datetime.datetime.strptime(Fecha, '%Y-%m-%dT%H:%M:%S'),
    cuenta_consent_id = Consent,
    cuenta_nickname = Nickname,
    cuenta_currency = Currency,
    cuenta_status = Status,
    cuenta_cliente = Cliente_id
    )
    r.save()
def getConssentCNBV():
######Obtiene el acces consents

  url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents"

  payload = "{  \"Data\":{    \"TransactionToDateTime\":\"2020-10-23T06:44:05.618Z\",    \"ExpirationDateTime\":\"2021-10-23T06:44:05.618Z\",    \"Permissions\":[\"ReadAccountsBasic\",\"ReadAccountsDetail\",\"ReadBalances\",\"ReadTransactionsBasic\",\"ReadTransactionsDebits\",\"ReadTransactionsDetail\"],    \"TransactionFromDateTime\":\"2020-10-23T06:44:05.618Z\"  }}"
  headers = {
    'Content-Type': 'application/json',
    'Authorization': 'DirectLogin token='+TokenApp+','
    'Cookie: JSESSIONID=dku1uxd4wixj1bkqsb9pir52g'
  }

  response = requests.request("POST", url, headers=headers, data = payload)
  respuesta = response.json()
  Data = respuesta['Data']
  Consent = Data['ConsentId']
  Fecha = Data['TransactionFromDateTime']
  temp = len(Fecha)
  Fecha = Fecha[:temp - 5]

def getSaldo(cuenta, token):
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta+"/balances"

    payload = {}
    headers = {
      'Authorization': 'DirectLogin token='+token+','
      'Cookie: JSESSIONID=180q56fxhc4zj13xmvtan5s8f'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    print('------------------------Detalle de Saldo---------------------------')
    print(response.text)
    print('--------------------------------------------------------------------')
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        for Informacion in pruebaload["Data"]["Balance"]:
            Monto = Informacion["Amount"]['amount']
        return(Monto)
    else:
        return('NoOK')

def DetalleCuenta(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_cliente=Cliente_id, cuenta_numero=cuenta)
    for entry in cuentaUsuario:
        tokenCliente = entry.cuenta_token
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta

    payload  = {}
    headers = {
      'Authorization': 'DirectLogin token='+tokenCliente+','
      'Cookie: JSESSIONID=17ex35y5ry18u1atusfi3y4clt'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    print('------------------------Detalle de cuenta---------------------------')
    print(response.text)
    print('--------------------------------------------------------------------')
    RegistrosCta = []
    for entry in pruebaload["Data"]["Account"]:
        RegistrosCta.append(DetallesCuenta(entry['AccountId'], entry['Status'], entry['StatusUpdateDateTime'], entry['Currency'], entry['AccountType'], entry['AccountSubType'], entry['AccountIndicator'], entry['OnboardingType'], entry['Nickname'], entry['OpeningDate'], entry['Servicer']['SchemeName'], entry['Servicer']['Identification']))
    return(RegistrosCta)

def DetalleConsentimiento(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_cliente=Cliente_id, cuenta_numero=cuenta)
    for entry in cuentaUsuario:
        tokenCliente = entry.cuenta_token
        consent_id = entry.cuenta_consent_id
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents/"+consent_id

    payload = {}
    headers = {
      'Content-Type': 'application/json',
      'Authorization': 'DirectLogin token='+tokenCliente+','
      'Cookie: JSESSIONID=17ex35y5ry18u1atusfi3y4clt'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    print('------------------------Detalle de consentimiento---------------------------')
    print(response.text)
    print('--------------------------------------------------------------------------')
    DetallesCon = []
    DetallesCon.append(DetalleConsent(pruebaload["Data"]['CreationDateTime'], pruebaload["Data"]['ExpirationDateTime'], pruebaload["Data"]['ConsentId'], pruebaload["Data"]['Status'],pruebaload["Data"]['Permissions']))
    return(DetallesCon)

def DevTransacciones(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_cliente=Cliente_id, cuenta_numero=cuenta)
    for entry in cuentaUsuario:
        tokenCliente = entry.cuenta_token
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/accounts/"+cuenta+"/transactions"

    payload = {}
    headers = {
      'Authorization': 'DirectLogin token='+tokenCliente+','
      'Cookie: JSESSIONID=17ex35y5ry18u1atusfi3y4clt'
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    print('------------------------Detalle de transacciones---------------------------')
    print(response.text)
    print('-------------------------------------------------------------------------')
    Transaccionesdeta = []
    for entry in pruebaload["Data"]["Transaction"]:
        Transaccionesdeta.append(DetalleTransaccion(entry['TransactionId'], entry['Status'], entry['BookingDateTime'], entry['TransactionInformation'], entry['Amount']['Amount'], entry['Amount']['Currency']))
    return(Transaccionesdeta)

def EliminaConsent(cuenta):
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_cliente=Cliente_id, cuenta_numero=cuenta)
    for entry in cuentaUsuario:
        tokenCliente = entry.cuenta_token
        consentid = entry.cuenta_consent_id
    url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents/"+consentid

    payload = {}
    headers = {
        'Content-Type': 'application/json'+','
        'Authorization: DirectLogin token='+tokenCliente
    }

    response = requests.request("DELETE", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    for entry in cuentaUsuario:
        entry.delete()
>>>>>>> 5a28afeafdb6503d5350fa1d8071ad7d096d13aa
