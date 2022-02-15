# Generated by Django 4.0.2 on 2022-02-13 01:40

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_grouproom_partnergrouproom_clientgrouproom'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='event_budget',
            new_name='client_payment',
        ),
        migrations.AddField(
            model_name='event',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='package_cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='payment_status',
            field=models.CharField(default='Partially Paid', max_length=20),
        ),
        migrations.AddField(
            model_name='event',
            name='updated_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='event',
            name='venue_location',
            field=models.CharField(default='Tagum City', max_length=250),
        ),
    ]
