# Generated by Django 3.2.5 on 2022-01-22 10:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20220122_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventbookings',
            name='time_schedule',
            field=models.CharField(max_length=30),
        ),
    ]
