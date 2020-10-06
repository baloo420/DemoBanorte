# Generated by Django 3.1.1 on 2020-09-25 21:51

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0002_auto_20200925_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuentasusuario',
            name='cuenta_consent_id',
            field=models.CharField(default=django.utils.timezone.now, max_length=100, verbose_name='Id de consentimiento'),
            preserve_default=False,
        ),
    ]
