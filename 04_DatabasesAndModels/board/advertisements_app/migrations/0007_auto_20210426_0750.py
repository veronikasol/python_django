# Generated by Django 2.2 on 2021-04-26 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements_app', '0006_auto_20210426_0551'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advertisement',
            options={'ordering': ['title']},
        ),
        migrations.AlterModelTable(
            name='advertisement',
            table='Advertisements',
        ),
    ]
