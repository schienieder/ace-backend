# Generated by Django 4.0.2 on 2022-04-01 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_chatroom_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatroom',
            name='owner',
        ),
    ]
