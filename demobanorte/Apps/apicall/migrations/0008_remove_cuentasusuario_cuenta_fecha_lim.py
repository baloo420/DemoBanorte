# Generated by Django 3.1.1 on 2020-10-06 05:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0007_auto_20201005_2139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasusuario',
            name='cuenta_fecha_lim',
        ),
    ]