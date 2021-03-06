# Generated by Django 3.1.1 on 2020-10-07 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cuentasUsuario',
            fields=[
                ('cuenta_id', models.AutoField(primary_key=True, serialize=False)),
                ('cuenta_numero', models.CharField(max_length=50, verbose_name='Numero de Cuenta')),
                ('cuenta_user', models.CharField(max_length=100, verbose_name='Usuario Banco')),
                ('cuenta_institucion', models.CharField(max_length=30, verbose_name='Institucion')),
                ('cuenta_nickname', models.CharField(max_length=100, verbose_name='nickname de la cuenta')),
                ('cuenta_currency', models.CharField(max_length=100, verbose_name='Moneda')),
                ('cuenta_status', models.CharField(max_length=100, verbose_name='Estatus')),
                ('cuenta_id_token', models.CharField(max_length=9999, verbose_name='Id token')),
                ('cuenta_scope', models.CharField(max_length=999, verbose_name='Scope')),
            ],
        ),
        migrations.CreateModel(
            name='instituciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion_id', models.CharField(max_length=30, verbose_name='Id')),
                ('institucion_nombre', models.CharField(max_length=50, verbose_name='Nombre')),
                ('institucion_tipo', models.CharField(max_length=30, verbose_name='Tipo')),
                ('institucion_codigo', models.CharField(max_length=25, verbose_name='codigo')),
            ],
        ),
        migrations.CreateModel(
            name='Parametros',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parametro_id', models.CharField(max_length=35, verbose_name='Id')),
                ('parametro_valor', models.CharField(max_length=99999, verbose_name='Valor')),
                ('parametro_proxi', models.CharField(max_length=100, verbose_name='Institucion')),
            ],
        ),
        migrations.CreateModel(
            name='procesocta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proceso_user', models.CharField(max_length=100, verbose_name='Usuario Banco')),
                ('proceso_token', models.CharField(max_length=99999, verbose_name='Token')),
                ('proceso_refresh_token', models.CharField(max_length=100, verbose_name='Refresh Token')),
                ('proceso_inst_inf', models.CharField(max_length=40, verbose_name='Proveedor de Informacion')),
                ('proceso_cod_inst', models.CharField(max_length=30, verbose_name='Codigo Institucion')),
            ],
        ),
    ]
