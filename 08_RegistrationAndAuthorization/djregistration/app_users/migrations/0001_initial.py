# Generated by Django 2.2 on 2021-05-20 08:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app_news', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, verbose_name='Телефон')),
                ('city', models.CharField(max_length=30, verbose_name='Город')),
                ('is_verified', models.BooleanField(default=False, verbose_name='Верифицирован?')),
                ('news', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='app_news.News', verbose_name='новость')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Profile',
            },
        ),
    ]