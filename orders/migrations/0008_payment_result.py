# Generated by Django 3.1.4 on 2021-02-14 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_order_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='result',
            field=models.BooleanField(default=False, verbose_name='result'),
        ),
    ]
