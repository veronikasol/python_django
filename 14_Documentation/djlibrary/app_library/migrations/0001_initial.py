# Generated by Django 2.2 on 2021-07-22 12:28

import app_library.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('surname', models.CharField(max_length=100, verbose_name='surname')),
                ('year_of_birth', models.PositiveSmallIntegerField(validators=[app_library.models.validate_year], verbose_name='date of birth')),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
                'ordering': ('surname',),
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='book name')),
                ('isbn', models.CharField(max_length=100, verbose_name='ISBN')),
                ('year_of_publish', models.PositiveSmallIntegerField(validators=[app_library.models.validate_year], verbose_name='date of publication')),
                ('num_of_pages', models.IntegerField(verbose_name='number of pages')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='app_library.Author', verbose_name='author')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
                'ordering': ('name',),
            },
        ),
    ]