# Generated by Django 2.2 on 2021-07-17 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='ru_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='category'),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AddField(
            model_name='product',
            name='ru_name',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='product'),
        ),
    ]