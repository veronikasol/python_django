# Generated by Django 2.2 on 2021-04-25 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements_app', '0003_auto_20210425_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='price',
            field=models.IntegerField(default=0, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='advertisement',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='количество просмотров'),
        ),
    ]