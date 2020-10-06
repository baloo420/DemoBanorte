# Generated by Django 3.1.1 on 2020-10-06 05:55

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0008_remove_cuentasusuario_cuenta_fecha_lim'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituciones',
            name='institucion_codigo',
            field=models.CharField(default=django.utils.timezone.now, max_length=10, verbose_name='codigo'),
            preserve_default=False,
        ),
    ]
