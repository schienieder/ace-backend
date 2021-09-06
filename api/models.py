from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=10)
    REQUIRED_FIELDS = ["password", "role"]


class Admin(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Client(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    sex = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state_province = models.CharField(max_length=150, blank=True)
    postal_zip = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-account"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class BusinessPartner(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=150, unique=True)
    business_name = models.CharField(max_length=255, blank=True)
    type_of_business = models.CharField(max_length=150, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state_province = models.CharField(max_length=150, blank=True)
    postal_zip = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-account"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class EventBookings(models.Model):
    type_of_event = models.CharField(max_length=55)
    venue_name = models.CharField(max_length=150)
    event_budget = models.IntegerField()
    desired_date = models.DateField()
    time_schedule = models.TimeField()
    guests_no = models.IntegerField()
    service_requirements = models.CharField(max_length=55)
    beverages = models.CharField(max_length=55)
    best_way_contact = models.CharField(max_length=55)
    booked_by = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.booked_by.first_name + " " + self.booked_by.last_name


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    venue = models.CharField(max_length=250)
    event_date = models.DateField()
    time_schedule = models.TimeField()
    event_budget = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name


class InterviewSchedule(models.Model):
    location = models.CharField(max_length=250)
    date = models.DateField()
    time = models.TimeField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    booking = models.ForeignKey(EventBookings, on_delete=models.CASCADE)

    def __str__(self):
        return self.client
