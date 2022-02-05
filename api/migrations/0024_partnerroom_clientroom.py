# Generated by Django 4.0.2 on 2022-02-04 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0023_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.businesspartner')),
            ],
        ),
        migrations.CreateModel(
            name='ClientRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.client')),
            ],
        ),
    ]
