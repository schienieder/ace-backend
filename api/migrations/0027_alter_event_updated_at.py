# Generated by Django 4.0.2 on 2022-02-13 01:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_rename_event_budget_event_client_payment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='updated_at',
            field=models.DateField(default=datetime.date(2022, 2, 13)),
        ),
    ]