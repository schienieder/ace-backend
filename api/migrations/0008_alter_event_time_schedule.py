# Generated by Django 3.2.5 on 2021-12-23 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_businesspartner_services_offered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='time_schedule',
            field=models.CharField(max_length=30),
        ),
    ]