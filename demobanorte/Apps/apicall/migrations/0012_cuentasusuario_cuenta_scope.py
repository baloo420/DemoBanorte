# Generated by Django 3.1.1 on 2020-10-06 06:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0011_remove_cuentasusuario_cuenta_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_scope',
            field=models.CharField(default=django.utils.timezone.now, max_length=999, verbose_name='Id token'),
            preserve_default=False,
        ),
    ]
