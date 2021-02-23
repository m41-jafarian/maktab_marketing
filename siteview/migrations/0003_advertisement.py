# Generated by Django 3.1.4 on 2021-02-17 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteview', '0002_auto_20210117_1347'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advertisement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('subtitle', models.CharField(max_length=250, verbose_name='subtitle')),
                ('background', models.ImageField(upload_to='site/Advertisement', verbose_name='background')),
                ('action_text', models.CharField(max_length=50, verbose_name='action text')),
                ('action_url', models.URLField(default='http://127.0.0.1:8000', verbose_name='action url')),
            ],
            options={
                'verbose_name': 'Advertisement',
                'verbose_name_plural': 'Advertisements',
            },
        ),
    ]
