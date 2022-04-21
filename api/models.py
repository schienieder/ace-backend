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


def upload_to_files(instance, filename):
    now = timezone.now()
    milliseconds = now.microsecond
    return "files/{milliseconds}{filename}".format(
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
    permit_profile = models.FileField(null=True, blank=True, upload_to=upload_to_files)
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
    venue_location = models.CharField(max_length=250, default="Tagum City")
    venue_name = models.CharField(max_length=250)
    venue_lat = models.DecimalField(max_digits=30, decimal_places=10, default=7.45)
    venue_long = models.DecimalField(max_digits=30, decimal_places=10, default=125.8)
    package_cost = models.IntegerField(default=0)
    client_payment = models.IntegerField()
    payment_status = models.CharField(max_length=20, default="Partially Paid")
    date_schedule = models.DateField()
    time_schedule = models.CharField(max_length=30)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.event_name

    class Meta:
        ordering = ["date_schedule"]


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
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)

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


# [1] FIRST IS MAKEMIGRATIONS & MIGRATE THE FF MODELS
# [2.1] WHENEVER A PARTNER OR CLIENT REGISTERS, CREATE A CHATROOM
# [2.2] ASSIGN CLIENT OR PARTNER USERNAME AS ROOM_KEY
# [3] DEFINE A ROOM_KEY WHEN CREATING A GROUP CHAT ROOM


class ChatRoom(models.Model):
    room_name = models.CharField(max_length=50)
    room_key = models.CharField(max_length=50)

    def __str__(self):
        return self.room_name


class RoomMember(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    member = models.CharField(max_length=150)  # THIS IS THE USERNAME OF THE USER

    def __str__(self):
        return self.room.room_name


class Chat(models.Model):
    content = models.CharField(max_length=1000)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.sender_name
