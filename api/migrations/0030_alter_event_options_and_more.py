# Generated by Django 4.0.2 on 2022-02-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_alter_event_updated_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['date_schedule']},
        ),
        migrations.RenameField(
            model_name='event',
            old_name='event_date',
            new_name='date_schedule',
        ),
        migrations.AlterField(
            model_name='event',
            name='updated_at',
            field=models.DateField(auto_now=True, null=True),
        ),
    ]