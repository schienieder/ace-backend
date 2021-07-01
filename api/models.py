from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Account(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=10)
    REQUIRED_FIELDS = ["password", "role"]


class Profile(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    sex = models.IntegerField(null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    street_address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=150, blank=True)
    state_province = models.CharField(max_length=150, blank=True)
    postal_zip = models.IntegerField(null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username


class BusinessPartner(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    mobile_number = models.CharField(max_length=150, unique=True, null=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return self.account.username


class BusinessProfile(models.Model):
    business_name = models.CharField(max_length=255, blank=True)
    type_of_business = models.CharField(max_length=150, blank=True)
    personal_profile = models.ForeignKey(BusinessPartner, on_delete=models.CASCADE)

    def __str__(self):
        return self.personal_profile.first_name + " " + self.personal_profile.last_name
