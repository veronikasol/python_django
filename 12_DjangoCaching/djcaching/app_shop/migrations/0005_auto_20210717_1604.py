# Generated by Django 2.2 on 2021-07-17 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_shop', '0004_offer_promo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='product',
        ),
        migrations.AddField(
            model_name='offer',
            name='product',
            field=models.ManyToManyField(to='app_shop.Product'),
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=300, max_digits=10, verbose_name='balance')),
                ('offer', models.ManyToManyField(to='app_shop.Offer')),
                ('promo', models.ManyToManyField(to='app_shop.Promo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
