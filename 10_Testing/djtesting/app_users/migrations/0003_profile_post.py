# Generated by Django 2.2 on 2021-06-29 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
        ('app_users', '0002_auto_20210628_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='post',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='app_blog.Post', verbose_name='публикация'),
        ),
    ]
