# Generated by Django 3.2.5 on 2021-08-07 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_goods', '0003_useraccount_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='status',
            field=models.CharField(choices=[('I', 'Initial'), ('S', 'Silver'), ('P', 'Platinum'), ('G', 'Gold')], default='Initial', max_length=10),
        ),
    ]
