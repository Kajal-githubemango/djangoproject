# Generated by Django 4.0.5 on 2023-02-23 17:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_alter_customer_dt'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
