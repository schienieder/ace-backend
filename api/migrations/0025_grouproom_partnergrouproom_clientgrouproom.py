# Generated by Django 4.0.2 on 2022-02-04 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_partnerroom_clientroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=50)),
                ('room_key', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerGroupRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.grouproom')),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.businesspartner')),
            ],
        ),
        migrations.CreateModel(
            name='ClientGroupRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.client')),
                ('group_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.grouproom')),
            ],
        ),
    ]
