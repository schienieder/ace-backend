# Generated by Django 3.2.5 on 2022-01-17 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20220117_2221'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='venue_lat',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='venue_long',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]