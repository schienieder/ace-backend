# Generated by Django 4.0.2 on 2022-04-29 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affiliationrequest',
            name='task',
        ),
    ]
