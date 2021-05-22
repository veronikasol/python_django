# Generated by Django 2.2 on 2021-05-19 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000, verbose_name='Заголовок новости')),
                ('content', models.TextField(verbose_name='Тескт новости')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='дата редактирования')),
                ('is_active', models.BooleanField(verbose_name='Активна?')),
            ],
            options={
                'db_table': 'News',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20, verbose_name='имя пользователя')),
                ('content', models.TextField(verbose_name='текст комментария')),
                ('news', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='app_news.News', verbose_name='новость')),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='пользователь')),
            ],
            options={
                'db_table': 'Comment',
            },
        ),
    ]