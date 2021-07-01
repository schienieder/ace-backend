# Generated by Django 3.2.4 on 2021-06-29 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='password',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='account',
            name='username',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='admin',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='admin',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='client',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='client',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='client',
            name='state_province',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='partner',
            name='city',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='partner',
            name='first_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='partner',
            name='last_name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='partner',
            name='state_province',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
