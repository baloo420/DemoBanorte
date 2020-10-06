# Generated by Django 3.1.1 on 2020-09-23 05:03

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
                ('cuenta_numero', models.CharField(max_length=50, verbose_name='Usuario')),
                ('cuenta_user', models.CharField(max_length=100, verbose_name='Usuario')),
                ('cuenta_token', models.CharField(max_length=99999, verbose_name='Token')),
                ('cuenta_institucion', models.CharField(max_length=100, verbose_name='Institucion')),
                ('cuenta_fecha_lim', models.DateTimeField(verbose_name='Fecha Expiracion')),
            ],
        ),
        migrations.CreateModel(
            name='instituciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institucion_id', models.CharField(max_length=5, verbose_name='Usuario')),
                ('institucion_nombre', models.CharField(max_length=50, verbose_name='Usuario')),
                ('institucion_tipo', models.CharField(max_length=30, verbose_name='Usuario')),
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
    ]
