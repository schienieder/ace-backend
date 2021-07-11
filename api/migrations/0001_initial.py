# Generated by Django 3.2.4 on 2021-07-10 10:53

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=150)),
                ('role', models.CharField(max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('mobile_number', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('sex', models.IntegerField(blank=True, null=True)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=150)),
                ('state_province', models.CharField(blank=True, max_length=150)),
                ('postal_zip', models.IntegerField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EventBookings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of_event', models.CharField(max_length=55)),
                ('venue_name', models.CharField(max_length=150)),
                ('event_budget', models.IntegerField()),
                ('desired_date', models.DateField()),
                ('time_schedule', models.TimeField()),
                ('guests_no', models.IntegerField()),
                ('service_requirements', models.CharField(max_length=10)),
                ('beverages', models.CharField(max_length=15)),
                ('best_way_contact', models.CharField(max_length=20)),
                ('booked_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.client')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessPartner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('mobile_number', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('business_name', models.CharField(blank=True, max_length=255)),
                ('type_of_business', models.CharField(blank=True, max_length=150)),
                ('street_address', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=150)),
                ('state_province', models.CharField(blank=True, max_length=150)),
                ('postal_zip', models.IntegerField(blank=True, null=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('mobile_number', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=150, unique=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
