# Generated by Django 2.2 on 2021-05-21 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_news', '0002_news_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='Активна?'),
        ),
    ]
