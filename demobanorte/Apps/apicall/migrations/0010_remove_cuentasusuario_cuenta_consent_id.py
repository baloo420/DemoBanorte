# Generated by Django 3.1.1 on 2020-10-06 06:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0009_instituciones_institucion_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasusuario',
            name='cuenta_consent_id',
        ),
    ]