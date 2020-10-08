import requests
import json
import datetime
from demobanorte.Apps.apicall.models import cuentasUsuario, Parametros
from django.http import HttpResponse
from django.contrib.auth.models import User
from demobanorte.Apps.apicall.models import DetallesCuenta, DetalleConsent, DetalleTransaccion, procesocta
#####Flujo inicial
def logincnbv(code, state):
    Mensaje= ''
    cliente = User.objects.get()
    Cliente_id = cliente.username
    client_id = Parametros.objects.get(parametro_id='CLIENT_ID', parametro_proxi='CNBV')
    client_secret = Parametros.objects.get(parametro_id='CLIENT_SEC', parametro_proxi='CNBV')
    Ruta_Redirect = Parametros.objects.get(parametro_id='RUTA_RED', parametro_proxi='CNBV')
# Se obtiene el Access Token para las operaciones
    url = "https://oauth2.ofpilot.com/hydra-public/oauth2/token"

    payload = 'grant_type=authorization_code&code='+code+'&client_id='+client_id.parametro_valor+'&client_secret='+client_secret.parametro_valor+'&redirect_uri='+Ruta_Redirect.parametro_valor
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Cookie': 'oauth2_authentication_csrf=MTYwMTkzMDQ2N3xEdi1CQkFFQ180SUFBUkFCRUFBQVB2LUNBQUVHYzNSeWFXNW5EQVlBQkdOemNtWUdjM1J5YVc1bkRDSUFJRGRqTmpFMFlUSmxZVGRtWXpRME0yTTVNREEwTXpFMFlUVmhaakV4WXpGbXyYQXMOqEMA7vX-n-hOsUszVLGKwsXzu6iBDnYDTWHGvg=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    print('------------------------Access Token-------------------------------')
    print(response)
    print('-----------------------------------------------------------------------')
    if response.status_code == 200:
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
        print('------------------------Devuelvo las cuentas-------------------------------')
        print(response)
        print('-----------------------------------------------------------------------')
        if response.status_code == 200:
            pruebaload = json.loads(response.text)
            if pruebaload["Data"]["Account"]:
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
                    cuenta_scope = scope,
                    cuenta_inst_inf = 'CNBV'
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
                Mensaje = 'Se agregaron las cuentas correctamente'
            else:
                Mensaje = 'No se recibieron cuentas relacionadas al usuario o no se le dio consentimiento a ninguna cuenta'
        elif response.status_code == 400 or response.status_code == 401:
            codigo = response.status_code
            Mensaje = 'Error:'+str(codigo)
        else:
            codigo = response.status_code
            Descrip = response.error_description
            Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
    elif response.status_code == 400 or response.status_code == 401:
        codigo = response.status_code
        Mensaje = 'Error:'+str(codigo)
    else:
        codigo = response.status_code
        Descrip = response.error_description
        Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
    return(Mensaje)

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
    print('------------------------Dev Saldo-------------------------------')
    print(response)
    print('-----------------------------------------------------------------------')
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
    print('------------------------Detalle de Cuenta-------------------------------')
    print(response)
    print('-----------------------------------------------------------------------')
    pruebaload = json.loads(response.text)
    if response.status_code == 200:
        RegistrosCta = []
        for entry in pruebaload["Data"]["Account"]:
            RegistrosCta.append(DetallesCuenta(entry['AccountId'], entry['Status'], entry['StatusUpdateDateTime'], entry['Currency'], entry['AccountType'], entry['AccountSubType'], entry['AccountIndicator'], entry['OnboardingType'], entry['Nickname'], entry['OpeningDate'], entry['Servicer']['SchemeName'], entry['Servicer']['Identification']))
    elif response.status_code == 400 or response.status_code == 401:
        codigo = response.status_code
        RegistrosCta.append(DetallesCuenta(codigo, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        RegistrosCta.append(DetallesCuenta(codigo, Descrip, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
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
    print('------------------------Obtengo el Consentimiento-------------------------------')
    print(response)
    print('-----------------------------------------------------------------------')
    if response.status_code == 201:
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
        print('------------------------Detalle de Consentimiento-------------------------------')
        print(response)
        print('-----------------------------------------------------------------------')
        if response.status_code == 200:
            pruebaload = json.loads(response.text)
            DetallesCon = []
            DetallesCon.append(DetalleConsent(pruebaload["Data"]['CreationDateTime'], pruebaload["Data"]['ExpirationDateTime'], pruebaload["Data"]['ConsentId'], pruebaload["Data"]['Status'],pruebaload["Data"]['Permissions']))
        elif response.status_code == 400 or response.status_code == 401:
            codigo = response.status_code
            DetallesCon.append(DetalleConsent(codigo, ' ', ' ', ' ',' '))
        else:
            codigo = response.status_code
            Descrip = response.error_description
            DetallesCon.append(DetalleConsent(codigo, Descrip, ' ', ' ',' '))
    elif response.status_code == 400 or response.status_code == 401:
        codigo = response.status_code
        DetallesCon.append(DetalleConsent(codigo, ' ', ' ', ' ',' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        DetallesCon.append(DetalleConsent(codigo, Descrip, ' ', ' ',' '))
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
    print('------------------------Dev transacciones-------------------------------')
    print(response)
    print('-----------------------------------------------------------------------')
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        Transaccionesdeta = []
        for entry in pruebaload["Data"]["Transaction"]:
            Transaccionesdeta.append(DetalleTransaccion(entry['TransactionId'], entry['Status'], entry['BookingDateTime'], entry['TransactionInformation'], entry['Amount']['Amount'], entry['Amount']['Currency']))
    elif response.status_code == 400 or response.status_code == 401:
        codigo = response.status_code
        Transaccionesdeta.append(DetalleTransaccion(codigo, ' ', ' ', ' ', ' ', ' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        Transaccionesdeta.append(DetalleTransaccion(codigo, Descrip, ' ', ' ', ' ', ' '))
    return(Transaccionesdeta)
def EliminaConsent(cuenta):
    Existe = 'No'
    cliente = User.objects.get()
    Cliente_id = cliente.username
    cuentaeliminar = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta, cuenta_inst_inf='CNBV')
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id, cuenta_inst_inf='CNBV', cuenta_institucion=cuentaeliminar.cuenta_institucion)
    for entry in cuentaUsuario:
        if entry.cuenta_numero != cuenta:
            Existe = 'Si'
    if Existe == 'No':
        DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='CNBV')
        token = DatosProceso.proceso_token
        #Se va por el consent_Id
        url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents"

        payload = "{  \"Data\":{    \"TransactionToDateTime\":\"2020-10-23T06:44:05.618Z\",    \"ExpirationDateTime\":\"2021-10-23T06:44:05.618Z\",    \"Permissions\":[\"ReadAccountsBasic\",\"ReadAccountsDetail\",\"ReadBalances\",\"ReadTransactionsBasic\",\"ReadTransactionsDebits\",\"ReadTransactionsDetail\"],    \"TransactionFromDateTime\":\"2020-10-23T06:44:05.618Z\"  }}"
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+token,
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code == 201:
            respuesta = response.json()
            Data = respuesta['Data']
            Consent = Data['ConsentId']
            #Con el consent se envia la eliminacion del mismo
            url = "https://apisandbox.ofpilot.com/mx-open-finance/v0.0.1/account-access-consents/"+Consent

            payload = {}
            headers = {
              'Authorization': 'Bearer '+token,
              'Cookie': 'JSESSIONID=1e7rpb6c1xah11mbdrh00adr0p'
            }
            response = requests.request("DELETE", url, headers=headers, data = payload)
            print('------------------------Eliminar Consentimiento-------------------------------')
            print(response)
            print('-----------------------------------------------------------------------')
            if response.status_code == 204:
                proceliminar = procesocta.objects.get(proceso_user=Cliente_id, proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='CNBV')
                proceliminar.delete()
                cuentaeliminar.delete()
                Mensaje = 'Se elimino consentimiento'
            elif response.status_code == 400 or response.status_code == 401:
                codigo = response.status_code
                Mensaje = 'Error:'+str(codigo)
            else:
                codigo = response.status_code
                Descrip = response.error_description
                Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
        elif response.status_code == 400 or response.status_code == 401:
            codigo = response.status_code
            Mensaje = 'Error:'+str(codigo)
        else:
            codigo = response.status_code
            Descrip = response.error_description
            Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
    else:
        Mensaje = 'Se elimino la cuenta '+cuentaeliminar.cuenta_nickname+' no asi el consentimiento ya que se tiene otra cuenta ligada'
        cuentaeliminar.delete()
        print('MENSAJE:'+Mensaje)
    return(Mensaje)

def refrescarToken(client_user):
    Mensaje = ' '
    client_id = Parametros.objects.get(parametro_id='CLIENT_ID', parametro_proxi='CNBV')
    client_secret = Parametros.objects.get(parametro_id='CLIENT_SEC', parametro_proxi='CNBV')
    Ruta_Redirect = Parametros.objects.get(parametro_id='RUTA_RED', parametro_proxi='CNBV')
    TokenAActualizar = procesocta.objects.all().filter(proceso_user=client_user, proceso_inst_inf='CNBV')
    for entry in TokenAActualizar:
        tokenRefresh = entry.proceso_refresh_token
        url = "https://oauth2.ofpilot.com/hydra-public/oauth2/token"

        payload = 'grant_type=refresh_token&refresh_token='+tokenRefresh+'&client_id='+client_id.parametro_valor+'&client_secret='+client_secret.parametro_valor+'&redirect_uri='+Ruta_Redirect.parametro_valor
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          'Cookie': 'oauth2_authentication_csrf=MTYwMTkzMDQ2N3xEdi1CQkFFQ180SUFBUkFCRUFBQVB2LUNBQUVHYzNSeWFXNW5EQVlBQkdOemNtWUdjM1J5YVc1bkRDSUFJRGRqTmpFMFlUSmxZVGRtWXpRME0yTTVNREEwTXpFMFlUVmhaakV4WXpGbXyYQXMOqEMA7vX-n-hOsUszVLGKwsXzu6iBDnYDTWHGvg=='
        }
        response = requests.request("POST", url, headers=headers, data = payload)
        print('------------------------Actualizar Token-------------------------------')
        print(response)
        print('-----------------------------------------------------------------------')
        respuesta = response.json()
        if response.status_code == 200:
            Access_Token = respuesta['access_token']
            id_token = respuesta['id_token']
            refresh_token = respuesta['refresh_token']
            entry.proceso_token = Access_Token
            entry.proceso_refresh_token = refresh_token
            entry.save()
        elif response.status_code == 400 or response.status_code == 401:
            codigo = response.status_code
            Mensaje += 'Error:'+str(codigo)+'-'
        else:
            codigo = response.status_code
            Descrip = response.error_description
            Mensaje += 'Error:'+str(codigo)+' Que indica:'+Descrip
    return(Mensaje)
