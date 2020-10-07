from django.contrib import admin
from django.contrib.auth.models import User
# Register your models here.
from demobanorte.Apps.apicall.models import *

admin.site.register(Parametros)
admin.site.register(cuentasUsuario)
admin.site.register(instituciones)
admin.site.register(procesocta)
