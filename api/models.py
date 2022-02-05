from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


def upload_to(instance, filename):
    now = timezone.now()
    milliseconds = now.microsecond
    return "posts/{milliseconds}{filename}".format(
        filename=filename, milliseconds=milliseconds
    )


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
    profile_image = models.ImageField(
        _("Image"),
        null=True,
        blank=True,
        upload_to=upload_to,
    )
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
    services_offered = models.TextField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-account"]

    def __str__(self):
        return self.first_name + " " + self.last_name


class EventBookings(models.Model):
    type_of_event = models.CharField(max_length=55)
    venue_name = models.CharField(max_length=150)
    event_budget = models.IntegerField(null=True, blank=True)
    desired_date = models.DateField()
    time_schedule = models.CharField(max_length=30)
    guests_no = models.IntegerField()
    status = models.CharField(max_length=10, default="Pending")
    booked_by = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.booked_by.first_name + " " + self.booked_by.last_name

    class Meta:
        ordering = ["desired_date"]


class Event(models.Model):
    event_name = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=250)
    venue_lat = models.DecimalField(max_digits=30, decimal_places=10, default=7.45)
    venue_long = models.DecimalField(max_digits=30, decimal_places=10, default=125.8)
    event_date = models.DateField()
    time_schedule = models.CharField(max_length=30)
    event_budget = models.IntegerField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ["event_date"]


class InterviewSchedule(models.Model):
    location = models.CharField(max_length=250)
    date = models.DateField()
    time = models.CharField(max_length=30)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    booking = models.ForeignKey(EventBookings, on_delete=models.CASCADE)

    def __str__(self):
        return self.client.first_name + " " + self.client.last_name

    class Meta:
        ordering = ["date"]


class AffiliationRequest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)
    task = models.CharField(max_length=150)
    task_status = models.CharField(max_length=20, default="On Going", blank="True")
    status = models.CharField(max_length=10, default="Pending", blank=True)
    created_at = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.event.event_name

    class Meta:
        ordering = ["-created_at"]


class Rating(models.Model):
    event_name = models.CharField(max_length=200)
    event_date = models.DateField()
    venue_rate = models.IntegerField()
    catering_rate = models.IntegerField()
    styling_rate = models.IntegerField()
    mc_rate = models.IntegerField()
    presentation_rate = models.IntegerField()
    courtesy_rate = models.IntegerField()

    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ["pk"]


class ClientRoom(models.Model):
    room_name = models.CharField(max_length=50)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name


class PartnerRoom(models.Model):
    room_name = models.CharField(max_length=50)
    partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)

    def __str__(self):
        return self.room_name


class GroupRoom(models.Model):
    room_name = models.CharField(max_length=50)
    room_key = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class ClientGroupRoom(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    group_room = models.ForeignKey(GroupRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_room.room_name


class PartnerGroupRoom(models.Model):
    partner = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)
    group_room = models.ForeignKey(GroupRoom, on_delete=models.CASCADE)

    def __str__(self):
        return self.group_room.room_name
