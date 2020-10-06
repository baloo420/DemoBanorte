# Generated by Django 3.1.1 on 2020-10-06 17:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0013_auto_20201006_1149'),
    ]

    operations = [
        migrations.AddField(
            model_name='procesocta',
            name='proceso_cod_inst',
            field=models.CharField(default=django.utils.timezone.now, max_length=30, verbose_name='Codigo Institucion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cuentasusuario',
            name='cuenta_institucion',
            field=models.CharField(max_length=30, verbose_name='Institucion'),
        ),
    ]
