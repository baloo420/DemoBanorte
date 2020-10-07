"""demobanorte URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from demobanorte.Apps.apicall import views
from demobanorte.Apps.apicall.servicesCNBV import getSaldo
from demobanorte.Apps.apicall.models import cuentasUsuario

urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login),
    path('', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('admin/', admin.site.urls),
    path('home/', views.home, name='home'),
    path('redirect/', views.redirigir, name='redirigir'),
    path('administro_ctas/', views.agregobanco, name='agregobanco'),
    path('administro_ctas_/', views.adminbanco, name='adminbanco'),
    path('administro_ctas-/', views.eliminocta, name='eliminocta'),
    path('informacion_ctas/', views.informacioncuenta, name='informacioncuenta'),
    path('informacion_ctas_/', views.devinformacion, name='devinformacion'),
    path('', getSaldo, name='getSaldo'),
    path('', cuentasUsuario, name='cuentasUsuario'),
]
