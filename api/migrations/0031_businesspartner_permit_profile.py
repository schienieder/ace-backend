# Generated by Django 4.0.2 on 2022-02-18 09:19

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_alter_event_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='businesspartner',
            name='permit_profile',
            field=models.FileField(blank=True, null=True, upload_to=api.models.upload_to_files),
        ),
    ]
