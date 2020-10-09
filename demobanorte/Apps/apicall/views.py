from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login
from demobanorte.Apps.apicall.servicesCNBV import getSaldo, DetalleCuenta, DetalleConsentimiento, DevTransacciones, EliminaConsent, logincnbv, refrescarToken, eliminoconsent
from demobanorte.Apps.apicall.models import cuentasUsuario, instituciones, MostrarSaldos, DetallesCuenta, DetalleConsent, DetalleTransaccion, procesocta
from django.contrib.auth.models import User
import requests
import json
import http.client
import mimetypes
import random

#Pantalla de inicio para usuarios
def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
    # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)
            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('home')
            # Añadimos los datos recibidos al formulario
    # Si llegamos al final renderizamos el formulario
    return render(request, "login.html", {'form': form})
#registro de nuevos usuarios
def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():
            # Creamos la nueva cuenta de usuario
            user = form.save()
            # Si el usuario se crea correctamente
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('login')

    # Si llegamos al final renderizamos el formulario
    return render(request, "register.html", {'form': form})
# Llamado a la pagina de inicio de la aplicacion
def home(request):
    Cliente_id = request.user.get_username ()
    print('EL USUARIO DENTRO ES'+str(Cliente_id))
    #Cliente_id = request.GET['username']
    Mensaje = refrescarToken('elopez')
    #AGREAR A LA VISTA
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    Json_file = []
    Nombre_Institucion = ''
    for entry in cuentaUsuario:
        numeroCuenta = entry.cuenta_numero
        Institucion_desc = instituciones.objects.get(institucion_codigo=entry.cuenta_institucion)
        if Institucion_desc:
            Nombre_Institucion = Institucion_desc.institucion_nombre
            icono = "img/logo_"+Institucion_desc.institucion_id+".svg"
        SaldoCuenta = getSaldo(numeroCuenta, entry.cuenta_institucion, Cliente_id)
        if SaldoCuenta == 'NoOK':
            Json_file.append(MostrarSaldos(entry.cuenta_numero, entry.cuenta_nickname, 'Consentimiento Vencido', entry.cuenta_institucion, Nombre_Institucion, entry.cuenta_currency, icono))
        else:
            Json_file.append(MostrarSaldos(entry.cuenta_numero, entry.cuenta_nickname, SaldoCuenta, entry.cuenta_institucion, Nombre_Institucion, entry.cuenta_currency, icono))
    context={'Saldos':Json_file, 'ErrorActToken':Mensaje}
    return render(request, 'masterpage.html', context)
#Pagina donde se iniciara el proceso para agregar las cuentas de cualquier Banco que se solicite
def agregobanco(request):
    Mensaje = ''
    Cliente_id = request.user.get_username ()
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    Json_file = []
    for entry in cuentaUsuario:
        numeroCuenta = entry.cuenta_numero
        Json_file.append(MostrarSaldos(entry.cuenta_numero, entry.cuenta_nickname, '', entry.cuenta_institucion, "", entry.cuenta_currency, ""))
    context={'Saldos':Json_file, 'Error_Descr': Mensaje}
    return render(request, 'administroctas.html', context)

def adminbanco(request):
    Cliente_id = request.user.get_username ()
    institucion = request.POST['Institucion']
    Ruta = 'https://oauth2.ofpilot.com/hydra-public/oauth2/auth?client_id='
    Client_id = 'z104dwltrg5e2cteoskjy5j2f20w0pte5cex3k0z'
    characters = list('abcdefghijklmnopqrstvwyzABCDEFGHIJKLMNOPQRSTVWYZ1234567890')
    state = ''
    for x in range(25):
        state += random.choice(characters)
    redirecion = 'https://127.0.0.1:8000/redirect/'
    RutaArmada = Ruta+Client_id+'&response_type=code&state='+state+'&scope=openid+offline+ReadAccountsBasic+ReadAccountsDetail+ReadBalances+ReadTransactionsBasic+ReadTransactionsDebits+ReadTransactionsDetail&redirect_uri='+redirecion
    return redirect(RutaArmada)

def redirigir(request):
    CuentaCode = request.GET['code']
    Cuentastate = request.GET['state']
    Cliente_id = request.user.get_username ()
    Mensaje = logincnbv(CuentaCode, Cuentastate, Cliente_id)
    Cliente_id = request.user.get_username ()
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    Json_file = []
    for entry in cuentaUsuario:
        numeroCuenta = entry.cuenta_numero
        Json_file.append(MostrarSaldos(entry.cuenta_numero, entry.cuenta_nickname, '', entry.cuenta_institucion, "", entry.cuenta_currency, ""))
    context={'Saldos':Json_file, 'Error_Descr': Mensaje}
    return render(request, 'administroctas.html', context)

def eliminocta(request):
    Cliente_id = request.user.get_username ()
    cuenta = request.POST['numerocuenta']
    if request.method=='POST' and 'Elimino' in request.POST:
        Mensaje = EliminaConsent(cuenta, Cliente_id)
    else:
        Mensaje = eliminoconsent(cuenta, Cliente_id)
    cuentaUsuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    Json_file = []
    for entry in cuentaUsuario:
        numeroCuenta = entry.cuenta_numero
        Json_file.append(MostrarSaldos(entry.cuenta_numero, entry.cuenta_nickname, '', entry.cuenta_institucion, "", entry.cuenta_currency, ""))
    context={'Saldos':Json_file, 'Error_Descr': Mensaje}
    return render(request, 'administroctas.html', context)

def informacioncuenta(request):
    Cliente_id = request.user.get_username ()
    cuentasusuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    context={'cuentasusuario':cuentasusuario}
    return render(request, 'detallecuenta.html', context)

def devinformacion(request):
    CuentaDetalle = request.POST['cuentadetalle']
    serviciosolicitado = request.POST['serviciosolicitado']
    Cliente_id = request.user.get_username ()
    cuentausuario = cuentasUsuario.objects.all().filter(cuenta_user=Cliente_id)
    if serviciosolicitado == 'detalle':
        DetallesCuenta = DetalleCuenta(CuentaDetalle, Cliente_id)
        context={'DetalleCuenta':DetallesCuenta, 'cuentasusuario':cuentausuario, 'cuentadetalle':CuentaDetalle, 'Cliente_id':Cliente_id}
    elif serviciosolicitado == 'consent':
        DetallesCon = DetalleConsentimiento(CuentaDetalle, Cliente_id)
        context={'DetallesConsent':DetallesCon, 'cuentasusuario':cuentausuario, 'cuentadetalle':CuentaDetalle, 'Cliente_id':Cliente_id}
    elif serviciosolicitado == 'transacciones':
        TransaccionesCuenta = DevTransacciones(CuentaDetalle, Cliente_id)
        context={'TransaccionesCuenta':TransaccionesCuenta, 'cuentasusuario':cuentausuario, 'cuentadetalle':CuentaDetalle, 'Cliente_id':Cliente_id}
    else:
        context = {}
    return render(request, 'detallecuenta.html', context)

def logout(request):
    logout(request)
    return redirect('https://www.banorte.com/wps/portal/banorte/Home/inicio')
    # Redirect to a success page.
