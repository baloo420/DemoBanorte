# Generated by Django 3.1.1 on 2020-10-06 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0010_remove_cuentasusuario_cuenta_consent_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasusuario',
            name='cuenta_cliente',
        ),
    ]
