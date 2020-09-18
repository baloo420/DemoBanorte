from django.shortcuts import render
from django.http import HttpResponse
#from services import identity
import requests
import json
import http.client
import mimetypes
import services

#from login.service import GenerateToken

# Create your views here.
def home(request):
    context = identity.generateToken()
    return render(request, 'login/masterpage.html', context)

def llamadologin(url, params={}):
    url = 'https://hugomendietapacheco-62916-eval-test.apigee.net/identity/v1/authorize'
    params = {'client_id':'SZK0gfxWSC7zy46BL0m1rGTROqqCiS5A', 'consent_id':'3801dcad-a69f-4f8e-a79c-b37720fe1102'}
    response = requests.post(url, params=params)

def agregobanco(request):
    context={}
    return render(request, 'login/agregobanco.html', context)

def solicitotransaccion(request):
    context={}
    return render(request, 'login/solicitotransaccion.html', context)


def solicitoinformacion(request):
    context={}
    return render(request, 'login/solicitoinformacion.html', context)


def modificoinformacion(request):
    context={}
    return render(request, 'login/modificoinformacion.html', context)

def saldos(request):
    context={}
    return render(request, 'login/saldos.html', context)
