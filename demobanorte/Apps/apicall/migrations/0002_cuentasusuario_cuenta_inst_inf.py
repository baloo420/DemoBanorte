# Generated by Django 3.1.1 on 2020-10-07 17:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_inst_inf',
            field=models.CharField(default=django.utils.timezone.now, max_length=40, verbose_name='Proveedor de Informacion'),
            preserve_default=False,
        ),
    ]
