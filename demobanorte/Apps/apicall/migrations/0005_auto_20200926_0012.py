# Generated by Django 3.1.1 on 2020-09-26 05:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0004_auto_20200925_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_cliente',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Cliente'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuentasusuario',
            name='cuenta_user',
            field=models.CharField(max_length=100, verbose_name='Usuario Banco'),
        ),
    ]
