# Generated by Django 3.1.1 on 2020-09-25 22:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0003_cuentasusuario_cuenta_consent_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cuentasusuario',
            name='cuenta_proveedor',
        ),
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_currency',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Moneda'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_nickname',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='nickname de la cuenta'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_status',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Estatus'),
            preserve_default=False,
        ),
    ]
