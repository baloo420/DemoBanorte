# Generated by Django 3.1.1 on 2020-10-07 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apicall', '0014_auto_20201006_1200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instituciones',
            name='institucion_codigo',
            field=models.CharField(max_length=25, verbose_name='codigo'),
        ),
        migrations.AlterField(
            model_name='procesocta',
            name='proceso_refresh_token',
            field=models.CharField(max_length=100, verbose_name='Refresh Token'),
        ),
    ]
