from django.db import models

# Create your models here.
class Parametros(models.Model):
    parametro_id = models.CharField('Id',max_length=35, null=False)
    parametro_valor = models.CharField('Valor',max_length=99999, null=False)
    parametro_proxi = models.CharField('Institucion',max_length=100, null=False)

    def __str__(self):
        txt = "{0}, {1}, {2}"
        return txt.format(self.parametro_id, self.parametro_valor, self.parametro_proxi)

    def ParmValor(parametro_id):
        return parametro_valor()

class instituciones(models.Model):
    institucion_id = models.CharField('Id',max_length=30, null=False)
    institucion_nombre = models.CharField('Nombre',max_length=50, null=False)
    institucion_tipo = models.CharField('Tipo',max_length=30, null=False)
    institucion_codigo = models.CharField('codigo',max_length=25, null=False)

    def __str__(self):
        txt = "{0}, {1}, {2}, {3}"
        return txt.format(self.institucion_id, self.institucion_nombre, self.institucion_tipo, self.institucion_codigo)

class cuentasUsuario(models.Model):
    cuenta_id = models.AutoField(primary_key=True)
    cuenta_numero = models.CharField('Numero de Cuenta',max_length=50, null=False)
    cuenta_user = models.CharField('Usuario Banco',max_length=100, null=False)
    cuenta_institucion = models.CharField('Institucion',max_length=30, null=False)
    cuenta_nickname = models.CharField('nickname de la cuenta',max_length=100, null=False)
    cuenta_currency = models.CharField('Moneda',max_length=100, null=False)
    cuenta_status = models.CharField('Estatus',max_length=100, null=False)
    cuenta_id_token = models.CharField('Id token',max_length=9999, null=False)
    cuenta_scope = models.CharField('Scope',max_length=999, null=False)
    cuenta_inst_inf = models.CharField('Proveedor de Informacion',max_length=40, null=False)

    def __str__(self):
        txt = "{0}, {1}, {2}"
        return txt.format(self.cuenta_numero, self.cuenta_institucion, self.cuenta_nickname, self.cuenta_currency)

    def dev_cuenta_token(cuenta_numero):
        return(self.cuenta_token)

class procesocta(models.Model):
    proceso_user = models.CharField('Usuario Banco',max_length=100, null=False)
    proceso_token = models.CharField('Token',max_length=99999, null=False)
    proceso_refresh_token = models.CharField('Refresh Token',max_length=100, null=False)
    proceso_inst_inf = models.CharField('Proveedor de Informacion',max_length=40, null=False)
    proceso_cod_inst = models.CharField('Codigo Institucion',max_length=30, null=False)
    proceso_consent =  models.CharField('Id de Consentimiento',max_length=100, null=False)

    def __str__(self):
        txt = "{0}, {1}, {2}"
        return txt.format(self.proceso_user, self.proceso_token, self.proceso_refresh_token, self.proceso_inst_inf, self.proceso_cod_inst)

class MostrarSaldos:
    def __init__(self, cuenta_numero, cuenta_nickname, cuenta_saldo, cuenta_institucion, institucion_descripcion, cuenta_currency,cuenta_icono):
        self.cuenta_numero = cuenta_numero
        self.cuenta_nickname = cuenta_nickname
        self.cuenta_saldo = cuenta_saldo
        self.cuenta_institucion = cuenta_institucion
        self.institucion_descripcion = institucion_descripcion
        self.cuenta_currency = cuenta_currency
        self.cuenta_icono = cuenta_icono

class DetallesCuenta:
    def __init__(self, AccountId, Status, StatusUpdateDateTime, Currency, AccountType, AccountSubType, AccountIndicator, OnboardingType, Nickname, OpeningDate, SchemeName, Identification):
        self.AccountId = AccountId
        self.Status = Status
        self.StatusUpdateDateTime = StatusUpdateDateTime
        self.Currency = Currency
        self.AccountType = AccountType
        self.AccountSubType = AccountSubType
        self.AccountIndicator = AccountIndicator
        self.OnboardingType = OnboardingType
        self.Nickname = Nickname
        self.OpeningDate = OpeningDate
        self.SchemeName = SchemeName
        self.Identification = Identification

class DetalleConsent:
    def __init__(self, CreationDateTime, ExpirationDateTime, ConsentId, Status, Permissions):
        self.CreationDateTime = CreationDateTime
        self.ExpirationDateTime = ExpirationDateTime
        self.ConsentId = ConsentId
        self.Status = Status
        self.Permissions = Permissions

class DetalleTransaccion:
    def __init__(self, TransactionId, Status, BookingDateTime, TransactionInformation, Amount, Currency):
        self.TransactionId  = TransactionId
        self.Status  = Status
        self.BookingDateTime  = BookingDateTime
        self.TransactionInformation = TransactionInformation
        self.Amount  = Amount
        self.Currency  = Currency
