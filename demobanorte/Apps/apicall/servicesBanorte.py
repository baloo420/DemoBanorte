import requests
import json
import datetime
from demobanorte.Apps.apicall.models import cuentasUsuario, Parametros
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.serializers.json import DjangoJSONEncoder
from demobanorte.Apps.apicall.models import DetallesCuenta, DetalleConsent, DetalleTransaccion, procesocta
import uuid
import hashlib
import os
import base64
import python_jwt as jwt, jwcrypto.jwk as jwk, datetime
import jwt


def identity():
    url = "https://amer-api-partner67-test.apigee.net/identity/v1/token?grant_type=client_credentials"

    payload = {}
    headers = {
      'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    Msj = response.text
    if response.status_code == 200:
        respuesta = response.json()
        access_token = respuesta['access_token']

        url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1"

        payload = "{\n    \"Data\": {\n        \"TransactionToDateTime\": \"2020-10-19T11:25:41-05:00\",\n        \"ExpirationDateTime\": \"2020-11-03T11:25:41-06:00\",\n        \"Permissions\": [\n            \"ReadAccountsBasic\",\n            \"ReadAccountsDetail\",\n            \"ReadBalances\",\n            \"ReadTransactionsBasic\",\n            \"ReadTransactionsDebits\",\n            \"ReadTransactionsDetail\"\n        ],\n        \"TransactionFromDateTime\": \"2020-10-19T11:25:41-05:00\"\n    }\n}"
        headers = {
          'Authorization': 'Bearer '+access_token,
          'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data = payload)
        if response.status_code == 200:
            respuesta = response.json()
            Data = respuesta['Data']
            consent_id = Data['ConsentId']
            Ruta = 'https://amer-api-partner67-test.apigee.net/identity/v1/authorize?response_type=code id_token'
            parametro = Parametros.objects.get(parametro_id='CLIENT_ID', parametro_proxi='banorte')
            client_id = parametro.parametro_valor
            parametro2 = Parametros.objects.get(parametro_id='RUTA_RED', parametro_proxi='banorte')
            redirect_uri = parametro2.parametro_valor
            parametro3 = Parametros.objects.get(parametro_id='PRIVATEKEY', parametro_proxi='banorte')
            #secret = parametro3.parametro_valor
            scope = 'openid email profile'
            noncec = uuid.uuid4()
            nonce = str(noncec)
            verifier_bytes = os.urandom(32)
            code_verifier = base64.urlsafe_b64encode(verifier_bytes).rstrip(b'=')
            challenge_bytes = hashlib.sha256(code_verifier).digest()
            code_challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=')
            code_challenge_method = 'S256'
            statex = uuid.uuid4()
            state = str(statex)
            id_application = "e452e391-5afb-476d-9343-70b394e3c051"
            audience = "https://amer-api-partner67-test.apigee.net/identity/v1/token"
            jwt_idx = uuid.uuid4()
            jwt_id = str(jwt_idx)
            now = datetime.datetime.now()
            payload = {
              "max_age": "3600",
              "iss": client_id,
              "sub": client_id,
              "iat": now,
              "jti": jwt_id,
              "id": id_application,
              "client_id": client_id,
              "redirect_uri": redirect_uri,
              "aud": audience,
              "scope": scope,
              "response_type": "code id_token",
              "state": state,
              "nonce": nonce,
              "claims": {
                "id_token": {
                    "openbanking_intent_id": {
                        "value": consent_id,
                        "essential": "true"
                    }
                }
               }
            }
            priv_key = b'-----BEGIN RSA PRIVATE KEY-----\n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\n-----END RSA PRIVATE KEY-----\n'
            client_assertion = jwt.encode(payload, priv_key, algorithm='RS256')
            X = str(client_assertion)
            Y = X[2 :len(X) -1]
            URLGenerada = Ruta+"&client_id="+client_id+"&scope="+scope+"&nonce="+nonce+"&code_challenge="+str(code_challenge)+"&code_challenge_method="+code_challenge_method+"&state="+state+"&client_assertion="+Y
            return(URLGenerada)
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

def GenerateAccessTokenApigee(code, Cliente_id):
    parametro2 = Parametros.objects.get(parametro_id='RUTA_RED', parametro_proxi='banorte')
    redirect_uri = parametro2.parametro_valor
    url = "https://amer-api-partner67-test.apigee.net/identity/v1/token?grant_type=authorization_code"

    payload = 'code='+code+'&redirect_uri='+redirect_uri
    headers = {
      'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA==',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.request("POST", url, headers=headers, data = payload)
    if response.status_code == 200:
        respuesta = response.json()
        access_token = respuesta['access_token']
        id_token = respuesta['id_token']
        refresh_token = respuesta['refresh_token']
        scope = respuesta['scope']
        Consent = respuesta['consent_id']
        url = "https://amer-api-partner67-test.apigee.net/mx-open-finance/v0.0.1/accounts"

        payload = {}
        headers = {
          'Authorization': 'Bearer '+access_token
        }

        response = requests.request("GET", url, headers=headers, data = payload)
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
                    cuenta_inst_inf = 'banorte'
                    )
                    r.save()
                s = procesocta(
                proceso_user = Cliente_id,
                proceso_token = access_token,
                proceso_refresh_token = refresh_token,
                proceso_inst_inf = 'banorte',
                proceso_cod_inst = institucion,
                proceso_consent = Consent
                )
                s.save()
                Mensaje = 'Se agregaron las cuentas correctamente'
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
    return (Mensaje)

def getSaldob(cuenta, cod_institucion, Cliente_id):
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cod_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
    token = DatosProceso.proceso_token
    url = "https://amer-api-partner67-test.apigee.net/mx-open-finance/v0.0.1/accounts/"+cuenta+"/balances"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        for Informacion in pruebaload["Data"]["Balance"]:
            Monto = Informacion["Amount"]['Amount']
        return(Monto)
    else:
        return('NoOK')

def DetalleCuentaB(cuenta, Cliente_id):
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
    token = DatosProceso.proceso_token
    url = "https://amer-api-partner67-test.apigee.net/mx-open-finance/v0.0.1/accounts/"+cuenta

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    pruebaload = json.loads(response.text)
    RegistrosCta = []
    if response.status_code == 200:
        for entry in pruebaload["Data"]["Account"]:
            RegistrosCta.append(DetallesCuenta(entry['AccountId'], entry['Status'], entry['StatusUpdateDateTime'], entry['Currency'], entry['AccountType'], entry['AccountSubType'], entry['AccountIndicator'], entry['OnboardingType'], entry['Nickname'], entry['OpeningDate'], entry['Servicer']['SchemeName'], entry['Servicer']['Identification']))
    elif response.status_code == 400 or response.status_code == 401 or response.status_code == 404:
        codigo = response.status_code
        RegistrosCta.append(DetallesCuenta(codigo, 'No tiene autorización para solicitar esta información', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        RegistrosCta.append(DetallesCuenta(codigo, Descrip, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '))
    return(RegistrosCta)

def DetalleConsentimientoB(cuenta, Cliente_id):
######Obtiene el acces consents
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
    token = DatosProceso.proceso_token
    Consent = DatosProceso.proceso_consent
    ####se obtiene el detalle

    url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1/"+Consent

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token,
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    DetallesCon = []
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        DetallesCon.append(DetalleConsent(pruebaload["Data"]['CreationDateTime'], pruebaload["Data"]['ExpirationDateTime'], pruebaload["Data"]['ConsentId'], pruebaload["Data"]['Status'],pruebaload["Data"]['Permissions']))
    elif response.status_code == 400 or response.status_code == 401 or response.status_code == 403 or response.status_code == 404:
        codigo = response.status_code
        DetallesCon.append(DetalleConsent(codigo, 'No tiene autorización para solicitar esta información', ' ', ' ',' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        DetallesCon.append(DetalleConsent(codigo, Descrip, ' ', ' ',' '))
    return(DetallesCon)

def DevTransaccionesB(cuenta, Cliente_id):
    cuentaUsuario = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta)
    DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaUsuario.cuenta_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
    token = DatosProceso.proceso_token

    url = "https://amer-api-partner67-test.apigee.net/mx-open-finance/v0.0.1/accounts/"+cuenta+"/transactions"

    payload = {}
    headers = {
      'Authorization': 'Bearer '+token
    }

    response = requests.request("GET", url, headers=headers, data = payload)
    Transaccionesdeta = []
    if response.status_code == 200:
        pruebaload = json.loads(response.text)
        for entry in pruebaload["Data"]["Transaction"]:
            Transaccionesdeta.append(DetalleTransaccion(entry['TransactionId'], entry['Status'], entry['BookingDateTime'], entry['TransactionInformation'], entry['Amount']['Amount'], entry['Amount']['Currency']))
    elif response.status_code == 400 or response.status_code == 401 or response.status_code == 404:
        codigo = response.status_code
        Transaccionesdeta.append(DetalleTransaccion(codigo, 'No tiene autorización para solicitar esta información', ' ', ' ', ' ', ' '))
    else:
        codigo = response.status_code
        Descrip = response.error_description
        Transaccionesdeta.append(DetalleTransaccion(codigo, Descrip, ' ', ' ', ' ', ' '))
    return(Transaccionesdeta)

def EliminaConsentB(cuenta, Cliente_id):
    Existe = 'No'
    cuentaeliminar = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta, cuenta_inst_inf='banorte')
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id, cuenta_inst_inf='banorte', cuenta_institucion=cuentaeliminar.cuenta_institucion)
    for entry in cuentaUsuario:
        if entry.cuenta_numero != cuenta:
            Existe = 'Si'
    if Existe == 'No':
        DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
        token = DatosProceso.proceso_token
        Consent = DatosProceso.proceso_consent
            #Con el consent se envia la eliminacion del mismo
        url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1/"+Consent

        payload = {}
        headers = {
          'Authorization': 'Bearer '+token,
        }
        response = requests.request("DELETE", url, headers=headers, data = payload)
        if response.status_code == 204:
            proceliminar = procesocta.objects.get(proceso_user=Cliente_id, proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='banorte')
            proceliminar.delete()
            cuentaeliminar.delete()
            Mensaje = 'Se elimino consentimiento y la cuenta '+cuentaeliminar.cuenta_nickname
        elif response.status_code == 400 or response.status_code == 401 or response.status_code == 404:
            codigo = response.status_code
            Mensaje = 'Error:'+str(codigo)+' Se elimino la cuenta '+cuentaeliminar.cuenta_nickname +' ya no existia consentimiento'
            proceliminar = procesocta.objects.get(proceso_user=Cliente_id, proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='banorte')
            proceliminar.delete()
            cuentaeliminar.delete()
        else:
            codigo = response.status_code
            Descrip = response.error_description
            Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
    else:
        Mensaje = 'Se elimino la cuenta '+cuentaeliminar.cuenta_nickname+' no asi el consentimiento ya que se tiene otra cuenta ligada'
        cuentaeliminar.delete()
        print('MENSAJE:'+Mensaje)
    return(Mensaje)

def refrescarTokenB(client_user, tokenRefresh):
    Mensaje = ' '
    client_id = Parametros.objects.get(parametro_id='CLIENT_ID', parametro_proxi='banorte')
    client_secret = Parametros.objects.get(parametro_id='CLIENT_SEC', parametro_proxi='banorte')
    Ruta_Redirect = Parametros.objects.get(parametro_id='RUTA_RED', parametro_proxi='banorte')
    TokenAActualizar = procesocta.objects.get(proceso_user=client_user, proceso_refresh_token=tokenRefresh)
    url = "https://amer-api-partner67-test.apigee.net/identity/v1/token/refresh?grant_type=refresh_token&refresh_token="+tokenRefresh

    payload = {}
    headers = {
      'Authorization': 'Basic emNXVTBvQ3RjVHJjVFlIajdmUHg5bHZBR0Jzb1N2aE06dGhaeXk5b09DaU5YaEdJVA=='
    }

    response = requests.request("POST", url, headers=headers, data = payload)
    respuesta = response.json()
    if response.status_code == 200:
        Access_Token = respuesta['access_token']
        id_token = respuesta['id_token']
        refresh_token = respuesta['refresh_token']
        TokenAActualizar.proceso_token = Access_Token
        TokenAActualizar.proceso_refresh_token = refresh_token
        TokenAActualizar.save()
    elif response.status_code == 400 or response.status_code == 401:
        codigo = response.status_code
        Mensaje += 'Error:'+str(codigo)+'-'
    else:
        codigo = response.status_code
        Descrip = response.error_description
        Mensaje += 'Error:'+str(codigo)+' Que indica:'+Descrip
    return(Mensaje)

def eliminoconsentB(cuenta, Cliente_id):
    Existe = 'No'
    cuentaeliminar = cuentasUsuario.objects.get(cuenta_user=Cliente_id, cuenta_numero=cuenta, cuenta_inst_inf='banorte')
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id, cuenta_inst_inf='banorte', cuenta_institucion=cuentaeliminar.cuenta_institucion)
    for entry in cuentaUsuario:
        if entry.cuenta_numero != cuenta:
            Existe = 'No'
    if Existe == 'No':
        DatosProceso = procesocta.objects.get(proceso_cod_inst=cuentaeliminar.cuenta_institucion, proceso_inst_inf='banorte', proceso_user=Cliente_id)
        token = DatosProceso.proceso_token
        Consent = DatosProceso.proceso_consent
            #Con el consent se envia la eliminacion del mismo
        url = "https://amer-api-partner67-test.apigee.net/account-access-consent/v3.1/"+Consent

        payload = {}
        headers = {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer '+token,
        }
        response = requests.request("DELETE", url, headers=headers, data = payload)
        if response.status_code == 204:
            Mensaje = 'Se elimino consentimiento'
        elif response.status_code == 400 or response.status_code == 401:
            codigo = response.status_code
            Mensaje = 'Error:'+str(codigo)
        else:
            codigo = response.status_code
            Descrip = response.error_description
            Mensaje = 'Error:'+str(codigo)+' Que indica:'+Descrip
    else:
        Mensaje = 'Se elimino la cuenta '+cuentaeliminar.cuenta_nickname+' no asi el consentimiento ya que se tiene otra cuenta ligada'
        #cuentaeliminar.delete()
    return(Mensaje)
