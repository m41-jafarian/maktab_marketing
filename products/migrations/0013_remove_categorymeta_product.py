# Generated by Django 3.1.4 on 2021-02-12 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_categorymeta_categorymetavalue'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymeta',
            name='product',
        ),
    ]
