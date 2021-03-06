# Generated by Django 3.1.4 on 2021-02-17 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteview', '0005_sitesetting'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sitesetting',
            options={'verbose_name': 'SiteSetting', 'verbose_name_plural': 'SiteSettings'},
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='section1',
            field=models.IntegerField(verbose_name='section1'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='section2',
            field=models.IntegerField(verbose_name='section2'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='section3',
            field=models.IntegerField(verbose_name='section3'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='section4',
            field=models.IntegerField(verbose_name='section4'),
        ),
        migrations.AlterField(
            model_name='sitesetting',
            name='section5',
            field=models.IntegerField(verbose_name='section5'),
        ),
    ]
